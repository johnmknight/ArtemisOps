/**
 * ArtemisOps - ISS Orbital Map
 * 
 * Leaflet-based real-time ISS tracking map.
 * Extends OrbitalMap base class with live position tracking.
 * 
 * Features:
 * - Real-time ISS position from WhereTheISS API
 * - Ground track visualization
 * - Visibility footprint circle
 * - Crew roster integration
 * - Location reverse geocoding
 * 
 * @extends OrbitalMap
 * @version 1.0.0
 */

class ISSMap extends OrbitalMap {
  constructor(containerId, options = {}) {
    super(containerId, {
      showGroundTrack: true,
      showFootprint: true,
      centerOnISS: false,
      trackHistoryLength: 200,
      ...options
    });
    
    // Leaflet specific properties
    this.map = null;
    this.issMarker = null;
    this.footprintCircle = null;
    this.groundTrack = null;
    this.positionHistory = [];
    
    // ISS data
    this.altitude = null;
    this.velocity = null;
    this.visibility = null;
    this.crew = [];
    this.locationName = '';
  }
  
  async init() {
    await super.init();
    
    // Check if Leaflet is loaded
    if (typeof L === 'undefined') {
      throw new Error('Leaflet library not loaded. Include leaflet.js before using ISSMap.');
    }
    
    this.container.className = 'orbital-map-container';
    
    // Create map container
    const mapDiv = document.createElement('div');
    mapDiv.id = `${this.containerId}-leaflet`;
    mapDiv.style.width = '100%';
    mapDiv.style.height = '100%';
    this.container.appendChild(mapDiv);
    
    // Initialize Leaflet map
    this.map = L.map(mapDiv.id, {
      center: [20, 0],
      zoom: 2,
      minZoom: 1,
      maxZoom: 8,
      worldCopyJump: true
    });
    
    // Add dark tile layer
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; OpenStreetMap &copy; CARTO',
      subdomains: 'abcd',
      maxZoom: 19
    }).addTo(this.map);
    
    // Create ISS marker
    this.createISSMarker();
    
    // Create footprint circle
    if (this.options.showFootprint) {
      this.createFootprintCircle();
    }
    
    // Create ground track
    if (this.options.showGroundTrack) {
      this.createGroundTrack();
    }
    
    // Add custom styles
    this.addMapStyles();
    
    // Add overlays
    this.addDataOverlay();
    this.addMapControls();
    
    // Fetch initial data
    await this.fetchPosition();
    await this.fetchCrew();
    
    // Start tracking
    this.startTracking();
    
    return this;
  }
  
  createISSMarker() {
    const issIcon = L.divIcon({
      className: 'iss-marker',
      html: `
        <div class="iss-icon">
          <svg viewBox="0 0 60 36" width="60" height="36">
            <rect x="6" y="0" width="10" height="36" fill="#ffd60a" opacity="0.9" rx="1"/>
            <rect x="44" y="0" width="10" height="36" fill="#ffd60a" opacity="0.9" rx="1"/>
            <rect x="0" y="14" width="60" height="8" fill="#00bcd4" rx="1"/>
            <rect x="20" y="10" width="20" height="16" fill="#00bcd4" rx="2"/>
            <circle cx="30" cy="18" r="4" fill="#0d1a2d" opacity="0.5"/>
          </svg>
        </div>
      `,
      iconSize: [60, 36],
      iconAnchor: [30, 18]
    });
    
    this.issMarker = L.marker([0, 0], { icon: issIcon }).addTo(this.map);
  }
  
  createFootprintCircle() {
    this.footprintCircle = L.circle([0, 0], {
      radius: 2200000,
      color: '#00bcd4',
      fillColor: '#00bcd4',
      fillOpacity: 0.08,
      weight: 1.5,
      dashArray: '8, 4'
    }).addTo(this.map);
  }
  
  createGroundTrack() {
    this.groundTrack = L.polyline([], {
      color: '#ffd60a',
      weight: 2,
      opacity: 0.5,
      dashArray: '10, 6'
    }).addTo(this.map);
  }
  
  addMapStyles() {
    if (document.getElementById('iss-map-styles')) return;
    
    const style = document.createElement('style');
    style.id = 'iss-map-styles';
    style.textContent = `
      .iss-marker {
        background: transparent !important;
        border: none !important;
      }
      
      .iss-icon {
        filter: drop-shadow(0 0 10px #00bcd4);
        animation: iss-pulse 2s ease-in-out infinite;
      }
      
      @keyframes iss-pulse {
        0%, 100% { filter: drop-shadow(0 0 10px #00bcd4); }
        50% { filter: drop-shadow(0 0 20px #ffd60a); }
      }
      
      .leaflet-container {
        background: #0a1628 !important;
        font-family: 'Courier New', monospace;
      }
      
      .leaflet-control-attribution {
        background: rgba(13, 26, 45, 0.9) !important;
        color: #8b949e !important;
        font-size: 10px !important;
      }
      
      .leaflet-control-attribution a {
        color: #00bcd4 !important;
      }
      
      .leaflet-control-zoom a {
        background: #0d1a2d !important;
        color: #00bcd4 !important;
        border-color: #1a3a5c !important;
      }
      
      .leaflet-control-zoom a:hover {
        background: #1a3a5c !important;
      }
      
      .leaflet-popup-content-wrapper {
        background: #0d1a2d !important;
        border: 1px solid #00bcd4 !important;
        border-radius: 4px !important;
        color: #fff !important;
      }
      
      .leaflet-popup-tip {
        background: #0d1a2d !important;
      }
      
      .iss-data-overlay {
        position: absolute;
        bottom: 20px;
        left: 20px;
        background: rgba(10, 22, 40, 0.95);
        border: 1px solid #1a3a5c;
        border-radius: 4px;
        padding: 12px;
        z-index: 1000;
        min-width: 200px;
        font-family: 'Courier New', monospace;
      }
      
      .iss-data-row {
        display: flex;
        gap: 16px;
        margin-bottom: 8px;
      }
      
      .iss-data-row:last-child {
        margin-bottom: 0;
      }
      
      .iss-data-item label {
        font-size: 0.6rem;
        color: #8b949e;
        letter-spacing: 1px;
        display: block;
        margin-bottom: 2px;
        text-transform: uppercase;
      }
      
      .iss-data-item span {
        font-size: 0.95rem;
        color: #fff;
      }
      
      .iss-map-controls {
        position: absolute;
        top: 12px;
        right: 12px;
        display: flex;
        gap: 6px;
        z-index: 1000;
      }
      
      .iss-ctrl-btn {
        background: rgba(10, 22, 40, 0.9);
        border: 1px solid #1a3a5c;
        color: #8b949e;
        padding: 6px 12px;
        font-family: 'Courier New', monospace;
        font-size: 0.7em;
        cursor: pointer;
        border-radius: 3px;
        transition: all 0.2s;
      }
      
      .iss-ctrl-btn:hover {
        border-color: #00bcd4;
        color: #00bcd4;
      }
      
      .iss-ctrl-btn.active {
        background: rgba(0, 188, 212, 0.2);
        border-color: #00bcd4;
        color: #00bcd4;
      }
      
      .iss-location-display {
        position: absolute;
        top: 12px;
        left: 12px;
        background: rgba(10, 22, 40, 0.95);
        border: 1px solid #1a3a5c;
        border-radius: 4px;
        padding: 10px 14px;
        z-index: 1000;
        font-family: 'Courier New', monospace;
      }
      
      .iss-location-label {
        font-size: 0.6rem;
        color: #8b949e;
        letter-spacing: 1px;
        text-transform: uppercase;
      }
      
      .iss-location-name {
        font-size: 1rem;
        color: #00bcd4;
        margin-top: 4px;
      }
    `;
    document.head.appendChild(style);
  }
  
  addDataOverlay() {
    const overlay = document.createElement('div');
    overlay.className = 'iss-data-overlay';
    overlay.innerHTML = `
      <div class="iss-data-row">
        <div class="iss-data-item">
          <label>Latitude</label>
          <span id="${this.containerId}-lat">--°</span>
        </div>
        <div class="iss-data-item">
          <label>Longitude</label>
          <span id="${this.containerId}-lng">--°</span>
        </div>
      </div>
      <div class="iss-data-row">
        <div class="iss-data-item">
          <label>Altitude</label>
          <span id="${this.containerId}-alt">-- km</span>
        </div>
        <div class="iss-data-item">
          <label>Velocity</label>
          <span id="${this.containerId}-vel">-- km/h</span>
        </div>
      </div>
    `;
    this.container.appendChild(overlay);
    
    // Location display
    const locationDisplay = document.createElement('div');
    locationDisplay.className = 'iss-location-display';
    locationDisplay.innerHTML = `
      <div class="iss-location-label">Currently Over</div>
      <div class="iss-location-name" id="${this.containerId}-location">Calculating...</div>
    `;
    this.container.appendChild(locationDisplay);
  }
  
  addMapControls() {
    const controls = document.createElement('div');
    controls.className = 'iss-map-controls';
    controls.innerHTML = `
      <button class="iss-ctrl-btn ${this.options.showFootprint ? 'active' : ''}" 
              id="${this.containerId}-btn-footprint">Footprint</button>
      <button class="iss-ctrl-btn ${this.options.showGroundTrack ? 'active' : ''}" 
              id="${this.containerId}-btn-track">Track</button>
      <button class="iss-ctrl-btn" id="${this.containerId}-btn-center">Center</button>
    `;
    this.container.appendChild(controls);
    
    // Add event listeners
    document.getElementById(`${this.containerId}-btn-footprint`).addEventListener('click', () => {
      this.toggleFootprint();
    });
    
    document.getElementById(`${this.containerId}-btn-track`).addEventListener('click', () => {
      this.toggleGroundTrack();
    });
    
    document.getElementById(`${this.containerId}-btn-center`).addEventListener('click', () => {
      this.centerOnISS();
    });
  }
  
  async fetchPosition() {
    try {
      const response = await fetch('https://api.wheretheiss.at/v1/satellites/25544');
      if (!response.ok) throw new Error('API request failed');
      
      const data = await response.json();
      
      this.spacecraftPosition = {
        lat: data.latitude,
        lng: data.longitude
      };
      this.altitude = data.altitude;
      this.velocity = data.velocity;
      this.visibility = data.visibility;
      
      // Update marker
      this.issMarker.setLatLng([data.latitude, data.longitude]);
      
      // Update footprint
      if (this.footprintCircle) {
        this.footprintCircle.setLatLng([data.latitude, data.longitude]);
        this.footprintCircle.setRadius(data.footprint * 1000 / 2);
      }
      
      // Update ground track
      if (this.groundTrack) {
        this.positionHistory.push([data.latitude, data.longitude]);
        if (this.positionHistory.length > this.options.trackHistoryLength) {
          this.positionHistory.shift();
        }
        this.groundTrack.setLatLngs(this.positionHistory);
      }
      
      // Update UI
      this.updateDataDisplay(data);
      
      // Update location name
      this.updateLocationName(data.latitude, data.longitude);
      
      // Update popup
      this.updatePopup(data);
      
      // Center if enabled
      if (this.options.centerOnISS) {
        this.map.panTo([data.latitude, data.longitude], { animate: true });
      }
      
      // Emit update event
      this.onPositionUpdate(data);
      
    } catch (error) {
      console.error('Failed to fetch ISS position:', error);
      
      // Try fallback API
      try {
        const fallback = await fetch('http://api.open-notify.org/iss-now.json');
        const fallbackData = await fallback.json();
        
        if (fallbackData.message === 'success') {
          const lat = parseFloat(fallbackData.iss_position.latitude);
          const lng = parseFloat(fallbackData.iss_position.longitude);
          
          this.spacecraftPosition = { lat, lng };
          this.issMarker.setLatLng([lat, lng]);
          
          if (this.footprintCircle) {
            this.footprintCircle.setLatLng([lat, lng]);
          }
        }
      } catch (fallbackError) {
        console.error('Fallback API also failed:', fallbackError);
        if (this.callbacks.onError) {
          this.callbacks.onError(fallbackError);
        }
      }
    }
  }
  
  async fetchCrew() {
    try {
      const response = await fetch('http://api.open-notify.org/astros.json');
      const data = await response.json();
      
      this.crew = data.people.filter(p => p.craft === 'ISS');
      
    } catch (error) {
      console.error('Failed to fetch crew:', error);
    }
  }
  
  updateDataDisplay(data) {
    const lat = data.latitude;
    const lng = data.longitude;
    
    const latEl = document.getElementById(`${this.containerId}-lat`);
    const lngEl = document.getElementById(`${this.containerId}-lng`);
    const altEl = document.getElementById(`${this.containerId}-alt`);
    const velEl = document.getElementById(`${this.containerId}-vel`);
    
    if (latEl) latEl.textContent = Math.abs(lat).toFixed(2) + '°' + (lat >= 0 ? 'N' : 'S');
    if (lngEl) lngEl.textContent = Math.abs(lng).toFixed(2) + '°' + (lng >= 0 ? 'E' : 'W');
    if (altEl) altEl.textContent = Math.round(data.altitude) + ' km';
    if (velEl) velEl.textContent = Math.round(data.velocity).toLocaleString() + ' km/h';
  }
  
  async updateLocationName(lat, lng) {
    try {
      const response = await fetch(`https://api.wheretheiss.at/v1/coordinates/${lat},${lng}`);
      const data = await response.json();
      
      const locationEl = document.getElementById(`${this.containerId}-location`);
      if (locationEl) {
        if (data.timezone_id) {
          const parts = data.timezone_id.split('/');
          const location = parts[parts.length - 1].replace(/_/g, ' ');
          this.locationName = location;
          locationEl.textContent = `${location}${data.country_code ? ' (' + data.country_code + ')' : ''}`;
        } else {
          this.locationName = 'Ocean';
          locationEl.textContent = 'International Waters';
        }
      }
    } catch {
      const locationEl = document.getElementById(`${this.containerId}-location`);
      if (locationEl) {
        locationEl.textContent = `${lat.toFixed(1)}°, ${lng.toFixed(1)}°`;
      }
    }
  }
  
  updatePopup(data) {
    this.issMarker.bindPopup(`
      <strong style="color: #00bcd4;">🛰️ International Space Station</strong><br>
      <hr style="border-color: #1a3a5c; margin: 5px 0;">
      <span style="color: #8b949e;">Lat:</span> ${data.latitude.toFixed(4)}°<br>
      <span style="color: #8b949e;">Lng:</span> ${data.longitude.toFixed(4)}°<br>
      <span style="color: #8b949e;">Alt:</span> ${data.altitude.toFixed(1)} km<br>
      <span style="color: #8b949e;">Speed:</span> ${Math.round(data.velocity).toLocaleString()} km/h<br>
      <span style="color: #8b949e;">Visibility:</span> ${data.visibility}
    `);
  }
  
  toggleFootprint() {
    this.options.showFootprint = !this.options.showFootprint;
    const btn = document.getElementById(`${this.containerId}-btn-footprint`);
    btn?.classList.toggle('active', this.options.showFootprint);
    
    if (this.footprintCircle) {
      if (this.options.showFootprint) {
        this.footprintCircle.addTo(this.map);
      } else {
        this.footprintCircle.remove();
      }
    }
  }
  
  toggleGroundTrack() {
    this.options.showGroundTrack = !this.options.showGroundTrack;
    const btn = document.getElementById(`${this.containerId}-btn-track`);
    btn?.classList.toggle('active', this.options.showGroundTrack);
    
    if (this.groundTrack) {
      if (this.options.showGroundTrack) {
        this.groundTrack.addTo(this.map);
      } else {
        this.groundTrack.remove();
      }
    }
  }
  
  centerOnISS() {
    if (this.spacecraftPosition) {
      this.map.setView([this.spacecraftPosition.lat, this.spacecraftPosition.lng], 3, { animate: true });
    }
  }
  
  setCenterOnISS(enabled) {
    this.options.centerOnISS = enabled;
  }
  
  getCrew() {
    return this.crew;
  }
  
  getState() {
    return {
      ...super.getState(),
      altitude: this.altitude,
      velocity: this.velocity,
      visibility: this.visibility,
      locationName: this.locationName,
      crewCount: this.crew.length
    };
  }
  
  destroy() {
    super.destroy();
    if (this.map) {
      this.map.remove();
      this.map = null;
    }
  }
}

// Export for ES modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ISSMap;
}
