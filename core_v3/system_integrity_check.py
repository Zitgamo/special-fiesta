import os
import psutil
import json
import sys

def get_base_path():
    # Returns the absolute path to the IRON_COMMANDER directory
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def check_integrity():
    print("--- SOVEREIGN SYSTEM INTEGRITY AUDIT ---")
    is_passed, results = run_audit()
    
    for pillar, status in results.items():
        color = ">>" if "PASS" in status else "!!"
        print(f" {color} {pillar.ljust(25)}: {status}")
        
    print(f"\n--- AUDIT {'PASSED' if is_passed else 'FAILED'} ---")
    return is_passed

def run_audit():
    # Centralized Audit Logic
    results = {}
    base = get_base_path()
    core = os.path.join(base, "core_v3")
    
    # 1. PILLAR: PERSISTENCE
    sentinel_alive = any("sentinel.py" in " ".join(p.cmdline()).lower() for p in psutil.process_iter(['cmdline']) if p.info['cmdline'])
    results["PERSISTENCE (Sentinel)"] = "PASS" if sentinel_alive else "FAIL"

    # 2. PILLAR: DISCOVERY
    master_path = os.path.join(core, "master.py")
    if os.path.exists(master_path):
        with open(master_path, 'r') as f:
            content = f.read()
            if "self.perform_market_scan()" in content:
                results["DISCOVERY (Scanner)"] = "PASS"
            else:
                results["DISCOVERY (Scanner)"] = "FAIL"
    
    # 3. PILLAR: RISK
    engine_path = os.path.join(core, "engine.py")
    if os.path.exists(engine_path):
        with open(engine_path, 'r') as f:
            content = f.read()
            if "from vault_v2 import IronVault" in content:
                results["RISK (Vault V2)"] = "PASS"
            else:
                results["RISK (Vault V2)"] = "FAIL"

    # 4. PILLAR: EXECUTION
    bridge_path = os.path.join(core, "bridges.py")
    if os.path.exists(bridge_path):
        with open(bridge_path, 'r') as f:
            content = f.read()
            if "set_leverage" in content and "BINANCE_LEVERAGE" in content:
                results["EXECUTION (Leverage)"] = "PASS"
            else:
                results["EXECUTION (Leverage)"] = "FAIL"

    is_passed = all("PASS" in v for v in results.values())
    return is_passed, results

def check_integrity_silent():
    is_passed, results = run_audit()
    if is_passed:
        return True, "SYSTEM_COMPLIANT"
    else:
        # Return the first fail
        for k, v in results.items():
            if "FAIL" in v: return False, f"PROTOCOL_VIOLATION: {k}"
    return False, "UNKNOWN_ERROR"

if __name__ == "__main__":
    check_integrity()
