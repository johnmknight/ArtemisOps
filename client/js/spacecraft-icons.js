/**
 * ArtemisOps Spacecraft Icons
 * SVG icon definitions for spacecraft used in Artemis missions
 * Based on official reference imagery from NASA and SpaceX
 */

const SpacecraftIcons = {
  /**
   * Get an SVG icon for a spacecraft
   * @param {string} type - Spacecraft type: 'iss', 'orion', 'starship-hls', 'crew-dragon', 'lunar-lander'
   * @param {number} size - Icon size in pixels (default: 64)
   * @param {string} color - Stroke color (default: '#00bcd4' for dark UI)
   * @returns {string} SVG markup
   */
  getIcon(type, size = 64, color = '#00bcd4') {
    const icons = {
      'iss': this.iss,
      'orion': this.orion,
      'orion-esm': this.orionESM,
      'starship-hls': this.starshipHLS,
      'crew-dragon': this.crewDragon,
      'lunar-lander': this.lunarLander,
      'sls': this.sls
    };
    
    const iconFn = icons[type.toLowerCase()];
    if (!iconFn) {
      console.warn(`Unknown spacecraft type: ${type}`);
      return this.defaultIcon(size, color);
    }
    
    return iconFn.call(this, size, color);
  },

  /**
   * ISS - International Space Station
   * Features: 8 solar arrays in 4 pairs, horizontal truss, central module cluster
   */
  iss(size = 64, color = '#00bcd4') {
    // Determine stroke width based on size
    const strokeWidth = size <= 48 ? 5 : size <= 72 ? 3.5 : size <= 96 ? 2.5 : 2;
    const showDetails = size > 72;
    
    return `<svg viewBox="0 0 180 100" width="${size}" height="${Math.round(size * 100/180)}">
      <g stroke="${color}" fill="none" stroke-width="${strokeWidth}" stroke-linecap="round" stroke-linejoin="round">
        <!-- Main Truss (ITS) -->
        <line x1="8" y1="50" x2="172" y2="50" stroke-width="${strokeWidth + 1}"/>
        
        <!-- P6 Solar Arrays (far port) -->
        <rect x="8" y="12" width="16" height="34"/>
        <rect x="8" y="54" width="16" height="34"/>
        ${showDetails ? `
        <line x1="8" y1="22" x2="24" y2="22" stroke-width="0.6" opacity="0.5"/>
        <line x1="8" y1="32" x2="24" y2="32" stroke-width="0.6" opacity="0.5"/>
        <line x1="16" y1="12" x2="16" y2="46" stroke-width="0.6" opacity="0.5"/>
        <line x1="8" y1="64" x2="24" y2="64" stroke-width="0.6" opacity="0.5"/>
        <line x1="8" y1="74" x2="24" y2="74" stroke-width="0.6" opacity="0.5"/>
        <line x1="16" y1="54" x2="16" y2="88" stroke-width="0.6" opacity="0.5"/>
        ` : ''}
        
        <!-- P4 Solar Arrays -->
        <rect x="36" y="12" width="16" height="34"/>
        <rect x="36" y="54" width="16" height="34"/>
        ${showDetails ? `
        <line x1="36" y1="22" x2="52" y2="22" stroke-width="0.6" opacity="0.5"/>
        <line x1="36" y1="32" x2="52" y2="32" stroke-width="0.6" opacity="0.5"/>
        <line x1="44" y1="12" x2="44" y2="46" stroke-width="0.6" opacity="0.5"/>
        <line x1="36" y1="64" x2="52" y2="64" stroke-width="0.6" opacity="0.5"/>
        <line x1="36" y1="74" x2="52" y2="74" stroke-width="0.6" opacity="0.5"/>
        <line x1="44" y1="54" x2="44" y2="88" stroke-width="0.6" opacity="0.5"/>
        ` : ''}
        
        <!-- S4 Solar Arrays -->
        <rect x="128" y="12" width="16" height="34"/>
        <rect x="128" y="54" width="16" height="34"/>
        ${showDetails ? `
        <line x1="128" y1="22" x2="144" y2="22" stroke-width="0.6" opacity="0.5"/>
        <line x1="128" y1="32" x2="144" y2="32" stroke-width="0.6" opacity="0.5"/>
        <line x1="136" y1="12" x2="136" y2="46" stroke-width="0.6" opacity="0.5"/>
        <line x1="128" y1="64" x2="144" y2="64" stroke-width="0.6" opacity="0.5"/>
        <line x1="128" y1="74" x2="144" y2="74" stroke-width="0.6" opacity="0.5"/>
        <line x1="136" y1="54" x2="136" y2="88" stroke-width="0.6" opacity="0.5"/>
        ` : ''}
        
        <!-- S6 Solar Arrays (far starboard) -->
        <rect x="156" y="12" width="16" height="34"/>
        <rect x="156" y="54" width="16" height="34"/>
        ${showDetails ? `
        <line x1="156" y1="22" x2="172" y2="22" stroke-width="0.6" opacity="0.5"/>
        <line x1="156" y1="32" x2="172" y2="32" stroke-width="0.6" opacity="0.5"/>
        <line x1="164" y1="12" x2="164" y2="46" stroke-width="0.6" opacity="0.5"/>
        <line x1="156" y1="64" x2="172" y2="64" stroke-width="0.6" opacity="0.5"/>
        <line x1="156" y1="74" x2="172" y2="74" stroke-width="0.6" opacity="0.5"/>
        <line x1="164" y1="54" x2="164" y2="88" stroke-width="0.6" opacity="0.5"/>
        ` : ''}
        
        <!-- Central Module Cluster -->
        <rect x="75" y="40" width="30" height="20" rx="2"/>
        ${showDetails ? `
        <circle cx="90" cy="50" r="4" fill="${color}" opacity="0.3"/>
        <!-- Perpendicular modules -->
        <rect x="84" y="28" width="12" height="12" rx="1"/>
        <rect x="84" y="60" width="12" height="12" rx="1"/>
        <!-- Docking port -->
        <line x1="90" y1="24" x2="90" y2="28"/>
        <line x1="86" y1="24" x2="94" y2="24"/>
        ` : ''}
      </g>
    </svg>`;
  },

  /**
   * Starship HLS - SpaceX Human Landing System
   * Features: Tall cylindrical body, rounded nose, landing legs, window section
   */
  starshipHLS(size = 64, color = '#00bcd4') {
    const strokeWidth = size <= 36 ? 7 : size <= 48 ? 5 : size <= 72 ? 3.5 : 2;
    const showDetails = size > 48;
    
    return `<svg viewBox="0 0 60 160" width="${Math.round(size * 60/160)}" height="${size}">
      <g stroke="${color}" fill="none" stroke-width="${strokeWidth}" stroke-linecap="round" stroke-linejoin="round">
        <!-- Main body - tall cylinder with nose cone -->
        <path d="M18,145 L18,35 Q18,10 30,10 Q42,10 42,35 L42,145"/>
        
        <!-- Base of body -->
        <line x1="18" y1="145" x2="42" y2="145"/>
        
        ${showDetails ? `
        <!-- Nose tip detail -->
        <ellipse cx="30" cy="12" rx="10" ry="3" stroke-width="1.5" opacity="0.7"/>
        
        <!-- Dark band (below nose) -->
        <line x1="18" y1="42" x2="42" y2="42" stroke-width="1" opacity="0.5"/>
        <line x1="18" y1="52" x2="42" y2="52" stroke-width="1" opacity="0.5"/>
        
        <!-- Window/crew area -->
        <rect x="24" y="28" width="12" height="10" rx="2" stroke-width="1.5"/>
        <circle cx="30" cy="33" r="3" stroke-width="1"/>
        <circle cx="30" cy="33" r="1.5" fill="${color}" opacity="0.3"/>
        
        <!-- Body panel lines -->
        <line x1="18" y1="75" x2="42" y2="75" stroke-width="0.8" opacity="0.4"/>
        <line x1="18" y1="105" x2="42" y2="105" stroke-width="0.8" opacity="0.4"/>
        <line x1="18" y1="130" x2="42" y2="130" stroke-width="0.8" opacity="0.4"/>
        
        <!-- Footpads -->
        <ellipse cx="4" cy="158" rx="4" ry="2" stroke-width="1.5"/>
        <ellipse cx="56" cy="158" rx="4" ry="2" stroke-width="1.5"/>
        
        <!-- Engine area hint -->
        <path d="M22,145 L22,150 Q22,152 30,152 Q38,152 38,150 L38,145" stroke-width="1" opacity="0.6"/>
        ` : ''}
        
        <!-- Landing legs -->
        <line x1="18" y1="138" x2="${showDetails ? '4' : '6'}" y2="${showDetails ? '158' : '156'}" stroke-width="${Math.max(strokeWidth - 0.5, 2)}"/>
        <line x1="42" y1="138" x2="${showDetails ? '56' : '54'}" y2="${showDetails ? '158' : '156'}" stroke-width="${Math.max(strokeWidth - 0.5, 2)}"/>
      </g>
    </svg>`;
  },

  /**
   * Orion with European Service Module (ESM)
   * Features: Gumdrop crew module, cylindrical service module, 4 X-configuration solar arrays
   */
  orionESM(size = 64, color = '#00bcd4') {
    const strokeWidth = size <= 32 ? 4 : size <= 48 ? 3 : size <= 64 ? 2.5 : 2;
    const showDetails = size > 48;
    
    return `<svg viewBox="0 0 100 100" width="${size}" height="${size}">
      <g stroke="${color}" fill="none" stroke-width="${strokeWidth}" stroke-linecap="round" stroke-linejoin="round">
        <!-- Docking port at nose -->
        <ellipse cx="50" cy="12" rx="6" ry="2" stroke-width="1.5"/>
        
        <!-- Crew Module (gumdrop shape) -->
        <path d="M35,35 Q35,15 50,15 Q65,15 65,35 L60,45 L40,45 Z" stroke-width="${strokeWidth}"/>
        ${showDetails ? `<circle cx="50" cy="28" r="3" fill="${color}" opacity="0.3"/>` : ''}
        
        <!-- Service Module (cylindrical) -->
        <rect x="38" y="45" width="24" height="30" rx="2"/>
        ${showDetails ? `
        <!-- SM detail lines -->
        <line x1="38" y1="52" x2="62" y2="52" stroke-width="0.8" opacity="0.4"/>
        <line x1="38" y1="60" x2="62" y2="60" stroke-width="0.8" opacity="0.4"/>
        <line x1="38" y1="68" x2="62" y2="68" stroke-width="0.8" opacity="0.4"/>
        ` : ''}
        
        <!-- Engine bell at base -->
        <path d="M44,75 L44,82 Q44,88 50,88 Q56,88 56,82 L56,75" stroke-width="1.5"/>
        
        <!-- 4 Solar Arrays in X-configuration -->
        <!-- Upper Left -->
        <rect x="10" y="30" width="16" height="14" transform="rotate(-30 18 37)"/>
        <!-- Upper Right -->
        <rect x="74" y="30" width="16" height="14" transform="rotate(30 82 37)"/>
        <!-- Lower Left -->
        <rect x="10" y="56" width="16" height="14" transform="rotate(30 18 63)"/>
        <!-- Lower Right -->
        <rect x="74" y="56" width="16" height="14" transform="rotate(-30 82 63)"/>
        
        ${showDetails ? `
        <!-- Solar panel grid detail -->
        <line x1="14" y1="37" x2="22" y2="37" stroke-width="0.5" opacity="0.4" transform="rotate(-30 18 37)"/>
        <line x1="18" y1="30" x2="18" y2="44" stroke-width="0.5" opacity="0.4" transform="rotate(-30 18 37)"/>
        <line x1="78" y1="37" x2="86" y2="37" stroke-width="0.5" opacity="0.4" transform="rotate(30 82 37)"/>
        <line x1="82" y1="30" x2="82" y2="44" stroke-width="0.5" opacity="0.4" transform="rotate(30 82 37)"/>
        ` : ''}
      </g>
    </svg>`;
  },

  /**
   * Orion Crew Module only (no ESM)
   */
  orion(size = 64, color = '#00bcd4') {
    const strokeWidth = size <= 32 ? 4 : size <= 48 ? 3 : 2;
    
    return `<svg viewBox="0 0 60 50" width="${size}" height="${Math.round(size * 50/60)}">
      <g stroke="${color}" fill="none" stroke-width="${strokeWidth}" stroke-linecap="round" stroke-linejoin="round">
        <!-- Docking port -->
        <ellipse cx="30" cy="8" rx="5" ry="2"/>
        
        <!-- Crew Module (gumdrop/cone shape) -->
        <path d="M15,40 Q15,10 30,10 Q45,10 45,40 L40,48 L20,48 Z"/>
        
        <!-- Windows -->
        <circle cx="25" cy="25" r="2.5" fill="${color}" opacity="0.3"/>
        <circle cx="35" cy="25" r="2.5" fill="${color}" opacity="0.3"/>
        
        <!-- Heat shield line -->
        <line x1="20" y1="48" x2="40" y2="48" stroke-width="${strokeWidth + 0.5}"/>
      </g>
    </svg>`;
  },

  /**
   * Crew Dragon
   * Features: Gumdrop capsule, trunk with diagonal solar panel fins
   */
  crewDragon(size = 64, color = '#00bcd4') {
    const strokeWidth = size <= 32 ? 4 : size <= 48 ? 3 : 2;
    const showDetails = size > 48;
    
    return `<svg viewBox="0 0 70 100" width="${Math.round(size * 70/100)}" height="${size}">
      <g stroke="${color}" fill="none" stroke-width="${strokeWidth}" stroke-linecap="round" stroke-linejoin="round">
        <!-- Docking port at nose -->
        <ellipse cx="35" cy="10" rx="6" ry="2.5"/>
        
        <!-- Capsule (gumdrop shape) -->
        <path d="M20,45 Q20,12 35,12 Q50,12 50,45 L47,55 L23,55 Z"/>
        
        <!-- Window -->
        ${showDetails ? `<circle cx="35" cy="30" r="4" fill="${color}" opacity="0.3"/>` : ''}
        
        <!-- Trunk section -->
        <rect x="22" y="55" width="26" height="35" rx="1"/>
        ${showDetails ? `
        <!-- Trunk detail lines -->
        <line x1="22" y1="65" x2="48" y2="65" stroke-width="0.8" opacity="0.4"/>
        <line x1="22" y1="75" x2="48" y2="75" stroke-width="0.8" opacity="0.4"/>
        <line x1="22" y1="85" x2="48" y2="85" stroke-width="0.8" opacity="0.4"/>
        ` : ''}
        
        <!-- Diagonal solar panel fins (as seen in reference photo) -->
        <!-- Left fin - angled down-left -->
        <line x1="22" y1="60" x2="8" y2="85" stroke-width="${strokeWidth}"/>
        <line x1="22" y1="70" x2="10" y2="90" stroke-width="${strokeWidth - 0.5}"/>
        
        <!-- Right fin - angled down-right -->
        <line x1="48" y1="60" x2="62" y2="85" stroke-width="${strokeWidth}"/>
        <line x1="48" y1="70" x2="60" y2="90" stroke-width="${strokeWidth - 0.5}"/>
      </g>
    </svg>`;
  },

  /**
   * Lunar Lander (Apollo-style)
   * Features: Ascent stage cabin, octagonal descent stage, 4 landing legs
   */
  lunarLander(size = 64, color = '#00bcd4') {
    const strokeWidth = size <= 32 ? 4 : size <= 48 ? 3 : 2;
    const showDetails = size > 48;
    
    return `<svg viewBox="0 0 80 90" width="${Math.round(size * 80/90)}" height="${size}">
      <g stroke="${color}" fill="none" stroke-width="${strokeWidth}" stroke-linecap="round" stroke-linejoin="round">
        <!-- Antenna/hatch at top -->
        <line x1="40" y1="5" x2="40" y2="15"/>
        <line x1="35" y1="5" x2="45" y2="5"/>
        
        <!-- Ascent stage cabin -->
        <rect x="28" y="15" width="24" height="20" rx="3"/>
        ${showDetails ? `
        <!-- Windows -->
        <circle cx="34" cy="25" r="3" fill="${color}" opacity="0.3"/>
        <circle cx="46" cy="25" r="3" fill="${color}" opacity="0.3"/>
        ` : ''}
        
        <!-- Descent stage (octagonal body) -->
        <path d="M22,35 L22,55 L28,65 L52,65 L58,55 L58,35 L52,35 L28,35 Z"/>
        ${showDetails ? `
        <!-- Descent stage detail -->
        <line x1="25" y1="45" x2="55" y2="45" stroke-width="0.8" opacity="0.4"/>
        <line x1="25" y1="55" x2="55" y2="55" stroke-width="0.8" opacity="0.4"/>
        ` : ''}
        
        <!-- Descent engine -->
        <ellipse cx="40" cy="68" rx="6" ry="3"/>
        
        <!-- Landing legs (4 legs, showing 2 from side view) -->
        <line x1="22" y1="55" x2="8" y2="82" stroke-width="${strokeWidth}"/>
        <line x1="58" y1="55" x2="72" y2="82" stroke-width="${strokeWidth}"/>
        
        <!-- Footpads -->
        <ellipse cx="8" cy="84" rx="6" ry="3"/>
        <ellipse cx="72" cy="84" rx="6" ry="3"/>
      </g>
    </svg>`;
  },

  /**
   * SLS - Space Launch System
   * Features: Core stage, SRBs, Orion on top
   */
  sls(size = 64, color = '#00bcd4') {
    const strokeWidth = size <= 32 ? 4 : size <= 48 ? 3 : 2;
    const showDetails = size > 48;
    
    return `<svg viewBox="0 0 60 160" width="${Math.round(size * 60/160)}" height="${size}">
      <g stroke="${color}" fill="none" stroke-width="${strokeWidth}" stroke-linecap="round" stroke-linejoin="round">
        <!-- Orion on top -->
        <path d="M25,20 Q25,8 30,8 Q35,8 35,20 L33,25 L27,25 Z"/>
        <ellipse cx="30" cy="10" rx="3" ry="1" stroke-width="1"/>
        
        <!-- Launch Escape System tower -->
        <line x1="30" y1="8" x2="30" y2="2"/>
        <line x1="26" y1="5" x2="30" y2="2"/>
        <line x1="34" y1="5" x2="30" y2="2"/>
        
        <!-- Core stage -->
        <rect x="22" y="25" width="16" height="110" rx="2"/>
        ${showDetails ? `
        <line x1="22" y1="50" x2="38" y2="50" stroke-width="0.8" opacity="0.4"/>
        <line x1="22" y1="80" x2="38" y2="80" stroke-width="0.8" opacity="0.4"/>
        <line x1="22" y1="110" x2="38" y2="110" stroke-width="0.8" opacity="0.4"/>
        ` : ''}
        
        <!-- Left SRB -->
        <rect x="8" y="40" width="10" height="95" rx="1"/>
        <path d="M8,135 L8,145 Q8,150 13,150 Q18,150 18,145 L18,135" stroke-width="1.5"/>
        
        <!-- Right SRB -->
        <rect x="42" y="40" width="10" height="95" rx="1"/>
        <path d="M42,135 L42,145 Q42,150 47,150 Q52,150 52,145 L52,135" stroke-width="1.5"/>
        
        <!-- RS-25 engines -->
        <ellipse cx="26" cy="138" rx="3" ry="2"/>
        <ellipse cx="34" cy="138" rx="3" ry="2"/>
        <path d="M23,138 L23,148 Q23,152 30,152 Q37,152 37,148 L37,138" stroke-width="1" opacity="0.7"/>
      </g>
    </svg>`;
  },

  /**
   * Default/fallback icon (generic spacecraft)
   */
  defaultIcon(size = 64, color = '#00bcd4') {
    const strokeWidth = size <= 32 ? 3 : 2;
    
    return `<svg viewBox="0 0 50 50" width="${size}" height="${size}">
      <g stroke="${color}" fill="none" stroke-width="${strokeWidth}" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="25" cy="25" r="18"/>
        <circle cx="25" cy="25" r="8" fill="${color}" opacity="0.2"/>
        <line x1="25" y1="7" x2="25" y2="3"/>
        <line x1="43" y1="25" x2="47" y2="25"/>
        <line x1="25" y1="43" x2="25" y2="47"/>
        <line x1="7" y1="25" x2="3" y2="25"/>
      </g>
    </svg>`;
  },

  /**
   * Create an icon element
   * @param {string} type - Spacecraft type
   * @param {number} size - Size in pixels
   * @param {string} color - Color
   * @returns {HTMLElement} DOM element containing the SVG
   */
  createElement(type, size = 64, color = '#00bcd4') {
    const wrapper = document.createElement('span');
    wrapper.className = 'spacecraft-icon';
    wrapper.innerHTML = this.getIcon(type, size, color);
    wrapper.style.display = 'inline-block';
    wrapper.style.lineHeight = '0';
    return wrapper;
  },

  /**
   * Get all available icon types
   * @returns {string[]} Array of icon type names
   */
  getAvailableTypes() {
    return ['iss', 'orion', 'orion-esm', 'starship-hls', 'crew-dragon', 'lunar-lander', 'sls'];
  }
};

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
  module.exports = SpacecraftIcons;
}
