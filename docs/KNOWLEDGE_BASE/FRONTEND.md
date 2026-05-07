# 🎨 ZONE: FRONTEND HARDENING

This document tracks all visual and interaction-layer vulnerabilities identified during the development of the Nexus and Southern Command dashboards.

## 🚨 Identified Bug Zones

### 1. Chrome 3D Flipper "Ghosting"
- **Bug**: Backface side of a flipped panel appears overlapping with the front side.
- **Cause**: Chrome flattens 3D space when `overflow: hidden` is applied to elements with `transform-style: preserve-3d`.
- **Solution**: Remove `overflow: hidden` from `.front` and `.back` containers.

### 2. Flexbox Height Deception
- **Bug**: Panels appearing "squished" or collapsed to 0px even with `flex: 1`.
- **Cause**: Parent containers with fixed `height: calc(...)` and `min-height: 0` force children to collapse if the total children `min-height` exceeds the parent's limit.
- **Solution**: Use `min-height: calc(...)` on the `main` container and remove `min-height: 0` from columns to allow growth.

### 3. Uptime DOM Deletion
- **Bug**: Progress bar disappears when the clock updates.
- **Cause**: Using `.innerText` or `.innerHTML` on the parent container wipes out child `<div>` elements.
- **Solution**: Use a dedicated `<span id="uptime-ticker">` for text updates and target `#uptime-progress` separately.

### 4. Currency Detection Logic
- **Protocol**: Symbols like `VN30F1M` must be routed through `formatVND()` instead of the standard `$0.00` formatter to ensure tactical consistency with the Vietnamese market.
