"""Update SAPBA prompts for visual elements (tables, placeholders, and diagrams)"""
import requests, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = 'http://localhost:3013'
TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjNiNDhhMWQ5LTc3NzAtNDQ0Ni05Mzg4LTQxOWU2ZDY5YzEwYSIsImV4cCI6MTc3OTQ5MTIzNywianRpIjoiN2Y3NjhlNmUtMjA0OC00NjMwLTk5NzgtMzM2YzU2ZWE5NThkIiwiaWF0IjoxNzc3MDcyMDM3fQ.eJ7VE_jfFilMPNwefsZNiPdM_drjnSCN5UgDxLFCoGg'
H = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}

# 1. Update existing /tulis-subbab
UPDATED_SUBBAB = {
    'command': '/tulis-subbab',
    'name': 'Tulis Sub-bab (Visual & Tabel)',
    'content': (
        'Tulis sub-bab: {{judul_subbab}}\n'
        'Konteks: {{judul_bab}} | Jenjang: {{jenjang}}\n\n'
        'Wajib sertakan komponen berikut secara berurutan:\n'
        '1. Hook pembuka (fakta/pertanyaan menarik, 2-3 kalimat)\n'
        '2. Penjelasan konsep dengan gaya bahasa yang sesuai jenjang\n'
        '3. 📊 **Satu Tabel Perbandingan / Data** yang merangkum konsep agar mudah dibaca.\n'
        '4. 🖼️ **Satu Instruksi Gambar** dengan format: `[ILUSTRASI: <deskripsi detail gambar/grafik yang dibutuhkan illustrator untuk menggambar bagian ini>]`\n'
        '5. Min. 1 contoh konteks lokal Indonesia\n'
        '6. Min. 1 pertanyaan refleksi HOTS (C4-C6)\n'
        '7. 1 aktivitas mandiri/diskusi\n'
        'Panjang keseluruhan: 500-700 kata'
    ),
    'tags': ['sapba'],
    'access_grants': []
}

# 2. Add new /buat-diagram
NEW_DIAGRAM = {
    'command': '/buat-diagram',
    'name': 'Buat Diagram/Peta Konsep (Mermaid)',
    'content': (
        'Buatlah sebuah visualisasi diagram untuk materi berikut:\n'
        '{{materi}}\n\n'
        'Tugas:\n'
        '1. Analisis materi dan tentukan jenis diagram yang paling cocok (pilih salah satu: Mindmap, Flowchart, atau Pie Chart).\n'
        '2. Tuliskan kodenya menggunakan sintaks `mermaid` di dalam blok kode markdown.\n'
        '3. Pastikan diagramnya memiliki warna/styling dasar jika memungkinkan agar menarik.\n'
        '4. Berikan 1-2 kalimat pengantar sebelum menampilkan diagram.'
    ),
    'tags': ['sapba'],
    'access_grants': []
}

ok = fail = 0

# Retrieve prompts to find ID of /tulis-subbab
r = requests.get(f'{BASE}/api/v1/prompts/', headers=H)
if r.ok:
    prompts = r.json()
    subbab_prompt = next((p for p in prompts if p['command'] == '/tulis-subbab'), None)
    
    if subbab_prompt:
        pid = subbab_prompt['id']
        r_up = requests.post(f'{BASE}/api/v1/prompts/id/{pid}/update', headers=H, json=UPDATED_SUBBAB)
        if r_up.ok:
            print('[OK] Updated /tulis-subbab')
            ok += 1
        else:
            print(f'[FAIL] Update /tulis-subbab: {r_up.text[:100]}')
            fail += 1
    else:
        # Create if not exists
        r_cr = requests.post(f'{BASE}/api/v1/prompts/create', headers=H, json=UPDATED_SUBBAB)
        if r_cr.ok:
            print('[OK] Created /tulis-subbab')
            ok += 1
        else:
            print(f'[FAIL] Create /tulis-subbab: {r_cr.text[:100]}')
            fail += 1
else:
    print('Failed to get prompts list')

# Create /buat-diagram
r_diag = requests.post(f'{BASE}/api/v1/prompts/create', headers=H, json=NEW_DIAGRAM)
if r_diag.ok:
    print('[OK] Created /buat-diagram')
    ok += 1
else:
    # Maybe it exists, let's try updating
    diag_prompt = next((p for p in prompts if p['command'] == '/buat-diagram'), None)
    if diag_prompt:
        pid = diag_prompt['id']
        r_up2 = requests.post(f'{BASE}/api/v1/prompts/id/{pid}/update', headers=H, json=NEW_DIAGRAM)
        if r_up2.ok:
            print('[OK] Updated /buat-diagram')
            ok += 1
        else:
            print(f'[FAIL] Update /buat-diagram: {r_up2.text[:100]}')
            fail += 1
    else:
        print(f'[FAIL] Create /buat-diagram: {r_diag.text[:100]}')
        fail += 1

print(f'\nResult: {ok} OK, {fail} FAILED')
