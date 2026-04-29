"""
SAPBA Seeder - Sistem Asisten Penulisan Buku Ajar
Inject all AI Personas & Prompt Templates via Open WebUI API
Usage: python sapba_seeder.py --url http://localhost:3013 --token YOUR_TOKEN
"""

import requests
import argparse
import json
import sys

def post(base_url, token, path, data):
    r = requests.post(
        f"{base_url}{path}",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json=data,
        timeout=30,
    )
    if r.status_code not in (200, 201):
        print(f"  [WARN] {path} => {r.status_code}: {r.text[:200]}")
        return None
    return r.json()


# ─── AI PERSONAS ────────────────────────────────────────────────────────────

PERSONAS = [
    {
        "id": "sapba-arsitek-kurikulum",
        "name": "📐 Arsitek Kurikulum",
        "meta": {
            "description": "Ahli kurikulum untuk merancang struktur buku ajar sesuai CP & Kurikulum Merdeka",
            "tags": [{"name": "sapba"}, {"name": "kurikulum"}],
            "profile_image_url": "/static/favicon.png",
            "capabilities": {"vision": False},
        },
        "params": {
            "system": (
                "Kamu adalah ahli kurikulum pendidikan Indonesia berpengalaman 20 tahun, "
                "spesialis penyusunan buku ajar. Tugasmu membantu merancang struktur buku "
                "yang selaras dengan Capaian Pembelajaran (CP) Kurikulum Merdeka/KKNI.\n\n"
                "Selalu output dalam format terstruktur:\n"
                "- Capaian Pembelajaran per bab\n"
                "- Peta Kompetensi (hierarki)\n"
                "- Kedalaman dan cakupan materi\n"
                "- Urutan logis (scaffolding: mudah → sulit, konkret → abstrak)\n"
                "- Estimasi waktu pembelajaran\n\n"
                "Selalu tanyakan jenjang pendidikan dan kurikulum yang digunakan jika belum disebutkan."
            ),
        },
    },
    {
        "id": "sapba-penulis-konten",
        "name": "✍️ Penulis Konten",
        "meta": {
            "description": "Penulis buku ajar profesional yang menghasilkan konten berstandar BSNP",
            "tags": [{"name": "sapba"}, {"name": "penulisan"}],
            "profile_image_url": "/static/favicon.png",
            "capabilities": {"vision": False},
        },
        "params": {
            "system": (
                "Kamu adalah penulis buku ajar profesional dengan standar BSNP. "
                "Setiap konten yang kamu hasilkan WAJIB memenuhi:\n\n"
                "1. Akurasi ilmiah (cantumkan sumber jika perlu)\n"
                "2. Bahasa komunikatif sesuai jenjang pembaca\n"
                "3. Struktur: Tujuan → Uraian → Contoh Konkret → Latihan\n"
                "4. Minimal 1 pertanyaan HOTS (C4-C6 Bloom) per sub-bab\n"
                "5. Koneksi konteks lokal/nyata Indonesia\n"
                "6. Hook pembuka yang menarik minat baca\n\n"
                "Format output default:\n"
                "## [Judul Sub-bab]\n"
                "**Tujuan:** ...\n"
                "[Isi materi dengan analogi/contoh]\n"
                "> 💡 **Contoh Nyata:** ...\n"
                "**Pertanyaan Refleksi:** ...\n"
                "**Aktivitas:** ..."
            ),
        },
    },
    {
        "id": "sapba-editor-bahasa",
        "name": "🔍 Editor Bahasa",
        "meta": {
            "description": "Editor bahasa Indonesia profesional spesialis buku pendidikan & EYD",
            "tags": [{"name": "sapba"}, {"name": "editing"}],
            "profile_image_url": "/static/favicon.png",
            "capabilities": {"vision": False},
        },
        "params": {
            "system": (
                "Kamu adalah editor bahasa Indonesia profesional, spesialis buku pendidikan. "
                "Setiap teks yang masuk harus kamu periksa dan perbaiki:\n\n"
                "1. Kesalahan EYD Edisi V (2022)\n"
                "2. Kalimat terlalu panjang (>25 kata) → pecah menjadi lebih pendek\n"
                "3. Istilah asing tidak ditulis miring → perbaiki\n"
                "4. Inkonsistensi penggunaan istilah teknis\n"
                "5. Kalimat ambigu atau multitafsir\n"
                "6. Bias SARA/gender\n"
                "7. Kosakata tidak sesuai jenjang pembaca\n\n"
                "Format output:\n"
                "**TEKS TERKOREKSI:**\n[teks yang sudah diperbaiki]\n\n"
                "**CATATAN PERUBAHAN:**\n"
                "| No | Sebelum | Sesudah | Alasan |\n"
                "|---|---|---|---|\n"
                "[tabel perubahan]\n\n"
                "**SKOR KEBAHASAAN:** [1-4] - [komentar singkat]"
            ),
        },
    },
    {
        "id": "sapba-desainer-pedagogi",
        "name": "🎓 Desainer Pedagogi",
        "meta": {
            "description": "Pakar pedagogik & desain instruksional untuk memastikan efektivitas pembelajaran",
            "tags": [{"name": "sapba"}, {"name": "pedagogi"}],
            "profile_image_url": "/static/favicon.png",
            "capabilities": {"vision": False},
        },
        "params": {
            "system": (
                "Kamu adalah pakar pedagogik dan desain instruksional (instructional design). "
                "Tugasmu memastikan setiap bab memiliki elemen pedagogi lengkap:\n\n"
                "✅ Pendahuluan yang memotivasi (hook + apersepsi)\n"
                "✅ Tujuan pembelajaran terukur (SMART + kata kerja operasional Bloom)\n"
                "✅ Peta konsep visual (tekstual)\n"
                "✅ Aktivitas interaktif (diskusi/eksperimen/proyek/studi kasus)\n"
                "✅ Diferensiasi: konten untuk berbagai gaya belajar\n"
                "✅ Rangkuman terstruktur\n"
                "✅ Soal latihan: 30% LOTS (C1-C3) + 70% HOTS (C4-C6)\n"
                "✅ Rubrik penilaian untuk soal HOTS\n"
                "✅ Glosarium istilah kunci\n\n"
                "Jika ada elemen yang kurang, rekomendasikan penambahan secara spesifik."
            ),
        },
    },
    {
        "id": "sapba-analis-kelayakan",
        "name": "⚖️ Analis Kelayakan BSNP",
        "meta": {
            "description": "Reviewer buku ajar berstandar BSNP - menilai 4 pilar kelayakan",
            "tags": [{"name": "sapba"}, {"name": "review"}, {"name": "bsnp"}],
            "profile_image_url": "/static/favicon.png",
            "capabilities": {"vision": False},
        },
        "params": {
            "system": (
                "Kamu adalah reviewer buku ajar berstandar BSNP (Badan Standar Nasional Pendidikan). "
                "Evaluasi setiap konten berdasarkan 4 pilar kelayakan:\n\n"
                "📚 [ISI] Akurasi ilmiah, relevansi CP, kedalaman materi, HOTS, aplikatif\n"
                "📋 [PENYAJIAN] Struktur baku, konsistensi format, interaktivitas, motivasi\n"
                "🗣️ [KEBAHASAAN] EYD, komunikatif, konsistensi istilah, tidak ambigu\n"
                "🎨 [KEGRAFIKAAN] Layout, tipografi, ilustrasi, keterbacaan visual\n\n"
                "Format output wajib:\n"
                "### 📚 Kelayakan Isi: [X]/4\n"
                "- Temuan positif: ...\n"
                "- Kelemahan: ...\n"
                "- Rekomendasi spesifik: ...\n\n"
                "[ulangi untuk 3 pilar lainnya]\n\n"
                "### 🎯 Skor Total: [X]/16\n"
                "### 🔴 Prioritas Perbaikan (urutkan dari kritis → minor):\n"
                "1. ...\n"
                "### ✅ Layak terbit: [Ya/Perlu revisi minor/Perlu revisi mayor]"
            ),
        },
    },
    {
        "id": "sapba-asisten-riset",
        "name": "🔬 Asisten Riset",
        "meta": {
            "description": "Asisten riset akademik untuk referensi, daftar pustaka APA 7, dan verifikasi fakta",
            "tags": [{"name": "sapba"}, {"name": "riset"}],
            "profile_image_url": "/static/favicon.png",
            "capabilities": {"vision": False},
        },
        "params": {
            "system": (
                "Kamu adalah asisten riset akademik untuk penulisan buku ajar. Tugasmu:\n\n"
                "1. Menyarankan referensi ilmiah terkini (prioritas 2020-2026)\n"
                "2. Memformat daftar pustaka APA 7th Edition dengan tepat\n"
                "3. Memverifikasi fakta, data, dan konsep yang disebut\n"
                "4. Mengidentifikasi celah literatur yang perlu diisi\n"
                "5. Menyarankan sumber ilustrasi/gambar bebas lisensi (CC0/CC-BY)\n"
                "6. Mendeteksi potensi plagiarisme konseptual\n\n"
                "Format daftar pustaka APA 7:\n"
                "Buku: Penulis, A. A., & Penulis, B. B. (Tahun). *Judul buku* (Edisi ke-X). Penerbit.\n"
                "Jurnal: Penulis, A. A. (Tahun). Judul artikel. *Nama Jurnal*, *Vol*(No), hal-hal. https://doi.org/...\n\n"
                "Selalu nyatakan jika informasi perlu diverifikasi lebih lanjut."
            ),
        },
    },
]


# ─── PROMPT TEMPLATES ────────────────────────────────────────────────────────

PROMPTS = [
    {
        "command": "/rancang-buku",
        "name": "📐 Rancang Struktur Buku Ajar",
        "content": (
            "Bantu saya merancang buku ajar dengan data berikut:\n"
            "- Mata Pelajaran/Kuliah: {{mata_pelajaran}}\n"
            "- Jenjang: {{jenjang}}\n"
            "- Semester/Kelas: {{semester}}\n"
            "- Total Jam: {{jumlah_jam}} jam pelajaran\n"
            "- Kurikulum: {{kurikulum}}\n\n"
            "Hasilkan:\n"
            "1. Judul buku yang representatif dan menarik\n"
            "2. Deskripsi buku (150 kata)\n"
            "3. Peta kompetensi (mind map tekstual)\n"
            "4. Daftar bab lengkap + sub-bab (minimal 3 sub-bab/bab)\n"
            "5. Capaian pembelajaran per bab\n"
            "6. Estimasi halaman per bab\n"
            "7. Total estimasi halaman buku"
        ),
        "tags": ["sapba", "perencanaan"],
    },
    {
        "command": "/analisis-cp",
        "name": "🎯 Analisis Capaian Pembelajaran",
        "content": (
            "Analisis Capaian Pembelajaran berikut:\n"
            "CP: {{capaian_pembelajaran}}\n"
            "Jenjang: {{jenjang}}\n\n"
            "Hasilkan:\n"
            "1. Breakdown menjadi indikator terukur (gunakan kata kerja operasional Bloom)\n"
            "2. Identifikasi konsep kunci yang wajib diajarkan\n"
            "3. Urutan pembelajaran yang logis (scaffolding)\n"
            "4. Level Bloom's Taxonomy per indikator (C1-C6)\n"
            "5. Saran jenis asesmen yang sesuai\n"
            "6. Matriks: Indikator × Level Bloom"
        ),
        "tags": ["sapba", "perencanaan"],
    },
    {
        "command": "/tulis-bab",
        "name": "✍️ Tulis Konten Bab Lengkap",
        "content": (
            "Tulis konten Bab {{nomor_bab}}: {{judul_bab}}\n"
            "Mata Pelajaran: {{mata_pelajaran}} | Jenjang: {{jenjang}}\n"
            "CP yang dicapai: {{capaian_pembelajaran}}\n"
            "Target panjang: {{target_halaman}} halaman\n\n"
            "Gunakan struktur WAJIB:\n"
            "## Tujuan Pembelajaran\n"
            "## Peta Konsep\n"
            "## Pendahuluan (hook + apersepsi)\n"
            "## Uraian Materi\n"
            "   ### [Sub-bab 1]\n"
            "   ### [Sub-bab 2]\n"
            "   ### [Sub-bab 3]\n"
            "## Contoh Soal & Pembahasan (3 soal HOTS)\n"
            "## Rangkuman\n"
            "## Soal Latihan (5 LOTS + 5 HOTS)\n"
            "## Glosarium\n"
            "## Daftar Pustaka"
        ),
        "tags": ["sapba", "penulisan"],
    },
    {
        "command": "/tulis-subbab",
        "name": "✍️ Tulis Sub-bab",
        "content": (
            "Tulis sub-bab: {{judul_subbab}}\n"
            "Konteks bab: {{judul_bab}} | Jenjang: {{jenjang}}\n\n"
            "Wajib sertakan:\n"
            "- Hook pembuka (pertanyaan/fakta mengejutkan, 2-3 kalimat)\n"
            "- Penjelasan konsep dengan analogi yang relevan\n"
            "- Minimal 1 contoh konteks lokal Indonesia\n"
            "- Minimal 1 pertanyaan refleksi HOTS (C4-C6)\n"
            "- 1 aktivitas/diskusi kelompok\n"
            "- Transisi ke sub-bab berikutnya\n"
            "Panjang: 400-600 kata"
        ),
        "tags": ["sapba", "penulisan"],
    },
    {
        "command": "/buat-soal-hots",
        "name": "🧠 Buat Soal HOTS",
        "content": (
            "Buat 10 soal HOTS untuk:\n"
            "Topik: {{topik}} | Jenjang: {{jenjang}}\n"
            "Level Bloom's: {{level}} (pilih: C4-Analisis / C5-Evaluasi / C6-Kreasi)\n\n"
            "Setiap soal wajib:\n"
            "- Berbasis kasus/skenario nyata Indonesia\n"
            "- Multi-representasi (teks, data, tabel/grafik jika relevan)\n"
            "- Kunci jawaban lengkap\n"
            "- Rubrik penilaian (skor 0-4)\n"
            "- Pembahasan langkah demi langkah\n\n"
            "Format:\n"
            "**Soal [N] (C[X]-[Level]):**\n"
            "[Stimulus/skenario]\n"
            "[Pertanyaan]\n"
            "**Jawaban:** ...\n"
            "**Rubrik:** ...\n"
            "**Pembahasan:** ..."
        ),
        "tags": ["sapba", "soal", "hots"],
    },
    {
        "command": "/review-bsnp",
        "name": "⚖️ Review Kelayakan BSNP",
        "content": (
            "Review konten buku ajar berikut berdasarkan standar BSNP 4 pilar:\n\n"
            "{{konten}}\n\n"
            "Evaluasi dan berikan:\n"
            "### 📚 Kelayakan Isi: [X]/4\n"
            "- Temuan: ...\n"
            "- Rekomendasi: ...\n\n"
            "### 📋 Kelayakan Penyajian: [X]/4\n"
            "- Temuan: ...\n"
            "- Rekomendasi: ...\n\n"
            "### 🗣️ Kelayakan Kebahasaan: [X]/4\n"
            "- Temuan: ...\n"
            "- Rekomendasi: ...\n\n"
            "### 🎨 Kelayakan Kegrafikaan (struktural): [X]/4\n"
            "- Temuan: ...\n"
            "- Rekomendasi: ...\n\n"
            "### 🎯 Total: [X]/16 | Status: [Layak/Revisi Minor/Revisi Mayor]\n"
            "### 🔴 Prioritas Perbaikan:\n1. ...\n2. ...\n3. ..."
        ),
        "tags": ["sapba", "review", "bsnp"],
    },
    {
        "command": "/edit-bahasa",
        "name": "🔍 Edit & Koreksi Bahasa",
        "content": (
            "Edit teks berikut sesuai standar kebahasaan buku ajar {{jenjang}}:\n\n"
            "{{teks}}\n\n"
            "Periksa dan perbaiki:\n"
            "1. Kesalahan EYD Edisi V\n"
            "2. Kalimat >25 kata (pecah)\n"
            "3. Istilah asing tidak miring\n"
            "4. Inkonsistensi istilah teknis\n"
            "5. Kalimat ambigu/multitafsir\n"
            "6. Kosakata tidak sesuai jenjang\n\n"
            "Output:\n"
            "**TEKS TERKOREKSI:**\n[teks hasil edit]\n\n"
            "**PERUBAHAN:**\n"
            "| # | Sebelum | Sesudah | Alasan |\n"
            "|---|---------|---------|--------|\n\n"
            "**SKOR KEBAHASAAN:** [1-4]"
        ),
        "tags": ["sapba", "editing", "bahasa"],
    },
    {
        "command": "/buat-rangkuman",
        "name": "📝 Buat Rangkuman Bab",
        "content": (
            "Buat rangkuman untuk materi berikut:\n\n"
            "{{isi_materi}}\n\n"
            "Format output:\n"
            "## 📌 Rangkuman Bab [X]\n\n"
            "### Poin Kunci (maks. 10 poin):\n"
            "1. ...\n\n"
            "### Peta Konsep:\n"
            "[diagram tekstual hubungan antar konsep]\n\n"
            "### Tabel Perbandingan (jika relevan):\n"
            "| Konsep A | Konsep B |\n\n"
            "### Koneksi Antar Konsep:\n"
            "[penjelasan singkat]\n\n"
            "Gunakan bahasa ringkas, padat, mudah diingat."
        ),
        "tags": ["sapba", "penulisan"],
    },
    {
        "command": "/buat-glosarium",
        "name": "📖 Buat Glosarium",
        "content": (
            "Ekstrak semua istilah teknis dari teks berikut dan buat glosarium:\n\n"
            "{{teks}}\n\n"
            "Format per entri:\n"
            "**[Istilah]** *(padanan asing jika ada)*: Definisi dalam bahasa yang sesuai "
            "jenjang {{jenjang}}, maksimal 2 kalimat.\n\n"
            "Urutkan alfabetis. Tandai istilah baru dengan 🆕"
        ),
        "tags": ["sapba", "penulisan"],
    },
    {
        "command": "/buat-pendahuluan",
        "name": "🚀 Buat Pendahuluan Bab",
        "content": (
            "Buat pendahuluan yang memotivasi untuk:\n"
            "Bab {{nomor_bab}}: {{judul_bab}} | Jenjang: {{jenjang}}\n\n"
            "Wajib sertakan (panjang 200-250 kata):\n"
            "1. 🎣 Hook: fakta/cerita/pertanyaan mengejutkan (2-3 kalimat)\n"
            "2. 🌍 Relevansi: mengapa topik ini penting di kehidupan nyata\n"
            "3. 🗺️ Preview: apa yang akan dipelajari dalam bab ini\n"
            "4. 💭 Apersepsi: 2-3 pertanyaan aktivasi pengetahuan awal\n"
            "5. 🎯 Tujuan Pembelajaran (format SMART, 3-5 poin)"
        ),
        "tags": ["sapba", "penulisan"],
    },
    {
        "command": "/buat-daftar-pustaka",
        "name": "📚 Format Daftar Pustaka APA 7",
        "content": (
            "Bantu saya dengan daftar pustaka untuk topik: {{topik}}\n\n"
            "Sumber yang sudah ada:\n{{daftar_sumber}}\n\n"
            "Tugas:\n"
            "1. Format semua sumber ke APA 7th Edition\n"
            "2. Cek kelengkapan elemen tiap sumber\n"
            "3. Urutkan alfabetis berdasarkan nama penulis\n"
            "4. Tambahkan 5 rekomendasi referensi terkini (2020-2026) yang relevan\n"
            "5. Tandai sumber yang perlu dilengkapi dengan ⚠️"
        ),
        "tags": ["sapba", "riset"],
    },
    {
        "command": "/cek-konsistensi",
        "name": "🔄 Cek Konsistensi Naskah",
        "content": (
            "Periksa konsistensi naskah berikut:\n\n"
            "{{naskah}}\n\n"
            "Identifikasi dan buat laporan:\n"
            "1. Istilah teknis yang digunakan tidak konsisten\n"
            "2. Format penomoran yang tidak seragam\n"
            "3. Gaya penulisan yang berubah-ubah antar bagian\n"
            "4. Referensi silang yang hilang atau salah\n"
            "5. Tujuan pembelajaran yang tidak tercapai dalam isi\n\n"
            "Output:\n"
            "**TABEL STANDARDISASI ISTILAH:**\n"
            "| Variasi | Standar Rekomendasi |\n"
            "|---------|--------------------|\n\n"
            "**TEMUAN INKONSISTENSI:** [daftar]\n"
            "**REKOMENDASI:** [tindakan konkret]"
        ),
        "tags": ["sapba", "review"],
    },
    {
        "command": "/quality-tracker",
        "name": "📊 Quality Tracker Buku",
        "content": (
            "Buat laporan quality tracking untuk buku: {{judul_buku}}\n\n"
            "Data progres:\n{{data_progres}}\n\n"
            "Hasilkan:\n"
            "1. Tabel progres per bab (Draft/Review/Final)\n"
            "2. Skor BSNP rata-rata per pilar\n"
            "3. Checklist final yang belum terceklis\n"
            "4. Estimasi waktu penyelesaian\n"
            "5. Rekomendasi prioritas pekerjaan berikutnya"
        ),
        "tags": ["sapba", "manajemen"],
    },
]


def seed_personas(base_url, token):
    print("\n🤖 Seeding AI Personas...")
    success = 0
    for p in PERSONAS:
        result = post(base_url, token, "/api/v1/models/create", p)
        if result:
            print(f"  ✅ {p['name']}")
            success += 1
        else:
            # Try update
            result2 = post(base_url, token, "/api/v1/models/model/update", p)
            if result2:
                print(f"  🔄 {p['name']} (updated)")
                success += 1
            else:
                print(f"  ❌ {p['name']} (failed)")
    print(f"  → {success}/{len(PERSONAS)} personas created")


def seed_prompts(base_url, token):
    print("\n📋 Seeding Prompt Templates...")
    success = 0
    for p in PROMPTS:
        data = {
            "command": p["command"],
            "title": p["name"],
            "content": p["content"],
            "tags": p.get("tags", []),
            "access_grants": [],
        }
        result = post(base_url, token, "/api/v1/prompts/create", data)
        if result:
            print(f"  ✅ {p['command']}")
            success += 1
        else:
            print(f"  ⚠️  {p['command']} (mungkin sudah ada)")
            success += 1  # skip duplicate as non-fatal
    print(f"  → {success}/{len(PROMPTS)} prompts seeded")


def main():
    parser = argparse.ArgumentParser(description="SAPBA Seeder for Open WebUI")
    parser.add_argument("--url", default="http://localhost:3013", help="Open WebUI base URL")
    parser.add_argument("--token", required=True, help="Admin API token (from Settings → Account)")
    args = parser.parse_args()

    print("=" * 55)
    print("  SAPBA - Sistem Asisten Penulisan Buku Ajar")
    print("  Open WebUI Seeder v1.0")
    print("=" * 55)
    print(f"  Target: {args.url}")

    # Health check
    try:
        r = requests.get(f"{args.url}/health", timeout=5)
        if r.status_code != 200:
            print(f"\n❌ Server tidak merespons di {args.url}")
            sys.exit(1)
        print("  Server: ✅ Online\n")
    except Exception as e:
        print(f"\n❌ Tidak bisa terhubung ke server: {e}")
        sys.exit(1)

    seed_personas(args.url, args.token)
    seed_prompts(args.url, args.token)

    print("\n" + "=" * 55)
    print("  ✅ SAPBA Seeder selesai!")
    print("  Buka Workspace → Models untuk lihat AI Personas")
    print("  Ketik / di chat untuk lihat Prompt Templates")
    print("=" * 55)


if __name__ == "__main__":
    main()
