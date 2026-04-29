"""
SAPBA RAG Auto-Sync Watcher
Monitors local folders and automatically uploads documents to Open WebUI Knowledge Bases.
"""
import os
import time
import json
import requests
import mimetypes

BASE_URL = 'http://localhost:3013'
TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjNiNDhhMWQ5LTc3NzAtNDQ0Ni05Mzg4LTQxOWU2ZDY5YzEwYSIsImV4cCI6MTc3OTQ5MTIzNywianRpIjoiN2Y3NjhlNmUtMjA0OC00NjMwLTk5NzgtMzM2YzU2ZWE5NThkIiwiaWF0IjoxNzc3MDcyMDM3fQ.eJ7VE_jfFilMPNwefsZNiPdM_drjnSCN5UgDxLFCoGg'
HEADERS = {'Authorization': f'Bearer {TOKEN}'}

WATCH_DIR = r'E:\AntiGravityProject\openwebui\rag_docs'
STATE_FILE = os.path.join(WATCH_DIR, 'sync_state.json')

# Map folder names to Open WebUI Knowledge Collection names and Descriptions
KB_MAPPING = {
    'Kurikulum': {'name': 'RAG_Kurikulum_Merdeka', 'desc': 'Dokumen CP dan Pedoman Kurikulum Merdeka'},
    'BSNP': {'name': 'RAG_Standar_BSNP', 'desc': 'Pedoman Penilaian 4 Pilar Kelayakan Buku Ajar'},
    'Bahasa': {'name': 'RAG_Pedoman_Bahasa', 'desc': 'PUEBI, EYD Edisi V, dan Pedoman Penulisan'},
}

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def get_or_create_kb(folder_name):
    kb_info = KB_MAPPING.get(folder_name)
    if not kb_info:
        return None
    
    # Check if exists
    r = requests.get(f'{BASE_URL}/api/v1/knowledge/', headers=HEADERS)
    if r.ok:
        kbs = r.json().get('items', [])
        for kb in kbs:
            if kb.get('name') == kb_info['name']:
                return kb['id']
                
    # Create new
    payload = {
        'name': kb_info['name'],
        'description': kb_info['desc'],
        'access_grants': []
    }
    r_create = requests.post(f'{BASE_URL}/api/v1/knowledge/create', headers=HEADERS, json=payload)
    if r_create.ok:
        print(f"[+] Created new Knowledge Base: {kb_info['name']}")
        return r_create.json()['id']
    else:
        print(f"[-] Failed to create KB {kb_info['name']}: {r_create.text}")
        return None

def upload_file_to_openwebui(file_path):
    print(f"[*] Uploading {os.path.basename(file_path)}...")
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = 'application/octet-stream'
        
    with open(file_path, 'rb') as f:
        files = {'file': (os.path.basename(file_path), f, mime_type)}
        # Must not send Content-Type header so requests sets multipart boundary correctly
        r = requests.post(f'{BASE_URL}/api/v1/files/', headers=HEADERS, files=files)
        
    if r.ok:
        file_id = r.json()['id']
        print(f"[+] Upload successful. File ID: {file_id}")
        return file_id
    else:
        print(f"[-] Upload failed: {r.text}")
        return None

def add_file_to_kb(kb_id, file_id):
    print(f"[*] Adding file {file_id} to KB {kb_id} (Extracting vectors, this may take a moment)...")
    h = HEADERS.copy()
    h['Content-Type'] = 'application/json'
    r = requests.post(
        f'{BASE_URL}/api/v1/knowledge/{kb_id}/file/add', 
        headers=h, 
        json={'file_id': file_id}
    )
    if r.ok:
        print(f"[+] File successfully embedded into Knowledge Base!")
        return True
    else:
        print(f"[-] Failed to add file to KB: {r.text}")
        return False

def sync_folders():
    if not os.path.exists(WATCH_DIR):
        print(f"Directory {WATCH_DIR} not found.")
        return

    state = load_state()
    kb_cache = {}
    
    for folder in os.listdir(WATCH_DIR):
        folder_path = os.path.join(WATCH_DIR, folder)
        if not os.path.isdir(folder_path) or folder not in KB_MAPPING:
            continue
            
        kb_id = kb_cache.get(folder)
        if not kb_id:
            kb_id = get_or_create_kb(folder)
            if kb_id:
                kb_cache[folder] = kb_id
            else:
                continue
                
        # Scan files
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if not os.path.isfile(file_path):
                continue
                
            # Check modification time to see if we need to upload
            mtime = os.path.getmtime(file_path)
            file_key = f"{folder}/{filename}"
            
            if file_key not in state or state[file_key]['mtime'] < mtime:
                file_id = upload_file_to_openwebui(file_path)
                if file_id:
                    success = add_file_to_kb(kb_id, file_id)
                    if success:
                        state[file_key] = {'mtime': mtime, 'file_id': file_id, 'kb_id': kb_id}
                        save_state(state)

if __name__ == '__main__':
    print(f"Starting SAPBA RAG Watcher...")
    print(f"Monitoring folder: {WATCH_DIR}")
    print(f"Press Ctrl+C to stop.")
    try:
        while True:
            sync_folders()
            time.sleep(10)  # Check every 10 seconds
    except KeyboardInterrupt:
        print("\nWatcher stopped.")
