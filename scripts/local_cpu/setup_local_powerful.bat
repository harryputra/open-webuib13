@echo off
REM ============================================================
REM  ANTIGRAVITY ZENITH — FULL LOCAL POWERFUL SETUP
REM
REM  One-shot orchestrator: tune Ollama, pull models, create
REM  CPU-optimized profiles, verify, report.
REM
REM  Run dari: e:\AntiGravityProject\openwebui\
REM    scripts\local_cpu\setup_local_powerful.bat
REM ============================================================
setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "MODELFILES=%SCRIPT_DIR%..\modelfiles"
set "OLLAMA_HOST_LOCAL=http://127.0.0.1:11434"

echo.
echo ============================================================
echo   STEP 1/5 : OPTIMIZE OLLAMA SERVER (env vars + restart)
echo ============================================================
call "%SCRIPT_DIR%optimize_ollama_cpu.bat"

echo.
echo ============================================================
echo   STEP 2/5 : VERIFY OLLAMA REACHABLE
echo ============================================================
for /l %%i in (1,1,15) do (
    powershell -NoProfile -Command "try { (Invoke-WebRequest -Uri '%OLLAMA_HOST_LOCAL%/api/version' -UseBasicParsing -TimeoutSec 2).StatusCode } catch { 0 }" > "%TEMP%\ollama_check.txt" 2>nul
    set /p STATUS=<"%TEMP%\ollama_check.txt"
    if "!STATUS!"=="200" goto :ollama_up
    timeout /t 1 /nobreak >nul
)
echo ERROR: Ollama tidak respon di %OLLAMA_HOST_LOCAL%. Stop.
exit /b 1

:ollama_up
echo Ollama OK.

echo.
echo ============================================================
echo   STEP 3/5 : PULL BASE MODELS (skip yang sudah ada)
echo ============================================================
echo Required base models:
echo   - qwen2.5:0.5b   (task model, 397MB)
echo   - qwen2.5:1.5b   (fast profile, ~1GB) - NEW
echo   - qwen2.5:3b     (balanced + coder profile, 1.9GB)
echo   - nomic-embed-text   (RAG embedding, 274MB)
echo.

call :ensure_model qwen2.5:0.5b
call :ensure_model qwen2.5:1.5b
call :ensure_model qwen2.5:3b
call :ensure_model nomic-embed-text:latest

echo.
echo ============================================================
echo   STEP 4/5 : CREATE ANTIGRAVITY CPU-TUNED PROFILES
echo ============================================================

call :create_profile antigravity-fast       "%MODELFILES%\Modelfile.antigravity-fast"
call :create_profile antigravity-balanced   "%MODELFILES%\Modelfile.antigravity-balanced"
call :create_profile antigravity-coder      "%MODELFILES%\Modelfile.antigravity-coder"
call :create_profile antigravity-task       "%MODELFILES%\Modelfile.antigravity-task"

echo.
echo ============================================================
echo   STEP 5/5 : VERIFY PROFILES
echo ============================================================
echo.
echo Final model list:
ollama list
echo.

echo ============================================================
echo   QUICK BENCHMARK (antigravity-fast vs antigravity-balanced)
echo ============================================================
echo.
echo Warm-up + 1 short prompt (each)...

powershell -NoProfile -Command "$body = @{ model='antigravity-fast'; prompt='Halo, sebut nama anak presiden RI ke-7 dalam satu baris.'; stream=$false; options=@{num_predict=80} } | ConvertTo-Json; $sw=[Diagnostics.Stopwatch]::StartNew(); $r = Invoke-RestMethod -Method POST -Uri '%OLLAMA_HOST_LOCAL%/api/generate' -Body $body -ContentType 'application/json' -TimeoutSec 120; $sw.Stop(); $tok = if($r.eval_count){$r.eval_count}else{0}; $dur = if($r.eval_duration){$r.eval_duration/1e9}else{$sw.Elapsed.TotalSeconds}; $tps = if($dur -gt 0){[math]::Round($tok/$dur,2)}else{0}; Write-Host ('  antigravity-fast     : ' + $tps + ' tok/s (' + $tok + ' tokens, ' + [math]::Round($dur,2) + 's)')"

powershell -NoProfile -Command "$body = @{ model='antigravity-balanced'; prompt='Halo, sebut nama anak presiden RI ke-7 dalam satu baris.'; stream=$false; options=@{num_predict=80} } | ConvertTo-Json; $sw=[Diagnostics.Stopwatch]::StartNew(); $r = Invoke-RestMethod -Method POST -Uri '%OLLAMA_HOST_LOCAL%/api/generate' -Body $body -ContentType 'application/json' -TimeoutSec 180; $sw.Stop(); $tok = if($r.eval_count){$r.eval_count}else{0}; $dur = if($r.eval_duration){$r.eval_duration/1e9}else{$sw.Elapsed.TotalSeconds}; $tps = if($dur -gt 0){[math]::Round($tok/$dur,2)}else{0}; Write-Host ('  antigravity-balanced : ' + $tps + ' tok/s (' + $tok + ' tokens, ' + [math]::Round($dur,2) + 's)')"

echo.
echo ============================================================
echo   SETUP COMPLETE
echo ============================================================
echo.
echo Next steps:
echo   1. Restart Open WebUI container kalau lagi jalan:
echo        docker compose restart open-webui
echo   2. Buka http://localhost:3013
echo   3. Pilih model "antigravity-balanced" untuk chat utama
echo   4. Lihat docs\LOCAL_CPU_OPTIMIZATION.md untuk detail
echo.
endlocal
exit /b 0


REM ===================================================================
REM  Helper: ensure_model <name>
REM  Pull model kalau belum ada di local registry
REM ===================================================================
:ensure_model
set "MODEL=%~1"
ollama list 2>nul | findstr /B /C:"%MODEL% " >nul
if %ERRORLEVEL%==0 (
    echo [skip] %MODEL%   already present
    goto :eof
)
echo [pull] %MODEL% ...
ollama pull "%MODEL%"
goto :eof


REM ===================================================================
REM  Helper: create_profile <name> <modelfile_path>
REM  Re-create profile (force overwrite, idempotent)
REM ===================================================================
:create_profile
set "NAME=%~1"
set "MFILE=%~2"
if not exist "%MFILE%" (
    echo [SKIP] %NAME% — Modelfile not found: %MFILE%
    goto :eof
)
echo [create] %NAME% from %MFILE%
ollama create "%NAME%" -f "%MFILE%" 2>&1 | findstr /V "transferring writing using parsing" | findstr /R /V "^$"
goto :eof
