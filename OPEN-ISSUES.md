# ArtemisOps ISS Tracker - Open Issues

### Page Frame Border Not Visible at Corners (Mission Page)

**Date:** 2026-02-11
**Status:** IN PROGRESS

**Problem:** The ao-frame-page border system is applied to mission.html but the SVG corner brackets and inset border lines are not rendering visibly at the corner clip-path cuts. The diagonal cut is visible (content is clipped), but the actual border strokes/lines along the cut edges are invisible or too faint. See uploaded screenshot showing top-left corner: diagonal cut is there but no visible border line along it.

**Root Cause (suspected):**
- `clip-path: polygon()` clips `box-shadow: inset` — the shadow is drawn but then the corners where it would be most visible are literally cut away
- SVG corner brackets are positioned absolutely at 240px × 240px but may be rendering behind other elements or getting clipped themselves
- The inset box-shadow border approach from the spec may fundamentally not work with clip-path corners — need a different strategy (e.g., a `::before` pseudo with matching clip-path offset inward, or actual SVG border paths that trace the full octagonal frame edge)

**What's been tried:**
- Scaled corner SVGs from 60px to 240px, stroke-width from 1-2 to 3-4
- Increased box-shadow from 1px to 3px with --ao-border-bright
- Added overflow:hidden to prevent height expansion bug
- Boosted glow from 20px to 60px with stronger opacity

**What works:**
- CSS loads properly (after adding /css mount to server/main.py)
- clip-path polygon renders correctly (80px corner cuts visible)
- Page content renders normally inside the frame
- No JS errors, data flow intact
- Hazard stripes, notches positioned correctly

**Current state of files:**
- `client/css/ao-frames.css` — 4-tier border system CSS with scaled-up page frame (80px clips, 240px corners, 3px borders)
- `client/tabs/mission.html` — wrapped in ao-frame-page div with SVG corners, hazard bars, notches; crew strip + status panel HTML deleted with JS null guards
- `server/main.py` — added /css static file mount
- `_backup_current/mission_hidden_panels.html` — safe rollback point (display:none version, pre-border work)

**Next steps:**
- Consider replacing box-shadow border with a `::before` pseudo-element that draws an actual octagonal border path (SVG or gradient-based) instead of relying on clipped box-shadow
- Or use a full-perimeter SVG `<rect>` with the same octagonal clip applied, so the stroke follows the clipped edge
- Reference files: `ao-countdown-frames.html` and `scifi-border-variations.html` (uploaded to Claude) have working border examples
- Spec: `BORDER_IMPLEMENTATION_NOTE.md` in project root

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
