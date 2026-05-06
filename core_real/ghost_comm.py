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
                # Fetch live data from DNA or Bridge
                with open("core_v3/dna.json", "r") as f:
                    dna = json.load(f)
                
                status_msg = (
                    "--- SOVEREIGN COMMAND STATUS ---\n"
                    f"REGIME: {dna['GLOBAL'].get('REGIME', 'NEUTRAL')}\n"
                    f"ALPHA: {dna['ALPHA'].get('LOT_MULT', 1.0)}x | OMEGA: {dna['OMEGA'].get('LOT_MULT', 1.0)}x\n"
                    "--------------------------------"
                )
                self.bot.reply_to(message, status_msg)
            except Exception as e:
                self.bot.reply_to(message, f"ERR: {e}")

        @self.bot.message_handler(commands=['rebirth'])
        def force_rebirth(message):
            self.bot.reply_to(message, "COMMAND RECEIVED: Initiating Evolutionary Mutation...")
            # Trigger logic in DNA
            
    def notify(self, text):
        """Sends an urgent notification to the Commander."""
        try:
            self.bot.send_message(self.chat_id, f" !! [ALERT] {text}")
        except: pass

    def run(self):
        print("--- GHOST COMM ACTIVE: AWAITING MOBILE COMMANDS ---")
        self.bot.infinity_polling()

if __name__ == "__main__":
    comm = GhostComm()
    comm.run()
