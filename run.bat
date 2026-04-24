@echo off
echo Starting Open WebUI (b13)...
echo.

:: Check if .env exists
if not exist .env (
    echo Creating missing .env file...
    echo OPEN_WEBUI_PORT=3013 > .env
    echo WEBUI_SECRET_KEY=secret_key_change_me >> .env
    echo SCARF_NO_ANALYTICS=true >> .env
    echo DO_NOT_TRACK=true >> .env
    echo ANONYMIZED_TELEMETRY=false >> .env
    echo WORKSPACE_DIR=E:\AntiGravityProject >> .env
    echo WORKSPACE_MAX_FILE_SIZE=5242880 >> .env
)

echo Building and starting Docker containers...
docker compose up -d --build

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Failed to start Docker containers. Please ensure Docker Desktop is running.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Open WebUI is starting!
echo Access it at: http://localhost:3013
echo.
echo Opening browser...
start http://localhost:3013

echo.
echo Press any key to stop the containers or close this window to keep them running.
pause

echo Stopping containers...
docker compose down
