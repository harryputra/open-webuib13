from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import subprocess
import os
import platform
import re
import shutil
import tempfile
import time
from open_webui.utils.auth import get_admin_user, get_verified_user
from open_webui.config import UPLOAD_DIR

router = APIRouter()


# ----------------------------------------------------------------------
# Existing endpoints (run / save-preview)
# ----------------------------------------------------------------------

class RunRequest(BaseModel):
    path: str

@router.post("/run")
async def run_locally(request: RunRequest, user=Depends(get_admin_user)):
    try:
        path = request.path
        # Safety check: Ensure path is within E:\file_rag or workspace
        # For this specialized system, we allow local execution by admin
        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail="File not found")

        if platform.system() == "Windows":
            # Using start command to open file with default app
            subprocess.Popen(['start', '', path], shell=True)
        elif platform.system() == "Darwin":
            subprocess.Popen(['open', path])
        else:
            subprocess.Popen(['xdg-open', path])

        return {"status": "success", "message": f"Running {path} locally"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/save-preview")
async def save_preview(request: dict, user=Depends(get_admin_user)):
    try:
        content = request.get("content")
        filename = request.get("filename", "index.html")
        # Menggunakan folder di dalam workspace agar tidak tercecer
        base_dir = os.getcwd()
        folder = request.get("folder", os.path.join(base_dir, "projects", "live_preview"))

        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

        full_path = os.path.join(folder, filename)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        return {"status": "success", "path": full_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------------------------------------------------
# Marp Slide Generator
# ----------------------------------------------------------------------

SLIDES_DIR = os.path.join(os.getcwd(), "projects", "marp_slides")
SAFE_NAME_RE = re.compile(r"^[A-Za-z0-9._\- ]+$")


def _slides_dir() -> str:
    os.makedirs(SLIDES_DIR, exist_ok=True)
    return SLIDES_DIR


def _safe_filename(filename: str, default_ext: str = ".md") -> str:
    name = (filename or "").strip()
    if not name:
        raise HTTPException(status_code=400, detail="Filename is required")
    # strip any directory components
    name = os.path.basename(name)
    if not SAFE_NAME_RE.match(name):
        raise HTTPException(
            status_code=400,
            detail="Invalid filename. Use letters, numbers, dot, dash, underscore, space.",
        )
    if not os.path.splitext(name)[1]:
        name += default_ext
    return name


def _resolve_inside(base: str, filename: str) -> str:
    """Join filename to base and verify the result stays inside base."""
    full = os.path.realpath(os.path.join(base, filename))
    base_real = os.path.realpath(base)
    if not (full == base_real or full.startswith(base_real + os.sep)):
        raise HTTPException(status_code=400, detail="Path traversal not allowed")
    return full


class MarpSaveRequest(BaseModel):
    filename: str
    content: str


class MarpExportRequest(BaseModel):
    filename: Optional[str] = None  # nama file output (tanpa ekstensi diizinkan)
    content: str
    format: str  # 'pdf' | 'pptx' | 'html' | 'png'


@router.get("/marp/list")
async def marp_list(user=Depends(get_verified_user)):
    folder = _slides_dir()
    items = []
    try:
        for name in sorted(os.listdir(folder)):
            full = os.path.join(folder, name)
            if os.path.isfile(full) and name.lower().endswith((".md", ".markdown")):
                stat = os.stat(full)
                items.append(
                    {
                        "filename": name,
                        "size": stat.st_size,
                        "modified_at": int(stat.st_mtime),
                    }
                )
    except FileNotFoundError:
        pass
    return {"items": items, "folder": folder}


@router.get("/marp/load")
async def marp_load(filename: str, user=Depends(get_verified_user)):
    folder = _slides_dir()
    safe = _safe_filename(filename)
    full = _resolve_inside(folder, safe)
    if not os.path.exists(full):
        raise HTTPException(status_code=404, detail="Slide file not found")
    with open(full, "r", encoding="utf-8") as f:
        content = f.read()
    return {"filename": safe, "content": content, "path": full}


@router.post("/marp/save")
async def marp_save(req: MarpSaveRequest, user=Depends(get_verified_user)):
    folder = _slides_dir()
    safe = _safe_filename(req.filename)
    full = _resolve_inside(folder, safe)
    with open(full, "w", encoding="utf-8") as f:
        f.write(req.content or "")
    stat = os.stat(full)
    return {
        "status": "success",
        "filename": safe,
        "path": full,
        "size": stat.st_size,
        "modified_at": int(stat.st_mtime),
    }


@router.delete("/marp/delete")
async def marp_delete(filename: str, user=Depends(get_verified_user)):
    folder = _slides_dir()
    safe = _safe_filename(filename)
    full = _resolve_inside(folder, safe)
    if not os.path.exists(full):
        raise HTTPException(status_code=404, detail="Slide file not found")
    os.remove(full)
    return {"status": "success", "filename": safe}


def _resolve_marp_cli() -> Optional[List[str]]:
    """Locate the Marp CLI command. Returns argv prefix or None."""
    direct = shutil.which("marp")
    if direct:
        return [direct]
    npx = shutil.which("npx") or shutil.which("npx.cmd")
    if npx:
        return [npx, "--yes", "@marp-team/marp-cli@latest"]
    return None


@router.post("/marp/export")
async def marp_export(req: MarpExportRequest, user=Depends(get_verified_user)):
    fmt = (req.format or "").lower()
    if fmt not in {"pdf", "pptx", "html", "png"}:
        raise HTTPException(
            status_code=400, detail="format must be pdf, pptx, html, or png"
        )

    cli = _resolve_marp_cli()
    if cli is None:
        raise HTTPException(
            status_code=503,
            detail=(
                "Marp CLI not found. Install Node.js and run "
                "'npm install -g @marp-team/marp-cli', or ensure 'npx' is on PATH."
            ),
        )

    base_name = _safe_filename(req.filename or f"slides_{int(time.time())}.md")
    stem, _ = os.path.splitext(base_name)
    out_name = f"{stem}.{fmt}"

    workdir = tempfile.mkdtemp(prefix="marp_")
    try:
        in_path = os.path.join(workdir, base_name)
        out_path = os.path.join(workdir, out_name)
        with open(in_path, "w", encoding="utf-8") as f:
            f.write(req.content or "")

        argv = cli + [
            f"--{fmt}",
            "--allow-local-files",
            "-o",
            out_path,
            in_path,
        ]
        try:
            proc = subprocess.run(
                argv,
                capture_output=True,
                text=True,
                timeout=120,
                cwd=workdir,
            )
        except FileNotFoundError as e:
            raise HTTPException(
                status_code=503, detail=f"Marp CLI launch failed: {e}"
            )
        except subprocess.TimeoutExpired:
            raise HTTPException(status_code=504, detail="Marp CLI timed out")

        if proc.returncode != 0 or not os.path.exists(out_path):
            raise HTTPException(
                status_code=500,
                detail=f"Marp CLI failed: {proc.stderr or proc.stdout}".strip(),
            )

        # Move output into the slides folder so the user can access it later.
        final_dir = _slides_dir()
        final_path = _resolve_inside(final_dir, out_name)
        shutil.copyfile(out_path, final_path)

        media_types = {
            "pdf": "application/pdf",
            "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            "html": "text/html",
            "png": "image/png",
        }
        return FileResponse(
            final_path,
            media_type=media_types[fmt],
            filename=out_name,
        )
    finally:
        shutil.rmtree(workdir, ignore_errors=True)
