"""
SAPBA Image Generator Tool Injector
Injects a custom Python Tool into Open WebUI for generating illustrations.
"""
import requests, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE_URL = 'http://localhost:3013'
TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjNiNDhhMWQ5LTc3NzAtNDQ0Ni05Mzg4LTQxOWU2ZDY5YzEwYSIsImV4cCI6MTc3OTQ5MTIzNywianRpIjoiN2Y3NjhlNmUtMjA0OC00NjMwLTk5NzgtMzM2YzU2ZWE5NThkIiwiaWF0IjoxNzc3MDcyMDM3fQ.eJ7VE_jfFilMPNwefsZNiPdM_drjnSCN5UgDxLFCoGg'
HEADERS = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}

TOOL_CONTENT = '''"""
title: SAPBA Buku Ajar Illustrator
author: Antigravity Architect
description: Membuat gambar ilustrasi nyata untuk buku ajar berdasarkan deskripsi teks (menggantikan placeholder [ILUSTRASI: ...]).
version: 1.0.0
"""

class Tools:
    def __init__(self):
        pass

    def generate_illustration(self, image_prompt: str, style: str = "educational textbook illustration, clean, professional") -> str:
        """
        Membuat gambar ilustrasi secara otomatis dan menampilkannya langsung di dalam chat.
        Gunakan alat ini setiap kali pengguna meminta untuk membuat gambar, mengubah 
        placeholder [ILUSTRASI: ...] menjadi gambar sungguhan, atau meminta visualisasi dari sebuah konsep.
        
        :param image_prompt: Deskripsi detail dari gambar yang ingin dibuat (harus dalam Bahasa Inggris untuk hasil terbaik. Misal: "cross section of an animal cell showing nucleus and mitochondria").
        :param style: Gaya gambar (default: "educational textbook illustration, clean, professional", tapi bisa diubah misal menjadi "realistic photograph", "flat vector art", "3d render").
        """
        import urllib.parse
        import random
        
        try:
            # Memasukkan instruksi resolusi langsung ke dalam teks agar tidak menggunakan parameter URL (&)
            # karena Open WebUI kadang memotong atau gagal memparsing URL yang memiliki banyak karakter '&'
            full_prompt = f"{image_prompt}, {style}, landscape aspect ratio, highly detailed"
            encoded_prompt = urllib.parse.quote(full_prompt)
            seed = random.randint(1, 1000000)
            
            # Using Pollinations.ai free API with minimal URL parameters
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}/{seed}"
            
            # Return Markdown format so it renders directly in Open WebUI chat
            return f"Berikut adalah ilustrasi yang Anda minta:\\n\\n![{image_prompt}]({image_url})\\n\\n*Catatan: Gambar ini di-generate secara real-time.*"
            
        except Exception as e:
            return f"Terjadi kesalahan saat memproses gambar: {str(e)}"
'''

payload = {
    "id": "sapba_image_generator",
    "name": "SAPBA Illustrator",
    "meta": {
        "description": "Pembuat gambar edukasi otomatis (Text-to-Image)",
    },
    "content": TOOL_CONTENT
}

r = requests.get(f'{BASE_URL}/api/v1/tools/id/sapba_image_generator', headers=HEADERS)
if r.ok:
    print("Tool exists. Updating...")
    r2 = requests.post(f'{BASE_URL}/api/v1/tools/id/sapba_image_generator/update', headers=HEADERS, json=payload)
    if r2.ok:
        print("[OK] Illustrator Tool updated successfully.")
    else:
        print(f"[FAIL] Update failed: {r2.text}")
else:
    print("Creating new tool...")
    r2 = requests.post(f'{BASE_URL}/api/v1/tools/create', headers=HEADERS, json=payload)
    if r2.ok:
        print("[OK] Illustrator Tool created successfully.")
    else:
        print(f"[FAIL] Create failed: {r2.text}")

