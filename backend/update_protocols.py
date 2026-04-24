import asyncio
import sys

sys.path.append("/app/backend")
from open_webui.models.models import Models, ModelForm, ModelMeta

async def update_agent_protocols():
    agents = [
        {
            "id": "antigravity-architect",
            "system_update": (
                "\n\n5. AUTO-DEPLOYMENT: After writing the core project files, you MUST automatically start the live server.\n"
                "   - For PHP: Use `powershell Start-Process php -ArgumentList '-S localhost:8000' -WindowStyle Hidden`.\n"
                "   - For Python/Flask: Use `powershell Start-Process python -ArgumentList 'app.py' -WindowStyle Hidden`.\n"
                "6. ALWAYS provide the clickable local URL (e.g., http://localhost:5000 atau http://localhost:8000) di akhir respons."
            )
        },
        {
            "id": "antigravity-qa-expert",
            "system_update": (
                "\n\n5. FUNCTIONAL TESTING: After the Architect deploys, you MUST verify the URL works.\n"
                "6. Use `execute_shell_command` with `curl` or `ping` to ensure the server is responding."
            )
        }
    ]
    
    for agent in agents:
        model = await Models.get_model_by_id(agent["id"])
        if model:
            print(f"Updating protocol for {agent['id']}...")
            params_dict = model.params.model_dump()
            current_system = params_dict.get("system", "")
            new_system = current_system + agent["system_update"]
            
            params_dict["system"] = new_system
            
            form = ModelForm(
                id=model.id,
                base_model_id=model.base_model_id,
                name=model.name,
                params=params_dict,
                meta=model.meta.model_dump(),
                is_active=model.is_active
            )
            await Models.update_model_by_id(model.id, form)

    print("SUCCESS: Auto-Deployment protocols are now ACTIVE.")

if __name__ == "__main__":
    asyncio.run(update_agent_protocols())
