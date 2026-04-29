"""
SAPBA Live Web Researcher Tool Injector
Injects a custom Python Tool into Open WebUI for live internet research.
"""
import requests, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE_URL = 'http://localhost:3013'
TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjNiNDhhMWQ5LTc3NzAtNDQ0Ni05Mzg4LTQxOWU2ZDY5YzEwYSIsImV4cCI6MTc3OTQ5MTIzNywianRpIjoiN2Y3NjhlNmUtMjA0OC00NjMwLTk5NzgtMzM2YzU2ZWE5NThkIiwiaWF0IjoxNzc3MDcyMDM3fQ.eJ7VE_jfFilMPNwefsZNiPdM_drjnSCN5UgDxLFCoGg'
HEADERS = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}

TOOL_CONTENT = '''"""
title: SAPBA Live Web Researcher
author: Antigravity Architect
description: Melakukan pencarian internet secara live (DuckDuckGo) dan membaca isi artikel/jurnal untuk mendapatkan data atau referensi terbaru.
version: 1.0.0
"""

class Tools:
    def __init__(self):
        pass

    def search_and_read_web(self, query: str, num_results: int = 3) -> str:
        """
        Melakukan pencarian di internet secara live menggunakan DuckDuckGo, lalu membuka 
        dan membaca isi dari URL teratas untuk merangkum datanya.
        Gunakan alat ini jika Asisten Riset diminta mencari data terbaru, statistik, 
        atau jurnal yang tidak ada dalam database lokal (RAG).
        
        :param query: Kata kunci pencarian spesifik (misal: "Statistik stunting anak Indonesia 2024").
        :param num_results: Jumlah artikel maksimal yang akan dibaca (direkomendasikan: 3, maksimal: 5).
        """
        try:
            from duckduckgo_search import DDGS
            import requests
            from bs4 import BeautifulSoup
        except ImportError:
            return "Error: Library duckduckgo-search atau bs4 belum terinstall."

        try:
            results_text = f"Memulai riset untuk: '{query}'\\n\\n"
            
            with DDGS() as ddgs:
                search_results = list(ddgs.text(query, max_results=num_results))
                
            if not search_results:
                return f"Pencarian '{query}' tidak membuahkan hasil."
                
            for i, res in enumerate(search_results):
                title = res.get('title', 'Tanpa Judul')
                link = res.get('href', '')
                snippet = res.get('body', '')
                
                results_text += f"=== HASIL {i+1} ===\\n"
                results_text += f"Judul: {title}\\n"
                results_text += f"URL: {link}\\n"
                
                # Coba baca konten halamannya
                try:
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                    page = requests.get(link, headers=headers, timeout=5)
                    
                    if page.status_code == 200:
                        soup = BeautifulSoup(page.content, 'html.parser')
                        # Ambil teks dari paragraf
                        paragraphs = soup.find_all('p')
                        content = " ".join([p.get_text() for p in paragraphs])
                        # Batasi hingga 1500 karakter per halaman agar tidak token limit
                        content = content.replace('\\n', ' ').strip()
                        results_text += f"Isi Artikel (Cuplikan): {content[:1500]}...\\n\\n"
                    else:
                        results_text += f"Deskripsi (Tidak bisa diakses penuh): {snippet}\\n\\n"
                except Exception as req_err:
                    results_text += f"Deskripsi: {snippet}\\n\\n"
                    
            return results_text
            
        except Exception as e:
            return f"Terjadi kesalahan saat riset web: {str(e)}"
'''

payload = {
    "id": "sapba_web_researcher",
    "name": "SAPBA Web Researcher",
    "meta": {
        "description": "Alat riset jurnal dan data aktual via DuckDuckGo & Web Scraper",
    },
    "content": TOOL_CONTENT
}

r = requests.get(f'{BASE_URL}/api/v1/tools/id/sapba_web_researcher', headers=HEADERS)
if r.ok:
    print("Tool exists. Updating...")
    r2 = requests.post(f'{BASE_URL}/api/v1/tools/id/sapba_web_researcher/update', headers=HEADERS, json=payload)
    if r2.ok:
        print("[OK] Web Researcher Tool updated successfully.")
    else:
        print(f"[FAIL] Update failed: {r2.text}")
else:
    print("Creating new tool...")
    r2 = requests.post(f'{BASE_URL}/api/v1/tools/create', headers=HEADERS, json=payload)
    if r2.ok:
        print("[OK] Web Researcher Tool created successfully.")
    else:
        print(f"[FAIL] Create failed: {r2.text}")

