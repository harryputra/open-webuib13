import asyncio
import sys
import time

sys.path.append("/app/backend")
from open_webui.models.functions import Functions, FunctionForm, FunctionMeta

async def inject_auto_executor():
    executor_code = """
import os
import subprocess
import re
import logging
from pydantic import BaseModel, Field
from typing import Optional

log = logging.getLogger(__name__)

class Filter:
    def __init__(self):
        pass

    async def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        messages = body.get("messages", [])
        if not messages:
            return body
            
        last_message = messages[-1]
        content = last_message.get("content", "")
        
        # Cari blok kode bash
        bash_blocks = re.findall(r"```bash\\n(.*?)\\n```", content, re.DOTALL)
        
        if bash_blocks:
            log.info(f"IDE AGENT: Found {len(bash_blocks)} bash blocks to execute.")
            for block in bash_blocks:
                try:
                    # Bersihkan perintah
                    cmd = block.strip()
                    # Eksekusi
                    process = subprocess.run(
                        cmd,
                        shell=True,
                        capture_output=True,
                        text=True,
                        executable="/bin/bash"
                    )
                    log.info(f"IDE AGENT EXEC SUCCESS: {cmd[:50]}...")
                except Exception as e:
                    log.error(f"IDE AGENT EXEC ERROR: {e}")
                
        return body
"""

    fid = "antigravity_executor"
    uid = "3b48a1d9-7770-4446-9388-419e6d69c10a" # Admin User ID
    
    print(f"Injecting Auto-Executor Filter: {fid}")
    
    # Cek existing
    existing = await Functions.get_function_by_id(fid)
    
    form = FunctionForm(
        id=fid,
        name="Antigravity IDE Executor",
        content=executor_code,
        meta=FunctionMeta(description="Automatically executes bash blocks from Antigravity Architect")
    )
    
    if existing:
        print("Updating existing function...")
        await Functions.update_function_by_id(fid, {
            "content": executor_code,
            "is_active": True,
            "is_global": True
        })
    else:
        print("Inserting new function...")
        await Functions.insert_new_function(uid, "filter", form)
        # Aktifkan secara global
        await Functions.update_function_by_id(fid, {
            "is_active": True,
            "is_global": True
        })
    
    print("SUCCESS: Antigravity IDE Engine is now ACTIVE and GLOBAL.")

if __name__ == "__main__":
    asyncio.run(inject_auto_executor())
