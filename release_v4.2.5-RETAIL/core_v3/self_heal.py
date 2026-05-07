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
            # 1. Check if MT5 process is running
            mt5_proc = None
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] == 'terminal64.exe':
                    mt5_proc = proc
                    break
            
            if not mt5_proc:
                print(" !! [WATCHDOG] MT5 Terminal not running. Launching...")
                restart_terminal()
                continue

            # 2. Check if MT5 can initialize (Silent Check)
            if not mt5.initialize():
                print(" !! [WATCHDOG] Connection fractured. Checking process health...")
                
                # If process is not responding or we've failed too many times, then kill
                if not mt5_proc.is_running():
                    print(" !! [WATCHDOG] Process found dead. Restarting...")
                    restart_terminal()
                else:
                    # Maybe it's just busy. Let's not kill it immediately.
                    # Instead, we'll try to re-initialize with path ONLY IF it's really stuck.
                    print(" >> [WATCHDOG] Process is alive but busy. Waiting for next cycle.")
            else:
                # MT5 is fine. Keep the link alive, don't shutdown.
                # print(" >> [WATCHDOG] MT5 Heartbeat: OK")
                pass
                
            time.sleep(CHECK_INTERVAL)
        except Exception as e:
            print(f" !! [WATCHDOG_ERR] {e}")
            time.sleep(60)

if __name__ == "__main__":
    run_watchdog()
