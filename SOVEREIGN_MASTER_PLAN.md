# 🛰️ Project "Sovereign Commander" (v1.0)
**Objective:** Orchestrate multiple independent trading bots (Soldiers) using a central Risk/Logic controller (Commander) via a shared SQLite "Black Box."

---

## 1. The Database Architecture (`war_room.db`)
This is the single source of truth. Every bot and the commander must connect here.

| Table | Purpose | Key Columns |
| :--- | :--- | :--- |
| **`squad_status`** | Heartbeat of bots | `bot_id`, `state` (IDLE/ATTACK), `last_seen`, `performance_rank` |
| **`live_orders`** | Current battlefield | `order_id` (Magic/Client), `symbol`, `entry`, `lot`, `strategy_tag` |
| **`command_flags`** | The General's orders | `global_pause`, `max_account_risk`, `focus_fire_multiplier` |
| **`signals_log`** | Historical data | `timestamp`, `bot_id`, `symbol`, `signal_type`, `outcome` |

---

## 2. The Commander Logic (`commander.py`)
This script runs in a persistent loop (the RTS "Game Engine").

*   **Supply Cap Enforcement:** Calculates total margin across Exness + Binance. If $> 10\%$ (example), it writes `CAN_TRADE = 0` to the DB.
*   **Focus Fire Coordination:** If `bot_v8` and `bot_v16` both target Gold, the Commander calculates the "Total Force." It may reduce each bot's lot size so the aggregate position doesn't exceed the "Squad Limit."
*   **The Medic (Auto-Restart):** If a bot's `last_seen` in `squad_status` is $> 60s$, the Commander attempts to re-launch the process.
*   **Global Kill-Switch:** Monitors a "Panic" flag. If triggered (by you via phone/dashboard), it forces a `CLOSE_ALL` across all APIs.

---

## 3. The Soldier Template (`soldier_base.py`)
Update your current bots to follow this flow. Every bot must be "Permission-Based."

1.  **Scanning:** Bot runs its M1/M15 logic (Minigun).
2.  **Request Permission:** Before `order_send`, it queries `command_flags`.
    *   *If `global_pause == 1`:* Abort.
    *   *If `account_risk > limit`:* Abort.
3.  **Deploy Unit:** 
    *   **Exness:** Use `comment="SOV_V8"` and `magic=808`.
    *   **Binance:** Use `newClientOrderId="SOV_V8_12345"`.
4.  **Report Back:** Update `live_orders` in SQLite so the Commander knows the unit is engaged.

---

## 4. Integration with Antigravity & Streamlit
*   **Verification:** Use Antigravity to run a "Dry Run." Feed it the `commander.py` and ask: *"Simulate a crash in Bot A—does the Commander detect it?"*
*   **Visualization:** Your `appGemini.py` (Streamlit) should read the `squad_status` table. 
    *   **Green:** Bot is active and winning.
    *   **Red:** Bot is in drawdown or offline.
    *   **Heatmap:** Show which symbols have the most "Focus Fire" (multiple bots attacking).

---

## 5. RTS Tactical Thought
Imagine your bots are like a fleet of cars. You wouldn't want two cars trying to park in the same spot at the same time. The Commander is your **GPS/Traffic Control**—it ensures every "vehicle" (bot) has its own space to operate safely.
