import asyncio
import sys
import os

# Menambahkan path backend agar bisa import model Prompts
sys.path.append("/app/backend")
from open_webui.models.prompts import Prompts, PromptForm

async def create_buat_diagram_prompt():
    command = "buat-diagram"
    uid = "3b48a1d9-7770-4446-9388-419e6d69c10a" # Admin User ID
    
    content = """Tolong buatkan diagram Mermaid.js (Mindmap/Flowchart/Sequence) berdasarkan teks berikut:

- Materi: **{{ materi | type=text:placeholder="Masukkan teks materi yang ingin divisualisasikan" }}**
- Tema Warna: **{{ style | type=select:options=["semua","ocean","forest","sunset","galaxy","corporate","rainbow","mono","candy","volcano","sunflower","coffee","ice"]:placeholder="Pilih tema warna" }}**

[SAPBA_DIAGRAM_TRIGGER]"""

    print(f"Creating Prompt: /{command}")
    
    form = PromptForm(
        command=command,
        name="SAPBA: Pembuat Diagram Visual (Custom Style)",
        content=content
    )
    
    # Cek existing
    existing = await Prompts.get_prompt_by_command(command)
    
    if existing:
        print("Updating existing prompt...")
        await Prompts.update_prompt_by_command(command, {
            "name": "SAPBA: Pembuat Diagram Visual (Custom Style)",
            "content": content
        })
    else:
        print("Inserting new prompt...")
        await Prompts.insert_new_prompt(uid, form)
    
    print(f"SUCCESS: Prompt /{command} is now available with dropdown styles.")

if __name__ == "__main__":
    asyncio.run(create_buat_diagram_prompt())
