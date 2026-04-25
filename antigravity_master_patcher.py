import os
import re

def patch_file(file_path, search_pattern, replacement_text, anchor_pattern=None):
    if not os.path.exists(file_path):
        print(f"Skipping: {file_path} not found.")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if replacement_text in content:
        print(f"Already patched: {file_path}")
        return True

    print(f"Patching: {file_path}...")
    if anchor_pattern:
        new_content = re.sub(anchor_pattern, replacement_text, content, flags=re.MULTILINE)
    else:
        new_content = content.replace(search_pattern, replacement_text)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

def run_patches():
    base_dir = "backend/open_webui"
    
    # --- PATCH 1: main.py (Router Registration) ---
    patch_file(
        f"{base_dir}/main.py",
        "from open_webui.routers import",
        "from open_webui.routers import", # Dummy
        anchor_pattern=r"(from open_webui.routers import.*)"
    )
    # Re-injecting the logic
    patch_file(f"{base_dir}/main.py", "from open_webui.routers import", "from open_webui.routers import workspace_fs as workspace_fs_router, ")
    
    # --- PATCH 2: config.py (Workspace Vars) ---
    workspace_config = """
# WORKSPACE CONFIG
WORKSPACE_DIR = os.environ.get("WORKSPACE_DIR", "/workspace")
WORKSPACE_MAX_FILE_SIZE = int(os.environ.get("WORKSPACE_MAX_FILE_SIZE", 10 * 1024 * 1024))
"""
    patch_file(f"{base_dir}/config.py", "CACHE_DIR = ", workspace_config + "CACHE_DIR = ")

    # --- PATCH 3: Sidebar.svelte (UI Navigation) ---
    # This one is tricky due to frontend build, but we patch the source
    sidebar_path = "src/lib/components/layout/Sidebar.svelte"
    sidebar_item = """
            <SidebarItem
                id="ide"
                label="IDE"
                icon={CodeBracket}
                href="/workspace/ide"
            />
"""
    patch_file(sidebar_path, "label=\"Workspace\"", sidebar_item + "            <SidebarItem label=\"Workspace\"")

    # --- PATCH 4: builtin.py (IDE Tools Injection) ---
    tools_code = \"\"\"
class WorkspaceTools:
    def read_file(self, path: str) -> str:
        # (Logika read file kita)
        pass
    def write_file(self, path: str, content: str):
        # (Logika write file kita)
        pass
    # ... (Dan seterusnya)
\"\"\"
    patch_file(f"{base_dir}/tools/builtin.py", "class BuiltinTools:", tools_code + "\\nclass BuiltinTools:")

    print("\\n✅ ALL HARD-CODE PATCHES APPLIED.")

if __name__ == "__main__":
    run_patches()
