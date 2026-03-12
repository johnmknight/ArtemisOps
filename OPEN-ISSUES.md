# ArtemisOps — Open Issues

**Last Updated:** 2026-03-12

---

## 🔴 Active Issues

### ISSUE-003 — Countdown Digit Clipping (3-Digit DAYS)

**Date:** 2026-03-07
**Severity:** Visual / Medium
**Status:** OPEN

**Problem:** When DAYS value is 3 digits (e.g. "195"), the left digit clips outside the cell boundary.
Current clamp ceilings in `.countdown-left .ao-digit-cell` were tuned for 2-digit numbers.
SpaceX CRS-33 is 195 days elapsed; Artemis missions will count down from 300+ days.

**Affected file:** `client/tabs/mission.html` — `.countdown-left .ao-digit-cell` / `.ao-digit-value` clamps
**Root cause:** vh-based clamp values give cells enough height but the 3-digit DAYS box needs
a `.wide` variant or font-size scaling that backs off proportionally for 3 chars vs 2.

**Fix approach:**
- Detect digit count in JS and add a `.three-digit` class to the DAYS ao-digit-frame
- Add a CSS rule that reduces font-size ~15% when `.three-digit` is present
- OR: use `font-size: min(...)` driven by character count via a CSS custom property

---

### ISSUE-004 — ISS Video Auto-Load Not Triggering in Tracking Tab

**Date:** 2026-03-07
**Severity:** UX / Low
**Status:** OPEN

**Problem:** `DOMContentLoaded` listener added to `mode3-iss-live.html` calls `ISSVideo.load()`
on page init, but the LOAD STREAM button still appears on tracking tab load.

**Suspected causes:**
1. The iframe loads in background (tracking tab is hidden on launch); DOMContentLoaded fires
   but the IBm/YouTube embed may be blocked by autoplay policies until user interaction.
2. The `DOMContentLoaded` fires before `ISSVideo` object is defined (script ordering issue).

**Affected file:** `client/mockups/mode3-iss-live.html` — bottom `<script>` block

**Fix approach:**
- Move auto-load call to end of ISSVideo definition (after object closes)
- Or: use `window.onload` with a 500ms timeout to ensure DOM is settled
- Or: accept manual load as-is (autoplay policy may require user gesture regardless)

---

### ISSUE-005 — Mission Default Selection Inconsistent

**Date:** 2026-03-07
**Severity:** UX / Medium
**Status:** OPEN

**Problem:** On some reloads the shell selects SpaceX CRS-33 (195-day cargo mission) instead
of Crew-12 (active crewed mission). Sort logic picks "first active mission by launch_date
ascending" — CRS-33 was launched before Crew-12 and both have status "Go"/"In Flight".

**Fix approach:**
- Add a `priority` or `crewed` field to mission data
- Prefer crewed missions over cargo when selecting default
- Or: sort by most-recently-launched active mission (descending launch_date)

---

---



### DEFERRED-001 — Info Tab Development Paused

**Date:** 2026-03-07
**Status:** PAUSED — code preserved, removed from navigation

**Action taken:**
- `info` removed from `tabOrder` in `index-shell.html`
- `frame-info` iframe commented out (not removed)
- `client/tabs/info.html` untouched
- Shell `sendDataToTab` 'info' case left intact

**Resumption:** Re-add `'info'` to `tabOrder` array and uncomment iframe to restore.

---

### DEFERRED-002 — Tracking Tab Theme Wiring

**Date:** 2026-03-07
**Status:** DEFERRED

**Context:** `tracking.html` is a thin wrapper that embeds `mode3-iss-live.html` as a full-screen
iframe. The mockup has its own hardcoded color system and doesn't reference ao-themes.css tokens.
Direct wiring would require refactoring the mockup's color scheme.

**Resumption:** Pass theme name via postMessage to the inner iframe; add a theme-switch handler
inside mode3-iss-live.html that swaps CSS custom properties on `document.documentElement`.

---

## ✅ Closed Issues

### CLOSED-006 — Tracking Page Map Not Filling Available Screen Space

**Date:** 2026-03-07  **Closed:** 2026-03-12
**Resolution:** Map verified filling available space at 1573×781 viewport with NASA GIBS Blue Marble
tiles, ISS position overlay, orbit track, and footprint circle all rendering correctly.
No layout constraints found. Issue closed as not reproducible at current viewport.

### CLOSED-001 — Page Frame Border Not Visible at Corners (Mission Page)

**Date:** 2026-02-11  **Closed:** 2026-03-06
**Fix:** Double clip-path layer technique in ao-frames.css. Outer layer = border color background;
inner `::before` = dark fill; 2px gap between clips IS the border. No box-shadow required.

---

### CLOSED-002 — ISS Solar Array X-Pattern Bug

**Date:** 2026-01-26  **Closed:** 2026-01-26
**Resolution:** Not a bug. Port/starboard SARJ joints operate independently per NASA telemetry.
X-pattern is correct behavior when telemetry values differ.

---

### CLOSED-003 — Mission Data Not Rendering (postMessage Type Mismatch)

**Date:** 2026-03-07  **Closed:** 2026-03-07
**Fix:** Shell sends `type: 'setMissionData'`; mission.html was listening for `type: 'missionData'`.
Updated mission.html handler to accept both forms. Weather data handler patched to match same pattern.

---

### CLOSED-004 — Mission Layout Off-Screen (CSS Specificity Bug)

**Date:** 2026-03-07  **Closed:** 2026-03-07
**Fix:** `ao-frames.css` rule `> *:not(.ao-corner):not(.ao-hazard)...` was forcing `.ao-page-border`
SVG into normal flow (902px height), pushing `.mission-layout` below viewport.
Added `.ao-page-border` to the exclusion list so the SVG stays `position: absolute`.
