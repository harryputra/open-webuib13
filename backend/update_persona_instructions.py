import asyncio
import sys

sys.path.append("/app/backend")
from open_webui.models.models import Models, ModelForm, ModelMeta

async def update_personas():
    ids = ["antigravity-architect"]
    
    for mid in ids:
        model = await Models.get_model_by_id(mid)
        if model:
            print(f"Updating instructions for {mid}...")
            
            # System Prompt dengan mapping path
            new_system_prompt = (
                "You are Antigravity Architect, a powerful agentic AI coding assistant with DIRECT SYSTEM ACCESS.\n\n"
                "SYSTEM ENVIRONMENT MAPPING:\n"
                "- Host Path `E:\\file_rag` is mounted at `/file_rag` (INTERNAL).\n"
                "- Host Path `E:\\AntiGravityProject` is mounted at `/workspace` (INTERNAL).\n\n"
                "CRITICAL RULES:\n"
                "1. If the user asks to create/modify files in `E:\\file_rag\\`, you MUST use paths starting with `/file_rag/` in your tool calls.\n"
                "2. ALWAYS use your tools (`write_file`, `create_file`, `execute_shell_command`) for any filesystem or terminal task.\n"
                "3. When you write a code block (bash/python), it will be EXECUTED. Make sure it uses the correct INTERNAL paths (/file_rag/... or /workspace/...).\n"
                "4. Example: To create a folder in E:\\file_rag\\projek_app, run `mkdir -p /file_rag/projek_app/test_agent`.\n"
                "\nYour available tools: read_file, write_file, create_file, list_directory, execute_shell_command."
            )

            meta_dict = model.meta.model_dump()
            params_dict = model.params.model_dump()
            
            if not meta_dict.get("features"):
                meta_dict["features"] = {}
            meta_dict["features"]["code_interpreter"] = True
            
            if not meta_dict.get("capabilities"):
                meta_dict["capabilities"] = {}
            meta_dict["capabilities"]["code_interpreter"] = True
            meta_dict["capabilities"]["builtin_tools"] = True
            
            params_dict["system"] = new_system_prompt
            
            form = ModelForm(
                id=model.id,
                base_model_id=model.base_model_id,
                name=model.name,
                params=params_dict,
                meta=ModelMeta(**meta_dict),
                is_active=model.is_active
            )
            await Models.update_model_by_id(mid, form)
            print(f"Persona {mid} updated with path mapping and enforced execution.")

if __name__ == "__main__":
    asyncio.run(update_personas())
