# ISS Solar Array Rotation - Technical Documentation

## Overview

This document captures the tests, iterations, and learnings from implementing accurate ISS solar array rotation in the ArtemisOps 3D visualization using the NASA IGOAL model.

---

## ISS Solar Array Rotation System

The ISS Electrical Power System (EPS) uses two types of rotary joints to track the sun:

### SARJ (Solar Alpha Rotary Joint)
- **Purpose**: Rotates the entire solar array wing around the station truss axis
- **Location**: Where P4/P6 truss segments meet (port side) and S4/S6 (starboard side)
- **Motion**: "Windmill" sweep - arrays rotate like clock hands when viewed from port/starboard
- **Speed**: Completes one 360° revolution per orbit (~92 minutes)
- **Range**: Continuous 360° rotation

### BGA (Beta Gimbal Assembly)
- **Purpose**: Tilts individual solar array panels toward/away from the sun
- **Location**: Base of each solar array "blanket box"
- **Motion**: Panel tilt - adjusts for sun elevation angle (beta angle)
- **Speed**: Slower adjustments for seasonal sun angle changes
- **Range**: Typically ±90° tilt

---

## NASA IGOAL Model Joint Hierarchy

The IGOAL (ISS Generic Operational Assembly Language) 3D model includes dedicated rotation joints:

### SARJ Joints (Alpha Rotation)
| Joint Name | Description |
|------------|-------------|
| `PORT_ALPHA_ROT` | Port side SARJ - rotates all port arrays together |
| `STBD_ALPHA_ROT` | Starboard side SARJ - rotates all starboard arrays together |

### BGA Joints (Beta Rotation)
| Joint Name | Array | Side |
|------------|-------|------|
| `PORT_BETA_ROT_2A` | Array 2A | Port Inboard |
| `PORT_BETA_ROT_4A` | Array 4A | Port Outboard |
| `PORT_BETA_ROT_2B` | Array 2B | Port Inboard |
| `PORT_BETA_ROT_4B` | Array 4B | Port Outboard |
| `STBD_BETA_ROT_1A` | Array 1A | Starboard Inboard |
| `STBD_BETA_ROT_3A` | Array 3A | Starboard Outboard |
| `STBD_BETA_ROT_1B` | Array 1B | Starboard Inboard |
| `STBD_BETA_ROT_3B` | Array 3B | Starboard Outboard |

---

## Test History & Learnings

### Test 1: Initial Implementation (Wrong)
**Approach**: Rotated individual mesh objects on X/Z axes
**Result**: Arrays moved incorrectly, not matching real ISS behavior
**Learning**: Need to use the model's built-in joint hierarchy, not individual meshes

### Test 2: Using Proper Joint Nodes
**Approach**: Located `PORT_ALPHA_ROT`, `STBD_ALPHA_ROT`, and `*_BETA_ROT_*` joints
**Test Command**:
```javascript
model.traverse(child => {
  if (child.name === 'PORT_ALPHA_ROT') portSARJ = child;
  if (child.name === 'STBD_ALPHA_ROT') stbdSARJ = child;
  if (child.name.startsWith('PORT_BETA_ROT_')) portBGA.push(child);
  if (child.name.startsWith('STBD_BETA_ROT_')) stbdBGA.push(child);
});
```
**Result**: Found correct joints in model hierarchy
**Learning**: IGOAL model has dedicated rotation joints already set up

### Test 3: SARJ on Z-Axis
**Approach**: `joints.portSARJ.rotation.z = angle`
**Result**: Arrays tilted incorrectly - pitched up/down rather than sweeping
**Learning**: Z-axis was wrong for SARJ in this model's coordinate system


### Test 4: SARJ on X-Axis
**Approach**: `joints.portSARJ.rotation.x = angle` (45°)
**Test Command**:
```javascript
// Reset all rotations first
joints.portSARJ.rotation.set(0, 0, 0);
joints.stbdSARJ.rotation.set(0, 0, 0);

// Test SARJ on X axis
joints.portSARJ.rotation.x = Math.PI / 4;  // 45 degrees
joints.stbdSARJ.rotation.x = -Math.PI / 4;
```
**Result**: Arrays moved but motion was incorrect - not the windmill sweep
**Learning**: X-axis was also wrong

### Test 5: SARJ on Y-Axis ✅ CORRECT
**Approach**: `joints.portSARJ.rotation.y = angle` (45°)
**Test Command**:
```javascript
// Reset all
joints.portSARJ.rotation.set(0, 0, 0);
joints.stbdSARJ.rotation.set(0, 0, 0);

// Test SARJ on Y axis
joints.portSARJ.rotation.y = Math.PI / 4;  // 45 degrees
joints.stbdSARJ.rotation.y = -Math.PI / 4;
```
**Result**: ✅ Correct windmill-like sweep motion!
**Learning**: **SARJ rotates on Y-axis** in the IGOAL model coordinate system

### Test 6: BGA on Y-Axis (Wrong)
**Approach**: `joints.portBGA.forEach(j => j.rotation.y = angle)`
**Result**: Panels rotated around wrong axis - twisted rather than tilted
**Learning**: Y-axis was wrong for BGA

### Test 7: BGA on X-Axis ✅ CORRECT
**Approach**: `joints.portBGA.forEach(j => j.rotation.x = angle)` (30°)
**Test Command**:
```javascript
// Reset SARJ, test BGA
joints.portSARJ.rotation.set(0, 0, 0);
joints.stbdSARJ.rotation.set(0, 0, 0);
joints.portBGA.forEach(j => j.rotation.set(0, 0, 0));
joints.stbdBGA.forEach(j => j.rotation.set(0, 0, 0));

// Test BGA on X axis
const bgaAngle = Math.PI / 6; // 30 degrees
joints.portBGA.forEach(j => j.rotation.x = bgaAngle);
joints.stbdBGA.forEach(j => j.rotation.x = bgaAngle);
```
**Result**: ✅ Correct panel tilt motion - arrays angle toward/away from sun!
**Learning**: **BGA rotates on X-axis** in the IGOAL model coordinate system

---

## Final Correct Implementation

### Rotation Axes Summary
| Joint Type | Three.js Axis | Motion Description |
|------------|---------------|-------------------|
| **SARJ** | `rotation.y` | Windmill sweep (like clock hands) |
| **BGA** | `rotation.x` | Panel tilt (toward/away from sun) |

### Code Implementation
```javascript
// Update solar array rotations based on telemetry
function updateSolarArrays() {
  // Convert telemetry angles to radians
  const sarjPortRad = (nasaTelemetry.sarjPort || 0) * Math.PI / 180;
  const sarjStbdRad = (nasaTelemetry.sarjStbd || 0) * Math.PI / 180;
  const bgaPortRad = (nasaTelemetry.bgaPort || 0) * Math.PI / 180;
  const bgaStbdRad = (nasaTelemetry.bgaStbd || 0) * Math.PI / 180;
  
  // Apply rotations to both views (nadir and velocity)
  ['nadir', 'velocity'].forEach(viewName => {
    const joints = solarJoints[viewName];
    if (!joints) return;
    
    // SARJ rotation - Y axis (windmill motion perpendicular to truss)
    if (joints.portSARJ) joints.portSARJ.rotation.y = sarjPortRad;
    if (joints.stbdSARJ) joints.stbdSARJ.rotation.y = sarjStbdRad;
    
    // BGA rotation - X axis (panel tilt)
    joints.portBGA.forEach(joint => joint.rotation.x = bgaPortRad);
    joints.stbdBGA.forEach(joint => joint.rotation.x = bgaStbdRad);
  });
}
```


---

## NASA Telemetry Data Items

The following telemetry items drive the solar array animations:

### SARJ Telemetry
| Data Item | Description | Units |
|-----------|-------------|-------|
| `P1000004` | Port SARJ position angle | Degrees |
| `S1000004` | Starboard SARJ position angle | Degrees |

### BGA Telemetry
| Data Item | Description | Units |
|-----------|-------------|-------|
| `P4000001` | Port 2A/2B BGA position | Degrees |
| `P6000001` | Port 4A/4B BGA position | Degrees |
| `S4000001` | Stbd 1A/1B BGA position | Degrees |
| `S6000001` | Stbd 3A/3B BGA position | Degrees |

---

## Test Script

A test script (`client/components/test-solar-animation.js`) provides automated testing:

### Test Phases
1. **SARJ Sweep (Port)** - 5 seconds - Sweeps port SARJ 360°
2. **SARJ Sweep (Stbd)** - 5 seconds - Sweeps starboard SARJ 360°
3. **BGA Sweep (Port)** - 5 seconds - Tilts port BGA ±90°
4. **BGA Sweep (Stbd)** - 5 seconds - Tilts starboard BGA ±90°
5. **All Arrays Sync** - 5 seconds - Sinusoidal motion all arrays
6. **Realistic Sun Tracking** - 10 seconds - Simulates actual sun tracking

### Usage
```javascript
// Load test script in browser console
const script = document.createElement('script');
script.src = '/client/components/test-solar-animation.js?' + Date.now();
document.head.appendChild(script);
```

---

## Coordinate System Notes

### IGOAL Model Orientation (as loaded)
- **X-axis**: Along velocity vector (direction of travel)
- **Y-axis**: Perpendicular to truss (up when viewed from nadir)
- **Z-axis**: Along truss (port-starboard direction)

### Nadir View
- Camera positioned below station looking up
- Arrays visible as "wings" extending port/starboard
- SARJ windmill rotation is clearly visible

### Velocity View
- Camera positioned behind station looking forward
- Good view of array tilt angles
- BGA rotation visible as arrays angle up/down

---

## Git Commits

| Commit | Description |
|--------|-------------|
| `6ebae37` | Fix solar array rotation - use proper SARJ/BGA joint nodes from IGOAL model |
| `2fb1f81` | Fix solar array rotation planes - SARJ on Y-axis, BGA on X-axis |

---

## Common Issues & Troubleshooting

### Issue: Arrays not moving
**Cause**: Joints not found in model hierarchy
**Fix**: Verify model loaded completely, check console for joint discovery log

### Issue: Arrays move wrong direction
**Cause**: Sign of angle may need inversion
**Fix**: Some arrays may need negated angles for proper mirroring

### Issue: Arrays twisting instead of tilting
**Cause**: Wrong rotation axis for BGA
**Fix**: Ensure using `rotation.x` not `rotation.y` or `rotation.z`

### Issue: Windmill motion looks like pitch/tilt
**Cause**: Wrong rotation axis for SARJ
**Fix**: Ensure using `rotation.y` not `rotation.x` or `rotation.z`

---

## References

- [NASA ISS Systems Handbook](https://www.nasa.gov/reference/iss-systems-handbook/)
- [SARJ Wikipedia](https://en.wikipedia.org/wiki/Solar_Alpha_Rotary_Joint)
- [ISS Live Telemetry](https://isslive.com/)
- Adobe Stock Reference Video: Stock #313713832 (ISS solar panel rotation animation)

---

*Last Updated: January 25, 2026*
*ArtemisOps Mission Control Application*
