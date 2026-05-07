import pandas as pd
import json
import os
import requests
from datetime import datetime

class HighCouncil:
    def __init__(self, trades_path="03_DATA/vn30_paper_trades.csv"):
        self.trades_path = trades_path
        self.api_key = os.getenv("GROQ_API_KEY") # Prioritize Groq for speed
        
    def generate_tactical_briefing(self):
        """Generates the Markdown report that the LLM will read."""
        uptime = "UNKNOWN"
        try:
            with open("03_DATA/vn30_active_pos.json", "r") as f:
                state = json.load(f)
                uptime = state.get("meta", {}).get("uptime", "UNKNOWN")
        except: pass

        if not os.path.exists(self.trades_path):
            return f" !! [ERROR] No trade data found. [UPTIME: {uptime}]"
            
        try:
            df = pd.read_csv(self.trades_path, on_bad_lines='skip')
            
            pnl_col = df.columns[6]
            total_pnl = df[pnl_col].astype(float).sum()
            wr = (df[pnl_col].astype(float) > 0).mean() * 100
            
            briefing = f"""
# SOVEREIGN TACTICAL BRIEFING: {datetime.now().strftime('%Y-%m-%d')}
## System Vitals
- **Uptime**: {uptime}
- **Total Points Captured**: {total_pnl:+.1f}
- **Win Rate**: {wr:.1f}%
- **Engine**: Deep Sovereign v9.1 (Prophetic Architecture)

## Trade Log (Last 5 Actions)
{df.tail(5).to_markdown(index=False)}

## Tactical Request
Define the current 'Market Scenario.' Predict the boundaries for the next 4-8 hours.
Return ONLY a JSON object with this structure:
{{
  "council_advice": "string",
  "min_boundary": float (The price below which this scenario is INVALID),
  "max_boundary": float (The price above which this scenario is INVALID),
  "bias": "BULLISH/BEARISH/CHOP",
  "overrides": {{
    "governor_sensitivity": float,
    "sentinel_threshold": float
  }}
}}
"""
            return briefing
        except Exception as e:
            return f" !! [ERROR] Briefing generation failed: {str(e)}"

    def get_global_pulse(self):
        """Fetches US30 and Nikkei sentiment to inform the Council."""
        print(" >> [COUNCIL] Harvesting Global Pulse (US30 / Nikkei)...")
        # In a real setup, we use vnstock or a news API here.
        # For now, we simulate the global context for the LLM briefing.
        return {
            "us30_close": "39,500 (+0.4%)",
            "nikkei_open": "38,200 (-0.2%)",
            "sentiment": "NEUTRAL-BULLISH"
        }

    def send_telegram_alert(self, message):
        """Sends tactical alerts to the User's Telegram."""
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        if not token or not chat_id: return
        
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        try:
            requests.post(url, json={"chat_id": chat_id, "text": f"🔱 [SOVEREIGN_COUNCIL]\n{message}"})
        except: pass

    def consult_council(self, is_morning_ritual=False):
        """Consults the LLM and saves the verdict."""
        try:
            if not self.api_key:
                self.save_mock_verdict()
            else:
                briefing = self.generate_tactical_briefing()
                pulse = self.get_global_pulse()
                
                if is_morning_ritual:
                    briefing += f"\n## GLOBAL PULSE (OVERNIGHT)\n- US30: {pulse['us30_close']}\n- Nikkei: {pulse['nikkei_open']}\n- Sentiment: {pulse['sentiment']}"

                print(f" >> [COUNCIL] Consulting the High Council via Groq...")
                
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": "llama-3.1-70b-versatile",
                    "messages": [
                        {"role": "system", "content": "You are the High Council, a tactical AI auditor. You analyze global context and local trade logs to set price boundaries and bias for the VN30 index."},
                        {"role": "user", "content": briefing}
                    ],
                    "response_format": {"type": "json_object"}
                }

                response = requests.post(url, headers=headers, json=data)
                verdict_str = response.json()['choices'][0]['message']['content']
                verdict = json.loads(verdict_str)
                
                with open("03_DATA/council_verdict.json", "w") as f:
                    json.dump(verdict, f, indent=2)
                    
                print(" >> [SUCCESS] High Council Verdict Saved.")
            
        except Exception as e:
            print(f" !! [ERROR] Council consultation failed: {str(e)}")
            self.save_mock_verdict()
            
        finally:
            # --- INTEGRATED REPORTING (v12.0) ---
            try:
                from fleet_report import FleetReporter
                reporter = FleetReporter()
                reporter.send_council_report()
            except Exception as re:
                print(f" !! [ERROR] Reporting bridge failed: {str(re)}")

    def save_mock_verdict(self):
        verdict = {
            "council_advice": "No API key found. Operating on Safe Baseline DNA.",
            "bias": "NEUTRAL-BULLISH",
            "min_boundary": 1250.0,
            "max_boundary": 1350.0,
            "overrides": {
                "governor_sensitivity": 1.0,
                "sentinel_threshold": 0.8
            },
            "timestamp": datetime.now().isoformat()
        }
        with open("03_DATA/council_verdict.json", "w") as f:
            json.dump(verdict, f, indent=2)
        print(" >> [COUNCIL] Safe Verdict Saved to 03_DATA/council_verdict.json")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--morning", action="store_true", help="Trigger Morning Ritual briefing")
    args = parser.parse_args()
    
    council = HighCouncil()
    council.consult_council(is_morning_ritual=args.morning)
