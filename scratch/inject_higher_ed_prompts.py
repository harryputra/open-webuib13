import subprocess
import uuid
import time

def inject_prompts():
    print("Injeksi Prompt Higher-Ed via SQL...")
    
    # Get Admin User ID
    try:
        user_id = subprocess.check_output([
            'docker', 'exec', 'open-webui-db', 
            'psql', '-U', 'openwebui', '-d', 'openwebui', '-t', '-A',
            '-c', 'SELECT id FROM "user" LIMIT 1;'
        ]).decode('utf-8').strip()
        print(f"Found User ID: {user_id}")
    except:
        user_id = "f0a5f963-c78b-4b1f-9b24-9f899b8979e2" # Fallback
    
    prompts = [
        {
            "command": "/rancang-modul-studi",
            "name": "🎓 Rancang Modul Perguruan Tinggi (OBE)",
            "content": "Rancang struktur Mata Kuliah/Modul untuk jenjang Kampus:\n- Nama Mata Kuliah: {{mata_pelajaran}}\n- Beban SKS: {{jumlah_sks}}\n- Fokus Bidang: {{fokus_bidang}}\n- Kurikulum: Outcome-Based Education (OBE)\n\nHasilkan RPS, CPMK, dan Proyek Industri."
        },
        {
            "command": "/standar-industri",
            "name": "🏗️ Terapkan Standar Industri",
            "content": "Berikan optimasi standar industri pada materi berikut:\n\n{{konten_materi}}\n\nBidang: {{bidang}}\n\nMasukkan SOP, ISO/IEEE, dan Best Practices Industri."
        },
        {
            "command": "/lab-engineering",
            "name": "🧪 Buat Panduan Lab/Praktikum",
            "content": "Buat modul praktikum laboratorium untuk:\nTopik: {{topik}}\nAlat/Tools: {{tools}}\n\nWajib menyertakan Alat/Bahan, Diagram (Mermaid), dan Langkah Kerja."
        }
    ]

    for p in prompts:
        pid = str(uuid.uuid4())
        now = int(time.time())
        sql = f"""
        INSERT INTO prompt (id, command, user_id, name, content, created_at, updated_at, is_active)
        VALUES ('{pid}', '{p['command']}', '{user_id}', '{p['name']}', '{p['content']}', {now}, {now}, true)
        ON CONFLICT (command) DO UPDATE SET content = EXCLUDED.content;
        """
        subprocess.run([
            'docker', 'exec', 'open-webui-db', 
            'psql', '-U', 'openwebui', '-d', 'openwebui', '-c', sql
        ])
        print(f"Injected: {p['command']}")

if __name__ == "__main__":
    inject_prompts()
