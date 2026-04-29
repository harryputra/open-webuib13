import subprocess
import json
import time

def inject_mythos():
    print("Injeksi Zenith Mythos Logic via SQL...")
    
    # 1. NEW PERSONA: Zenith Mythos Architect
    persona = {
        "id": "antigravity-mythos-architect",
        "name": "🌀 Zenith Mythos Architect",
        "meta": {
            "description": "AI dengan logika Recurrent-Depth (Looped Reasoning) untuk pemecahan masalah kompleks",
            "tags": [{"name": "zenith"}, {"name": "mythos"}, {"name": "research"}],
            "capabilities": {"vision": False},
        },
        "params": {
            "system": (
                "Kamu adalah Zenith Mythos Architect, sebuah AI yang mengimplementasikan logika 'Recurrent-Depth Transformer' (RDT).\n\n"
                "PROTOKOL PENALARAN (MANDATORY):\n"
                "Setiap jawabanmu harus melalui 3 tahap internal yang disimulasikan dalam output:\n\n"
                "1. [PRELUDE]: Identifikasi parameter masalah dan batasan teknis.\n"
                "2. [RECURRENT LOOPS (Iterasi 1-3)]: Lakukan 'Deep Thinking' secara berulang. Di setiap iterasi, perbaiki kesalahan logika, tambahkan kedalaman teknis, dan verifikasi terhadap standar industri (ISO/IEEE).\n"
                "3. [CODA]: Hasil akhir yang sudah sangat teroptimasi, elegan, dan siap pakai.\n\n"
                "Gunakan format markdown yang indah dengan blok 'details' untuk menyembunyikan proses loop jika terlalu panjang."
            )
        }
    }

    # 2. NEW PROMPT TEMPLATE: /mythos-reasoning
    prompt = {
        "command": "/mythos-reasoning",
        "name": "🌀 Mythos Deep Reasoning",
        "content": (
            "Gunakan Logika Mythos (Recurrent-Depth) untuk menganalisis masalah berikut:\n\n"
            "Masalah: {{masalah}}\n"
            "Domain: {{domain}}\n\n"
            "Terapkan 3 tahap (Prelude -> 3 Loops -> Coda) untuk memberikan solusi yang paling optimal dan 'future-proof'."
        )
    }

    now = int(time.time())
    try:
        user_id = subprocess.check_output([
            'docker', 'exec', 'open-webui-db', 
            'psql', '-U', 'openwebui', '-d', 'openwebui', '-t', '-A',
            '-c', 'SELECT id FROM "user" LIMIT 1;'
        ]).decode('utf-8').strip()
    except:
        user_id = "3b48a1d9-7770-4446-9388-419e6d69c10a"

    # Inject Persona
    clean_meta = json.dumps(persona["meta"]).replace("'", "''")
    clean_params = json.dumps(persona["params"]).replace("'", "''")
    
    sql_p = f"""
    INSERT INTO model (id, user_id, name, meta, params, created_at, updated_at, is_active)
    VALUES ('{persona['id']}', '{user_id}', '{persona['name']}', '{clean_meta}', '{clean_params}', {now}, {now}, true)
    ON CONFLICT (id) DO UPDATE SET meta = EXCLUDED.meta, params = EXCLUDED.params;
    """
    
    # Inject Prompt
    clean_content = prompt["content"].replace("'", "''")
    sql_pr = f"""
    INSERT INTO prompt (id, command, user_id, name, content, created_at, updated_at, is_active)
    VALUES ('{str(time.time())}', '{prompt['command']}', '{user_id}', '{prompt['name']}', '{clean_content}', {now}, {now}, true)
    ON CONFLICT (command) DO UPDATE SET content = EXCLUDED.content;
    """

    subprocess.run(['docker', 'exec', 'open-webui-db', 'psql', '-U', 'openwebui', '-d', 'openwebui', '-c', sql_p])
    subprocess.run(['docker', 'exec', 'open-webui-db', 'psql', '-U', 'openwebui', '-d', 'openwebui', '-c', sql_pr])
    
    print("Zenith Mythos Architect & Prompt Injected Successfully!")

if __name__ == "__main__":
    inject_mythos()
