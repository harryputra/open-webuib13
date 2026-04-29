import os
import time
import subprocess
from datetime import datetime

class AntigravityAutoresearchEngine:
    def __init__(self, workspace_path="e:/AntiGravityProject/openwebui/aae"):
        self.workspace = workspace_path
        self.log_path = os.path.join(self.workspace, "history.log")
        self.goal_path = os.path.join(self.workspace, "goal.md")
        
    def log_evolution(self, generation, changes, status, metric=0):
        """Mencatat setiap generasi ke dalam history.log dengan format Markdown Premium."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status_icon = "✅" if status == "SUCCESS" else "❌"
        
        entry = f"""
## 🧬 Generation {generation} | {timestamp}
- **Status**: {status_icon} {status}
- **Metric Score**: `{metric}/100`
- **Technical Changes**: 
  {changes}

---
"""
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(entry)
        print(f"[*] Evolution Log updated for Generation {generation}")

    def validate_syntax(self, file_path):
        """Melakukan pemeriksaan sintaks dasar berdasarkan ekstensi file."""
        ext = os.path.splitext(file_path)[1]
        try:
            if ext == ".py":
                with open(file_path, 'r', encoding='utf-8') as f:
                    source = f.read()
                compile(source, file_path, 'exec')
            # Untuk JS/HTML kita anggap OK jika bisa dibaca (atau tambahkan linter nanti)
            return True, "Validation OK"
        except Exception as e:
            return False, str(e)

    def run_functional_tests(self, test_cmd):
        """Menjalankan perintah pengujian dan mengembalikan skor keberhasilan."""
        try:
            print(f"[*] Running tests: {test_cmd}")
            result = subprocess.run(test_cmd, shell=True, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                return True, 100, "All tests passed."
            else:
                # Logika sederhana: jika ada error, hitung skor rendah
                return False, 40, result.stderr or result.stdout
        except Exception as e:
            return False, 0, str(e)

    def start_experiment(self, generation, code_content, target_file, changes_summary, test_cmd=None):
        """Menjalankan siklus eksperimen penuh dengan validasi dinamis."""
        print(f"[!] Starting Experiment: Generation {generation}")
        
        # 1. Backup
        backup_file = target_file + ".bak"
        if os.path.exists(target_file):
            with open(target_file, 'r', encoding='utf-8') as f:
                old_content = f.read()
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(old_content)
        
        # 2. Tulis kode baru
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(code_content)
            
        # 3. Validasi Sintaks
        syntax_ok, msg = self.validate_syntax(target_file)
        if not syntax_ok:
            return self._handle_failure(generation, f"Syntax Error: {msg}", target_file, backup_file, changes_summary)

        # 4. Validasi Fungsional (Jika ada perintah tes)
        metric_score = 85 # Skor dasar jika sintaks OK
        if test_cmd:
            test_ok, score, test_msg = self.run_functional_tests(test_cmd)
            metric_score = score
            if not test_ok:
                return self._handle_failure(generation, f"Functional Test Failed: {test_msg}", target_file, backup_file, changes_summary, metric_score)

        # 5. Success
        self.log_evolution(generation, changes_summary, "SUCCESS", metric=metric_score)
        print(f"[+] Generation {generation} successfully deployed with score {metric_score}.")
        return True

    def _handle_failure(self, generation, message, target_file, backup_file, changes_summary, metric=0):
        print(f"[-] Generation {generation} failed: {message}")
        if os.path.exists(backup_file):
            with open(backup_file, 'r', encoding='utf-8') as f_in:
                content = f_in.read()
            with open(target_file, 'w', encoding='utf-8') as f_out:
                f_out.write(content)
            print("[!] Rollback completed.")
        
        self.log_evolution(generation, f"Failed: {message}\n\nIntent: {changes_summary}", "FAILED", metric=metric)
        return False

if __name__ == "__main__":
    # Test initialization
    engine = AntigravityAutoresearchEngine()
    print("AAE Engine v1.0 Initialized.")
