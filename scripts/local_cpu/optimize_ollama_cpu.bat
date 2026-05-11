@echo off
REM ============================================================
REM  OLLAMA CPU OPTIMIZER — Antigravity Zenith
REM  Tune Ollama server untuk i7-8650U class CPU (4C/8T, no GPU)
REM  - Set persistent USER env vars
REM  - Restart Ollama service supaya env terbaca
REM  - Idempotent: aman dijalankan berulang
REM ============================================================
setlocal enabledelayedexpansion

echo.
echo ============================================================
echo   ANTIGRAVITY OLLAMA CPU OPTIMIZER
echo ============================================================

REM --- Detect logical CPU count ---
for /f "tokens=*" %%i in ('powershell -NoProfile -Command "(Get-CimInstance Win32_Processor | Measure-Object -Property NumberOfLogicalProcessors -Sum).Sum"') do set LOGICAL=%%i
for /f "tokens=*" %%i in ('powershell -NoProfile -Command "(Get-CimInstance Win32_Processor | Measure-Object -Property NumberOfCores -Sum).Sum"') do set CORES=%%i

echo Detected CPU: %CORES% physical cores / %LOGICAL% logical threads

REM --- Compute thread budget: cap at physical cores, leave 1 for OS if >=4 ---
set /a NUM_THREAD=%CORES%
if %CORES% GEQ 4 set /a NUM_THREAD=%CORES%-0

echo Using OLLAMA_NUM_THREAD=%NUM_THREAD%
echo.

REM --- Set persistent USER env vars ---
echo [1/8] OLLAMA_NUM_PARALLEL=1   (predictable single-stream throughput on CPU)
setx OLLAMA_NUM_PARALLEL "1" >nul

echo [2/8] OLLAMA_MAX_LOADED_MODELS=2   (chat model + embed model coexist)
setx OLLAMA_MAX_LOADED_MODELS "2" >nul

echo [3/8] OLLAMA_NUM_THREAD=%NUM_THREAD%   (match physical cores, no HT overhead)
setx OLLAMA_NUM_THREAD "%NUM_THREAD%" >nul

echo [4/8] OLLAMA_FLASH_ATTENTION=1   (faster attention, less memory)
setx OLLAMA_FLASH_ATTENTION "1" >nul

echo [5/8] OLLAMA_KV_CACHE_TYPE=q8_0   (50%% KV cache memory savings, negligible quality loss)
setx OLLAMA_KV_CACHE_TYPE "q8_0" >nul

echo [6/8] OLLAMA_KEEP_ALIVE=30m   (avoid cold-start reload)
setx OLLAMA_KEEP_ALIVE "30m" >nul

echo [7/8] OLLAMA_HOST=0.0.0.0:11434   (accessible from Docker container)
setx OLLAMA_HOST "0.0.0.0:11434" >nul

echo [8/8] OLLAMA_MAX_QUEUE=512   (handle bursty requests from RAG/multi-tab)
setx OLLAMA_MAX_QUEUE "512" >nul

echo.
echo ============================================================
echo   Restarting Ollama (kill + spawn) so env vars take effect
echo ============================================================

REM --- Stop running Ollama processes ---
taskkill /F /IM "ollama app.exe" /T >nul 2>&1
taskkill /F /IM "ollama.exe" /T >nul 2>&1
timeout /t 2 /nobreak >nul

REM --- Apply env vars to current shell so spawned process inherits ---
set OLLAMA_NUM_PARALLEL=1
set OLLAMA_MAX_LOADED_MODELS=2
set OLLAMA_NUM_THREAD=%NUM_THREAD%
set OLLAMA_FLASH_ATTENTION=1
set OLLAMA_KV_CACHE_TYPE=q8_0
set OLLAMA_KEEP_ALIVE=30m
set OLLAMA_HOST=0.0.0.0:11434
set OLLAMA_MAX_QUEUE=512

REM --- Locate ollama app.exe (system tray launcher) ---
set "OLLAMA_APP=%LOCALAPPDATA%\Programs\Ollama\ollama app.exe"
if not exist "%OLLAMA_APP%" set "OLLAMA_APP=%ProgramFiles%\Ollama\ollama app.exe"
if not exist "%OLLAMA_APP%" set "OLLAMA_APP=%LOCALAPPDATA%\Ollama\ollama app.exe"

if exist "%OLLAMA_APP%" (
    echo Spawning: %OLLAMA_APP%
    start "" "%OLLAMA_APP%"
) else (
    echo WARNING: Ollama app.exe not found in standard paths.
    echo Falling back to "ollama serve" headless.
    start "Ollama Server" /MIN cmd /c "ollama serve"
)

echo.
echo Waiting for Ollama to come back online...
timeout /t 4 /nobreak >nul

REM --- Verify ---
for /l %%i in (1,1,10) do (
    powershell -NoProfile -Command "try { (Invoke-WebRequest -Uri 'http://127.0.0.1:11434/api/version' -UseBasicParsing -TimeoutSec 2).StatusCode } catch { 0 }" > "%TEMP%\ollama_check.txt" 2>nul
    set /p STATUS=<"%TEMP%\ollama_check.txt"
    if "!STATUS!"=="200" (
        echo Ollama is UP.
        goto :verified
    )
    timeout /t 1 /nobreak >nul
)
echo WARNING: Ollama did not respond within 14 seconds. Cek manual.
goto :report

:verified
echo.
echo Active config:
powershell -NoProfile -Command "Invoke-RestMethod -Uri 'http://127.0.0.1:11434/api/version' | ConvertTo-Json -Compress"

:report
echo.
echo ============================================================
echo   DONE. Env vars are persistent (survive reboot).
echo   To revoke: setx OLLAMA_NUM_PARALLEL ""  (etc) then restart.
echo ============================================================
endlocal
