@echo off
echo 🔱 SOVEREIGN CLEANUP: PREPARING FOR SHIPMENT...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo [+] Purging Massive Root Logs...
del /q *.log >nul 2>&1

echo [+] Cleaning up Legacy Artifacts...
rmdir /s /q core_real >nul 2>&1

echo [+] Moving Scratch scripts to vault (optional)...
echo [!] NOTE: Scratch folder is now IGNORED by Git.

echo [+] Refreshing Git Cache...
git rm -r --cached . >nul 2>&1
git add . >nul 2>&1

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ✅ CLEANUP COMPLETE. 
echo [!] Ready for: git commit -m "v4.2.5 Hardened Release"
pause
