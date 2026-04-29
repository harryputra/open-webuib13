import subprocess
import json
import time

def inject_persona():
    print("Injeksi Persona Higher-Ed via SQL...")
    
    persona = {
        "id": "sapba-pakar-industri",
        "name": "🏭 Pakar Industri & Lead Engineer",
        "meta": {
            "description": "Spesialis standar industri (IEEE/ISO), Software Engineering, IoT, dan Otomasi",
            "tags": [{"name": "sapba"}, {"name": "industri"}],
            "capabilities": {"vision": False},
        },
        "params": {
            "system": "Kamu adalah Senior Lead Engineer dan Arsitek Sistem dengan pengalaman 25 tahun di industri teknologi global. Fokus: OBE, Industry 4.0, Software Architecture (Clean/SOLID), IoT Protocols (MQTT), dan AI MLOps."
        }
    }

    meta_json = json.dumps(persona["meta"])
    params_json = json.dumps(persona["params"])
    now = int(time.time())
    
    # Check for existing admin user
    try:
        user_id = subprocess.check_output([
            'docker', 'exec', 'open-webui-db', 
            'psql', '-U', 'openwebui', '-d', 'openwebui', '-t', '-A',
            '-c', 'SELECT id FROM "user" LIMIT 1;'
        ]).decode('utf-8').strip()
    except:
        user_id = "3b48a1d9-7770-4446-9388-419e6d69c10a"

    sql = f"""
    INSERT INTO model (id, user_id, name, meta, params, created_at, updated_at, is_active)
    VALUES ('{persona['id']}', '{user_id}', '{persona['name']}', '{meta_json}', '{params_json}', {now}, {now}, true)
    ON CONFLICT (id) DO UPDATE SET meta = EXCLUDED.meta, params = EXCLUDED.params;
    """
    
    subprocess.run([
        'docker', 'exec', 'open-webui-db', 
        'psql', '-U', 'openwebui', '-d', 'openwebui', '-c', sql
    ])
    print(f"Injected Persona: {persona['id']}")

if __name__ == "__main__":
    inject_persona()
