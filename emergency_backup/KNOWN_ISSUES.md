# KNOWN ISSUES & WORKAROUNDS

## 🚨 ACTIVE ISSUES

### 1. MT5 Connectivity Latency
- **Symptom**: Slight delay in `nexus_bridge.py` when polling MT5 equity.
- **Root Cause**: Windows process priority and MT5 internal polling.
- **Workaround**: Global telemetry cache implemented in `nexus_bridge.py` with 10s TTL.

### 2. VN30F1M VCI Data Gaps
- **Symptom**: Occasional "Empty Dataframe" warnings from `vnstock`.
- **Root Cause**: Upstream server instability at VCI.
- **Workaround**: Deterministic retry loop (5x) added to `fleet_report.py` and `southern_paper_bridge.py`.

### 3. Librarian Index Encoding
- **Symptom**: Emojis in `00_INDEX.md` can sometimes cause UTF-8 artifacts in Windows viewers.
- **Fix**: Librarian now uses explicit `encoding='utf-8'` and PowerShell post-processing.

## 🛠️ RESOLVED RECENTLY
- [FIXED] Telegram report spamming (Separated SSS from Council).
- [FIXED] Persistent Uptime reset on Sentinel restart.
