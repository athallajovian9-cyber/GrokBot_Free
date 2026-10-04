@echo off
setlocal
cd /d "%~dp0"

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found on PATH.
    pause
    exit /b 1
)

echo.
echo   ==================================================
echo     GROK BOT (FREE LOCAL EDITION)
echo     An AI Teammate with its own Computer Tools
echo   ==================================================
echo.
echo   Opening Grok Bot web app in your browser...
echo.

start "" "http://127.0.0.1:8088"
python "%~dp0server.py"

pause
