import os

def test_ui_version():
    target_file = 'e:/AntiGravityProject/openwebui/antigravity_ui_fix.js'
    if not os.path.exists(target_file):
        return False, "File tidak ditemukan."
    
    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if "AAE: Gen 3" in content:
        return True, "Versi UI terverifikasi: Gen 3."
    else:
        return False, "Versi UI salah atau tidak terupdate."

if __name__ == "__main__":
    success, msg = test_ui_version()
    if success:
        print(msg)
        exit(0)
    else:
        print(f"ERROR: {msg}")
        exit(1)
