@echo off
chcp 65001 >nul
echo ---------------------------------------------------
echo 🔄 Vivace Engine Sync (F: -> E:)
echo ---------------------------------------------------

if not exist "F:\Vivace" (
    echo ❌ F:\Vivace not found.
    exit /b 1
)
if not exist "E:\vivace_music" (
    echo ⚠️ E:\vivace_music missing. Creating...
    mkdir "E:\vivace_music"
)

echo [1/5] Syncing Modules (Code)...
robocopy "F:\Vivace\modules" "E:\vivace_music\modules" /E /MT:16 /XD "__pycache__" /R:1 /W:1 /NP /NFL /NDL >nul

echo [2/5] Syncing Root Scripts...
robocopy "F:\Vivace" "E:\vivace_music" "*.py" "*.bat" "*.json" "*.md" /XD ".venv" "__pycache__" ".git" "modules" "vivace-studio" "output" "gradio_outputs" "ace_step_1_5" "vivace-core" /XF ".env" /R:1 /W:1 /NP /NFL /NDL >nul

echo [3/5] Syncing Subsystems (UI/Assets)...
robocopy "F:\Vivace\ace_step_1_5" "E:\vivace_music\ace_step_1_5" /E /MT:16 /XD "__pycache__" /R:1 /W:1 /NP /NFL /NDL >nul
robocopy "F:\Vivace\vivace-studio" "E:\vivace_music\vivace-studio" /E /MT:16 /XD "node_modules" ".git" /R:1 /W:1 /NP /NFL /NDL >nul
robocopy "F:\Vivace\vivace-core" "E:\vivace_music\vivace-core" /E /MT:16 /XD "target" ".git" /R:1 /W:1 /NP /NFL /NDL >nul

if exist "F:\Vivace\vivace-core\target\release" (
    echo    + Syncing Rust Binaries...
    robocopy "F:\Vivace\vivace-core\target\release" "E:\vivace_music\vivace-core\target\release" "*.exe" "*.dll" /R:1 /W:1 /NP /NFL /NDL >nul
)

echo [4/5] Setting up Virtual Environment (Junction)...
if not exist "E:\vivace_music\.venv" (
    if exist "F:\Vivace\venv" (
        mklink /J "E:\vivace_music\.venv" "F:\Vivace\venv" >nul
        echo 🔗 Linked .venv -> F:\Vivace\venv
    ) else if exist "F:\Vivace\.venv" (
        mklink /J "E:\vivace_music\.venv" "F:\Vivace\.venv" >nul
        echo 🔗 Linked .venv -> F:\Vivace\.venv
    )
)

echo.
echo [Verification]
if exist "E:\vivace_music\modules\engine\stem_separator.py" (
    echo ✅ Verification SUCCESS: stem_separator.py synced.
) else (
    echo ❌ Verification FAILED: stem_separator.py MISSING.
)
echo ---------------------------------------------------
echo ✅ Sync Task Completed.
