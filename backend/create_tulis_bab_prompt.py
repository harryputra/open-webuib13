import asyncio
import sys
import os

# Menambahkan path backend agar bisa import model Prompts
sys.path.append("/app/backend")
from open_webui.models.prompts import Prompts, PromptForm

async def create_tulis_bab_prompt():
    command = "tulis-bab"
    uid = "3b48a1d9-7770-4446-9388-419e6d69c10a" # Admin User ID
    
    content = """Kamu adalah **Pakar Penulis Buku Ajar (Textbook Expert)**. Tugasmu adalah menulis isi bab buku secara lengkap, naratif, deskriptif, dan sistematis.

### 📝 INSTRUKSI PENULISAN
1. **Gaya Bahasa**: Naratif-Deskriptif (mengalir seperti cerita teknis).
2. **Struktur Paragraf**: Gunakan paragraf yang panjang dan berisi penjelasan mendalam. 
3. **Konektivitas**: Pastikan ada kalimat transisi yang kuat antar paragraf.
4. **JANGAN**: Memberikan jawaban dalam bentuk poin-poin (bullet points) sebagai materi utama. Gunakan paragraf utuh.
5. **Analogi**: Gunakan minimal satu analogi dunia nyata untuk menjelaskan konsep teknis yang sulit.
6. **Kedalaman**: Berikan detail teknis yang cukup untuk mahasiswa atau pembelajar tingkat lanjut.

### 🚀 ALUR KERJA
Sebutkan nama **Bab** dan **Sub-bab** yang ingin ditulis. Saya akan memberikan draf lengkapnya.

Sub-bab yang sedang dikerjakan: {{prompt}}"""

    print(f"Creating Prompt: /{command}")
    
    form = PromptForm(
        command=command,
        name="SAPBA: Penulisan Bab Buku (Naratif-Deskriptif)",
        content=content
    )
    
    # Cek existing
    existing = await Prompts.get_prompt_by_command(command)
    
    if existing:
        print("Updating existing prompt...")
        await Prompts.update_prompt_by_command(command, {
            "name": "SAPBA: Penulisan Bab Buku (Naratif-Deskriptif)",
            "content": content
        })
    else:
        print("Inserting new prompt...")
        await Prompts.insert_new_prompt(uid, form)
    
    print(f"SUCCESS: Prompt /{command} is now available.")

if __name__ == "__main__":
    asyncio.run(create_tulis_bab_prompt())
