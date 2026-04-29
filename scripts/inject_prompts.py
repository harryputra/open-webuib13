"""Inject SAPBA Prompts into Open WebUI"""
import requests, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = 'http://localhost:3013'
TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjNiNDhhMWQ5LTc3NzAtNDQ0Ni05Mzg4LTQxOWU2ZDY5YzEwYSIsImV4cCI6MTc3OTQ5MTIzNywianRpIjoiN2Y3NjhlNmUtMjA0OC00NjMwLTk5NzgtMzM2YzU2ZWE5NThkIiwiaWF0IjoxNzc3MDcyMDM3fQ.eJ7VE_jfFilMPNwefsZNiPdM_drjnSCN5UgDxLFCoGg'
H = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}

PROMPTS = [
    {
        'command': '/rancang-buku',
        'name': 'Rancang Struktur Buku Ajar',
        'content': (
            'Bantu saya merancang buku ajar:\n'
            '- Mata Pelajaran: {{mata_pelajaran}}\n'
            '- Jenjang: {{jenjang}}\n'
            '- Semester: {{semester}}\n'
            '- Total Jam: {{jumlah_jam}} JP\n'
            '- Kurikulum: {{kurikulum}}\n\n'
            'Hasilkan:\n'
            '1. Judul buku yang menarik\n'
            '2. Deskripsi buku (150 kata)\n'
            '3. Peta kompetensi (mind map tekstual)\n'
            '4. Daftar bab + sub-bab lengkap (min. 3 subbab/bab)\n'
            '5. Capaian pembelajaran per bab\n'
            '6. Estimasi halaman per bab\n'
            '7. Total estimasi halaman'
        ),
    },
    {
        'command': '/analisis-cp',
        'name': 'Analisis Capaian Pembelajaran',
        'content': (
            'Analisis CP berikut:\n'
            'CP: {{capaian_pembelajaran}}\n'
            'Jenjang: {{jenjang}}\n\n'
            'Hasilkan:\n'
            '1. Breakdown menjadi indikator terukur (kata kerja operasional Bloom)\n'
            '2. Konsep kunci yang wajib diajarkan\n'
            '3. Urutan pembelajaran logis (scaffolding)\n'
            '4. Level Bloom per indikator (C1-C6)\n'
            '5. Saran jenis asesmen\n'
            '6. Matriks: Indikator x Level Bloom'
        ),
    },
    {
        'command': '/tulis-bab',
        'name': 'Tulis Konten Bab Lengkap',
        'content': (
            'Tulis Bab {{nomor_bab}}: {{judul_bab}}\n'
            'Mapel: {{mata_pelajaran}} | Jenjang: {{jenjang}}\n'
            'CP: {{capaian_pembelajaran}}\n'
            'Target: {{target_halaman}} halaman\n\n'
            'Struktur WAJIB:\n'
            '## Tujuan Pembelajaran\n'
            '## Peta Konsep\n'
            '## Pendahuluan (hook + apersepsi)\n'
            '## Uraian Materi\n'
            '### [Sub-bab 1]\n'
            '### [Sub-bab 2]\n'
            '### [Sub-bab 3]\n'
            '## Contoh Soal & Pembahasan (3 soal HOTS)\n'
            '## Rangkuman\n'
            '## Soal Latihan (5 LOTS + 5 HOTS)\n'
            '## Glosarium\n'
            '## Daftar Pustaka'
        ),
    },
    {
        'command': '/tulis-subbab',
        'name': 'Tulis Sub-bab',
        'content': (
            'Tulis sub-bab: {{judul_subbab}}\n'
            'Konteks: {{judul_bab}} | Jenjang: {{jenjang}}\n\n'
            'Wajib sertakan:\n'
            '- Hook pembuka (fakta/pertanyaan menarik, 2-3 kalimat)\n'
            '- Penjelasan konsep + analogi relevan\n'
            '- Min. 1 contoh konteks lokal Indonesia\n'
            '- Min. 1 pertanyaan refleksi HOTS (C4-C6)\n'
            '- 1 aktivitas/diskusi kelompok\n'
            '- Transisi ke sub-bab berikutnya\n'
            'Panjang: 400-600 kata'
        ),
    },
    {
        'command': '/buat-soal-hots',
        'name': 'Buat Soal HOTS Bloom',
        'content': (
            'Buat 10 soal HOTS:\n'
            'Topik: {{topik}} | Jenjang: {{jenjang}}\n'
            'Level: {{level}} (C4-Analisis / C5-Evaluasi / C6-Kreasi)\n\n'
            'Setiap soal:\n'
            '- Berbasis kasus/skenario nyata Indonesia\n'
            '- Kunci jawaban + rubrik (0-4)\n'
            '- Pembahasan langkah demi langkah\n\n'
            'Format:\n'
            '**Soal [N] ([Level]):**\n'
            '[Stimulus/skenario]\n'
            '[Pertanyaan]\n'
            '**Jawaban:** ...\n'
            '**Rubrik:** ...\n'
            '**Pembahasan:** ...'
        ),
    },
    {
        'command': '/review-bsnp',
        'name': 'Review Kelayakan BSNP 4 Pilar',
        'content': (
            'Review konten buku ajar berdasarkan standar BSNP:\n\n'
            '{{konten}}\n\n'
            '### Kelayakan Isi: [X]/4\n'
            '- Temuan: ...\n'
            '- Rekomendasi: ...\n\n'
            '### Kelayakan Penyajian: [X]/4\n'
            '- Temuan: ...\n'
            '- Rekomendasi: ...\n\n'
            '### Kelayakan Kebahasaan: [X]/4\n'
            '- Temuan: ...\n'
            '- Rekomendasi: ...\n\n'
            '### Kelayakan Kegrafikaan (struktural): [X]/4\n'
            '- Temuan: ...\n'
            '- Rekomendasi: ...\n\n'
            '### Total: [X]/16 | Status: [Layak/Revisi Minor/Revisi Mayor]\n'
            '### Prioritas Perbaikan:\n1. ...\n2. ...\n3. ...'
        ),
    },
    {
        'command': '/edit-bahasa',
        'name': 'Edit dan Koreksi Bahasa',
        'content': (
            'Edit teks berikut sesuai standar buku ajar {{jenjang}}:\n\n'
            '{{teks}}\n\n'
            'Periksa:\n'
            '1. Kesalahan EYD Edisi V\n'
            '2. Kalimat >25 kata (pecah)\n'
            '3. Istilah asing tidak miring\n'
            '4. Inkonsistensi istilah teknis\n'
            '5. Kalimat ambigu/multitafsir\n'
            '6. Kosakata tidak sesuai jenjang\n\n'
            'Output:\n'
            '**TEKS TERKOREKSI:**\n'
            '[teks hasil edit]\n\n'
            '**PERUBAHAN:**\n'
            '| # | Sebelum | Sesudah | Alasan |\n\n'
            '**SKOR KEBAHASAAN:** [1-4]'
        ),
    },
    {
        'command': '/buat-rangkuman',
        'name': 'Buat Rangkuman Bab',
        'content': (
            'Buat rangkuman materi berikut:\n\n'
            '{{isi_materi}}\n\n'
            'Format:\n'
            '## Rangkuman Bab [X]\n\n'
            '### Poin Kunci (maks. 10):\n'
            '1. ...\n\n'
            '### Peta Konsep:\n'
            '[diagram tekstual]\n\n'
            '### Tabel Perbandingan (jika relevan):\n\n'
            '### Koneksi Antar Konsep:\n\n'
            'Gunakan bahasa ringkas, padat, mudah diingat.'
        ),
    },
    {
        'command': '/buat-glosarium',
        'name': 'Buat Glosarium Istilah',
        'content': (
            'Ekstrak istilah teknis dari teks dan buat glosarium:\n\n'
            '{{teks}}\n\n'
            'Format per entri:\n'
            '**[Istilah]** *(padanan asing)*: Definisi sesuai jenjang {{jenjang}}, maks. 2 kalimat.\n\n'
            'Urutkan alfabetis. Tandai istilah baru dengan [BARU].'
        ),
    },
    {
        'command': '/buat-pendahuluan',
        'name': 'Buat Pendahuluan Bab',
        'content': (
            'Buat pendahuluan untuk:\n'
            'Bab {{nomor_bab}}: {{judul_bab}} | Jenjang: {{jenjang}}\n\n'
            'Wajib (200-250 kata):\n'
            '1. Hook: fakta/cerita/pertanyaan mengejutkan\n'
            '2. Relevansi: mengapa topik ini penting di kehidupan nyata\n'
            '3. Preview: apa yang akan dipelajari\n'
            '4. Apersepsi: 2-3 pertanyaan aktivasi pengetahuan awal\n'
            '5. Tujuan Pembelajaran (SMART, 3-5 poin)'
        ),
    },
    {
        'command': '/buat-daftar-pustaka',
        'name': 'Format Daftar Pustaka APA 7',
        'content': (
            'Bantu daftar pustaka topik: {{topik}}\n\n'
            'Sumber yang ada:\n'
            '{{daftar_sumber}}\n\n'
            'Tugas:\n'
            '1. Format ke APA 7th Edition\n'
            '2. Cek kelengkapan elemen tiap sumber\n'
            '3. Urutkan alfabetis\n'
            '4. Tambahkan 5 referensi terkini (2020-2026) yang relevan\n'
            '5. Tandai sumber kurang lengkap dengan [!]'
        ),
    },
    {
        'command': '/cek-konsistensi',
        'name': 'Cek Konsistensi Naskah',
        'content': (
            'Periksa konsistensi naskah berikut:\n\n'
            '{{naskah}}\n\n'
            'Identifikasi:\n'
            '1. Istilah teknis tidak konsisten\n'
            '2. Format penomoran tidak seragam\n'
            '3. Gaya penulisan berubah-ubah antar bagian\n'
            '4. Referensi silang hilang atau salah\n'
            '5. Tujuan pembelajaran tidak tercapai dalam isi\n\n'
            'Output:\n'
            '**TABEL STANDARDISASI ISTILAH:**\n'
            '| Variasi | Standar Rekomendasi |\n\n'
            '**TEMUAN INKONSISTENSI:** ...\n'
            '**REKOMENDASI:** ...'
        ),
    },
    {
        'command': '/quality-tracker',
        'name': 'Quality Tracker Buku Ajar',
        'content': (
            'Buat laporan quality tracking untuk: {{judul_buku}}\n\n'
            'Data progres:\n'
            '{{data_progres}}\n\n'
            'Hasilkan:\n'
            '1. Tabel progres per bab (Draft/Review/Final)\n'
            '2. Skor BSNP rata-rata per pilar\n'
            '3. Checklist final yang belum terceklis\n'
            '4. Estimasi waktu penyelesaian\n'
            '5. Rekomendasi prioritas pekerjaan berikutnya'
        ),
    },
]

ok = fail = 0
for p in PROMPTS:
    data = {
        'command': p['command'],
        'name': p['name'],
        'content': p['content'],
        'tags': ['sapba'],
        'access_grants': [],
    }
    r = requests.post(f'{BASE}/api/v1/prompts/create', headers=H, json=data, timeout=30)
    if r.ok:
        print(f'  [OK]   {p["command"]}')
        ok += 1
    else:
        print(f'  [FAIL] {p["command"]}: {r.status_code} - {r.text[:100]}')
        fail += 1

print(f'\nResult: {ok} OK, {fail} FAILED')
