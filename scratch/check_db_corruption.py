import json
import subprocess

def check_db():
    print("Checking model table for JSON corruption...")
    try:
        # Get all rows
        res = subprocess.check_output([
            'docker', 'exec', 'open-webui-db', 
            'psql', '-U', 'openwebui', '-d', 'openwebui', 
            '-t', '-A', '-F', '|||', 
            '-c', 'SELECT id, meta, params FROM model;'
        ]).decode('utf-8', errors='ignore')
        
        lines = res.strip().split('\n')
        for line in lines:
            if not line: continue
            parts = line.split('|||')
            if len(parts) != 3:
                print(f"Malformed row output: {line[:100]}...")
                continue
            
            mid, meta, params = parts
            
            try:
                json.loads(meta)
            except Exception as e:
                print(f"\n[CORRUPT META] ID: {mid}")
                print(f"Error: {e}")
                print(f"Data: {meta}")
            
            try:
                json.loads(params)
            except Exception as e:
                print(f"\n[CORRUPT PARAMS] ID: {mid}")
                print(f"Error: {e}")
                print(f"Data: {params}")
                
    except Exception as e:
        print(f"Error during DB check: {e}")

if __name__ == "__main__":
    check_db()
