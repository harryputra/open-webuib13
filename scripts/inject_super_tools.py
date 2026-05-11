"""
Antigravity Super Tools — Master Injector
==========================================
Script untuk mendeploy SEMUA Antigravity Tools ke Open WebUI secara otomatis.
Mendukung create dan update (idempotent).

Usage:
    python scripts/inject_super_tools.py [--base-url URL] [--token TOKEN]

Atau set environment variables:
    OWUI_BASE_URL=http://localhost:3013
    OWUI_TOKEN=your_jwt_token
"""

import os
import sys
import io
import argparse
import requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# === Configuration ===
DEFAULT_BASE_URL = os.environ.get("OWUI_BASE_URL", "http://localhost:3013")
DEFAULT_TOKEN = os.environ.get("OWUI_TOKEN", "")

# === Tool Definitions ===
TOOLS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools")

TOOLS = [
    {
        "id": "antigravity_research_engine",
        "name": "🔬 Antigravity Research Engine",
        "description": "Mesin riset otonom v3.0 — pencarian akademik multi-sumber, sintesis literature review otomatis, ekstraksi PDF paper, deep web scraping, dan manajemen sitasi.",
        "file": "antigravity_research_engine.py",
    },
    {
        "id": "antigravity_book_engine",
        "name": "📖 Antigravity Book Engine",
        "description": "Mesin penulisan buku otonom v3.0 — outline generation, penulisan bab naratif, manajemen state multi-bab persisten, konsistensi checker, dan ekspor multi-format.",
        "file": "antigravity_book_engine.py",
    },
    {
        "id": "antigravity_code_engine",
        "name": "💻 Antigravity Code Engine",
        "description": "Mesin dev otonom v3.0 — eksekusi kode multi-bahasa, pencarian kode workspace-wide, manajemen dependensi (pip/npm), analisis kualitas, operasi Git.",
        "file": "antigravity_code_engine.py",
    },
    {
        "id": "antigravity_project_manager",
        "name": "📋 Antigravity Project Manager",
        "description": "Manajemen proyek otonom v3.0 — scaffolding (6 template), progress tracking, health scanning, changelog generation, dokumentasi otomatis.",
        "file": "antigravity_project_manager.py",
    },
    {
        "id": "antigravity_presenter_engine",
        "name": "🎤 Antigravity Presenter Engine",
        "description": "Mesin presentasi otonom v1.0 — generate slide Marp dari outline, simpan/list/edit deck, export ke PDF/PPTX/HTML/PNG, scaffold landing page HTML untuk live preview.",
        "file": "antigravity_presenter_engine.py",
    },
]


def read_tool_content(filename: str) -> str:
    filepath = os.path.join(TOOLS_DIR, filename)
    if not os.path.exists(filepath):
        print(f"  [ERROR] File not found: {filepath}")
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def inject_tool(base_url: str, headers: dict, tool_def: dict) -> bool:
    tool_id = tool_def["id"]
    content = read_tool_content(tool_def["file"])
    if content is None:
        return False

    payload = {
        "id": tool_id,
        "name": tool_def["name"],
        "meta": {"description": tool_def["description"]},
        "content": content,
    }

    # Check if tool exists
    r = requests.get(f"{base_url}/api/v1/tools/id/{tool_id}", headers=headers)

    if r.ok:
        # Update existing
        r2 = requests.post(
            f"{base_url}/api/v1/tools/id/{tool_id}/update",
            headers=headers,
            json=payload,
        )
        if r2.ok:
            print(f"  [UPDATED] {tool_def['name']}")
            return True
        else:
            print(f"  [FAIL] Update failed: {r2.status_code} — {r2.text[:200]}")
            return False
    else:
        # Create new
        r2 = requests.post(
            f"{base_url}/api/v1/tools/create",
            headers=headers,
            json=payload,
        )
        if r2.ok:
            print(f"  [CREATED] {tool_def['name']}")
            return True
        else:
            print(f"  [FAIL] Create failed: {r2.status_code} — {r2.text[:200]}")
            return False


def main():
    parser = argparse.ArgumentParser(description="Antigravity Super Tools Injector")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Open WebUI base URL")
    parser.add_argument("--token", default=DEFAULT_TOKEN, help="JWT auth token")
    parser.add_argument("--tool", default="all", help="Specific tool ID to inject, or 'all'")
    args = parser.parse_args()

    if not args.token:
        print("[ERROR] Token tidak tersedia. Set OWUI_TOKEN atau gunakan --token.")
        print("Dapatkan token dari Open WebUI → Settings → Account → API Keys.")
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {args.token}",
        "Content-Type": "application/json",
    }

    print("=" * 60)
    print("🌌 ANTIGRAVITY SUPER TOOLS — MASTER INJECTOR")
    print("=" * 60)
    print(f"Target: {args.base_url}")
    print(f"Tools dir: {TOOLS_DIR}")
    print()

    # Verify connection
    try:
        r = requests.get(f"{args.base_url}/api/config", timeout=10)
        if not r.ok:
            print(f"[WARN] Server returned {r.status_code}. Continuing anyway...")
    except Exception as e:
        print(f"[ERROR] Cannot connect to {args.base_url}: {e}")
        sys.exit(1)

    # Inject tools
    success = 0
    fail = 0
    tools_to_inject = TOOLS if args.tool == "all" else [t for t in TOOLS if t["id"] == args.tool]

    if not tools_to_inject:
        print(f"[ERROR] Tool '{args.tool}' not found.")
        sys.exit(1)

    for tool_def in tools_to_inject:
        print(f"\n🔧 Processing: {tool_def['name']}...")
        if inject_tool(args.base_url, headers, tool_def):
            success += 1
        else:
            fail += 1

    print("\n" + "=" * 60)
    print(f"✅ Sukses: {success} | ❌ Gagal: {fail} | Total: {len(tools_to_inject)}")
    print("=" * 60)

    if success > 0:
        print("\n💡 Langkah selanjutnya:")
        print("   1. Buka Open WebUI → Workspace → Tools")
        print("   2. Aktifkan tools pada model yang digunakan")
        print("   3. Mulai gunakan tools via chat!")


if __name__ == "__main__":
    main()
