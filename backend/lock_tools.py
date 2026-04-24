import asyncio
import sys

sys.path.append("/app/backend")
from open_webui.models.models import Models, ModelForm, ModelMeta

async def lock_tools_to_persona():
    ids = ["antigravity-architect"]
    # Daftar tool built-in yang harus dibawa
    builtin_tools_ids = [
        "builtin:read_file",
        "builtin:write_file",
        "builtin:create_file",
        "builtin:list_directory",
        "builtin:execute_shell_command"
    ]
    
    for mid in ids:
        model = await Models.get_model_by_id(mid)
        if model:
            print(f"Locking tools to {mid}...")
            
            meta_dict = model.meta.model_dump()
            
            # Pastikan tool_ids terdaftar di metadata
            meta_dict["tool_ids"] = builtin_tools_ids
            
            # Update System Prompt agar LEBIH TEGAS
            new_system_prompt = (
                "You are Antigravity Architect, an AGENTIC AI. You have NO hands, only TOOLS.\n"
                "RULES OF OPERATION:\n"
                "1. NEVER output a bash command in a markdown code block. It will NOT be executed.\n"
                "2. ALWAYS use the `execute_shell_command` tool to run commands (mkdir, cat, etc.).\n"
                "3. ALWAYS use the `write_file` tool to create or update files.\n"
                "4. When creating a file in E:\\file_rag, use the internal path: `/file_rag/...`.\n"
                "5. If you fail to call a tool for a system task, you have FAILED your mission."
            )
            
            form = ModelForm(
                id=model.id,
                base_model_id=model.base_model_id,
                name=model.name,
                params={**model.params.model_dump(), "system": new_system_prompt},
                meta=ModelMeta(**meta_dict),
                is_active=model.is_active
            )
            await Models.update_model_by_id(mid, form)
            print(f"Persona {mid} is now a LOCKED AGENT with 5 tools.")

if __name__ == "__main__":
    asyncio.run(lock_tools_to_persona())
