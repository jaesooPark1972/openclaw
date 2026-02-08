@echo off
chcp 65001 >nul
echo Starting Pony Alpha API Server...
call "F:\Vivace\venv\Scripts\activate.bat"
python pony_api.py
pause
