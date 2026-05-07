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

    def send_report(self, forced=False, is_breach=False):
        state = self.load_state()
        current_time = time.time()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(os.path.dirname(base_dir), "03_DATA")
        
        # 1. CHECK IF REPORT IS DUE
        if not forced and (current_time - state['last_report_time']) < state['interval_seconds']:
            return False

        # 2. FETCH BRIDGE METRICS (Deterministic Retry)
        bridge_meta = {}
        for _ in range(5): # Retry loop instead of sleep
            try:
                with open(os.path.join(data_dir, "vn30_active_pos.json"), "r") as f:
                    bridge_data = json.load(f)
                    bridge_meta = bridge_data.get("meta", {})
                    break
            except: time.sleep(0.1)

        # 3. CALCULATE STREAK & PROFIT
        uptime_str = bridge_meta.get("uptime", "0:00:00")
        
        # Equity Calc (Unified to use Bridge Meta for consistency in PTS)
        VND_PER_PT = 100000
        current_equity_pts = bridge_meta.get("peak_equity", 0) / VND_PER_PT # default to peak if current not found
        # Actually bridge meta doesn't have current_equity, but we can calculate from peak - curr_dd
        peak_pts = bridge_meta.get("peak_equity", 0) / VND_PER_PT
        curr_dd_pts = bridge_meta.get("current_dd_vnd", 0) / VND_PER_PT
        max_dd_pts = bridge_meta.get("max_dd_vnd", 0) / VND_PER_PT
        
        current_equity_pts = peak_pts - curr_dd_pts
        
        if state['streak_start_equity'] == 0:
            state['streak_start_equity'] = current_equity_pts
            self.save_state(state)
            
        profit = current_equity_pts - state['streak_start_equity']
        
        dd_pct = (curr_dd_pts / peak_pts) * 100 if peak_pts > 0 else 0
        max_dd_pct = (max_dd_pts / peak_pts) * 100 if peak_pts > 0 else 0
        
        # Trade Stats
        ts = bridge_meta.get("trade_stats", {"total": 0, "wins": 0, "losses": 0, "last_t": "Never"})
        last_t = ts.get("last_t", "Never")
        if last_t != "Never" and last_t:
            try:
                lt_dt = datetime.strptime(last_t, '%Y-%m-%d %H:%M:%S')
                mins_ago = int((datetime.now() - lt_dt).total_seconds() / 60)
                last_t_str = f"{mins_ago} mins ago"
            except: last_t_str = "Unknown"
        else:
            last_t_str = "Never"
            
        # Estimation of decision cycles (Assuming 30s loop)
        cycles = int((current_time - state['streak_start_time']) / 30)

        # 4. FETCH COUNCIL PROPHECY
        council_info = "NEUTRAL"
        min_b, max_b = 0, 0
        try:
            with open(os.path.join(data_dir, "council_verdict.json"), "r") as f:
                v = json.load(f)
                council_info = v.get('bias') or v.get('bias_verdict', 'NEUTRAL')
                min_b = v.get('min_boundary', 0)
                max_b = v.get('max_boundary', 0)
        except: pass

        # 5. CONSTRUCT RECOMMENDED FORMAT (v11.1)
        status_report = self.get_status()
        
        header = f"🛡️ SOVEREIGN HEARTBEAT — T+{uptime_str}"
        if is_breach:
            header = "🚨 PROPHECY BREACH — IMMEDIATE ACTION REQUIRED"
        
        breach_status = bridge_meta.get("breach_status", "SAFE ✅")
        live_price_str = "LIVE" # Could be enhanced to show actual price if passed
        if "⚠️ BREACH" in breach_status:
            try:
                live_price_str = breach_status.split(" ")[2] # Extract price from string
            except: pass
        
        interval_hours = state['interval_seconds']/3600
        
        final_report = (
            f"{header}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"STABILITY  : {uptime_str} continuous | {cycles} GREEN cycles\n"
            f"EQUITY     : ${current_equity_pts:,.2f} | Peak: ${peak_pts:,.2f}\n"
            f"DRAWDOWN   : Current -${curr_dd_pts:,.2f} (-{dd_pct:.1f}%) | Max -${max_dd_pts:,.2f} (-{max_dd_pct:.1f}%)\n"
            f"TRADES     : {ts['total']} total | W/L ratio: {ts['wins']}/{ts['losses']} | Last: {last_t_str}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"COUNCIL    : BIAS [{council_info}]\n"
            f"BOUNDARY   : [{min_b}] ←——— {breach_status} ———→ [{max_b}]\n"
            f"NEXT REPORT: T+{interval_hours:.1f}h (interval x2 if stable)\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"{status_report}"
        )

        # 6. EXECUTE BROADCAST
        if self.comm:
            self.comm.notify(final_report)
            
        # 7. UPDATE STATE (Exponential Silence - CAP AT 8H)
        state['last_report_time'] = current_time
        if not is_breach: # Only double if it was a normal report
            state['interval_seconds'] = min(state['interval_seconds'] * 2, 8 * 3600)
        
        self.save_state(state)
        return True
    
        print(f" >> [SSS] Report sent. Next in {state['interval_seconds']/3600:.0f} hours.")
        return True

if __name__ == "__main__":
    reporter = FleetReporter()
    # Force first report to initialize
    reporter.send_report(forced=True)
