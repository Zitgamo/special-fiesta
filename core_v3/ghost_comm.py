import telebot
import json
import os
import time

class GhostComm:
    """
    Secure Telegram Command Bridge.
    Allows for remote mobile command and control.
    """
    def __init__(self, secrets_path="core_v3/secrets.json"):
        with open(secrets_path, 'r') as f:
            secrets = json.load(f)
        self.bot = telebot.TeleBot(secrets["telegram_token"])
        self.chat_id = secrets["telegram_chat_id"]
        self._setup_handlers()

    def _setup_handlers(self):
        @self.bot.message_handler(commands=['start', 'status'])
        def send_status(message):
            try:
                import requests
                # Fetch live data from the local Bridge API
                response = requests.get('http://127.0.0.1:5050/api/telemetry')
                data = response.json()
                
                # HTML Formatting for a premium Telegram UI
                status_msg = (
                    "<b>🦅 SOVEREIGN TACTICAL COMMAND 🦅</b>\n"
                    "━━━━━━━━━━━━━━━━━━\n"
                    f"🟢 <b>STATUS</b>: {data.get('status', 'ONLINE')}\n"
                    f"🕒 <b>LOCAL TIME</b>: <code>{data.get('current_time_utc', '--')}</code>\n\n"
                    
                    "<b>📊 PERFORMANCE (DAY)</b>\n"
                    f" 🔹 <b>Global (USD)</b>: <code>${data.get('session_pnl_usd', 0):+.2f}</code>\n"
                    f" 🔹 <b>Southern (VND)</b>: <code>{data.get('session_pnl_vnd', 0):+,} đ</code>\n\n"
                    
                    "<b>📅 AGGREGATE RECAP</b>\n"
                    f" 🔸 <b>WEEK</b>: <code>${data.get('stats_week', {}).get('usd', 0):+.2f}</code> | <code>{data.get('stats_week', {}).get('vnd', 0):+,} đ</code>\n"
                    f" 🔸 <b>MONTH</b>: <code>${data.get('stats_month', {}).get('usd', 0):+.2f}</code> | <code>{data.get('stats_month', {}).get('vnd', 0):+,} đ</code>\n\n"
                    
                    "<b>⚖️ SYSTEM BALANCE (RUỘT vs VỎ)</b>\n"
                    f" [<code>{'█' * int(data.get('system_balance', {}).get('back', 70) / 10)}{'░' * (10 - int(data.get('system_balance', {}).get('back', 70) / 10))}</code>]\n"
                    f" <i>Back (Logic): {data.get('system_balance', {}).get('back', 0):.1f}% | Front (UI): {data.get('system_balance', {}).get('front', 0):.1f}%</i>\n"
                    "━━━━━━━━━━━━━━━━━━\n"
                    "🔗 <a href='http://127.0.0.1:5050/'>OPEN NEXUS DASHBOARD</a>"
                )
                self.bot.reply_to(message, status_msg, parse_mode='HTML')
            except Exception as e:
                self.bot.reply_to(message, f"❌ <b>COMMAND FAILED</b>: <code>{e}</code>", parse_mode='HTML')

        @self.bot.message_handler(commands=['rebirth'])
        def force_rebirth(message):
            self.bot.reply_to(message, "COMMAND RECEIVED: Initiating Evolutionary Mutation...")
            # Trigger logic in DNA
            
    def notify(self, text):
        """Sends an urgent notification to the Commander."""
        try:
            self.bot.send_message(self.chat_id, f" !! [ALERT] {text}")
        except Exception as e:
            print(f" !! [GHOST_ERR] Notify failed: {e}")

    def run(self):
        print("--- GHOST COMM ACTIVE: AWAITING MOBILE COMMANDS ---")
        while True:
            try:
                self.bot.infinity_polling()
            except Exception as e:
                if "401" in str(e):
                    print(" !! [FATAL] GHOST COMM: 401 UNAUTHORIZED. Verify Telegram Token.")
                    time.sleep(3600) # Wait an hour before retrying to prevent spam
                else:
                    print(f" !! [GHOST_ERR] Connection failed: {e}. Retrying in 30s...")
                    time.sleep(30)

if __name__ == "__main__":
    try:
        comm = GhostComm()
        comm.run()
    except Exception as e:
        print(f" !! [GHOST_CRIT] Initialization failed: {e}")
        time.sleep(60)
