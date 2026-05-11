# Deployment Guide — Antigravity Open WebUI

Panduan ini menjelaskan cara menjalankan Antigravity Open WebUI baik untuk
**development lokal (Windows)** maupun **deployment VPS (Linux)**.

Sistem ini dipaketkan via Docker Compose (open-webui + Postgres + Redis), dan
kedua script peluncur (`run.bat`, `run.sh`) sudah dirancang **idempotent** —
aman dijalankan berulang.

---

## TL;DR

| Kasus | Perintah |
|---|---|
| Windows (dev lokal) | klik dua kali `run.bat`, atau `run.bat` dari cmd |
| Linux/macOS/VPS | `bash run.sh` |

Akses di `http://localhost:3013` (default).

---

## Arsitektur Stack

`docker-compose.yaml` mengangkat tiga service:

| Service | Image | Fungsi |
|---|---|---|
| `open-webui` | dibuild dari `Dockerfile` | Aplikasi utama (FastAPI + SvelteKit) |
| `db` | `postgres:16-alpine` | Database utama |
| `redis` | `redis:7-alpine` | Session pool, socket, rate limit |

Volume yang dimount ke container `open-webui`:

| Host | Container | Keterangan |
|---|---|---|
| `open-webui` (named volume) | `/app/backend/data` | Data aplikasi (chats, knowledge, dll) |
| `/var/run/docker.sock` | `/var/run/docker.sock` | Untuk fitur terminal/eksekusi (admin) |
| `${WORKSPACE_DIR}` | `/workspace` | Root workspace (project Antigravity) |
| `${RAG_VAULT_PATH}` | `/file_rag` | Folder vault untuk RAG |

---

## 1. Deployment ke VPS Linux

### Prasyarat

- VPS dengan Ubuntu 20.04+/Debian 11+/RHEL 8+/CentOS Stream/Fedora
- Akses `sudo`
- Minimal **2 vCPU, 4 GB RAM, 20 GB disk** (CUDA tidak diperlukan untuk mode default CPU)
- Port 3013/tcp terbuka di Security Group / firewall

### Langkah

```bash
# 1. Clone repo
git clone <URL_REPO> AntiGravityProject
cd AntiGravityProject/openwebui

# 2. Beri permission eksekusi
chmod +x run.sh

# 3. Jalankan — sekali untuk semua urusan
bash run.sh
```

Apa yang dilakukan `run.sh` otomatis:

1. **Cek Docker** — kalau belum ada, tawarkan auto-install (Ubuntu/Debian/RHEL/CentOS/Fedora) lewat repo resmi Docker.
2. **Aktifkan daemon** — `systemctl enable --now docker`.
3. **Tambahkan user ke group `docker`** (best-effort; perlu logout/login agar aktif).
4. **Deteksi compose** — pilih `docker compose` v2 atau `docker-compose` v1.
5. **Generate `WEBUI_SECRET_KEY`** 64-karakter random, simpan di `.webui_secret_key` (`chmod 600`). Re-run tidak menimpa.
6. **Tulis `.env`** kalau belum ada, dengan default:
   - `OPEN_WEBUI_PORT=3013`
   - `WORKSPACE_DIR=$(parent dir)` — biasanya root `AntiGravityProject`
   - `RAG_VAULT_PATH=$WORKSPACE_DIR/file_rag`
7. **Buat folder bantu**: `projects/marp_slides`, `projects/live_preview`, RAG vault.
8. **`docker compose up -d --build`**.
9. **Tunggu health check** di `/health` (max ~3 menit).
10. **Tampilkan ringkasan**: URL lokal + URL publik (auto-deteksi IP via `api.ipify.org`), folder mount, perintah penting.

### Auto-start saat reboot

Sudah otomatis: setiap service di `docker-compose.yaml` punya `restart: unless-stopped`, dan Docker daemon di-enable lewat `systemctl` saat install.

### Membuka port di firewall

UFW (Ubuntu/Debian):
```bash
sudo ufw allow 3013/tcp
```

firewalld (RHEL/CentOS/Fedora):
```bash
sudo firewall-cmd --permanent --add-port=3013/tcp
sudo firewall-cmd --reload
```

Cloud provider (AWS/GCP/Azure/DigitalOcean): buka port di Security Group / Firewall console.

### HTTPS via reverse proxy (rekomendasi)

Pasang Nginx atau Caddy di depan, proxy ke `localhost:3013`. Contoh Caddyfile minimal:

```caddyfile
ai.example.com {
    reverse_proxy localhost:3013
}
```

Caddy mengurus TLS otomatis via Let's Encrypt. Untuk Nginx, gunakan `proxy_pass http://127.0.0.1:3013;` plus header `Upgrade`/`Connection` agar WebSocket jalan.

---

## 2. Development Lokal di Windows

### Prasyarat

- Docker Desktop terinstall dan **berjalan** (icon pojok kanan bawah hijau)
- PowerShell tersedia (default Windows)

### Langkah

Klik dua kali `run.bat`, atau dari cmd:

```bat
cd E:\AntiGravityProject\openwebui
run.bat
```

Apa yang dilakukan `run.bat`:

1. Cek Docker Desktop running.
2. Generate `WEBUI_SECRET_KEY` lewat PowerShell (`RandomNumberGenerator`) — sekali saja.
3. Tulis `.env` baru kalau belum ada (default `WORKSPACE_DIR=E:/AntiGravityProject`).
4. Buat folder bantu (`projects/marp_slides`, `projects/live_preview`, `E:\file_rag`).
5. `docker compose up -d --build`.
6. Buka browser ke `http://localhost:3013`.
7. Saat user pencet sembarang tombol → `docker compose down`. Tutup jendela tanpa pencet → container tetap jalan.

---

## 3. File `.env` — Variabel Penting

| Variable | Default | Fungsi |
|---|---|---|
| `OPEN_WEBUI_PORT` | `3013` | Port host yang dimap ke 8080 container |
| `WEBUI_SECRET_KEY` | auto-generate | Kunci JWT/session — **harus rahasia** |
| `WORKSPACE_DIR` | parent dir / `E:/AntiGravityProject` | Mount → `/workspace` |
| `WORKSPACE_MAX_FILE_SIZE` | `5242880` (5 MB) | Batas upload via workspace API |
| `RAG_VAULT_PATH` | `${WORKSPACE_DIR}/file_rag` atau `E:/file_rag` | Mount → `/file_rag` |
| `OLLAMA_BASE_URL` | `http://host.docker.internal:11434` | Endpoint Ollama (uncomment di `.env` kalau perlu override) |
| `WEBUI_DOCKER_TAG` | `latest` | Tag image |

`.env` **tidak ditimpa** oleh script setelah pertama dibuat — boleh diedit
manual untuk override.

---

## 4. Operasi Sehari-hari

Pakai dari folder `openwebui/`:

```bash
# Lihat log app realtime
docker compose logs -f open-webui

# Cek status semua service
docker compose ps

# Restart hanya app (tanpa rebuild)
docker compose restart open-webui

# Rebuild image setelah pull update kode
docker compose up -d --build

# Stop semua (data tetap aman di volume)
docker compose down

# Stop + HAPUS data app (volume open-webui)
docker compose down -v   # ⚠️ destruktif
```

### Update kode

```bash
git pull
docker compose up -d --build
```

### Backup data penting

Tiga lokasi data:

1. **Named volume `open-webui`** → data app (chats, knowledge, dll).
   ```bash
   docker run --rm -v open-webui:/data -v $(pwd):/backup alpine \
     tar czf /backup/openwebui-data-$(date +%F).tgz -C /data .
   ```
2. **Named volume `db_data`** → Postgres.
   ```bash
   docker compose exec db pg_dump -U openwebui openwebui \
     > backup-db-$(date +%F).sql
   ```
3. **`${WORKSPACE_DIR}` dan `${RAG_VAULT_PATH}`** → file biasa di host, backup pakai `tar`/`rsync`/`borg`.

---

## 5. Troubleshooting

### `docker compose` gagal: port 3013 sudah dipakai
Edit `.env`, ganti `OPEN_WEBUI_PORT` ke port lain (mis. `8080`), lalu:
```bash
docker compose up -d
```

### Health check timeout di `run.sh`
Cek log:
```bash
docker compose logs -f open-webui
```
Penyebab umum: build image masih jalan (image pertama bisa makan 5–10 menit), atau
Postgres belum ready. Tunggu 1–2 menit lalu refresh.

### Volume `/workspace` kosong di container
Pastikan `WORKSPACE_DIR` di `.env` mengarah ke folder yang **ada di host**.
Cek dari container:
```bash
docker compose exec open-webui ls -la /workspace
```

### Marp export PDF/PPTX gagal
Endpoint `/api/v1/antigravity/marp/export` butuh **Marp CLI**. Karena container
berjalan di image Open WebUI standar, install Marp CLI satu kali:
```bash
docker compose exec open-webui sh -c "npm install -g @marp-team/marp-cli"
```
Atau cukup pakai **Export HTML** dari UI — itu dirender di browser, tidak butuh
Marp CLI di server.

### User tidak bisa pakai `docker` tanpa `sudo` setelah install
`run.sh` sudah menambahkan user ke group `docker`, tapi efeknya baru aktif
setelah **logout & login kembali** (atau `newgrp docker`).

### Ganti secret key
```bash
rm .webui_secret_key
# edit .env, hapus baris WEBUI_SECRET_KEY=...
bash run.sh
```
Catatan: mengganti secret akan invalidasi semua session login yang ada.

---

## 6. Struktur Folder yang Ideal di VPS

```
/home/<user>/AntiGravityProject/
├── openwebui/              <- run.sh dijalankan dari sini
│   ├── run.sh
│   ├── docker-compose.yaml
│   ├── .env                <- auto-generate
│   ├── .webui_secret_key   <- auto-generate, chmod 600
│   ├── projects/
│   │   ├── marp_slides/    <- output Marp slide generator
│   │   └── live_preview/   <- artifact preview
│   └── ...
├── file_rag/               <- RAG vault (mount /file_rag)
├── si-tk/
├── kkn/
└── ...                     <- semua project lain bisa diakses dari /workspace
```

Dengan layout di atas, container Open WebUI bisa membaca/menulis semua project
Antigravity lain via `/workspace` (mis. fitur IDE, FileExplorer, save-preview,
Marp slide generator).

---

## 7. Endpoint Health & Monitoring

| Endpoint | Fungsi |
|---|---|
| `GET /health` | Status app (dipakai HEALTHCHECK Docker) |
| `GET /api/config` | Konfigurasi runtime (publik) |
| `docker compose ps` | Status container + port mapping |
| `docker stats` | CPU/memory realtime per container |

Untuk monitoring serius: aktifkan OpenTelemetry exporter via
`docker-compose.otel.yaml` (lihat file di root repo).
