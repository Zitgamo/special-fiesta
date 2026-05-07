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
    Handles distinct report types:
    1. SSS Heartbeat (Exponential Silence Protocol)
    2. Council Verdicts (Event-Driven Tactical Cards)
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

    def get_running_processes(self):
        procs = []
        for p in psutil.process_iter(['cmdline']):
            try:
                cmd = " ".join(p.info['cmdline']).lower() if p.info['cmdline'] else ""
                procs.append(cmd)
            except: continue
        return procs

    def get_status(self):
        procs = self.get_running_processes()
        status_lines = []
        online_count = 0
        active_fleet_count = 0
        
        # Load DNA to check for Quarantine
        dna = {}
        try:
            with open("03_DATA/iron_dna.json", "r") as f:
                dna = json.load(f)
        except: pass

        for name, identifier in self.fleet.items():
            if dna.get(name, {}).get("QUARANTINE"):
                continue
            
            active_fleet_count += 1
            is_online = any(identifier in cmd for cmd in procs)
            status_char = "√" if is_online else "X"
            if is_online: online_count += 1
            status_lines.append(f"{status_char} {name.ljust(10)}")

        # Arrange in a symmetric grid
        grid = ""
        for i in range(0, len(status_lines), 2):
            line = status_lines[i]
            if i + 1 < len(status_lines):
                line += " | " + status_lines[i+1]
            grid += line + "\n"

        report = f"📊 FLEET READINESS: {online_count}/{active_fleet_count}\n"
        if grid:
            report += f"<code>{grid.strip()}</code>"
        
        return report

    def load_state(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        state_path = os.path.join(base_dir, "report_state.json")
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
        base_dir = os.path.dirname(os.path.abspath(__file__))
        state_path = os.path.join(base_dir, "report_state.json")
        with open(state_path, "w") as f:
            json.dump(state, f, indent=4)

    def send_report(self, forced=False):
        """
        [SSS PROTOCOL]
        Sends the standard Sovereign Heartbeat.
        Uses exponential silence doubling (Capped at 8H).
        """
        state = self.load_state()
        current_time = time.time()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(os.path.dirname(base_dir), "03_DATA")
        
        # 1. CHECK IF REPORT IS DUE
        if not forced and (current_time - state['last_report_time']) < state['interval_seconds']:
            return False

        # 2. FETCH BRIDGE METRICS
        bridge_meta = {}
        for _ in range(5):
            try:
                with open(os.path.join(data_dir, "vn30_active_pos.json"), "r") as f:
                    bridge_data = json.load(f)
                    bridge_meta = bridge_data.get("meta", {})
                    break
            except: time.sleep(0.1)

        # 3. CALCULATE STREAK & PROFIT
        uptime_str = bridge_meta.get("uptime", "0:00:00")
        VND_PER_PT = 100000
        peak_pts = bridge_meta.get("peak_equity", 0) / VND_PER_PT
        curr_dd_pts = bridge_meta.get("current_dd_vnd", 0) / VND_PER_PT
        max_dd_pts = bridge_meta.get("max_dd_vnd", 0) / VND_PER_PT
        current_equity_pts = peak_pts - curr_dd_pts
        
        if state['streak_start_equity'] == 0:
            state['streak_start_equity'] = current_equity_pts
            
        profit = current_equity_pts - state['streak_start_equity']
        dd_pct = (curr_dd_pts / peak_pts) * 100 if peak_pts > 0 else 0
        max_dd_pct = (max_dd_pts / peak_pts) * 100 if peak_pts > 0 else 0
        
        ts = bridge_meta.get("trade_stats", {"total": 0, "wins": 0, "losses": 0, "last_t": "Never"})
        last_t_str = "Never"
        if ts.get("last_t") and ts["last_t"] != "Never":
            try:
                from datetime import datetime
                lt_dt = datetime.strptime(ts["last_t"], '%Y-%m-%d %H:%M:%S')
                mins_ago = int((datetime.now() - lt_dt).total_seconds() / 60)
                last_t_str = f"{mins_ago} mins ago"
            except: last_t_str = "Unknown"
            
        cycles = int((current_time - state['streak_start_time']) / 30)
        interval_hours = state['interval_seconds']/3600
        status_report = self.get_status()

        # 4. CONSTRUCT HEARTBEAT (SSS v12.0)
        final_report = (
            f"🛡️ SOVEREIGN HEARTBEAT — T+{uptime_str}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"STABILITY  : {uptime_str} | {cycles} GREEN cycles\n"
            f"EQUITY     : {current_equity_pts:,.2f} pts | Peak: {peak_pts:,.2f} pts\n"
            f"DRAWDOWN   : Current -{curr_dd_pts:,.2f} pts (-{dd_pct:.1f}%) | Max -{max_dd_pts:,.2f} pts (-{max_dd_pct:.1f}%)\n"
            f"TRADES     : {ts['total']} total | W/L: {ts['wins']}/{ts['losses']} | Last: {last_t_str}\n"
            f"NEXT PULSE : T+{interval_hours:.1f}h (Interval x2 if stable)\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"{status_report}"
        )

        if self.comm:
            self.comm.notify(final_report)
            
        # 5. UPDATE SSS STATE
        state['last_report_time'] = current_time
        state['interval_seconds'] = min(state['interval_seconds'] * 2, 8 * 3600)
        self.save_state(state)
        print(f" >> [SSS] Heartbeat dispatched. Next in {state['interval_seconds']/3600:.1f} hours.")
        return True

    def send_council_report(self, is_breach=False):
        """
        [EVENT-DRIVEN]
        Sends a dedicated Tactical Card for Council Verdicts or Breaches.
        Does NOT affect SSS timing.
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(os.path.dirname(base_dir), "03_DATA")
        
        # 1. FETCH COUNCIL INFO
        council_info = "NEUTRAL"
        min_b, max_b = 0, 0
        advice = "No advice found."
        try:
            with open(os.path.join(data_dir, "council_verdict.json"), "r") as f:
                v = json.load(f)
                council_info = v.get('bias') or v.get('bias_verdict', 'NEUTRAL')
                min_b = v.get('min_boundary', 0)
                max_b = v.get('max_boundary', 0)
                advice = v.get('council_advice', advice)
        except: pass

        # 2. FETCH LIVE BREACH STATUS
        breach_status = "SAFE ✅"
        try:
            with open(os.path.join(data_dir, "vn30_active_pos.json"), "r") as f:
                meta = json.load(f).get("meta", {})
                breach_status = meta.get("breach_status", "SAFE ✅")
        except: pass

        # 3. CONSTRUCT TACTICAL CARD
        header = "🏛️ HIGH COUNCIL VERDICT — TACTICAL UPDATE"
        if is_breach:
            header = "🚨 PROPHECY BREACH — IMMEDIATE ACTION"
        
        report = (
            f"{header}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"COUNCIL BIAS: [{council_info}]\n"
            f"PROPHETIC BW: [{min_b}] ←——— {breach_status} ———→ [{max_b}]\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"ADVICE:\n<i>\"{advice}\"</i>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<i>Event-driven report. SSS Pulse unaffected.</i>"
        )

        if self.comm:
            try:
                self.comm.bot.send_message(self.comm.chat_id, report, parse_mode='HTML')
                print(f" >> [COUNCIL] Tactical report dispatched.")
                return True
            except:
                self.comm.notify(report)
                return True
        return False

if __name__ == "__main__":
    reporter = FleetReporter()
    # Force first report to initialize
    reporter.send_report(forced=True)
