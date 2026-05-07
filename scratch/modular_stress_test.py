import sys
import os
import json
import time
import datetime

# Inject Path
sys.path.append(os.path.join(os.getcwd(), 'core_v3'))

from dna_engine import DNAEngine
from squad_logistics import SquadLogistics
from forensics import IronForensics

def test_modular_integrity():
    print("--- SOVEREIGN TACTICAL STRESS TEST (TST) ---")
    
    # 1. BRAIN AUDIT
    print("\n[TEST 1] Auditing DNA Engine Mutation...")
    try:
        engine = DNAEngine()
        forensics = IronForensics()
        # Mocking a mutation trigger
        res = engine.mutate_dna(forensics)
        if res:
            with open("core_v3/dna.json", 'r') as f:
                dna = json.load(f)
            print(f" >> SUCCESS: DNA Engine mutated core. ALPHA SL: {dna['ALPHA']['SL']}")
        else:
            print(" !! FAIL: DNA Engine failed mutation cycle.")
    except Exception as e:
        print(f" !! ERR: DNA Engine Exception: {e}")

    # 2. LOGISTICS AUDIT
    print("\n[TEST 2] Auditing Squad Logistics Migration...")
    try:
        logistics = SquadLogistics()
        res = logistics.autonomous_asset_migration()
        if res:
            with open("core_v3/squadron.json", 'r') as f:
                squad = json.load(f)
            print(f" >> SUCCESS: Logistics Engine synchronized squadrons: {list(squad.keys())}")
        else:
            print(" !! FAIL: Logistics Engine failed migration.")
    except Exception as e:
        print(f" !! ERR: Logistics Engine Exception: {e}")

    # 3. MAINTENANCE AUDIT (Janitor Mock)
    print("\n[TEST 3] Auditing Sentinel-Janitor Handshake...")
    try:
        report_path = "logs/janitor_report.json"
        # Mock an overdue cleanup (2 days ago)
        old_report = {
            "timestamp": (datetime.datetime.now() - datetime.timedelta(days=2)).isoformat(),
            "cleaned_items": 0
        }
        with open(report_path, 'w') as f:
            json.dump(old_report, f, indent=4)
        
        print(" >> Mocking overdue report. Please check logs for 'Summoning the Janitor' signal.")
        # We won't run the full sentinel loop, but we will test the logic
        from sentinel import IronSentinel
        sentinel = IronSentinel()
        sentinel.autonomous_cleanup()
    except Exception as e:
        print(f" !! ERR: Maintenance Audit Exception: {e}")

if __name__ == "__main__":
    test_modular_integrity()
