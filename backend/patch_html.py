import os

path = r'E:\AntiGravityProject\openwebui\backend\open_webui\static\index.html'
if os.path.exists(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'antigravity_ui.js' not in content:
        new_content = content.replace('</body>', '<script src="/static/antigravity_ui.js"></script></body>')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("SUCCESS: index.html patched.")
    else:
        print("ALREADY PATCHED.")
else:
    print("ERROR: index.html not found.")
