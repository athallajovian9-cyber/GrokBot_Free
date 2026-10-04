@echo off
setlocal
cd /d "%~dp0"

where pythonw >nul 2>&1
if %errorlevel% neq 0 (
    where python >nul 2>&1
    if %errorlevel% neq 0 exit /b 1
)

start "" pythonw "%~dp0desktop_app.py"
exit
