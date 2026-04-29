import os
import sys
sys.path.append('e:/AntiGravityProject/openwebui/aae')
from aae_engine import AntigravityAutoresearchEngine

def run_audit():
    engine = AntigravityAutoresearchEngine()
    results = []

    print("\n=== STARTING AAE COMPREHENSIVE AUDIT ===\n")

    # --- TEST CASE 1: SUCCESSFUL GENERATION ---
    print("[Test 1] Testing Successful Generation (Gen 4)...")
    target = 'e:/AntiGravityProject/openwebui/aae/audit_target.py'
    # Inisialisasi file target
    with open(target, 'w') as f: f.write("# Initial State\n")
    
    code_success = "# Generation 4: Optimized Code\nprint('Success')"
    success = engine.start_experiment(
        generation=4,
        code_content=code_success,
        target_file=target,
        changes_summary="Audit Success Case: Valid code with passing tests.",
        test_cmd="python -c \"print('Test Passed')\""
    )
    results.append(f"Test 1 (Success Path): {'PASS' if success else 'FAIL'}")

    # --- TEST CASE 2: FAILED LOGIC & ROLLBACK ---
    print("\n[Test 2] Testing Failed Logic & Auto-Rollback (Gen 5)...")
    code_fail = "# Generation 5: Broken Code\nprint('Fail')"
    # Perintah tes yang sengaja gagal (exit 1)
    failed = engine.start_experiment(
        generation=5,
        code_content=code_fail,
        target_file=target,
        changes_summary="Audit Failure Case: Testing rollback mechanism.",
        test_cmd="python -c \"import sys; sys.exit(1)\""
    )
    
    # Verifikasi Rollback
    with open(target, 'r') as f:
        current_content = f.read()
    
    rollback_ok = "# Generation 4" in current_content
    results.append(f"Test 2 (Failure Path): {'PASS' if not failed else 'FAIL'}")
    results.append(f"Test 3 (Rollback Integrity): {'PASS' if rollback_ok else 'FAIL'}")

    # --- TEST CASE 4: LOG INTEGRITY ---
    log_exists = os.path.exists('e:/AntiGravityProject/openwebui/aae/history.log')
    results.append(f"Test 4 (Log Persistence): {'PASS' if log_exists else 'FAIL'}")

    # --- FINAL REPORT ---
    print("\n=== AUDIT REPORT ===")
    report_content = "# 🛡️ AAE Audit Report\n\n"
    report_content += f"**Date**: {os.popen('date /t').read().strip()}\n"
    report_content += "| Test Case | Result |\n|---|---|\n"
    for r in results:
        print(r)
        report_content += f"| {r.split(':')[0]} | {r.split(':')[1]} |\n"
    
    with open('e:/AntiGravityProject/openwebui/aae/test_results.md', 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print("\n[!] Audit results saved to aae/test_results.md")

if __name__ == "__main__":
    run_audit()
