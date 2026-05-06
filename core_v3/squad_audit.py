import MetaTrader5 as mt5
import json
import os
import sys

# Ensure core_v3 is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_audit():
    print("="*60)
    print("SOVEREIGN SQUADRON AUDIT - Volume & Margin Validation")
    print("="*60)
    
    if not mt5.initialize():
        print(" !! [ERROR] MT5 Initialization Failed.")
        return

    # 1. Load Squadron
    squad_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "squadron.json")
    if not os.path.exists(squad_path):
        print(f" !! [ERROR] Squadron file not found at {squad_path}")
        return

    with open(squad_path, "r") as f:
        squadron = json.load(f)

    # 2. Get Account Info
    acc = mt5.account_info()
    if not acc:
        print(" !! [ERROR] Could not fetch account info.")
        return
    
    print(f" ACCOUNT: {acc.login} | BALANCE: ${acc.balance:,.2f} | EQUITY: ${acc.equity:,.2f}")
    print("-" * 60)
    print(f"{'SYMBOL':<10} | {'MIN_LOT':<8} | {'STEP':<8} | {'CONTRACT':<10} | {'MAR_REQ(1L)':<12}")
    print("-" * 60)

    all_symbols = set()
    for unit, symbols in squadron.items():
        for s in symbols: all_symbols.add(s)

    for symbol in sorted(list(all_symbols)):
        if "USDT" in symbol:
            print(f"{symbol:<10} | {'0.001':<8} | {'0.001':<8} | {'1.0':<10} | {'CRYPTO':<12}")
            continue

        info = mt5.symbol_info(symbol)
        if not info:
            print(f"{symbol:<10} | {'NOT FOUND':<45}")
            continue

        # Calculate Margin for 1 lot
        price = mt5.symbol_info_tick(symbol).ask if mt5.symbol_info_tick(symbol) else 0
        margin_req = 0
        if price > 0:
            # Simple margin estimate: (Price * ContractSize) / Leverage
            # In MT5, we can use order_calc_margin
            margin_req = mt5.order_calc_margin(mt5.ORDER_TYPE_BUY, symbol, 1.0, price)
        
        mar_str = f"${margin_req:,.2f}" if margin_req is not None else "N/A"
        
        print(f"{symbol:<10} | {info.volume_min:<8} | {info.volume_step:<8} | {info.trade_contract_size:<10} | {mar_str:<12}")

    print("-" * 60)
    mt5.shutdown()
    print("Audit Complete.")

if __name__ == "__main__":
    run_audit()
