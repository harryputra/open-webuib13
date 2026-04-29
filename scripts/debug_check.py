import requests, json
TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjNiNDhhMWQ5LTc3NzAtNDQ0Ni05Mzg4LTQxOWU2ZDY5YzEwYSIsImV4cCI6MTc3OTQ5MTIzNywianRpIjoiN2Y3NjhlNmUtMjA0OC00NjMwLTk5NzgtMzM2YzU2ZWE5NThkIiwiaWF0IjoxNzc3MDcyMDM3fQ.eJ7VE_jfFilMPNwefsZNiPdM_drjnSCN5UgDxLFCoGg'
H = {'Authorization': f'Bearer {TOKEN}'}

# Check functions/filters
print("=== FUNCTIONS (Filters) ===")
r = requests.get('http://localhost:3013/api/v1/functions/', headers=H)
for x in r.json():
    print(f"  id={x['id']} | type={x['type']} | active={x['is_active']} | global={x['is_global']} | name={x['name']}")

# Check tools
print("\n=== TOOLS ===")
r2 = requests.get('http://localhost:3013/api/v1/tools/', headers=H)
for x in r2.json():
    print(f"  id={x['id']} | name={x['name']}")
