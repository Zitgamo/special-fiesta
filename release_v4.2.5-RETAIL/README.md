# 🛰️ Iron Commander Elite (v3.5)

**Iron Commander Elite** is a sovereign, autonomous trading ecosystem inspired by Real-Time Strategy (RTS) mechanics.

## 📂 Project Structure

| Path | Purpose |
| :--- | :--- |
| [**`docs/`**](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/docs) | **Documentation & Intelligence Center.** (Architecture, Specs, Manuals) |
| [**`core_v3/`**](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/core_v3) | The primary engine, orchestrator, and trading logic. |
| [**`nexus/`**](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/nexus) | Tactical dashboards for real-time monitoring. |
| [**`03_DATA/`**](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/03_DATA) | Persistent data storage and historical logs. |

## 📖 Essential Documentation
- [**Architecture Master Plan**](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/docs/ARCH_MASTER_PLAN.md)
- [**Sovereign Philosophy Bible**](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/docs/PHILOSOPHY_BIBLE.md)
- [**Risk Management Protocol**](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/docs/RISK_PROTOCOL.md)
- [**User Manual & Control**](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/docs/USER_MANUAL_CONTROL.md)
- [**Developer Operational Protocol**](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/docs/DEV_OPERATIONAL_PROTOCOL.md)

## 🚀 Quick Start
To launch the full sovereign fleet:
1. Ensure MT5 and Binance API keys are configured in `core_v3/secrets.json`.
2. Run the main launch script:
   ```powershell
   ./SOVEREIGN_REAL_LAUNCH.bat
   ```
3. Monitor the fleet via the [**Sovereign Nexus Dashboard**](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/nexus/sovereign_nexus.html).

## 🛡️ Fail-Safe & Emergency Protocols

**Sovereign Philosophy:** Hệ thống được thiết kế để **Tự động hóa & Tự phục hồi**. Nó không bao giờ yêu cầu sự can thiệp thủ công để giữ an toàn (Auto-Trailing, Auto-SL, Equity Guard).

**Manual Overrides:**
- **Web UI:** Sử dụng nút **MASTER ARM** + **EMERGENCY STOP** trên Dashboard.
- **Physical Kill-Switch:** Nếu giao diện web bị treo, hãy chạy file [**`KILL_SWITCH.bat`**](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/KILL_SWITCH.bat) tại thư mục gốc. File này sẽ dừng ngay lập tức các tiến trình Python và khóa Database (`GLOBAL_PAUSE=1`).

---
**Documentation Agent:** *Sovereign Docs*
**Coder Agent:** *Antigravity*
**Commander:** *User*
