"""Debug: compare existing working model structure vs SAPBA personas"""
import requests, sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = 'http://localhost:3013'
TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjNiNDhhMWQ5LTc3NzAtNDQ0Ni05Mzg4LTQxOWU2ZDY5YzEwYSIsImV4cCI6MTc3OTQ5MTIzNywianRpIjoiN2Y3NjhlNmUtMjA0OC00NjMwLTk5NzgtMzM2YzU2ZWE5NThkIiwiaWF0IjoxNzc3MDcyMDM3fQ.eJ7VE_jfFilMPNwefsZNiPdM_drjnSCN5UgDxLFCoGg'
H = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}

# Get ALL models from list (paginated)
r = requests.get(f'{BASE}/api/v1/models/list?page=1', headers=H)
data = r.json()
items = data.get('items', [])
print(f'Total in list: {data.get("total", "?")} | Page items: {len(items)}')

print('\n--- ALL MODEL IDs ---')
for m in items:
    mid = m.get('id')
    name = m.get('name')
    meta = m.get('meta') or {}
    base = meta.get('base_model_id')
    print(f'  {mid!r:45s} base={base!r}')

print('\n--- SAPBA PERSONA DETAIL (raw) ---')
r2 = requests.get(f'{BASE}/api/v1/models/model?id=sapba-arsitek-kurikulum', headers=H)
print('Status:', r2.status_code)
if r2.ok:
    m = r2.json()
    print(json.dumps(m, indent=2, ensure_ascii=False)[:2000])
else:
    print(r2.text[:300])

print('\n--- EXISTING WORKING MODEL DETAIL ---')
r3 = requests.get(f'{BASE}/api/v1/models/model?id=antigravity-architect', headers=H)
print('Status:', r3.status_code)
if r3.ok:
    m = r3.json()
    print(json.dumps(m, indent=2, ensure_ascii=False)[:2000])
