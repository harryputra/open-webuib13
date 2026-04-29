import requests, json

TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjNiNDhhMWQ5LTc3NzAtNDQ0Ni05Mzg4LTQxOWU2ZDY5YzEwYSIsImV4cCI6MTc3OTQ5MTIzNywianRpIjoiN2Y3NjhlNmUtMjA0OC00NjMwLTk5NzgtMzM2YzU2ZWE5NThkIiwiaWF0IjoxNzc3MDcyMDM3fQ.eJ7VE_jfFilMPNwefsZNiPdM_drjnSCN5UgDxLFCoGg'
H = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}
BASE = 'http://localhost:3013'

# Step 1: Check current state
print("=== Current Ollama Config ===")
r = requests.get(f'{BASE}/ollama/api/config', headers=H)
print(f"  Status: {r.status_code}")
print(f"  Response: {r.text[:500]}")

# Step 2: Force update with correct localhost URL
print("\n=== Updating Ollama Config ===")
payload = {
    "ENABLE_OLLAMA_API": True,
    "OLLAMA_BASE_URLS": ["http://localhost:11434"],
    "OLLAMA_API_CONFIGS": {}
}
r2 = requests.post(f'{BASE}/ollama/api/config/update', headers=H, json=payload)
print(f"  Status: {r2.status_code}")
print(f"  Response: {r2.text[:500]}")

# Step 3: Verify models are now visible
print("\n=== Verifying Models ===")
r3 = requests.get(f'{BASE}/ollama/api/tags', headers=H)
print(f"  Status: {r3.status_code}")
data = r3.json()
if 'models' in data:
    print(f"  Models found: {len(data['models'])}")
    for m in data['models']:
        print(f"    - {m['name']}")
else:
    print(f"  Response: {r3.text[:300]}")
