# Crew Tab — Feature List

**File:** `client/tabs/crew.html`
**Last Updated:** February 7, 2026

---

## ✅ Completed

### Layout & Cards
- [x] 4-column responsive grid (supports 2–9 crew members)
- [x] Uniform card height via CSS grid (`grid-template-rows: 1fr auto`)
- [x] Portrait photos with `object-fit: cover` cropping
- [x] Name, role, and bio text in info panel below photo
- [x] Bio text clamped to 5 lines (`-webkit-line-clamp`)
- [x] All portraits and bio panels aligned identically across cards

### Data Source
- [x] Crew data sourced from NASA "Our Artemis Crew" page
- [x] Official JSC Artemis II portraits (jsc2023e0016433–0016436)
- [x] Bios derived from individual NASA/CSA astronaut bio pages
- [x] Bio URLs link to official NASA/CSA pages
- [x] Fallback data in `server/fetcher.py` prevents API overwrites

### EVA Mode
- [x] Normal mode: crew grid (+ optional EVA sidebar when EVA data present)
- [x] EVA active mode: 3-column layout (IVA crew / live feed / EVA crew + timeline)
- [x] EVA elapsed timer with auto-refresh
- [x] EVA sidebar hidden when no scheduled EVAs in system
- [x] Mock EVA data preserved for development testing

### Navigation
- [x] Keyboard forwarding to parent shell (←/→, 0–4, F, F11)
- [x] Receives crew data via postMessage from index-shell

---

## 🔲 Backlog

### Polish
- [x] **Agency badges** — Colored dot + agency name (NASA/CSA/ESA/JAXA/etc) above crew name
- [x] **Bio link** — Clickable "Full bio ↗" link to official NASA/CSA bio page
- [x] **Loading skeleton** — Animated shimmer placeholder cards (4-column grid)
- [x] **Error state** — Astronaut emoji + message + hint when crew data unavailable
- [x] **Photo URL fix** — Cards now use `photo_url` field (was incorrectly using `photo`)

### Features
- [ ] **Card hover/click detail** — Expand card or show modal with full bio, flight history, social links
- [ ] **Agency logo in card header** — Small NASA/CSA logo next to role text
- [ ] **Flight stats** — Days in space, number of EVAs, missions flown (data partially available)
- [ ] **Social media links** — Instagram/X handles (available on NASA crew page)

### Mission Control Mode (Phase 5)
- [ ] **Crew photo strip** — Horizontal compact crew display for kiosk mode (per PRODUCTION_QUEUE.md)

---

## Notes

- Crew data flows: Space Devs API → `fetcher.py` → SQLite → `/api/missions/{id}` → shell → iframe postMessage
- For Artemis II, sync always uses curated fallback (API bios are inconsistent)
- EVA mode activates automatically when an EVA status is set to `"active"`
- Portrait `object-position: center 20%` works well for all four official JSC photos
