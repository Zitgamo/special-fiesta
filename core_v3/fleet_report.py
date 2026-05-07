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
        report = "🛰️ **SOVEREIGN FLEET STATUS REPORT**\n"
        report += "==============================\n"
        
        procs = []
        for p in psutil.process_iter(['cmdline']):
            try:
                cmd = " ".join(p.info['cmdline']).lower() if p.info['cmdline'] else ""
                procs.append(cmd)
            except: continue

        online_count = 0
        for name, identifier in self.fleet.items():
            is_online = any(identifier in cmd for cmd in procs)
            status_icon = "✅" if is_online else "❌"
            if is_online: online_count += 1
            report += f"{status_icon} {name.ljust(12)}: {'ONLINE' if is_online else 'OFFLINE'}\n"

        report += "==============================\n"
        report += f"📊 Fleet Readiness: {online_count}/{len(self.fleet)}\n"
        report += f"⏰ Timestamp: {time.strftime('%H:%M:%S ICT')}"
        
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
