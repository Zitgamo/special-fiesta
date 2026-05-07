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
            "SOUTHERN": "southern_paper_bridge.py"
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

        status_lines = []
        online_count = 0
        for name, identifier in self.fleet.items():
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

        report = f"📊 **FLEET READINESS**: {online_count}/{len(self.fleet)}\n"
        report += f"<code>{grid}</code>"
        return report

    def send_report(self):
        report = self.get_status()
        print(report)
        if self.comm:
            self.comm.notify(report)
            return True
        return False

if __name__ == "__main__":
    reporter = FleetReporter()
    reporter.send_report()
