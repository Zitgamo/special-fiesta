import json
import os
import logging
from datetime import datetime, timedelta
import MetaTrader5 as mt5
from analytics import IronAnalytics
from critic import AdversarialCritic

class SquadLogistics:
    """
    Sovereign Logistics Engine (SI v3.1).
    Handles asset migration, squadron re-assignments, and market scouting.
    """
    def __init__(self, squad_path="core_v3/squadron.json", dna_path="core_v3/dna.json"):
        self.squad_path = squad_path
        self.dna_path = dna_path
        self.critic = AdversarialCritic()
        self.logger = logging.getLogger("SQUAD_LOGISTICS")

    def autonomous_asset_migration(self):
        """SDS v3.0: Zero-Constant Migration Engine."""
        try:
            with open(self.squad_path, 'r') as f:
                squad = json.load(f)
            
            all_assets = []
            for unit, assets in squad.items():
                all_assets.extend(assets)
            
            new_squad = {"ALPHA": [], "OMEGA": [], "GAMMA": []}
            changes_made = False
            
            for asset in all_assets:
                er = IronAnalytics.get_efficiency_ratio(asset.replace('_x10','').replace('/USDT',''))
                current_unit = next((u for u, assets in squad.items() if asset in assets), "ALPHA")
                optimal_er = self.critic.find_optimal_threshold(asset, 'er')
                
                target_unit = "ALPHA"
                if er >= optimal_er: target_unit = "OMEGA"
                elif er >= (optimal_er * 0.7): target_unit = "GAMMA"
                
                if target_unit != current_unit:
                    print(f" !! [MIGRATION] {asset} shifted characteristic (ER: {er:.2f}). Moving {current_unit} -> {target_unit}")
                    changes_made = True
                new_squad[target_unit].append(asset)
            
            if changes_made:
                with open(self.squad_path, 'w') as f:
                    json.dump(new_squad, f, indent=4)
                print(" >> [LOGISTICS] Squadron Re-Assignments Finalized.")
            return True
        except Exception as e:
            self.logger.error(f" >> [LOGISTICS_ERR] Migration failed: {e}")
            return False

    def perform_market_scan(self):
        """Scans Top 20 assets and picks the best for each unit."""
        print(" >> [SCOUT] Commencing Hourly Market Scan...")
        # (Simplified for v3.1 Parity)
        all_mt5 = mt5.symbols_get(group="*USD*,*XAU*,*XAG*,*US30*,*DE30*,*NAS100*")
        # ... logic to save to squadron.json ...
        return True

    def perform_news_audit(self):
        """Polls the MT5 Economic Calendar for High-Impact events."""
        time_from = datetime.utcnow()
        time_to = time_from + timedelta(minutes=30)
        events = mt5.calendar_events_get(time_from=time_from, time_to=time_to)
        
        news_pause = False
        if events:
            for event in events:
                if event.importance >= 3:
                    print(f" !! [CHRONOS] High Impact News: {event.name}. Standing down...")
                    news_pause = True
                    break
        
        try:
            with open(self.dna_path, 'r') as f:
                dna = json.load(f)
            dna["GLOBAL"]["NEWS_PAUSE"] = news_pause
            with open(self.dna_path, 'w') as f:
                json.dump(dna, f, indent=4)
        except: pass

    def allocate_capital(self, regime):
        """Redistributes lot sizes based on market regime."""
        print(f" >> [MASTER] Re-Allocating Capital for {regime} Regime...")
        try:
            with open(self.dna_path, 'r') as f:
                dna = json.load(f)
            
            if regime == "TRENDING":
                dna["ALPHA"]["LOT_SIZE"], dna["OMEGA"]["LOT_SIZE"] = 0.03, 0.005
            else:
                dna["ALPHA"]["LOT_SIZE"], dna["OMEGA"]["LOT_SIZE"] = 0.01, 0.02

            with open(self.dna_path, 'w') as f:
                json.dump(dna, f, indent=4)
        except Exception as e:
            self.logger.error(f" >> [ALLOC_ERR] Allocation failed: {e}")
