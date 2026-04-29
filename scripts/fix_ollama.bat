@echo off
:: Antigravity Ollama Connectivity Fixer
:: This script sets the required environment variables and restarts Ollama.

echo ========================================================
echo   🚀 Antigravity Ollama Connectivity Fixer
echo ========================================================
echo.

:: Check for Administrator privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Administrator privileges confirmed.
) else (
    echo [ERROR] Please run this script as Administrator!
    pause
    exit /b 1
)

echo.
echo [1/3] Setting OLLAMA_HOST to 0.0.0.0 (Global Access)...
setx OLLAMA_HOST "0.0.0.0" /M
if %errorLevel% == 0 (
    echo      Success.
) else (
    echo      Failed to set OLLAMA_HOST.
)

echo.
echo [2/3] Setting OLLAMA_ORIGINS to * (CORS Bypass)...
setx OLLAMA_ORIGINS "*" /M
if %errorLevel% == 0 (
    echo      Success.
) else (
    echo      Failed to set OLLAMA_ORIGINS.
)

echo.
echo [3/3] Restarting Ollama...
echo      Killing existing Ollama processes...
taskkill /F /IM ollama.exe /T >nul 2>&1
taskkill /F /IM "ollama app.exe" /T >nul 2>&1

timeout /t 2 /nobreak >nul

echo      Relaunching Ollama...
set "OLLAMA_PATH_1=%LOCALAPPDATA%\Programs\Ollama\ollama app.exe"
set "OLLAMA_PATH_2=%LOCALAPPDATA%\Ollama\ollama app.exe"

if exist "%OLLAMA_PATH_1%" (
    start "" "%OLLAMA_PATH_1%"
) else if exist "%OLLAMA_PATH_2%" (
    start "" "%OLLAMA_PATH_2%"
) else (
    echo [WARN] Could not find 'ollama app.exe' automatically.
    echo        Please start Ollama manually from your Start Menu.
)

echo.
echo ========================================================
echo   ✅ FIX COMPLETE!
echo   Ollama is now configured for Docker connectivity.
echo   Please wait a few seconds, then refresh Open WebUI.
echo ========================================================
echo.
pause
