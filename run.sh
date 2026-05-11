#!/usr/bin/env bash
# =============================================================================
# Antigravity Open WebUI - one-shot installer & launcher
# Cocok untuk VPS Linux (Ubuntu/Debian/RHEL/Fedora) maupun development lokal.
# Cukup jalankan:  bash run.sh
# =============================================================================
set -euo pipefail

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; CYAN='\033[0;36m'; NC='\033[0m'
info()  { echo -e "${GREEN}[run.sh]${NC} $*"; }
warn()  { echo -e "${YELLOW}[run.sh]${NC} $*"; }
err()   { echo -e "${RED}[run.sh]${NC} $*" >&2; }
title() { echo -e "${CYAN}==> $*${NC}"; }

SUDO=""
if [ "$(id -u)" -ne 0 ]; then
    if command -v sudo >/dev/null 2>&1; then
        SUDO="sudo"
    fi
fi

# ---------------------------------------------------------------------------
# 1. Pastikan Docker terpasang (auto-install di Linux jika perlu)
# ---------------------------------------------------------------------------
install_docker_linux() {
    title "Memasang Docker Engine..."
    if [ -f /etc/os-release ]; then
        # shellcheck disable=SC1091
        . /etc/os-release
    else
        err "Tidak bisa mendeteksi distro Linux (/etc/os-release tidak ada)."
        return 1
    fi

    case "${ID:-}" in
        ubuntu|debian|linuxmint|raspbian)
            $SUDO apt-get update -y
            $SUDO apt-get install -y ca-certificates curl gnupg
            $SUDO install -m 0755 -d /etc/apt/keyrings
            curl -fsSL "https://download.docker.com/linux/${ID}/gpg" \
                | $SUDO gpg --dearmor --yes -o /etc/apt/keyrings/docker.gpg
            $SUDO chmod a+r /etc/apt/keyrings/docker.gpg
            CODENAME="${VERSION_CODENAME:-$(lsb_release -cs 2>/dev/null || echo stable)}"
            echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/${ID} ${CODENAME} stable" \
                | $SUDO tee /etc/apt/sources.list.d/docker.list >/dev/null
            $SUDO apt-get update -y
            $SUDO apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
            ;;
        rhel|centos|rocky|almalinux|fedora)
            $SUDO dnf -y install dnf-plugins-core || $SUDO yum -y install yum-utils
            if command -v dnf >/dev/null 2>&1; then
                $SUDO dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
                $SUDO dnf -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
            else
                $SUDO yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
                $SUDO yum -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
            fi
            ;;
        *)
            err "Distro '${ID:-unknown}' belum di-handle script ini."
            err "Silakan pasang Docker manual: https://docs.docker.com/engine/install/"
            return 1
            ;;
    esac

    $SUDO systemctl enable --now docker
    info "Docker terpasang."
}

# ---------------------------------------------------------------------------
# 0. Cek Ollama + auto-pull model wajib + set env optimasi
# ---------------------------------------------------------------------------
ensure_ollama_models() {
    if ! command -v ollama >/dev/null 2>&1; then
        warn "Ollama tidak terpasang. Skip auto-pull model."
        warn "Tanpa Ollama, fitur lokal tidak jalan. Install: https://ollama.com/download"
        return 0
    fi
    title "Cek dan pull model wajib (idempotent)..."
    for m in nomic-embed-text:latest qwen2.5:0.5b qwen2.5:3b llama3.1:8b; do
        if ollama list 2>/dev/null | awk 'NR>1 {print $1}' | grep -qx "$m"; then
            info "Model $m sudah ada — skip."
        else
            info "Pulling $m ..."
            ollama pull "$m" || warn "Gagal pull $m, lanjut..."
        fi
    done

    # Hapus model cloud yang bukan free-unlimited (sesuai kriteria user)
    for c in deepseek-v4-pro:cloud deepseek-v3.1:671b-cloud gpt-oss:120b-cloud gpt-oss:20b-cloud; do
        if ollama list 2>/dev/null | awk 'NR>1 {print $1}' | grep -qx "$c"; then
            info "Hapus model cloud '$c' (bukan free unlimited)..."
            ollama rm "$c" >/dev/null 2>&1 || true
        fi
    done

    # Set env Ollama via systemd override (Linux) atau hint untuk Mac
    if [ "$(uname -s)" = "Linux" ] && [ -d /etc/systemd/system ]; then
        OVERRIDE_DIR="/etc/systemd/system/ollama.service.d"
        if [ -n "$SUDO" ] || [ "$(id -u)" -eq 0 ]; then
            $SUDO mkdir -p "$OVERRIDE_DIR"
            $SUDO tee "$OVERRIDE_DIR/antigravity.conf" >/dev/null <<EOF
[Service]
Environment="OLLAMA_NUM_CTX=4096"
Environment="OLLAMA_KEEP_ALIVE=30m"
Environment="OLLAMA_NUM_PARALLEL=1"
Environment="OLLAMA_FLASH_ATTENTION=1"
Environment="OLLAMA_KV_CACHE_TYPE=q8_0"
EOF
            $SUDO systemctl daemon-reload
            $SUDO systemctl restart ollama 2>/dev/null || true
            info "Env Ollama ter-set via systemd."
        else
            warn "Skip set env Ollama systemd (butuh sudo). Set manual di $OVERRIDE_DIR/antigravity.conf"
        fi
    elif [ "$(uname -s)" = "Darwin" ]; then
        warn "Mac: jalankan manual sekali untuk set env Ollama:"
        warn "  launchctl setenv OLLAMA_NUM_CTX 4096"
        warn "  launchctl setenv OLLAMA_KEEP_ALIVE 30m"
        warn "  launchctl setenv OLLAMA_KV_CACHE_TYPE q8_0"
        warn "  launchctl setenv OLLAMA_FLASH_ATTENTION 1"
        warn "Lalu restart Ollama app."
    fi
}

ensure_ollama_models

if ! command -v docker >/dev/null 2>&1; then
    warn "Docker belum terpasang."
    if [ "$(uname -s)" = "Linux" ]; then
        read -r -p "Pasang Docker sekarang? [Y/n] " ans
        ans="${ans:-Y}"
        if [[ "$ans" =~ ^[Yy]$ ]]; then
            install_docker_linux
        else
            err "Dibatalkan. Pasang Docker dulu lalu jalankan ulang."
            exit 1
        fi
    else
        err "Pasang Docker Desktop dulu: https://docs.docker.com/get-docker/"
        exit 1
    fi
fi

# Pastikan daemon hidup
if ! docker info >/dev/null 2>&1; then
    if [ -n "$SUDO" ]; then
        warn "Docker daemon tidak menyala — coba start..."
        $SUDO systemctl start docker || true
    fi
    if ! docker info >/dev/null 2>&1; then
        err "Docker daemon belum running. Jalankan: sudo systemctl start docker"
        exit 1
    fi
fi

# Tambahkan user ke group docker (best-effort, butuh re-login agar aktif)
if [ -n "$SUDO" ] && getent group docker >/dev/null 2>&1; then
    if ! id -nG "$USER" 2>/dev/null | tr ' ' '\n' | grep -qx docker; then
        warn "User '$USER' belum di group 'docker'. Menambahkan (logout/login agar aktif)..."
        $SUDO usermod -aG docker "$USER" || true
    fi
fi

# Detect docker compose v2 vs v1
if docker compose version >/dev/null 2>&1; then
    DC="docker compose"
elif command -v docker-compose >/dev/null 2>&1; then
    DC="docker-compose"
else
    err "docker compose plugin tidak ditemukan."
    err "Install: $SUDO apt-get install -y docker-compose-plugin"
    exit 1
fi
info "Compose: $DC"

# ---------------------------------------------------------------------------
# 2. Generate WEBUI_SECRET_KEY (sekali saja, simpan di .webui_secret_key)
# ---------------------------------------------------------------------------
SECRET_FILE=".webui_secret_key"
if [ ! -s "$SECRET_FILE" ]; then
    if command -v openssl >/dev/null 2>&1; then
        openssl rand -hex 32 > "$SECRET_FILE"
    else
        head -c 256 /dev/urandom | tr -dc 'a-f0-9' | head -c 64 > "$SECRET_FILE"
    fi
    chmod 600 "$SECRET_FILE"
    info "WEBUI_SECRET_KEY baru disimpan di $SECRET_FILE"
fi
GENERATED_SECRET="$(cat "$SECRET_FILE")"

# ---------------------------------------------------------------------------
# 3. Tulis .env jika belum ada (default cocok untuk VPS Linux)
# ---------------------------------------------------------------------------
DEFAULT_WORKSPACE="$(cd .. 2>/dev/null && pwd || echo "$SCRIPT_DIR")"
DEFAULT_RAG="${DEFAULT_WORKSPACE}/file_rag"

if [ ! -f .env ]; then
    title "Membuat .env baru..."
    cat > .env <<EOF
# Generated by run.sh on $(date -u +"%Y-%m-%dT%H:%M:%SZ")

OPEN_WEBUI_PORT=3013
WEBUI_SECRET_KEY=${GENERATED_SECRET}

# Telemetry off
SCARF_NO_ANALYTICS=true
DO_NOT_TRACK=true
ANONYMIZED_TELEMETRY=false

# Folders yang di-mount
WORKSPACE_DIR=${DEFAULT_WORKSPACE}
WORKSPACE_MAX_FILE_SIZE=5242880
RAG_VAULT_PATH=${DEFAULT_RAG}

# Ollama
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_KEEP_ALIVE=30m

# RAG via Ollama (kenceng + lokal)
RAG_EMBEDDING_ENGINE=ollama
RAG_EMBEDDING_MODEL=nomic-embed-text:latest
RAG_OLLAMA_BASE_URL=http://host.docker.internal:11434
ENABLE_RAG_HYBRID_SEARCH=True
CHUNK_SIZE=1500
CHUNK_OVERLAP=200
RAG_TOP_K=5

# Task model (title/tag/autocomplete) - super kecil biar gak rebut VRAM
TASK_MODEL=qwen2.5:0.5b
TASK_MODEL_EXTERNAL=qwen2.5:0.5b
ENABLE_TAGS_GENERATION=True
ENABLE_AUTOCOMPLETE_GENERATION=True

# Websocket + Redis (multi-tab sync)
ENABLE_WEBSOCKET_SUPPORT=True
WEBSOCKET_MANAGER=redis
WEBSOCKET_REDIS_URL=redis://redis:6379/0
EOF
    info ".env dibuat. Workspace = ${DEFAULT_WORKSPACE}"
else
    info ".env sudah ada — tidak ditimpa."
fi

# Load .env supaya variabel terpakai juga oleh script ini
set -a
# shellcheck disable=SC1091
. ./.env
set +a

# ---------------------------------------------------------------------------
# 4. Pastikan folder workspace, RAG, dan output project sudah ada
# ---------------------------------------------------------------------------
mkdir -p "${WORKSPACE_DIR:-$DEFAULT_WORKSPACE}"
mkdir -p "${RAG_VAULT_PATH:-$DEFAULT_RAG}"
mkdir -p "${SCRIPT_DIR}/projects/marp_slides"
mkdir -p "${SCRIPT_DIR}/projects/live_preview"

# ---------------------------------------------------------------------------
# 5. Build & start
# ---------------------------------------------------------------------------
title "Build & start container (mode detached)..."
$DC up -d --build

# ---------------------------------------------------------------------------
# 6. Tunggu health check
# ---------------------------------------------------------------------------
PORT="${OPEN_WEBUI_PORT:-3013}"
title "Menunggu Open WebUI siap di http://localhost:${PORT} ..."
HEALTHY=0
for i in $(seq 1 90); do
    if curl -sf "http://localhost:${PORT}/health" >/dev/null 2>&1; then
        HEALTHY=1
        break
    fi
    sleep 2
done

if [ "$HEALTHY" = "1" ]; then
    info "Open WebUI siap."
else
    warn "Timeout health check. Cek log: $DC logs -f open-webui"
fi

# ---------------------------------------------------------------------------
# 6b. Auto-register Antigravity tools (idempotent, butuh .owui_token)
# ---------------------------------------------------------------------------
register_tools() {
    if [ "$HEALTHY" != "1" ]; then return 0; fi
    if [ ! -s .owui_token ]; then
        echo
        info "AUTO-REGISTER TOOLS belum aktif - butuh JWT token sekali setup."
        info "Cara aktifin:"
        info "  1. Buka http://localhost:${PORT} - Settings - Account - API Keys"
        info "  2. Klik 'Create new key', salin token-nya"
        info "  3. echo 'TOKEN_DI_SINI' > .owui_token"
        info "  4. Jalankan ulang ./run.sh - tools auto register"
        return 0
    fi
    if ! command -v python3 >/dev/null 2>&1 && ! command -v python >/dev/null 2>&1; then
        warn "Python tidak ada di PATH. Skip auto-register tools."
        return 0
    fi
    PY=$(command -v python3 || command -v python)
    info "Registering Antigravity tools..."
    OWUI_TOKEN=$(tr -d '\r\n' < .owui_token) \
    OWUI_BASE_URL="http://localhost:${PORT}" \
    "$PY" scripts/inject_super_tools.py || warn "Tool registration ada error, lanjut..."

    info "Setup default persona 'Antigravity Local'..."
    OWUI_TOKEN=$(tr -d '\r\n' < .owui_token) \
    OWUI_BASE_URL="http://localhost:${PORT}" \
    "$PY" scripts/setup_default_persona.py || warn "Persona setup ada error, lanjut..."
}

register_tools

# ---------------------------------------------------------------------------
# 7. Ringkasan
# ---------------------------------------------------------------------------
echo
title "Status container:"
$DC ps

PUBLIC_IP="$(curl -s --max-time 3 https://api.ipify.org 2>/dev/null || true)"
cat <<EOF

==============================================================
${GREEN}✅ Open WebUI (Antigravity) sudah jalan${NC}
   URL lokal : http://localhost:${PORT}
$( [ -n "$PUBLIC_IP" ] && echo "   URL publik: http://${PUBLIC_IP}:${PORT}" )

   Workspace : ${WORKSPACE_DIR:-$DEFAULT_WORKSPACE}  -> /workspace
   RAG vault : ${RAG_VAULT_PATH:-$DEFAULT_RAG}  -> /file_rag
   Secret    : ${SECRET_FILE} (chmod 600)

Auto-start saat reboot: aktif (restart: unless-stopped di compose).
Pastikan firewall/Security Group VPS membuka port ${PORT}/tcp.

Perintah berguna:
   ${DC} logs -f open-webui    # tail log app
   ${DC} ps                    # cek status
   ${DC} restart open-webui    # restart app
   ${DC} down                  # stop semua service
   ${DC} up -d --build         # rebuild + restart
==============================================================
EOF
