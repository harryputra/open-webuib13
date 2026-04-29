import requests, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
BASE_URL = 'http://localhost:3013'
TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjNiNDhhMWQ5LTc3NzAtNDQ0Ni05Mzg4LTQxOWU2ZDY5YzEwYSIsImV4cCI6MTc3OTQ5MTIzNywianRpIjoiN2Y3NjhlNmUtMjA0OC00NjMwLTk5NzgtMzM2YzU2ZWE5NThkIiwiaWF0IjoxNzc3MDcyMDM3fQ.eJ7VE_jfFilMPNwefsZNiPdM_drjnSCN5UgDxLFCoGg'
H = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}

CONTENT = """Tolong buatkan diagram Mermaid.js dengan spesifikasi berikut:

- Topik: **{{ topik | type=text:placeholder="Misal: Topologi Star Jaringan" }}**
- Tema Warna: **{{ style | type=select:options=["semua","ocean","forest","sunset","galaxy","corporate","rainbow","mono","candy","volcano","sunflower","coffee","ice"]:placeholder="Pilih tema warna" }}**

[SAPBA_DIAGRAM_TRIGGER]"""

# Delete old ones first
r = requests.get(f'{BASE_URL}/api/v1/prompts/', headers=H)
if r.ok:
    for p in r.json():
        if p.get('command') == '/diagram-style':
            prompt_id = p.get('id')
            if prompt_id:
                del_req = requests.delete(f"{BASE_URL}/api/v1/prompts/id/{prompt_id}/delete", headers=H)
                print('Delete old:', del_req.status_code)

res = requests.post(f'{BASE_URL}/api/v1/prompts/create', headers=H, json={
    'command': '/diagram-style',
    'name': '🎨 SAPBA Diagram dengan Pilihan Warna/Style (Bersih)',
    'content': CONTENT
})
print('Deploy status:', res.status_code)
