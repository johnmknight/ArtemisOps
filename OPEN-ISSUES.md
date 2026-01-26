# ArtemisOps ISS Tracker - Open Issues

*No open issues at this time.*

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
