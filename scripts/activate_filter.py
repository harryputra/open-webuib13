import requests, json
TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjNiNDhhMWQ5LTc3NzAtNDQ0Ni05Mzg4LTQxOWU2ZDY5YzEwYSIsImV4cCI6MTc3OTQ5MTIzNywianRpIjoiN2Y3NjhlNmUtMjA0OC00NjMwLTk5NzgtMzM2YzU2ZWE5NThkIiwiaWF0IjoxNzc3MDcyMDM3fQ.eJ7VE_jfFilMPNwefsZNiPdM_drjnSCN5UgDxLFCoGg'
H = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}
BASE = 'http://localhost:3013'

# Step 1: Toggle ON the filter  
print("Activating filter...")
r = requests.post(f'{BASE}/api/v1/functions/id/sapba_image_filter/toggle', headers=H)
print(f"  Toggle response: {r.status_code} -> {r.text[:200]}")

# Step 2: Toggle global ON
print("Setting filter to Global...")
r2 = requests.post(f'{BASE}/api/v1/functions/id/sapba_image_filter/toggle/global', headers=H)
print(f"  Global toggle response: {r2.status_code} -> {r2.text[:200]}")

# Step 3: Verify
print("\nVerifying status...")
r3 = requests.get(f'{BASE}/api/v1/functions/id/sapba_image_filter', headers=H)
d = r3.json()
print(f"  active={d.get('is_active')} | global={d.get('is_global')}")
