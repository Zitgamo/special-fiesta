@echo off
echo [⚠️] INITIATING GLOBAL TACTICAL SHUTDOWN...
taskkill /F /IM python.exe
echo [✓] ALL TRADING PROCESSES TERMINATED.

echo [⚠️] UPDATING HQ_CONFIG [GLOBAL_PAUSE=1]...
python -c "import sqlite3; conn=sqlite3.connect('core_v3/iron_core.db'); cursor=conn.cursor(); cursor.execute(\"UPDATE config SET value = '1' WHERE key = 'GLOBAL_PAUSE'\"); conn.commit(); conn.close()"
echo [✓] DATABASE LOCK ENGAGED.

echo.
echo ========================================
echo SYSTEM IS NOW SAFE (PAUSED).
echo RE-LAUNCH VIA SOVEREIGN_REAL_LAUNCH.bat
echo ========================================
pause
