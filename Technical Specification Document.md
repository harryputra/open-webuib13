# 🌌 Antigravity IDE - Technical Specification Document

## 🏗️ Architecture Overview
Sistem ini dibangun di atas Open WebUI dengan integrasi filesystem Host (Windows) melalui Docker Volume.

### Key Components:
- **Core Engine**: Open WebUI (Python/Svelte)
- **Filesystem Mapping**: 
  - Host `E:\AntiGravityProject` -> Container `/workspace`
  - Host `E:\file_rag` -> Container `/file_rag`
- **Execution Layer**: Global Auto-Executor Filter (Python)

## 🛠️ Tool Standards
Setiap AI Persona dibekali dengan tool built-in:
1. `read_file`: Membaca konten file di workspace.
2. `write_file`: Menulis/Update file.
3. `execute_shell_command`: Menjalankan perintah terminal (CMD/Bash).

## 📝 Coding Standards
- **Commit Format**: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`.
- **Framework**: PHP Native (saat ini) dengan standar PDO untuk keamanan database.
- **Port Mapping**: MySQL berjalan di port `3307` (khusus sesi ini).

## 🛰️ Antigravity Sync Protocol
Setiap fitur baru harus:
1. Diverifikasi secara fisik di disk Host.
2. Dicatat dalam dokumen ini.
3. Diuji fungsionalitasnya melalui browser.
