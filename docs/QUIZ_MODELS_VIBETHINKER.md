# Generator Soal Kuis (TriniQ) — VibeThinker-3B + qwen2.5:3b

Panduan menambahkan model untuk **generate soal** di server **Dell PowerEdge T160**
(Proxmox → VM Linux, **CPU-only, RAM 8GB**).

## Strategi 2 model (soal campuran STEM + umum)

| Jenis soal | Model | Alasan |
|---|---|---|
| Matematika / STEM / coding (jawaban bisa diverifikasi) | `hf.co/oussaber/VibeThinker-3B-Q4_K_M-GGUF` | Fine-tune Qwen2.5-Coder-3B untuk reasoning verifiable. Bisa generate soal **sekaligus** verifikasi jawaban. |
| Pengetahuan umum / Bahasa Indonesia / campuran | `qwen2.5:3b` | Instruct, cepat, Bahasa Indonesia rapi, output JSON bersih. |

> **Catatan jujur soal VibeThinker:** ini model *reasoning* — selalu keluarkan
> rantai berpikir (CoT) panjang sebelum jawaban, **tidak mendukung tool use**, dan
> lemah untuk prosa umum/Indonesia. Di CPU bisa **30 dtk–2 menit per soal**. Pakai
> hanya untuk soal STEM yang jawabannya bisa diverifikasi; sisanya pakai qwen2.5:3b.

## Batasan 8GB — wajib dipatuhi

- `OLLAMA_MAX_LOADED_MODELS=1` → cuma 1 model di RAM, swap otomatis saat ganti model.
  (Sudah di-set otomatis oleh `run.sh` saat RAM < 16GB.)
- **Jangan build image di VM** (frontend build butuh heap ~4GB → OOM). Build di laptop
  32GB, transfer image-nya. Lihat langkah di bawah.
- Postgres `shared_buffers` & Redis cap sudah diturunkan di `docker-compose.yaml`.

---

## Langkah deploy di server (runbook)

### A. Build image di laptop (32GB), transfer ke server

```bash
# --- di laptop (Windows Git Bash / WSL), folder openwebui ---
docker compose build open-webui
docker save openwebui/open-webui:latest | gzip > owui.tar.gz
scp owui.tar.gz trin@<IP_VM>:/home/trin/

# --- di VM Linux ---
gunzip -c ~/owui.tar.gz | docker load
```

### B. Pasang Ollama (native di VM) + tuning

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

`run.sh` akan menulis tuning Ollama (termasuk `OLLAMA_HOST=0.0.0.0:11434` agar
container bisa akses, dan `OLLAMA_MAX_LOADED_MODELS=1`) ke systemd override.

### C. Copy project + sesuaikan `.env`

```bash
# copy folder openwebui ke /home/trin/docker/apps/openwebui/ (git clone / scp / rsync)
cd /home/trin/docker/apps/openwebui
cp .env.example .env   # atau biarkan run.sh generate .env minimal
```

Edit `.env` untuk server (path Linux, bukan E:\...):

```env
OPEN_WEBUI_PORT=3013
WORKSPACE_DIR=/home/trin/workspace
RAG_VAULT_PATH=/home/trin/file_rag
OLLAMA_BASE_URL=http://host.docker.internal:11434
DEFAULT_MODELS=qwen2.5:3b
# Hemat RAM (opsional, default sudah aman):
PG_SHARED_BUFFERS=192MB
PG_EFFECTIVE_CACHE=512MB
REDIS_MAXMEMORY=192mb
```

> **Ganti `WEBUI_SECRET_KEY`** dengan nilai baru (`openssl rand -hex 32`). Jangan
> pakai secret dari laptop. Hapus `GITHUB_TOKEN` kalau tidak dipakai di server.

### D. Jalankan (tanpa build, image sudah di-load)

```bash
chmod +x run.sh
./run.sh
# run.sh akan: pull model (qwen2.5:3b + VibeThinker-3B), set tuning Ollama, up -d stack.
```

Kalau image custom sudah di-load, ubah baris start agar **tidak rebuild** di server:
`docker compose up -d` (bukan `up -d --build`). Untuk amannya, edit `docker-compose.yaml`
di server → komentari `build: .` supaya selalu pakai image hasil `docker load`.

### E. Verifikasi

```bash
# Ollama jalan & reachable?
curl -s http://localhost:11434/api/tags | grep -o '"name":"[^"]*"'

# Open WebUI sehat?
curl -sf http://localhost:3013/health && echo "  OWUI OK"

# Model ada?
ollama list | grep -iE "vibethinker|qwen2.5:3b"
```

Buka `http://<IP>:3013` → model muncul otomatis di dropdown.

---

## Preset Workspace (system prompt generate soal)

Di Open WebUI: **Workspace → Models → +** → pilih base model → isi system prompt.

### Preset 1 — "Soal Umum" (base: `qwen2.5:3b`)

```
Kamu generator soal kuis Bahasa Indonesia untuk aplikasi TriniQ.
Tugas: buat soal pilihan ganda sesuai topik & tingkat kesulitan yang diminta.
WAJIB balas HANYA JSON valid (tanpa teks lain, tanpa markdown fence), format:
{
  "soal": [
    {
      "pertanyaan": "...",
      "opsi": {"A":"...","B":"...","C":"...","D":"..."},
      "jawaban": "A",
      "pembahasan": "penjelasan singkat 1-2 kalimat"
    }
  ]
}
Bahasa Indonesia baku. Jangan ada opsi yang ambigu. Satu jawaban benar per soal.
```

### Preset 2 — "Soal STEM" (base: `VibeThinker-3B`)

VibeThinker berpikir panjang dulu, jadi minta JSON di **akhir** dan set parameter
agar tidak kepanjangan:

```
Kamu generator soal MATEMATIKA/STEM untuk TriniQ. Hitung & verifikasi jawaban
dengan teliti sebelum menulis soal. Boleh berpikir panjang, TAPI di akhir keluarkan
blok terakhir berupa JSON valid (diawali baris ```json) berisi:
{
  "soal": [
    {"pertanyaan":"...","opsi":{"A":"...","B":"...","C":"...","D":"..."},
     "jawaban":"A","pembahasan":"langkah ringkas + hasil"}
  ]
}
Pastikan "jawaban" benar secara matematis (sudah kamu verifikasi).
```

Saran parameter VibeThinker (di Advanced Params preset): `temperature 0.6`,
`top_p 0.95`, `num_ctx 4096`, `num_predict 2048` (batasi panjang CoT).

---

## Integrasi ke aplikasi TriniQ

Open WebUI mengekspos **API OpenAI-compatible**. Dari TriniQ panggil:

```
POST http://<IP>:3013/api/chat/completions
Authorization: Bearer <API_KEY dari Settings → Account → API Keys>
Content-Type: application/json

{
  "model": "VibeThinker-3B",        // atau "qwen2.5:3b" / nama preset
  "messages": [{"role":"user","content":"Buat 5 soal aljabar SMA tingkat sedang"}],
  "stream": false
}
```

Atau langsung ke Ollama (`http://<IP>:11434/api/generate`) jika TriniQ tidak butuh
fitur Open WebUI. Untuk batch generate soal, **panggil berurutan** (jangan paralel)
karena `OLLAMA_MAX_LOADED_MODELS=1` di 8GB.

## Troubleshooting

- **Open WebUI tak lihat model** → cek `OLLAMA_HOST=0.0.0.0:11434` aktif
  (`sudo systemctl show ollama | grep OLLAMA_HOST`) lalu `systemctl restart ollama`.
- **OOM / server berat** → pastikan `OLLAMA_MAX_LOADED_MODELS=1`; pertimbangkan
  matikan SearXNG kalau web search tak dipakai (hemat ~250MB).
- **VibeThinker lambat banget** → wajar di CPU; turunkan `num_predict`, atau pakai
  qwen2.5:3b untuk soal yang tidak butuh verifikasi matematis.
- **Build OOM di server** → jangan build di VM; pakai `docker load` dari laptop (langkah A).
