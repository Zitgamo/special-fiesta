@echo off
title 🛡️ SOVEREIGN ALPHA 12H STRESS TEST
echo ====================================================
echo INITIATING PHASE 2: ALPHA STRESS TEST (12H)
echo ====================================================
echo.
echo [1/3] Verifying Demo Mode (CORE_MODE = 0)
python -c "import sqlite3; conn=sqlite3.connect('core_v3/iron_core.db'); c=conn.cursor(); c.execute(\"UPDATE hq_config SET value='0' WHERE key='CORE_MODE'\"); conn.commit(); conn.close()"
echo [OK] DEMO MODE LOCKED.
echo.

echo [2/3] Initializing Sovereign Nexus Dashboard...
start http://127.0.0.1:5050/
echo [OK] Dashboard launched.
echo.

echo [3/3] Deploying Iron Sentinel (Overwatch Guard)...
echo ⚠️ WARNING: DO NOT CLOSE THIS WINDOW.
echo ⚠️ TO STOP, CLOSE THIS WINDOW OR RUN KILL_SWITCH.bat.
echo.
python core_v3/sentinel.py

pause
