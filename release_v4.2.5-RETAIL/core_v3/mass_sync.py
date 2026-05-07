import MetaTrader5 as mt5
import sqlite3
import time
import os

def mass_sync():
    print("--- INITIATING MASS SYNC (20,000+ DEALS) ---")
    if not mt5.initialize():
        print(" !! MT5 INIT FAILED")
        return

    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "iron_core.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Fetch History
    days = 30
    from_date = int(time.time()) - (86400 * days)
    to_date = int(time.time()) + 100
    
    history = mt5.history_deals_get(from_date, to_date)
    if not history:
        print(" !! NO HISTORY DEALS FOUND")
        mt5.shutdown()
        return

    # 2. Batch Processing
    deals_to_insert = []
    for deal in history:
        if deal.entry == 1: # ENTRY_OUT (Close)
            symbol = deal.symbol
            ticket = deal.position_id
            pnl = deal.profit + deal.commission + deal.swap
            volume = deal.volume
            price = deal.price
            side = "SELL" if deal.type == 0 else "BUY"
            comment = deal.comment
            
            unit_id = "UNKNOWN"
            if "STRIKE_A" in comment: unit_id = "ALPHA"
            elif "STRIKE_O" in comment: unit_id = "OMEGA"
            elif "STRIKE_G" in comment: unit_id = "GAMMA"
            
            deals_to_insert.append((ticket, unit_id, symbol, side, volume, price, 0, 0, pnl, 'LIVE', comment))

    # 3. Mass Transaction
    try:
        from forensics import IronForensics
        forensics = IronForensics(db_path=db_path)
        
        cursor.execute("BEGIN TRANSACTION")
        added_count = 0
        for deal in deals_to_insert:
            # Check if we already processed this ticket (to avoid double XP)
            cursor.execute("SELECT pnl FROM trades WHERE ticket = ?", (deal[0],))
            existing = cursor.fetchone()
            
            # Insert or Update
            cursor.execute('''
                INSERT INTO trades (ticket, unit_id, symbol, side, volume, price, sl, tp, pnl, type, comment)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(ticket) DO UPDATE SET
                    pnl = excluded.pnl,
                    comment = excluded.comment
            ''', deal)
            
            # XP LOGIC: If profit > 0 and (not exists or was 0), grant XP
            pnl = deal[8]
            unit_id = deal[1]
            if pnl > 0 and unit_id != "UNKNOWN":
                if not existing or (existing[0] == 0):
                    forensics.add_xp(unit_id, amount=1)
                    added_count += 1

        conn.commit()
        print(f" >> [SUCCESS] Mass-Synchronized {len(deals_to_insert)} trades. Granted XP for {added_count} new strikes.")
    except Exception as e:
        conn.rollback()
        print(f" !! [MASS_SYNC_ERR] {e}")
    finally:
        conn.close()
        mt5.shutdown()

if __name__ == "__main__":
    mass_sync()
