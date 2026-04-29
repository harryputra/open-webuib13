import asyncio
import sys
import os

# Menambahkan path backend agar bisa import model Functions
sys.path.append("/app/backend")
from open_webui.models.functions import Functions

async def update_auto_coding_tool():
    fid = "antigravity_auto_coding_engine"
    
    new_content = """\"\"\"
title: Antigravity Auto-Coding Engine (Enhanced)
description: Powerfull developer tool for reading, writing, and executing code directly within the local workspace.
author: Antigravity Architect
version: 1.1.0
\"\"\"
import os
import json
import subprocess
import logging
from pydantic import BaseModel, Field

class Tools:
    class Valves(BaseModel):
        workspace_path: str = Field(
            default=os.environ.get("WORKSPACE_DIR", "/workspace"),
            description="Path to the primary workspace directory inside the container."
        )

    def __init__(self, valves=None):
        self.valves = valves if valves else self.Valves()

    def list_files(self, path: str = ".") -> str:
        \"\"\"
        Lists files and directories in a specific path within the workspace.
        \"\"\"
        try:
            path = path.replace("\\\\", "/")
            base_dir = self.valves.workspace_path.replace("\\\\", "/")
            full_path = os.path.normpath(os.path.join(base_dir, path.strip("/")))
            
            if not full_path.startswith(os.path.abspath(base_dir)):
                return f"Error: Access denied. Path must be within {base_dir}."
            
            items = os.listdir(full_path)
            return json.dumps(items)
        except Exception as e:
            return f"Error: {e}"

    def read_file(self, file_path: str) -> str:
        \"\"\"
        Reads the content of a file from the workspace.
        \"\"\"
        try:
            file_path = file_path.replace("\\\\", "/")
            base_dir = self.valves.workspace_path.replace("\\\\", "/")
            full_path = os.path.normpath(os.path.join(base_dir, file_path.strip("/")))
            
            if not full_path.startswith(os.path.abspath(base_dir)):
                return f"Error: Access denied."
                
            with open(full_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Error: {e}"

    def write_file(self, file_path: str, content: str) -> str:
        \"\"\"
        Writes content to a file in the workspace. Creates parent directories if they don't exist.
        \"\"\"
        try:
            file_path = file_path.replace("\\\\", "/")
            base_dir = self.valves.workspace_path.replace("\\\\", "/")
            full_path = os.path.normpath(os.path.join(base_dir, file_path.strip("/")))
            
            if not full_path.startswith(os.path.abspath(base_dir)):
                return f"Error: Access denied."
                
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
                
            return f"Success: File '{file_path}' has been written/updated."
        except Exception as e:
            return f"Error: {e}"

    def run_command(self, command: str) -> str:
        \"\"\"
        Executes a terminal/shell command inside the container. Use this to run scripts, start servers, or manage dependencies.
        \"\"\"
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=120,
                executable="/bin/bash"
            )
            output = f"STDOUT:\\n{result.stdout}\\n"
            if result.stderr:
                output += f"STDERR:\\n{result.stderr}\\n"
            output += f"Exit Code: {result.returncode}"
            return output
        except subprocess.TimeoutExpired:
            return "Error: Command timed out after 120 seconds."
        except Exception as e:
            return f"Error: {e}"
"""
    
    print(f"Updating Tool: {fid}")
    
    # Update content in DB
    # Note: versioning and specs are automatically handled by Open WebUI when content is updated via API/DB if we use the right flow.
    # However, since I am injecting via Python, I should ideally trigger the re-parsing of specs.
    # Open WebUI re-parses when the function is updated.
    
    await Functions.update_function_by_id(fid, {
        "content": new_content,
        "is_active": True,
        "is_global": True
    })
    
    print("SUCCESS: Antigravity Auto-Coding Engine updated with Terminal access.")

if __name__ == "__main__":
    asyncio.run(update_auto_coding_tool())
