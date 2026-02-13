/**
 * ArtemisOps - SpaceX Dragon Tracker
 * Overlays live Dragon positions on the ISS Leaflet map.
 *
 * Uses satellite.js (SGP4) for client-side orbit propagation from TLEs.
 * Dragons without TLEs (just launched, docked) shown at ISS position.
 * TLEs fetched from server every hour; positions computed locally at high frequency.
 *
 * Dependencies: Leaflet (loaded by parent), satellite.js (loaded via script tag)
 */

const DragonTracker = {
  // State
  enabled: false,
  dragons: [],           // Dragon data from server (TLE + mission enrichment)
  markers: {},           // Leaflet markers keyed by identifier (norad_id or mission_id)
  groundTracks: {},      // Predicted orbit polylines
  footprints: {},        // Visibility footprint circles
  layerGroup: null,      // Leaflet layer group for easy toggle
  refreshInterval: null, // Position update timer
  tleInterval: null,     // TLE refresh timer
  issPosition: null,     // Latest ISS position for Dragons without TLEs

  // Config
  TLE_REFRESH_MS: 3600000,      // Refresh TLEs every 1 hour
  POSITION_UPDATE_MS: 2000,     // Update positions every 2 seconds
  TRACK_POINTS: 150,            // Points per ground track
  TRACK_ORBITS: 1.5,            // Orbits ahead to show
  DRAGON_CREW_COLOR: '#e04040',   // SpaceX red for crew
  DRAGON_CARGO_COLOR: '#f0a030',  // Orange for cargo
  DRAGON_TRANSIT_COLOR: '#40c0e0', // Cyan for in-transit (no TLE)

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
   * Update ISS position reference (called by parent ISS tracker)
   */
  setISSPosition(lat, lng, alt) {
    this.issPosition = { lat, lng, alt };
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
   * Start tracking — fetch data and begin position updates
   */
  async start() {
    this.enabled = true;
    this.layerGroup.addTo(this.map);

    await this.fetchDragons();

    this.updatePositions();
    this.refreshInterval = setInterval(() => this.updatePositions(), this.POSITION_UPDATE_MS);
    this.tleInterval = setInterval(() => this.fetchDragons(), this.TLE_REFRESH_MS);

    console.log('[DragonTracker] Started — tracking %d Dragons', this.dragons.length);
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
   * Get unique identifier for a Dragon entry
   */
  _dragonId(dragon) {
    return dragon.norad_id || dragon.mission_id || dragon.name;
  },

  /**
   * Get color for a Dragon based on type and tracking mode
   */
  _dragonColor(dragon) {
    if (dragon.tracking === 'iss_position') return this.DRAGON_TRANSIT_COLOR;
    if (dragon.type === 'cargo') return this.DRAGON_CARGO_COLOR;
    return this.DRAGON_CREW_COLOR;
  },

  /**
   * Fetch Dragon data from our server (TLEs + mission enrichment)
   */
  async fetchDragons() {
    try {
      const resp = await fetch('/api/spacex/dragons');
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);

      const data = await resp.json();
      this.dragons = data.dragons || [];

      console.log('[DragonTracker] Fetched %d Dragons (cache age: %ds)',
        this.dragons.length, data.cache_age_seconds);

      // Parse TLEs into satellite.js records
      this.dragons.forEach(d => {
        if (d.tle) {
          try {
            d.satrec = satellite.twoline2satrec(d.tle.line1, d.tle.line2);
          } catch (e) {
            console.warn('[DragonTracker] Failed to parse TLE for', d.name, e);
            d.satrec = null;
          }
        } else {
          d.satrec = null;
        }
      });

      // Remove markers for Dragons no longer in the list
      const activeIds = new Set(this.dragons.map(d => this._dragonId(d)));
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
      console.error('[DragonTracker] Failed to fetch Dragons:', e);
    }
  },

  /**
   * Update all Dragon positions using SGP4 propagation or ISS fallback
   */
  updatePositions() {
    if (!this.enabled) return;

    const now = new Date();

    this.dragons.forEach(dragon => {
      const id = this._dragonId(dragon);

      if (dragon.satrec && window.satellite) {
        // TLE-based tracking via SGP4
        try {
          const posVel = satellite.propagate(dragon.satrec, now);
          if (!posVel.position) return;

          const gmst = satellite.gstime(now);
          const geo = satellite.eciToGeodetic(posVel.position, gmst);

          const lat = satellite.degreesLat(geo.latitude);
          const lng = satellite.degreesLong(geo.longitude);
          const altKm = geo.height;

          const v = posVel.velocity;
          const speedKms = Math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z);
          const speedKmh = speedKms * 3600;

          this._updateMarker(dragon, lat, lng, altKm, speedKmh);
          this._updateGroundTrack(dragon, now);

        } catch (e) {
          console.warn('[DragonTracker] Propagation failed for', dragon.name, e.message);
        }

      } else if (this.issPosition) {
        // No TLE — use ISS position (Dragon is docked or in close proximity)
        const { lat, lng, alt } = this.issPosition;
        // Offset slightly so marker doesn't overlap ISS icon exactly
        const offset = 0.3;
        this._updateMarker(dragon, lat + offset, lng + offset, alt || 420, 27600);
      }
    });
  },

  /**
   * Create or update a Dragon marker on the map
   */
  _updateMarker(dragon, lat, lng, altKm, speedKmh) {
    const id = this._dragonId(dragon);
    const color = this._dragonColor(dragon);
    const label = this._shortName(dragon);
    const isTransit = dragon.tracking === 'iss_position';

    if (!this.markers[id]) {
      // Create new marker
      const pulseClass = isTransit ? 'dragon-marker-pulse' : 'dragon-marker-glow';
      const icon = L.divIcon({
        className: 'dragon-marker',
        html: `
          <div class="dragon-marker-container">
            <div class="${pulseClass}" style="border-color:${color}; box-shadow:0 0 8px ${color}40, 0 0 16px ${color}20;"></div>
            <div class="dragon-marker-dot" style="background:${color};"></div>
            <div class="dragon-marker-label" style="color:${color};">${label}</div>
          </div>
        `,
        iconSize: [100, 40],
        iconAnchor: [50, 20],
      });

      const marker = L.marker([lat, lng], { icon, zIndexOffset: 500 });

      marker.bindPopup('', {
        className: 'dragon-popup',
        maxWidth: 260,
      });

      this.layerGroup.addLayer(marker);
      this.markers[id] = marker;

      // Footprint circle (only for TLE-tracked)
      if (!isTransit) {
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
    }

    // Update position
    this.markers[id].setLatLng([lat, lng]);
    if (this.footprints[id]) {
      this.footprints[id].setLatLng([lat, lng]);
      this.footprints[id].setRadius(this._footprintRadius(altKm));
    }

    // Update popup content
    this.markers[id].setPopupContent(this._buildPopup(dragon, lat, lng, altKm, speedKmh));
  },

  /**
   * Build rich popup HTML for a Dragon
   */
  _buildPopup(dragon, lat, lng, altKm, speedKmh) {
    const color = this._dragonColor(dragon);
    const typeLabel = dragon.type === 'crew' ? 'Crew Dragon' : dragon.type === 'cargo' ? 'Cargo Dragon' : 'Dragon';
    const isTransit = dragon.tracking === 'iss_position';

    let html = `<strong style="color:${color};">🚀 ${dragon.spacecraft || dragon.name}</strong>`;

    if (dragon.mission_name) {
      html += `<br><span style="color:#c0c8d0; font-size:12px;">${dragon.mission_name}</span>`;
    }

    html += `<hr style="border-color:#1a3a5c; margin:4px 0;">`;
    html += `<span style="color:#8b949e;">Type:</span> ${typeLabel}<br>`;

    if (dragon.status) {
      const statusColor = isTransit ? this.DRAGON_TRANSIT_COLOR : '#58a6ff';
      html += `<span style="color:#8b949e;">Status:</span> <span style="color:${statusColor};">${isTransit ? '🔵 In Transit' : '🟢 On Orbit'}</span><br>`;
    }

    if (dragon.norad_id) {
      html += `<span style="color:#8b949e;">NORAD:</span> ${dragon.norad_id}<br>`;
    }

    html += `<span style="color:#8b949e;">Lat:</span> ${lat.toFixed(4)}°<br>`;
    html += `<span style="color:#8b949e;">Lng:</span> ${lng.toFixed(4)}°<br>`;
    html += `<span style="color:#8b949e;">Alt:</span> ${altKm.toFixed(1)} km<br>`;
    html += `<span style="color:#8b949e;">Speed:</span> ${speedKmh.toFixed(0)} km/h`;

    // Crew roster
    if (dragon.crew && dragon.crew.length > 0) {
      html += `<hr style="border-color:#1a3a5c; margin:4px 0;">`;
      html += `<div style="font-size:11px; color:#8b949e; margin-bottom:2px;">CREW (${dragon.crew_count})</div>`;
      dragon.crew.forEach(c => {
        const flag = c.agency ? ` <span style="color:#666; font-size:10px;">${c.agency}</span>` : '';
        html += `<div style="font-size:11px; line-height:1.4;">
          <span style="color:#c0c8d0;">${c.name}</span>
          <span style="color:#666;"> — ${c.role}</span>${flag}
        </div>`;
      });
    }

    if (dragon.agencies) {
      html += `<hr style="border-color:#1a3a5c; margin:4px 0;">`;
      html += `<span style="color:#8b949e; font-size:10px;">Agencies: ${dragon.agencies}</span>`;
    }

    return html;
  },

  /**
   * Generate and update predicted ground track
   */
  _updateGroundTrack(dragon, now) {
    if (!dragon.satrec) return;
    const id = this._dragonId(dragon);
    const color = this._dragonColor(dragon);

    const meanMotion = dragon.satrec.no * (1440 / (2 * Math.PI));
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
    const R = 6371;
    const d = Math.sqrt(2 * R * altKm + altKm * altKm);
    return d * 1000;
  },

  /**
   * Short display name for map label
   */
  _shortName(dragon) {
    if (dragon.mission_name) {
      // "Crew-12" → "CREW-12", "CRS-33" → "CRS-33"
      return dragon.mission_name.toUpperCase().replace('SPACEX ', '');
    }
    // Fall back to TLE name
    return (dragon.name || 'DRAGON')
      .replace('CREW DRAGON', 'DRAGON')
      .replace('SPACEX ', '')
      .trim();
  },

  /**
   * Get summary of tracked Dragons for status display
   */
  getSummary() {
    return {
      total: this.dragons.length,
      crew: this.dragons.filter(d => d.type === 'crew').length,
      cargo: this.dragons.filter(d => d.type === 'cargo').length,
      withTLE: this.dragons.filter(d => d.tle).length,
      inTransit: this.dragons.filter(d => d.tracking === 'iss_position').length,
      dragons: this.dragons.map(d => ({
        name: d.spacecraft || d.name,
        mission: d.mission_name,
        type: d.type,
        tracking: d.tracking,
        crew_count: d.crew_count || 0,
      })),
    };
  },
};
