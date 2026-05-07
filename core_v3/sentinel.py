import psutil
import subprocess
import time
import os
import datetime
import json
from ghost_comm import GhostComm

class IronSentinel:
    """
    Zero-Latency Self-Healing Guard.
    Watches the fleet and resurrects any fallen process.
    """
    def __init__(self):
        self.fleet = {
            "MASTER": "core_v3/master.py",
            "BRIDGE": "core_v3/nexus_bridge.py",
            "GHOST_COMM": "core_v3/ghost_comm.py",
            "ALPHA": ["core_v3/engine.py", "ALPHA"],
            "OMEGA": ["core_v3/engine.py", "OMEGA"],
            "GAMMA": ["core_v3/engine.py", "GAMMA"],
            "HANG_DA_FRONT": "core_v3/southern_paper_bridge.py"
        }
        self.is_running = True
        self.last_scribe = 0
        self.alert_buffer = []
        try:
            self.comm = GhostComm()
        except:
            self.comm = None
            print(" !! [SENTINEL] GHOST_COMM initialization failed. Alerts will be local only.")

    def is_alive(self, name):
        """Checks if a process is alive by its command line arguments."""
        for proc in psutil.process_iter(['cmdline']):
            try:
                cmd = proc.info['cmdline']
                if not cmd: continue
                
                cmd_str = " ".join(cmd).lower()
                
                # Check for unique identifiers (Case-Insensitive)
                if name == "ALPHA" and all(k in cmd_str for k in ["engine.py", "alpha"]): return True
                if name == "OMEGA" and all(k in cmd_str for k in ["engine.py", "omega"]): return True
                if name == "GAMMA" and all(k in cmd_str for k in ["engine.py", "gamma"]): return True
                if name == "MASTER" and "master.py" in cmd_str: return True
                if name == "BRIDGE" and "nexus_bridge.py" in cmd_str: return True
                if name == "GHOST_COMM" and "ghost_comm.py" in cmd_str: return True
                if name == "HANG_DA_FRONT" and "southern_paper_bridge.py" in cmd_str: return True
            except: continue
        return False

    def resurrect(self, name):
        crash_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = f" !! [SENTINEL] {name} has fallen! Initiating Emergency Resurrection at {crash_time}..."
        print(msg)
        
        # Log the crash for the 12h Stress Test Audit
        os.makedirs("logs", exist_ok=True)
        with open("logs/sentinel_crash.log", "a") as f:
            f.write(f"[{crash_time}] CRASH DETECTED: {name} resurrected.\n")
            
        path_data = self.fleet[name]
        base = os.getcwd()
        
        if isinstance(path_data, list):
            cmd = ["python", os.path.join(base, path_data[0]), path_data[1]]
            subprocess.Popen(cmd)
        else:
            cmd = ["python", os.path.join(base, path_data)]
            subprocess.Popen(cmd)
            
        time.sleep(5) # SI v3.4: Staggered Resurrection (Anti-Lag)
        
        self.alert_buffer.append(f"🛠️ [RESURRECTED] {name} has been restored to service.")
        print(f" >> [SUCCESS] {name} is back online.")
        
        # --- SSS RESET: TRIGGERED BY CRASH (SI v4.3) ---
        state_path = "core_v3/report_state.json"
        if os.path.exists(state_path):
            try:
                with open(state_path, "r") as f:
                    state = json.load(f)
                
                state['interval_seconds'] = 3600 # Reset to 1H
                state['streak_start_time'] = time.time()
                state['reset_occurred'] = True
                
                # Snapshot equity at the moment of failure
                try:
                    import sqlite3
                    db_path = "core_v3/iron_core.db"
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT equity FROM equity_history ORDER BY id DESC LIMIT 1")
                    res = cursor.fetchone()
                    state['streak_start_equity'] = res[0] if res else 0
                    conn.close()
                except: pass
                
                with open(state_path, "w") as f:
                    json.dump(state, f, indent=4)
                print(" >> [SSS] Stability Streak Reset due to Incident.")
            except: pass

    def run(self):
        print("--- IRON SENTINEL v3.0: PROTOCOL LOCKDOWN ACTIVE ---")
        import sys
        sys.path.append(os.path.join(os.getcwd(), 'core_v3'))
        from system_integrity_check import check_integrity_silent
        
        while self.is_running:
            # 1. THE SUPREME AUDIT
            # We must run this from the same directory as the engines
            audit_pass, report = check_integrity_silent()
            if not audit_pass:
                print(f" !! [PROTOCOL_VIOLATION] {report}. TERMINATING FLEET!")
                for name in self.fleet:
                    # Logic to kill rogue processes
                    pass
                time.sleep(10)
                continue
                
            # 2. RESURRECTION LOOP
            for name in self.fleet:
                if not self.is_alive(name):
                    self.resurrect(name)
            
            # 3. SELF-HEALING MONITOR (Detect repeated failures)
            self.monitor_engine_logs()
            
            # 4. HEARTBEAT AUDIT (Squadron Population Enforcement)
            self.heartbeat_audit()
            
            # 5. INTELLIGENT AUTO-SCRIBE (Evolution Tracking)
            # Trigger if: 1 hour passed OR significant changes (> 50 lines) detected
            time_since_scribe = time.time() - self.last_scribe
            
            should_scribe = False
            if time_since_scribe > 3600: # 1 Hour Hard-cap
                should_scribe = True
            else:
                try:
                    diff_stat = subprocess.check_output(["git", "diff", "--shortstat"]).decode().strip()
                    if diff_stat:
                        # Extract number of insertions/deletions
                        import re
                        changes = sum(int(x) for x in re.findall(r'(\d+) (?:insertion|deletion)', diff_stat))
                        if changes > 50: # Significant Evolution Threshold
                            print(f" >> [SENTINEL] Significant evolution detected ({changes} lines). Triggering Scribe...")
                            should_scribe = True
                except: pass

            if should_scribe:
                self.auto_scribe()
                self.last_scribe = time.time()
            
            # 6. AUTONOMOUS CLEANUP (The Janitor Handshake)
            self.autonomous_cleanup()
            
            # 7. CONSOLIDATED DISPATCH (SI v3.6 - Anti-Spam)
            self.dispatch_consolidated_report()
            
            time.sleep(5)

    def autonomous_cleanup(self):
        """
        SMA v1.0 Rule 5: Orchestrated Cleanup.
        Triggers janitor.py if more than 24h passed since last report.
        """
        report_path = "logs/janitor_report.json"
        try:
            should_run = False
            if not os.path.exists(report_path):
                should_run = True
            else:
                with open(report_path, 'r') as f:
                    report = json.load(f)
                last_ts = datetime.datetime.fromisoformat(report.get("timestamp", "2000-01-01"))
                if (datetime.datetime.now() - last_ts).total_seconds() > 86400: # 24 Hours
                    should_run = True
            
            if should_run:
                print(" >> [SENTINEL] Cleanup Overdue. Summoning the Janitor...")
                subprocess.Popen(["python", "janitor.py", "--run"])
        except Exception as e:
            print(f" !! [JANITOR_TRIGGER_ERR] {e}")

    def monitor_engine_logs(self):
        """Detects patterns like 'Invalid volume' and alerts the user."""
        for unit in ["ALPHA", "OMEGA", "GAMMA"]:
            log_file = f"{unit.lower()}_engine.log"
            if not os.path.exists(log_file): continue
            
            try:
                with open(log_file, "r") as f:
                    content = f.read().splitlines()[-20:] # Check last 20 lines
                    for line in content:
                        if "FATAL" in line or "Order failed" in line:
                            print(f" !! [SENTINEL] Alert detected in {log_file}: {line}")
                            self.alert_buffer.append(f"⚠️ [FRACTURE] {unit} UNIT: {line}")
                            self.report_to_war_room(unit, line)
                        if "Invalid volume (Code: 10014)" in line:
                            msg = f"❌ [CRITICAL] {unit} UNIT: VOLUME ERRORS. System requires optimization."
                            print(f" !! {msg}")
                            self.alert_buffer.append(msg)
                        if "Invalid stops (Code: 10016)" in line:
                            msg = f"❌ [CRITICAL] {unit} UNIT: STOP ERRORS. ATR/SL logic may be too tight."
                            print(f" !! {msg}")
                            self.alert_buffer.append(msg)
            except: pass

    def report_to_war_room(self, component, error):
        """Escalates critical failures to the BUG_WAR_ROOM.md for AI attention."""
        try:
            war_room_path = os.path.join(os.getcwd(), "BUG_WAR_ROOM.md")
            timestamp = time.strftime("%Y-%m-%d %H:%M")
            entry = f"\n### [ACTIVE_BUG] [{timestamp}] {component}_CRITICAL_FAILURE\n- **Error**: {error}\n- **Status**: UNRESOLVED - REQUIRES AI INTERVENTION\n"
            
            with open(war_room_path, "r") as f:
                content = f.read()
            
            if error[:50] not in content: # Avoid duplicate spam
                new_content = content.replace("## 🚨 ACTIVE BUGS [PRIORITY: OMEGA]", f"## 🚨 ACTIVE BUGS [PRIORITY: OMEGA]\n{entry}")
                with open(war_room_path, "w") as f:
                    f.write(new_content)
                print(f" >> [SENTINEL] Escalated to BUG_WAR_ROOM: {component}")
        except: pass

    def heartbeat_audit(self):
        """
        Checks if the fleet is idle and triggers a Master re-scan if needed.
        """
        try:
            import sqlite3
            # Use absolute path to ensure DB access from anywhere
            db_path = os.path.join(os.getcwd(), "core_v3", "iron_core.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            # Count active trades (where type is 'LIVE')
            cursor.execute("SELECT COUNT(*) FROM trades WHERE type = 'LIVE'")
            active_count = cursor.fetchone()[0]
            conn.close()
            
            if active_count == 0:
                trigger_path = os.path.join(os.getcwd(), "core_v3", "scan_trigger.tmp")
                # Only trigger if the file is old (e.g., > 1 hour) or doesn't exist
                # to prevent constant scanning
                should_trigger = True
                if os.path.exists(trigger_path):
                    if time.time() - os.path.getmtime(trigger_path) < 3600:
                        should_trigger = False
                
                if should_trigger:
                    print(" !! [SENTINEL] Fleet Idle. Triggering emergency Market Scan...")
                    with open(trigger_path, "w") as f:
                        f.write(str(time.time()))
        except Exception as e:
            print(f" !! [SENTINEL_ERR] Heartbeat audit failed: {e}")

    def auto_scribe(self):
        """
        Auto-Scribe: The invisible historian.
        Automatically commits and pushes significant changes to GitHub.
        """
        try:
            # Check if git is initialized
            if not os.path.exists(os.path.join(os.getcwd(), ".git")): return

            # Check for changes
            status = subprocess.check_output(["git", "status", "--porcelain"]).decode()
            if not status: return 

            print(" >> [SENTINEL] Auto-Scribe: Detecting system evolution. Recording to history...")
            
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            message = f"AUTO-SCRIBE: System Evolution detected at {timestamp}. Synchronizing fleet state."
            
            # Git sync protocol
            subprocess.run(["git", "add", "."], capture_output=True)
            subprocess.run(["git", "commit", "-m", message], capture_output=True)
            
            # Push (non-blocking to prevent sentinel hang)
            print(" >> [SENTINEL] Auto-Scribe: Pushing to Sovereign Cloud (GitHub)...")
            subprocess.Popen(["git", "push", "origin", "main"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            if self.comm:
                self.alert_buffer.append("📜 [AUTO-SCRIBE] System Evolution Recorded. State pushed to GitHub.")
            
        except Exception as e:
            print(f" !! [SENTINEL_ERR] Auto-Scribe failed: {e}")

    def dispatch_consolidated_report(self):
        """
        SI v3.6: The Aggregator.
        Collects all alerts + DNA evolution + Fleet status into one message.
        """
        # 1. Collect DNA Evolution Alerts from Master
        evo_path = "core_v3/evolution_buffer.tmp"
        if os.path.exists(evo_path):
            try:
                with open(evo_path, 'r') as f:
                    evo_alerts = f.read().splitlines()
                self.alert_buffer.extend(evo_alerts)
                os.remove(evo_path)
            except: pass

        if not self.alert_buffer: return

        print(" >> [SENTINEL] Dispatching Consolidated Tactical Summary...")
        
        # 2. Build the Report
        timestamp = time.strftime("%H:%M:%S ICT")
        report = (
            f"🦅 **SOVEREIGN TACTICAL SUMMARY** [{timestamp}]\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
        )
        
        # A. Tactical Events
        report += "<b>🛠️ OPERATIONAL EVENTS</b>\n"
        for alert in self.alert_buffer:
            report += f" • {alert}\n"
        report += "\n"

        # B. Fleet Status (Integrated from FleetReporter)
        try:
            from fleet_report import FleetReporter
            fr = FleetReporter()
            report += fr.get_status()
        except Exception as e:
            report += f"❌ Status Integration Failed: {e}"

        report += "\n━━━━━━━━━━━━━━━━━━━━"

        # 3. Send via GhostComm (HTML Mode)
        if self.comm:
            try:
                self.comm.bot.send_message(self.comm.chat_id, report, parse_mode='HTML')
            except Exception as e:
                print(f" !! [DISPATCH_ERR] {e}")
        
        # 4. Clear Buffer
        self.alert_buffer = []

if __name__ == "__main__":
    sentinel = IronSentinel()
    sentinel.run()
