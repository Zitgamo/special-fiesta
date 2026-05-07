@echo off
title HANG_DA_SOVEREIGN_WATCHDOG
setlocal enabledelayedexpansion

:LOOP
:: 1. Check Morning Ritual (08:15 - Genetic Rebirth)
set "cur_time=%time:~0,5%"
if "!cur_time!"==" 8:15" (
    echo [!date! !time!] Initiating Genetic Rebirth...
    python core_v3/dual_dna_harvester.py
    timeout /t 65
)

:: 2. Check Morning Prophecy (08:35 - High Council)
if "!cur_time!"==" 8:35" (
    echo [!date! !time!] Initiating Morning Prophecy...
    python core_v3/high_council.py --morning
    timeout /t 65
)

:: 3. Run the Bridge (Ensure Persistence)
echo [!date! !time!] Sovereign Bridge Heartbeat...
python core_v3/southern_paper_bridge.py

echo [!date! !time!] Bridge crashed or exited. Restarting in 10s...
timeout /t 10
goto LOOP
