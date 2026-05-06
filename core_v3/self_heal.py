import os
import subprocess
import time
import MetaTrader5 as mt5
import psutil
import json

# --- CONFIGURATION ---
TERMINAL_PATH = r"C:\Program Files\MetaTrader 5 EXNESS\terminal64.exe"
MAX_RETRIES = 3
CHECK_INTERVAL = 300 # Check every 5 minutes

def kill_terminal():
    print(" !! [SELF_HEAL] Attempting to kill frozen terminal64.exe...")
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'terminal64.exe':
            try:
                proc.kill()
                print(" >> [SELF_HEAL] Process terminated.")
            except Exception as e:
                print(f" !! [SELF_HEAL_ERR] Kill failed: {e}")

def restart_terminal():
    print(f" >> [SELF_HEAL] Restarting MT5 from: {TERMINAL_PATH}")
    try:
        subprocess.Popen([TERMINAL_PATH], creationflags=subprocess.DETACHED_PROCESS)
        print(" >> [SELF_HEAL] MT5 Launch signal sent. Waiting for boot (30s)...")
        time.sleep(30)
    except Exception as e:
        print(f" !! [SELF_HEAL_ERR] Restart failed: {e}")

def verify_connection():
    if not mt5.initialize():
        print(" !! [SELF_HEAL] MT5 Initialization failed.")
        return False
    
    print(" >> [SELF_HEAL] MT5 Neural Link Re-established.")
    mt5.shutdown()
    return True

def run_watchdog():
    print("--- SOVEREIGN SELF-HEAL WATCHDOG ACTIVE ---")
    while True:
        try:
            # 1. Check if MT5 can initialize
            if not mt5.initialize():
                print(" !! [WATCHDOG] Connection fractured. Terminal may be frozen.")
                kill_terminal()
                time.sleep(5)
                restart_terminal()
                
                # 2. Verify recovery
                if verify_connection():
                    print(" >> [SUCCESS] Terminal recovered successfully.")
                else:
                    print(" !! [FAILURE] Recovery failed. Manual intervention may be required.")
            else:
                # MT5 is fine, just shutdown the temp link
                mt5.shutdown()
                # print(" >> [WATCHDOG] MT5 Heartbeat: OK")
                
            time.sleep(CHECK_INTERVAL)
        except Exception as e:
            print(f" !! [WATCHDOG_ERR] {e}")
            time.sleep(60)

if __name__ == "__main__":
    run_watchdog()
