@echo off
title OpenClaw Gateway (Vivace AI)
echo ========================================================
echo       Starting OpenClaw Gateway (Vivace System)
echo ========================================================
echo.
echo [1/3] Moving to installation directory...
cd /d "D:\OpenClaw"

echo [2/3] Setting environment variables...
set OPENCLAW_NO_RESPAWN=1

echo [3/3] Launching Gateway via NPM...
echo.
echo * Web Dashboard: http://localhost:18789
echo * Telegram Bot: @park_vivace_bot
echo.
echo Press Ctrl+C to stop the server.
echo.

rem Use npm start instead of direct dist file execution (since dist might not exist)
npm run start -- gateway --verbose --port 18789

pause
