# TELEGRAM REPORTING PROTOCOL (v12.0)

## 1. SSS: SOVEREIGN SILENCE SYSTEM
The SSS is a "Stability-First" reporting protocol designed to minimize noise during periods of high fleet autonomy.

### Exponential Silence Intervals:
- **Baseline**: 1 Hour (3600s)
- **Growth**: Each successful heartbeat doubles the interval.
- **Sequence**: 1H → 2H → 4H → 8H
- **Cap**: 8 Hours max silence.
- **Reset Trigger**: Any process crash detected by the Sentinel or a Prophecy Breach resets the interval to **1 Hour**.

### Heartbeat Format:
- **Header**: 🛡️ SOVEREIGN HEARTBEAT — T+[Uptime]
- **Focus**: Fleet Readiness, Stability Cycles, Equity, and Drawdown.

## 2. HIGH COUNCIL (EVENT-DRIVEN)
The Council report is an tactical overlay that operates independently of the SSS timer.

### Trigger Events:
1. **Periodic Consultation**: Triggered by `high_council.py`.
2. **Prophecy Breach**: Triggered when price breaks $[MIN, MAX]$ boundaries set by the Council.

### Verdict Format:
- **Header**: 🏛️ HIGH COUNCIL VERDICT or 🚨 PROPHECY BREACH
- **Focus**: Bias (BULLISH/BEARISH/CHOP), Price Boundaries, and Tactical Advice.

## 3. REPORTING FLOW
- Regular status → `FleetReporter.send_report()`
- Tactical/Breach → `FleetReporter.send_council_report()`
