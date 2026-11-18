@echo off
title AGRISHIELD Live Server & Public Tunnel
echo ===================================================================
echo     AGRISHIELD MULTI-CROP ENTERPRISE CROP PATHOLOGY SUITE
echo         (Local Server on 8000 + Public Cloudflare Tunnel)
echo ===================================================================

echo [1/3] Starting AGRISHIELD Backend on Port 8000...
start /min "AGRISHIELD Backend" python backend\server.py

timeout /t 2 /nobreak >nul

echo [2/3] Checking Cloudflare Tunnel binary...
if not exist "%TEMP%\cloudflared.exe" (
    echo Downloading cloudflared...
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe' -OutFile '%TEMP%\cloudflared.exe'"
)

echo [3/3] Starting Public Cloudflare Tunnel...
start "Cloudflare Public Tunnel" "%TEMP%\cloudflared.exe" tunnel --url http://127.0.0.1:8000

start "" "http://localhost:8000"
echo.
echo AGRISHIELD is running locally at http://localhost:8000
echo The Cloudflare window will show your public HTTPS link (trycloudflare.com).
echo Keep this window open to keep the public tunnel alive.
echo ===================================================================
pause
