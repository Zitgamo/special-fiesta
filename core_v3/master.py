import subprocess
import time
import os
import signal
import sys
import json
import MetaTrader5 as mt5
import threading
import sys
import logging

# Sovereign Modular Architecture (SMA v1.0)
# Injecting local path for internal module discovery
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dna_engine import DNAEngine
from squad_logistics import SquadLogistics
from analytics import IronAnalytics
from forensics import IronForensics
from critic import AdversarialCritic
from vault_v2 import IronVault

class SovereignMaster:
    """
    Sovereign Orchestrator (SMA v1.0 Compliant).
    Responsibility: Loop management, Sentinel handshake, and Service delegation.
    """
    def __init__(self):
        self.is_running = True
        self.logger = logging.getLogger("MASTER_ORCHESTRATOR")
        
        # Initialize Infrastructure
        from bridges import IronBridges
        secrets_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "secrets.json")
        self.bridges = IronBridges(secrets_path)
        
        # Initialize Sovereign Services
        self.dna_engine = DNAEngine()
        self.logistics = SquadLogistics()
        self.forensics = IronForensics()
        self.critic = AdversarialCritic()
        self.vault = IronVault(bridges=self.bridges)

    def start_units(self):
        """Sentinel now handles unit launches. Maintained for legacy bridge."""
        print("--- SOVEREIGN MASTER v4.0: ORCHESTRATION MODE ---")

    def monitor(self):
        """The Heartbeat Loop."""
        print("--- MASTER COMMAND ACTIVE (MODULAR) ---")
        try:
            loop_count = 0
            if not mt5.initialize():
                print(" !! [MASTER] MT5 Neural Handshake Failed. Retrying...")

            while self.is_running:
                try:
                    if not mt5.initialize():
                        time.sleep(5); continue

                    # 1. Logistics: Market Discovery & News Audit
                    trigger_path = "core_v3/scan_trigger.tmp"
                    if loop_count % 60 == 0 or os.path.exists(trigger_path):
                        self.logistics.perform_market_scan()
                        self.logistics.perform_news_audit()
                        if os.path.exists(trigger_path):
                            os.remove(trigger_path)
                    
                    # 2. Intelligence: DNA Evolution (Every 10 mins)
                    loop_count += 1
                    if loop_count % 20 == 0:
                        print(" >> [MASTER] Triggering Evolutionary DNA Mutation...")
                        self.dna_engine.mutate_dna(self.forensics)
                        self.critic.audit_performance()
                        self.logistics.autonomous_asset_migration()

                    # 3. Security: Active Risk Governor
                    self.vault.active_risk_governor(self.bridges)
                    
                    # 4. Forensics: Database Sync (Every 1 hour)
                    if loop_count % 120 == 0:
                        self.forensics.reconcile_trades(self.bridges)
                        loop_count = 0 
                    
                    time.sleep(30)
                except Exception as e:
                    print(f" !! [SHIELD_RECOVERY] Heartbeat Anomaly: {e}")
                    time.sleep(10)
        except KeyboardInterrupt:
            self.neutralize()

    def neutralize(self):
        print("--- ACCOUNT SECURED ---")
        self.is_running = False

if __name__ == "__main__":
    master = SovereignMaster()
    master.monitor()
