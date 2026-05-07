import requests
import json
import time
import os

class SignalCommander:
    """
    The Elite Co-Pilot.
    Watches the Sovereign Fleet and provides manual copy signals for the $100 Real Account.
    """
    def __init__(self, secrets_path="core_v3/secrets.json", quiet_mode=True):
        with open(secrets_path, 'r') as f:
            self.secrets = json.load(f)
        self.token = self.secrets.get("telegram_token")
        self.chat_id = self.secrets.get("telegram_chat_id")
        self.last_signal_time = 0
        self.last_alert_time = {}  # Track per-symbol alert times
        self.quiet_mode = quiet_mode  # Disable alerts if True
        self.min_alert_interval = 300  # Minimum 5 minutes between alerts per symbol

    def send_signal(self, symbol, side, price, sl, tp, er, lot=0.01, reason="Elite Alpha"):
        """
        Sends a professional tactical strike card for manual copy-trading.
        Still sends even in quiet mode (important signals only).
        """
        regime = "TRENDING" if er > 0.5 else "VOLATILE"
        message = (
            f"⚡️ *SOVEREIGN ELITE STRIKE* ⚡️\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"⚔️ *ACTION*: {side} {symbol}\n"
            f"💰 *PRICE*: `{price:.5f}`\n\n"
            f"🛑 *STOP LOSS*: `{sl:.5f}`\n"
            f"🎯 *TAKE PROFIT*: `{tp:.5f}`\n\n"
            f"📊 *TACTICAL GUIDANCE*:\n"
            f" 🔸 *Trade Size*: {lot} Lot (Fixed $100 Plan)\n"
            f" 🔸 *Market Regime*: {regime}\n"
            f" 🔸 *Strategy*: {reason}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🚀 *Copy these parameters to your REAL account now.*"
        )
        
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                print(f" >> [SIGNAL_SENT] {side} {symbol}")
            return response.status_code == 200
        except Exception as e:
            print(f" !! [SIGNAL_ERR] {e}")
            return False

    def send_alert(self, title, symbol, details, pnl=None):
        """
        Sends a tactical update or trailing advice for an active position.
        Rate-limited to prevent Telegram spam.
        """
        # Skip alerts if quiet mode is enabled
        if self.quiet_mode:
            return False
        
        # Rate limiting: don't send the same alert more than once per 5 minutes
        current_time = time.time()
        last_alert = self.last_alert_time.get(symbol, 0)
        if current_time - last_alert < self.min_alert_interval:
            return False  # Skip this alert
        
        self.last_alert_time[symbol] = current_time
        
        pnl_str = f"\n💰 *PNL*: {pnl:+.2f}" if pnl is not None else ""
        message = (
            f"🛰️ *TACTICAL ALERT: {title}* 🛰️\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🛡️ *ASSET*: {symbol}\n"
            f"📝 *DETAILS*: {details}"
            f"{pnl_str}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🔗 *Monitor this position in your MT5 Terminal.*"
        )
        
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        try:
            response = requests.post(url, json=payload)
            return response.status_code == 200
        except Exception as e:
            print(f" !! [ALERT_ERR] {e}")
            return False

if __name__ == "__main__":
    # Test Signal
    sc = SignalCommander()
    sc.send_signal("XAUUSD", "BUY", 4534.0, 4520.0, 4560.0, 0.75)
