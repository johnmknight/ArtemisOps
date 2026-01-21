/**
 * ArtemisOps ISS Tracker
 * Real-time International Space Station tracking using Open Notify API and Leaflet.js
 */

class ISSTracker {
  constructor(containerId, options = {}) {
    this.containerId = containerId;
    this.options = {
      updateInterval: 5000,      // Update position every 5 seconds
      showGroundTrack: true,     // Show predicted orbit path
      showFootprint: true,       // Show visibility footprint
      showTerminator: true,      // Show day/night line
      centerOnISS: false,        // Keep ISS centered (can be toggled)
      ...options
    };
    
    this.map = null;
    this.issMarker = null;
    this.footprintCircle = null;
    this.groundTrack = null;
    this.updateTimer = null;
    this.positionHistory = [];
    
    // ISS data
    this.currentPosition = null;
    this.velocity = null;
    this.altitude = null;
    this.visibility = null;
  }
  
  async init() {
    // Create map container if it doesn't exist
    const container = document.getElementById(this.containerId);
    if (!container) {
      console.error(`Container #${this.containerId} not found`);
      return;
    }
    
    // Initialize Leaflet map
    this.map = L.map(this.containerId, {
      center: [20, 0],
      zoom: 2,
      minZoom: 1,
      maxZoom: 8,
      worldCopyJump: true
    });
    
    // Add dark tile layer (matches ArtemisOps theme)
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; OpenStreetMap &copy; CARTO',
      subdomains: 'abcd',
      maxZoom: 19
    }).addTo(this.map);
    
    // Create ISS marker icon
    const issIcon = L.divIcon({
      className: 'iss-marker',
      html: `
        <div class="iss-icon">
          <svg viewBox="0 0 50 30" width="50" height="30">
            <!-- Solar panels -->
            <rect x="5" y="0" width="8" height="30" fill="#ffd60a" opacity="0.8"/>
            <rect x="37" y="0" width="8" height="30" fill="#ffd60a" opacity="0.8"/>
            <!-- Main truss -->
            <rect x="0" y="12" width="50" height="6" fill="#00bcd4"/>
            <!-- Modules -->
            <rect x="18" y="8" width="14" height="14" fill="#00bcd4" rx="2"/>
            <circle cx="25" cy="15" r="4" fill="#fff" opacity="0.5"/>
          </svg>
        </div>
      `,
      iconSize: [50, 30],
      iconAnchor: [25, 15]
    });
    
    // Initialize ISS marker (will be positioned on first update)
    this.issMarker = L.marker([0, 0], { icon: issIcon }).addTo(this.map);
    
    // Initialize footprint circle
    if (this.options.showFootprint) {
      this.footprintCircle = L.circle([0, 0], {
        radius: 2200000, // ~2200km visibility radius
        color: '#00bcd4',
        fillColor: '#00bcd4',
        fillOpacity: 0.1,
        weight: 1,
        dashArray: '5, 5'
      }).addTo(this.map);
    }
    
    // Initialize ground track
    if (this.options.showGroundTrack) {
      this.groundTrack = L.polyline([], {
        color: '#ffd60a',
        weight: 2,
        opacity: 0.6,
        dashArray: '10, 5'
      }).addTo(this.map);
    }
    
    // Add custom CSS for ISS marker
    this.addStyles();
    
    // Fetch initial position
    await this.updatePosition();
    
    // Start auto-update
    this.startTracking();
    
    return this;
  }
  
  addStyles() {
    if (document.getElementById('iss-tracker-styles')) return;
    
    const style = document.createElement('style');
    style.id = 'iss-tracker-styles';
    style.textContent = `
      .iss-marker {
        background: transparent;
        border: none;
      }
      
      .iss-icon {
        filter: drop-shadow(0 0 10px #00bcd4);
        animation: iss-pulse 2s ease-in-out infinite;
      }
      
      @keyframes iss-pulse {
        0%, 100% { filter: drop-shadow(0 0 10px #00bcd4); }
        50% { filter: drop-shadow(0 0 20px #ffd60a); }
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
      
      .leaflet-popup-content {
        font-family: 'Courier New', monospace;
        font-size: 12px;
      }
      
      .leaflet-container {
        background: #0a1628;
      }
      
      .leaflet-control-attribution {
        background: rgba(13, 26, 45, 0.8) !important;
        color: #8b949e !important;
      }
      
      .leaflet-control-attribution a {
        color: #00bcd4 !important;
      }
    `;
    document.head.appendChild(style);
  }
  
  async updatePosition() {
    try {
      // Fetch from Where The ISS At API (more data)
      const response = await fetch('https://api.wheretheiss.at/v1/satellites/25544');
      if (!response.ok) throw new Error('API request failed');
      
      const data = await response.json();
      
      this.currentPosition = {
        lat: data.latitude,
        lng: data.longitude
      };
      this.altitude = data.altitude;
      this.velocity = data.velocity;
      this.visibility = data.visibility;
      
      // Update marker position
      this.issMarker.setLatLng([this.currentPosition.lat, this.currentPosition.lng]);
      
      // Update footprint
      if (this.footprintCircle) {
        this.footprintCircle.setLatLng([this.currentPosition.lat, this.currentPosition.lng]);
        // Adjust footprint radius based on altitude
        const footprintRadius = data.footprint * 1000 / 2; // Convert km to m
        this.footprintCircle.setRadius(footprintRadius);
      }
      
      // Update ground track
      if (this.groundTrack) {
        this.positionHistory.push([this.currentPosition.lat, this.currentPosition.lng]);
        // Keep last 100 points
        if (this.positionHistory.length > 100) {
          this.positionHistory.shift();
        }
        this.groundTrack.setLatLngs(this.positionHistory);
      }
      
      // Center map on ISS if option enabled
      if (this.options.centerOnISS) {
        this.map.panTo([this.currentPosition.lat, this.currentPosition.lng], { animate: true });
      }
      
      // Update popup content
      this.issMarker.bindPopup(`
        <strong style="color: #00bcd4;">🛰️ International Space Station</strong><br>
        <hr style="border-color: #1a3a5c; margin: 5px 0;">
        <span style="color: #8b949e;">Latitude:</span> ${this.currentPosition.lat.toFixed(4)}°<br>
        <span style="color: #8b949e;">Longitude:</span> ${this.currentPosition.lng.toFixed(4)}°<br>
        <span style="color: #8b949e;">Altitude:</span> ${this.altitude.toFixed(1)} km<br>
        <span style="color: #8b949e;">Velocity:</span> ${this.velocity.toFixed(0)} km/h<br>
        <span style="color: #8b949e;">Visibility:</span> ${this.visibility}
      `);
      
      // Emit update event
      this.onPositionUpdate(data);
      
    } catch (error) {
      console.error('Failed to fetch ISS position:', error);
      
      // Try fallback API (Open Notify)
      try {
        const fallbackResponse = await fetch('http://api.open-notify.org/iss-now.json');
        const fallbackData = await fallbackResponse.json();
        
        if (fallbackData.message === 'success') {
          this.currentPosition = {
            lat: parseFloat(fallbackData.iss_position.latitude),
            lng: parseFloat(fallbackData.iss_position.longitude)
          };
          this.issMarker.setLatLng([this.currentPosition.lat, this.currentPosition.lng]);
          
          if (this.footprintCircle) {
            this.footprintCircle.setLatLng([this.currentPosition.lat, this.currentPosition.lng]);
          }
        }
      } catch (fallbackError) {
        console.error('Fallback API also failed:', fallbackError);
      }
    }
  }
  
  // Override this method to handle position updates
  onPositionUpdate(data) {
    // Can be overridden by consumer
    const event = new CustomEvent('issPositionUpdate', { detail: data });
    document.dispatchEvent(event);
  }
  
  startTracking() {
    if (this.updateTimer) return;
    this.updateTimer = setInterval(() => this.updatePosition(), this.options.updateInterval);
  }
  
  stopTracking() {
    if (this.updateTimer) {
      clearInterval(this.updateTimer);
      this.updateTimer = null;
    }
  }
  
  centerOnISS() {
    if (this.currentPosition) {
      this.map.setView([this.currentPosition.lat, this.currentPosition.lng], 3);
    }
  }
  
  toggleFootprint(show) {
    if (this.footprintCircle) {
      if (show) {
        this.footprintCircle.addTo(this.map);
      } else {
        this.footprintCircle.remove();
      }
    }
  }
  
  toggleGroundTrack(show) {
    if (this.groundTrack) {
      if (show) {
        this.groundTrack.addTo(this.map);
      } else {
        this.groundTrack.remove();
      }
    }
  }
  
  setCenterOnISS(enabled) {
    this.options.centerOnISS = enabled;
  }
  
  getPosition() {
    return {
      ...this.currentPosition,
      altitude: this.altitude,
      velocity: this.velocity,
      visibility: this.visibility
    };
  }
  
  destroy() {
    this.stopTracking();
    if (this.map) {
      this.map.remove();
      this.map = null;
    }
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ISSTracker;
}
