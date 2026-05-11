"""
Antigravity Default Persona Setup
==================================
Bikin/refresh persona "🌌 Antigravity Local" — model default dengan SEMUA tools attached.
User tinggal pilih dari dropdown, gak perlu mikir.

Idempotent — aman di-run berulang. Update kalau sudah ada.

Usage:
    OWUI_TOKEN=xxx python scripts/setup_default_persona.py
    OR
    python scripts/setup_default_persona.py --token xxx
"""

import os
import sys
import io
import argparse
import urllib.request
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

DEFAULT_BASE_URL = os.environ.get("OWUI_BASE_URL", "http://localhost:3013")
DEFAULT_TOKEN = os.environ.get("OWUI_TOKEN", "")

PERSONA_ID = "antigravity-local"
PERSONA_NAME = "🌌 Antigravity Local"
# Smart fallback chain — pakai model pertama yang tersedia di Ollama.
# Kalau semua gagal, default ke item terakhir (asumsinya pasti ada).
BASE_MODEL_PREFERENCES = ["qwen2.5:3b", "llama3.1:8b", "gemma4:e2b", "phi3:mini"]

ALL_TOOLS = [
    "antigravity_research_engine",
    "antigravity_book_engine",
    "antigravity_code_engine",
    "antigravity_project_manager",
    "antigravity_presenter_engine",
    "antigravity_auto_coding_engine",
    "sapba_web_researcher",
    "sapba_image_generator",
    "sapba_docx_exporter",
]

SYSTEM_PROMPT = """Kamu adalah Antigravity Local — asisten AI lokal milik Harry Putra Saputra (dosen POLMAN Bandung) yang jalan 100% di laptop tanpa internet, tanpa limit, gratis selamanya.

Aturan:
1. Bahasa Indonesia yang jelas, ramah-tegas, to-the-point. Hindari basa-basi.
2. Manfaatkan tools yang tersedia waktu user minta action konkret:
   - Bikin slide presentasi → pakai antigravity_presenter_engine
   - Riset web / cari sumber → pakai sapba_web_researcher
   - Cari/baca/tulis file kode → pakai antigravity_code_engine
   - Riset literatur akademik → pakai antigravity_research_engine
   - Tulis buku/bab panjang → pakai antigravity_book_engine
   - Manage proyek baru → pakai antigravity_project_manager
3. Kalau user minta sesuatu yang ambigu (judul belum jelas, format belum jelas), tanya 1-2 hal singkat dulu, jangan asumsi.
4. Setelah eksekusi tool, ringkas hasil dalam 1-2 paragraf — kasih tahu user file disimpan dimana atau apa langkah selanjutnya.
5. Konteks utama user: dosen + dev gov systems (puskesmas, KKN, UMKM, sekolah). Asumsikan audience mahasiswa atau staf instansi pemerintah saat bikin materi.
"""


def call(method: str, path: str, token: str, base_url: str, body=None):
    url = base_url + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            raw = r.read().decode("utf-8")
            return r.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return 0, {"error": str(e)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--token", default=DEFAULT_TOKEN)
    args = parser.parse_args()

    if not args.token:
        print("[ERROR] OWUI_TOKEN tidak tersedia. Set env atau pakai --token.")
        sys.exit(1)

    base_url = args.base_url

    # Pilih base model dari fallback chain — ambil yang ada di Ollama list
    chosen_base = BASE_MODEL_PREFERENCES[-1]  # default fallback
    try:
        import subprocess
        ollama_out = subprocess.check_output(
            ["ollama", "list"], text=True, timeout=10
        )
        installed_models = {
            line.split()[0] for line in ollama_out.splitlines()[1:] if line.strip()
        }
        for candidate in BASE_MODEL_PREFERENCES:
            if candidate in installed_models:
                chosen_base = candidate
                break
        print(f"[INFO] Base model dipilih: {chosen_base}")
        if chosen_base != BASE_MODEL_PREFERENCES[0]:
            print(
                f"[INFO] Catatan: ideal-nya pakai {BASE_MODEL_PREFERENCES[0]}. "
                f"Setelah pull selesai, jalankan ulang script ini untuk upgrade."
            )
    except Exception as e:
        print(f"[WARN] Gak bisa cek ollama list ({e}). Pakai default: {chosen_base}")

    print("=" * 60)
    print("🌌 ANTIGRAVITY DEFAULT PERSONA SETUP")
    print("=" * 60)
    print(f"Target: {base_url}")
    print(f"Persona ID: {PERSONA_ID}")
    print(f"Base model: {chosen_base}")
    print(f"Tools to attach: {len(ALL_TOOLS)}")
    print()

    # Cek tools yang benar-benar terdaftar (filter ALL_TOOLS biar gak error attach yang gak ada)
    status, registered = call("GET", "/api/v1/tools/", args.token, base_url)
    if status != 200:
        print(f"[WARN] Gagal fetch tools registry (HTTP {status}). Lanjut dengan list default.")
        actual_tools = ALL_TOOLS
    else:
        registered_ids = {t["id"] for t in registered}
        actual_tools = [t for t in ALL_TOOLS if t in registered_ids]
        missing = [t for t in ALL_TOOLS if t not in registered_ids]
        if missing:
            print(f"[INFO] Tools belum registered ({len(missing)}): {', '.join(missing)}")
            print(f"[INFO] Akan attach yang ada saja ({len(actual_tools)}).")

    payload = {
        "id": PERSONA_ID,
        "name": PERSONA_NAME,
        "base_model_id": chosen_base,
        "meta": {
            "profile_image_url": "/static/favicon.png",
            "description": f"Asisten lokal full gratis tanpa limit. Semua tools Antigravity di-attach. Berbasis {chosen_base}.",
            "capabilities": {
                "vision": False,
                "citations": True,
                "usage": False,
            },
            "toolIds": actual_tools,
            "tags": [{"name": "lokal"}, {"name": "default"}, {"name": "full-tools"}],
        },
        "params": {
            "system": SYSTEM_PROMPT,
            "temperature": 0.7,
            "num_ctx": 4096,
            "num_predict": -1,
        },
    }

    # Cek persona sudah ada belum
    status, existing = call("GET", f"/api/v1/models/model?id={PERSONA_ID}", args.token, base_url)

    if status == 200 and existing:
        print(f"[INFO] Persona '{PERSONA_ID}' sudah ada — UPDATE.")
        status, _ = call("POST", "/api/v1/models/model/update", args.token, base_url, payload)
        action = "UPDATED"
    else:
        print(f"[INFO] Persona '{PERSONA_ID}' belum ada — CREATE.")
        status, _ = call("POST", "/api/v1/models/create", args.token, base_url, payload)
        action = "CREATED"

    if 200 <= status < 300:
        print(f"[OK] Persona {action}: {PERSONA_NAME}")
        print(f"     Tools attached: {len(actual_tools)}")
        print(f"     Base: {chosen_base}")
        print()
        print("Buka Open WebUI → pilih '🌌 Antigravity Local' di dropdown model.")
    else:
        print(f"[FAIL] HTTP {status} saat {action}.")
        sys.exit(1)


if __name__ == "__main__":
    main()
