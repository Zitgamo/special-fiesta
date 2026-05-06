@echo off
title SOVEREIGN RECOVERY & LAUNCH
echo --- INITIALIZING SELF-HEAL WATCHDOG ---
start /min python core_v3/self_heal.py
timeout /t 5
echo --- LAUNCHING ALPHA SQUADRON ---
start python core_v3/master.py ALPHA
echo --- LAUNCHING OMEGA SQUADRON ---
start python core_v3/master.py OMEGA
echo --- LAUNCHING GAMMA SQUADRON ---
start python core_v3/master.py GAMMA
echo --- LAUNCHING POSITION MONITOR ---
start python core_v3/position_monitor.py
echo --- FLEET RE-ESTABLISHED ---
pause
