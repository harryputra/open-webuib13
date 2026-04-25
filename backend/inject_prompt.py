import psycopg2
import os

# Konfigurasi database dari environment atau default
conn = psycopg2.connect(
    host="db", # Host di dalam network docker
    database="openwebui",
    user="openwebui",
    password="openwebui_pass"
)

system_prompt = """Anda adalah Antigravity Analyst & Architect, pakar perancangan sistem enterprise. 
Tugas Anda adalah merancang sistem secara mendalam (Database, Folder Structure, Fitur Utama).

SETIAP KALI Anda selesai memberikan narasi rancangan sistem, Anda WAJIB mengakhirinya dengan blok kode berikut tepat di bagian paling bawah jawaban Anda tanpa pengecekan tambahan, agar sistem UI Antigravity dapat memprosesnya menjadi tombol interaktif:

---ANTIGRAVITY_PROPOSAL---
```json
{
  "project_name": "[Nama Projek]",
  "features": ["Fitur 1", "Fitur 2", "dst"],
  "tech_stack": "PHP Native / FastAPI / dsb",
  "files": [
    {"path": "index.php", "content": "<!-- Konten Awal -->"},
    {"path": "README.md", "content": "# Dokumentasi Projek"}
  ]
}
```"""

try:
    cursor = conn.cursor()
    # Update model yang memiliki nama 'antigravity'
    cursor.execute("UPDATE model SET system = %s WHERE id LIKE %s", (system_prompt, '%antigravity-analyst%'))
    conn.commit()
    print(f"SUCCESS: {cursor.rowcount} models updated with Architect Instructions.")
    cursor.close()
except Exception as e:
    print(f"ERROR: {e}")
finally:
    conn.close()
