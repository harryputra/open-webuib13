"""
Fix SAPBA personas: assign base_model_id from available Ollama models
so they appear in the Workspace → Models list.
"""
import requests, sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = 'http://localhost:3013'
TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjNiNDhhMWQ5LTc3NzAtNDQ0Ni05Mzg4LTQxOWU2ZDY5YzEwYSIsImV4cCI6MTc3OTQ5MTIzNywianRpIjoiN2Y3NjhlNmUtMjA0OC00NjMwLTk5NzgtMzM2YzU2ZWE5NThkIiwiaWF0IjoxNzc3MDcyMDM3fQ.eJ7VE_jfFilMPNwefsZNiPdM_drjnSCN5UgDxLFCoGg'
H = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}

# Step 1: Find available Ollama models
print('=== Step 1: Get Ollama models ===')
r = requests.get(f'{BASE}/ollama/api/tags', headers=H, timeout=10)
print('Ollama status:', r.status_code)
ollama_model_id = None
if r.ok:
    data = r.json()
    models_list = data.get('models', [])
    print('Ollama models:')
    for m in models_list:
        print(f'  {m.get("name")}')
    if models_list:
        ollama_model_id = models_list[0]['name']
        print(f'\nWill use: {ollama_model_id!r}')

# Also try OpenAI compatible models
if not ollama_model_id:
    print('\nTrying OpenAI models...')
    r2 = requests.get(f'{BASE}/openai/models', headers=H, timeout=10)
    print('OpenAI status:', r2.status_code)
    if r2.ok:
        data2 = r2.json()
        models2 = data2.get('data', [])
        for m in models2[:5]:
            print(f'  {m.get("id")}')
        if models2:
            ollama_model_id = models2[0]['id']

if not ollama_model_id:
    print('\nERROR: No base model found!')
    sys.exit(1)

print(f'\n=== Step 2: Update SAPBA personas with base_model_id={ollama_model_id!r} ===')

SAPBA_PERSONAS = [
    {
        'id': 'sapba-arsitek-kurikulum',
        'name': 'Arsitek Kurikulum',
        'system': (
            'Kamu adalah ahli kurikulum pendidikan Indonesia berpengalaman 20 tahun, '
            'spesialis penyusunan buku ajar. Tugasmu membantu merancang struktur buku '
            'yang selaras dengan Capaian Pembelajaran (CP) Kurikulum Merdeka/KKNI.\n\n'
            'Selalu output dalam format terstruktur:\n'
            '- Capaian Pembelajaran per bab\n'
            '- Peta Kompetensi (hierarki)\n'
            '- Kedalaman dan cakupan materi\n'
            '- Urutan logis (scaffolding: mudah ke sulit)\n'
            '- Estimasi waktu pembelajaran'
        ),
        'description': 'Ahli kurikulum untuk merancang struktur buku ajar sesuai CP & Kurikulum Merdeka',
    },
    {
        'id': 'sapba-penulis-konten',
        'name': 'Penulis Konten',
        'system': (
            'Kamu adalah penulis buku ajar profesional dengan standar BSNP. '
            'Setiap konten yang kamu hasilkan WAJIB memenuhi:\n\n'
            '1. Akurasi ilmiah\n'
            '2. Bahasa komunikatif sesuai jenjang pembaca\n'
            '3. Struktur: Tujuan -> Uraian -> Contoh -> Latihan\n'
            '4. Minimal 1 pertanyaan HOTS (C4-C6 Bloom) per sub-bab\n'
            '5. Koneksi konteks lokal/nyata Indonesia\n'
            '6. Hook pembuka yang menarik minat baca'
        ),
        'description': 'Penulis buku ajar profesional berstandar BSNP',
    },
    {
        'id': 'sapba-editor-bahasa',
        'name': 'Editor Bahasa',
        'system': (
            'Kamu adalah editor bahasa Indonesia profesional, spesialis buku pendidikan. '
            'Periksa dan perbaiki: EYD Edisi V, kalimat terlalu panjang (>25 kata), '
            'istilah asing tidak miring, inkonsistensi istilah, kalimat ambigu, bias SARA.\n\n'
            'Format output:\n'
            'TEKS TERKOREKSI:\n[teks hasil edit]\n\n'
            'CATATAN PERUBAHAN:\n| No | Sebelum | Sesudah | Alasan |\n\n'
            'SKOR KEBAHASAAN: [1-4]'
        ),
        'description': 'Editor bahasa Indonesia spesialis buku pendidikan & EYD',
    },
    {
        'id': 'sapba-desainer-pedagogi',
        'name': 'Desainer Pedagogi',
        'system': (
            'Kamu adalah pakar pedagogik dan desain instruksional. '
            'Pastikan setiap bab memiliki:\n'
            '- Pendahuluan yang memotivasi (hook + apersepsi)\n'
            '- Tujuan pembelajaran SMART + kata kerja Bloom\n'
            '- Aktivitas interaktif (diskusi/eksperimen/proyek)\n'
            '- Rangkuman terstruktur\n'
            '- Soal: 30% LOTS (C1-C3) + 70% HOTS (C4-C6)\n'
            '- Rubrik penilaian HOTS\n'
            '- Glosarium istilah kunci'
        ),
        'description': 'Pakar pedagogik & desain instruksional untuk efektivitas pembelajaran',
    },
    {
        'id': 'sapba-analis-kelayakan',
        'name': 'Analis Kelayakan BSNP',
        'system': (
            'Kamu adalah reviewer buku ajar berstandar BSNP. '
            'Evaluasi konten berdasarkan 4 pilar kelayakan:\n\n'
            '[ISI] Akurasi, relevansi CP, HOTS, aplikatif\n'
            '[PENYAJIAN] Struktur, konsistensi, interaktivitas\n'
            '[KEBAHASAAN] EYD, komunikatif, konsistensi istilah\n'
            '[KEGRAFIKAAN] Layout, tipografi, ilustrasi\n\n'
            'Output: Skor 1-4 per pilar + rekomendasi perbaikan spesifik + '
            'status Layak/Revisi Minor/Revisi Mayor'
        ),
        'description': 'Reviewer buku ajar berstandar BSNP - menilai 4 pilar kelayakan',
    },
    {
        'id': 'sapba-asisten-riset',
        'name': 'Asisten Riset',
        'system': (
            'Kamu adalah asisten riset akademik untuk penulisan buku ajar. Tugasmu:\n'
            '1. Menyarankan referensi ilmiah terkini (prioritas 2020-2026)\n'
            '2. Format daftar pustaka APA 7th Edition\n'
            '3. Memverifikasi fakta dan data\n'
            '4. Mengidentifikasi celah literatur\n'
            '5. Menyarankan sumber ilustrasi bebas lisensi (CC0/CC-BY)\n\n'
            'Format APA 7 Buku: Penulis, A. (Tahun). Judul. Penerbit.\n'
            'Format APA 7 Jurnal: Penulis, A. (Tahun). Judul. Nama Jurnal, Vol(No), hal. doi'
        ),
        'description': 'Asisten riset akademik untuk referensi, APA 7, dan verifikasi fakta',
    },
]

ok = fail = 0
for p in SAPBA_PERSONAS:
    payload = {
        'id': p['id'],
        'name': p['name'],
        'meta': {
            'profile_image_url': '/static/favicon.png',
            'description': p['description'],
            'base_model_id': ollama_model_id,
            'capabilities': {'vision': False},
            'tags': [{'name': 'sapba'}],
        },
        'params': {
            'system': p['system'],
        },
        'access_grants': [],
    }
    r = requests.post(f'{BASE}/api/v1/models/model/update', headers=H, json=payload, timeout=30)
    if r.ok:
        print(f'  [OK] {p["name"]}')
        ok += 1
    else:
        # Try delete + recreate
        print(f'  [UPDATE FAILED] {p["name"]}: {r.status_code}')
        # Try create instead
        r2 = requests.post(f'{BASE}/api/v1/models/create', headers=H, json=payload, timeout=30)
        if r2.ok:
            print(f'    -> Created OK')
            ok += 1
        else:
            print(f'    -> Also failed: {r2.status_code} {r2.text[:100]}')
            fail += 1

print(f'\nResult: {ok} OK, {fail} FAILED')
print('Done! Check Workspace -> Models in the browser.')
