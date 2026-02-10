@echo off
chcp 65001 > nul
echo 🚀 Launching AirLLM (OpenClaw) on Low-VRAM Mode...
echo ⚠️ PLEASE WAIT: This uses f:/vivace/venv (where airllm is installed)
echo.

set PYTHON_PATH=f:\vivace\venv\Scripts\python.exe

if not exist "%PYTHON_PATH%" (
    echo ❌ ERROR: Python not found at %PYTHON_PATH%
    echo Please check your Vivace installation path.
    pause
    exit /b
)

"%PYTHON_PATH%" d:\OpenClaw\workspace\airllm_inference.py %*

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Execution failed.
) else (
    echo.
    echo ✅ Finished.
)
pause
