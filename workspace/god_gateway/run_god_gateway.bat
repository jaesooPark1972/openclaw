@echo off
title 🦞 OpenClaw God Gateway Nexus v6.0.0-GOD
cd /d "D:\OpenClaw"

echo ========================================================
echo   🦞 OpenClaw God Gateway Nexus v6.0.0-GOD
echo   Sovereign Mode: Full Autonomy & System Control
echo ========================================================
echo.

REM Check and start required services
echo [1/5] Checking core services...

REM Check PostgreSQL
tasklist /FI "IMAGENAME eq postgres.exe" 2>NUL | find /I /N "postgres.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo    - PostgreSQL: Running
) else (
    echo    - PostgreSQL: Not running (vector DB will use fallback)
)

REM Check Ollama
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo    - Ollama: Running
) else (
    echo    - Ollama: Not running
)

echo.
echo [2/5] Starting God Gateway API (Port 8095)...
start "God Gateway Nexus API" "F:\Vivace\venv\Scripts\python.exe" "mcp_servers\god_gateway_nexus_v5.py"

echo [3/5] Starting Secretary Services (Ports 8091-8092)...
if exist "workspace\secretary\run_secretary.bat" (
    start "Secretary Services" /min cmd /c "cd /d D:\OpenClaw\workspace\secretary && run_secretary.bat"
) else (
    echo    - Secretary batch file not found
)

echo [4/5] Verifying AGen MCP servers...
if exist "F:\AGen\mcp_servers" (
    echo    - AGen MCP servers: Available at F:\AGen\mcp_servers
) else (
    echo    - AGen MCP servers: Not found
)

echo [5/5] Checking Everything Search...
if exist "C:\Program Files\Everything\Everything.exe" (
    echo    - Everything Search: Available
) else (
    echo    - Everything Search: Not installed
)

echo.
echo ========================================================
echo   ✅ God Gateway Nexus is ONLINE (ML Enabled)
echo ========================================================
echo.
echo   📡 API Server: http://localhost:8095
echo   📋 Docs:        http://localhost:8095/docs
echo   🗂️ Vector DB:  D:\OpenClaw\workspace\vector_db
echo.
echo   🔗 Integrated Systems:
echo      - OpenClaw: D:\OpenClaw
echo      - Vivace:   F:\Vivace (Port 8080)
echo      - ComfyUI:  F:\ComfyUI (Port 8188)
echo      - AGen:     F:\AGen
echo      - Secretary: Ports 8091-8092
echo.
echo ========================================================
echo.
echo Press any key to close...
pause >nul
