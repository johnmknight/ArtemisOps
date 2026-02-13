/**
 * ArtemisOps - SpaceX Crew Dragon Tracker
 * Overlays live Dragon positions on the ISS Leaflet map.
 * 
 * Uses satellite.js (SGP4) for client-side orbit propagation from TLEs.
 * TLEs fetched from server every hour; positions computed locally at high frequency.
 * 
 * Dependencies: Leaflet (loaded by parent), satellite.js (loaded via script tag)
 */

const DragonTracker = {
  // State
  enabled: false,
  dragons: [],           // TLE data from server
  markers: {},           // Leaflet markers keyed by NORAD ID
  groundTracks: {},      // Predicted orbit polylines
  footprints: {},        // Visibility footprint circles
  layerGroup: null,      // Leaflet layer group for easy toggle
  refreshInterval: null, // Position update timer
  tleInterval: null,     // TLE refresh timer

  // Config
  TLE_REFRESH_MS: 3600000,      // Refresh TLEs every 1 hour
  POSITION_UPDATE_MS: 2000,     // Update positions every 2 seconds
  TRACK_POINTS: 150,            // Points per ground track
  TRACK_ORBITS: 1.5,            // Orbits ahead to show
  DRAGON_COLOR: '#e04040',      // SpaceX red
  DRAGON_COLOR_CARGO: '#f0a030', // Cargo orange

  /**
   * Initialize the tracker. Call once after map is ready.
   * @param {L.Map} map - Leaflet map instance
   */
  init(map) {
    this.map = map;
    this.layerGroup = L.layerGroup();
    console.log('[DragonTracker] Initialized');
  },

  /**
   * Toggle tracker on/off
   */
  async toggle() {
    this.enabled = !this.enabled;

    if (this.enabled) {
      await this.start();
    } else {
      this.stop();
    }

    return this.enabled;
  },

  /**
   * Start tracking — fetch TLEs and begin position updates
   */
  async start() {
    this.enabled = true;
    this.layerGroup.addTo(this.map);

    // Fetch initial TLEs
    await this.fetchTLEs();

    // Start position update loop
    this.updatePositions();
    this.refreshInterval = setInterval(() => this.updatePositions(), this.POSITION_UPDATE_MS);

    // Schedule TLE refresh
    this.tleInterval = setInterval(() => this.fetchTLEs(), this.TLE_REFRESH_MS);

    console.log('[DragonTracker] Started — tracking %d objects', this.dragons.length);
  },

  /**
   * Stop tracking — clear intervals and remove markers
   */
  stop() {
    this.enabled = false;

    if (this.refreshInterval) clearInterval(this.refreshInterval);
    if (this.tleInterval) clearInterval(this.tleInterval);
    this.refreshInterval = null;
    this.tleInterval = null;

    this.layerGroup.clearLayers();
    this.markers = {};
    this.groundTracks = {};
    this.footprints = {};

    console.log('[DragonTracker] Stopped');
  },

  /**
   * Fetch TLE data from our server
   */
  async fetchTLEs() {
    try {
      const resp = await fetch('/api/spacex/dragons');
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);

      const data = await resp.json();
      this.dragons = data.dragons || [];

      console.log('[DragonTracker] Fetched %d Dragon TLEs (cache age: %ds)',
        this.dragons.length, data.cache_age_seconds);

      // Parse TLEs into satellite.js records
      this.dragons.forEach(d => {
        try {
          d.satrec = satellite.twoline2satrec(d.tle.line1, d.tle.line2);
        } catch (e) {
          console.warn('[DragonTracker] Failed to parse TLE for', d.name, e);
          d.satrec = null;
        }
      });

      // Remove markers for dragons no longer in the list
      const activeIds = new Set(this.dragons.map(d => d.norad_id));
      Object.keys(this.markers).forEach(id => {
        if (!activeIds.has(id)) {
          this.layerGroup.removeLayer(this.markers[id]);
          delete this.markers[id];
          if (this.groundTracks[id]) {
            this.layerGroup.removeLayer(this.groundTracks[id]);
            delete this.groundTracks[id];
          }
          if (this.footprints[id]) {
            this.layerGroup.removeLayer(this.footprints[id]);
            delete this.footprints[id];
          }
        }
      });

    } catch (e) {
      console.error('[DragonTracker] Failed to fetch TLEs:', e);
    }
  },

  /**
   * Update all Dragon positions using SGP4 propagation
   */
  updatePositions() {
    if (!this.enabled || !window.satellite) return;

    const now = new Date();

    this.dragons.forEach(dragon => {
      if (!dragon.satrec) return;

      try {
        // Propagate position
        const posVel = satellite.propagate(dragon.satrec, now);
        if (!posVel.position) return;

        // Convert ECI to geodetic
        const gmst = satellite.gstime(now);
        const geo = satellite.eciToGeodetic(posVel.position, gmst);

        const lat = satellite.degreesLat(geo.latitude);
        const lng = satellite.degreesLong(geo.longitude);
        const altKm = geo.height;

        // Calculate velocity (km/s → km/h)
        const v = posVel.velocity;
        const speedKms = Math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z);
        const speedKmh = speedKms * 3600;

        // Update or create marker
        this._updateMarker(dragon, lat, lng, altKm, speedKmh);

        // Update ground track
        this._updateGroundTrack(dragon, now);

      } catch (e) {
        // SGP4 can fail for decayed objects
        console.warn('[DragonTracker] Propagation failed for', dragon.name, e.message);
      }
    });
  },

  /**
   * Create or update a Dragon marker on the map
   */
  _updateMarker(dragon, lat, lng, altKm, speedKmh) {
    const id = dragon.norad_id;
    const color = dragon.type === 'cargo' ? this.DRAGON_COLOR_CARGO : this.DRAGON_COLOR;
    const label = this._shortName(dragon.name);

    if (!this.markers[id]) {
      // Create new marker
      const icon = L.divIcon({
        className: 'dragon-marker',
        html: `
          <div class="dragon-marker-container">
            <div class="dragon-marker-glow" style="border-color:${color}; box-shadow:0 0 8px ${color}40, 0 0 16px ${color}20;"></div>
            <div class="dragon-marker-dot" style="background:${color};"></div>
            <div class="dragon-marker-label" style="color:${color};">${label}</div>
          </div>
        `,
        iconSize: [80, 40],
        iconAnchor: [40, 20],
      });

      const marker = L.marker([lat, lng], { icon, zIndexOffset: 500 });

      marker.bindPopup('', {
        className: 'dragon-popup',
        maxWidth: 220,
      });

      this.layerGroup.addLayer(marker);
      this.markers[id] = marker;

      // Footprint circle
      const footprint = L.circle([lat, lng], {
        radius: this._footprintRadius(altKm),
        color: color,
        fillColor: color,
        fillOpacity: 0.04,
        weight: 1,
        opacity: 0.4,
        dashArray: '6, 4',
        interactive: false,
      });
      this.layerGroup.addLayer(footprint);
      this.footprints[id] = footprint;
    }

    // Update position
    this.markers[id].setLatLng([lat, lng]);
    if (this.footprints[id]) {
      this.footprints[id].setLatLng([lat, lng]);
      this.footprints[id].setRadius(this._footprintRadius(altKm));
    }

    // Update popup content
    this.markers[id].setPopupContent(`
      <strong style="color:${color};">🚀 ${dragon.name}</strong><br>
      <hr style="border-color:#1a3a5c; margin:4px 0;">
      <span style="color:#8b949e;">Type:</span> ${dragon.type === 'crew' ? 'Crew Dragon' : 'Dragon'}<br>
      <span style="color:#8b949e;">NORAD:</span> ${dragon.norad_id}<br>
      <span style="color:#8b949e;">Lat:</span> ${lat.toFixed(4)}°<br>
      <span style="color:#8b949e;">Lng:</span> ${lng.toFixed(4)}°<br>
      <span style="color:#8b949e;">Alt:</span> ${altKm.toFixed(1)} km<br>
      <span style="color:#8b949e;">Speed:</span> ${speedKmh.toFixed(0)} km/h
    `);
  },

  /**
   * Generate and update predicted ground track
   */
  _updateGroundTrack(dragon, now) {
    if (!dragon.satrec) return;
    const id = dragon.norad_id;
    const color = dragon.type === 'cargo' ? this.DRAGON_COLOR_CARGO : this.DRAGON_COLOR;

    // Orbital period estimate (~92 min for LEO)
    const meanMotion = dragon.satrec.no * (1440 / (2 * Math.PI)); // rev/day
    const periodMin = 1440 / meanMotion;
    const totalMin = periodMin * this.TRACK_ORBITS;

    const segments = [];
    let currentSegment = [];

    for (let i = 0; i <= this.TRACK_POINTS; i++) {
      const minutesAhead = (i / this.TRACK_POINTS) * totalMin;
      const futureTime = new Date(now.getTime() + minutesAhead * 60000);

      try {
        const posVel = satellite.propagate(dragon.satrec, futureTime);
        if (!posVel.position) continue;

        const gmst = satellite.gstime(futureTime);
        const geo = satellite.eciToGeodetic(posVel.position, gmst);
        const lat = satellite.degreesLat(geo.latitude);
        const lng = satellite.degreesLong(geo.longitude);

        // Split at dateline
        if (currentSegment.length > 0) {
          const prevLng = currentSegment[currentSegment.length - 1][1];
          if (Math.abs(lng - prevLng) > 180) {
            segments.push(currentSegment);
            currentSegment = [];
          }
        }
        currentSegment.push([lat, lng]);
      } catch {
        // Skip failed propagations
      }
    }
    if (currentSegment.length > 0) segments.push(currentSegment);

    // Update or create polyline
    if (this.groundTracks[id]) {
      this.groundTracks[id].setLatLngs(segments);
    } else {
      const track = L.polyline(segments, {
        color: color,
        weight: 1.5,
        opacity: 0.35,
        dashArray: '4, 6',
        interactive: false,
      });
      this.layerGroup.addLayer(track);
      this.groundTracks[id] = track;
    }
  },

  /**
   * Calculate visibility footprint radius from altitude
   */
  _footprintRadius(altKm) {
    // Horizon distance = sqrt(2 * R * h + h^2), R = 6371 km
    const R = 6371;
    const d = Math.sqrt(2 * R * altKm + altKm * altKm);
    return d * 1000; // meters
  },

  /**
   * Shorten satellite name for map label
   */
  _shortName(name) {
    // "CREW DRAGON 8" → "DRAGON 8", "CREW-9" → "CREW-9"
    return name
      .replace('CREW DRAGON', 'DRAGON')
      .replace('SPACEX ', '')
      .trim();
  },
};
