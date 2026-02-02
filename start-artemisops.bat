@echo off
title ArtemisOps Launcher
echo ========================================
echo    ArtemisOps Mission Control Launcher
echo ========================================
echo.

:: Check if server is already running on port 8080
netstat -ano | findstr ":8080.*LISTENING" >nul 2>&1
if %errorlevel%==0 (
    echo [OK] Server already running on port 8080
) else (
    echo [..] Starting ArtemisOps server...
    cd /d C:\Users\john_\ArtemisOps\server
    start "ArtemisOps Server" cmd /c ".\venv\Scripts\python.exe main.py"
    echo [OK] Server starting...
    :: Wait a moment for server to initialize
    timeout /t 3 /nobreak >nul
)

echo.
echo [..] Opening ArtemisOps in Chrome...
start "" "chrome.exe" "http://localhost:8080"

echo.
echo ========================================
echo ArtemisOps is ready!
echo ========================================
timeout /t 2 /nobreak >nul
