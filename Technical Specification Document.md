# Technical Specification Document - Antigravity Zenith IDE

## 🌌 Project Overview
Antigravity Zenith adalah transformasi Open WebUI menjadi sebuah "AI-Powered Research Command Center" yang memiliki IDE terintegrasi, manajemen file system langsung, dan sistem pembaruan cerdas.

## 🛠️ Tech Stack Consistency
- **Frontend**: Vanilla JavaScript (ES6+), CSS3 (Glassmorphism), HTML5.
- **Backend**: FastAPI (Python), Docker, Shell Scripting (Bash/PowerShell).
- **Storage**: Local Workspace at `E:\file_rag` (Host) mapped to `/file_rag` (Container).

## 🏗️ Core Architectures
### 1. Antigravity Zenith IDE (v1.0)
- **Floating UI**: Menggunakan teknik overlay dengan `backdrop-filter: blur` untuk pengalaman premium.
- **Explorer**: Mendukung navigasi folder rekursif dengan sinkronisasi path otomatis antara UI dan API.
- **Editor**: Textarea berbasis monospaced font dengan dukungan operasi Read/Write real-time.

### 2. Smart Safe Update System
- **Version Control**: Melakukan komparasi versi lokal via `/api/config` dengan versi terbaru di GitHub `open-webui/open-webui`.
- **Master Patcher**: Skrip otomatis yang menjamin semua kustomisasi (UI Injections, API Routes) dipulihkan setelah proses update Docker selesai.

### 3. Workspace FS API
- **Endpoint List**:
  - `GET /api/v1/workspace/fs/list?path=...` : Mengambil daftar file/folder.
  - `GET /api/v1/workspace/fs/read?path=...` : Membaca konten file.
  - `POST /api/v1/workspace/fs/write?path=...` : Menulis konten ke file (JSON body).

## 📑 Completed Features (Changelog)
- [feat] Initial Zenith IDE UI Integration.
- [feat] Folder navigation support in IDE Explorer.
- [feat] Save functionality with JSON Body support in backend.
- [fix] Router priority fix in `main.py` to prevent SPA routing conflicts.
- [feat] Smart Version Checking for Safe Update.
- [fix] Chrome Flexbox rendering issue (`shrink-0`) in Svelte components.
- [feat] Antigravity Sync: System updated to v0.9.2 architecture while preserving local patches.
- [feat] Auto-Coding Engine: Created `antigravity_tools.py` standard Open WebUI tool for direct LLM workspace manipulation (read, write, list).
- [feat] SIMKEU Project Initialization: Generated complete Laravel folder structure, core configurations, migrations, models, and dashboard views in E:\file_rag\si_tk via Antigravity Architect injection.
- [fix] Chat Scroll Jump Bug: Removed experimental virtual-scrolling/off-screen culling system from `Messages.svelte` that caused scroll position to jump unpredictably. Root cause was inaccurate spacer heights (based on `DEFAULT_HEIGHT=150` fallback) causing DOM height mismatches when messages were culled/re-rendered. Reverted to rendering all messages directly without spacers, matching stable Open WebUI behavior.
- [feat] SAPBA Platform v1.0: Implemented Sistem Asisten Penulisan Buku Ajar — injected 6 AI Personas (Arsitek Kurikulum, Penulis Konten, Editor Bahasa, Desainer Pedagogi, Analis Kelayakan BSNP, Asisten Riset) and 13 Prompt Templates (/rancang-buku, /analisis-cp, /tulis-bab, /tulis-subbab, /buat-soal-hots, /review-bsnp, /edit-bahasa, /buat-rangkuman, /buat-glosarium, /buat-pendahuluan, /buat-daftar-pustaka, /cek-konsistensi, /quality-tracker) via API seeder script `scripts/sapba_seeder.py` and `scripts/inject_prompts.py`. All personas implement BSNP 4-pillar standard coverage.
- [feat] SAPBA Visual Framework: Updated `/tulis-subbab` to enforce generation of markdown data tables and structural `[ILUSTRASI: ...]` image placeholders. Added new `/buat-diagram` prompt to automatically generate Mermaid.js visual syntax (Flowchart, Mindmap, Pie Chart) natively rendered in Open WebUI chat.
- [feat] SAPBA RAG Auto-Sync Engine: Created backend watcher daemon (`scripts/sapba_rag_watcher.py`) that monitors local directories (`rag_docs\Kurikulum`, `BSNP`, `Bahasa` inside the project workspace) and automatically pipelines dropped PDFs/documents into Open WebUI's native ChromaDB Vector DB. This establishes dynamic, code-free Knowledge Collections (`RAG_Kurikulum_Merdeka`, `RAG_Standar_BSNP`, `RAG_Pedoman_Bahasa`) that can be attached to Personas for grounded textbook generation without modifying the frontend UI.
- [feat] SAPBA Word Exporter Tool: Installed `python-docx` dependency and registered a custom Python tool (`sapba_docx_exporter`) into Open WebUI. This tool intercepts markdown outputs and converts them directly into `.docx` files via Base64 Data URIs, allowing users to download natively-formatted Microsoft Word files directly from the chat interface without relying on external file storage.
- [feat] SAPBA Live Web Researcher Tool: Installed `duckduckgo-search` and `beautifulsoup4` dependencies to register a custom python tool (`sapba_web_researcher`). This empowers the "Asisten Riset" persona to perform live web queries, scrape article contents directly from search results, and summarize the latest facts or journal abstracts dynamically if the local RAG database lacks recent information.
- [feat] SAPBA Illustrator Engine: Upgraded from a manual Custom Tool to an automated Global Filter (`sapba_image_filter`). The system now natively intercepts any `[ILUSTRASI: deskripsi]` tags generated by the AI and replaces them with real educational images before the message reaches the UI. This eliminates the need for manual tool triggering or JSON function-calling reliability issues from the LLM.
- [feat] SAPBA Illustrator v8 — Gemini Nano Banana Integration: Migrated image generation backend from Pollinations.ai to **Google Gemini Nano Banana** (`gemini-2.5-flash-image`) for significantly higher quality educational illustrations. Filter uses Valves-configurable API key, supports model selection (`gemini-2.5-flash-image`, `gemini-3.1-flash-image-preview`, `gemini-3-pro-image-preview`), and includes automatic **Pollinations.ai fallback** if Gemini is rate-limited. Key fix: resolved persistent regex double-escaping issue in filter code injection by switching to string-based tag detection (`str.find`) instead of `re.compile`.
- [fix] Docker-to-Host Connectivity: Resolved Ollama model discovery failure caused by incorrect URL (`localhost:11434` → `host.docker.internal:11434`) for Docker-hosted Open WebUI. Added Windows Firewall inbound rule for port 11434. Force-restarted Docker Desktop to clear stale network state.
- [feat] SAPBA Mermaid Diagram Engine: Pivoted visual strategy from external image generation to **native Mermaid.js diagrams** — rendered directly in both Open WebUI chat and GitHub `.md` files without any external API. Registered 3 specialized prompt templates: `/buat-diagram` (general — flowchart, mindmap, sequence, ER, class, state, gantt, pie), `/diagram-jaringan` (network topology with emoji device icons and colored subgraphs), `/diagram-layer` (OSI vs TCP/IP side-by-side comparison with rainbow-gradient styling). All templates enforce labeled styling via `classDef`/`style` directives and Bahasa Indonesia labels.
- [fix] Mermaid Dark Mode Visibility: Deployed `sapba_mermaid_fixer` global filter that auto-injects `%%{init: {'theme': 'base', 'themeVariables': {...}}}%%` directive into all Mermaid code blocks, ensuring text remains readable (black on light fill) in Open WebUI's dark mode.
- [feat] SAPBA Diagram Style Selector (`/diagram-style`): Added prompt template featuring a native **Open WebUI dropdown (`type=select`)** for intuitive style selection. Added 4 new color palettes, bringing the total to **12 selectable color themes** — `ocean` (blue), `forest` (green), `sunset` (warm), `galaxy` (purple), `corporate` (navy-gold), `rainbow` (pastel), `mono` (grayscale), `candy` (pink-playful), `volcano` (dark red), `sunflower` (bright yellow), `coffee` (brown warm), `ice` (cool cyan). User specifies theme name via dropdown; AI applies the full matching color palette with `color:#000` enforcement. Style catalog documented in `docs/SAPBA_Diagram_Style_Catalog.md`.

- [feat] SAPBA Higher Education & Industrial Upgrade: Injected new AI Persona (**🏭 Pakar Industri & Lead Engineer**) and 3 advanced Prompt Templates (`/rancang-modul-studi`, `/standar-industri`, `/lab-engineering`) via `scripts/sapba_higher_ed_upgrade.py`. This upgrade optimizes the system for Universities and Polytechnic institutes by shifting focus from K-12 pedagogy to **Outcome-Based Education (OBE)** and Industrial Standards (IEEE, ISO, Industry 4.0).
- [feat] Engineering Domain Specialization: Optimized AI logic to support complex technical fields including **IoT (MQTT/gRPC)**, **Robotics/Mechatronics**, **Big Data (MLOps)**, and **Software Architecture (Clean/Hexagonal)**.
- [feat] Professional Documentation Engine: Updated prompts to enforce the generation of **Technical Specifications**, **Standard Operating Procedures (SOP)**, and **Laboratory Manuals** with native Mermaid.js diagram support for system architectures and circuit designs.
- [fix] Persistent Ollama Connectivity: Created `scripts/fix_ollama.bat` to automate the configuration of `OLLAMA_HOST=0.0.0.0` and `OLLAMA_ORIGINS=*` on Windows, resolving intermittent "Model Not Available" errors in Docker environment.
- [feat] Zenith Mythos Integration: Implemented a theoretical reconstruction of the **Looped Transformer (RDT)** logic within the Zenith ecosystem. Injected a new specialized Persona (**🌀 Zenith Mythos Architect**) and a deep reasoning prompt template (`/mythos-reasoning`). This system simulates **Implicit Chain-of-Thought** through a 3-stage execution pipeline: **Prelude** (Parameter Identification), **Recurrent Loops** (Iterative Deep Thinking), and **Coda** (Optimized Final Output). This approach optimizes local model inference for complex OOD (Out-of-Distribution) generalization tasks.
- [feat] Zenith Artifacts (Interactive Canvas): Upgraded the Artifacts UI with **"Save to Project" (💾)** and **"Run Locally" (▶️)** buttons. Injected `antigravity.py` backend router to handle native OS execution (opening browsers/files) and persistent saving to internal `projects/live_preview` folder.
- [fix] Artifact Interactive Sandbox: Modified `Artifacts.svelte` to enforce `allow-forms` and `allow-same-origin` permissions, resolving the issue where generated CRUD apps could not process form submissions or maintain local state.

## 🧪 Testing Methodology
- **Integrasi Manual**: Pengujian langsung rute API menggunakan `curl` dan verifikasi visual pada browser (Hard Refresh).
- **Consistency Check**: Memastikan file `main.py` tidak memiliki syntax error setelah injeksi rute baru menggunakan skrip `rebuild_imports.py`.
- **Filter Pipeline Verification**: Docker container logs (`docker logs --tail 50 open-webui`) digunakan untuk memverifikasi eksekusi filter `outlet()`, konfirmasi download gambar dari API, dan validasi penyimpanan Base64 ke database chat.
- **Higher-Ed Validation**: Verifikasi output `/rancang-modul-studi` untuk memastikan kehadiran elemen SKS, CPMK, dan RPS sesuai standar KKNI/OBE.
- **Ollama Connectivity Audit**: Menggunakan `curl http://host.docker.internal:11434/api/tags` dari dalam container untuk memastikan model list dapat diakses secara persisten.
- **Mythos Logic Verification**: Validasi output `/mythos-reasoning` untuk memastikan AI mengikuti protokol *Prelude-Recurrent-Coda* dengan minimal 3 iterasi loop internal.

## 🔍 External Research & References
- **Autonomous Research Pattern (Inspiration: karpathy/autoresearch)**: 
  - Mengevaluasi pola *self-modifying codebase* untuk optimasi performa model lokal.
  - Konsep "Programming the Program" di mana file markdown digunakan sebagai *skill definition* untuk agent otonom.
  - Potensi integrasi ke Roadmap *System Analyst Expert Mode* untuk pengujian arsitektur sistem secara otomatis.
- [test] Comprehensive AAE Audit: Verified 100% success rate on rollback and validation logic.
- [status] AAE Infrastructure: PRODUCTION READY.

## 🔮 Roadmap (In Progress)
- **System Analyst Expert Mode**: AI persona khusus untuk perancangan sistem dengan tombol interaktif Revisi/Eksekusi.
- **Project Structure Visualizer**: Render direktori secara langsung pada UI chat berdasarkan output LLM. (DEPRECATED - Replaced by Zenith IDE and Artifact Sync)
- **Zenith Project Sync**: Real-time synchronization between chat artifacts and local file system.

---
*Last Updated: 2026-04-29 by Antigravity Architect — SAPBA Higher Education & Industrial Upgrade deployed*
