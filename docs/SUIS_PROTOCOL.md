# 🔱 SOVEREIGN UI STANDARD (SUIS) v1.1
## [Deep Layer & Multi-State Hardening]

This protocol is MANDATORY for all Sovereign Nexus UI modifications. Any AI update that bypasses these checks is a direct violation of Phase 3 Operational Integrity.

### 1. Viewport & Scroll Integrity
- **100vh Lock**: The root `body` and `main` must never exceed `window.innerHeight`.
- **Nested Mobility**: All tactical modules (`#trade-log`, `#intel-list`, etc.) must have `overflow-y: auto` and `flex: 1` to ensure internal scrolling works independently of the viewport lock.

### 2. Multi-State Audit (Deep Layer Inspection)
Before declaring an update stable, the following states MUST be inspected:
- **FRONT STATE**: Default dashboard view.
- **HOVER STATE**: Verify `translateZ` and `rotate` interactions do not clip into sibling panels or the header/footer.
- **BACK STATE (FLIPPED)**: All summary metrics (Win Rate, Drawdown) must be fully visible and scrollable. `justify-content: center` is forbidden on back-side panels to prevent clipping on small viewports.

### 3. Contrast & Accessibility
- **HUD Contrast**: Minimum 4.5:1 ratio for all telemetry labels.
- **Palette Enforcement**:
  - `var(--neon-blue)`: Primaries
  - `var(--neon-purple)`: Secondary/VND Command
  - `var(--neon-gold)`: Escalation/Scale-Up
  - `var(--neon-red)`: Emergency/Error

### 4. Interactive Integrity
- **Pointer Events**: Ensure overlays like `scanline` do not block interaction with deeper layers (modals/buttons).
- **Z-Index Hierarchy**: Strict layering to prevent holographic overlap between the fixed header and 3D-hovering panels.
