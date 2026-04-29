import json
import subprocess

def fix_db():
    print("Antigravity DB Doctor: Starting JSON repair...")
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
            if len(parts) != 3: continue
            
            mid, meta, params = parts
            dirty = False
            
            # Fix META
            try:
                json.loads(meta)
            except json.JSONDecodeError as e:
                if "Extra data" in str(e):
                    print(f"  [FIXING] Meta for {mid}")
                    # Try to merge concatenated JSONs
                    # Basic fix: Find the split point
                    # For simplicity, we'll just take the first valid object or merge them
                    # In our case it looks like {obj1}{obj2} -> merge(obj1, obj2)
                    fixed_meta = repair_concatenated_json(meta)
                    if fixed_meta:
                        meta = fixed_meta
                        dirty = True

            # Fix PARAMS
            try:
                json.loads(params)
            except json.JSONDecodeError as e:
                if "Extra data" in str(e):
                    print(f"  [FIXING] Params for {mid}")
                    fixed_params = repair_concatenated_json(params)
                    if fixed_params:
                        params = fixed_params
                        dirty = True
            
            if dirty:
                # Update the row
                clean_meta = meta.replace("'", "''")
                clean_params = params.replace("'", "''")
                sql = f"UPDATE model SET meta = '{clean_meta}', params = '{clean_params}' WHERE id = '{mid}';"
                update_cmd = [
                    'docker', 'exec', 'open-webui-db', 
                    'psql', '-U', 'openwebui', '-d', 'openwebui', 
                    '-c', sql
                ]
                subprocess.run(update_cmd, check=True)
                print(f"  [DONE] {mid} repaired.")
                
        print("\nDB Repair Complete. Please restart the open-webui container.")
                
    except Exception as e:
        print(f"Error during repair: {e}")

def repair_concatenated_json(s):
    # Try to find all JSON objects in string
    decoder = json.JSONDecoder()
    pos = 0
    objs = []
    while pos < len(s):
        try:
            obj, next_pos = decoder.raw_decode(s, pos)
            objs.append(obj)
            pos = next_pos
            # Skip any whitespace/noise between objects
            while pos < len(s) and s[pos].isspace():
                pos += 1
        except Exception:
            break
    
    if len(objs) > 1:
        # Merge all objects into one
        merged = {}
        for o in objs:
            if isinstance(o, dict):
                merged.update(o)
        return json.dumps(merged)
    return None

if __name__ == "__main__":
    fix_db()
