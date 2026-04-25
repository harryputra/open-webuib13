import asyncio
import sys

sys.path.append("/app/backend")
from open_webui.models.functions import Functions

async def update_filter_logic():
    fid = "antigravity_executor"
    filter_record = await Functions.get_function_by_id(fid)
    
    if filter_record:
        # Menambahkan logika deteksi update ke dalam filter
        new_content = filter_record.content.replace(
            "def filter(self, body: dict) -> dict:",
            "def filter(self, body: dict) -> dict:\n"
            "        # Auto-Update Logic\n"
            "        if body.get('messages') and '/execute_safe_update' in body['messages'][-1]['content']:\n"
            "            import subprocess\n"
            "            subprocess.Popen(['cmd', '/c', 'E:\\\\AntiGravityProject\\\\openwebui\\\\safe_update.bat'])\n"
            "            body['messages'][-1]['content'] = '🚀 **MEMULAI SAFE UPDATE...** Sistem akan restart dalam beberapa detik. Harap tunggu.'\n"
            "            return body\n"
        )
        
        await Functions.update_function_by_id(fid, {"content": new_content})
        print("SUCCESS: Filter now supports One-Click Safe Update.")

if __name__ == "__main__":
    asyncio.run(update_filter_logic())
