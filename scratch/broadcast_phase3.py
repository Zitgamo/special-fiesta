import sys
import os

# Add root to path to import ghost_comm
sys.path.append(os.getcwd())

try:
    from core_v3.ghost_comm import GhostComm
    comm = GhostComm()
    msg = "🚀 <b>PHASE 3 (TACTICAL BETA) INITIALIZED</b>\n━━━━━━━━━━━━━━━━━━\n🟢 <b>SYSTEM MODE</b>: <code>REAL ACCOUNT OVERWATCH</code>\n🛡️ <b>SAFETY STATUS</b>: HARDENED\n📊 <b>TELEMETRY</b>: LIVE FEED ACTIVATED\n\nStanding by for tactical strikes."
    comm.bot.send_message(comm.chat_id, msg, parse_mode='HTML')
    print("SUCCESS: Phase 3 Broadcast sent.")
except Exception as e:
    print(f"Error sending broadcast: {e}")
