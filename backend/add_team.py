import asyncio
import sys

sys.path.append("/app/backend")
from open_webui.models.models import Models, ModelForm, ModelMeta

async def add_team_personas():
    team = [
        {
            "id": "antigravity-qa-expert",
            "name": "🔍 Antigravity QA Expert",
            "system": (
                "You are Antigravity QA Expert. Your mission is to find bugs and ensure security.\n"
                "1. ALWAYS review code for SQL Injection and XSS vulnerabilities.\n"
                "2. ALWAYS use `execute_shell_command` to run unit tests or check file existence.\n"
                "3. NEVER allow insecure database connections.\n"
                "4. Use the internal path `/file_rag/...` for project files."
            )
        },
        {
            "id": "antigravity-designer",
            "name": "🎨 Antigravity UI/UX Designer",
            "system": (
                "You are Antigravity UI/UX Designer. Your mission is to make applications BEAUTIFUL.\n"
                "1. ALWAYS provide premium CSS using glassmorphism, gradients, and smooth transitions.\n"
                "2. ALWAYS ensure mobile responsiveness.\n"
                "3. Use `write_file` to update style.css or assets.\n"
                "4. Your motto: 'Function is nothing without Elegance'."
            )
        }
    ]
    
    uid = "3b48a1d9-7770-4446-9388-419e6d69c10a" # Admin
    
    for member in team:
        print(f"Registering {member['name']}...")
        form = ModelForm(
            id=member["id"],
            base_model_id="deepseek-v3:latest", # Atau model default Anda
            name=member["name"],
            params={"system": member["system"]},
            meta=ModelMeta(
                description=f"Specialized Antigravity Agent: {member['name']}",
                tool_ids=["builtin:read_file", "builtin:write_file", "builtin:execute_shell_command"]
            )
        )
        
        existing = await Models.get_model_by_id(member["id"])
        if existing:
            await Models.update_model_by_id(member["id"], form)
        else:
            await Models.insert_new_model(form, uid)
            
    print("SUCCESS: Your development team is now READY in the Workspace.")

if __name__ == "__main__":
    asyncio.run(add_team_personas())
