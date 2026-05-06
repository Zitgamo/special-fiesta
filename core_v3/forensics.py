import sqlite3
import time
import os
try:
    from paths import DB_PATH
except ImportError:
    DB_PATH = "core_v3/iron_core.db"

class IronForensics:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._initialize_db()

    def _execute_with_retry(self, query, params=(), is_commit=False):
        for attempt in range(5):
            try:
                conn = sqlite3.connect(self.db_path, timeout=10)
                cursor = conn.cursor()
                cursor.execute(query, params)
                if is_commit: conn.commit()
                res = cursor.fetchall()
                conn.close()
                return res
            except sqlite3.OperationalError as e:
                if "locked" in str(e).lower():
                    time.sleep(0.5)
                    continue
                raise e
        return []

    def _initialize_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Enable WAL mode for concurrency
        cursor.execute("PRAGMA journal_mode=WAL;")
        
        # 1. Trade History (Hardened with TICKET)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket INTEGER UNIQUE,
                unit_id TEXT,
                symbol TEXT,
                side TEXT,
                volume REAL,
                price REAL,
                sl REAL,
                tp REAL,
                sl_mult REAL,
                tp_mult REAL,
                er_at_entry REAL,
                exit_price REAL,
                exit_time DATETIME,
                pnl REAL DEFAULT 0,
                type TEXT DEFAULT 'LIVE',
                comment TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 2. Equity History (Snapshotting)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS equity_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                balance REAL,
                equity REAL,
                drawdown REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 3. Unit Veterancy (XP & Rank)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS unit_veterancy (
                unit_id TEXT PRIMARY KEY,
                xp INTEGER DEFAULT 0,
                rank INTEGER DEFAULT 0,
                last_rank_up DATETIME
            )
        ''')
        
        # 4. Empirical Learning (The Brain)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS empirical_learning (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                unit_id TEXT,
                symbol TEXT,
                side TEXT,
                sl_mult REAL,
                tp_mult REAL,
                er_at_entry REAL,
                volatility_atr REAL,
                spread_ratio REAL,
                session TEXT,
                outcome_pnl REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Initialize default units if missing
        for unit in ["ALPHA", "OMEGA", "GAMMA"]:
            cursor.execute("INSERT OR IGNORE INTO unit_veterancy (unit_id) VALUES (?)", (unit,))

        # Hardening: Ensure all columns exist
        try: cursor.execute("ALTER TABLE trades ADD COLUMN ticket INTEGER UNIQUE")
        except: pass
        try: cursor.execute("ALTER TABLE trades ADD COLUMN exit_price REAL")
        except: pass
        try: cursor.execute("ALTER TABLE trades ADD COLUMN exit_time DATETIME")
        except: pass
        try: cursor.execute("ALTER TABLE trades ADD COLUMN pnl REAL DEFAULT 0")
        except: pass
        try: cursor.execute("ALTER TABLE trades ADD COLUMN comment TEXT")
        except: pass
        try: cursor.execute("ALTER TABLE trades ADD COLUMN sl_mult REAL")
        except: pass
        try: cursor.execute("ALTER TABLE trades ADD COLUMN tp_mult REAL")
        except: pass
        try: cursor.execute("ALTER TABLE trades ADD COLUMN er_at_entry REAL")
        except: pass
        try: cursor.execute("ALTER TABLE empirical_learning ADD COLUMN volatility_atr REAL")
        except: pass
        try: cursor.execute("ALTER TABLE empirical_learning ADD COLUMN spread_ratio REAL")
        except: pass
        try: cursor.execute("ALTER TABLE empirical_learning ADD COLUMN session TEXT")
        except: pass

        conn.commit()
        conn.close()

    def get_unit_stats(self, unit_id, trade_type='LIVE'):
        try:
            # Check last 10 trades for this unit
            trades = self._execute_with_retry(
                "SELECT pnl FROM trades WHERE unit_id = ? AND type = ? ORDER BY id DESC LIMIT 10",
                (unit_id, trade_type)
            )
            if not trades: return {"win_rate": 0.5, "total": 0}
            
            wins = sum(1 for t in trades if t[0] and t[0] > 0)
            return {
                "win_rate": wins / len(trades),
                "total": len(trades)
            }
        except: return {"win_rate": 0.5, "total": 0}

    def get_unit_rank(self, unit_id):
        try:
            res = self._execute_with_retry(
                "SELECT rank, xp FROM unit_veterancy WHERE unit_id = ?",
                (unit_id,)
            )
            if res:
                return {"rank": res[0][0], "xp": res[0][1]}
            return {"rank": 0, "xp": 0}
        except: return {"rank": 0, "xp": 0}

    def add_xp(self, unit_id, amount=1):
        try:
            # 1. Update XP
            self._execute_with_retry(
                "UPDATE unit_veterancy SET xp = xp + ? WHERE unit_id = ?",
                (amount, unit_id),
                is_commit=True
            )
            
            # 2. Check for Rank Up
            res = self._execute_with_retry(
                "SELECT xp, rank FROM unit_veterancy WHERE unit_id = ?",
                (unit_id,)
            )
            if res:
                xp, rank = res[0]
                new_rank = xp // 10
                if new_rank > rank:
                    self._execute_with_retry(
                        "UPDATE unit_veterancy SET rank = ?, last_rank_up = CURRENT_TIMESTAMP WHERE unit_id = ?",
                        (new_rank, unit_id),
                        is_commit=True
                    )
                    print(f" !! [LEVEL_UP] {unit_id} promoted to Rank {new_rank}!")
        except Exception as e:
            print(f" !! [FORENSICS_ERR] XP update failed: {e}")

    def record_learning(self, unit_id, symbol, side, sl_mult, tp_mult, er, pnl, atr=0, spread=0, session='N/A'):
        try:
            self._execute_with_retry(
                '''INSERT INTO empirical_learning (unit_id, symbol, side, sl_mult, tp_mult, er_at_entry, volatility_atr, spread_ratio, session, outcome_pnl, timestamp)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now', 'localtime'))''',
                (unit_id, symbol, side, sl_mult, tp_mult, er, atr, spread, session, pnl),
                is_commit=True
            )
        except Exception as e:
            print(f" !! [LEARNING_ERR] Failed to record experience: {e}")

    def get_optimal_hint(self, symbol, current_er, current_atr=0):
        """
        Retrieves the best sl/tp multipliers from history for a similar environment.
        """
        try:
            # Context-Aware query: Matches ER (+/- 0.1) and Session (if possible)
            res = self._execute_with_retry(
                '''SELECT sl_mult, tp_mult, AVG(outcome_pnl) as avg_pnl 
                   FROM empirical_learning 
                   WHERE symbol = ? AND er_at_entry BETWEEN ? AND ? 
                   GROUP BY sl_mult, tp_mult 
                   HAVING avg_pnl > 0 
                   ORDER BY avg_pnl DESC LIMIT 1''',
                (symbol, current_er - 0.1, current_er + 0.1)
            )
            if res:
                return res[0][0], res[0][1] # sl_mult, tp_mult
            return None
        except: return None

    def log_trade(self, unit_id, symbol, side, volume, price, sl, tp, pnl=0, status='LIVE', ticket=None, comment=None, sl_mult=None, tp_mult=None, er=None):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if ticket:
                cursor.execute('''
                    INSERT INTO trades (ticket, unit_id, symbol, side, volume, price, sl, tp, sl_mult, tp_mult, er_at_entry, pnl, type, comment, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now', 'localtime'))
                    ON CONFLICT(ticket) DO UPDATE SET
                        pnl = excluded.pnl,
                        type = excluded.type,
                        comment = excluded.comment,
                        exit_price = CASE WHEN excluded.type = 'CLOSED' THEN excluded.price ELSE exit_price END,
                        exit_time = CASE WHEN excluded.type = 'CLOSED' THEN datetime('now', 'localtime') ELSE exit_time END
                ''', (ticket, unit_id, symbol, side, volume, price, sl, tp, sl_mult, tp_mult, er, pnl, status, comment))
            else:
                # No ticket yet (PENDING)
                cursor.execute('''
                    INSERT INTO trades (unit_id, symbol, side, volume, price, sl, tp, sl_mult, tp_mult, er_at_entry, pnl, type, comment, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now', 'localtime'))
                ''', (unit_id, symbol, side, volume, price, sl, tp, sl_mult, tp_mult, er, pnl, status, comment))
                
            conn.commit()
            conn.close()
            
            # --- AUTO-LEARN: If trade is being logged as CLOSED/FAILED, record it to learning table ---
            if status in ['CLOSED', 'FAILED', 'PAPER'] and pnl != 0:
                # We extract context if available in the comment or params
                self.record_learning(unit_id, symbol, side, sl_mult, tp_mult, er, pnl)
        except Exception as e:
            print(f" !! [FORENSICS_ERR] {e}")

    def log_snapshot(self, balance, equity, drawdown):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO equity_history (balance, equity, drawdown, timestamp)
                VALUES (?, ?, ?, datetime('now', 'localtime'))
            ''', (balance, equity, drawdown))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f" !! [FORENSICS_ERR] {e}")

    def reconcile_trades(self, bridges=None):
        """
        SAFE RECONCILER (v3.0):
        Syncs MT5 history with the local DB while excluding 'LLM Mistakes'.
        """
        import MetaTrader5 as mt5
        from datetime import datetime, timedelta
        
        if not mt5.initialize(): return 0
        
        start = datetime.now() - timedelta(days=7)
        deals = mt5.history_deals_get(start, datetime.now())
        if not deals: return 0
        
        added_count = 0
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for d in deals:
            if d.profit == 0: continue # Skip non-pnl events
            
            # --- THE USER FORGIVENESS FILTER ---
            # Exclude the 'LLM Mistake' trades: Anything massive (>0.1 lots) or huge loss (<-200)
            if d.volume > 0.1 or d.profit < -200:
                print(f" >> [FORGIVEN] Skipping anomalous trade: {d.symbol} {d.volume} lots (PnL: {d.profit})")
                continue

            # Check if already exists in DB
            cursor.execute("SELECT id FROM trades WHERE ticket = ?", (d.ticket,))
            if cursor.fetchone(): continue
            
            # Insert missing legitimate trade
            timestamp = datetime.fromtimestamp(d.time).strftime('%Y-%m-%d %H:%M:%S')
            side = "BUY" if d.type == 0 else "SELL"
            
            cursor.execute("""
                INSERT INTO trades (ticket, unit_id, symbol, side, volume, price, pnl, timestamp, type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (d.ticket, "RECON", d.symbol, side, d.volume, d.price, d.profit, timestamp, 'LIVE'))
            added_count += 1
            
            # Add XP for winners
            if d.profit > 0:
                # We don't know the exact unit_id easily from RECON, 
                # but we can try to guess or just skip XP for RECON trades
                pass

        conn.commit()
        conn.close()
        if added_count > 0:
            print(f"--- RECONCILIATION COMPLETE: Added {added_count} missing legitimate trades ---")
        return added_count
