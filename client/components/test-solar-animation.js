/**
 * Solar Array Animation Test Script
 * 
 * Run this in the browser console on the ISS Tracker page to test
 * solar array animations with simulated telemetry data.
 * 
 * Usage: Copy/paste into console or load via script tag
 */

(function() {
  console.log('🛰️ Solar Array Animation Test Starting...');
  
  // Check if we have access to the telemetry objects
  if (typeof nasaTelemetry === 'undefined') {
    console.error('❌ nasaTelemetry not found - are you on the ISS Tracker page?');
    return;
  }
  
  if (typeof updateSolarArrays === 'undefined') {
    console.error('❌ updateSolarArrays function not found');
    return;
  }
  
  // Test configuration
  const config = {
    duration: 30000,      // Total test duration (ms)
    updateInterval: 100,  // Update rate (ms)
    sarjSpeed: 2,         // Degrees per update for SARJ
    bgaSpeed: 1.5,        // Degrees per update for BGA
    sarjRange: [-180, 180],
    bgaRange: [-90, 90]
  };
  
  // Animation state
  let startTime = Date.now();
  let animationId = null;
  let testPhase = 0;
  
  // Test phases
  const phases = [
    { name: 'SARJ Sweep (Port)', duration: 5000, 
      animate: (t) => ({ sarjPort: t * 360 - 180, sarjStbd: 0, bgaPort: 0, bgaStbd: 0 }) },
    { name: 'SARJ Sweep (Stbd)', duration: 5000,
      animate: (t) => ({ sarjPort: 0, sarjStbd: t * 360 - 180, bgaPort: 0, bgaStbd: 0 }) },
    { name: 'BGA Sweep (Port)', duration: 5000,
      animate: (t) => ({ sarjPort: 0, sarjStbd: 0, bgaPort: t * 180 - 90, bgaStbd: 0 }) },
    { name: 'BGA Sweep (Stbd)', duration: 5000,
      animate: (t) => ({ sarjPort: 0, sarjStbd: 0, bgaPort: 0, bgaStbd: t * 180 - 90 }) },
    { name: 'All Arrays Sync', duration: 5000,
      animate: (t) => ({ 
        sarjPort: Math.sin(t * Math.PI * 4) * 180, 
        sarjStbd: Math.sin(t * Math.PI * 4) * 180,
        bgaPort: Math.cos(t * Math.PI * 4) * 90,
        bgaStbd: Math.cos(t * Math.PI * 4) * 90
      }) },
    { name: 'Realistic Sun Tracking', duration: 10000,
      animate: (t) => ({
        // Simulate realistic sun tracking - SARJ rotates continuously, BGA adjusts seasonally
        sarjPort: (t * 360 * 2) % 360 - 180,  // ~4° per second like real ISS
        sarjStbd: (t * 360 * 2) % 360 - 180,
        bgaPort: Math.sin(t * Math.PI * 2) * 45,  // Seasonal beta adjustment
        bgaStbd: Math.sin(t * Math.PI * 2) * 45
      }) }
  ];
  
  // Calculate total duration
  const totalDuration = phases.reduce((sum, p) => sum + p.duration, 0);
  
  // Create status display
  const statusDiv = document.createElement('div');
  statusDiv.id = 'solar-test-status';
  statusDiv.style.cssText = `
    position: fixed;
    top: 60px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0, 20, 40, 0.95);
    border: 2px solid #00bcd4;
    border-radius: 8px;
    padding: 15px 25px;
    color: #00d4ff;
    font-family: 'Courier New', monospace;
    font-size: 14px;
    z-index: 10000;
    min-width: 400px;
    box-shadow: 0 4px 20px rgba(0, 188, 212, 0.3);
  `;
  statusDiv.innerHTML = `
    <div style="font-size: 16px; font-weight: bold; margin-bottom: 10px; color: #7ed321;">
      🛰️ SOLAR ARRAY ANIMATION TEST
    </div>
    <div id="test-phase" style="margin: 5px 0;">Phase: Initializing...</div>
    <div id="test-progress" style="margin: 5px 0;">Progress: 0%</div>
    <div id="test-values" style="margin: 10px 0; font-size: 12px; color: #aaa;">
      <div>Port SARJ: <span id="tv-sarjP">--</span>° | Stbd SARJ: <span id="tv-sarjS">--</span>°</div>
      <div>Port BGA: <span id="tv-bgaP">--</span>° | Stbd BGA: <span id="tv-bgaS">--</span>°</div>
    </div>
    <div style="margin-top: 10px;">
      <button id="test-stop" style="
        background: #ff4444;
        border: none;
        color: white;
        padding: 5px 15px;
        border-radius: 4px;
        cursor: pointer;
        margin-right: 10px;
      ">Stop Test</button>
      <button id="test-pause" style="
        background: #ffaa00;
        border: none;
        color: black;
        padding: 5px 15px;
        border-radius: 4px;
        cursor: pointer;
      ">Pause</button>
    </div>
  `;
  document.body.appendChild(statusDiv);
  
  let isPaused = false;
  let pauseTime = 0;
  
  document.getElementById('test-stop').onclick = stopTest;
  document.getElementById('test-pause').onclick = () => {
    isPaused = !isPaused;
    document.getElementById('test-pause').textContent = isPaused ? 'Resume' : 'Pause';
    if (isPaused) {
      pauseTime = Date.now();
    } else {
      startTime += (Date.now() - pauseTime);
    }
  };
  
  function updateStatus(phase, progress, values) {
    document.getElementById('test-phase').textContent = `Phase: ${phase}`;
    document.getElementById('test-progress').innerHTML = `
      Progress: ${(progress * 100).toFixed(0)}%
      <div style="background: #1a3a5c; height: 6px; border-radius: 3px; margin-top: 5px;">
        <div style="background: #00bcd4; height: 100%; width: ${progress * 100}%; border-radius: 3px;"></div>
      </div>
    `;
    document.getElementById('tv-sarjP').textContent = values.sarjPort.toFixed(1);
    document.getElementById('tv-sarjS').textContent = values.sarjStbd.toFixed(1);
    document.getElementById('tv-bgaP').textContent = values.bgaPort.toFixed(1);
    document.getElementById('tv-bgaS').textContent = values.bgaStbd.toFixed(1);
  }
  
  function applyValues(values) {
    // Update nasaTelemetry state
    nasaTelemetry.sarjPort = values.sarjPort;
    nasaTelemetry.sarjStbd = values.sarjStbd;
    nasaTelemetry.bgaPort2A = values.bgaPort;
    nasaTelemetry.bgaPort4A = values.bgaPort;
    nasaTelemetry.bgaStbd1A = values.bgaStbd;
    nasaTelemetry.bgaStbd3A = values.bgaStbd;
    
    // Update UI displays
    const sarjPortEl = document.getElementById('telSARJPort');
    const sarjStbdEl = document.getElementById('telSARJStbd');
    const bgaPortEl = document.getElementById('telBGAPort');
    const bgaStbdEl = document.getElementById('telBGAStbd');
    
    if (sarjPortEl) sarjPortEl.textContent = values.sarjPort.toFixed(1) + '°';
    if (sarjStbdEl) sarjStbdEl.textContent = values.sarjStbd.toFixed(1) + '°';
    if (bgaPortEl) bgaPortEl.textContent = values.bgaPort.toFixed(1) + '°';
    if (bgaStbdEl) bgaStbdEl.textContent = values.bgaStbd.toFixed(1) + '°';
    
    // Trigger 3D model update
    updateSolarArrays();
  }
  
  function animate() {
    if (isPaused) {
      animationId = requestAnimationFrame(animate);
      return;
    }
    
    const elapsed = Date.now() - startTime;
    const totalProgress = elapsed / totalDuration;
    
    if (elapsed >= totalDuration) {
      stopTest();
      return;
    }
    
    // Determine current phase
    let phaseElapsed = elapsed;
    let currentPhase = null;
    for (const phase of phases) {
      if (phaseElapsed < phase.duration) {
        currentPhase = phase;
        break;
      }
      phaseElapsed -= phase.duration;
    }
    
    if (currentPhase) {
      const phaseProgress = phaseElapsed / currentPhase.duration;
      const values = currentPhase.animate(phaseProgress);
      
      applyValues(values);
      updateStatus(currentPhase.name, totalProgress, values);
    }
    
    animationId = requestAnimationFrame(animate);
  }
  
  function stopTest() {
    if (animationId) {
      cancelAnimationFrame(animationId);
      animationId = null;
    }
    
    // Reset to neutral position
    applyValues({ sarjPort: 0, sarjStbd: 0, bgaPort: 0, bgaStbd: 0 });
    
    // Remove status display
    const status = document.getElementById('solar-test-status');
    if (status) {
      status.innerHTML = `
        <div style="color: #7ed321; font-weight: bold;">✅ Test Complete!</div>
        <div style="margin-top: 10px; font-size: 12px; color: #aaa;">
          Arrays reset to neutral position.<br>
          Live telemetry will resume on next update.
        </div>
      `;
      setTimeout(() => status.remove(), 3000);
    }
    
    console.log('✅ Solar Array Animation Test Complete');
  }
  
  // Start animation
  console.log(`
  ╔══════════════════════════════════════════╗
  ║   SOLAR ARRAY ANIMATION TEST             ║
  ╠══════════════════════════════════════════╣
  ║ Duration: ${(totalDuration/1000).toFixed(0)}s                           ║
  ║ Phases: ${phases.length}                                ║
  ╠══════════════════════════════════════════╣
  ║ Test Phases:                             ║
  ${phases.map((p, i) => `  ║  ${i+1}. ${p.name.padEnd(30)} ${(p.duration/1000).toFixed(0)}s  ║`).join('\n')}
  ╚══════════════════════════════════════════╝
  `);
  
  animationId = requestAnimationFrame(animate);
  
  // Expose stop function globally
  window.stopSolarTest = stopTest;
  console.log('💡 Call stopSolarTest() to end the test early');
  
})();
