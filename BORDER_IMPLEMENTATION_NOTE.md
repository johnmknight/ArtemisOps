# ArtemisOps — Border Design System Implementation Note
## Target: Mission Page (Screen 1)

**Author:** Claude (for future Claude sessions)
**Date:** February 11, 2026
**Project:** C:\Users\john_\dev\ArtemisOps
**Reference files created in this session (ask John for local copies or re-download from chat):**
- `artemisops-border-system.html` — Full 4-tier design system with all CSS classes
- `ao-countdown-frames.html` — 5 countdown digit frame variants
- `scifi-border-kit.html` — 9-slice page frame proof-of-concept
- `scifi-border-variations.html` — 5 standalone SVG border style explorations

---

## 1. DESIGN SYSTEM OVERVIEW

Four tiers of border frames, each with decreasing visual weight:

| Tier | CSS Class | Used For | Key Features |
|------|-----------|----------|--------------|
| 1 — Page | `.ao-frame-page` | Full screen wrapper (one per view) | Cut-corner clip-path, SVG corner brackets, hazard stripes, side notches, scanline overlay |
| 2 — Panel | `.ao-frame-panel` | Major content areas (countdown center, weather sidebar, timeline) | Subtle corner clips, bright top-edge accent, corner pin dots, header bar |
| 3 — Sub | `.ao-frame-sub` | Individual readouts (GO/NOGO indicators, weather stats, milestone items) | Thin border, left-edge status stripe (.nominal/.caution/.alert), corner tick |
| 4 — Popup | `.ao-frame-popup` | Settings gear, tooltips, overlays | Solid bg, floating tab label, drop shadow. Variants: default/warning/alert |
| Special | `.ao-digit-frame` | Countdown digit cells | Recessed panel, integrated label tab, corner accents, glow |

---

## 2. DESIGN TOKENS (CSS CUSTOM PROPERTIES)

All borders reference these tokens. Add to a shared `ao-frames.css` or top of `mission.html`:

```css
:root {
  /* Core palette */
  --ao-bg-deep:       #060a10;
  --ao-bg-panel:      rgba(8, 14, 24, 0.85);
  --ao-bg-sub:        rgba(12, 20, 32, 0.7);
  --ao-bg-popup:      rgba(10, 16, 28, 0.95);

  /* Border colors — nominal cyan */
  --ao-border-bright: #88ccff;
  --ao-border-mid:    #4a80aa;
  --ao-border-dim:    #1e3348;
  --ao-border-faint:  rgba(30, 51, 72, 0.5);

  /* Glow */
  --ao-glow:          rgba(100, 180, 255, 0.25);
  --ao-glow-strong:   rgba(136, 204, 255, 0.4);

  /* Status accents */
  --ao-nominal:       #44dd88;
  --ao-caution:       #ddaa44;
  --ao-alert:         #dd4455;

  /* Countdown cyan (more green-cyan than panel blue-cyan) */
  --ao-cyan:          #00f0d4;
  --ao-cyan-mid:      #00c4ad;
  --ao-cyan-dim:      #0a8a7a;
  --ao-cyan-glow:     rgba(0, 240, 212, 0.35);

  /* Corner geometry per tier */
  --ao-clip-page:     20px;
  --ao-clip-panel:    12px;
  --ao-clip-sub:      6px;
  --ao-clip-popup:    8px;

  /* Fonts (already in use — host locally for kiosk) */
  --ao-font-mono:     'Space Mono', monospace;
  --ao-font-sans:     'IBM Plex Sans', sans-serif;

  /* Scanline overlay */
  --ao-scanline: repeating-linear-gradient(
    0deg,
    transparent 0px, transparent 2px,
    rgba(136, 204, 255, 0.012) 2px,
    rgba(136, 204, 255, 0.012) 4px
  );
}
```

---

## 3. MISSION PAGE LAYOUT + BORDER MAPPING

Current Mission page structure (from mockup v9 and production `tabs/mission.html`):

```
┌─────────────────────────────────────────────────────────────────────┐
│ ao-frame-page                                                       │
│ ┌───────────┬───────────────────────────────────────┬─────────────┐ │
│ │           │                                       │             │ │
│ │ ao-frame  │  COUNTDOWN CENTER                     │ ao-frame    │ │
│ │ -panel    │  ┌─────────────────────────────────┐  │ -panel      │ │
│ │           │  │ ao-countdown-label               │  │             │ │
│ │ GO/NOGO   │  │ "T-MINUS · COUNTDOWN TO LAUNCH" │  │ [NASA LOGO] │ │
│ │ STATUS    │  ├─────────────────────────────────┤  │             │ │
│ │           │  │ ao-digit-frame x4 + separators  │  │ [MISSION    │ │
│ │ ┌───────┐ │  │ DAYS : HOURS : MIN : SEC        │  │  PATCH]     │ │
│ │ │ao-sub │ │  └─────────────────────────────────┘  │             │ │
│ │ │Weather│ │                                       │             │ │
│ │ │.nomi- │ │  ┌──────────────┬──────────────────┐  │             │ │
│ │ │nal   │ │  │ ao-frame-sub │ ao-frame-sub     │  │             │ │
│ │ ├───────┤ │  │ Next Mile-   │ Weather at KSC   │  │             │ │
│ │ │ao-sub │ │  │ stone        │ Clear · 78°F     │  │             │ │
│ │ │Range  │ │  └──────────────┴──────────────────┘  │             │ │
│ │ │.nomi- │ │                                       │             │ │
│ │ │nal   │ │  Launch Info: Date / Time / Location   │             │ │
│ │ ├───────┤ │                                       │             │ │
│ │ │ao-sub │ │                                       │             │ │
│ │ │Vehic. │ │                                       │             │ │
│ │ │.nomi- │ │                                       │             │ │
│ │ │nal   │ │                                       │             │ │
│ │ ├───────┤ │                                       │             │ │
│ │ │ao-sub │ │                                       │             │ │
│ │ │Crew   │ │                                       │             │ │
│ │ │.nomi- │ │                                       │             │ │
│ │ │nal   │ │                                       │             │ │
│ │ └───────┘ │                                       │             │ │
│ └───────────┴───────────────────────────────────────┴─────────────┘ │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ ao-frame-panel — TIMELINE STRIP                                 │ │
│ │ ✓ FRR  ✓ Quarantine  ● Vehicle Checks  ○ Rollout  ○ LIFTOFF   │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ NEWS TICKER (scrolling, thin bar — no frame needed, or minimal)│ │
│ └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Border Assignment Summary

| Element | Border Class | Status Class | Notes |
|---------|-------------|-------------|-------|
| Whole Mission screen | `ao-frame-page` | — | Includes 4 SVG corners, hazard bars, notches |
| GO/NOGO sidebar | `ao-frame-panel` | — | Header: "▸ Status" with badge |
| Each GO/NOGO indicator | `ao-frame-sub` | `.nominal` / `.caution` / `.alert` | Left-stripe shows status color |
| Countdown center area | No frame (lives directly in page) | — | The digit frames ARE the visual treatment |
| Each countdown digit cell | `ao-digit-frame` + `ao-digit-cell` | — | Use "Default" or "Heavy" variant |
| Days cell specifically | `ao-digit-frame wide` | — | Extra width for 3-digit |
| Colon separators | `ao-digit-sep` > `.dot` x2 | — | Pulsing animation |
| Next Milestone info box | `ao-frame-sub` | — | No status stripe needed |
| Weather at KSC info box | `ao-frame-sub` | `.nominal` | Green stripe when GO |
| Timeline strip | `ao-frame-panel` | — | Thin horizontal, minimal header |
| News ticker | None or `ao-frame-sub` | — | Keep minimal to avoid visual clutter |
| Settings popup (gear icon) | `ao-frame-popup` | — | Floating tab label "Settings" |

---

## 4. SVG CORNER BRACKET IMPLEMENTATION

The page frame uses 4 inline SVGs positioned absolutely at each corner. These are lightweight and self-contained (no external files needed).

### Corner SVG Template (Top-Left):
```html
<div class="ao-corner tl">
  <svg viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg" fill="none">
    <path d="M 60,8 L 20,8 L 8,20 L 8,60" stroke="var(--ao-border-mid)" stroke-width="1"/>
    <path d="M 60,8 L 20,8 L 8,20 L 8,40" stroke="var(--ao-border-bright)" stroke-width="2" opacity="0.9"/>
    <circle cx="20" cy="20" r="2" fill="var(--ao-border-bright)" opacity="0.8"/>
    <circle cx="20" cy="20" r="4" fill="var(--ao-border-bright)" opacity="0.15"/>
  </svg>
</div>
```

Other corners mirror this — flip the path coordinates:
- **TR:** `M 0,8 L 40,8 L 52,20 L 52,60` (and bright path to 52,40)
- **BL:** `M 8,0 L 8,40 L 20,52 L 60,52` (and bright path from 8,20)
- **BR:** `M 52,0 L 52,40 L 40,52 L 0,52` (and bright path from 52,20)

Corner vertex dot positions: TL(20,20) TR(40,20) BL(20,40) BR(40,40)

### CSS Positioning:
```css
.ao-frame-page .ao-corner {
  position: absolute;
  width: 60px;
  height: 60px;
  z-index: 12;
  pointer-events: none;
}
.ao-corner.tl { top: 0; left: 0; }
.ao-corner.tr { top: 0; right: 0; }
.ao-corner.bl { bottom: 0; left: 0; }
.ao-corner.br { bottom: 0; right: 0; }
```

**Important:** The SVGs use `currentColor` or hardcoded hex. For future theming (caution/alert page frames), swap `--ao-border-bright` and `--ao-border-mid` via a parent class.

---

## 5. CLIP-PATH STRATEGY

All tiers use the same octagonal clip-path pattern with different corner sizes:

```css
clip-path: polygon(
  VAR 0%,                    /* top-left cut */
  calc(100% - VAR) 0%,       /* top-right cut */
  100% VAR,
  100% calc(100% - VAR),
  calc(100% - VAR) 100%,     /* bottom-right cut */
  VAR 100%,                  /* bottom-left cut */
  0% calc(100% - VAR),
  0% VAR
);
```

Where VAR = `--ao-clip-page` (20px), `--ao-clip-panel` (12px), `--ao-clip-sub` (6px), `--ao-clip-popup` (8px).

**Gotcha:** `clip-path` kills `border` and `border-radius`. Borders are faked using:
- `box-shadow: inset 0 0 0 Npx color` for solid border simulation
- `::before` pseudo-element with matching clip-path for glow effects
- `::after` for scanline overlay or accent lines

---

## 6. COUNTDOWN DIGIT FRAME — DETAILED STRUCTURE

Each digit cell is a layered stack:

```
Layer 1 (z:1)  — .ao-digit-bg      Outer border + background gradient
Layer 2 (z:2)  — .ao-digit-recess  Inner recessed darker panel (inset 6px)
Layer 3 (z:3)  — .ao-digit-corner  4x corner accent marks (TL/TR/BL/BR)
Layer 4 (z:4)  — .ao-digit-value   The actual digit text
Layer 5 (z:5)  — .ao-digit-label   "DAYS" / "HOURS" / "MIN" / "SEC"
```

### HTML for one digit group:
```html
<div class="ao-digit-frame">          <!-- or .ao-digit-frame.wide for days -->
  <div class="ao-digit-cell">
    <div class="ao-digit-bg"></div>
    <div class="ao-digit-recess"></div>
    <div class="ao-digit-corner tl"></div>
    <div class="ao-digit-corner tr"></div>
    <div class="ao-digit-corner bl"></div>
    <div class="ao-digit-corner br"></div>
    <div class="ao-digit-value" data-unit="hours">03</div>
  </div>
  <div class="ao-digit-label">Hours</div>
</div>
```

### Separator between groups:
```html
<div class="ao-digit-sep">
  <div class="dot"></div>
  <div class="dot"></div>
</div>
```

### Variant Recommendations:
- **Mission page (main kiosk view):** Use "Heavy" variant (`.ao-countdown.heavy`) — maximum visual impact from distance
- **Crew page EVA countdown:** Use "Minimal" variant (`.ao-countdown.minimal`) — secondary importance, less visual weight
- **Settings/overlay countdown:** Use "Default" — balanced

### Key Sizing (responsive via clamp):
```css
.ao-digit-cell {
  width: clamp(100px, 18vw, 220px);    /* standard */
  height: clamp(90px, 15vw, 180px);
}
.ao-digit-frame.wide .ao-digit-cell {
  width: clamp(140px, 24vw, 300px);    /* days (3-digit) */
}
.ao-digit-value {
  font-size: clamp(42px, 10vw, 110px);
}
```

John's design intent: "largest possible countdown clock while maintaining correct space for live feed panel." So on the Mission page, the countdown should fill the available vertical space. Use `vh` units or dynamic sizing to maximize digit height.

---

## 7. IMPLEMENTATION STEPS

### Step 1: Create the CSS file
Create `client/css/ao-frames.css` with all tier styles + design tokens + countdown digit styles.

### Step 2: Add to index.html
```html
<link rel="stylesheet" href="css/ao-frames.css">
```

### Step 3: Wrap Mission page content
In `client/tabs/mission.html`, wrap the entire view in:
```html
<div class="ao-frame-page">
  <div class="ao-corner tl"><!-- SVG --></div>
  <div class="ao-corner tr"><!-- SVG --></div>
  <div class="ao-corner bl"><!-- SVG --></div>
  <div class="ao-corner br"><!-- SVG --></div>
  <div class="ao-hazard top"></div>
  <div class="ao-hazard bottom"></div>
  <div class="ao-notch left"></div>
  <div class="ao-notch right"></div>

  <!-- existing mission page content, wrapped in panels -->
</div>
```

### Step 4: Wrap major sections in ao-frame-panel
Each major content block (status sidebar, countdown area, timeline) gets:
```html
<div class="ao-frame-panel">
  <span class="ao-pin tl"></span>
  <span class="ao-pin tr"></span>
  <span class="ao-pin bl"></span>
  <span class="ao-pin br"></span>
  <div class="ao-panel-inner">
    <div class="ao-panel-header">
      <span class="ao-panel-title">▸ Section Title</span>
      <span class="ao-panel-badge nominal">Status</span>
    </div>
    <!-- content -->
  </div>
</div>
```

### Step 5: Replace countdown digit containers
Swap the existing `.countdown-segment` divs with the `ao-digit-frame` structure. Keep the existing JS countdown logic — it just needs to target `[data-unit="days"]` etc. instead of `#days`.

### Step 6: Apply ao-frame-sub to data readouts
Each GO/NOGO indicator, weather stat, and milestone item gets:
```html
<div class="ao-frame-sub nominal">
  <div class="ao-sub-label">Weather</div>
  <div class="ao-sub-value"><span class="status-dot nominal"></span>GO</div>
</div>
```

### Step 7: Test at kiosk resolution
The design is built for large display viewing. Test at:
- 1920×1080 (standard kiosk)
- 2560×1440 (ultrawide)
- 3840×2160 (4K display)
Verify countdown digits scale properly via clamp() and that clip-paths render cleanly.

---

## 8. GOTCHAS & EDGE CASES

1. **clip-path + overflow:** Elements with clip-path will clip children. SVG corners, hazard bars, and notches must be INSIDE the clipped element or positioned via siblings.

2. **Kiosk font loading:** Fonts must be hosted locally (no Google CDN). The .woff2 files for Space Mono and IBM Plex Sans should already be in the project — verify at `client/fonts/`.

3. **Scanline overlay:** The `::after` pseudo on `ao-frame-page` has `pointer-events: none` but `z-index: 11`. Make sure interactive elements inside have `position: relative; z-index: 12+` or they won't be clickable.

4. **Status dot animation:** The `@keyframes pulse` for `.status-dot` and `@keyframes sep-pulse` for countdown separators may conflict if both are defined. Use distinct names.

5. **Existing countdown CSS:** The current `mission.html` has its own countdown styles (`.countdown-value`, `.countdown-unit`, etc.). These need to be retired or namespaced to avoid conflicts. Don't delete them until the new system is verified.

6. **Dark-on-dark contrast:** The `ao-frame-sub` border is very subtle by design. On some displays it may be invisible. The left status stripe provides the primary visual boundary — this is intentional.

7. **9-slice approach was explored but NOT used:** The earlier session explored cutting the page frame into 8 SVG tiles for responsive tiling. This was deferred in favor of CSS clip-path + pseudo-element borders, which are simpler and sufficient since the page frame doesn't need to tile — it just needs to fill the viewport. The 9-slice kit exists as `scifi-border-kit.html` if revisited.

---

## 9. FILES IN THIS SESSION TO RETRIEVE

Ask John to provide or re-download from the Claude.ai chat:

| File | Contains | Priority |
|------|----------|----------|
| `artemisops-border-system.html` | Complete 4-tier CSS design system with all classes, tokens, and demo layouts | **CRITICAL** — extract CSS into `ao-frames.css` |
| `ao-countdown-frames.html` | 5 countdown digit variants with live ticking | **CRITICAL** — extract chosen variant CSS |
| `scifi-border-kit.html` | 9-slice proof of concept (not used but archived) | Low |
| `scifi-border-variations.html` | 5 SVG style explorations | Reference only |
| `scifi-border.svg` | Single standalone SVG border | Reference only |

---

## 10. WHAT SUCCESS LOOKS LIKE

When complete, the Mission page should have:
- A visible octagonal page frame with glowing cyan corners that says "mission control"
- The countdown digits sitting in recessed, individually-framed cells with integrated labels
- GO/NOGO indicators with colored left-edge stripes that change with status
- The timeline strip in its own panel frame with a bright top accent
- Everything scaling cleanly from 1080p to 4K without distortion
- No visual regression on Tracking, Crew, or Info pages (those get borders in a subsequent pass)
