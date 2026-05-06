from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import os
import json
import MetaTrader5 as mt5
import sys

# Ensure core_v3 is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from bridges import IronBridges
from analytics import IronAnalytics

app = Flask(__name__)
CORS(app)

# --- PATHS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(BASE_DIR, "iron_core.db")
DNA_PATH = os.path.join(BASE_DIR, "dna.json")
SQUADRON_PATH = os.path.join(BASE_DIR, "squadron.json")
SECRETS_PATH = os.path.join(BASE_DIR, "secrets.json")
SOUTH_STATE_PATH = os.path.join(ROOT_DIR, "03_DATA", "vn30_active_pos.json")

# Visual Paths
NEXUS_HTML = os.path.join(ROOT_DIR, "nexus", "sovereign_nexus.html")
SOUTH_HTML = os.path.join(ROOT_DIR, "nexus", "southern_command.html")
ELITE_HTML = os.path.join(ROOT_DIR, "nexus", "elite_focus.html")

BRIDGES = IronBridges(SECRETS_PATH)

@app.route('/', methods=['GET'])
def index():
    try:
        with open(NEXUS_HTML, 'r', encoding='utf-8') as f: return f.read()
    except Exception as e: return f"NEXUS_NOT_FOUND: {e}", 404

@app.route('/elite', methods=['GET'])
def elite():
    try:
        with open(ELITE_HTML, 'r', encoding='utf-8') as f: return f.read()
    except Exception as e: return f"ELITE_NOT_FOUND: {e}", 404

@app.route('/southern_command.html', methods=['GET'])
def southern():
    try:
        with open(SOUTH_HTML, 'r', encoding='utf-8') as f: return f.read()
    except Exception as e: return f"SOUTH_NOT_FOUND: {e}", 404

@app.route('/api/telemetry', methods=['GET'])
def get_telemetry():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 1. MT5 Health (Exness)
        cursor.execute("SELECT balance, equity, drawdown, timestamp FROM equity_history ORDER BY id DESC LIMIT 1")
        health = cursor.fetchone()
        
        # 2. Strike Logs (Filter out FAILED/PENDING)
        cursor.execute("SELECT symbol, side, volume, price, pnl, timestamp, unit_id, sl, tp FROM trades WHERE type IN ('LIVE', 'CLOSED', 'PAPER') ORDER BY id DESC LIMIT 10")
        trades_raw = cursor.fetchall()
        
        # 3. Session PnL (Realized Growth Today - Multi-Front)
        # Using 00:00 UTC as the anchor for professional session tracking
        cursor.execute("SELECT unit_id, symbol, pnl FROM trades WHERE date(timestamp) = date('now')")
        today_trades = cursor.fetchall()
        
        ex_realized = sum(t[2] for t in today_trades if "USDT" not in str(t[1]) and "SOUTH" not in str(t[0]) and t[1] != "VN30F1M")
        bnc_realized = sum(t[2] for t in today_trades if "USDT" in str(t[1]))
        south_realized_vnd = sum(t[2] for t in today_trades if "SOUTH" in str(t[0]) or t[1] == "VN30F1M")
        
        session_pnl = round(ex_realized + bnc_realized, 2)
        session_pnl_vnd = int(south_realized_vnd) if south_realized_vnd != 0 else int(session_pnl * 25000)
        
        from datetime import datetime
        current_time_utc = datetime.utcnow().strftime('%H:%M:%S')
        
        # 4. Binance Health
        bnc_health = {"equity": 0, "drawdown": 0}
        try:
            if BRIDGES.binance:
                bal = BRIDGES.binance.fetch_balance()
                bnc_health["equity"] = bal['total'].get('USDT', 0)
        except: pass

        # 5. Southern Health (Entrade/VN30)
        south_health = {"equity_vnd": 100000000, "drawdown": 0, "active": False, "fleet": {}, "context": {"er": 0.5, "atr": 0, "confidence": 50}}
        try:
            if os.path.exists(SOUTH_STATE_PATH):
                with open(SOUTH_STATE_PATH, 'r') as f:
                    south_health["fleet"] = json.load(f)
                    if south_health["fleet"]:
                        first_unit = list(south_health["fleet"].values())[0]
                        south_health["equity_vnd"] = first_unit.get("equity_vnd", 100000000)
                        south_health["active"] = any(u.get("active", False) for u in south_health["fleet"].values())
            
            # Context v2.0 for Southern Front
            er_vn = IronAnalytics.get_efficiency_ratio("VN30F1M", BRIDGES)
            south_health["context"]["er"] = er_vn
            south_health["context"]["atr"] = IronAnalytics.get_atr("VN30F1M", BRIDGES)
            
            # Neural Confidence for VN30F1M
            cursor.execute("""
                SELECT AVG(CASE WHEN outcome_pnl > 0 THEN 1 ELSE 0 END) * 100, COUNT(*)
                FROM empirical_learning 
                WHERE symbol = 'VN30F1M' AND er_at_entry BETWEEN ? AND ?
            """, (er_vn - 0.1, er_vn + 0.1))
            c_res = cursor.fetchone()
            if c_res and c_res[1] > 0:
                south_health["context"]["confidence"] = int(c_res[0])
        except: pass

        # 6. DNA & Squadron
        dna = {}
        squad = {}
        if os.path.exists(DNA_PATH):
            with open(DNA_PATH, 'r') as f: dna = json.load(f)
        if os.path.exists(SQUADRON_PATH):
            with open(SQUADRON_PATH, 'r') as f: squad = json.load(f)
            
        # 7. Unit Stats Audit
        unit_stats = {}
        for unit in ["ALPHA", "OMEGA", "GAMMA"]:
            cursor.execute("SELECT COUNT(*), SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) FROM trades WHERE unit_id = ? AND pnl != 0", (unit,))
            total, wins = cursor.fetchone()
            wr = (wins / total * 100) if total and total > 0 else 0
            
            # Fetch Live Market Context (Context v2.0)
            m_ctx = {"er": 0.5, "atr": 0, "confidence": 50}
            if squad.get(unit):
                main_sym = squad[unit][0]
                er = IronAnalytics.get_efficiency_ratio(main_sym, BRIDGES)
                m_ctx["er"] = er
                m_ctx["atr"] = IronAnalytics.get_atr(main_sym, BRIDGES)
                
                # Calculate Neural Confidence (Historical WR at similar ER)
                try:
                    cursor.execute("""
                        SELECT AVG(CASE WHEN outcome_pnl > 0 THEN 1 ELSE 0 END) * 100, COUNT(*)
                        FROM empirical_learning 
                        WHERE symbol = ? AND er_at_entry BETWEEN ? AND ?
                    """, (main_sym, er - 0.1, er + 0.1))
                    conf_res = cursor.fetchone()
                    if conf_res and conf_res[1] > 0:
                        m_ctx["confidence"] = int(conf_res[0])
                except: pass
            
            unit_stats[unit] = {
                "win_rate": f"{wr:.0f}%", 
                "strikes": total or 0,
                "context": m_ctx
            }
        
        conn.close()
        
        return jsonify({
            "status": "ONLINE",
            "safety_status": "HARDENED",
            "session_pnl_usd": session_pnl,
            "session_pnl_vnd": session_pnl_vnd,
            "health_mt5": {
                "balance": health[0] if health else 0,
                "equity": health[1] if health else 0,
                "drawdown": health[2] if health else 0,
                "last_update": health[3] if health else "N/A"
            },
            "health_bnc": bnc_health,
            "health_south": south_health,
            "trades": [{
                "symbol": t[0], "side": t[1], "vol": t[2], "price": t[3], "pnl": t[4], "time": t[5], "unit": t[6], "sl": t[7], "tp": t[8]
            } for t in trades_raw],
            "dna": dna,
            "squadron": squad,
            "unit_stats": unit_stats,
            "current_time_utc": current_time_utc
        })
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

@app.route('/api/intelligence', methods=['GET'])
def get_intelligence():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 1. Total Learning Samples
        cursor.execute("SELECT COUNT(*) FROM empirical_learning")
        total_samples = cursor.fetchone()[0]
        
        # 2. Top Performing Configs
        cursor.execute("""
            SELECT symbol, sl_mult, tp_mult, COUNT(*) as count, AVG(outcome_pnl) as pnl
            FROM empirical_learning
            GROUP BY symbol, sl_mult, tp_mult
            ORDER BY pnl DESC LIMIT 5
        """)
        top_configs = cursor.fetchall()
        
        # 3. Regime Performance
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN er_at_entry < 0.3 THEN 'Ranging'
                    WHEN er_at_entry BETWEEN 0.3 AND 0.6 THEN 'Transition'
                    ELSE 'Trending'
                END as regime,
                AVG(outcome_pnl) as avg_pnl
            FROM empirical_learning
            GROUP BY regime
        """)
        regime_perf = cursor.fetchall()
        
        conn.close()
        
        return jsonify({
            "samples": total_samples,
            "top_configs": [{
                "symbol": c[0], "sl": c[1], "tp": c[2], "trades": c[3], "avg_pnl": round(c[4], 2)
            } for c in top_configs],
            "regime_perf": {r[0]: round(r[1], 2) for r in regime_perf}
        })
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5050, debug=False)
