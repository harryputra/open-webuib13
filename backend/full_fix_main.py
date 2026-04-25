import os
import re

path = 'e:/AntiGravityProject/openwebui/backend/open_webui/main.py'
if os.path.exists(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    import_fixed = False
    router_fixed = False
    
    for line in lines:
        # Perbaiki baris import yang rusak
        if 'from open_webui.routers import' in line and not import_fixed:
            new_lines.append('from open_webui.routers import workspace_fs, (chats, configs, documents, forms, groups, mems, models, oauth, prompts, retrieval, users, utils)\n')
            import_fixed = True
        # Perbaiki baris pendaftaran router yang rusak
        elif 'app.include_router(workspace_fs.router' in line:
            if not router_fixed:
                new_lines.append('app.include_router(workspace_fs.router, prefix="/api/v1/workspace/fs", tags=["workspace"])\n')
                router_fixed = True
        else:
            new_lines.append(line)
            
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("SUCCESS: main.py fully cleaned and fixed.")
else:
    print("ERROR: File not found.")
