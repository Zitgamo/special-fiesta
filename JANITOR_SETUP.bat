@echo off
REM SOVEREIGN JANITOR - Daily Maintenance Scheduler Setup
REM This script creates a Windows Task Scheduler task to run janitor.py daily

setlocal enabledelayedexpansion

set PYTHON_EXE=C:/Users/ADMIN/AppData/Local/Programs/Python/Python312/python.exe
set SCRIPT_PATH=%~dp0janitor.py
set TASK_NAME=IRON_COMMANDER_JANITOR

echo --- SOVEREIGN JANITOR SCHEDULER SETUP ---
echo.

REM Check if running as administrator
openfiles >nul 2>&1
if errorlevel 1 (
    echo ERROR: This script must run as Administrator
    echo Please right-click and select "Run as administrator"
    pause
    exit /b 1
)

REM Create the scheduled task
echo Creating Task Scheduler task: %TASK_NAME%...
schtasks /create /tn %TASK_NAME% /tr "\"!PYTHON_EXE!\" \"!SCRIPT_PATH!\" --run" /sc daily /st 02:00 /force

if errorlevel 0 (
    echo SUCCESS: Task created
    echo Task: %TASK_NAME%
    echo Time: Daily at 02:00 AM
    echo Script: %SCRIPT_PATH%
    echo.
    echo To verify: schtasks /query /tn %TASK_NAME%
    echo To remove: schtasks /delete /tn %TASK_NAME% /f
) else (
    echo FAILED: Could not create task
    exit /b 1
)

pause
