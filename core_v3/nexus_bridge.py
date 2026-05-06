from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os
import json
import subprocess
import MetaTrader5 as mt5
import sys
import time
from datetime import datetime, timedelta

START_TIME = time.time()

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

def calculate_sovereign_scale():
    """Calculates Logic (Back) vs Aesthetic (Front) balance with complexity weighting."""
    try:
        py_lines = 0
        py_files = 0
        for root, _, files in os.walk(ROOT_DIR):
            if "venv" in root or ".git" in root: continue
            for f in files:
                if f.endswith('.py'):
                    py_files += 1
                    with open(os.path.join(root, f), 'r', encoding='utf-8', errors='ignore') as f_obj:
                        py_lines += len(f_obj.readlines())
        
        ui_lines = 0
        ui_files = 0
        nexus_dir = os.path.join(ROOT_DIR, "nexus")
        if os.path.exists(nexus_dir):
            for root, _, files in os.walk(nexus_dir):
                for f in files:
                    if f.endswith(('.html', '.css', '.js')):
                        ui_files += 1
                        with open(os.path.join(root, f), 'r', encoding='utf-8', errors='ignore') as f_obj:
                            ui_lines += len(f_obj.readlines())
                            
        # Intelligence Weight: 1MB of DB = 5000 virtual lines of "Experience"
        db_size = 0
        db_path = os.path.join(ROOT_DIR, "core_v3", "iron_core.db")
        if os.path.exists(db_path):
            db_size = os.path.getsize(db_path) / (1024 * 1024) # MB
        
        # Complexity Weight: Back has 1.5x weight per line + Experience weight
        back_score = (py_lines * 1.5) + (db_size * 5000)
        front_score = ui_lines * 1.0
        total = back_score + front_score
        
        return {
            "back": round(back_score / total * 100, 1) if total > 0 else 73.2,
            "front": round(front_score / total * 100, 1) if total > 0 else 26.8,
            "back_lines": py_lines,
            "front_lines": ui_lines
        }
    except:
        return {"back": 73.2, "front": 26.8, "back_lines": 4043, "front_lines": 1480}

def _get_git_metadata():
    try:
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], stderr=subprocess.DEVNULL).decode().strip()
        commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL).decode().strip()
        status = subprocess.check_output(["git", "status", "--porcelain"], stderr=subprocess.DEVNULL).decode().strip()
        return {"branch": branch, "commit": commit, "dirty": len(status) > 0}
    except:
        return {"branch": "MASTER", "commit": "---", "dirty": False}

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

@app.route('/report', methods=['GET'])
def report():
    try:
        report_path = os.path.join(ROOT_DIR, "nexus", "elite_report.html")
        with open(report_path, 'r', encoding='utf-8') as f: return f.read()
    except Exception as e: return f"REPORT_NOT_FOUND: {e}", 404

@app.route('/api/reports/equity_curve', methods=['GET'])
def get_equity_curve():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Fetch last 100 points for a smooth curve
        cursor.execute("SELECT timestamp, equity FROM equity_history ORDER BY id DESC LIMIT 100")
        data = cursor.fetchall()
        conn.close()
        return jsonify([{"t": d[0], "e": d[1]} for d in reversed(data)])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/telemetry', methods=['GET'])
def get_telemetry():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 1. (Legacy MT5 fetch removed - now using live mt5_health below)
        
        # 2. Strike Logs (Filter out FAILED/PENDING)
        cursor.execute("SELECT symbol, side, volume, price, pnl, timestamp, unit_id, sl, tp FROM trades WHERE type IN ('LIVE', 'CLOSED', 'PAPER') ORDER BY id DESC LIMIT 10")
        trades_raw = cursor.fetchall()
        
        # 3. Multi-Timeframe PnL Audit
        # --- DAY (Last 24h) ---
        cursor.execute("SELECT pnl, unit_id, symbol FROM trades WHERE timestamp >= datetime('now', '-1 day')")
        day_trades = cursor.fetchall()
        day_pnl_front = sum(t[0] for t in day_trades if "SOUTH" not in str(t[1]) and t[2] != "VN30F1M")
        day_pnl_back = sum(t[0] for t in day_trades if "SOUTH" in str(t[1]) or t[2] == "VN30F1M") * 100000

        # --- WEEK (Last 7d) ---
        cursor.execute("SELECT pnl, unit_id, symbol FROM trades WHERE timestamp >= datetime('now', '-7 days')")
        week_trades = cursor.fetchall()
        week_pnl_front = sum(t[0] for t in week_trades if "SOUTH" not in str(t[1]) and t[2] != "VN30F1M")
        week_pnl_back = sum(t[0] for t in week_trades if "SOUTH" in str(t[1]) or t[2] == "VN30F1M") * 100000

        # --- MONTH (Last 30d) ---
        cursor.execute("SELECT pnl, unit_id, symbol FROM trades WHERE timestamp >= datetime('now', '-30 days')")
        month_trades = cursor.fetchall()
        month_pnl_front = sum(t[0] for t in month_trades if "SOUTH" not in str(t[1]) and t[2] != "VN30F1M")
        month_pnl_back = sum(t[0] for t in month_trades if "SOUTH" in str(t[1]) or t[2] == "VN30F1M") * 100000

        session_pnl = round(day_pnl_front, 2)
        session_pnl_vnd = int(day_pnl_back)
        
        # Calculate Sovereign System Balance (Ruột vs Vỏ)
        system_balance = calculate_sovereign_scale()

        current_time_local = (datetime.utcnow() + timedelta(hours=7)).strftime('%H:%M:%S')
        
        # 2. MT5 Health (Exness)
        mt5_health = {"equity": 0, "drawdown": 0}
        try:
            if mt5.initialize():
                acc = mt5.account_info()
                if acc:
                    mt5_health["equity"] = acc.equity
                    mt5_health["drawdown"] = (acc.equity / acc.balance - 1) if acc.balance != 0 else 0
        except: pass
        
        # 4. Binance Health
        bnc_health = {"equity": 0, "drawdown": 0}
        try:
            if BRIDGES.binance:
                bal = BRIDGES.binance.fetch_balance()
                bnc_health["equity"] = bal['total'].get('USDT', 0)
                positions = BRIDGES.binance.fetch_positions()
                float_pnl = sum(float(p.get('unrealizedProfit', 0)) for p in positions if float(p.get('contracts', 0)) > 0)
                if bnc_health["equity"] > 0:
                    bnc_health["drawdown"] = float_pnl / bnc_health["equity"]
        except: pass

        # 5. Southern Health (Entrade/VN30)
        last_vnd_equity = 100000000
        try:
            cursor.execute("SELECT equity FROM equity_history WHERE equity > 1000000 ORDER BY id DESC LIMIT 1")
            res = cursor.fetchone()
            if res: last_vnd_equity = res[0]
        except: pass

        south_health = {"equity_vnd": last_vnd_equity, "drawdown": 0, "active": False, "fleet": {}, "context": {"er": 0.5, "atr": 0, "confidence": 50}}
        try:
            if os.path.exists(SOUTH_STATE_PATH):
                with open(SOUTH_STATE_PATH, 'r') as f:
                    south_health["fleet"] = json.load(f)
                    if south_health["fleet"]:
                        first_unit = list(south_health["fleet"].values())[0]
                        south_health["equity_vnd"] = first_unit.get("equity_vnd", last_vnd_equity)
                        south_health["active"] = any(u.get("active", False) for u in south_health["fleet"].values())
            
            float_pnl_vnd = sum(u.get("pnl_vnd", 0) for u in south_health["fleet"].values())
            if south_health["equity_vnd"] > 0:
                south_health["drawdown"] = float_pnl_vnd / south_health["equity_vnd"]
            
            er_vn = IronAnalytics.get_efficiency_ratio("VN30F1M", BRIDGES)
            south_health["context"]["er"] = er_vn
            south_health["context"]["atr"] = IronAnalytics.get_atr("VN30F1M", BRIDGES)
            
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
            
            m_ctx = {"er": 0.5, "atr": 0, "confidence": 50}
            if squad.get(unit):
                main_sym = squad[unit][0]
                er = IronAnalytics.get_efficiency_ratio(main_sym, BRIDGES)
                m_ctx["er"] = er
                m_ctx["atr"] = IronAnalytics.get_atr(main_sym, BRIDGES)
                
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
        
        # Add Uptime
        cursor.execute("SELECT value FROM hq_config WHERE key = 'SYSTEM_BOOT_TIME'")
        boot_res = cursor.fetchone()
        if not boot_res:
            boot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT OR REPLACE INTO hq_config (key, value, description) VALUES ('SYSTEM_BOOT_TIME', ?, 'Persistent Uptime Tracker')", (boot_time,))
            conn.commit()
        else:
            boot_time = boot_res[0]
            
        boot_dt = datetime.strptime(boot_time, "%Y-%m-%d %H:%M:%S")
        uptime_sec = (datetime.now() - boot_dt).total_seconds()
        
        data = {
            "status": "ONLINE",
            "safety_status": "HARDENED",
            "session_pnl_usd": round(day_pnl_front, 2),
            "session_pnl_vnd": int(day_pnl_back),
            "system_balance": system_balance,
            "stats_day": {"usd": round(day_pnl_front, 2), "vnd": int(day_pnl_back)},
            "stats_week": {"usd": round(week_pnl_front, 2), "vnd": int(week_pnl_back)},
            "stats_month": {"usd": round(month_pnl_front, 2), "vnd": int(month_pnl_back)},
            "health_mt5": mt5_health,
            "health_bnc": bnc_health,
            "health_south": south_health,
            "trades": [{
                "symbol": t[0], "side": t[1], "vol": t[2], "price": t[3], "pnl": t[4], "time": t[5], "unit": t[6], "sl": t[7], "tp": t[8]
            } for t in trades_raw],
            "dna": dna,
            "squadron": squad,
            "unit_stats": unit_stats,
            "git_status": _get_git_metadata(),
            "back_score": round(system_balance['back'], 1),
            "front_score": round(system_balance['front'], 1),
            "deploy_mode": get_deploy_mode(),
            "current_time_utc": current_time_local,
            "uptime_seconds": uptime_sec
        }
        
        return jsonify(data)
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

@app.route('/report', methods=['GET'])
def view_report():
    try:
        with open(os.path.join(ROOT_DIR, "nexus", "elite_report.html"), 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"REPORT ERROR: {str(e)}", 500

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
            WHERE sl_mult IS NOT NULL AND tp_mult IS NOT NULL
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
                "symbol": c[0], "sl": c[1], "tp": c[2], "trades": c[3], "avg_pnl": round(c[4] or 0, 2)
            } for c in top_configs],
            "regime_perf": {r[0]: round(r[1] or 0, 2) for r in regime_perf}
        })
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

@app.route('/api/sync', methods=['POST'])
def force_sync():
    try:
        # Trigger actual MT5/Binance re-poll
        mt5.initialize()
        IronBridges.refresh_all()
        return jsonify({"status": "SUCCESS", "message": "FLEET SYNCHRONIZED"})
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

@app.route('/api/tactical/stop', methods=['POST'])
def tactical_stop():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE hq_config SET value = '1' WHERE key = 'GLOBAL_PAUSE'")
        conn.commit()
        conn.close()
        return jsonify({"status": "SUCCESS", "message": "GLOBAL KILL-SWITCH ACTIVATED"})
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

@app.route('/api/tactical/reinforce', methods=['POST'])
def tactical_reinforce():
    try:
        data = request.json
        unit = data.get('unit')
        action = data.get('action', 'reinforce') # 'reinforce' or 'reset'
        
        if not unit or not os.path.exists(DNA_PATH):
            return jsonify({"status": "ERROR", "message": "INVALID_UNIT_OR_DNA"}), 400
            
        with open(DNA_PATH, 'r') as f: dna_data = json.load(f)
        
        if unit in dna_data:
            if action == 'reinforce':
                dna_data[unit]['LOT_SIZE'] = round(dna_data[unit].get('LOT_SIZE', 0.01) * 1.5, 2)
                dna_data[unit]['DCA_LAYERS'] = dna_data[unit].get('DCA_LAYERS', 5) + 2
            else:
                dna_data[unit]['LOT_SIZE'] = 0.01 # Reset to base
                
            with open(DNA_PATH, 'w') as f: json.dump(dna_data, f, indent=4)
            return jsonify({"status": "SUCCESS", "message": f"UNIT {unit} {action.upper()}ED"})
            
        return jsonify({"status": "ERROR", "message": "UNIT_NOT_IN_DNA"}), 404
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

@app.route('/api/tactical/mode', methods=['POST'])
def tactical_mode():
    try:
        data = request.json
        mode = data.get('mode', 'DEMO').upper()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO config (key, value) VALUES ('DEPLOY_MODE', ?)", (mode,))
        conn.commit()
        conn.close()
        return jsonify({"status": "SUCCESS", "message": f"SYSTEM MODE SET TO {mode}"})
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

def get_deploy_mode():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM config WHERE key = 'DEPLOY_MODE'")
        res = cursor.fetchone()
        conn.close()
        return res[0] if res else "DEMO"
    except:
        return "DEMO"

@app.route('/api/git_status', methods=['GET'])
def get_git_status():
    try:
        import subprocess
        # Get last 3 commits
        cmd = ["git", "log", "-n", "3", "--oneline", "--format=%h|%s|%ar"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        commits = []
        for line in result.stdout.strip().split('\n'):
            if '|' in line:
                h, s, r = line.split('|')
                commits.append({"hash": h, "msg": s, "rel": r})
        
        # Check if dirty
        dirty_cmd = ["git", "status", "--porcelain"]
        dirty_res = subprocess.run(dirty_cmd, capture_output=True, text=True)
        is_dirty = len(dirty_res.stdout.strip()) > 0
        
        return jsonify({
            "status": "SUCCESS", 
            "commits": commits, 
            "is_dirty": is_dirty,
            "srs_score": 65, # Auditor manually injected score
            "uptime_seconds": time.time() - START_TIME,
            "current_time_utc": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

@app.route('/api/tactical/mode', methods=['POST'])
def toggle_core_mode():
    try:
        data = request.json
        new_mode = data.get('mode', '0') # '0'=Demo, '1'=Real
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE hq_config SET value = ? WHERE key = 'CORE_MODE'", (str(new_mode),))
        conn.commit()
        conn.close()
        return jsonify({"status": "SUCCESS", "message": f"CORE_MODE SET TO {new_mode}"})
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=False)
