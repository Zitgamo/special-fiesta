# DNA ENGINE PROTOCOL

## 1. THE GENETIC ARCHITECTURE
The Sovereign system uses a **DNA-driven execution model** where every unit's behavior is dictated by `03_DATA/iron_dna.json`.

### Parameters:
- `LOT_SIZE`: The base risk unit.
- `DCA_LAYERS`: Number of reinforcement layers.
- `QUARANTINE`: Boolean flag to disable underperforming units.

## 2. EVOLUTIONARY REBIRTH
Every morning at **08:15 ICT**, the `dual_dna_harvester.py` runs to mutate the DNA based on the previous day's performance.

- **Success Mutation**: Profitable units get increased capacity.
- **Failure Mutation**: Losing units have their target multipliers tightened or are quarantined if WR < 35%.

## 3. ZERO-CONSTANT COMPLIANCE
No hardcoded trading constants are permitted in `engine.py`. All thresholds must be derived from the DNA or calculated in real-time by the `IronAnalytics` engine.
