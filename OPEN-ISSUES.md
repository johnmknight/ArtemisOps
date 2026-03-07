# ArtemisOps ISS Tracker - Open Issues

### ~~Page Frame Border Not Visible at Corners (Mission Page)~~ — CLOSED

**Date:** 2026-02-11
**Closed:** 2026-03-06
**Status:** RESOLVED

**Original Problem:** ao-frame-page border not rendering at corner clip-path cuts — diagonal clip visible but no border strokes along the cut edges. Root cause was that `clip-path: polygon()` was clipping the `box-shadow: inset` exactly where it mattered.

**Fix Applied (ao-frames.css):**
Replaced the inset box-shadow border technique with the double clip-path layer approach:
- Outer `.ao-frame-page`: octagonal clip + border color as background
- Inner `::before`: same octagonal clip inset by 2px + dark fill background
- The 2px gap between the two clips IS the visible border ring — no box-shadow required, nothing to clip away
- `box-shadow` now used only for outward glow (unaffected by clip-path)

This technique is confirmed working and now formalized in `ao-frames.css` as the canonical border method for the page tier.

---

## Closed Issues

### ~~ISS Solar Array X-Pattern Bug~~ - CLOSED (Not a Bug)

**Date:** 2026-01-26  
**Status:** CLOSED - Working as intended

**Original Report:** When SARJ rotation is applied, the port and starboard solar arrays form an "X" pattern in the velocity view.

**Clarification:** The original concern was that a **previous bug** had caused port and starboard SARJ joints to rotate in opposite directions due to incorrect code. That bug was fixed earlier. 

The X-pattern observed during this investigation was **not** from that bug - it was correct behavior from NASA telemetry reporting different angles for port vs starboard SARJ.

**Investigation confirmed:**
- The previous rotation direction bug is **not present** in the current code
- Port and starboard SARJ correctly rotate based on their respective telemetry values
- The real ISS SARJ joints operate **independently** and can be at different angles
- X-pattern appears when telemetry values differ (correct behavior)
- Parallel arrays appear when telemetry values are similar (also correct)

**Verified:**
- Rotation axis: X-axis is correct for SARJ joints
- Code correctly applies NASA Lightstreamer telemetry
- No sign inversion or opposite rotation bug present

**Files involved:**
- `client/components/iss-tracker.html` (updateSolarArrays function)
