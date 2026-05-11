@echo off
setlocal EnableDelayedExpansion
title Antigravity Open WebUI

cd /d "%~dp0"

echo.
echo === Antigravity Open WebUI - launcher ===
echo.

:: ---------------------------------------------------------------------------
:: 1. Pastikan Docker tersedia
:: ---------------------------------------------------------------------------
where docker >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker tidak ditemukan. Pasang Docker Desktop dulu:
    echo         https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)

docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker daemon tidak berjalan. Jalankan Docker Desktop dulu.
    pause
    exit /b 1
)

:: ---------------------------------------------------------------------------
:: 2. Cek Ollama + auto-pull model wajib + set env optimasi
:: ---------------------------------------------------------------------------
where ollama >nul 2>&1
if not errorlevel 1 (
    echo [info] Ollama terdeteksi - cek dan pull model wajib...

    :: Pull model wajib (idempotent - skip kalau udah ada)
    for %%M in (nomic-embed-text:latest qwen2.5:0.5b qwen2.5:3b llama3.1:8b) do (
        ollama list 2>nul | findstr /B /C:"%%M" >nul
        if errorlevel 1 (
            echo [info] Pulling %%M ...
            ollama pull %%M
        ) else (
            echo [info] %%M sudah ada - skip.
        )
    )

    :: Bersihkan model cloud yang gak gratis-unlimited dari Ollama (otomatis, gak interaktif)
    for %%C in (deepseek-v4-pro:cloud deepseek-v3.1:671b-cloud gpt-oss:120b-cloud gpt-oss:20b-cloud) do (
        ollama list 2>nul | findstr /B /C:"%%C" >nul
        if not errorlevel 1 (
            echo [info] Hapus model cloud "%%C" (bukan free unlimited)...
            ollama rm %%C >nul 2>&1
        )
    )

    :: Set Ollama env vars permanent (User scope, butuh restart Ollama)
    echo [info] Set Ollama optimization env vars (permanent)...
    setx OLLAMA_NUM_CTX 4096 >nul 2>&1
    setx OLLAMA_KEEP_ALIVE 30m >nul 2>&1
    setx OLLAMA_NUM_PARALLEL 1 >nul 2>&1
    setx OLLAMA_FLASH_ATTENTION 1 >nul 2>&1
    setx OLLAMA_KV_CACHE_TYPE q8_0 >nul 2>&1
    echo [info] Env Ollama di-set. WAJIB quit Ollama tray icon ^& buka lagi agar aktif.
) else (
    echo [warn] Ollama tidak terinstall. Skip auto-pull.
    echo [warn] Tanpa Ollama, fitur lokal tidak jalan. Install: https://ollama.com
    timeout /t 3 >nul
)

:: ---------------------------------------------------------------------------
:: 3. Generate WEBUI_SECRET_KEY (sekali saja)
:: ---------------------------------------------------------------------------
set "SECRET_FILE=.webui_secret_key"
if not exist "%SECRET_FILE%" (
    echo [info] Membuat WEBUI_SECRET_KEY baru...
    powershell -NoProfile -Command "$b = New-Object byte[] 32; [System.Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($b); ($b | ForEach-Object { $_.ToString('x2') }) -join '' | Set-Content -NoNewline -Encoding ASCII '%SECRET_FILE%'"
)
set /p GENERATED_SECRET=<%SECRET_FILE%

:: ---------------------------------------------------------------------------
:: 4. Buat .env kalau belum ada
:: ---------------------------------------------------------------------------
if not exist .env (
    echo [info] Membuat .env baru...
    > .env echo OPEN_WEBUI_PORT=3013
    >> .env echo WEBUI_SECRET_KEY=!GENERATED_SECRET!
    >> .env echo OLLAMA_BASE_URL=http://host.docker.internal:11434
    >> .env echo SCARF_NO_ANALYTICS=true
    >> .env echo DO_NOT_TRACK=true
    >> .env echo ANONYMIZED_TELEMETRY=false
    >> .env echo WORKSPACE_DIR=E:/AntiGravityProject
    >> .env echo WORKSPACE_MAX_FILE_SIZE=5242880
    >> .env echo RAG_VAULT_PATH=E:/file_rag
    >> .env echo RAG_EMBEDDING_ENGINE=ollama
    >> .env echo RAG_EMBEDDING_MODEL=nomic-embed-text:latest
    >> .env echo RAG_OLLAMA_BASE_URL=http://host.docker.internal:11434
    >> .env echo ENABLE_RAG_HYBRID_SEARCH=True
    >> .env echo OLLAMA_KEEP_ALIVE=30m
    >> .env echo TASK_MODEL=qwen2.5:0.5b
    >> .env echo TASK_MODEL_EXTERNAL=qwen2.5:0.5b
    >> .env echo ENABLE_WEBSOCKET_SUPPORT=True
    >> .env echo WEBSOCKET_MANAGER=redis
    echo [info] .env dibuat.
) else (
    echo [info] .env sudah ada - tidak ditimpa.
)

:: ---------------------------------------------------------------------------
:: 5. Pastikan folder bantu ada
:: ---------------------------------------------------------------------------
if not exist "projects\marp_slides" mkdir "projects\marp_slides"
if not exist "projects\live_preview" mkdir "projects\live_preview"
if not exist "E:\file_rag" mkdir "E:\file_rag"

:: ---------------------------------------------------------------------------
:: 6. Build & start
:: ---------------------------------------------------------------------------
echo.
echo [info] Build dan start docker compose...
docker compose up -d --build
if errorlevel 1 (
    echo.
    echo [ERROR] docker compose gagal. Pastikan Docker Desktop sudah penuh siap.
    pause
    exit /b 1
)

:: ---------------------------------------------------------------------------
:: 7. Tunggu Open WebUI healthy
:: ---------------------------------------------------------------------------
set "PORT=3013"
for /f "tokens=2 delims==" %%V in ('findstr /B "OPEN_WEBUI_PORT=" .env 2^>nul') do set "PORT=%%V"

echo.
echo [info] Tunggu Open WebUI siap di http://localhost:%PORT% ...
set /a WAIT=0
:wait_health
set /a WAIT+=1
if %WAIT% gtr 60 (
    echo [warn] Health check timeout. Cek log: docker compose logs -f open-webui
    goto :skip_register
)
curl -sf "http://localhost:%PORT%/health" >nul 2>&1
if errorlevel 1 (
    timeout /t 2 /nobreak >nul
    goto :wait_health
)
echo [info] Open WebUI siap.

:: ---------------------------------------------------------------------------
:: 8. Auto-register Antigravity tools (idempotent, butuh .owui_token)
:: ---------------------------------------------------------------------------
if exist .owui_token (
    set /p OWUI_TOKEN=<.owui_token
    if not "!OWUI_TOKEN!"=="" (
        where python >nul 2>&1
        if errorlevel 1 (
            echo [warn] Python tidak ditemukan di PATH. Skip auto-register.
            echo [warn] Install Python 3.10+ untuk auto-register tools dan persona.
        ) else (
            echo [info] Registering Antigravity tools...
            python scripts\inject_super_tools.py --base-url http://localhost:%PORT% --token !OWUI_TOKEN!
            echo.
            echo [info] Setup default persona "Antigravity Local"...
            python scripts\setup_default_persona.py --base-url http://localhost:%PORT% --token !OWUI_TOKEN!
        )
    )
) else (
    echo.
    echo [info] AUTO-REGISTER TOOLS belum aktif - butuh JWT token.
    echo [info] Cara aktifin sekali saja:
    echo        1. Buka http://localhost:%PORT% - Settings - Account - API Keys
    echo        2. Klik 'Create new key', salin token-nya
    echo        3. Buat file .owui_token di folder ini, tempel token-nya
    echo        4. Jalankan ulang run.bat - tools auto register
    echo.
)

:skip_register

:: ---------------------------------------------------------------------------
:: 9. Buka browser
:: ---------------------------------------------------------------------------
echo.
echo [info] Akses: http://localhost:%PORT%
start "" http://localhost:%PORT%

echo.
echo Container jalan di background.
echo   docker compose logs -f open-webui   ^<- tail log
echo   docker compose ps                   ^<- cek status
echo   docker compose down                 ^<- stop semua
echo.
echo Pencet sembarang tombol untuk STOP semua container,
echo atau tutup jendela ini supaya container tetap jalan.
pause >nul

echo.
echo [info] Stopping containers...
docker compose down
endlocal
