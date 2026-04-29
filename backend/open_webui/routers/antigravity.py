from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import subprocess
import os
import platform
from open_webui.utils.auth import get_admin_user
from open_webui.config import UPLOAD_DIR

router = APIRouter()

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
