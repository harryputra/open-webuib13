#!/usr/bin/env bash
# =============================================================================
# Antigravity Open WebUI - rebuild after code/dependency changes
# Pakai script ini setelah ubah file frontend (.svelte/.ts), backend (.py),
# atau menambah package di package.json / backend/requirements.txt.
#
# Untuk install pertama kali, pakai run.sh. Script ini menganggap stack
# sudah pernah jalan (.env dan .webui_secret_key sudah ada).
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; CYAN='\033[0;36m'; NC='\033[0m'
info()  { echo -e "${GREEN}[rebuild]${NC} $*"; }
warn()  { echo -e "${YELLOW}[rebuild]${NC} $*"; }
err()   { echo -e "${RED}[rebuild]${NC} $*" >&2; }
title() { echo -e "${CYAN}==> $*${NC}"; }

# ---------------------------------------------------------------------------
# 0. Validasi state
# ---------------------------------------------------------------------------
if [ ! -f .env ]; then
    err ".env tidak ada — jalankan ./run.sh dulu untuk setup awal."
    exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
    err "Docker tidak ditemukan."
    exit 1
fi

if docker compose version >/dev/null 2>&1; then
    DC="docker compose"
elif command -v docker-compose >/dev/null 2>&1; then
    DC="docker-compose"
else
    err "docker compose plugin tidak ditemukan."
    exit 1
fi

# ---------------------------------------------------------------------------
# 1. Sinkronkan package-lock kalau package.json lebih baru
# ---------------------------------------------------------------------------
if [ -f package.json ]; then
    if [ ! -f package-lock.json ] || [ package.json -nt package-lock.json ]; then
        if command -v npm >/dev/null 2>&1; then
            title "package.json berubah — update package-lock.json..."
            npm install --package-lock-only --no-audit --no-fund
            info "package-lock.json sinkron."
        else
            warn "package.json lebih baru dari lock, tapi npm tidak ada di host."
            warn "Lewati update lock — Docker build mungkin error 'npm ci' kalau tidak sinkron."
        fi
    fi
fi

# ---------------------------------------------------------------------------
# 2. Rebuild image + recreate container
# ---------------------------------------------------------------------------
title "Build image (output progress di bawah)..."
echo
$DC build open-webui

title "Recreate container open-webui..."
$DC up -d --no-deps open-webui

# ---------------------------------------------------------------------------
# 3. Tunggu sampai healthy
# ---------------------------------------------------------------------------
PORT="$(grep -E '^OPEN_WEBUI_PORT=' .env 2>/dev/null | cut -d= -f2 | tr -d '\r' || echo 3013)"
PORT="${PORT:-3013}"

title "Menunggu open-webui healthy (akan retry sampai 5 menit)..."
HEALTHY=0
for i in $(seq 1 60); do
    STATUS="$(docker inspect open-webui --format '{{.State.Health.Status}}' 2>/dev/null || echo unknown)"
    if [ "$STATUS" = "healthy" ]; then
        HEALTHY=1
        break
    fi
    if [ "$STATUS" = "unhealthy" ]; then
        err "Container unhealthy. Cek log: $DC logs --tail=80 open-webui"
        $DC logs --tail=80 open-webui || true
        exit 1
    fi
    sleep 5
done

echo
$DC ps

if [ "$HEALTHY" = "1" ]; then
    info "✅ Rebuild selesai. Akses: http://localhost:${PORT}"
else
    warn "Timeout health check. Container mungkin masih warm-up."
    warn "Cek log realtime: $DC logs -f open-webui"
fi

# ---------------------------------------------------------------------------
# 3b. Auto re-register tools (idempotent, kalau .owui_token ada)
# ---------------------------------------------------------------------------
if [ "$HEALTHY" = "1" ] && [ -s .owui_token ]; then
    if command -v python3 >/dev/null 2>&1 || command -v python >/dev/null 2>&1; then
        PY=$(command -v python3 || command -v python)
        info "Re-register Antigravity tools (idempotent)..."
        OWUI_TOKEN=$(tr -d '\r\n' < .owui_token) \
        OWUI_BASE_URL="http://localhost:${PORT}" \
        "$PY" scripts/inject_super_tools.py || warn "Tool registration ada error, lanjut..."

        info "Refresh default persona 'Antigravity Local'..."
        OWUI_TOKEN=$(tr -d '\r\n' < .owui_token) \
        OWUI_BASE_URL="http://localhost:${PORT}" \
        "$PY" scripts/setup_default_persona.py || warn "Persona setup ada error, lanjut..."
    else
        warn "Python tidak ada di PATH. Skip re-register tools."
    fi
fi

# ---------------------------------------------------------------------------
# 4. Bersih-bersih image dangling (opsional, hemat disk)
# ---------------------------------------------------------------------------
DANGLING=$(docker images -f "dangling=true" -q 2>/dev/null | wc -l | tr -d ' ')
if [ "${DANGLING:-0}" -gt 0 ]; then
    info "Hapus ${DANGLING} dangling image hasil rebuild..."
    docker image prune -f >/dev/null
fi
