# ISS Solar Array Articulation Status

**Date:** 2026-01-26  
**Status:** ✅ WORKING

## Model
- NASA ISS Stationary GLB (44.5 MB)
- Source: https://solarsystem.nasa.gov/resources/2378/international-space-station-3d-model/
- Location: `client/assets/iss-stationary.glb`

## 10 Articulated Joints

### SARJ Joints (X-axis rotation)
| Joint | Node | Axis | Telemetry Channel |
|-------|------|------|-------------------|
| Port SARJ | `20_P4_Truss` | X | S0000004 |
| Starboard SARJ | `23_S4_Truss` | X | S0000003 |

**Note:** Port and starboard SARJ operate independently. Different telemetry values will produce an X-pattern - this is correct behavior matching the real ISS.

### BGA Joints (Z-axis rotation)
| Joint | Node | Axis | Notes |
|-------|------|------|-------|
| P4 Wing 1 (4B) | `20_P4_Truss_01` | Z | Normal |
| P4 Wing 2 (2B) | `20_P4_Truss_02` | Z | **Negated** |
| P6 Wing 1 (4A) | `08_P6_Truss_01` | Z | Normal |
| P6 Wing 2 (2A) | `08_P6_Truss_02` | Z | **Negated** |
| S4 Wing 1 (3B) | `23_S4_Truss_01` | Z | Normal |
| S4 Wing 2 (1B) | `23_S4_Truss_02` | Z | **Negated** |
| S6 Wing 1 (3A) | `32_S6_Truss_01` | Z | Normal |
| S6 Wing 2 (1A) | `32_S6_Truss_02` | Z | **Negated** |

## Code Implementation

```javascript
// SARJ rotation: X-axis
if (joints.portSARJ) joints.portSARJ.rotation.x = sarjPortRad;
if (joints.stbdSARJ) joints.stbdSARJ.rotation.x = sarjStbdRad;

// BGA rotation: Z-axis (_02 wings negated)
joint.node.rotation.z = sign * bgaAngle;  // sign = -1 for _02 wings
```

## Verified Behavior
- ✅ SARJ X-axis rotation matches NASA telemetry
- ✅ BGA Z-axis rotation with _02 wing negation
- ✅ Arrays parallel when telemetry values similar
- ✅ Arrays form X-pattern when telemetry values differ (correct)
- ✅ NASA Lightstreamer telemetry integration working

## Files
- `client/components/iss-tracker.html` - updateSolarArrays() function
- `client/components/test-solar-rotation.js` - Manual test script
