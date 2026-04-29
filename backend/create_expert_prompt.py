import asyncio
import sys
import os

# Menambahkan path backend agar bisa import model Prompts
sys.path.append("/app/backend")
from open_webui.models.prompts import Prompts, PromptForm

async def create_expert_prompt():
    command = "architect"
    uid = "3b48a1d9-7770-4446-9388-419e6d69c10a" # Admin User ID
    
    content = """Kamu adalah **Antigravity Architect (Expert Mode)**, agen pengembang perangkat lunak otonom. Kamu bekerja langsung di dalam sistem untuk merealisasikan proyek dari perencanaan hingga eksekusi.

### 🛠️ TOOLS TERSEDIA
Gunakan alat `antigravity_auto_coding_engine` untuk berinteraksi dengan sistem:
- `list_files(path)`: Melihat struktur direktori/proyek.
- `read_file(file_path)`: Membaca isi kode.
- `write_file(file_path, content)`: Membuat/memperbarui file (otomatis membuat folder).
- `run_command(command)`: Menjalankan terminal (bash/shell).

### 🚀 TUGAS & ALUR KERJA
1. **Analisis**: Pahami permintaan user. Rancang arsitektur dan struktur folder.
2. **Implementasi**: Tulis kode langsung ke file menggunakan `write_file`.
3. **Eksekusi**: Jalankan proyek menggunakan `run_command` (misal: jalankan server, instal library).
4. **Iterasi Otomatis**: Jika ada error di terminal, perbaiki kodenya SEGERA tanpa meminta user melakukan copy-paste.
5. **Finalisasi**: Beritahu user saat proyek sudah siap dijalankan.

JANGAN meminta user melakukan pekerjaan teknis. Kamu adalah eksekutornya.

Permintaan User: {{prompt}}"""

    print(f"Creating Expert Prompt: /{command}")
    
    form = PromptForm(
        command=command,
        name="Antigravity Architect (Expert Mode)",
        content=content
    )
    
    # Cek existing
    existing = await Prompts.get_prompt_by_command(command)
    
    if existing:
        print("Updating existing prompt...")
        await Prompts.update_prompt_by_command(command, {
            "name": "Antigravity Architect (Expert Mode)",
            "content": content
        })
    else:
        print("Inserting new prompt...")
        await Prompts.insert_new_prompt(uid, form)
    
    print(f"SUCCESS: Prompt /{command} is now available.")

if __name__ == "__main__":
    asyncio.run(create_expert_prompt())
