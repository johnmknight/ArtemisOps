/**
 * ArtemisOps - Artemis II Orbital Map
 * 
 * SVG-based visualization of the Artemis II free return trajectory.
 * Shows Earth-to-Moon flyby and return path.
 * 
 * Trajectory phases:
 * - TLI (Trans-Lunar Injection)
 * - Outbound Transit
 * - Lunar Flyby (~7,400 km from Moon surface)
 * - Return Transit
 * - Entry & Splashdown
 * 
 * @extends OrbitalMap
 * @version 1.0.0
 */

class ArtemisIIMap extends OrbitalMap {
  constructor(containerId, options = {}) {
    super(containerId, {
      showDistanceIndicator: true,
      showWaypoints: true,
      animateTrajectory: true,
      ...options
    });
    
    // Artemis II specific waypoints
    this.waypoints = [
      { id: 1, name: 'Launch', phase: 'launch', x: 140, y: 250, completed: false },
      { id: 7, name: 'TLI Burn', phase: 'tli', x: 260, y: 190, completed: false },
      { id: 8, name: 'Outbound Coast', phase: 'outbound', x: 420, y: 75, completed: false },
      { id: 9, name: 'Mid-Course', phase: 'outbound', x: 580, y: 85, completed: false },
      { id: 10, name: 'Lunar Approach', phase: 'approach', x: 720, y: 160, completed: false },
      { id: 11, name: 'Lunar Flyby', phase: 'flyby', x: 800, y: 290, completed: false },
      { id: 12, name: 'Trans-Earth', phase: 'return', x: 720, y: 340, completed: false },
      { id: 13, name: 'Return Coast', phase: 'return', x: 500, y: 430, completed: false },
      { id: 14, name: 'Earth Approach', phase: 'entry', x: 320, y: 420, completed: false },
      { id: 15, name: 'Splashdown', phase: 'splashdown', x: 225, y: 335, completed: false }
    ];
    
    // Current active waypoint index
    this.activeWaypointIndex = 0;
    
    // SVG element reference
    this.svg = null;
    this.spacecraftElement = null;
  }
  
  async init() {
    await super.init();
    this.render();
    return this;
  }
  
  render() {
    if (!this.container) return;
    
    this.container.innerHTML = '';
    this.container.className = 'orbital-map-container';
    
    // Create SVG
    this.svg = this.createSVGElement('svg', {
      class: 'artemis-ii-map-svg',
      viewBox: '0 0 900 500',
      preserveAspectRatio: 'xMidYMid meet',
      style: 'width: 100%; height: 100%;'
    });
    
    // Add defs (gradients, filters, symbols)
    this.svg.appendChild(this.createDefs());
    
    // Add background stars
    this.svg.appendChild(this.createStarfield());
    
    // Add Earth
    this.svg.appendChild(this.createEarth());
    
    // Add Moon
    this.svg.appendChild(this.createMoon());
    
    // Add trajectory paths
    this.svg.appendChild(this.createTrajectory());
    
    // Add waypoints
    this.svg.appendChild(this.createWaypoints());
    
    // Add spacecraft
    this.svg.appendChild(this.createSpacecraft());
    
    // Add distance indicator
    if (this.options.showDistanceIndicator) {
      this.svg.appendChild(this.createDistanceIndicator());
    }
    
    this.container.appendChild(this.svg);
    
    // Add legend
    if (this.options.showLegend) {
      this.container.appendChild(this.createLegend());
    }
    
    // Add phase info box
    if (this.options.showPhaseInfo) {
      this.container.appendChild(this.createPhaseInfo());
    }
    
    // Update display based on mission data
    this.updateDisplay();
  }
  
  createDefs() {
    const defs = this.createSVGElement('defs');
    
    // Earth gradient
    const earthGradient = this.createSVGElement('radialGradient', {
      id: 'artemis2-earthGradient',
      cx: '30%',
      cy: '30%'
    });
    earthGradient.innerHTML = `
      <stop offset="0%" stop-color="#4a90d9"/>
      <stop offset="50%" stop-color="#2d5a8a"/>
      <stop offset="100%" stop-color="#1a3a5c"/>
    `;
    defs.appendChild(earthGradient);
    
    // Moon gradient
    const moonGradient = this.createSVGElement('radialGradient', {
      id: 'artemis2-moonGradient',
      cx: '30%',
      cy: '30%'
    });
    moonGradient.innerHTML = `
      <stop offset="0%" stop-color="#d4d4d4"/>
      <stop offset="50%" stop-color="#a0a0a0"/>
      <stop offset="100%" stop-color="#707070"/>
    `;
    defs.appendChild(moonGradient);
    
    // Glow filter
    const glowFilter = this.createSVGElement('filter', { id: 'artemis2-glow' });
    glowFilter.innerHTML = `
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    `;
    defs.appendChild(glowFilter);
    
    // Orion spacecraft symbol
    const orionSymbol = this.createSVGElement('symbol', {
      id: 'artemis2-orion',
      viewBox: '0 0 40 20'
    });
    orionSymbol.innerHTML = `
      <polygon points="5,10 15,5 15,15" fill="none" stroke="currentColor" stroke-width="1.5"/>
      <rect x="15" y="6" width="18" height="8" fill="none" stroke="currentColor" stroke-width="1.5" rx="1"/>
      <line x1="22" y1="6" x2="22" y2="2" stroke="currentColor" stroke-width="1"/>
      <line x1="22" y1="14" x2="22" y2="18" stroke="currentColor" stroke-width="1"/>
      <rect x="19" y="0" width="6" height="3" fill="none" stroke="currentColor" stroke-width="0.75"/>
      <rect x="19" y="17" width="6" height="3" fill="none" stroke="currentColor" stroke-width="0.75"/>
    `;
    defs.appendChild(orionSymbol);
    
    return defs;
  }
  
  createStarfield() {
    const g = this.createSVGElement('g', { opacity: '0.4', class: 'starfield' });
    
    // Generate random stars
    const stars = [
      [50, 50, 1], [150, 80, 0.5], [250, 30, 1], [400, 60, 0.5],
      [550, 40, 1], [700, 70, 0.5], [800, 50, 1], [100, 420, 0.5],
      [300, 450, 1], [500, 470, 0.5], [750, 440, 1], [850, 460, 0.5],
      [120, 150, 0.75], [450, 380, 0.5], [650, 120, 1], [180, 350, 0.5]
    ];
    
    stars.forEach(([cx, cy, r]) => {
      const circle = this.createSVGElement('circle', { cx, cy, r, fill: '#fff' });
      g.appendChild(circle);
    });
    
    return g;
  }
  
  createEarth() {
    const g = this.createSVGElement('g', { transform: 'translate(140, 250)', class: 'earth' });
    
    // Main Earth circle
    const earth = this.createSVGElement('circle', {
      r: '85',
      fill: 'url(#artemis2-earthGradient)'
    });
    g.appendChild(earth);
    
    // Equator line
    const equator = this.createSVGElement('ellipse', {
      rx: '85',
      ry: '30',
      fill: 'none',
      stroke: 'rgba(100,180,255,0.3)',
      'stroke-width': '1'
    });
    g.appendChild(equator);
    
    // Outer glow
    const glow = this.createSVGElement('circle', {
      r: '85',
      fill: 'none',
      stroke: 'rgba(100,180,255,0.4)',
      'stroke-width': '2'
    });
    g.appendChild(glow);
    
    // Label
    const label = this.createSVGElement('text', {
      y: '110',
      'text-anchor': 'middle',
      fill: '#4a90d9',
      'font-family': 'Arial, sans-serif',
      'font-size': '12',
      'font-weight': '600',
      'letter-spacing': '2'
    });
    label.textContent = 'EARTH';
    g.appendChild(label);
    
    return g;
  }
  
  createMoon() {
    const g = this.createSVGElement('g', { transform: 'translate(760, 250)', class: 'moon' });
    
    // Main Moon circle
    const moon = this.createSVGElement('circle', {
      r: '35',
      fill: 'url(#artemis2-moonGradient)'
    });
    g.appendChild(moon);
    
    // Craters
    const craters = [
      { cx: -8, cy: -8, r: 6 },
      { cx: 10, cy: 5, r: 8 },
      { cx: -5, cy: 12, r: 4 }
    ];
    craters.forEach(c => {
      const crater = this.createSVGElement('circle', {
        cx: c.cx,
        cy: c.cy,
        r: c.r,
        fill: 'none',
        stroke: 'rgba(100,100,100,0.5)',
        'stroke-width': '1'
      });
      g.appendChild(crater);
    });
    
    // Label
    const label = this.createSVGElement('text', {
      y: '55',
      'text-anchor': 'middle',
      fill: '#a0a0a0',
      'font-family': 'Arial, sans-serif',
      'font-size': '12',
      'font-weight': '600',
      'letter-spacing': '2'
    });
    label.textContent = 'MOON';
    g.appendChild(label);
    
    return g;
  }
  
  createTrajectory() {
    const g = this.createSVGElement('g', { class: 'trajectory' });
    
    // High Earth Orbit (parking orbit)
    const heo = this.createSVGElement('ellipse', {
      cx: '140',
      cy: '250',
      rx: '130',
      ry: '80',
      fill: 'none',
      stroke: '#00bcd4',
      'stroke-width': '1.5',
      'stroke-dasharray': '4,4',
      opacity: '0.4'
    });
    g.appendChild(heo);
    
    // HEO label
    const heoLabel = this.createSVGElement('text', {
      x: '140',
      y: '145',
      'text-anchor': 'middle',
      fill: '#00bcd4',
      'font-family': 'Courier New, monospace',
      'font-size': '10',
      'letter-spacing': '1',
      opacity: '0.6'
    });
    heoLabel.textContent = 'HIGH EARTH ORBIT';
    g.appendChild(heoLabel);
    
    // Outbound trajectory
    const outbound = this.createSVGElement('path', {
      d: 'M 260 190 Q 380 80 500 70 Q 620 60 700 130 Q 740 170 750 215',
      fill: 'none',
      stroke: '#00bcd4',
      'stroke-width': '2.5',
      class: 'trajectory-outbound'
    });
    g.appendChild(outbound);
    
    // Lunar flyby (active segment)
    const flyby = this.createSVGElement('path', {
      d: 'M 750 215 Q 810 250 795 310 Q 780 360 720 340',
      fill: 'none',
      stroke: '#ffd60a',
      'stroke-width': '3',
      filter: 'url(#artemis2-glow)',
      class: 'trajectory-flyby'
    });
    g.appendChild(flyby);
    
    // Return trajectory
    const returnPath = this.createSVGElement('path', {
      d: 'M 720 340 Q 580 420 420 440 Q 280 455 225 335',
      fill: 'none',
      stroke: '#8bc34a',
      'stroke-width': '2',
      'stroke-dasharray': '8,4',
      class: 'trajectory-return'
    });
    g.appendChild(returnPath);
    
    return g;
  }
  
  createWaypoints() {
    const g = this.createSVGElement('g', { class: 'waypoints' });
    
    this.waypoints.forEach((wp, index) => {
      const wpGroup = this.createSVGElement('g', {
        transform: `translate(${wp.x}, ${wp.y})`,
        class: `waypoint waypoint-${wp.id}`,
        'data-waypoint-id': wp.id
      });
      
      // Determine waypoint state
      const isActive = index === this.activeWaypointIndex;
      const isCompleted = index < this.activeWaypointIndex;
      
      // Circle
      let strokeColor = '#1a3a5c';
      let fillColor = '#0a1628';
      let radius = 8;
      let strokeWidth = 2;
      
      if (isCompleted) {
        strokeColor = '#7ed321';
      } else if (isActive) {
        strokeColor = '#ffd60a';
        radius = 10;
        strokeWidth = 3;
      } else if (wp.phase === 'outbound') {
        strokeColor = '#00bcd4';
      } else if (wp.phase === 'return') {
        strokeColor = '#8bc34a';
      }
      
      const circle = this.createSVGElement('circle', {
        r: radius,
        fill: fillColor,
        stroke: strokeColor,
        'stroke-width': strokeWidth,
        class: isActive ? 'waypoint-active' : ''
      });
      wpGroup.appendChild(circle);
      
      // Number
      const number = this.createSVGElement('text', {
        'text-anchor': 'middle',
        'dominant-baseline': 'central',
        fill: strokeColor,
        'font-family': 'Arial, sans-serif',
        'font-size': '10',
        'font-weight': 'bold'
      });
      number.textContent = wp.id;
      wpGroup.appendChild(number);
      
      g.appendChild(wpGroup);
    });
    
    // Add special labels
    const labels = [
      { text: 'TLI BURN', x: 260, y: 170 },
      { text: 'LUNAR FLYBY', x: 840, y: 280 },
      { text: '~7,400 km', x: 840, y: 295, small: true },
      { text: 'RETURN COAST', x: 500, y: 455, color: '#8bc34a' },
      { text: 'SPLASHDOWN', x: 225, y: 365, color: '#8bc34a' }
    ];
    
    labels.forEach(lbl => {
      const text = this.createSVGElement('text', {
        x: lbl.x,
        y: lbl.y,
        'text-anchor': lbl.x > 700 ? 'start' : 'middle',
        fill: lbl.color || '#8b949e',
        'font-family': 'Courier New, monospace',
        'font-size': lbl.small ? '9' : '10',
        'letter-spacing': '1'
      });
      text.textContent = lbl.text;
      g.appendChild(text);
    });
    
    return g;
  }
  
  createSpacecraft() {
    const g = this.createSVGElement('g', { class: 'spacecraft-group' });
    
    // Get active waypoint position
    const activeWp = this.waypoints[this.activeWaypointIndex] || this.waypoints[3];
    
    // Position spacecraft slightly ahead of active waypoint
    const scX = activeWp.x + 30;
    const scY = activeWp.y + 10;
    
    this.spacecraftElement = this.createSVGElement('g', {
      transform: `translate(${scX}, ${scY}) rotate(-15)`,
      class: 'spacecraft spacecraft-active'
    });
    
    const orion = this.createSVGElement('use', {
      href: '#artemis2-orion',
      width: '35',
      height: '18',
      x: '-17',
      y: '-9',
      style: 'color: #ffd60a',
      filter: 'url(#artemis2-glow)'
    });
    this.spacecraftElement.appendChild(orion);
    
    g.appendChild(this.spacecraftElement);
    
    return g;
  }
  
  createDistanceIndicator() {
    const g = this.createSVGElement('g', { opacity: '0.6', class: 'distance-indicator' });
    
    // Get active waypoint
    const activeWp = this.waypoints[this.activeWaypointIndex] || this.waypoints[3];
    
    // Line from Earth to spacecraft
    const line = this.createSVGElement('line', {
      x1: '225',
      y1: '250',
      x2: activeWp.x,
      y2: activeWp.y,
      stroke: '#3a5a7a',
      'stroke-width': '1',
      'stroke-dasharray': '3,3'
    });
    g.appendChild(line);
    
    // Distance text
    const text = this.createSVGElement('text', {
      x: (225 + activeWp.x) / 2,
      y: (250 + activeWp.y) / 2 - 10,
      'text-anchor': 'middle',
      fill: '#8b949e',
      'font-family': 'Courier New, monospace',
      'font-size': '11'
    });
    text.textContent = this.formatDistance(this.missionData?.currentDistance || 185000);
    g.appendChild(text);
    
    // Distance to Moon box
    const distBox = this.createSVGElement('g', { transform: 'translate(700, 30)' });
    
    const rect = this.createSVGElement('rect', {
      width: '170',
      height: '50',
      fill: 'rgba(10,22,40,0.9)',
      stroke: '#1a3a5c',
      rx: '4'
    });
    distBox.appendChild(rect);
    
    const label = this.createSVGElement('text', {
      x: '10',
      y: '20',
      fill: '#8b949e',
      'font-size': '9',
      'letter-spacing': '1'
    });
    label.textContent = 'DISTANCE TO MOON';
    distBox.appendChild(label);
    
    const value = this.createSVGElement('text', {
      x: '10',
      y: '38',
      fill: '#fff',
      'font-family': 'Courier New, monospace',
      'font-size': '16',
      'font-weight': 'bold',
      class: 'distance-to-moon-value'
    });
    value.textContent = this.formatDistance(this.missionData?.distanceToMoon || 198500);
    distBox.appendChild(value);
    
    g.appendChild(distBox);
    
    return g;
  }
  
  createLegend() {
    const legend = document.createElement('div');
    legend.className = 'orbital-map-legend';
    legend.innerHTML = `
      <div class="orbital-map-legend-title">TRAJECTORY</div>
      <div class="orbital-map-legend-item">
        <span class="orbital-map-legend-line" style="background: #00bcd4;"></span>
        <span>Outbound</span>
      </div>
      <div class="orbital-map-legend-item">
        <span class="orbital-map-legend-line" style="background: #ffd60a;"></span>
        <span>Active</span>
      </div>
      <div class="orbital-map-legend-item">
        <span class="orbital-map-legend-line" style="background: #8bc34a; background-image: repeating-linear-gradient(90deg, #8bc34a, #8bc34a 4px, transparent 4px, transparent 6px);"></span>
        <span>Return</span>
      </div>
    `;
    return legend;
  }
  
  createPhaseInfo() {
    const phaseInfo = document.createElement('div');
    phaseInfo.className = 'orbital-map-phase-info';
    phaseInfo.id = 'artemis2-phase-info';
    
    const phase = this.getCurrentPhaseName();
    phaseInfo.innerHTML = `
      <div class="orbital-map-phase-label">CURRENT PHASE</div>
      <div class="orbital-map-phase-name">${phase}</div>
    `;
    return phaseInfo;
  }
  
  getCurrentPhaseName() {
    const activeWp = this.waypoints[this.activeWaypointIndex];
    if (!activeWp) return 'UNKNOWN';
    
    const phaseNames = {
      'launch': 'LAUNCH',
      'tli': 'TLI BURN',
      'outbound': 'OUTBOUND TRANSIT',
      'approach': 'LUNAR APPROACH',
      'flyby': 'LUNAR FLYBY',
      'return': 'RETURN TRANSIT',
      'entry': 'EARTH APPROACH',
      'splashdown': 'ENTRY & SPLASHDOWN'
    };
    
    return phaseNames[activeWp.phase] || activeWp.name.toUpperCase();
  }
  
  /**
   * Set the active waypoint/phase
   * @param {number} waypointId - Waypoint ID (1-15)
   */
  setActiveWaypoint(waypointId) {
    const index = this.waypoints.findIndex(wp => wp.id === waypointId);
    if (index !== -1) {
      this.activeWaypointIndex = index;
      this.render();
    }
  }
  
  /**
   * Move to next waypoint
   */
  advanceToNextWaypoint() {
    if (this.activeWaypointIndex < this.waypoints.length - 1) {
      this.activeWaypointIndex++;
      this.render();
      
      const newWp = this.waypoints[this.activeWaypointIndex];
      if (this.callbacks.onWaypointReached) {
        this.callbacks.onWaypointReached(newWp);
      }
    }
  }
  
  /**
   * Update mission distances
   * @param {Object} distances - { currentDistance, distanceToMoon }
   */
  updateDistances(distances) {
    if (this.missionData) {
      this.missionData.currentDistance = distances.currentDistance;
      this.missionData.distanceToMoon = distances.distanceToMoon;
    }
    
    // Update distance display
    const moonDistEl = this.svg?.querySelector('.distance-to-moon-value');
    if (moonDistEl) {
      moonDistEl.textContent = this.formatDistance(distances.distanceToMoon);
    }
  }
  
  /**
   * Update display based on mission data
   */
  updateDisplay() {
    if (!this.missionData) return;
    
    // Update active waypoint based on mission phase
    if (this.missionData.currentPhase) {
      const phaseWaypointMap = {
        'launch': 1,
        'tli': 7,
        'outbound_early': 8,
        'outbound_mid': 9,
        'outbound_late': 10,
        'flyby': 11,
        'return_early': 12,
        'return_mid': 13,
        'entry': 14,
        'splashdown': 15
      };
      
      const wpId = phaseWaypointMap[this.missionData.currentPhase];
      if (wpId) {
        this.setActiveWaypoint(wpId);
      }
    }
  }
}

// Export for ES modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ArtemisIIMap;
}
