@echo off
chcp 65001 >nul
echo ========================================================
echo   🦞 OpenClaw Model Organizer
echo   C:\ -> D:\Models 이동 및 정리
echo ========================================================
echo.

REM 설정
set "SOURCE_CACHE=C:\Users\JayPark1004\.cache\huggingface"
set "DEST_ROOT=D:\Models"

echo [1/6] 디렉토리 구조 생성...
mkdir "%DEST_ROOT%\huggingface\hub" 2>nul
mkdir "%DEST_ROOT%\llm\quantized" 2>nul
mkdir "%DEST_ROOT%\audio\musicgen" 2>nul
mkdir "%DEST_ROOT%\embedding" 2>nul
mkdir "%DEST_ROOT%\video" 2>nul
echo    - 완료

echo [2/6] 모델 이동 시작...

REM ======= C:\Users\JayPark1004\.cache\huggingface =======
echo.
echo 📦 HuggingFace 캐시 이동...

REM MusicGen-Large (3.4GB)
if exist "%SOURCE_CACHE%\hub\models--facebook--musicgen-large\snapshots" (
    echo    → MusicGen-Large (3.4GB) 이동 중...
    robocopy "%SOURCE_CACHE%\hub\models--facebook--musicgen-large" "%DEST_ROOT%\audio\musicgen\musicgen-large" /E /MOVE /R:3 /W:5 /NFL /NDL /NJH /NJS
    echo    - 완료
)

REM MusicGen-Medium (3.2GB)
if exist "%SOURCE_CACHE%\hub\models--facebook--musicgen-medium\snapshots" (
    echo    → MusicGen-Medium (3.2GB) 이동 중...
    robocopy "%SOURCE_CACHE%\hub\models--facebook--musicgen-medium" "%DEST_ROOT%\audio\musicgen\musicgen-medium" /E /MOVE /R:3 /W:5 /NFL /NDL /NJH /NJS
    echo    - 완료
)

REM Sentence-Transformers (91MB)
if exist "%SOURCE_CACHE%\hub\models--sentence-transformers--all-MiniLM-L6-v2\snapshots" (
    echo    → Sentence-Transformers (91MB) 이동 중...
    robocopy "%SOURCE_CACHE%\hub\models--sentence-transformers--all-MiniLM-L6-v2" "%DEST_ROOT%\embedding\all-MiniLM-L6-v2" /E /MOVE /R:3 /W:5 /NFL /NDL /NJH /NJS
    echo    - 완료
)

REM ACE-Step
if exist "%SOURCE_CACHE%\hub\models--ACE-Step" (
    echo    → ACE-Step 이동 중...
    robocopy "%SOURCE_CACHE%\hub\models--ACE-Step" "%DEST_ROOT%\huggingface\hub\models--ACE-Step" /E /MOVE /R:3 /W:5 /NFL /NDL /NJH /NJS
    echo    - 완료
)

REM Wan-AI (Wan2.1)
if exist "%SOURCE_CACHE%\hub\models--Wan-AI" (
    echo    → Wan2.1 이동 중...
    robocopy "%SOURCE_CACHE%\hub\models--Wan-AI" "%DEST_ROOT%\video\wan2.1" /E /MOVE /R:3 /W:5 /NFL /NDL /NJH /NJS
    echo    - 완료
)

REM ======= C:\AI-Models =======
echo.
echo 📦 GGUF 모델 이동...

if exist "C:\AI-Models\Qwen3-8B-Coder-Abliterated-Q4_K_M.gguf" (
    echo    → Qwen3-8B-Coder 이동 중...
    move "C:\AI-Models\Qwen3-8B-Coder-Abliterated-Q4_K_M.gguf" "%DEST_ROOT%\llm\quantized\" >nul
    rmdir "C:\AI-Models" 2>nul
    echo    - 완료
)

REM ======= F:\AGen\models =======
echo.
echo 📦 AGen 모델 이동...

if exist "F:\AGen\models\brain.gguf" (
    echo    → brain.gguf 이동 중...
    move "F:\AGen\models\brain.gguf" "%DEST_ROOT%\llm\brain.gguf" >nul
    echo    - 완료
)

echo [3/6] 이동 완료!

echo [4/6] D:\Models 구조 확인...
echo.
tree "%DEST_ROOT%" /F 2>nul | head -60

echo.
echo [5/6] 원본 정리...
rmdir "%SOURCE_CACHE%\hub\models--facebook" /S /Q 2>nul
rmdir "%SOURCE_CACHE%\hub\models--ACE-Step" /S /Q 2>nul
rmdir "%SOURCE_CACHE%\hub\models--Wan-AI" /S /Q 2>nul
rmdir "%SOURCE_CACHE%\hub\models--sentence-transformers" /S /Q 2>nul
echo    - C:\Users\JayPark1004\.cache\huggingface 정리 완료

echo [6/6] 완료!
echo.
echo ========================================================
echo   ✅ 모델 이동 완료!
echo ========================================================
echo.
echo 📂 새 위치: D:\Models
echo.
echo 💾 예상 절감 공간: 약 7-10GB
echo.
pause
