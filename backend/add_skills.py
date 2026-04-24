import asyncio
import sys

sys.path.append("/app/backend")
from open_webui.models.skills import Skills, SkillForm

async def add_essential_skills():
    skills = [
        {
            "id": "project-scaffolder",
            "name": "🏗️ Project Scaffolder",
            "content": """
def scaffold_php_project(project_name: str, base_path: str = "/file_rag"):
    import os
    target = os.path.join(base_path, project_name)
    dirs = ['config', 'models', 'assets/css', 'assets/js', 'views']
    for d in dirs:
        os.makedirs(os.path.join(target, d), exist_ok=True)
    return f"Project {project_name} scaffolded at {target}"
"""
        },
        {
            "id": "system-monitor",
            "name": "🖥️ System Monitor",
            "content": """
def check_system_status():
    import subprocess
    try:
        mysql = subprocess.run("netstat -ano | findstr :3307", shell=True, capture_output=True, text=True)
        status = "MySQL (3307) is UP" if mysql.stdout else "MySQL (3307) is DOWN"
        return status
    except Exception as e:
        return f"Error checking: {e}"
"""
        }
    ]
    
    uid = "3b48a1d9-7770-4446-9388-419e6d69c10a"
    
    for s in skills:
        print(f"Adding Skill: {s['name']}...")
        form = SkillForm(
            id=s["id"],
            name=s["name"],
            content=s["content"],
            meta={"description": f"Antigravity Skill: {s['name']}"}
        )
        existing = await Skills.get_skill_by_id(s["id"])
        if existing:
            await Skills.update_skill_by_id(s["id"], form)
        else:
            await Skills.insert_new_skill(uid, form)
            
    print("SUCCESS: Skills have been added to the Workspace.")

if __name__ == "__main__":
    asyncio.run(add_essential_skills())
