/**
 * ISS Solar Array Rotation Test Script
 * 
 * Tests SARJ and BGA rotations through 180 degrees each.
 * SARJ: Z axis creates H baseline, Y axis rotates panels
 * BGA: Y axis rotates panels
 * H shape always preserved from nadir view.
 * 
 * Usage: 
 *   testSolarRotation.start()   - Begin test sequence
 *   testSolarRotation.stop()    - Stop current test
 *   testSolarRotation.reset()   - Reset to baseline
 */

window.testSolarRotation = (function() {
  let animationId = null;
  
  const SARJ_Z_BASELINE = -45 * Math.PI / 180;  // Fixed Z for H shape
  const ANIMATION_SPEED = 0.02;
  const TARGET_ANGLE = Math.PI;  // 180 degrees
  
  function log(msg) {
    console.log(`[Solar Test] ${msg}`);
  }
  
  function getJoints() {
    return {
      nadir: window.solarJoints?.nadir,
      velocity: window.solarJoints?.velocity
    };
  }
  
  function disableTelemetry() {
    if (!window._originalUpdateSolarArrays && window.updateSolarArrays) {
      window._originalUpdateSolarArrays = window.updateSolarArrays;
      window.updateSolarArrays = function() {};
      log('Telemetry disabled');
    }
  }
  
  function enableTelemetry() {
    if (window._originalUpdateSolarArrays) {
      window.updateSolarArrays = window._originalUpdateSolarArrays;
      delete window._originalUpdateSolarArrays;
      log('Telemetry enabled');
    }
  }
  
  function resetToBaseline() {
    const joints = getJoints();
    
    ['nadir', 'velocity'].forEach(view => {
      const j = joints[view];
      if (!j) return;
      
      // SARJ: Z for H baseline, Y = 0
      if (j.portSARJ) j.portSARJ.rotation.set(0, 0, SARJ_Z_BASELINE);
      if (j.stbdSARJ) j.stbdSARJ.rotation.set(0, 0, SARJ_Z_BASELINE);
      
      // BGA: Y = 0
      j.portBGA.forEach(b => b.rotation.y = 0);
      j.stbdBGA.forEach(b => b.rotation.y = 0);
    });
    
    log('Reset to H baseline (SARJ Y=0°, BGA=0°)');
  }

  // ============================================
  // TEST: SARJ Rotation
  // ============================================
  function testSARJ(callback) {
    log('=== SARJ TEST: Panel rotation (Y axis, Z baseline preserved) ===');
    log('Watch: Panels rotate, H shape stays intact (0° → 180°)');
    
    const joints = getJoints();
    let angle = 0;
    
    resetToBaseline();
    
    function animate() {
      angle += ANIMATION_SPEED;
      
      ['nadir', 'velocity'].forEach(view => {
        const j = joints[view];
        if (!j) return;
        
        // Keep Z baseline, rotate Y
        if (j.portSARJ) j.portSARJ.rotation.set(0, angle, SARJ_Z_BASELINE);
        if (j.stbdSARJ) j.stbdSARJ.rotation.set(0, angle, SARJ_Z_BASELINE);
      });
      
      if (angle >= TARGET_ANGLE) {
        log(`SARJ test complete: 0° → 180°`);
        if (callback) setTimeout(callback, 1000);
        return;
      }
      
      animationId = requestAnimationFrame(animate);
    }
    
    animationId = requestAnimationFrame(animate);
  }

  // ============================================
  // TEST: BGA Rotation
  // ============================================
  function testBGA(callback) {
    log('=== BGA TEST: Panel rotation (Y axis) ===');
    log('Watch: Panels rotate around boom (0° → 180°)');
    
    const joints = getJoints();
    let angle = 0;
    
    resetToBaseline();
    
    function animate() {
      angle += ANIMATION_SPEED;
      
      ['nadir', 'velocity'].forEach(view => {
        const j = joints[view];
        if (!j) return;
        
        j.portBGA.forEach(b => b.rotation.y = angle);
        j.stbdBGA.forEach(b => b.rotation.y = angle);
      });
      
      if (angle >= TARGET_ANGLE) {
        log(`BGA test complete: 0° → 180°`);
        if (callback) setTimeout(callback, 1000);
        return;
      }
      
      animationId = requestAnimationFrame(animate);
    }
    
    animationId = requestAnimationFrame(animate);
  }

  // ============================================
  // TEST: Combined
  // ============================================
  function testCombined(callback) {
    log('=== COMBINED TEST: SARJ + BGA ===');
    
    const joints = getJoints();
    let angle = 0;
    
    resetToBaseline();
    
    function animate() {
      angle += ANIMATION_SPEED;
      
      ['nadir', 'velocity'].forEach(view => {
        const j = joints[view];
        if (!j) return;
        
        if (j.portSARJ) j.portSARJ.rotation.set(0, angle, SARJ_Z_BASELINE);
        if (j.stbdSARJ) j.stbdSARJ.rotation.set(0, angle, SARJ_Z_BASELINE);
        j.portBGA.forEach(b => b.rotation.y = angle);
        j.stbdBGA.forEach(b => b.rotation.y = angle);
      });
      
      if (angle >= TARGET_ANGLE) {
        log(`Combined test complete`);
        if (callback) setTimeout(callback, 1000);
        return;
      }
      
      animationId = requestAnimationFrame(animate);
    }
    
    animationId = requestAnimationFrame(animate);
  }
  
  function runFullSequence() {
    log('========================================');
    log('SOLAR ARRAY ROTATION TEST');
    log('H shape always preserved from nadir');
    log('========================================');
    
    disableTelemetry();
    
    testSARJ(() => {
      testBGA(() => {
        testCombined(() => {
          resetToBaseline();
          log('ALL TESTS COMPLETE');
        });
      });
    });
  }

  // ============================================
  // PUBLIC API
  // ============================================
  return {
    start: runFullSequence,
    
    stop: function() {
      if (animationId) {
        cancelAnimationFrame(animationId);
        animationId = null;
        log('Stopped');
      }
    },
    
    reset: function() {
      this.stop();
      disableTelemetry();
      resetToBaseline();
    },
    
    resume: function() {
      enableTelemetry();
      log('Telemetry resumed');
    },
    
    sarj: function() {
      this.stop();
      disableTelemetry();
      testSARJ(() => { resetToBaseline(); log('SARJ done'); });
    },
    
    bga: function() {
      this.stop();
      disableTelemetry();
      testBGA(() => { resetToBaseline(); log('BGA done'); });
    },
    
    combined: function() {
      this.stop();
      disableTelemetry();
      testCombined(() => { resetToBaseline(); log('Combined done'); });
    },
    
    help: function() {
      console.log(`
Solar Array Test Commands:
  testSolarRotation.start()    - Full sequence
  testSolarRotation.sarj()     - SARJ only
  testSolarRotation.bga()      - BGA only
  testSolarRotation.combined() - Both together
  testSolarRotation.reset()    - Reset to H baseline
  testSolarRotation.resume()   - Resume telemetry

Rotation: SARJ Z=-45° baseline + Y telemetry, BGA Y telemetry
      `);
    }
  };
})();

console.log('[Solar Test] Loaded. testSolarRotation.help() for commands');
