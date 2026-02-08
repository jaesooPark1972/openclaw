@echo off
chcp 65001 >nul
echo ========================================
echo  OpenClaw REST API Bridge Launcher
echo ========================================
echo.

REM 가상환경 체크 및 생성
if not exist ".venv_api" (
    echo 가상환경 생성 중...
    python -m venv .venv_api
)

echo 가상환경 활성화...
call .venv_api\Scripts\activate.bat

echo 의존성 설치 중...
pip install -q -r api_requirements.txt

echo.
echo ========================================
echo  서버 시작 중...
echo ========================================
echo REST API: http://localhost:8081
echo Telegram Bot: @park_vivace_bot
echo.
echo 사용법:
echo 1. 텔레그램에서 @park_vivace_bot 찾기
echo 2. /start 입력
echo 3. 원하는 명령 입력 (예: "파일 목록 보여줘")
echo 4. 승인/거부 버튼 클릭
echo.
echo 종료하려면 Ctrl+C를 누르세요
echo ========================================
echo.

python api_bridge.py

pause
