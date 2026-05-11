"""
title: Antigravity Presenter Engine
author: Antigravity Architect
description: Mesin presentasi & live-preview otonom — generate slide Marp dari outline, simpan/list/load/export ke PDF/PPTX/HTML/PNG, scaffold landing page HTML untuk live preview. Cocok untuk dosen yang butuh bikin materi kuliah cepat.
version: 1.0.0
"""

import os
import re
import json
import shutil
import subprocess
import tempfile
import time
from typing import Optional, List
from pydantic import BaseModel, Field


SAFE_NAME_RE = re.compile(r"^[A-Za-z0-9._\- ]+$")


class Tools:
    class Valves(BaseModel):
        slides_dir: str = Field(
            default=os.environ.get(
                "ANTIGRAVITY_SLIDES_DIR",
                os.path.join(os.getcwd(), "projects", "marp_slides"),
            ),
            description="Folder penyimpanan deck slide Marp (.md). Default mengikuti router antigravity.",
        )
        preview_dir: str = Field(
            default=os.environ.get(
                "ANTIGRAVITY_PREVIEW_DIR",
                os.path.join(os.getcwd(), "projects", "live_preview"),
            ),
            description="Folder penyimpanan HTML live preview.",
        )
        marp_timeout: int = Field(
            default=180,
            description="Timeout (detik) untuk eksekusi Marp CLI saat export.",
        )
        default_theme: str = Field(
            default="default",
            description="Theme Marp default ('default', 'gaia', 'uncover').",
        )

    def __init__(self):
        self.valves = self.Valves()

    def _safe_filename(self, filename: str, default_ext: str = ".md") -> str:
        name = (filename or "").strip()
        if not name:
            raise ValueError("Filename wajib diisi")
        name = os.path.basename(name)
        if not SAFE_NAME_RE.match(name):
            raise ValueError(
                "Nama file tidak valid. Gunakan huruf, angka, titik, strip, underscore, atau spasi."
            )
        if not os.path.splitext(name)[1]:
            name += default_ext
        return name

    def _resolve_inside(self, base: str, filename: str) -> str:
        os.makedirs(base, exist_ok=True)
        full = os.path.realpath(os.path.join(base, filename))
        base_real = os.path.realpath(base)
        if not (full == base_real or full.startswith(base_real + os.sep)):
            raise PermissionError("Path traversal tidak diizinkan")
        return full

    def _resolve_marp_cli(self) -> Optional[List[str]]:
        direct = shutil.which("marp")
        if direct:
            return [direct]
        npx = shutil.which("npx") or shutil.which("npx.cmd")
        if npx:
            return [npx, "--yes", "@marp-team/marp-cli@latest"]
        return None

    # ------------------------------------------------------------------
    # SLIDE OPERATIONS
    # ------------------------------------------------------------------

    async def generate_slide_deck(
        self,
        title: str,
        sections: List[str],
        filename: Optional[str] = None,
        theme: Optional[str] = None,
        author: Optional[str] = None,
        __event_emitter__=None,
    ) -> str:
        """
        Generate slide deck Marp lengkap dari judul + daftar isi section, lalu simpan sebagai file .md.
        Setiap section bisa berupa string biasa (jadi judul slide) atau format "Judul Slide | konten body".
        Pisahkan multi-paragraf dalam body dengan dua newline.

        :param title: Judul utama presentasi (dipakai di slide cover).
        :param sections: Daftar isi slide. Contoh: ["Pendahuluan | Apa itu Laravel?", "Routing | Definisi route di routes/web.php"].
        :param filename: Nama file output. Otomatis dibuat dari title kalau kosong.
        :param theme: Tema Marp ('default', 'gaia', 'uncover').
        :param author: Nama pemateri (muncul di footer slide cover).
        :return: JSON berisi path file dan jumlah slide.
        """
        try:
            theme = theme or self.valves.default_theme
            if not filename:
                slug = re.sub(r"[^A-Za-z0-9]+", "_", title)[:60].strip("_")
                filename = f"{slug or 'untitled'}_{int(time.time())}.md"
            safe = self._safe_filename(filename)
            full = self._resolve_inside(self.valves.slides_dir, safe)

            front = (
                "---\n"
                "marp: true\n"
                f"theme: {theme}\n"
                "paginate: true\n"
                "size: 16:9\n"
                "---\n\n"
            )
            cover_footer = f"\n\n_{author}_" if author else ""
            cover = f"# {title}{cover_footer}\n\n---\n\n"

            slides = []
            for idx, item in enumerate(sections, 1):
                if "|" in item:
                    head, body = item.split("|", 1)
                    head = head.strip()
                    body = body.strip()
                else:
                    head = item.strip()
                    body = ""
                slides.append(f"## {head}\n\n{body}".rstrip())

            content = front + cover + "\n\n---\n\n".join(slides) + "\n"
            with open(full, "w", encoding="utf-8") as f:
                f.write(content)

            return json.dumps(
                {
                    "status": "success",
                    "filename": safe,
                    "path": full,
                    "slide_count": len(sections) + 1,
                    "size": os.path.getsize(full),
                    "next_step": (
                        "Gunakan export_slide_deck() untuk render ke PDF/PPTX/HTML/PNG."
                    ),
                },
                ensure_ascii=False,
                indent=2,
            )
        except Exception as e:
            return f"Error: {e}"

    async def list_slide_decks(self, __event_emitter__=None) -> str:
        """
        Tampilkan semua deck slide Marp yang sudah disimpan.

        :return: JSON list berisi filename, ukuran, dan waktu modifikasi.
        """
        try:
            folder = self.valves.slides_dir
            os.makedirs(folder, exist_ok=True)
            items = []
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
            return json.dumps({"folder": folder, "items": items}, ensure_ascii=False, indent=2)
        except Exception as e:
            return f"Error: {e}"

    async def read_slide_deck(self, filename: str, __event_emitter__=None) -> str:
        """
        Baca isi mentah file slide Marp (.md).

        :param filename: Nama file deck slide yang ingin dibaca.
        :return: Isi file dalam string.
        """
        try:
            safe = self._safe_filename(filename)
            full = self._resolve_inside(self.valves.slides_dir, safe)
            if not os.path.exists(full):
                return f"Error: File '{safe}' tidak ditemukan."
            with open(full, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Error: {e}"

    async def save_slide_deck(
        self,
        filename: str,
        content: str,
        __event_emitter__=None,
    ) -> str:
        """
        Simpan/replace isi file slide Marp secara langsung. Pakai untuk edit deck yang sudah ada
        atau menyimpan markdown Marp custom yang Anda susun sendiri.

        :param filename: Nama file (.md akan ditambah otomatis kalau belum ada).
        :param content: Isi penuh markdown Marp (termasuk front-matter --- marp: true ---).
        :return: JSON status simpan.
        """
        try:
            safe = self._safe_filename(filename)
            full = self._resolve_inside(self.valves.slides_dir, safe)
            with open(full, "w", encoding="utf-8") as f:
                f.write(content or "")
            return json.dumps(
                {
                    "status": "success",
                    "filename": safe,
                    "path": full,
                    "size": os.path.getsize(full),
                },
                ensure_ascii=False,
                indent=2,
            )
        except Exception as e:
            return f"Error: {e}"

    async def export_slide_deck(
        self,
        filename: str,
        format: str = "pdf",
        __event_emitter__=None,
    ) -> str:
        """
        Render deck Marp ke file output (PDF/PPTX/HTML/PNG) menggunakan Marp CLI.
        Wajib jalankan generate_slide_deck() atau save_slide_deck() lebih dulu.

        :param filename: Nama file deck Marp source (.md).
        :param format: Format output: 'pdf', 'pptx', 'html', atau 'png'.
        :return: JSON path file output yang berhasil dibuat.
        """
        try:
            fmt = (format or "").lower()
            if fmt not in {"pdf", "pptx", "html", "png"}:
                return "Error: format harus pdf, pptx, html, atau png."

            cli = self._resolve_marp_cli()
            if cli is None:
                return (
                    "Error: Marp CLI tidak ditemukan. Install via "
                    "'npm install -g @marp-team/marp-cli' atau pastikan 'npx' ada di PATH."
                )

            safe_in = self._safe_filename(filename)
            src = self._resolve_inside(self.valves.slides_dir, safe_in)
            if not os.path.exists(src):
                return f"Error: Source deck '{safe_in}' tidak ada. Generate dulu via generate_slide_deck()."

            stem = os.path.splitext(safe_in)[0]
            out_name = f"{stem}.{fmt}"
            out_path = self._resolve_inside(self.valves.slides_dir, out_name)

            workdir = tempfile.mkdtemp(prefix="marp_tool_")
            try:
                tmp_in = os.path.join(workdir, safe_in)
                tmp_out = os.path.join(workdir, out_name)
                shutil.copyfile(src, tmp_in)
                argv = cli + [
                    f"--{fmt}",
                    "--allow-local-files",
                    "-o",
                    tmp_out,
                    tmp_in,
                ]
                proc = subprocess.run(
                    argv,
                    capture_output=True,
                    text=True,
                    timeout=self.valves.marp_timeout,
                    cwd=workdir,
                )
                if proc.returncode != 0 or not os.path.exists(tmp_out):
                    err = (proc.stderr or proc.stdout or "").strip()[:1000]
                    return f"Error: Marp CLI gagal export. {err}"
                shutil.copyfile(tmp_out, out_path)
            finally:
                shutil.rmtree(workdir, ignore_errors=True)

            return json.dumps(
                {
                    "status": "success",
                    "format": fmt,
                    "source": safe_in,
                    "output_filename": out_name,
                    "output_path": out_path,
                    "size": os.path.getsize(out_path),
                },
                ensure_ascii=False,
                indent=2,
            )
        except subprocess.TimeoutExpired:
            return "Error: Marp CLI timeout. Coba kurangi jumlah slide atau gambar."
        except Exception as e:
            return f"Error: {e}"

    async def delete_slide_deck(self, filename: str, __event_emitter__=None) -> str:
        """
        Hapus file slide deck (.md atau hasil export).

        :param filename: Nama file yang ingin dihapus.
        :return: JSON status hapus.
        """
        try:
            safe = self._safe_filename(filename)
            full = self._resolve_inside(self.valves.slides_dir, safe)
            if not os.path.exists(full):
                return f"Error: File '{safe}' tidak ditemukan."
            os.remove(full)
            return json.dumps({"status": "success", "filename": safe}, ensure_ascii=False)
        except Exception as e:
            return f"Error: {e}"

    # ------------------------------------------------------------------
    # LIVE PREVIEW (HTML)
    # ------------------------------------------------------------------

    async def save_html_preview(
        self,
        content: str,
        filename: str = "index.html",
        __event_emitter__=None,
    ) -> str:
        """
        Simpan HTML ke folder live preview agar bisa langsung di-render di browser.
        Cocok untuk demo cepat: landing page, prototipe UI, atau dashboard sederhana.

        :param content: Isi penuh dokumen HTML.
        :param filename: Nama file output (default index.html).
        :return: JSON path file dan URL akses.
        """
        try:
            safe = self._safe_filename(filename, default_ext=".html")
            full = self._resolve_inside(self.valves.preview_dir, safe)
            with open(full, "w", encoding="utf-8") as f:
                f.write(content or "")
            return json.dumps(
                {
                    "status": "success",
                    "filename": safe,
                    "path": full,
                    "size": os.path.getsize(full),
                    "hint": (
                        "File tersimpan. Buka path-nya langsung di browser, "
                        "atau gunakan tool antigravity_code_engine untuk men-serve folder ini."
                    ),
                },
                ensure_ascii=False,
                indent=2,
            )
        except Exception as e:
            return f"Error: {e}"

    async def list_html_previews(self, __event_emitter__=None) -> str:
        """
        Tampilkan semua file HTML yang ada di folder live preview.

        :return: JSON list filename + ukuran.
        """
        try:
            folder = self.valves.preview_dir
            os.makedirs(folder, exist_ok=True)
            items = []
            for name in sorted(os.listdir(folder)):
                full = os.path.join(folder, name)
                if os.path.isfile(full) and name.lower().endswith((".html", ".htm")):
                    items.append({"filename": name, "size": os.path.getsize(full)})
            return json.dumps({"folder": folder, "items": items}, ensure_ascii=False, indent=2)
        except Exception as e:
            return f"Error: {e}"
