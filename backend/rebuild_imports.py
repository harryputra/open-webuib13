import os

path = 'e:/AntiGravityProject/openwebui/backend/open_webui/main.py'
if os.path.exists(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Menemukan range baris yang rusak
    start_idx = -1
    end_idx = -1
    for i, line in enumerate(lines):
        if 'from open_webui.routers import' in line:
            start_idx = i
        if start_idx != -1 and line.strip() == ')' and i > start_idx:
            end_idx = i
            break
    
    if start_idx != -1 and end_idx != -1:
        new_import = [
            "from open_webui.routers import (\n",
            "    analytics, audio, images, ollama, openai, retrieval, pipelines,\n",
            "    tasks, auths, channels, chats, notes, folders, configs, groups,\n",
            "    files, functions, memories, models, knowledge, prompts,\n",
            "    evaluations, skills, tools, users, utils, scim, terminals,\n",
            "    automations, calendar, workspace_fs\n",
            ")\n"
        ]
        # Ganti range baris
        lines[start_idx:end_idx+1] = new_import
        
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print("SUCCESS: main.py imports rebuilt.")
    else:
        print("ERROR: Could not find import block range.")
else:
    print("ERROR: File not found.")
