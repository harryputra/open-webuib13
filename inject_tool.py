import sys
import asyncio
import types

sys.path.append("/app/backend")

from open_webui.models.tools import Tools, ToolForm, ToolMeta
from open_webui.models.users import Users
from open_webui.utils.tools import get_tool_specs

async def inject():
    try:
        # Read the tool code from the mounted workspace
        with open("/workspace/openwebui/antigravity_tools.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        user_id = "admin"
        
        # Manually compile module to get specs (to avoid requiring FastAPI Request context)
        module_name = "tool_antigravity_auto_coding_engine"
        module = types.ModuleType(module_name)
        exec(content, module.__dict__)
        
        if not hasattr(module, "Tools"):
            print("No Tools class found in the module.")
            return

        tool_instance = module.Tools()
        specs = get_tool_specs(tool_instance)
        
        meta = ToolMeta(
            description="Allows the LLM to read, write, list, and create files directly within the local workspace (E:/AntiGravityProject).",
            manifest={"title": "Antigravity Auto-Coding Engine", "author": "Antigravity Architect", "version": "1.0.0"}
        )
        
        form = ToolForm(
            id="antigravity_auto_coding_engine",
            name="Antigravity Auto-Coding Engine",
            content=content,
            meta=meta,
            access_grants=[]
        )
        
        # Delete if exists to overwrite
        existing = await Tools.get_tool_by_id("antigravity_auto_coding_engine")
        if existing:
            await Tools.delete_tool_by_id("antigravity_auto_coding_engine")
            
        await Tools.insert_new_tool(user_id=user_id, form_data=form, specs=specs)
        print("SUCCESS: Tool injected into Open WebUI database.")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(inject())
