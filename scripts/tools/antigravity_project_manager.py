"""
title: Antigravity Project Manager
author: Antigravity Architect
description: Manajemen proyek otonom — scaffolding multi-template, pelacakan progress, health scanning, changelog generation, dan dokumentasi otomatis.
version: 3.0.0
"""

import os
import json
from datetime import datetime
from pydantic import BaseModel, Field


class Tools:
    class Valves(BaseModel):
        workspace_path: str = Field(
            default=os.environ.get("WORKSPACE_DIR", "/workspace"),
            description="Path ke direktori workspace utama."
        )
        projects_dir: str = Field(
            default="projects",
            description="Subdirektori untuk menyimpan proyek (relatif terhadap workspace)."
        )

    def __init__(self):
        self.valves = self.Valves()

    async def create_project_structure(
        self,
        name: str,
        template: str = "generic",
        description: str = "",
        __event_emitter__=None,
    ) -> str:
        """
        Membuat struktur folder proyek lengkap berdasarkan template.
        Template tersedia: generic, web-app, api-server, python-library, book-project, research-project.

        :param name: Nama proyek (akan menjadi nama folder utama).
        :param template: Template struktur — "generic", "web-app", "api-server", "python-library", "book-project", "research-project".
        :param description: Deskripsi singkat proyek.
        :return: Laporan struktur proyek yang berhasil dibuat.
        """
        if __event_emitter__:
            await __event_emitter__({"type": "status", "data": {"description": f"🏗️ Membuat proyek: {name}...", "done": False}})

        ws = self.valves.workspace_path.replace("\\", "/")
        base = os.path.join(ws, self.valves.projects_dir, name)

        templates = {
            "generic": {
                "dirs": ["src", "tests", "docs", "scripts", "config"],
                "files": {
                    "README.md": f"# {name}\n\n{description}\n\n## Getting Started\n\nTODO\n",
                    ".gitignore": "node_modules/\n__pycache__/\n*.pyc\n.env\n.venv/\ndist/\nbuild/\n",
                    "src/.gitkeep": "",
                    "tests/.gitkeep": "",
                    "docs/.gitkeep": "",
                }
            },
            "web-app": {
                "dirs": ["src/components", "src/pages", "src/styles", "src/utils", "src/assets", "public", "tests"],
                "files": {
                    "README.md": f"# {name}\n\n{description}\n\n## Setup\n```bash\nnpm install\nnpm run dev\n```\n",
                    "package.json": json.dumps({"name": name, "version": "1.0.0", "scripts": {"dev": "vite", "build": "vite build"}}, indent=2),
                    "src/index.html": f"<!DOCTYPE html>\n<html><head><title>{name}</title></head><body><div id='app'></div></body></html>\n",
                    ".gitignore": "node_modules/\ndist/\n.env\n",
                }
            },
            "api-server": {
                "dirs": ["app/routers", "app/models", "app/services", "app/utils", "app/middleware", "tests", "docs", "migrations"],
                "files": {
                    "README.md": f"# {name} API\n\n{description}\n\n## Setup\n```bash\npip install -r requirements.txt\nuvicorn app.main:app --reload\n```\n",
                    "requirements.txt": "fastapi\nuvicorn\npydantic\nsqlalchemy\n",
                    "app/__init__.py": "",
                    "app/main.py": f'from fastapi import FastAPI\n\napp = FastAPI(title="{name}")\n\n@app.get("/")\ndef root():\n    return {{"message": "Welcome to {name}"}}\n',
                    ".gitignore": "__pycache__/\n*.pyc\n.env\n.venv/\n",
                }
            },
            "python-library": {
                "dirs": [f"src/{name.replace('-','_')}", "tests", "docs", "examples"],
                "files": {
                    "README.md": f"# {name}\n\n{description}\n\n## Installation\n```bash\npip install {name}\n```\n",
                    "pyproject.toml": f'[project]\nname = "{name}"\nversion = "0.1.0"\ndescription = "{description}"\n',
                    f"src/{name.replace('-','_')}/__init__.py": f'"""{ name } - {description}"""\n__version__ = "0.1.0"\n',
                    "tests/__init__.py": "",
                    ".gitignore": "__pycache__/\n*.pyc\ndist/\nbuild/\n*.egg-info/\n",
                }
            },
            "book-project": {
                "dirs": ["chapters", "assets/images", "assets/diagrams", "references", "drafts", "exports"],
                "files": {
                    "README.md": f"# 📖 {name}\n\n{description}\n\n## Struktur\n- `chapters/` — Konten bab\n- `references/` — Referensi & sitasi\n- `exports/` — File ekspor (DOCX, EPUB)\n",
                    "outline.md": f"# Outline: {name}\n\n## Bab 1: [Judul]\n### 1.1 [Sub-bab]\n### 1.2 [Sub-bab]\n\n## Bab 2: [Judul]\n### 2.1 [Sub-bab]\n",
                    "chapters/.gitkeep": "",
                    "references/bibliography.md": "# Daftar Pustaka\n\n",
                    "progress.json": json.dumps({"title": name, "chapters": [], "status": "draft", "created": datetime.now().isoformat()}, indent=2),
                }
            },
            "research-project": {
                "dirs": ["literature", "data/raw", "data/processed", "analysis", "papers/drafts", "papers/figures", "notes"],
                "files": {
                    "README.md": f"# 🔬 {name}\n\n{description}\n\n## Struktur\n- `literature/` — Paper & referensi\n- `data/` — Dataset\n- `analysis/` — Analisis & notebook\n- `papers/` — Draf paper\n",
                    "notes/research_log.md": f"# Research Log: {name}\n\n## {datetime.now().strftime('%Y-%m-%d')}\n- Proyek dimulai\n- Topik: {description}\n",
                    "literature/bibliography.bib": "",
                    "progress.json": json.dumps({"title": name, "phase": "exploration", "tasks": [], "created": datetime.now().isoformat()}, indent=2),
                }
            },
        }

        tmpl = templates.get(template, templates["generic"])

        # Create directories
        created_dirs = []
        for d in tmpl["dirs"]:
            dp = os.path.join(base, d)
            os.makedirs(dp, exist_ok=True)
            created_dirs.append(d)

        # Create files
        created_files = []
        for fp, content in tmpl["files"].items():
            full = os.path.join(base, fp)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, "w", encoding="utf-8") as f:
                f.write(content)
            created_files.append(fp)

        report = f"# ✅ Proyek '{name}' Berhasil Dibuat\n\n"
        report += f"| Info | Detail |\n|:---|:---|\n"
        report += f"| **Nama** | {name} |\n"
        report += f"| **Template** | {template} |\n"
        report += f"| **Path** | `{base}` |\n"
        report += f"| **Folder** | {len(created_dirs)} |\n"
        report += f"| **File** | {len(created_files)} |\n\n"
        report += "## Struktur:\n```\n"
        report += f"{name}/\n"
        for d in sorted(created_dirs):
            report += f"  📁 {d}/\n"
        for fp in sorted(created_files):
            report += f"  📄 {fp}\n"
        report += "```\n"

        if __event_emitter__:
            await __event_emitter__({"type": "status", "data": {"description": f"✅ Proyek '{name}' berhasil dibuat!", "done": True}})

        return report

    async def track_progress(
        self,
        project_name: str,
        action: str = "view",
        task_description: str = "",
        task_status: str = "pending",
        __event_emitter__=None,
    ) -> str:
        """
        Melacak progress proyek — menambah, memperbarui, atau melihat status tugas.

        :param project_name: Nama proyek yang akan dilacak.
        :param action: Aksi — "view" (lihat progress), "add" (tambah task), "update" (update status task).
        :param task_description: Deskripsi tugas (untuk action add/update).
        :param task_status: Status tugas — "pending", "in-progress", "done", "blocked".
        :return: Laporan progress proyek.
        """
        ws = self.valves.workspace_path.replace("\\", "/")
        progress_file = os.path.join(ws, self.valves.projects_dir, project_name, "progress.json")

        try:
            if os.path.exists(progress_file):
                with open(progress_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
            else:
                data = {"title": project_name, "tasks": [], "created": datetime.now().isoformat()}

            if action == "add" and task_description:
                data["tasks"].append({
                    "id": len(data["tasks"]) + 1,
                    "description": task_description,
                    "status": task_status,
                    "created": datetime.now().isoformat(),
                    "updated": datetime.now().isoformat(),
                })
                with open(progress_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                return f"✅ Task ditambahkan: '{task_description}' [{task_status}]"

            elif action == "update" and task_description:
                for task in data["tasks"]:
                    if task_description.lower() in task["description"].lower():
                        task["status"] = task_status
                        task["updated"] = datetime.now().isoformat()
                        with open(progress_file, "w", encoding="utf-8") as f:
                            json.dump(data, f, indent=2)
                        return f"✅ Task diupdate: '{task['description']}' → [{task_status}]"
                return f"Task '{task_description}' tidak ditemukan."

            elif action == "view":
                tasks = data.get("tasks", [])
                if not tasks:
                    return f"📋 Proyek '{project_name}' belum memiliki task."

                report = f"# 📋 Progress: {project_name}\n\n"
                total = len(tasks)
                done = sum(1 for t in tasks if t["status"] == "done")
                report += f"**Progress**: {done}/{total} ({(done/max(total,1)*100):.0f}%)\n\n"
                report += f"| # | Task | Status | Updated |\n|:---|:---|:---|:---|\n"
                for t in tasks:
                    icon = {"pending": "⏳", "in-progress": "🔄", "done": "✅", "blocked": "🚫"}.get(t["status"], "❓")
                    report += f"| {t['id']} | {t['description']} | {icon} {t['status']} | {t.get('updated', 'N/A')[:10]} |\n"
                return report

            return "Aksi tidak valid. Gunakan: view, add, update."
        except Exception as e:
            return f"Error: {e}"

    async def generate_documentation(
        self,
        project_name: str,
        doc_type: str = "readme",
        __event_emitter__=None,
    ) -> str:
        """
        Menghasilkan dokumentasi otomatis berdasarkan analisis struktur proyek.

        :param project_name: Nama proyek di workspace.
        :param doc_type: Jenis dokumentasi — "readme", "structure", "api-doc".
        :return: Dokumentasi yang dihasilkan dalam format Markdown.
        """
        if __event_emitter__:
            await __event_emitter__({"type": "status", "data": {"description": f"📝 Menghasilkan dokumentasi {doc_type}...", "done": False}})

        ws = self.valves.workspace_path.replace("\\", "/")
        project_path = os.path.join(ws, self.valves.projects_dir, project_name)

        if not os.path.exists(project_path):
            return f"Error: Proyek '{project_name}' tidak ditemukan di {project_path}"

        # Scan project structure
        def scan_dir(path, prefix="", depth=0, max_depth=4):
            if depth > max_depth:
                return ""
            result = ""
            try:
                items = sorted(os.listdir(path))
                dirs = [i for i in items if os.path.isdir(os.path.join(path, i)) and not i.startswith(".")]
                files = [i for i in items if os.path.isfile(os.path.join(path, i)) and not i.startswith(".")]
                for d in dirs:
                    result += f"{prefix}📁 {d}/\n"
                    result += scan_dir(os.path.join(path, d), prefix + "  ", depth + 1)
                for f in files:
                    size = os.path.getsize(os.path.join(path, f))
                    result += f"{prefix}📄 {f} ({size} bytes)\n"
            except Exception:
                pass
            return result

        tree = scan_dir(project_path)

        if doc_type == "structure":
            doc = f"# 🗂️ Struktur Proyek: {project_name}\n\n```\n{tree}```\n"
        elif doc_type == "readme":
            doc = f"# {project_name}\n\n"
            doc += f"## Struktur Proyek\n\n```\n{tree}```\n\n"
            doc += f"## Cara Memulai\n\nTODO: Tambahkan instruksi setup\n\n"
            doc += f"## Kontribusi\n\nTODO: Tambahkan panduan kontribusi\n\n"
            doc += f"---\n*Generated by Antigravity Project Manager — {datetime.now().strftime('%Y-%m-%d')}*\n"
        elif doc_type == "api-doc":
            # Scan for Python files with route definitions
            doc = f"# 📡 API Documentation: {project_name}\n\n"
            doc += "TODO: Auto-scan route files for API endpoints\n\n"
            doc += f"## Struktur\n```\n{tree}```\n"
        else:
            doc = f"Tipe dokumen '{doc_type}' tidak didukung."

        if __event_emitter__:
            await __event_emitter__({"type": "status", "data": {"description": "✅ Dokumentasi selesai!", "done": True}})

        return doc

    async def scan_project_health(
        self,
        project_name: str,
        __event_emitter__=None,
    ) -> str:
        """
        Melakukan audit kesehatan proyek secara otomatis — mendeteksi file
        yang hilang, folder kosong, potensi masalah konfigurasi, dan memberikan
        skor kesehatan beserta rekomendasi perbaikan.

        :param project_name: Nama proyek di workspace.
        :return: Laporan kesehatan proyek dengan skor dan rekomendasi.
        """
        if __event_emitter__:
            await __event_emitter__({"type": "status", "data": {"description": f"🏥 Scanning kesehatan proyek '{project_name}'...", "done": False}})

        ws = self.valves.workspace_path.replace("\\", "/")
        project_path = os.path.join(ws, self.valves.projects_dir, project_name)

        if not os.path.exists(project_path):
            return f"Error: Proyek '{project_name}' tidak ditemukan."

        score = 100
        issues = []
        good = []

        # Check README
        if os.path.exists(os.path.join(project_path, "README.md")):
            readme_size = os.path.getsize(os.path.join(project_path, "README.md"))
            if readme_size > 200:
                good.append("README.md ada dan cukup detail")
            else:
                issues.append("README.md terlalu singkat (< 200 bytes)")
                score -= 10
        else:
            issues.append("README.md tidak ditemukan")
            score -= 20

        # Check .gitignore
        if os.path.exists(os.path.join(project_path, ".gitignore")):
            good.append(".gitignore ada")
        else:
            issues.append(".gitignore tidak ditemukan")
            score -= 10

        # Check for tests
        has_tests = False
        for root, dirs, files in os.walk(project_path):
            if 'tests' in dirs or 'test' in dirs or '__tests__' in dirs:
                has_tests = True
                break
            for f in files:
                if f.startswith('test_') or f.endswith('_test.py') or f.endswith('.test.js'):
                    has_tests = True
                    break
        if has_tests:
            good.append("Folder/file testing ditemukan")
        else:
            issues.append("Tidak ada tests — tambahkan unit tests")
            score -= 15

        # Check for empty directories
        empty_dirs = []
        for root, dirs, files in os.walk(project_path):
            if not dirs and not files:
                rel = os.path.relpath(root, project_path)
                empty_dirs.append(rel)
        if empty_dirs:
            issues.append(f"{len(empty_dirs)} folder kosong: {', '.join(empty_dirs[:5])}")
            score -= 5

        # Count files and lines
        total_files = 0
        total_lines = 0
        file_types = {}
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', '__pycache__', '.venv'}]
            for f in files:
                total_files += 1
                ext = os.path.splitext(f)[1].lower()
                file_types[ext] = file_types.get(ext, 0) + 1
                try:
                    fp = os.path.join(root, f)
                    if os.path.getsize(fp) < 500_000:
                        with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
                            total_lines += sum(1 for _ in fh)
                except Exception:
                    pass

        # Check for config files
        config_files = ['package.json', 'pyproject.toml', 'setup.py', 'requirements.txt', 'Makefile', 'docker-compose.yml']
        found_configs = [c for c in config_files if os.path.exists(os.path.join(project_path, c))]
        if found_configs:
            good.append(f"Config files: {', '.join(found_configs)}")

        # Check for docs
        if os.path.exists(os.path.join(project_path, "docs")):
            good.append("Folder docs/ ada")
        else:
            issues.append("Tidak ada folder docs/")
            score -= 5

        score = max(0, min(100, score))
        grade = "A" if score >= 90 else "B" if score >= 75 else "C" if score >= 60 else "D" if score >= 40 else "F"

        report = f"# 🏥 Health Report: {project_name}\n\n"
        report += f"## Skor: **{score}/100 ({grade})**\n\n"
        report += f"| Metrik | Nilai |\n|:---|:---|\n"
        report += f"| Total File | {total_files} |\n"
        report += f"| Total Baris Kode | {total_lines:,} |\n"
        report += f"| Tipe File | {len(file_types)} jenis |\n\n"

        if file_types:
            report += "### Distribusi File\n\n"
            for ext, count in sorted(file_types.items(), key=lambda x: -x[1])[:10]:
                report += f"- `{ext or '(no ext)'}`: {count} file\n"
            report += "\n"

        if good:
            report += "### ✅ Baik\n\n"
            for g in good:
                report += f"- {g}\n"
            report += "\n"

        if issues:
            report += "### ⚠️ Perlu Perbaikan\n\n"
            for iss in issues:
                report += f"- {iss}\n"
            report += "\n"

        if __event_emitter__:
            await __event_emitter__({"type": "status", "data": {"description": f"✅ Health scan selesai — Skor: {score}/100 ({grade})", "done": True}})

        return report

    async def generate_changelog(
        self,
        project_name: str,
        num_entries: int = 20,
        __event_emitter__=None,
    ) -> str:
        """
        Menghasilkan changelog otomatis dari riwayat Git commit proyek.
        Mengelompokkan commit berdasarkan tipe (feat, fix, docs, dll)
        dan menghasilkan format changelog yang rapi.

        :param project_name: Nama proyek di workspace.
        :param num_entries: Jumlah commit terakhir yang diproses (default: 20).
        :return: Changelog terstruktur dalam format Markdown.
        """
        import subprocess

        if __event_emitter__:
            await __event_emitter__({"type": "status", "data": {"description": f"📝 Generating changelog dari Git...", "done": False}})

        ws = self.valves.workspace_path.replace("\\", "/")
        project_path = os.path.join(ws, self.valves.projects_dir, project_name)

        if not os.path.exists(project_path):
            return f"Error: Proyek '{project_name}' tidak ditemukan."

        try:
            result = subprocess.run(
                f"git log --oneline --format='%h|%s|%an|%ai' -n {num_entries}",
                shell=True, capture_output=True, text=True, timeout=15, cwd=project_path,
                executable="/bin/bash" if os.path.exists("/bin/bash") else None,
            )
            if result.returncode != 0:
                return f"Error: Bukan git repository atau git error: {result.stderr[:200]}"

            lines = [l.strip() for l in result.stdout.strip().split("\n") if l.strip()]
            if not lines:
                return "Tidak ada commit ditemukan."

            # Parse and categorize
            categories = {"feat": [], "fix": [], "docs": [], "refactor": [], "style": [], "test": [], "chore": [], "other": []}

            for line in lines:
                parts = line.split("|", 3)
                if len(parts) >= 2:
                    hash_id = parts[0].strip("'")
                    msg = parts[1] if len(parts) > 1 else ""
                    author = parts[2] if len(parts) > 2 else ""
                    date = parts[3][:10] if len(parts) > 3 else ""

                    categorized = False
                    for cat in ["feat", "fix", "docs", "refactor", "style", "test", "chore"]:
                        if msg.lower().startswith(f"{cat}:") or msg.lower().startswith(f"{cat}("):
                            categories[cat].append({"hash": hash_id, "msg": msg, "author": author, "date": date})
                            categorized = True
                            break
                    if not categorized:
                        categories["other"].append({"hash": hash_id, "msg": msg, "author": author, "date": date})

            changelog = f"# 📋 Changelog: {project_name}\n\n"
            changelog += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"

            labels = {
                "feat": "🚀 Features", "fix": "🐛 Bug Fixes", "docs": "📚 Documentation",
                "refactor": "♻️ Refactoring", "style": "💅 Styling", "test": "🧪 Tests",
                "chore": "🔧 Chores", "other": "📦 Other"
            }

            for cat, label in labels.items():
                if categories[cat]:
                    changelog += f"## {label}\n\n"
                    for c in categories[cat]:
                        changelog += f"- `{c['hash']}` {c['msg']}"
                        if c['date']:
                            changelog += f" ({c['date']})"
                        changelog += "\n"
                    changelog += "\n"

            if __event_emitter__:
                await __event_emitter__({"type": "status", "data": {"description": f"✅ Changelog selesai! {len(lines)} commit diproses.", "done": True}})

            return changelog

        except Exception as e:
            return f"Error: {e}"
