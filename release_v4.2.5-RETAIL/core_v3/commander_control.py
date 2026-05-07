import os
import subprocess
import sys
import time

# --- DYNAMIC ROOT DETECTION ---
# Automatically find the IRON_COMMANDER root directory
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE_DIR = os.path.join(ROOT_DIR, "core_v3")

def start_all():
    print(f"--- INITIALIZING SOVEREIGN FLEET AT {ROOT_DIR} ---")
    
    fleet = {
        "MASTER": os.path.join(CORE_DIR, "master.py"),
        "SENTINEL": os.path.join(CORE_DIR, "sentinel.py"),
        "NEXUS": os.path.join(CORE_DIR, "nexus_bridge.py")
    }
    
    for name, path in fleet.items():
        if os.path.exists(path):
            print(f" >> Launching {name}...")
            # Use subprocess.Popen to run in background
            subprocess.Popen([sys.executable, path], cwd=ROOT_DIR)
            time.sleep(2)
        else:
            print(f" !! FAILED to find {name} at {path}")

def stop_all():
    print("--- TERMINATING FLEET ---")
    import psutil
    for proc in psutil.process_iter(['cmdline']):
        try:
            cmd = proc.info['cmdline']
            if not cmd: continue
            cmd_str = " ".join(cmd).lower()
            if any(k in cmd_str for k in ["master.py", "sentinel.py", "engine.py", "nexus_bridge.py"]):
                print(f" >> Grounding {proc.name()} (PID: {proc.pid})")
                proc.terminate()
        except: pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python commander_control.py [start|stop]")
        sys.exit(1)
        
    cmd = sys.argv[1].lower()
    if cmd == "start":
        start_all()
    elif cmd == "stop":
        stop_all()
    else:
        print(f"Unknown command: {cmd}")
