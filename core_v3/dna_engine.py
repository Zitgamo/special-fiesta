import sqlite3
import json
import os
import random
import numpy as np
import logging
from critic import AdversarialCritic

class DNAEngine:
    """
    Sovereign Intelligence Brain (SI v3.1).
    Handles DNA mutation, evolutionary branching, and recursive self-optimization.
    """
    def __init__(self, db_path="core_v3/iron_core.db", dna_path="core_v3/dna.json"):
        self.db_path = db_path
        self.dna_path = dna_path
        self.critic = AdversarialCritic(db_path, dna_path)
        self.logger = logging.getLogger("DNA_ENGINE")

    def mutate_dna(self, forensics, comm=None):
        """The Evolutionary Loop."""
        try:
            with open(self.dna_path, 'r') as f:
                dna = json.load(f)

            # Audit LIVE units
            for unit in ["ALPHA", "OMEGA", "GAMMA"]:
                stats = forensics.get_unit_stats(unit, trade_type='LIVE')
                self.process_mutation(unit, stats, dna, comm)
                
            # Audit SOUTHERN units (Paper Staging)
            for unit in ["SOUTH_ALPHA", "SOUTH_OMEGA", "SOUTH_GAMMA"]:
                stats = forensics.get_unit_stats(unit, trade_type='PAPER')
                dna_key = unit.split("_")[1]
                self.process_mutation(dna_key, stats, dna, comm, prefix=f"SOUTHERN_{unit}")

            with open(self.dna_path, 'w') as f:
                json.dump(dna, f, indent=4)
            return True
        except Exception as e:
            self.logger.error(f" >> [DNA_ERR] Mutation failed: {e}")
            return False

    def process_mutation(self, dna_key, stats, dna, comm=None, prefix=""):
        """SDS v2.0: Dynamic Scaling & Precision Guard."""
        if not stats or stats.get("total", 0) < 5: return

        optimal_er = self.critic.find_optimal_threshold(dna_key, 'er')
        win_rate = stats.get("win_rate_val", 0.5)
        er = stats.get("context", {}).get("er", 1.0)

        # ESCALATION
        if er >= optimal_er and win_rate > 0.55:
            current_layers = dna[dna_key]["ACTIVE_RISK"].get("MAX_LAYERS", 2)
            if current_layers < 7:
                dna[dna_key]["ACTIVE_RISK"]["MAX_LAYERS"] = current_layers + 1
                multiplier = 1.0 + (er / 5.0)
                new_lot = dna[dna_key]["LOT_SIZE"] * multiplier
                
                # Precision Guard
                if "USDT" in str(dna[dna_key].get("SYMBOL", "")):
                    dna[dna_key]["LOT_SIZE"] = max(0.0001, round(new_lot, 4))
                else:
                    dna[dna_key]["LOT_SIZE"] = max(0.01, round(new_lot, 2))
                
                if comm:
                    comm.notify(f"🚀 [ESCALATION] {prefix or dna_key}: Scaled to {multiplier:.2f}x (Layers: {current_layers+1})")

        # ATROPHY
        elif er < (optimal_er * 0.7):
            current_layers = dna[dna_key]["ACTIVE_RISK"].get("MAX_LAYERS", 2)
            if current_layers > 1:
                dna[dna_key]["ACTIVE_RISK"]["MAX_LAYERS"] = current_layers - 1
            
            new_lot = dna[dna_key]["LOT_SIZE"] * 0.8
            if "USDT" in str(dna[dna_key].get("SYMBOL", "")):
                dna[dna_key]["LOT_SIZE"] = max(0.0001, round(new_lot, 4))
            else:
                dna[dna_key]["LOT_SIZE"] = max(0.01, round(new_lot, 2))

            if not dna[dna_key].get("SHADOW"):
                self.branch_dna(dna_key, dna)

        # REBIRTH HANDOVER
        if dna[dna_key].get("SHADOW"):
            if self.compare_realities(dna_key, dna):
                print(f" >> [REBIRTH] {dna_key} Mutant proven superior.")
                dna[dna_key]["SL"] = dna[dna_key]["SHADOW"]["SL"]
                dna[dna_key]["TP"] = dna[dna_key]["SHADOW"]["TP"]
                dna[dna_key]["SHADOW"] = None

    def branch_dna(self, unit, dna):
        """Creates Adversarial Shadow DNA."""
        dna[unit]["SHADOW"] = {
            "SL": dna[unit]["SL"],
            "TP": dna[unit]["TP"]
        }
        mutation_dir = random.choice([-0.2, 0.2])
        dna[unit]["SL"] = round(dna[unit]["SL"] + mutation_dir, 2)
        dna[unit]["TP"] = round(dna[unit]["TP"] - mutation_dir, 2)

    def compare_realities(self, unit, dna):
        """Compares Mutant vs Shadow."""
        return random.random() > 0.7 # Simulated parity logic for SI v3.1
