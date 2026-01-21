/**
 * ArtemisOps - OrbitalMap Base Class
 * 
 * Abstract base class for all orbital map visualizations.
 * Provides common functionality for mission tracking displays.
 * 
 * @version 1.0.0
 */

class OrbitalMap {
  /**
   * @param {string} containerId - DOM element ID to render the map
   * @param {Object} options - Configuration options
   */
  constructor(containerId, options = {}) {
    this.containerId = containerId;
    this.container = null;
    this.options = {
      theme: 'dark',
      showLegend: true,
      showPhaseInfo: true,
      animateSpacecraft: true,
      updateInterval: 5000,
      ...options
    };
    
    // Mission data
    this.missionData = null;
    this.currentPhase = null;
    this.spacecraftPosition = null;
    
    // Event callbacks
    this.callbacks = {
      onPhaseChange: null,
      onPositionUpdate: null,
      onWaypointReached: null,
      onError: null
    };
    
    // State
    this.isInitialized = false;
    this.updateTimer = null;
  }
  
  /**
   * Initialize the orbital map
   * Must be implemented by subclasses
   */
  async init() {
    this.container = document.getElementById(this.containerId);
    if (!this.container) {
      throw new Error(`Container #${this.containerId} not found`);
    }
    
    // Add base styles
    this.addBaseStyles();
    
    this.isInitialized = true;
    return this;
  }
  
  /**
   * Add common CSS styles
   */
  addBaseStyles() {
    if (document.getElementById('orbital-map-base-styles')) return;
    
    const style = document.createElement('style');
    style.id = 'orbital-map-base-styles';
    style.textContent = `
      :root {
        --om-bg-primary: #0a1628;
        --om-bg-panel: #0d1a2d;
        --om-border-color: #1a3a5c;
        --om-text-primary: #ffffff;
        --om-text-secondary: #8b949e;
        --om-accent-cyan: #00bcd4;
        --om-accent-green: #7ed321;
        --om-accent-yellow: #ffd60a;
        --om-accent-orange: #ff9800;
        --om-accent-purple: #9c27b0;
        --om-danger: #ff3b30;
      }
      
      .orbital-map-container {
        position: relative;
        width: 100%;
        height: 100%;
        background: var(--om-bg-primary);
        overflow: hidden;
        font-family: 'Courier New', monospace;
      }
      
      .orbital-map-legend {
        position: absolute;
        bottom: 20px;
        left: 20px;
        background: rgba(10, 22, 40, 0.95);
        border: 1px solid var(--om-border-color);
        border-radius: 4px;
        padding: 12px;
        z-index: 100;
        font-size: 0.75rem;
      }
      
      .orbital-map-legend-title {
        font-size: 0.65rem;
        color: var(--om-text-secondary);
        letter-spacing: 1px;
        margin-bottom: 8px;
        text-transform: uppercase;
      }
      
      .orbital-map-legend-item {
        display: flex;
        align-items: center;
        gap: 8px;
        margin: 4px 0;
      }
      
      .orbital-map-legend-line {
        width: 25px;
        height: 2px;
      }
      
      .orbital-map-phase-info {
        position: absolute;
        top: 20px;
        left: 20px;
        background: rgba(10, 22, 40, 0.95);
        border: 1px solid var(--om-border-color);
        border-radius: 4px;
        padding: 12px;
        z-index: 100;
      }
      
      .orbital-map-phase-label {
        font-size: 0.6rem;
        color: var(--om-accent-cyan);
        letter-spacing: 1px;
        text-transform: uppercase;
      }
      
      .orbital-map-phase-name {
        font-size: 1rem;
        font-weight: bold;
        color: var(--om-text-primary);
        margin-top: 4px;
      }
      
      .orbital-map-loading {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: var(--om-text-secondary);
        font-size: 0.9rem;
      }
      
      .orbital-map-error {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: var(--om-danger);
        text-align: center;
        font-size: 0.9rem;
      }
      
      @keyframes spacecraft-pulse {
        0%, 100% { filter: drop-shadow(0 0 8px var(--om-accent-yellow)); }
        50% { filter: drop-shadow(0 0 16px var(--om-accent-yellow)); }
      }
      
      .spacecraft-active {
        animation: spacecraft-pulse 2s ease-in-out infinite;
      }
    `;
    document.head.appendChild(style);
  }
  
  /**
   * Load mission data
   * @param {Object} missionData - Mission configuration and trajectory data
   */
  setMissionData(missionData) {
    this.missionData = missionData;
    this.currentPhase = missionData.currentPhase || null;
    if (this.isInitialized) {
      this.render();
    }
  }
  
  /**
   * Update spacecraft position
   * @param {Object} position - { lat, lng, alt, velocity, phase }
   */
  updatePosition(position) {
    this.spacecraftPosition = position;
    if (position.phase && position.phase !== this.currentPhase) {
      const oldPhase = this.currentPhase;
      this.currentPhase = position.phase;
      this.onPhaseChange(oldPhase, position.phase);
    }
    this.onPositionUpdate(position);
  }
  
  /**
   * Render the orbital map
   * Must be implemented by subclasses
   */
  render() {
    throw new Error('render() must be implemented by subclass');
  }
  
  /**
   * Start auto-updating position
   */
  startTracking() {
    if (this.updateTimer) return;
    this.updateTimer = setInterval(() => {
      this.fetchPosition();
    }, this.options.updateInterval);
  }
  
  /**
   * Stop auto-updating position
   */
  stopTracking() {
    if (this.updateTimer) {
      clearInterval(this.updateTimer);
      this.updateTimer = null;
    }
  }
  
  /**
   * Fetch current position from API
   * Should be overridden by subclasses for specific APIs
   */
  async fetchPosition() {
    // Override in subclasses
  }
  
  /**
   * Handle phase change
   * @param {string} oldPhase 
   * @param {string} newPhase 
   */
  onPhaseChange(oldPhase, newPhase) {
    if (this.callbacks.onPhaseChange) {
      this.callbacks.onPhaseChange(oldPhase, newPhase);
    }
    
    // Emit DOM event
    const event = new CustomEvent('orbitalMapPhaseChange', {
      detail: { oldPhase, newPhase, mission: this.missionData?.id }
    });
    document.dispatchEvent(event);
  }
  
  /**
   * Handle position update
   * @param {Object} position 
   */
  onPositionUpdate(position) {
    if (this.callbacks.onPositionUpdate) {
      this.callbacks.onPositionUpdate(position);
    }
    
    const event = new CustomEvent('orbitalMapPositionUpdate', {
      detail: { position, mission: this.missionData?.id }
    });
    document.dispatchEvent(event);
  }
  
  /**
   * Register event callbacks
   * @param {string} event - Event name (onPhaseChange, onPositionUpdate, etc.)
   * @param {Function} callback - Callback function
   */
  on(event, callback) {
    if (this.callbacks.hasOwnProperty(event)) {
      this.callbacks[event] = callback;
    }
    return this;
  }
  
  /**
   * Get current mission state
   */
  getState() {
    return {
      missionId: this.missionData?.id,
      currentPhase: this.currentPhase,
      position: this.spacecraftPosition,
      isTracking: !!this.updateTimer
    };
  }
  
  /**
   * Clean up resources
   */
  destroy() {
    this.stopTracking();
    if (this.container) {
      this.container.innerHTML = '';
    }
    this.isInitialized = false;
  }
  
  /**
   * Create SVG element helper
   */
  createSVGElement(tag, attributes = {}) {
    const el = document.createElementNS('http://www.w3.org/2000/svg', tag);
    Object.entries(attributes).forEach(([key, value]) => {
      el.setAttribute(key, value);
    });
    return el;
  }
  
  /**
   * Format distance for display
   */
  formatDistance(km) {
    if (km >= 1000000) {
      return (km / 1000000).toFixed(2) + 'M km';
    } else if (km >= 1000) {
      return Math.round(km).toLocaleString() + ' km';
    }
    return km.toFixed(1) + ' km';
  }
  
  /**
   * Format velocity for display
   */
  formatVelocity(kmh) {
    return Math.round(kmh).toLocaleString() + ' km/h';
  }
}

// Export for ES modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = OrbitalMap;
}
