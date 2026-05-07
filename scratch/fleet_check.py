import psutil
import os

fleet = ["master.py", "nexus_bridge.py", "ghost_comm.py", "engine.py", "southern_paper_bridge.py"]
print("--- FLEET STATUS CHECK ---")
for proc in psutil.process_iter(['cmdline']):
    try:
        cmd = proc.info['cmdline']
        if cmd:
            cmd_str = " ".join(cmd).lower()
            for f in fleet:
                if f in cmd_str:
                    print(f"🟢 [ACTIVE] {f} | PID: {proc.pid}")
    except: pass
print("--- END ---")
