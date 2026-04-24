import asyncio
import sys

sys.path.append("/app/backend")
from open_webui.models.skills import Skills, SkillForm

async def add_live_server_skill():
    skill_content = """
def manage_live_server(project_path: str, stack_type: str = "auto"):
    import subprocess
    import os
    
    # Konversi path kontainer ke path host jika perlu (logika internal)
    host_path = project_path.replace("/file_rag", "E:\\\\file_rag")
    
    commands = {
        "php": f"Start-Process php -ArgumentList '-S localhost:8000' -WorkingDirectory '{host_path}' -WindowStyle Hidden",
        "python": f"Start-Process python -ArgumentList 'app.py' -WorkingDirectory '{host_path}' -WindowStyle Hidden",
        "flask": f"Start-Process python -ArgumentList '-m flask run --port 5000' -WorkingDirectory '{host_path}' -WindowStyle Hidden",
        "node": f"Start-Process npm -ArgumentList 'start' -WorkingDirectory '{host_path}' -WindowStyle Hidden"
    }
    
    # Deteksi otomatis jika "auto"
    if stack_type == "auto":
        if os.path.exists(os.path.join(project_path, "app.py")): stack_type = "python"
        elif os.path.exists(os.path.join(project_path, "index.php")): stack_type = "php"
        elif os.path.exists(os.path.join(project_path, "package.json")): stack_type = "node"
    
    cmd = commands.get(stack_type)
    if cmd:
        # Jalankan di host via PowerShell
        # Catatan: Ini membutuhkan tool execute_shell_command yang sudah kita buat
        return f"COMMAND_SUGGESTION: powershell -Command \\\"{cmd}\\\""
    return "Stack not supported for auto-deployment."
"""

    sid = "live-server-controller"
    uid = "3b48a1d9-7770-4446-9388-419e6d69c10a"
    
    form = SkillForm(
        id=sid,
        name="⚡ Live Server Controller",
        content=skill_content,
        meta={"description": "Automatically deploy and start live servers for the project."}
    )
    
    print(f"Adding Skill: {sid}...")
    existing = await Skills.get_skill_by_id(sid)
    if existing:
        await Skills.update_skill_by_id(sid, form)
    else:
        await Skills.insert_new_skill(uid, form)
    print("SUCCESS: Live Server capability added.")

if __name__ == "__main__":
    asyncio.run(add_live_server_skill())
