import subprocess
import os

def run_git(cmd):
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f">> SUCCESS: {' '.join(cmd)}")
        if res.stdout: print(res.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"!! FAILED: {' '.join(cmd)}")
        print(f"   Error: {e.stderr}")
        return False

print("--- SOVEREIGN GIT AUTO-SYNC ---")

# 1. Refresh Gitignore cache (remove files that are now ignored)
run_git(["git", "rm", "-r", "--cached", ".", "--quiet"])

# 2. Add all current files (respecting new gitignore)
run_git(["git", "add", "."])

# 3. Commit stability milestone
msg = "STABILITY_HARDENING_V4.0: Isolated Equity, Binance Fixes, Tactical Guardrails & VN30 Hibernation"
run_git(["git", "commit", "-m", msg])

# 4. Push (optional, depends on origin)
print("--- SYNC COMPLETE ---")
