# Technical Specification Document - Antigravity Zenith IDE

## 🌌 Project Overview
Antigravity Zenith adalah transformasi Open WebUI menjadi sebuah "AI-Powered Research Command Center" yang memiliki IDE terintegrasi, manajemen file system langsung, dan sistem pembaruan cerdas.

## 🛠️ Tech Stack Consistency
- **Frontend**: Vanilla JavaScript (ES6+), Svelte, Tailwind CSS v4 (Glassmorphism), HTML5.
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
- [feat] **Antigravity Zenith UI Overhaul (Premium)**: Migrated the entire interface (Sidebar, Navbar, MessageInput, ModelSelector) to a premium, deep-space glassmorphism design language.
  - **Background**: Implemented fixed radial gradients (`#1e1b4b` to `#030303`) for immersive depth.
  - **Branding**: Renamed app to "Antigravity Zenith" and disabled persistent version update notifications (`ENABLE_VERSION_UPDATE_CHECK=False`).
  - **Refined Glass**: Increased sidebar blur to `40px` with 180% saturation and thin translucent borders for a sleek aerospace aesthetic.
  - **Chat Interface**: Floating chat input with purple glow (`#8b5cf6`) and blurred background.

- [feat] SAPBA Higher Education & Industrial Upgrade: Injected new AI Persona (**🏭 Pakar Industri & Lead Engineer**) and 3 advanced Prompt Templates (`/rancang-modul-studi`, `/standar-industri`, `/lab-engineering`) via `scripts/sapba_higher_ed_upgrade.py`. This upgrade optimizes the system for Universities and Polytechnic institutes by shifting focus from K-12 pedagogy to **Outcome-Based Education (OBE)** and Industrial Standards (IEEE, ISO, Industry 4.0).
- [feat] Engineering Domain Specialization: Optimized AI logic to support complex technical fields including **IoT (MQTT/gRPC)**, **Robotics/Mechatronics**, **Big Data (MLOps)**, and **Software Architecture (Clean/Hexagonal)**.
- [feat] Professional Documentation Engine: Updated prompts to enforce the generation of **Technical Specifications**, **Standard Operating Procedures (SOP)**, and **Laboratory Manuals** with native Mermaid.js diagram support for system architectures and circuit designs.
- [fix] Persistent Ollama Connectivity: Created `scripts/fix_ollama.bat` to automate the configuration of `OLLAMA_HOST=0.0.0.0` and `OLLAMA_ORIGINS=*` on Windows, resolving intermittent "Model Not Available" errors in Docker environment.
- [feat] Zenith Mythos Integration: Implemented a theoretical reconstruction of the **Looped Transformer (RDT)** logic within the Zenith ecosystem. Injected a new specialized Persona (**🌀 Zenith Mythos Architect**) and a deep reasoning prompt template (`/mythos-reasoning`). This system simulates **Implicit Chain-of-Thought** through a 3-stage execution pipeline: **Prelude** (Parameter Identification), **Recurrent Loops** (Iterative Deep Thinking), and **Coda** (Optimized Final Output). This approach optimizes local model inference for complex OOD (Out-of-Distribution) generalization tasks.
- [feat] Zenith Artifacts (Interactive Canvas): Upgraded the Artifacts UI with **"Save to Project" (💾)** and **"Run Locally" (▶️)** buttons. Injected `antigravity.py` backend router to handle native OS execution (opening browsers/files) and persistent saving to internal `projects/live_preview` folder.
- [fix] Artifact Interactive Sandbox: Modified `Artifacts.svelte` to enforce `allow-forms` and `allow-same-origin` permissions, resolving the issue where generated CRUD apps could not process form submissions or maintain local state.

### 🌌 Antigravity Super Tools Platform (v2.0)
- [feat] **Antigravity Research Engine** (`antigravity_research_engine`): Mesin riset komprehensif dengan 4 metode async — `search_academic_papers` (pencarian multi-sumber: arXiv, Semantic Scholar, CrossRef secara bersamaan), `search_web_deep` (DuckDuckGo + full-content extraction dengan pembersihan HTML otomatis), `manage_citations` (format sitasi otomatis APA/IEEE/Chicago), `get_paper_details` (metadata lengkap, abstrak, referensi, dan paper yang mengutip). Semua metode menggunakan `__event_emitter__` untuk progress real-time ke UI. Lokasi: `scripts/tools/antigravity_research_engine.py`.
- [feat] **Antigravity Book Engine** (`antigravity_book_engine`): Mesin penulisan buku end-to-end dengan 4 metode — `generate_book_outline` (outline terstruktur dengan panduan penulisan naratif deskriptif), `write_chapter_draft` (kerangka penulisan bab dengan 4 gaya: naratif-deskriptif, akademis, semi-formal, teknis), `check_writing_consistency` (analisis readability, struktur, terminologi), `export_book` (ekspor ke DOCX/EPUB/Markdown dengan title page dan formatting profesional). Lokasi: `scripts/tools/antigravity_book_engine.py`.
- [feat] **Antigravity Code Engine** (`antigravity_code_engine`): Upgrade dari Auto-Coding Engine v1 dengan 7 metode — `list_files`/`read_file`/`write_file` (manajemen file workspace), `execute_code` (eksekusi multi-bahasa: Python, Bash, Node.js dengan sandbox), `run_command` (perintah terminal), `analyze_code_quality` (analisis statis + scoring), `git_operations` (status, log, diff, branch, commit, pull). Menggunakan helper `_resolve_path` untuk keamanan path traversal. Lokasi: `scripts/tools/antigravity_code_engine.py`.
- [feat] **Antigravity Project Manager** (`antigravity_project_manager`): Manajemen proyek dengan 3 metode — `create_project_structure` (scaffolding otomatis dengan 6 template: generic, web-app, api-server, python-library, book-project, research-project), `track_progress` (task tracking dengan status pending/in-progress/done/blocked), `generate_documentation` (auto-generate README dan project structure docs). Lokasi: `scripts/tools/antigravity_project_manager.py`.
- [feat] **Master Injector Script** (`scripts/inject_super_tools.py`): Script deployment all-in-one yang mendeploy keempat tool engine ke Open WebUI secara idempotent (create/update). Mendukung konfigurasi via CLI args (`--base-url`, `--token`, `--tool`) atau environment variables (`OWUI_BASE_URL`, `OWUI_TOKEN`).
- [feat] **Super Tool Personas** (`scripts/inject_super_personas.py`): 3 persona AI khusus yang sudah di-bind ke Super Tools:
  - **🔬 Research Scientist** — Ilmuwan riset doktoral, menguasai pencarian akademik multi-sumber, literature review, dan manajemen sitasi.
  - **📖 Book Author** — Penulis buku profesional, gaya naratif deskriptif, kalimat panjang natural, anti poin-poin singkat.
  - **💻 Lead Developer** — Senior full-stack engineer, eksekusi kode, Git, scaffolding, dan analisis kualitas.
- [feat] **8 Prompt Templates**: `/riset-paper`, `/literature-review`, `/riset-web`, `/outline-buku`, `/tulis-bab-buku`, `/ekspor-buku`, `/buat-proyek`, `/analisis-kode` — semua terintegrasi dengan tool functions.
- [feat] **Cross-Persona Tool Binding**: Super Tools diaktifkan pada persona lama (`Asisten Riset`, `Penulis Konten`) sehingga seluruh ekosistem persona mendapat kapabilitas baru.

### 🚀 Antigravity Super Tools v3.0 — Power Upgrade
- [feat] **Research Engine v3.0**: +2 metode baru — `synthesize_literature_review` (riset otomatis + sintesis lit review dengan analisis tren, distribusi tahun, research gap, dan bibliografi terstruktur), `extract_pdf_content` (unduh + ekstraksi teks dari PDF paper via PyPDF2/pdfplumber, normalisasi URL arXiv otomatis). `max_content_length` dinaikkan 3000→8000 karakter.
- [feat] **Book Engine v3.0**: +1 metode baru — `manage_book_state` (pelacakan progress buku persisten lintas sesi: word count per bab, status tracking [draft/outline/writing/review/done], ringkasan cross-chapter untuk konteks, estimasi halaman, progress bar visual).
- [feat] **Code Engine v3.0**: +2 metode baru — `search_in_files` (grep/regex workspace-wide dengan filter ekstensi, skip dirs otomatis, max 30 hasil terstruktur per file), `manage_dependencies` (pip/npm: list, install, uninstall, freeze, outdated).
- [feat] **Project Manager v3.0**: +2 metode baru — `scan_project_health` (audit kesehatan otomatis: cek README, .gitignore, tests, empty dirs, config files, docs; scoring A-F dengan rekomendasi), `generate_changelog` (parse git log → kategorisasi Conventional Commits: feat/fix/docs/refactor/style/test/chore).
- [deps] **PyPDF2**: Terinstall di container untuk mendukung ekstraksi PDF paper akademik.

### 🏗️ Autonomous Dev Architect — Personal Software Development Assistant
- [feat] **Software Architect Persona** (`antigravity-software-architect`): Persona AI full-stack baru yang bertindak sebagai arsitek perangkat lunak senior. Alur kerja 5 Fase: (1) Perancangan Sistem — menghasilkan dokumen desain lengkap (overview, tech stack, architecture diagram Mermaid, ERD, API design, UI wireframe, folder structure, implementation plan), (2) Review & Revisi — menerima masukan user dan merancang ulang, (3) Implementasi — membuat folder, install dependencies, menulis SEMUA kode backend dan frontend secara lengkap dan fungsional via tools, (4) Debugging — analisis error otomatis menggunakan `read_file` + `search_in_files`, perbaikan langsung via `write_file`, verifikasi ulang, (5) Iterasi & Enhancement — penambahan fitur, refactoring, optimasi.
- [feat] **6 Prompt Templates Baru**:
  - `/rancang-sistem` — Input ide → dokumen perancangan sistem lengkap (8 bagian) dengan Architecture + ERD Mermaid. User bisa revisi atau setujui.
  - `/implementasi` — Auto-build: scaffolding, install deps, konfigurasi, database migration, tulis semua kode, jalankan server.
  - `/debug-error` — Paste error → AI otomatis baca file, cari root cause, perbaiki kode langsung, verifikasi.
  - `/deploy-lokal` — Jalankan proyek: cek deps, setup DB, migration, start dev server, tampilkan URL.
  - `/tambah-fitur` — Deskripsikan fitur → AI analisis proyek, implementasi, dan test.
  - `/refactor` — Audit kualitas kode, refactoring otomatis, laporan before/after.
- [infra] **Injector Script**: `scripts/inject_dev_architect.py` — deploy persona + prompts secara idempotent ke Open WebUI.

- [feat] Multi-Provider AI Architecture: Migrated system to support multiple OpenAI-compatible providers simultaneously. Successfully integrated DeepSeek (Official API), OpenRouter (Aggregation), and LM Studio (Local Inference) by injecting configurations directly into the PostgreSQL `config` table. Resolved `.env` priority issues by enforcing database-level settings.
- [fix] Redis Configuration Patch: Corrected malformed JSON strings in Redis (`OPENAI_API_BASE_URLS`, `OPENAI_API_KEYS`) using a custom Python script (`fix_redis.py`) inside the container, resolving "Invalid JSON" errors in backend logs that caused model discovery failures.
- [feat] Antigravity Book Architect: Deployed a specialized high-capacity persona based on `hermes-3-llama-3.1-405b:free` (405B parameters), configured for multi-phase structured book writing.
- [opt] Model Parameter Calibration: Optimized `max_tokens` (4096 tokens) and system prompts for free-tier giant models to comply with OpenRouter's free-tier rate limits and ensure stable output.

## 🧪 Testing Methodology
- **Integrasi Manual**: Pengujian langsung rute API menggunakan `curl` dan verifikasi visual pada browser (Hard Refresh).
- **Consistency Check**: Memastikan file `main.py` tidak memiliki syntax error setelah injeksi rute baru menggunakan skrip `rebuild_imports.py`.
- **Filter Pipeline Verification**: Docker container logs (`docker logs --tail 50 open-webui`) digunakan untuk memverifikasi eksekusi filter `outlet()`, konfirmasi download gambar dari API, dan validasi penyimpanan Base64 ke database chat.
- **Higher-Ed Validation**: Verifikasi output `/rancang-modul-studi` untuk memastikan kehadiran elemen SKS, CPMK, dan RPS sesuai standar KKNI/OBE.
- **Ollama Connectivity Audit**: Menggunakan `curl http://host.docker.internal:11434/api/tags` dari dalam container untuk memastikan model list dapat diakses secara persisten.
- **Mythos Logic Verification**: Validasi output `/mythos-reasoning` untuk memastikan AI mengikuti protokol *Prelude-Recurrent-Coda* dengan minimal 3 iterasi loop internal.
- **Super Tools Unit Testing**: Verifikasi import dan syntax setiap tool engine via `python -c "exec(open('scripts/tools/<tool>.py').read())"`. Validasi metode async dan event_emitter pattern. Pengujian integrasi via Open WebUI chat setelah injeksi.
- **Master Injector Verification**: Uji `inject_super_tools.py` dengan `--tool` flag per-tool, lalu verifikasi keberadaan tools di Open WebUI → Workspace → Tools. Confirmed 4/4 tools created successfully.
- **Persona & Prompt Verification**: Deploy via `inject_super_personas.py`, verifikasi 3/3 personas created dan 8/8 prompt templates seeded. Tool binding diverifikasi via API (`toolIds` array pada setiap model).
- **API Registry Check**: Script `scratch/verify_tools.py` mengkonfirmasi 8 total tools terdaftar (4 legacy + 4 Super Tools baru).

## 🔍 External Research & References
- **Autonomous Research Pattern (Inspiration: karpathy/autoresearch)**: 
  - Mengevaluasi pola *self-modifying codebase* untuk optimasi performa model lokal.
  - Konsep "Programming the Program" di mana file markdown digunakan sebagai *skill definition* untuk agent otonom.
  - Potensi integrasi ke Roadmap *System Analyst Expert Mode* untuk pengujian arsitektur sistem secara otomatis.
- **Academic API Integration**: arXiv API (bulk search), Semantic Scholar Graph API (200M+ papers, citation graphs), CrossRef (DOI metadata & journal indexing).
- **Book Authoring Patterns**: python-docx (Word generation), ebooklib (EPUB creation), markdown processing untuk multi-format export.
- [test] Comprehensive AAE Audit: Verified 100% success rate on rollback and validation logic.
- [status] AAE Infrastructure: PRODUCTION READY.
- [status] Super Tools Platform: ✅ **v3.0 DEPLOYED** — 4 tools (7 metode baru), 3 personas, 8 prompts active.
- [fix] **Critical Chat Rendering Crash (visibleEnd ReferenceError)**: Menghapus assignment `visibleEnd = messages.length;` yang orphan di fungsi `buildMessages()` pada `Messages.svelte` (line 105). Variabel `visibleEnd` tidak pernah dideklarasikan dalam komponen — merupakan sisa dari penghapusan sistem virtual-scrolling sebelumnya. Bug ini menyebabkan **72+ ReferenceError per chat message** yang membuat Svelte reactivity loop crash, sehingga respons model tidak ditampilkan meskipun backend mengembalikan HTTP 200 OK. Setelah fix, chat streaming berfungsi normal dengan respons ~2.3 detik (qwen2.5:1.5b).
  - **Root Cause**: Implicit global variable assignment tanpa deklarasi (`let`/`const`/`var`).
  - **Impact**: Chat UI stuck di spinner tanpa menampilkan respons apapun.
  - **Resolution**: Hapus baris orphan — variabel `visibleEnd` tidak lagi digunakan di template.
  - **Verification**: Diuji dengan model `qwen2.5:1.5b`, respons muncul dalam ~2.3s, 0 console errors.

## 📊 Tool Method Registry (v3.0)
| Tool | Metode | Deskripsi |
|:---|:---|:---|
| Research Engine | `search_academic_papers` | Pencarian multi-sumber (arXiv, S2, CrossRef) |
| | `search_web_deep` | DuckDuckGo + full-content extraction |
| | `manage_citations` | Format sitasi APA/IEEE/Chicago |
| | `get_paper_details` | Metadata lengkap + referensi + citations |
| | `synthesize_literature_review` | 🆕 Auto lit review + trend analysis |
| | `extract_pdf_content` | 🆕 PDF paper text extraction |
| Book Engine | `generate_book_outline` | Outline terstruktur multi-audience |
| | `write_chapter_draft` | Kerangka penulisan 4 gaya |
| | `check_writing_consistency` | Analisis readability + terminologi |
| | `export_book` | Ekspor DOCX/EPUB/Markdown |
| | `manage_book_state` | 🆕 Progress tracking persisten |
| Code Engine | `list_files` / `read_file` / `write_file` | Manajemen file workspace |
| | `execute_code` | Eksekusi Python/Bash/Node.js |
| | `run_command` | Terminal/shell commands |
| | `analyze_code_quality` | Analisis statis + scoring |
| | `git_operations` | Git status/log/diff/commit/branch |
| | `search_in_files` | 🆕 Grep/regex workspace-wide |
| | `manage_dependencies` | 🆕 pip/npm management |
| Project Manager | `create_project_structure` | Scaffolding 6 template |
| | `track_progress` | Task tracking multi-status |
| | `generate_documentation` | Auto README/structure docs |
| | `scan_project_health` | 🆕 Audit kesehatan + scoring |
| | `generate_changelog` | 🆕 Git → Conventional Commits |

## 🔮 Roadmap (In Progress)
- **System Analyst Expert Mode**: AI persona khusus untuk perancangan sistem dengan tombol interaktif Revisi/Eksekusi.
- ~~**Project Structure Visualizer**~~: (DEPRECATED - Replaced by Zenith IDE, Artifact Sync, and Project Manager Tool)
- **Zenith Project Sync**: Real-time synchronization between chat artifacts and local file system.
- **MCP Universal Integration**: Menghubungkan Open WebUI dengan server MCP eksternal via MCPO bridge untuk plug-and-play tool ecosystem.
- **Agent Pipeline Orchestration**: Multi-tool pipeline yang memecah tugas kompleks menjadi chain of tool calls secara otonom.
- **Research-to-Book Pipeline**: Automated workflow dari pencarian paper → literature review → outline buku → penulisan bab → ekspor final.
- **Zenith Branding Suite**: Completion of custom high-fidelity icons and assets for a 100% unique brand experience.

## 🎨 Antigravity Zenith UI Modernization (v1.0)
### 1. Visual Language & Tokens
- **Zenith Glass (`.zenith-glass`)**: Implementasi glassmorphism menggunakan `backdrop-filter: blur(16px)` dengan background semi-transparan `bg-white/70` (light) dan `bg-gray-900/70` (dark).
- **Zenith Gradient (`.zenith-gradient-text`)**: Skema warna aksen menggunakan gradien linear dari biru neon ke ungu futuristik untuk elemen branding utama.
- **Premium Borders**: Penggunaan `border-white/5` (dark mode) untuk menciptakan efek kedalaman "deep-space" yang halus.

### 2. Component Overhauls
- **Sidebar & Navbar**: Transformasi total ke layout Zenith dengan trigger menu yang diperhalus dan transparansi dinamis.
- **Message Input**: Kontainer input chat didesain ulang dengan drop-shadow premium dan integrasi glassmorphism untuk kesan "floating".
- **Model Selector**: Tipografi tajam dengan font-weight bold dan dropdown menu berbasis `.zenith-glass`.
- **Welcome Screen (Placeholder)**: Header modern dengan tipografi dampak tinggi (Outfit/Inter) dan branding Antigravity Zenith yang menonjol.

### 3. Interactive UX
- **Fluid States**: Transisi hover pada User Menu dan navigation links diperbarui menggunakan semi-transparent states (`hover:bg-white/5`) untuk menghindari kontras tajam yang merusak estetika gelap.
- **Spatial Optimization**: Penyesuaian padding dan margin sistemik untuk memastikan interface terasa lega dan profesional.

---
*Last Updated: 2026-05-11 by Antigravity Architect — Critical Chat Rendering Fix (visibleEnd ReferenceError)*
