"""Check base models and inject SAPBA personas with correct base_model_id"""
import requests, sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = 'http://localhost:3013'
TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjNiNDhhMWQ5LTc3NzAtNDQ0Ni05Mzg4LTQxOWU2ZDY5YzEwYSIsImV4cCI6MTc3OTQ5MTIzNywianRpIjoiN2Y3NjhlNmUtMjA0OC00NjMwLTk5NzgtMzM2YzU2ZWE5NThkIiwiaWF0IjoxNzc3MDcyMDM3fQ.eJ7VE_jfFilMPNwefsZNiPdM_drjnSCN5UgDxLFCoGg'
H = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}

# Step 1: Get available base models
r = requests.get(f'{BASE}/api/v1/models/base', headers=H)
print('Base models status:', r.status_code)
base_model_id = None
if r.ok:
    models = r.json()
    print('Available base models:')
    for m in models[:15]:
        mid = m.get('id', '')
        mname = m.get('name', '')
        print(f'  id={mid!r} name={mname!r}')
    if models:
        base_model_id = models[0]['id']
        print(f'\nUsing base model: {base_model_id!r}')
else:
    print('Response:', r.text[:300])

# Step 2: Also check what existing custom models look like
r2 = requests.get(f'{BASE}/api/v1/models/list', headers=H)
print('\nCustom models list status:', r2.status_code)
if r2.ok:
    data = r2.json()
    items = data.get('items', [])
    print(f'Total custom models: {len(items)}')
    for m in items[:5]:
        print(f'  id={m.get("id")!r} base_model_id={m.get("meta", {}).get("base_model_id")!r}')
