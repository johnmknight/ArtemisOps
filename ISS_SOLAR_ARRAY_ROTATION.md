# ISS Solar Array Rotation System

## Overview

The ISS solar arrays use a two-axis rotation system to track the sun. The port and starboard SARJ joints operate **independently** - they can be at different angles.

## Physical Mechanics

### SARJ (Solar Alpha Rotary Joint)
- Located between P3/P4 and S3/S4 truss segments
- Rotates the outboard truss sections around the main truss axis
- Port and starboard operate independently
- Each completes approximately one 360° rotation per orbit (~90 minutes)

### BGA (Beta Gimbal Assembly)
- Each array wing has its own BGA
- Rotates individual panels around the boom axis
- Adjusts for seasonal beta angle changes

## IGOAL Model Implementation

### Rotation Axes
| Joint | Axis | Notes |
|-------|------|-------|
| SARJ | X | Port and starboard independent |
| BGA | Z | _02 wings negated for mirror geometry |

### Joint Hierarchy
```
ISS Model
├── 20_P4_Truss (Port SARJ) ─── rotation.x
│   ├── 20_P4_Truss_01 (4B BGA) ─── rotation.z
│   └── 20_P4_Truss_02 (2B BGA) ─── rotation.z (negated)
├── 08_P6_Truss
│   ├── 08_P6_Truss_01 (4A BGA) ─── rotation.z
│   └── 08_P6_Truss_02 (2A BGA) ─── rotation.z (negated)
├── 23_S4_Truss (Stbd SARJ) ─── rotation.x
│   ├── 23_S4_Truss_01 (3B BGA) ─── rotation.z
│   └── 23_S4_Truss_02 (1B BGA) ─── rotation.z (negated)
└── 32_S6_Truss
    ├── 32_S6_Truss_01 (3A BGA) ─── rotation.z
    └── 32_S6_Truss_02 (1A BGA) ─── rotation.z (negated)
```

## NASA Telemetry Channels

### SARJ (Alpha Rotation)
- `S0000004` - Port SARJ angle (degrees)
- `S0000003` - Starboard SARJ angle (degrees)

### BGA (Beta Gimbal)
- `P4000007` - Port 2A BGA angle
- `P4000008` - Port 4A BGA angle  
- `S4000007` - Starboard 1A BGA angle
- `S4000008` - Starboard 3A BGA angle

## Visual Behavior

| Telemetry State | Visual Result |
|-----------------|---------------|
| Port ≈ Starboard SARJ | Arrays appear parallel |
| Port ≠ Starboard SARJ | Arrays form X-pattern |

Both are **correct** - the real ISS SARJ joints operate independently.

## Code Location
- Main: `client/components/iss-tracker.html` - `updateSolarArrays()`
- Test: `client/components/test-solar-rotation.js`

## Revision History
- 2026-01-26: Confirmed X-axis for SARJ, Z-axis for BGA
- 2026-01-26: Verified X-pattern is correct when telemetry differs
