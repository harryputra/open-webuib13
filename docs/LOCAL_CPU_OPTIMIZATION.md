# Local CPU Optimization — Antigravity Zenith

Mode operasi: **fully local, CPU-only, no GPU, no cloud, no token limit**.

Target hardware: laptop kelas i5/i7 ULV (4C/8T, 16-32GB RAM) — diuji di Intel i7-8650U + 32GB.

---

## TL;DR — One-shot setup

```bash
cd e:/AntiGravityProject/openwebui
scripts/local_cpu/setup_local_powerful.bat
```

Script akan:
1. Set env var Ollama (parallel, threads, KV cache, flash attention) — persistent.
2. Restart Ollama supaya env terbaca.
3. Pull base model (qwen2.5 0.5b/1.5b/3b + nomic-embed-text).
4. Create 4 profile CPU-tuned: `antigravity-fast`, `antigravity-balanced`, `antigravity-coder`, `antigravity-task`.
5. Mini-benchmark fast vs balanced.

Setelah selesai: restart container `docker compose restart open-webui`, buka `http://localhost:3013`.

---

## Apa yang berubah

### 1. Ollama server tuning (host-side env vars)

| Env var | Nilai | Alasan |
|---|---|---|
| `OLLAMA_NUM_PARALLEL` | `1` | CPU tidak punya parallelism gratis seperti GPU. 1 stream = throughput max. |
| `OLLAMA_MAX_LOADED_MODELS` | `2` | Chat model + embed model bisa coexist tanpa thrash. |
| `OLLAMA_NUM_THREAD` | `<jumlah core fisik>` | Hyperthreading malah slow di llama.cpp. 4C = 4 thread. |
| `OLLAMA_FLASH_ATTENTION` | `1` | Attention lebih cepat, hemat memory. |
| `OLLAMA_KV_CACHE_TYPE` | `q8_0` | KV cache di-quantize → hemat RAM ~50% tanpa loss berarti. |
| `OLLAMA_KEEP_ALIVE` | `30m` | Hindari cold-start tiap idle. |
| `OLLAMA_HOST` | `0.0.0.0:11434` | Reachable dari Docker container via `host.docker.internal`. |
| `OLLAMA_MAX_QUEUE` | `512` | Bursty request dari RAG/multi-tab tidak di-drop. |

Disetel persistent via `setx` (survive reboot).

### 2. Model profiles (CPU-tuned)

| Profile | Base | Konteks | Use case | Throughput target* |
|---|---|---|---|---|
| `antigravity-fast` | qwen2.5:1.5b | 4K | Chat ringkas, Q&A cepat | 25-40 tok/s |
| `antigravity-balanced` | qwen2.5:3b | 8K | Chat utama, RAG, web search, tools | 8-15 tok/s |
| `antigravity-coder` | qwen2.5:3b | 16K | Refactor, debugging, generate code | 6-12 tok/s |
| `antigravity-task` | qwen2.5:0.5b | 2K | Title/tag/autocomplete (background) | 50-80 tok/s |

\* Estimasi di i7-8650U. Lebih cepat di CPU yang lebih baru.

Semua profile pakai `temperature`, `top_k`, `top_p`, `repeat_penalty` yang sudah di-tune per use case.

### 3. `.env` changes

- `DEFAULT_MODELS=antigravity-balanced:latest,qwen2.5:3b` (fallback chain)
- `TASK_MODEL=antigravity-task:latest`
- `OLLAMA_KEEP_ALIVE=60m`, `AIOHTTP_CLIENT_TIMEOUT=900` — long generation tidak timeout
- `ENABLE_VERSION_UPDATE_CHECK=False`, `ENABLE_COMMUNITY_SHARING=False` — full offline
- Title/tag prompt template di-cap pendek supaya `antigravity-task` tetap instan

### 4. Web search (sudah ada — tinggal pakai)

SearXNG container = unlimited self-hosted meta-search (DuckDuckGo + Google + dst.). Tidak butuh API key, tidak ada rate limit. Aktif via `WEB_SEARCH_ENGINE=searxng`.

### 5. RAG (sudah ada — tinggal pakai)

- Embedding: `nomic-embed-text` (lokal via Ollama, 274MB).
- Hybrid search aktif (`ENABLE_RAG_HYBRID_SEARCH=True`).
- Vault: `E:\file_rag` (mount ke container as `/file_rag`).

---

## Cara pakai harian

### Start full stack
```bash
cd e:/AntiGravityProject/openwebui
docker compose up -d
```

### Pilih profile yang sesuai workload
- **Chat ngobrol biasa** → `antigravity-fast`
- **Riset / RAG / web search** → `antigravity-balanced` (default)
- **Coding / code review** → `antigravity-coder`
- **Background task** (auto) → `antigravity-task`

### Cek throughput
```bash
scripts/local_cpu/benchmark.bat
```

Output:
```
=== antigravity-fast ===
  load:        0.42s
  prompt-eval: 0.18s
  generate:    78 tok in 2.65s = 29.43 tok/s
```

### Re-tune profile
Edit Modelfile di `scripts/modelfiles/`, lalu:
```bash
ollama create antigravity-balanced -f scripts/modelfiles/Modelfile.antigravity-balanced
```

---

## Troubleshooting

### "Open WebUI tidak detect model antigravity-*"
- Cek `ollama list` — pastikan profile sudah ke-create.
- Restart Open WebUI: `docker compose restart open-webui`.
- Cek bahwa container bisa hit Ollama host: `docker exec open-webui curl -s http://host.docker.internal:11434/api/version`.

### "Container tidak bisa connect ke Ollama"
- Pastikan `OLLAMA_HOST=0.0.0.0:11434` (bukan `127.0.0.1:11434`) — re-run `optimize_ollama_cpu.bat`.
- Cek Windows Firewall: allow port 11434 inbound.

### "Generation lambat banget (< 3 tok/s)"
- Cek model size — `gemma4:latest` (9.6GB) atau `gpt-oss:20b` (13GB) terlalu besar untuk CPU. Pakai 3B family.
- Cek `OLLAMA_NUM_THREAD` — harus = jumlah **core fisik**, bukan logical.
- Tutup aplikasi lain yang makan CPU (Chrome dengan 50 tab dst.).

### "RAM penuh"
- Set `OLLAMA_MAX_LOADED_MODELS=1` (hanya 1 model di-load saat itu).
- Set `OLLAMA_KEEP_ALIVE=5m` (faster eviction).
- Atau pakai profile `fast` (1.5b) ganti `balanced` (3b).

### Mau revert ke setting lama
```bash
setx OLLAMA_NUM_PARALLEL ""
setx OLLAMA_MAX_LOADED_MODELS ""
setx OLLAMA_NUM_THREAD ""
setx OLLAMA_FLASH_ATTENTION ""
setx OLLAMA_KV_CACHE_TYPE ""
# restart Ollama
```
Lalu restore `.env` dari `.env.bak.YYYYMMDD_HHMMSS`.

---

## Roadmap optimasi lanjut

- [ ] Pull `qwen2.5-coder:1.5b` sebagai base alternatif `antigravity-coder`
- [ ] Tambah profile `antigravity-vision` (qwen2.5-vl atau llava 7b q4) untuk OCR/chart
- [ ] Switch SearXNG engine ke yang lebih lokal (`brave`, `qwant`) saat DDG/Google rate-limit
- [ ] Cache layer di nginx depan SearXNG untuk hit repeat query instan
- [ ] Pre-warm semua profile saat startup via `ollama run <name> ""` di run.bat
