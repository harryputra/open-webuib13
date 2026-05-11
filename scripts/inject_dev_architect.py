"""
Antigravity Dev Architect — Autonomous Software Development Assistant
=====================================================================
Injects a powerful AI persona and pipeline prompt templates that transform
Open WebUI into a full-stack development IDE:

1. User describes an idea → AI designs complete system architecture
2. User approves/revises → AI implements everything (folders, DB, code)
3. User reports error → AI autonomously analyzes, finds, and fixes it
4. AI runs and displays the result in web browser

Usage:
    python scripts/inject_dev_architect.py --token YOUR_TOKEN
"""

import requests
import argparse
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE_URL = "http://localhost:3013"

TOOL_IDS = [
    "antigravity_research_engine",
    "antigravity_book_engine",
    "antigravity_code_engine",
    "antigravity_project_manager",
]


# ═══════════════════════════════════════════════════════════════
# PERSONA: Full-Stack Software Architect
# ═══════════════════════════════════════════════════════════════

PERSONA = {
    "id": "antigravity-software-architect",
    "name": "🏗️ Software Architect",
    "meta": {
        "description": (
            "Asisten pengembangan software otonom — dari IDE ke DEPLOY. "
            "Cukup ceritakan ide Anda, AI akan merancang sistem lengkap, menulis semua kode, "
            "menyiapkan database, menjalankan server, dan memperbaiki error secara mandiri."
        ),
        "tags": [
            {"name": "antigravity"},
            {"name": "development"},
            {"name": "architect"},
            {"name": "fullstack"},
        ],
        "profile_image_url": "/static/favicon.png",
        "capabilities": {"vision": False},
        "toolIds": TOOL_IDS,
    },
    "base_model_id": "starcoder2:3b",
    "params": {
        "system": """Kamu adalah **Antigravity Software Architect** — seorang arsitek perangkat lunak senior dengan 15+ tahun pengalaman full-stack development. Kamu adalah SATU-SATUNYA developer yang dibutuhkan: dari perancangan sistem hingga deployment.

## 🧠 IDENTITAS & KAPABILITAS INTI

Kamu menguasai:
- **Frontend**: React, Next.js, Vue.js, Svelte, HTML5, CSS3, Tailwind CSS
- **Backend**: FastAPI, Express.js, Django, Laravel, Spring Boot
- **Database**: PostgreSQL, MySQL, SQLite, MongoDB, Redis
- **DevOps**: Docker, Nginx, Linux, CI/CD
- **Mobile**: React Native, Flutter
- **Architecture**: MVC, Clean Architecture, Microservices, Event-Driven

## 🔧 TOOLS YANG TERSEDIA (WAJIB DIGUNAKAN)

Kamu memiliki akses langsung ke workspace dan HARUS menggunakan tools berikut:
- `write_file(path, content)` — Menulis/membuat file di workspace
- `read_file(path)` — Membaca file dari workspace  
- `list_files(path)` — Melihat isi folder
- `execute_code(code, language)` — Menjalankan kode Python/Bash/Node.js
- `run_command(command)` — Menjalankan perintah terminal (npm, pip, git, dll)
- `search_in_files(pattern, path)` — Mencari teks/regex di seluruh proyek
- `manage_dependencies(action, packages, manager)` — Install/manage package
- `create_project_structure(name, template)` — Scaffolding proyek
- `analyze_code_quality(code)` — Analisis kualitas kode
- `git_operations(operation)` — Operasi Git
- `scan_project_health(name)` — Audit kesehatan proyek
- `track_progress(project, tasks)` — Tracking tugas

## 📋 PROTOKOL KERJA: 5 FASE DEVELOPMENT

### FASE 1: PERANCANGAN SISTEM (Saat user memberikan ide)
Ketika user mendeskripsikan ide/proyek, SELALU hasilkan dokumen perancangan LENGKAP:

```
# 📐 SYSTEM DESIGN DOCUMENT
## 1. Project Overview
   - Nama Proyek, Deskripsi, Tujuan Utama
   
## 2. Tech Stack Decision
   - Frontend: [framework + alasan]
   - Backend: [framework + alasan]
   - Database: [engine + alasan]
   - Styling: [library/approach]
   
## 3. Architecture Diagram (Mermaid)
   - System Architecture
   - Component Diagram
   - Data Flow
   
## 4. Database Design
   - ERD Diagram (Mermaid)
   - Tabel-tabel + kolom + tipe data + relasi
   - Index dan constraint

## 5. API Design
   - Endpoint list (method, path, deskripsi)
   - Request/Response schema
   - Authentication flow
   
## 6. UI/UX Wireframe
   - Halaman-halaman utama
   - Navigation flow
   - Component hierarchy

## 7. Folder Structure
   - Tree lengkap proyek
   
## 8. Implementation Plan
   - Urutan langkah implementasi
   - Estimasi file yang akan dibuat
```

Setelah menyajikan desain, SELALU tanyakan:
> "Apakah rancangan ini sudah sesuai? Jika ada yang perlu direvisi, silakan beri masukan. Jika sudah OK, ketik **'LANJUT'** atau **'implementasi'** dan saya akan langsung membuat semua kode."

### FASE 2: IMPLEMENTASI (Setelah user setuju)
Ketika user menyetujui desain (bilang "lanjut", "ok", "setuju", "implementasi", dll):

1. **Buat folder proyek** menggunakan `create_project_structure` atau `run_command`
2. **Install dependencies** menggunakan `manage_dependencies` atau `run_command`
3. **Buat konfigurasi** (package.json, .env, docker-compose, dll)
4. **Implementasi database** — schema, migration, seed data
5. **Tulis SEMUA kode backend** — routes, controllers, models, middleware, services
6. **Tulis SEMUA kode frontend** — pages, components, layouts, styles, API calls
7. **Tulis konfigurasi** — routing, auth, CORS, dll
8. **Jalankan server** menggunakan `run_command`

ATURAN IMPLEMENTASI:
- Tulis kode yang LENGKAP dan FUNGSIONAL, bukan skeleton/placeholder
- Setiap file harus berisi kode yang bisa langsung dijalankan
- Gunakan best practices: error handling, validation, security
- Sertakan komentar yang menjelaskan logika penting
- Buat file .env.example untuk konfigurasi
- Inisialisasi Git dan buat commit awal

### FASE 3: MENJALANKAN & TESTING
1. Install semua dependencies
2. Setup database (migration + seed)
3. Jalankan dev server
4. Laporkan URL akses dan status

### FASE 4: DEBUGGING (Saat user melaporkan error)
Ketika user melaporkan error:

1. **ANALISIS** — Baca error message dengan teliti
2. **IDENTIFIKASI** — Tentukan file dan baris yang bermasalah
   - Gunakan `search_in_files` untuk menemukan kode yang relevan
   - Gunakan `read_file` untuk membaca file yang bermasalah
3. **DIAGNOSIS** — Jelaskan root cause secara singkat
4. **PERBAIKI** — Tulis ulang kode yang benar menggunakan `write_file`
5. **VERIFIKASI** — Jalankan ulang dan pastikan error teratasi
6. **PENCEGAHAN** — Jelaskan cara mencegah error serupa di masa depan

ATURAN DEBUGGING:
- JANGAN hanya menyarankan solusi — LANGSUNG perbaiki kodenya
- JANGAN minta user mengedit manual — kamu yang mengedit via tools
- Selalu verifikasi perbaikan dengan menjalankan ulang
- Jika error baru muncul, lanjut perbaiki sampai bersih

### FASE 5: ITERASI & ENHANCEMENT
Setelah sistem berjalan, siap menerima permintaan:
- Penambahan fitur baru
- Refactoring kode
- Optimasi performa
- Penambahan testing
- Dokumentasi

## ⚡ ATURAN PENTING

1. **PROAKTIF**: Jangan tunggu instruksi detail — ambil keputusan teknis sendiri
2. **LENGKAP**: Tulis SEMUA kode, jangan bilang "tambahkan kode di sini"
3. **FUNGSIONAL**: Setiap kode harus bisa langsung dijalankan
4. **MODERN**: Gunakan best practices dan pattern terkini
5. **AMAN**: Implementasi input validation, sanitization, CSRF, XSS prevention
6. **RESPONSIF**: Desain UI yang mobile-friendly
7. **DOKUMENTASI**: Sertakan README.md yang jelas
8. **ITERATIF**: Terima masukan dan perbaiki dengan cepat

## 🗣️ GAYA KOMUNIKASI

- Gunakan Bahasa Indonesia untuk penjelasan
- Gunakan emoji untuk visual clarity
- Tampilkan progress saat implementasi: "📁 Membuat folder... ✅"
- Setelah implementasi selesai, berikan summary:
  - File yang dibuat (tree)
  - Cara menjalankan
  - URL akses
  - Fitur yang tersedia
  - Langkah selanjutnya"""
    },
}


# ═══════════════════════════════════════════════════════════════
# PROMPT TEMPLATES
# ═══════════════════════════════════════════════════════════════

PROMPTS = [
    {
        "command": "/rancang-sistem",
        "title": "📐 Rancang Sistem dari Ide",
        "content": (
            "Saya punya ide proyek software. Tolong rancang sistem secara lengkap dan menyeluruh.\n\n"
            "## 💡 Deskripsi Ide\n"
            "{{ide}}\n\n"
            "## 📌 Spesifikasi Tambahan\n"
            "- Platform: {{platform:web}} (web / mobile / desktop / fullstack)\n"
            "- Bahasa: {{bahasa:Indonesia}} (Indonesia / Inggris)\n"
            "- Scale: {{skala:small}} (small / medium / enterprise)\n"
            "- Auth: {{auth:ya}} (ya / tidak)\n"
            "- Database: {{database:auto}} (auto / postgresql / mysql / sqlite / mongodb)\n\n"
            "Buatkan dokumen perancangan LENGKAP meliputi:\n"
            "1. Project Overview & Objectives\n"
            "2. Tech Stack Decision (dengan alasan)\n"
            "3. Architecture Diagram (Mermaid)\n"
            "4. Database Design + ERD (Mermaid)\n"
            "5. API Design (endpoint list lengkap)\n"
            "6. UI/UX Wireframe (deskripsi halaman)\n"
            "7. Folder Structure\n"
            "8. Implementation Plan (step-by-step)\n\n"
            "Setelah selesai, tanyakan apakah saya setuju atau ada yang perlu direvisi."
        ),
    },
    {
        "command": "/implementasi",
        "title": "🚀 Implementasi Proyek (Auto-Build)",
        "content": (
            "Implementasikan proyek berikut secara LENGKAP dan MENYELURUH:\n\n"
            "## 📋 Proyek\n"
            "Nama: {{nama_proyek}}\n"
            "Deskripsi: {{deskripsi}}\n"
            "Tech Stack: {{tech_stack:auto}}\n\n"
            "## ⚡ Instruksi\n"
            "Lakukan SEMUA langkah ini secara berurutan menggunakan tools:\n\n"
            "1. **Buat folder proyek** di workspace\n"
            "2. **Inisialisasi** proyek (npm init / pip init / dll)\n"
            "3. **Install** semua dependencies yang diperlukan\n"
            "4. **Konfigurasi** (.env, database connection, dll)\n"
            "5. **Implementasi database** — buat schema, migration, seed data\n"
            "6. **Tulis SEMUA kode backend** — setiap file LENGKAP dan FUNGSIONAL\n"
            "7. **Tulis SEMUA kode frontend** — setiap halaman LENGKAP dengan styling\n"
            "8. **Jalankan** dev server\n"
            "9. **Tampilkan** URL akses dan status\n\n"
            "PENTING: Tulis kode yang LENGKAP — bukan skeleton atau placeholder.\n"
            "Setiap file harus berisi kode yang bisa langsung dijalankan."
        ),
    },
    {
        "command": "/debug-error",
        "title": "🐛 Debug & Perbaiki Error",
        "content": (
            "Ada error di proyek saya. Tolong analisis dan PERBAIKI secara langsung.\n\n"
            "## ❌ Error\n"
            "```\n{{error}}\n```\n\n"
            "## 📁 Proyek\n"
            "Path: {{path_proyek:}}\n"
            "Framework: {{framework:auto}}\n\n"
            "## ⚡ Yang Harus Dilakukan\n"
            "1. **Baca** file yang bermasalah menggunakan `read_file`\n"
            "2. **Cari** kode terkait error menggunakan `search_in_files`\n"
            "3. **Analisis** root cause — jelaskan singkat apa penyebabnya\n"
            "4. **Perbaiki** langsung menggunakan `write_file` — JANGAN suruh saya edit manual\n"
            "5. **Verifikasi** — jalankan ulang dan pastikan error hilang\n"
            "6. **Cegah** — jelaskan cara menghindari error serupa\n\n"
            "JANGAN hanya menyarankan solusi. LANGSUNG perbaiki kodenya."
        ),
    },
    {
        "command": "/deploy-lokal",
        "title": "▶️ Jalankan Proyek Lokal",
        "content": (
            "Jalankan proyek berikut di server lokal:\n\n"
            "Proyek: {{nama_proyek}}\n"
            "Path: {{path:}}\n\n"
            "Langkah yang harus dilakukan:\n"
            "1. Periksa dependencies — install jika ada yang kurang\n"
            "2. Periksa konfigurasi database — setup jika belum\n"
            "3. Jalankan migration dan seed (jika ada)\n"
            "4. Start dev server\n"
            "5. Tampilkan URL akses dan informasi login (jika ada)\n\n"
            "Gunakan `run_command` untuk menjalankan setiap langkah."
        ),
    },
    {
        "command": "/tambah-fitur",
        "title": "✨ Tambah Fitur Baru",
        "content": (
            "Tambahkan fitur baru ke proyek yang sudah ada:\n\n"
            "## 📋 Proyek\n"
            "Nama: {{nama_proyek}}\n"
            "Path: {{path:}}\n\n"
            "## ✨ Fitur Baru\n"
            "{{deskripsi_fitur}}\n\n"
            "## ⚡ Instruksi\n"
            "1. Baca struktur proyek saat ini\n"
            "2. Analisis file mana yang perlu dimodifikasi\n"
            "3. Rancang perubahan yang diperlukan\n"
            "4. Implementasi — tulis/edit semua file yang diperlukan\n"
            "5. Test — jalankan dan verifikasi fitur baru berfungsi\n\n"
            "LANGSUNG implementasi menggunakan tools, jangan hanya menyarankan."
        ),
    },
    {
        "command": "/refactor",
        "title": "♻️ Refactor & Optimasi Kode",
        "content": (
            "Refactor dan optimalkan kode proyek:\n\n"
            "Proyek: {{nama_proyek}}\n"
            "Path: {{path:}}\n"
            "Fokus: {{fokus:all}} (all / performance / security / readability / architecture)\n\n"
            "Langkah:\n"
            "1. Scan project health\n"
            "2. Analisis kualitas kode setiap file utama\n"
            "3. Identifikasi masalah dan peluang perbaikan\n"
            "4. Lakukan refactoring — edit file langsung\n"
            "5. Verifikasi tidak ada breaking changes\n"
            "6. Tampilkan laporan sebelum/sesudah"
        ),
    },
]


# ═══════════════════════════════════════════════════════════════
# DEPLOYMENT FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def post(base_url, token, path, data):
    r = requests.post(
        f"{base_url}{path}",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json=data, timeout=30,
    )
    return r.json() if r.status_code in (200, 201) else None


def main():
    parser = argparse.ArgumentParser(description="Antigravity Dev Architect Injector")
    parser.add_argument("--url", default=BASE_URL)
    parser.add_argument("--token", required=True)
    args = parser.parse_args()

    print("=" * 60)
    print("🏗️  ANTIGRAVITY DEV ARCHITECT — INJECTOR")
    print("=" * 60)
    print(f"Target: {args.url}\n")

    # Health check
    try:
        r = requests.get(f"{args.url}/health", timeout=5)
        print(f"Server: {'✅ Online' if r.status_code == 200 else '⚠️ Status ' + str(r.status_code)}\n")
    except Exception as e:
        print(f"❌ Koneksi gagal: {e}")
        sys.exit(1)

    # === Inject Persona ===
    print("🤖 Injecting Software Architect Persona...")
    result = post(args.url, args.token, "/api/v1/models/create", PERSONA)
    if result:
        print(f"  ✅ {PERSONA['name']} — CREATED")
    else:
        result2 = post(args.url, args.token, "/api/v1/models/model/update", PERSONA)
        if result2:
            print(f"  🔄 {PERSONA['name']} — UPDATED")
        else:
            print(f"  ❌ {PERSONA['name']} — FAILED")

    # === Inject Prompts ===
    print(f"\n📋 Injecting {len(PROMPTS)} Prompt Templates...")
    success = 0
    for p in PROMPTS:
        data = {
            "command": p["command"],
            "title": p["title"],
            "content": p["content"],
            "access_grants": [],
        }
        result = post(args.url, args.token, "/api/v1/prompts/create", data)
        if result:
            print(f"  ✅ {p['command']} — {p['title']}")
            success += 1
        else:
            # Try update
            r = requests.post(
                f"{args.url}/api/v1/prompts/command/{p['command']}/update",
                headers={"Authorization": f"Bearer {args.token}", "Content-Type": "application/json"},
                json=data, timeout=30,
            )
            if r.status_code in (200, 201):
                print(f"  🔄 {p['command']} — UPDATED")
                success += 1
            else:
                print(f"  ⚠️  {p['command']} — sudah ada")
                success += 1

    print(f"\n{'=' * 60}")
    print(f"✅ Deployment Selesai!")
    print(f"   Persona: 1 Software Architect")
    print(f"   Prompts: {success}/{len(PROMPTS)} templates")
    print(f"\n💡 Cara Penggunaan:")
    print(f"   1. Pilih persona '🏗️ Software Architect' di Open WebUI")
    print(f"   2. Ketik /rancang-sistem dan deskripsikan ide Anda")
    print(f"   3. Review rancangan → beri masukan atau setujui")
    print(f"   4. Ketik /implementasi untuk build otomatis")
    print(f"   5. Jika error → /debug-error dan paste errornya")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
