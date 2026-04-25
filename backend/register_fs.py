import os

path = '/app/backend/open_webui/main.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'workspace_fs' not in content:
    # Injeksi Import
    content = content.replace(
        'from open_webui.routers import',
        'from open_webui.routers import workspace_fs, '
    )
    # Injeksi Router
    content = content.replace(
        'app.include_router(chats.router',
        'app.include_router(workspace_fs.router, prefix="/api/v1/workspace/fs", tags=["workspace"]);\napp.include_router(chats.router'
    )
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: Router registered in main.py")
else:
    print("ALREADY REGISTERED")
