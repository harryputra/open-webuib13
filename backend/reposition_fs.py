import os

path = '/app/backend/open_webui/main.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Hapus pendaftaran lama yang mungkin salah
content = content.replace('app.include_router(workspace_fs.router, prefix="/api/v1/workspace/fs", tags=["workspace"]);', '')

# Pastikan import ada
if 'from open_webui.routers import workspace_fs' not in content:
    content = content.replace(
        'from open_webui.routers import',
        'from open_webui.routers import workspace_fs, '
    )

# Sisipkan di rute paling awal
if 'workspace_fs.router' not in content:
    content = content.replace(
        'app.include_router(',
        'app.include_router(workspace_fs.router, prefix="/api/v1/workspace/fs", tags=["workspace"])\napp.include_router('
    )

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("SUCCESS: Router repositioned to top priority.")
