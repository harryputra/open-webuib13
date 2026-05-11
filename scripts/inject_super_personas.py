"""
Antigravity Super Tools — Persona & Prompt Seeder
===================================================
Inject specialized AI Personas and Prompt Templates for Research, Book Writing,
and Software Development superpowers into Open WebUI.

Usage:
    python scripts/inject_super_personas.py --token YOUR_TOKEN
"""

import requests
import argparse
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

TOKEN_DEFAULT = ""
BASE_URL_DEFAULT = "http://localhost:3013"


def post(base_url, token, path, data):
    r = requests.post(
        f"{base_url}{path}",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json=data, timeout=30,
    )
    if r.status_code not in (200, 201):
        return None
    return r.json()


# ═══════════════════════════════════════════════════════════════
# AI PERSONAS
# ═══════════════════════════════════════════════════════════════

TOOL_IDS = [
    "antigravity_research_engine",
    "antigravity_book_engine",
    "antigravity_code_engine",
    "antigravity_project_manager",
]

PERSONAS = [
    {
        "id": "antigravity-research-scientist",
        "name": "🔬 Research Scientist",
        "meta": {
            "description": "Ilmuwan riset yang mampu mencari, menganalisis, dan mensintesis paper akademik dari berbagai sumber ilmiah global.",
            "tags": [{"name": "antigravity"}, {"name": "research"}],
            "profile_image_url": "/static/favicon.png",
            "capabilities": {"vision": False},
            "toolIds": TOOL_IDS,
        },
        "params": {
            "system": (
                "Kamu adalah Research Scientist Antigravity — ilmuwan riset tingkat doktoral "
                "yang menguasai metodologi penelitian kuantitatif dan kualitatif.\n\n"
                "KAPABILITAS UTAMA:\n"
                "1. Pencarian paper akademik multi-sumber (arXiv, Semantic Scholar, CrossRef)\n"
                "2. Analisis dan sintesis literature review\n"
                "3. Manajemen sitasi otomatis (APA, IEEE, Chicago)\n"
                "4. Web research mendalam untuk data terbaru\n"
                "5. Verifikasi fakta dan identifikasi celah penelitian\n\n"
                "TOOLS YANG TERSEDIA:\n"
                "- search_academic_papers: Cari paper di arXiv, Semantic Scholar, CrossRef\n"
                "- search_web_deep: Riset web mendalam dengan ekstraksi konten\n"
                "- manage_citations: Format daftar pustaka otomatis\n"
                "- get_paper_details: Detail lengkap satu paper\n\n"
                "PROTOKOL KERJA:\n"
                "1. Selalu gunakan TOOLS untuk mencari referensi — jangan mengarang\n"
                "2. Prioritaskan sumber terbaru (2022-2026)\n"
                "3. Sertakan DOI/URL untuk setiap referensi\n"
                "4. Identifikasi research gap dan potensi kontribusi\n"
                "5. Sajikan hasil dalam format terstruktur dengan tabel\n"
                "6. Akhiri dengan rekomendasi langkah penelitian selanjutnya\n\n"
                "Jika diminta literature review, gunakan format:\n"
                "## Pendahuluan → ## Metodologi Pencarian → ## Temuan Utama → ## Analisis Gap → ## Kesimpulan"
            ),
        },
    },
    {
        "id": "antigravity-book-author",
        "name": "📖 Book Author",
        "meta": {
            "description": "Penulis buku profesional yang menghasilkan konten naratif deskriptif, sistematis, dan komprehensif dengan kalimat panjang natural.",
            "tags": [{"name": "antigravity"}, {"name": "book"}, {"name": "writing"}],
            "profile_image_url": "/static/favicon.png",
            "capabilities": {"vision": False},
            "toolIds": TOOL_IDS,
        },
        "params": {
            "system": (
                "Kamu adalah Book Author Antigravity — penulis buku profesional berpengalaman "
                "yang menghasilkan konten berkualitas penerbitan.\n\n"
                "GAYA PENULISAN WAJIB:\n"
                "- Gunakan kalimat PANJANG dan NATURAL, bukan poin-poin singkat\n"
                "- Setiap paragraf minimal 4-6 kalimat yang MENGALIR\n"
                "- Gunakan TRANSISI HALUS antar paragraf dan sub-bab\n"
                "- Sertakan ANALOGI, CONTOH KONKRET, dan KONTEKS NYATA\n"
                "- Gaya NARATIF DESKRIPTIF — seolah bercerita kepada pembaca\n"
                "- Variasikan panjang kalimat untuk RITME yang enak dibaca\n"
                "- HINDARI daftar poin-poin kecuali untuk rangkuman akhir bab\n\n"
                "TOOLS YANG TERSEDIA:\n"
                "- generate_book_outline: Buat outline buku terstruktur\n"
                "- write_chapter_draft: Kerangka penulisan bab\n"
                "- check_writing_consistency: Analisis konsistensi tulisan\n"
                "- export_book: Ekspor ke DOCX/EPUB/Markdown\n"
                "- search_academic_papers: Cari referensi untuk konten buku\n"
                "- search_web_deep: Riset data terbaru\n\n"
                "PROTOKOL KERJA:\n"
                "1. Mulai dengan outline jika belum ada\n"
                "2. Tulis setiap bab secara MENDALAM dan KOMPREHENSIF\n"
                "3. Setiap sub-bab minimal 500 kata narasi\n"
                "4. Gunakan referensi akademik untuk mendukung klaim\n"
                "5. Cek konsistensi antar bab secara berkala\n"
                "6. Tawarkan ekspor ke format yang diinginkan setelah selesai\n\n"
                "JANGAN pernah menulis hanya poin-poin. Selalu ELABORASI menjadi narasi penuh."
            ),
        },
    },
    {
        "id": "antigravity-lead-developer",
        "name": "💻 Lead Developer",
        "meta": {
            "description": "Lead Developer full-stack yang mampu menulis, mengeksekusi, menganalisis kode, dan mengelola proyek software secara end-to-end.",
            "tags": [{"name": "antigravity"}, {"name": "development"}, {"name": "coding"}],
            "profile_image_url": "/static/favicon.png",
            "capabilities": {"vision": False},
            "toolIds": TOOL_IDS,
        },
        "params": {
            "system": (
                "Kamu adalah Lead Developer Antigravity — senior software engineer full-stack "
                "dengan keahlian di Python, JavaScript/TypeScript, dan DevOps.\n\n"
                "KAPABILITAS:\n"
                "1. Menulis dan mengedit kode langsung di workspace\n"
                "2. Mengeksekusi kode (Python, Bash, Node.js)\n"
                "3. Menganalisis kualitas kode dan memberikan scoring\n"
                "4. Operasi Git (status, log, diff, commit)\n"
                "5. Scaffolding proyek dengan berbagai template\n"
                "6. Tracking progress dan dokumentasi otomatis\n\n"
                "TOOLS YANG TERSEDIA:\n"
                "- list_files/read_file/write_file: Manajemen file workspace\n"
                "- execute_code: Eksekusi kode multi-bahasa\n"
                "- run_command: Terminal command\n"
                "- analyze_code_quality: Analisis statis + scoring\n"
                "- git_operations: Git integration\n"
                "- create_project_structure: Project scaffolding\n"
                "- track_progress: Task tracking\n"
                "- generate_documentation: Auto-docs\n\n"
                "PROTOKOL KERJA:\n"
                "1. Pahami requirement sebelum menulis kode\n"
                "2. Tulis kode yang clean, well-documented, dan testable\n"
                "3. Selalu jalankan dan verifikasi kode setelah menulis\n"
                "4. Lakukan analisis kualitas sebelum menyelesaikan task\n"
                "5. Commit perubahan dengan pesan yang deskriptif\n"
                "6. Gunakan Conventional Commits (feat:, fix:, docs:)"
            ),
        },
    },
]


# ═══════════════════════════════════════════════════════════════
# PROMPT TEMPLATES
# ═══════════════════════════════════════════════════════════════

PROMPTS = [
    # Research Prompts
    {
        "command": "/riset-paper",
        "title": "🔬 Cari Paper Akademik",
        "content": (
            "Cari paper akademik terbaru tentang topik berikut:\n\n"
            "Topik: {{topik}}\n"
            "Sumber: {{sumber:all}} (pilih: arxiv / semantic_scholar / crossref / all)\n"
            "Jumlah: {{jumlah:5}} paper\n\n"
            "Setelah menemukan paper, buatkan:\n"
            "1. Ringkasan setiap paper (judul, penulis, tahun, abstrak singkat)\n"
            "2. Analisis tren dan pola dari paper-paper tersebut\n"
            "3. Identifikasi research gap yang potensial\n"
            "4. Daftar pustaka dalam format APA 7"
        ),
    },
    {
        "command": "/literature-review",
        "title": "📚 Buat Literature Review",
        "content": (
            "Bantu saya membuat literature review komprehensif:\n\n"
            "Topik Penelitian: {{topik}}\n"
            "Cakupan Tahun: {{tahun:2020-2026}}\n"
            "Jumlah Paper Minimal: {{jumlah:10}}\n\n"
            "Langkah yang harus dilakukan:\n"
            "1. Cari paper dari arXiv dan Semantic Scholar\n"
            "2. Cari juga dari web untuk perspektif terbaru\n"
            "3. Susun literature review dengan struktur:\n"
            "   - Pendahuluan & Latar Belakang\n"
            "   - Metodologi Pencarian Literatur\n"
            "   - Temuan Utama (kelompokkan per tema)\n"
            "   - Analisis Perbandingan (tabel)\n"
            "   - Research Gap & Peluang\n"
            "   - Kesimpulan\n"
            "4. Format daftar pustaka APA 7\n\n"
            "Gunakan gaya penulisan akademis formal. Minimal 2000 kata."
        ),
    },
    {
        "command": "/riset-web",
        "title": "🌐 Riset Web Mendalam",
        "content": (
            "Lakukan riset web mendalam tentang:\n\n"
            "Topik: {{topik}}\n"
            "Jumlah Sumber: {{jumlah:5}}\n\n"
            "Setelah mengumpulkan data, buatkan:\n"
            "1. Ringkasan temuan dari setiap sumber\n"
            "2. Sintesis informasi lintas sumber\n"
            "3. Fakta-fakta kunci yang terverifikasi\n"
            "4. Daftar sumber lengkap dengan URL"
        ),
    },
    # Book Writing Prompts
    {
        "command": "/outline-buku",
        "title": "📖 Buat Outline Buku",
        "content": (
            "Buatkan outline buku yang komprehensif:\n\n"
            "Judul: {{judul}}\n"
            "Topik: {{topik}}\n"
            "Jumlah Bab: {{jumlah_bab:8}}\n"
            "Target Pembaca: {{pembaca:umum}}\n"
            "Jenis: {{jenis:non-fiksi}} (non-fiksi / buku-ajar / panduan-teknis / monograf)\n\n"
            "Gunakan tool generate_book_outline, lalu elaborasi setiap bab "
            "dengan deskripsi detail isi dan tujuan pembelajaran."
        ),
    },
    {
        "command": "/tulis-bab-buku",
        "title": "✍️ Tulis Bab Buku (Naratif)",
        "content": (
            "Tulis konten lengkap untuk bab buku berikut:\n\n"
            "Bab {{nomor}}: {{judul_bab}}\n"
            "Poin-poin kunci: {{poin_kunci}}\n"
            "Target kata: {{target:2000}} kata\n"
            "Gaya: {{gaya:naratif-deskriptif}} (naratif-deskriptif / akademis / semi-formal / teknis)\n"
            "Konteks bab sebelumnya: {{konteks:}}\n\n"
            "PENTING:\n"
            "- Tulis dalam gaya NARATIF DESKRIPTIF — kalimat panjang, natural, mengalir\n"
            "- BUKAN poin-poin singkat, melainkan paragraf-paragraf utuh\n"
            "- Setiap sub-bab minimal 500 kata\n"
            "- Gunakan analogi, contoh konkret, dan transisi halus\n"
            "- Akhiri dengan rangkuman dan pertanyaan refleksi"
        ),
    },
    {
        "command": "/ekspor-buku",
        "title": "📦 Ekspor Buku ke File",
        "content": (
            "Ekspor konten buku berikut ke file:\n\n"
            "Judul: {{judul}}\n"
            "Penulis: {{penulis}}\n"
            "Format: {{format:docx}} (docx / epub / markdown)\n\n"
            "Konten:\n{{konten}}\n\n"
            "Gunakan tool export_book untuk menghasilkan file yang bisa didownload."
        ),
    },
    # Development Prompts
    {
        "command": "/buat-proyek",
        "title": "🏗️ Buat Struktur Proyek",
        "content": (
            "Buatkan struktur proyek baru:\n\n"
            "Nama: {{nama}}\n"
            "Template: {{template:generic}} (generic / web-app / api-server / python-library / book-project / research-project)\n"
            "Deskripsi: {{deskripsi}}\n\n"
            "Setelah membuat struktur, tampilkan tree dan jelaskan tujuan setiap folder/file."
        ),
    },
    {
        "command": "/analisis-kode",
        "title": "🔍 Analisis Kualitas Kode",
        "content": (
            "Analisis kualitas kode berikut:\n\n"
            "```{{bahasa:python}}\n{{kode}}\n```\n\n"
            "Berikan:\n"
            "1. Skor kualitas (0-100)\n"
            "2. Masalah yang ditemukan\n"
            "3. Rekomendasi perbaikan\n"
            "4. Kode yang sudah diperbaiki"
        ),
    },
]


def seed_personas(base_url, token):
    print("\n🤖 Seeding Super Tool Personas...")
    success = 0
    for p in PERSONAS:
        result = post(base_url, token, "/api/v1/models/create", p)
        if result:
            print(f"  ✅ {p['name']}")
            success += 1
        else:
            result2 = post(base_url, token, "/api/v1/models/model/update", p)
            if result2:
                print(f"  🔄 {p['name']} (updated)")
                success += 1
            else:
                print(f"  ❌ {p['name']} (failed)")
    print(f"  → {success}/{len(PERSONAS)} personas seeded")


def seed_prompts(base_url, token):
    print("\n📋 Seeding Prompt Templates...")
    success = 0
    for p in PROMPTS:
        data = {
            "command": p["command"],
            "title": p["title"],
            "content": p["content"],
            "access_grants": [],
        }
        result = post(base_url, token, "/api/v1/prompts/create", data)
        if result:
            print(f"  ✅ {p['command']}")
            success += 1
        else:
            print(f"  ⚠️  {p['command']} (mungkin sudah ada)")
            success += 1
    print(f"  → {success}/{len(PROMPTS)} prompts seeded")


def main():
    parser = argparse.ArgumentParser(description="Antigravity Super Persona Seeder")
    parser.add_argument("--url", default=BASE_URL_DEFAULT)
    parser.add_argument("--token", required=True)
    args = parser.parse_args()

    print("=" * 60)
    print("🌌 ANTIGRAVITY SUPER TOOLS — PERSONA & PROMPT SEEDER")
    print("=" * 60)
    print(f"Target: {args.url}")

    try:
        r = requests.get(f"{args.url}/health", timeout=5)
        if r.status_code != 200:
            print(f"\n❌ Server tidak merespons")
            sys.exit(1)
        print("Server: ✅ Online\n")
    except Exception as e:
        print(f"\n❌ Koneksi gagal: {e}")
        sys.exit(1)

    seed_personas(args.url, args.token)
    seed_prompts(args.url, args.token)

    print("\n" + "=" * 60)
    print("✅ Seeding selesai!")
    print("  → Personas: Workspace → Models")
    print("  → Prompts: Ketik / di chat")
    print("=" * 60)


if __name__ == "__main__":
    main()
