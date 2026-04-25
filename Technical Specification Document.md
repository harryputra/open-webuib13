# Technical Specification Document - Antigravity Zenith IDE

## 🌌 Project Overview
Antigravity Zenith adalah transformasi Open WebUI menjadi sebuah "AI-Powered Research Command Center" yang memiliki IDE terintegrasi, manajemen file system langsung, dan sistem pembaruan cerdas.

## 🛠️ Tech Stack Consistency
- **Frontend**: Vanilla JavaScript (ES6+), CSS3 (Glassmorphism), HTML5.
- **Backend**: FastAPI (Python), Docker, Shell Scripting (Bash/PowerShell).
- **Storage**: Local Workspace at `E:\file_rag` (Host) mapped to `/file_rag` (Container).

## 🏗️ Core Architectures
### 1. Antigravity Zenith IDE (v1.0)
- **Floating UI**: Menggunakan teknik overlay dengan `backdrop-filter: blur` untuk pengalaman premium.
- **Explorer**: Mendukung navigasi folder rekursif dengan sinkronisasi path otomatis antara UI dan API.
- **Editor**: Textarea berbasis monospaced font dengan dukungan operasi Read/Write real-time.

### 2. Smart Safe Update System
- **Version Control**: Melakukan komparasi versi lokal via `/api/config` dengan versi terbaru di GitHub `open-webui/open-webui`.
- **Master Patcher**: Skrip otomatis yang menjamin semua kustomisasi (UI Injections, API Routes) dipulihkan setelah proses update Docker selesai.

### 3. Workspace FS API
- **Endpoint List**:
  - `GET /api/v1/workspace/fs/list?path=...` : Mengambil daftar file/folder.
  - `GET /api/v1/workspace/fs/read?path=...` : Membaca konten file.
  - `POST /api/v1/workspace/fs/write?path=...` : Menulis konten ke file (JSON body).

## 📑 Completed Features (Changelog)
- [feat] Initial Zenith IDE UI Integration.
- [feat] Folder navigation support in IDE Explorer.
- [feat] Save functionality with JSON Body support in backend.
- [fix] Router priority fix in `main.py` to prevent SPA routing conflicts.
- [feat] Smart Version Checking for Safe Update.

## 🧪 Testing Methodology
- **Integrasi Manual**: Pengujian langsung rute API menggunakan `curl` dan verifikasi visual pada browser (Hard Refresh).
- **Consistency Check**: Memastikan file `main.py` tidak memiliki syntax error setelah injeksi rute baru menggunakan skrip `rebuild_imports.py`.

## 🔮 Roadmap (In Progress)
- **System Analyst Expert Mode**: AI persona khusus untuk perancangan sistem dengan tombol interaktif Revisi/Eksekusi.
- **Auto-Coding Engine**: Otomatisasi penulisan file berdasarkan blueprint yang disetujui.

---
*Last Updated: 2026-04-25 by Antigravity Architect*
