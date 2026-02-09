@echo off
chcp 65001 >nul
echo ---------------------------------------------------
echo 🔄 Vivace Supplement Sync (F: -> E:) Missing Folders
echo ---------------------------------------------------

if not exist "E:\vivace_music" mkdir "E:\vivace_music"

echo [1/3] Syncing CONFIG (Essential Constants)...
robocopy "F:\Vivace\config" "E:\vivace_music\config" /E /MT:16 /XD "__pycache__" /R:1 /W:1 /NP /NFL /NDL >nul

echo [2/3] Syncing FAIRSEQ (Voice Lib)...
robocopy "F:\Vivace\fairseq" "E:\vivace_music\fairseq" /E /MT:16 /XD "__pycache__" ".git" /R:1 /W:1 /NP /NFL /NDL >nul

echo [3/3] Syncing RESOURCES (Icons/Assets)...
robocopy "F:\Vivace\resources" "E:\vivace_music\resources" /E /MT:16 /XD "__pycache__" /R:1 /W:1 /NP /NFL /NDL >nul

echo.
echo [Verification]
if exist "E:\vivace_music\config\constants.py" (
    echo ✅ config\constants.py exists.
) else (
    echo ❌ config\constants.py MISSING.
)
if exist "E:\vivace_music\fairseq" (
    echo ✅ fairseq folder exists.
) else (
    echo ❌ fairseq folder MISSING.
)
if exist "E:\vivace_music\resources" (
    echo ✅ resources folder exists.
) else (
    echo ❌ resources folder MISSING.
)

echo ---------------------------------------------------
echo ✅ Supplement Sync Completed.
echo ---------------------------------------------------
