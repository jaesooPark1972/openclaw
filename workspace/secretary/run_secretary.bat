@echo off
title OpenClaw Secretary Service (Orchestrator + TTS)
cd /d "D:\OpenClaw\workspace\secretary"

echo [1/3] Checking Ollama...
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo    - Ollama is running.
) else (
    echo    - Starting Ollama...
    start /min "Ollama Service" ollama serve
)

echo [2/3] Starting Secretary Orchestrator (Port 8091)...
start "Secretary Orchestrator" "F:\Vivace\venv\Scripts\python.exe" "D:\OpenClaw\workspace\secretary\secretary_api.py"

echo [3/3] Starting Qwen-TTS Engine (Port 8092)...
start "Qwen-TTS Engine" "F:\Vivace\venv\Scripts\python.exe" "D:\OpenClaw\workspace\secretary\qwen_tts_server.py"

echo.
echo ========================================================
echo   OpenClaw Secretary Service is ONLINE
echo   - Orchestrator: http://localhost:8091/docs
echo   - TTS Engine:   http://localhost:8092/docs
echo ========================================================
echo.
pause
