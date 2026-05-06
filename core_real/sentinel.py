import psutil
import subprocess
import time
import os

class IronSentinel:
    """
    Zero-Latency Self-Healing Guard.
    Watches the fleet and resurrects any fallen process.
    """
    def __init__(self):
        self.fleet = {
            "MASTER_REAL": "core_real/master.py",
            "BRIDGE_REAL": "core_real/nexus_bridge.py",
            "ALPHA_REAL": ["core_real/engine.py", "ALPHA"],
            "OMEGA_REAL": ["core_real/engine.py", "OMEGA"],
            "GAMMA_REAL": ["core_real/engine.py", "GAMMA"]
        }
        self.is_running = True

    def is_alive(self, name):
        """Checks if a process is alive by its command line arguments."""
        for proc in psutil.process_iter(['cmdline']):
            try:
                cmd = proc.info['cmdline']
                if not cmd: continue
                
                cmd_str = " ".join(cmd).lower()
                
                # Check for unique identifiers (Targeting core_real)
                if "core_real" not in cmd_str: continue
                
                if name == "ALPHA_REAL" and "alpha" in cmd_str: return True
                if name == "OMEGA_REAL" and "omega" in cmd_str: return True
                if name == "GAMMA_REAL" and "gamma" in cmd_str: return True
                if name == "MASTER_REAL" and "master.py" in cmd_str: return True
                if name == "BRIDGE_REAL" and "nexus_bridge.py" in cmd_str: return True
            except: continue
        return False

    def resurrect(self, name):
        print(f" !! [SENTINEL] {name} has fallen! Initiating Emergency Resurrection...")
        path_data = self.fleet[name]
        base = os.getcwd()
        
        if isinstance(path_data, list):
            cmd = ["python", os.path.join(base, path_data[0]), path_data[1]]
            subprocess.Popen(cmd)
        else:
            cmd = ["python", os.path.join(base, path_data)]
            subprocess.Popen(cmd)
            
        print(f" >> [SUCCESS] {name} is back online.")

    def run(self):
        print("--- IRON SENTINEL REAL v3.0 ACTIVE ---")
        import sys
        sys.path.append(os.path.join(os.getcwd(), 'core_real'))
        from system_integrity_check import check_integrity_silent
        
        while self.is_running:
            # 1. THE SUPREME AUDIT
            audit_pass, report = check_integrity_silent()
            if not audit_pass:
                print(f" !! [REAL_VIOLATION] {report}. STAND DOWN!")
                time.sleep(60)
                continue
                
            # 2. RESURRECTION LOOP
            for name in self.fleet:
                if not self.is_alive(name):
                    self.resurrect(name)
            
            # 3. HEARTBEAT AUDIT
            self.heartbeat_audit()
            
            time.sleep(10)

    def heartbeat_audit(self):
        try:
            import sqlite3
            db_path = os.path.join(os.getcwd(), "core_real", "iron_core.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM trades WHERE type = 'LIVE'")
            active_count = cursor.fetchone()[0]
            conn.close()
            
            if active_count == 0:
                trigger_path = os.path.join(os.getcwd(), "core_real", "scan_trigger.tmp")
                if not os.path.exists(trigger_path) or time.time() - os.path.getmtime(trigger_path) > 3600:
                    print(" !! [SENTINEL_REAL] Fleet Idle. Triggering scan...")
                    with open(trigger_path, "w") as f:
                        f.write(str(time.time()))
        except Exception as e:
            print(f" !! [SENTINEL_ERR] Heartbeat audit failed: {e}")

if __name__ == "__main__":
    sentinel = IronSentinel()
    sentinel.run()
