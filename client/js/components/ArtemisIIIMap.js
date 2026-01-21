/**
 * ArtemisOps - Artemis III Orbital Map
 * 
 * SVG-based visualization of the Artemis III mission profile.
 * Shows NRHO (Near Rectilinear Halo Orbit), HLS operations, and lunar landing.
 * 
 * Mission phases:
 * - TLI (Trans-Lunar Injection)
 * - Outbound Transit
 * - NRHO Insertion
 * - HLS Transfer & Docking
 * - Lunar Descent & Landing
 * - Surface Operations
 * - Lunar Ascent
 * - Orion Rendezvous
 * - Trans-Earth Injection
 * - Return & Splashdown
 * 
 * @extends OrbitalMap
 * @version 1.0.0
 */

class ArtemisIIIMap extends OrbitalMap {
  constructor(containerId, options = {}) {
    super(containerId, {
      showNRHO: true,
      showHLSPath: true,
      showLandingSite: true,
      ...options
    });
    
    // Artemis III specific waypoints (more complex than Artemis II)
    this.waypoints = [
      { id: 1, name: 'Launch', phase: 'launch', x: 100, y: 400, completed: false },
      { id: 2, name: 'TLI', phase: 'tli', x: 180, y: 320, completed: false },
      { id: 3, name: 'Outbound Transit', phase: 'outbound', x: 350, y: 200, completed: false },
      { id: 4, name: 'NRHO Insertion', phase: 'nrho-insert', x: 550, y: 100, completed: false },
      { id: 5, name: 'Gateway Rendezvous', phase: 'gateway', x: 650, y: 80, completed: false },
      { id: 6, name: 'HLS Transfer', phase: 'hls-transfer', x: 720, y: 120, completed: false },
      { id: 7, name: 'Descent Orbit', phase: 'descent', x: 750, y: 200, completed: false },
      { id: 8, name: 'Lunar Landing', phase: 'landing', x: 780, y: 290, completed: false },
      { id: 9, name: 'Surface Ops', phase: 'surface', x: 780, y: 310, completed: false },
      { id: 10, name: 'Ascent', phase: 'ascent', x: 750, y: 250, completed: false },
      { id: 11, name: 'Orion Rendezvous', phase: 'rendezvous', x: 680, y: 150, completed: false },
      { id: 12, name: 'TEI', phase: 'tei', x: 580, y: 180, completed: false },
      { id: 13, name: 'Return Transit', phase: 'return', x: 380, y: 350, completed: false },
      { id: 14, name: 'Entry', phase: 'entry', x: 200, y: 420, completed: false },
      { id: 15, name: 'Splashdown', phase: 'splashdown', x: 120, y: 450, completed: false }
    ];
    
    this.activeWaypointIndex = 0;
    this.svg = null;
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
    
    this.svg = this.createSVGElement('svg', {
      class: 'artemis-iii-map-svg',
      viewBox: '0 0 900 500',
      preserveAspectRatio: 'xMidYMid meet',
      style: 'width: 100%; height: 100%;'
    });
    
    this.svg.appendChild(this.createDefs());
    this.svg.appendChild(this.createStarfield());
    this.svg.appendChild(this.createEarth());
    this.svg.appendChild(this.createMoon());
    this.svg.appendChild(this.createNRHO());
    this.svg.appendChild(this.createTrajectory());
    this.svg.appendChild(this.createHLSPath());
    this.svg.appendChild(this.createLandingSite());
    this.svg.appendChild(this.createWaypoints());
    this.svg.appendChild(this.createSpacecraft());
    this.svg.appendChild(this.createInfoBoxes());
    
    this.container.appendChild(this.svg);
    
    if (this.options.showLegend) {
      this.container.appendChild(this.createLegend());
    }
    
    if (this.options.showPhaseInfo) {
      this.container.appendChild(this.createPhaseInfo());
    }
  }
  
  createDefs() {
    const defs = this.createSVGElement('defs');
    
    // Earth gradient
    const earthGradient = this.createSVGElement('radialGradient', {
      id: 'artemis3-earthGradient',
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
      id: 'artemis3-moonGradient',
      cx: '30%',
      cy: '30%'
    });
    moonGradient.innerHTML = `
      <stop offset="0%" stop-color="#d4d4d4"/>
      <stop offset="50%" stop-color="#a0a0a0"/>
      <stop offset="100%" stop-color="#707070"/>
    `;
    defs.appendChild(moonGradient);
    
    // NRHO orbit gradient
    const nrhoGradient = this.createSVGElement('linearGradient', {
      id: 'artemis3-nrhoGradient',
      x1: '0%',
      y1: '0%',
      x2: '100%',
      y2: '100%'
    });
    nrhoGradient.innerHTML = `
      <stop offset="0%" stop-color="#9c27b0"/>
      <stop offset="50%" stop-color="#7b1fa2"/>
      <stop offset="100%" stop-color="#6a1b9a"/>
    `;
    defs.appendChild(nrhoGradient);
    
    // Glow filters
    const glowFilter = this.createSVGElement('filter', { id: 'artemis3-glow' });
    glowFilter.innerHTML = `
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    `;
    defs.appendChild(glowFilter);
    
    const orangeGlow = this.createSVGElement('filter', { id: 'artemis3-orangeGlow' });
    orangeGlow.innerHTML = `
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feColorMatrix type="matrix" values="1 0 0 0 0.4  0 1 0 0 0.2  0 0 1 0 0  0 0 0 1 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    `;
    defs.appendChild(orangeGlow);
    
    // Orion symbol
    const orionSymbol = this.createSVGElement('symbol', {
      id: 'artemis3-orion',
      viewBox: '0 0 40 20'
    });
    orionSymbol.innerHTML = `
      <polygon points="5,10 15,5 15,15" fill="none" stroke="currentColor" stroke-width="1.5"/>
      <rect x="15" y="6" width="18" height="8" fill="none" stroke="currentColor" stroke-width="1.5" rx="1"/>
      <rect x="19" y="0" width="6" height="3" fill="none" stroke="currentColor" stroke-width="0.75"/>
      <rect x="19" y="17" width="6" height="3" fill="none" stroke="currentColor" stroke-width="0.75"/>
    `;
    defs.appendChild(orionSymbol);
    
    // Starship HLS symbol
    const hlsSymbol = this.createSVGElement('symbol', {
      id: 'artemis3-hls',
      viewBox: '0 0 20 50'
    });
    hlsSymbol.innerHTML = `
      <path d="M10,0 Q15,5 15,15 L15,40 Q15,45 10,50 Q5,45 5,40 L5,15 Q5,5 10,0" 
            fill="none" stroke="currentColor" stroke-width="1.5"/>
      <rect x="2" y="35" width="5" height="10" fill="none" stroke="currentColor" stroke-width="1"/>
      <rect x="13" y="35" width="5" height="10" fill="none" stroke="currentColor" stroke-width="1"/>
      <ellipse cx="10" cy="20" rx="3" ry="4" fill="none" stroke="currentColor" stroke-width="1"/>
    `;
    defs.appendChild(hlsSymbol);
    
    return defs;
  }
  
  createStarfield() {
    const g = this.createSVGElement('g', { opacity: '0.4', class: 'starfield' });
    
    const stars = [
      [50, 80, 1], [150, 50, 0.5], [250, 100, 1], [400, 30, 0.5],
      [550, 60, 1], [700, 40, 0.5], [800, 70, 1], [100, 450, 0.5],
      [300, 480, 1], [500, 460, 0.5], [750, 420, 1], [850, 380, 0.5],
      [450, 150, 0.75], [620, 220, 0.5], [820, 150, 1], [50, 250, 0.5]
    ];
    
    stars.forEach(([cx, cy, r]) => {
      const circle = this.createSVGElement('circle', { cx, cy, r, fill: '#fff' });
      g.appendChild(circle);
    });
    
    return g;
  }
  
  createEarth() {
    const g = this.createSVGElement('g', { transform: 'translate(100, 400)', class: 'earth' });
    
    const earth = this.createSVGElement('circle', {
      r: '60',
      fill: 'url(#artemis3-earthGradient)'
    });
    g.appendChild(earth);
    
    const glow = this.createSVGElement('circle', {
      r: '60',
      fill: 'none',
      stroke: 'rgba(100,180,255,0.4)',
      'stroke-width': '2'
    });
    g.appendChild(glow);
    
    const label = this.createSVGElement('text', {
      y: '80',
      'text-anchor': 'middle',
      fill: '#4a90d9',
      'font-size': '11',
      'font-weight': '600',
      'letter-spacing': '2'
    });
    label.textContent = 'EARTH';
    g.appendChild(label);
    
    return g;
  }
  
  createMoon() {
    const g = this.createSVGElement('g', { transform: 'translate(780, 200)', class: 'moon' });
    
    const moon = this.createSVGElement('circle', {
      r: '80',
      fill: 'url(#artemis3-moonGradient)'
    });
    g.appendChild(moon);
    
    // Craters
    const craters = [
      { cx: -20, cy: -30, r: 12 },
      { cx: 25, cy: 10, r: 15 },
      { cx: -10, cy: 35, r: 8 },
      { cx: 30, cy: -25, r: 10 }
    ];
    craters.forEach(c => {
      const crater = this.createSVGElement('circle', {
        cx: c.cx,
        cy: c.cy,
        r: c.r,
        fill: 'none',
        stroke: 'rgba(100,100,100,0.4)',
        'stroke-width': '1'
      });
      g.appendChild(crater);
    });
    
    const label = this.createSVGElement('text', {
      y: '105',
      'text-anchor': 'middle',
      fill: '#a0a0a0',
      'font-size': '11',
      'font-weight': '600',
      'letter-spacing': '2'
    });
    label.textContent = 'MOON';
    g.appendChild(label);
    
    return g;
  }
  
  createNRHO() {
    const g = this.createSVGElement('g', { class: 'nrho-orbit' });
    
    // NRHO is a highly elliptical orbit around the Moon
    // Periselene: ~3,000 km, Aposelene: ~70,000 km
    const nrho = this.createSVGElement('ellipse', {
      cx: '680',
      cy: '150',
      rx: '120',
      ry: '40',
      fill: 'none',
      stroke: '#9c27b0',
      'stroke-width': '2',
      'stroke-dasharray': '6,3',
      transform: 'rotate(-20 680 150)'
    });
    g.appendChild(nrho);
    
    // NRHO label
    const label = this.createSVGElement('text', {
      x: '680',
      y: '85',
      'text-anchor': 'middle',
      fill: '#9c27b0',
      'font-family': 'Courier New, monospace',
      'font-size': '9',
      'letter-spacing': '1'
    });
    label.textContent = 'NRHO';
    g.appendChild(label);
    
    // Gateway station marker (if applicable)
    const gateway = this.createSVGElement('g', { transform: 'translate(650, 80)' });
    const gwMarker = this.createSVGElement('rect', {
      x: '-6',
      y: '-3',
      width: '12',
      height: '6',
      fill: '#9c27b0',
      rx: '1'
    });
    gateway.appendChild(gwMarker);
    
    const gwLabel = this.createSVGElement('text', {
      x: '0',
      y: '-10',
      'text-anchor': 'middle',
      fill: '#9c27b0',
      'font-size': '8'
    });
    gwLabel.textContent = 'GATEWAY';
    gateway.appendChild(gwLabel);
    
    g.appendChild(gateway);
    
    return g;
  }
  
  createTrajectory() {
    const g = this.createSVGElement('g', { class: 'trajectory' });
    
    // Outbound trajectory (Earth to NRHO)
    const outbound = this.createSVGElement('path', {
      d: 'M 160 400 Q 250 300 350 200 Q 450 100 550 100 Q 600 95 650 80',
      fill: 'none',
      stroke: '#00bcd4',
      'stroke-width': '2.5',
      class: 'trajectory-outbound'
    });
    g.appendChild(outbound);
    
    // Return trajectory (NRHO back to Earth)
    const returnPath = this.createSVGElement('path', {
      d: 'M 580 180 Q 480 250 380 350 Q 280 420 200 420 Q 150 430 120 450',
      fill: 'none',
      stroke: '#8bc34a',
      'stroke-width': '2',
      'stroke-dasharray': '8,4',
      class: 'trajectory-return'
    });
    g.appendChild(returnPath);
    
    return g;
  }
  
  createHLSPath() {
    const g = this.createSVGElement('g', { class: 'hls-path' });
    
    // HLS descent path
    const descent = this.createSVGElement('path', {
      d: 'M 720 120 Q 750 160 750 200 Q 760 250 780 290',
      fill: 'none',
      stroke: '#ff9800',
      'stroke-width': '2.5',
      filter: 'url(#artemis3-orangeGlow)',
      class: 'hls-descent'
    });
    g.appendChild(descent);
    
    // HLS ascent path (dashed)
    const ascent = this.createSVGElement('path', {
      d: 'M 780 290 Q 770 260 750 250 Q 730 220 680 150',
      fill: 'none',
      stroke: '#ff9800',
      'stroke-width': '2',
      'stroke-dasharray': '5,3',
      class: 'hls-ascent'
    });
    g.appendChild(ascent);
    
    // HLS path label
    const label = this.createSVGElement('text', {
      x: '800',
      y: '240',
      fill: '#ff9800',
      'font-family': 'Courier New, monospace',
      'font-size': '9',
      'letter-spacing': '1'
    });
    label.textContent = 'HLS';
    g.appendChild(label);
    
    return g;
  }
  
  createLandingSite() {
    const g = this.createSVGElement('g', { transform: 'translate(780, 290)', class: 'landing-site' });
    
    // Landing site marker
    const marker = this.createSVGElement('polygon', {
      points: '0,-12 8,8 -8,8',
      fill: '#ff9800',
      filter: 'url(#artemis3-orangeGlow)'
    });
    g.appendChild(marker);
    
    // Label
    const label = this.createSVGElement('text', {
      x: '15',
      y: '5',
      fill: '#ff9800',
      'font-family': 'Courier New, monospace',
      'font-size': '9',
      'letter-spacing': '1'
    });
    label.textContent = 'SOUTH POLE';
    g.appendChild(label);
    
    return g;
  }
  
  createWaypoints() {
    const g = this.createSVGElement('g', { class: 'waypoints' });
    
    // Only show key waypoints to avoid clutter
    const keyWaypoints = [1, 4, 6, 8, 11, 12, 15];
    
    this.waypoints.forEach((wp, index) => {
      if (!keyWaypoints.includes(wp.id) && index !== this.activeWaypointIndex) {
        return; // Skip non-key waypoints unless active
      }
      
      const wpGroup = this.createSVGElement('g', {
        transform: `translate(${wp.x}, ${wp.y})`,
        class: `waypoint waypoint-${wp.id}`
      });
      
      const isActive = index === this.activeWaypointIndex;
      const isCompleted = index < this.activeWaypointIndex;
      
      let strokeColor = '#1a3a5c';
      let radius = 6;
      
      if (isCompleted) {
        strokeColor = '#7ed321';
      } else if (isActive) {
        strokeColor = '#ffd60a';
        radius = 8;
      } else if (wp.phase.includes('hls') || wp.phase === 'descent' || wp.phase === 'landing' || wp.phase === 'surface' || wp.phase === 'ascent') {
        strokeColor = '#ff9800';
      } else if (wp.phase.includes('nrho') || wp.phase === 'gateway') {
        strokeColor = '#9c27b0';
      } else if (wp.phase === 'outbound' || wp.phase === 'tli') {
        strokeColor = '#00bcd4';
      } else if (wp.phase === 'return' || wp.phase === 'tei') {
        strokeColor = '#8bc34a';
      }
      
      const circle = this.createSVGElement('circle', {
        r: radius,
        fill: '#0a1628',
        stroke: strokeColor,
        'stroke-width': isActive ? 3 : 2
      });
      wpGroup.appendChild(circle);
      
      const number = this.createSVGElement('text', {
        'text-anchor': 'middle',
        'dominant-baseline': 'central',
        fill: strokeColor,
        'font-size': '8',
        'font-weight': 'bold'
      });
      number.textContent = wp.id;
      wpGroup.appendChild(number);
      
      g.appendChild(wpGroup);
    });
    
    return g;
  }
  
  createSpacecraft() {
    const g = this.createSVGElement('g', { class: 'spacecraft-group' });
    
    const activeWp = this.waypoints[this.activeWaypointIndex] || this.waypoints[0];
    
    // Determine which spacecraft to show based on phase
    const hlsPhases = ['hls-transfer', 'descent', 'landing', 'surface', 'ascent'];
    const isHLS = hlsPhases.includes(activeWp.phase);
    
    const scGroup = this.createSVGElement('g', {
      transform: `translate(${activeWp.x + 15}, ${activeWp.y})`,
      class: 'spacecraft spacecraft-active'
    });
    
    if (isHLS) {
      const hls = this.createSVGElement('use', {
        href: '#artemis3-hls',
        width: '15',
        height: '35',
        x: '-7',
        y: '-17',
        style: 'color: #ff9800',
        filter: 'url(#artemis3-orangeGlow)'
      });
      scGroup.appendChild(hls);
    } else {
      const orion = this.createSVGElement('use', {
        href: '#artemis3-orion',
        width: '30',
        height: '15',
        x: '-15',
        y: '-7',
        style: 'color: #ffd60a',
        filter: 'url(#artemis3-glow)'
      });
      scGroup.appendChild(orion);
    }
    
    g.appendChild(scGroup);
    
    return g;
  }
  
  createInfoBoxes() {
    const g = this.createSVGElement('g', { class: 'info-boxes' });
    
    // Mission status box
    const statusBox = this.createSVGElement('g', { transform: 'translate(700, 380)' });
    
    const rect = this.createSVGElement('rect', {
      width: '180',
      height: '80',
      fill: 'rgba(10,22,40,0.95)',
      stroke: '#1a3a5c',
      rx: '4'
    });
    statusBox.appendChild(rect);
    
    const title = this.createSVGElement('text', {
      x: '10',
      y: '18',
      fill: '#ff9800',
      'font-size': '9',
      'letter-spacing': '1'
    });
    title.textContent = 'SURFACE OPERATIONS';
    statusBox.appendChild(title);
    
    const duration = this.createSVGElement('text', {
      x: '10',
      y: '38',
      fill: '#fff',
      'font-family': 'Courier New',
      'font-size': '11'
    });
    duration.textContent = 'Duration: ~6.5 days';
    statusBox.appendChild(duration);
    
    const evas = this.createSVGElement('text', {
      x: '10',
      y: '55',
      fill: '#fff',
      'font-family': 'Courier New',
      'font-size': '11'
    });
    evas.textContent = 'EVAs: 2 planned';
    statusBox.appendChild(evas);
    
    const crew = this.createSVGElement('text', {
      x: '10',
      y: '72',
      fill: '#8b949e',
      'font-size': '9'
    });
    crew.textContent = 'Crew: 2 on surface, 2 in Orion';
    statusBox.appendChild(crew);
    
    g.appendChild(statusBox);
    
    return g;
  }
  
  createLegend() {
    const legend = document.createElement('div');
    legend.className = 'orbital-map-legend';
    legend.style.minWidth = '160px';
    legend.innerHTML = `
      <div class="orbital-map-legend-title">TRAJECTORY</div>
      <div class="orbital-map-legend-item">
        <span class="orbital-map-legend-line" style="background: #00bcd4;"></span>
        <span>Outbound</span>
      </div>
      <div class="orbital-map-legend-item">
        <span class="orbital-map-legend-line" style="background: #9c27b0;"></span>
        <span>NRHO</span>
      </div>
      <div class="orbital-map-legend-item">
        <span class="orbital-map-legend-line" style="background: #ff9800;"></span>
        <span>HLS Descent/Ascent</span>
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
    phaseInfo.style.borderColor = this.getPhaseColor();
    
    const activeWp = this.waypoints[this.activeWaypointIndex];
    phaseInfo.innerHTML = `
      <div class="orbital-map-phase-label" style="color: ${this.getPhaseColor()}">CURRENT PHASE</div>
      <div class="orbital-map-phase-name">${activeWp?.name?.toUpperCase() || 'UNKNOWN'}</div>
    `;
    return phaseInfo;
  }
  
  getPhaseColor() {
    const activeWp = this.waypoints[this.activeWaypointIndex];
    if (!activeWp) return '#00bcd4';
    
    const phase = activeWp.phase;
    if (phase.includes('hls') || phase === 'descent' || phase === 'landing' || phase === 'surface' || phase === 'ascent') {
      return '#ff9800';
    } else if (phase.includes('nrho') || phase === 'gateway') {
      return '#9c27b0';
    } else if (phase === 'return' || phase === 'tei' || phase === 'entry' || phase === 'splashdown') {
      return '#8bc34a';
    }
    return '#00bcd4';
  }
  
  setActiveWaypoint(waypointId) {
    const index = this.waypoints.findIndex(wp => wp.id === waypointId);
    if (index !== -1) {
      this.activeWaypointIndex = index;
      this.render();
    }
  }
}

// Export for ES modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ArtemisIIIMap;
}
