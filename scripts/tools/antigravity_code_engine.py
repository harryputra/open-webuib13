"""
title: Antigravity Code Engine
author: Antigravity Architect
description: Mesin pengembangan perangkat lunak otonom — eksekusi kode multi-bahasa, pencarian kode workspace-wide, manajemen dependensi, analisis kualitas, operasi Git, dan manajemen file dengan sandbox aman.
version: 3.0.0
"""

import os
import json
import subprocess
from datetime import datetime
from pydantic import BaseModel, Field


class Tools:
    class Valves(BaseModel):
        workspace_path: str = Field(
            default=os.environ.get("WORKSPACE_DIR", "/workspace"),
            description="Path ke direktori workspace utama di dalam container."
        )
        rag_path: str = Field(
            default="/file_rag",
            description="Path ke direktori RAG vault."
        )
        command_timeout: int = Field(
            default=120,
            description="Timeout dalam detik untuk eksekusi command."
        )
        max_output_length: int = Field(
            default=5000,
            description="Maksimum karakter output yang dikembalikan."
        )

    def __init__(self):
        self.valves = self.Valves()

    def _resolve_path(self, path: str) -> str:
        """Helper: resolve relative path ke absolute path."""
        path = path.replace("\\", "/")
        ws = self.valves.workspace_path.replace("\\", "/")
        rag = self.valves.rag_path.replace("\\", "/")

        if "E:/file_rag" in path or "/file_rag" in path:
            base = rag
            rel = path.replace("E:/file_rag", "").replace("/file_rag", "").strip("/")
        elif "E:/AntiGravityProject" in path:
            base = ws
            rel = path.replace("E:/AntiGravityProject", "").strip("/")
        else:
            base = ws
            rel = path.strip("/")

        full = os.path.normpath(os.path.join(base, rel))
        if not full.startswith(os.path.abspath(base)):
            raise PermissionError(f"Access denied: path outside {base}")
        return full

    async def list_files(self, path: str = ".", __event_emitter__=None) -> str:
        """
        Menampilkan daftar file dan folder dalam direktori workspace.

        :param path: Path relatif ke direktori (default: root workspace).
        :return: Daftar file/folder dalam format JSON.
        """
        try:
            full = self._resolve_path(path)
            items = []
            for name in sorted(os.listdir(full)):
                fp = os.path.join(full, name)
                is_dir = os.path.isdir(fp)
                size = os.path.getsize(fp) if not is_dir else None
                items.append({"name": name, "type": "dir" if is_dir else "file", "size": size})
            return json.dumps(items, indent=2)
        except Exception as e:
            return f"Error: {e}"

    async def read_file(self, file_path: str, __event_emitter__=None) -> str:
        """
        Membaca konten file dari workspace.

        :param file_path: Path relatif ke file yang akan dibaca.
        :return: Konten file sebagai string.
        """
        try:
            full = self._resolve_path(file_path)
            if not os.path.exists(full):
                return f"Error: File '{file_path}' tidak ditemukan."
            with open(full, "r", encoding="utf-8") as f:
                content = f.read()
            if len(content) > self.valves.max_output_length:
                content = content[:self.valves.max_output_length] + "\n\n[... file terpotong ...]"
            return content
        except Exception as e:
            return f"Error: {e}"

    async def write_file(self, file_path: str, content: str, __event_emitter__=None) -> str:
        """
        Menulis konten ke file di workspace. Membuat direktori parent otomatis.

        :param file_path: Path relatif ke file tujuan.
        :param content: Konten yang akan ditulis.
        :return: Pesan sukses atau error.
        """
        try:
            full = self._resolve_path(file_path)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, "w", encoding="utf-8") as f:
                f.write(content)
            return f"✅ File '{file_path}' berhasil ditulis ({len(content)} karakter)."
        except Exception as e:
            return f"Error: {e}"

    async def execute_code(
        self,
        code: str,
        language: str = "python",
        timeout: int = 60,
        __event_emitter__=None,
    ) -> str:
        """
        Mengeksekusi kode dalam bahasa pemrograman tertentu di dalam container.
        Mendukung Python, Bash/Shell, Node.js, dan command terminal umum.

        :param code: Kode sumber yang akan dieksekusi.
        :param language: Bahasa pemrograman — "python", "bash", "node", "shell".
        :param timeout: Timeout eksekusi dalam detik (default: 60, max: 300).
        :return: Output eksekusi (stdout + stderr + exit code).
        """
        if __event_emitter__:
            await __event_emitter__({"type": "status", "data": {"description": f"⚡ Mengeksekusi kode {language}...", "done": False}})

        timeout = min(max(5, timeout), 300)

        cmd_map = {
            "python": ["python3", "-c", code],
            "bash": ["bash", "-c", code],
            "shell": ["bash", "-c", code],
            "node": ["node", "-e", code],
        }

        cmd = cmd_map.get(language.lower())
        if not cmd:
            return f"Error: Bahasa '{language}' tidak didukung. Gunakan: python, bash, node."

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.valves.workspace_path,
            )
            output = ""
            if result.stdout:
                out = result.stdout[:self.valves.max_output_length]
                output += f"**STDOUT:**\n```\n{out}\n```\n\n"
            if result.stderr:
                err = result.stderr[:2000]
                output += f"**STDERR:**\n```\n{err}\n```\n\n"
            output += f"**Exit Code:** {result.returncode}"

            if __event_emitter__:
                status = "✅ Eksekusi berhasil!" if result.returncode == 0 else "⚠️ Eksekusi selesai dengan error."
                await __event_emitter__({"type": "status", "data": {"description": status, "done": True}})

            return output
        except subprocess.TimeoutExpired:
            return f"Error: Eksekusi timeout setelah {timeout} detik."
        except Exception as e:
            return f"Error: {e}"

    async def run_command(self, command: str, working_dir: str = "", __event_emitter__=None) -> str:
        """
        Mengeksekusi perintah terminal/shell di dalam container.
        Gunakan untuk menjalankan skrip, menginstall dependensi, mengelola file, dsb.

        :param command: Perintah shell yang akan dijalankan (contoh: "pip install requests", "ls -la").
        :param working_dir: Direktori kerja relatif (opsional, default: workspace root).
        :return: Output perintah beserta exit code.
        """
        if __event_emitter__:
            await __event_emitter__({"type": "status", "data": {"description": f"🖥️ Menjalankan: {command[:60]}...", "done": False}})

        try:
            cwd = self.valves.workspace_path
            if working_dir:
                cwd = self._resolve_path(working_dir)

            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.valves.command_timeout,
                cwd=cwd,
                executable="/bin/bash" if os.path.exists("/bin/bash") else None,
            )

            output = ""
            if result.stdout:
                out = result.stdout[:self.valves.max_output_length]
                output += f"**Output:**\n```\n{out}\n```\n\n"
            if result.stderr:
                err = result.stderr[:2000]
                output += f"**Errors:**\n```\n{err}\n```\n\n"
            output += f"**Exit Code:** {result.returncode}"

            if __event_emitter__:
                await __event_emitter__({"type": "status", "data": {"description": "✅ Perintah selesai.", "done": True}})

            return output
        except subprocess.TimeoutExpired:
            return f"Error: Perintah timeout setelah {self.valves.command_timeout} detik."
        except Exception as e:
            return f"Error: {e}"

    async def analyze_code_quality(
        self,
        code: str,
        language: str = "python",
        __event_emitter__=None,
    ) -> str:
        """
        Menganalisis kualitas kode — menghitung metrik kompleksitas, mendeteksi
        potensi masalah, dan memberikan rekomendasi perbaikan.

        :param code: Kode sumber yang akan dianalisis.
        :param language: Bahasa kode — "python" (saat ini didukung penuh).
        :return: Laporan analisis kualitas kode.
        """
        if __event_emitter__:
            await __event_emitter__({"type": "status", "data": {"description": "🔍 Menganalisis kualitas kode...", "done": False}})

        lines = code.split("\n")
        total_lines = len(lines)
        blank_lines = sum(1 for l in lines if not l.strip())
        comment_lines = sum(1 for l in lines if l.strip().startswith("#") or l.strip().startswith("//"))
        code_lines = total_lines - blank_lines - comment_lines

        report = "# 🔍 Laporan Analisis Kualitas Kode\n\n"
        report += f"| Metrik | Nilai |\n|:---|:---|\n"
        report += f"| Total Baris | {total_lines} |\n"
        report += f"| Baris Kode | {code_lines} |\n"
        report += f"| Baris Komentar | {comment_lines} |\n"
        report += f"| Baris Kosong | {blank_lines} |\n"
        report += f"| Rasio Komentar | {(comment_lines / max(code_lines, 1) * 100):.1f}% |\n\n"

        issues = []
        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                issues.append(f"Baris {i}: Terlalu panjang ({len(line)} karakter, max 120)")
            if "TODO" in line or "FIXME" in line or "HACK" in line:
                issues.append(f"Baris {i}: Ditemukan marker: {line.strip()[:80]}")
            if "import *" in line:
                issues.append(f"Baris {i}: Wildcard import terdeteksi")
            if "eval(" in line or "exec(" in line:
                issues.append(f"Baris {i}: ⚠️ Penggunaan eval/exec (risiko keamanan)")
            if "password" in line.lower() and "=" in line:
                issues.append(f"Baris {i}: ⚠️ Potensi hardcoded password")

        if language == "python":
            functions = [l.strip() for l in lines if l.strip().startswith("def ") or l.strip().startswith("async def ")]
            classes = [l.strip() for l in lines if l.strip().startswith("class ")]
            imports = [l.strip() for l in lines if l.strip().startswith("import ") or l.strip().startswith("from ")]

            report += f"## Struktur Kode (Python)\n\n"
            report += f"- **Fungsi**: {len(functions)}\n"
            report += f"- **Kelas**: {len(classes)}\n"
            report += f"- **Import**: {len(imports)}\n\n"

        if issues:
            report += f"## ⚠️ Masalah Ditemukan ({len(issues)})\n\n"
            for issue in issues[:20]:
                report += f"- {issue}\n"
        else:
            report += "## ✅ Tidak Ada Masalah Ditemukan\n"

        # Score
        score = 100
        score -= len(issues) * 5
        score -= max(0, (total_lines - 500)) // 100 * 2  # Penalty for very long files
        if comment_lines / max(code_lines, 1) < 0.05:
            score -= 10
        score = max(0, min(100, score))

        grade = "A" if score >= 90 else "B" if score >= 75 else "C" if score >= 60 else "D" if score >= 40 else "F"
        report += f"\n## 📊 Skor Kualitas: **{score}/100 ({grade})**\n"

        if __event_emitter__:
            await __event_emitter__({"type": "status", "data": {"description": f"✅ Analisis selesai — Skor: {score}/100 ({grade})", "done": True}})

        return report

    async def git_operations(
        self,
        action: str,
        repo_path: str = ".",
        args: str = "",
        __event_emitter__=None,
    ) -> str:
        """
        Melakukan operasi Git pada repository di workspace.
        Mendukung: status, log, diff, branch, add, commit, remote.

        :param action: Operasi Git — "status", "log", "diff", "branch", "add", "commit", "remote", "pull".
        :param repo_path: Path relatif ke repository (default: root workspace).
        :param args: Argumen tambahan (contoh: untuk commit: "pesan commit", untuk log: "-n 10").
        :return: Output dari operasi Git.
        """
        if __event_emitter__:
            await __event_emitter__({"type": "status", "data": {"description": f"🔀 Git {action}...", "done": False}})

        safe_actions = ["status", "log", "diff", "branch", "remote", "show", "stash"]
        write_actions = ["add", "commit", "pull", "push", "checkout", "merge"]

        if action not in safe_actions + write_actions:
            return f"Error: Operasi '{action}' tidak didukung."

        try:
            cwd = self._resolve_path(repo_path)
        except Exception:
            cwd = self.valves.workspace_path

        cmd = f"git {action}"
        if args:
            if action == "commit":
                cmd = f'git commit -m "{args}"'
            elif action == "log" and not args:
                cmd = "git log --oneline -n 15"
            else:
                cmd = f"git {action} {args}"
        elif action == "log":
            cmd = "git log --oneline -n 15"

        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True,
                timeout=30, cwd=cwd,
                executable="/bin/bash" if os.path.exists("/bin/bash") else None,
            )
            output = ""
            if result.stdout:
                output += result.stdout[:self.valves.max_output_length]
            if result.stderr:
                output += f"\n{result.stderr[:1000]}"

            if __event_emitter__:
                await __event_emitter__({"type": "status", "data": {"description": f"✅ Git {action} selesai.", "done": True}})

            return output.strip() or "(empty output)"
        except Exception as e:
            return f"Error: {e}"

    async def search_in_files(
        self,
        pattern: str,
        path: str = ".",
        file_types: str = "",
        case_sensitive: bool = False,
        max_results: int = 30,
        __event_emitter__=None,
    ) -> str:
        """
        Mencari pola teks atau regex di seluruh file dalam workspace.
        Sangat berguna untuk menemukan penggunaan fungsi, variabel, import,
        string, error message, atau pola kode tertentu di seluruh proyek.

        :param pattern: Pola pencarian (teks biasa atau regex).
        :param path: Path direktori untuk pencarian (default: seluruh workspace).
        :param file_types: Filter ekstensi file, dipisahkan koma (contoh: ".py,.js,.ts"). Kosongkan untuk semua file.
        :param case_sensitive: Jika True, pencarian case-sensitive.
        :param max_results: Jumlah maksimal hasil (default: 30).
        :return: Daftar file dan baris yang cocok dengan pola pencarian.
        """
        if __event_emitter__:
            await __event_emitter__({"type": "status", "data": {"description": f"🔍 Mencari '{pattern}' di workspace...", "done": False}})

        try:
            search_path = self._resolve_path(path)
        except Exception:
            search_path = self.valves.workspace_path

        results = []
        extensions = [e.strip().lower() for e in file_types.split(",") if e.strip()] if file_types else None
        skip_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', '.next', 'dist', 'build', '.egg-info'}

        import re as regex_module
        flags = 0 if case_sensitive else regex_module.IGNORECASE
        try:
            compiled = regex_module.compile(pattern, flags)
        except regex_module.error:
            compiled = regex_module.compile(regex_module.escape(pattern), flags)

        for root, dirs, files in os.walk(search_path):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            for fname in files:
                if extensions:
                    ext = os.path.splitext(fname)[1].lower()
                    if ext not in extensions:
                        continue

                fpath = os.path.join(root, fname)
                try:
                    if os.path.getsize(fpath) > 1_000_000:  # Skip >1MB
                        continue
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                        for line_num, line in enumerate(f, 1):
                            if compiled.search(line):
                                rel = os.path.relpath(fpath, search_path)
                                results.append({
                                    "file": rel.replace("\\", "/"),
                                    "line": line_num,
                                    "content": line.rstrip()[:200],
                                })
                                if len(results) >= max_results:
                                    break
                except (PermissionError, UnicodeDecodeError, OSError):
                    continue
                if len(results) >= max_results:
                    break
            if len(results) >= max_results:
                break

        output = f"# 🔍 Hasil Pencarian: `{pattern}`\n\n"
        output += f"**Path**: {search_path}\n"
        output += f"**Ditemukan**: {len(results)} hasil\n\n"

        if results:
            current_file = ""
            for r in results:
                if r['file'] != current_file:
                    current_file = r['file']
                    output += f"\n### 📄 {current_file}\n"
                output += f"- **L{r['line']}**: `{r['content']}`\n"
        else:
            output += "*Tidak ditemukan hasil yang cocok.*\n"

        if len(results) >= max_results:
            output += f"\n⚠️ Hasil dipotong di {max_results}. Gunakan filter file_types atau path spesifik.\n"

        if __event_emitter__:
            await __event_emitter__({"type": "status", "data": {"description": f"✅ Ditemukan {len(results)} hasil.", "done": True}})

        return output

    async def manage_dependencies(
        self,
        action: str = "list",
        packages: str = "",
        manager: str = "pip",
        working_dir: str = "",
        __event_emitter__=None,
    ) -> str:
        """
        Mengelola dependensi proyek — install, uninstall, list, freeze, atau update package.
        Mendukung pip (Python) dan npm (Node.js).

        :param action: Aksi — "list" (daftar package), "install" (pasang), "uninstall" (hapus), "freeze" (export requirements), "outdated" (cek update).
        :param packages: Nama package yang akan diinstall/uninstall, dipisahkan spasi (contoh: "flask sqlalchemy redis").
        :param manager: Package manager — "pip" atau "npm".
        :param working_dir: Direktori kerja relatif (opsional).
        :return: Output dari operasi manajemen dependensi.
        """
        if __event_emitter__:
            await __event_emitter__({"type": "status", "data": {"description": f"📦 {manager} {action}: {packages[:40]}...", "done": False}})

        try:
            cwd = self._resolve_path(working_dir) if working_dir else self.valves.workspace_path
        except Exception:
            cwd = self.valves.workspace_path

        cmd_map = {
            "pip": {
                "list": "pip list --format=columns",
                "install": f"pip install {packages}",
                "uninstall": f"pip uninstall -y {packages}",
                "freeze": "pip freeze",
                "outdated": "pip list --outdated --format=columns",
            },
            "npm": {
                "list": "npm list --depth=0",
                "install": f"npm install {packages}",
                "uninstall": f"npm uninstall {packages}",
                "freeze": "npm list --json",
                "outdated": "npm outdated",
            }
        }

        if manager not in cmd_map:
            return f"Error: Manager '{manager}' tidak didukung. Gunakan: pip, npm."
        if action not in cmd_map[manager]:
            return f"Error: Aksi '{action}' tidak valid. Gunakan: list, install, uninstall, freeze, outdated."
        if action in ["install", "uninstall"] and not packages:
            return "Error: Parameter 'packages' wajib diisi untuk install/uninstall."

        cmd = cmd_map[manager][action]

        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True,
                timeout=self.valves.command_timeout, cwd=cwd,
                executable="/bin/bash" if os.path.exists("/bin/bash") else None,
            )
            output = ""
            if result.stdout:
                out = result.stdout[:self.valves.max_output_length]
                output += f"**Output:**\n```\n{out}\n```\n\n"
            if result.stderr:
                err = result.stderr[:2000]
                output += f"**Log:**\n```\n{err}\n```\n\n"
            output += f"**Exit Code:** {result.returncode}"

            if __event_emitter__:
                status = "✅ Selesai!" if result.returncode == 0 else "⚠️ Ada error."
                await __event_emitter__({"type": "status", "data": {"description": f"{status}", "done": True}})

            return output
        except subprocess.TimeoutExpired:
            return f"Error: Timeout setelah {self.valves.command_timeout} detik."
        except Exception as e:
            return f"Error: {e}"
