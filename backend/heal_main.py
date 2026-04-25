import os
import re

path = 'e:/AntiGravityProject/openwebui/backend/open_webui/main.py'
if os.path.exists(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Membersihkan import yang rusak
    content = re.sub(r'from open_webui\.routers import workspace_fs,.*\(', 'from open_webui.routers import workspace_fs, (', content)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: main.py healed.")
else:
    print("ERROR: File not found.")
