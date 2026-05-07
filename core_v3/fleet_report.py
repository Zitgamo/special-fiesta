import psutil
import os
import json
import time
import sys
from ghost_comm import GhostComm

# Ensure console supports tactical emojis
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

class FleetReporter:
    """
    Sovereign Status Aggregator.
    Performs a full fleet scan and sends a SINGLE Telegram report.
    """
    def __init__(self):
        self.fleet = {
            "MASTER": "master.py",
            "SENTINEL": "sentinel.py",
            "BRIDGE": "nexus_bridge.py",
            "GHOST_COMM": "ghost_comm.py",
            "ALPHA": "engine.py alpha",
            "OMEGA": "engine.py omega",
            "GAMMA": "engine.py gamma",
            "HANG_DA": "southern_paper_bridge.py"
        }
        try:
            self.comm = GhostComm()
        except:
            self.comm = None

    def get_status(self):
        procs = []
        for p in psutil.process_iter(['cmdline']):
            try:
                cmd = " ".join(p.info['cmdline']).lower() if p.info['cmdline'] else ""
                procs.append(cmd)
            except: continue

        # Load DNA for quarantine checks
        dna = {}
        try:
            with open("core_v3/dna.json", "r") as f:
                dna = json.load(f)
        except: pass

        status_lines = []
        online_count = 0
        active_fleet_count = 0
        quarantine_count = 0

        for name, identifier in self.fleet.items():
            # Check for Quarantine status
            if dna.get(name, {}).get("QUARANTINE"):
                quarantine_count += 1
                continue
            
            active_fleet_count += 1
            is_online = any(identifier in cmd for cmd in procs)
            status_icon = "🟢" if is_online else "🔴"
            if is_online: online_count += 1
            status_lines.append(f"{status_icon} {name.ljust(10)}")

        # Arrange in a grid for conciseness
        grid = ""
        for i in range(0, len(status_lines), 2):
            line = status_lines[i]
            if i + 1 < len(status_lines):
                line += " | " + status_lines[i+1]
            grid += line + "\n"

        report = f"📊 **FLEET READINESS**: {online_count}/{active_fleet_count}\n"
        if grid:
            report += f"<code>{grid}</code>"
        
        if quarantine_count > 0:
            report += f"\n<i>⚠️ {quarantine_count} units currently in Quarantine (Re-R&D)</i>"
        
        return report

    def load_state(self):
        state_path = "core_v3/report_state.json"
        if os.path.exists(state_path):
            with open(state_path, "r") as f:
                return json.load(f)
        
        # Initial State
        return {
            "last_report_time": 0,
            "interval_seconds": 3600, # Start at 1H
            "streak_start_time": time.time(),
            "streak_start_equity": 0,
            "total_cycles": 0,
            "reset_occurred": False
        }

    def save_state(self, state):
        with open("core_v3/report_state.json", "w") as f:
            json.dump(state, f, indent=4)

    def send_report(self, forced=False):
        state = self.load_state()
        current_time = time.time()
        
        # 1. CHECK IF REPORT IS DUE
        if not forced and (current_time - state['last_report_time']) < state['interval_seconds']:
            return False

        # 2. GENERATE REPORT
        status_report = self.get_status()
        
        # 3. CALCULATE STREAK METRICS
        uptime_hours = (current_time - state['streak_start_time']) / 3600
        
        # Get Current Equity for Profit calculation
        try:
            import sqlite3
            db_path = "core_v3/iron_core.db"
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT equity FROM equity_history ORDER BY id DESC LIMIT 1")
            res = cursor.fetchone()
            current_equity = res[0] if res else 0
            conn.close()
        except: current_equity = 0
        
        if state['streak_start_equity'] == 0:
            state['streak_start_equity'] = current_equity
            
        profit = current_equity - state['streak_start_equity']
        
        # Estimation of decision cycles (Assuming 30s loop)
        cycles = int((current_time - state['streak_start_time']) / 30)

        # 4. CONSTRUCT TACTICAL CARD
        title = "🛡️ **SOVEREIGN STABILITY STREAK** 🛡️"
        if state.get("reset_occurred"):
            title = "⚠️ **STREAK RESET: INCIDENT DETECTED** ⚠️"
            state['reset_occurred'] = False
            
        final_report = (
            f"{title}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🏆 **STABILITY**: `{uptime_hours:.1f} HOURS`\n"
            f"🔄 **CYCLES**: `{cycles:,} GREEN`\n"
            f"💰 **PROFIT**: `${profit:+.2f}`\n\n"
            f"💎 **STATUS**: `INTERVAL x2 ({state['interval_seconds']/3600:.0f}H)`\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"{status_report}"
        )

        # 5. EXECUTE BROADCAST
        if self.comm:
            self.comm.notify(final_report)
            
        # 6. UPDATE STATE (Exponential Silence)
        state['last_report_time'] = current_time
        state['interval_seconds'] *= 2 # Double the silence
        self.save_state(state)
        
        print(f" >> [SSS] Report sent. Next in {state['interval_seconds']/3600:.0f} hours.")
        return True

if __name__ == "__main__":
    reporter = FleetReporter()
    # Force first report to initialize
    reporter.send_report(forced=True)
