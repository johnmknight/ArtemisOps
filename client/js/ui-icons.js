/**
 * ArtemisOps UI Icons
 * SVG icon set in aerospace/mission control style
 * Matches the technical line-art style of spacecraft icons
 */

const UIIcons = {
  /**
   * Get an SVG icon
   * @param {string} name - Icon name
   * @param {number} size - Icon size in pixels (default: 24)
   * @param {string} color - Stroke color (default: 'currentColor')
   * @returns {string} SVG markup
   */
  get(name, size = 24, color = 'currentColor') {
    const icon = this.icons[name];
    if (!icon) {
      console.warn(`Unknown icon: ${name}`);
      return this.icons.default(size, color);
    }
    return icon(size, color);
  },

  /**
   * Create a DOM element with the icon
   */
  createElement(name, size = 24, color = 'currentColor') {
    const wrapper = document.createElement('span');
    wrapper.className = 'ui-icon';
    wrapper.innerHTML = this.get(name, size, color);
    wrapper.style.display = 'inline-flex';
    wrapper.style.alignItems = 'center';
    wrapper.style.justifyContent = 'center';
    wrapper.style.lineHeight = '0';
    return wrapper;
  },

  icons: {
    // ===== NAVIGATION ICONS =====
    
    /**
     * Mission/Launch icon - rocket with trajectory
     */
    mission: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 2L12 4"/>
        <path d="M8 8L12 4L16 8"/>
        <rect x="9" y="8" width="6" height="10" rx="1"/>
        <path d="M9 14L6 18L9 17"/>
        <path d="M15 14L18 18L15 17"/>
        <path d="M10 18L10 20L12 22L14 20L14 18"/>
        <path d="M11 22L11 23" stroke-dasharray="1 1"/>
        <path d="M13 22L13 23" stroke-dasharray="1 1"/>
      </svg>`,

    /**
     * Crew icon - astronaut helmet profile
     */
    crew: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="11" r="7"/>
        <path d="M7 9C7 9 8 7 12 7C16 7 17 9 17 9L17 13C17 13 16 15 12 15C8 15 7 13 7 13Z"/>
        <path d="M9 10L10 11" stroke-width="1" opacity="0.5"/>
        <path d="M8 17L8 19C8 20 9 21 12 21C15 21 16 20 16 19L16 17"/>
        <circle cx="18" cy="11" r="1" stroke-width="1"/>
      </svg>`,

    /**
     * Info icon - technical schematic style
     */
    info: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="9"/>
        <circle cx="12" cy="12" r="6" stroke-width="0.75" opacity="0.4"/>
        <circle cx="12" cy="8" r="1" fill="${color}"/>
        <path d="M12 11L12 17"/>
        <path d="M12 3L12 5" stroke-width="1"/>
        <path d="M12 19L12 21" stroke-width="1"/>
        <path d="M3 12L5 12" stroke-width="1"/>
        <path d="M19 12L21 12" stroke-width="1"/>
      </svg>`,

    /**
     * Timeline icon - horizontal sequence
     */
    timeline: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <line x1="3" y1="12" x2="21" y2="12"/>
        <circle cx="6" cy="12" r="2" fill="${color}"/>
        <circle cx="12" cy="12" r="2"/>
        <circle cx="18" cy="12" r="2"/>
        <line x1="6" y1="8" x2="6" y2="10"/>
        <line x1="12" y1="14" x2="12" y2="16"/>
        <line x1="18" y1="8" x2="18" y2="10"/>
        <line x1="4" y1="6" x2="8" y2="6" stroke-width="1"/>
        <line x1="10" y1="18" x2="14" y2="18" stroke-width="1"/>
        <line x1="16" y1="6" x2="20" y2="6" stroke-width="1"/>
      </svg>`,

    /**
     * Countdown/Timer icon
     */
    countdown: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="13" r="8"/>
        <circle cx="12" cy="13" r="5" stroke-width="0.75" opacity="0.4"/>
        <line x1="12" y1="13" x2="12" y2="9"/>
        <line x1="12" y1="13" x2="15" y2="15"/>
        <rect x="10" y="2" width="4" height="3" rx="0.5"/>
        <path d="M5 5L7 7"/>
        <path d="M19 5L17 7"/>
      </svg>`,

    /**
     * Weather icon - atmospheric monitoring
     */
    weather: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M6 16C4 16 2 14.5 2 12.5C2 10.5 3.5 9 5.5 9C5.5 6 8 4 11 4C14 4 16 6 16.5 8.5C18.5 8.5 20 10 20 12C20 14 18.5 15.5 16.5 15.5"/>
        <path d="M4 19L10 19"/>
        <path d="M6 21L14 21"/>
        <path d="M8 17L16 17"/>
        <circle cx="8" cy="12" r="0.75" fill="${color}"/>
        <circle cx="12" cy="10" r="0.75" fill="${color}"/>
      </svg>`,

    /**
     * Status/Dashboard icon
     */
    status: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <rect x="2" y="3" width="20" height="14" rx="1"/>
        <circle cx="7" cy="9" r="2"/>
        <path d="M7 9L8 8"/>
        <circle cx="17" cy="9" r="2"/>
        <path d="M17 9L17 7.5"/>
        <rect x="11" y="7" width="3" height="1" fill="${color}"/>
        <rect x="11" y="9" width="2" height="1" fill="${color}" opacity="0.6"/>
        <rect x="11" y="11" width="3" height="1" fill="${color}"/>
        <path d="M8 17L8 20"/>
        <path d="M16 17L16 20"/>
        <path d="M6 20L18 20"/>
      </svg>`,

    /**
     * Notification bell - technical style
     */
    notification: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 3C12 3 8 3 8 8L8 14L5 17L19 17L16 14L16 8C16 3 12 3 12 3"/>
        <path d="M12 1L12 3"/>
        <path d="M10 20C10 21 11 22 12 22C13 22 14 21 14 20"/>
        <path d="M19 8C20 8 21 9 21 11" stroke-width="1" opacity="0.5"/>
        <path d="M5 8C4 8 3 9 3 11" stroke-width="1" opacity="0.5"/>
      </svg>`,

    /**
     * Settings/Gear icon
     */
    settings: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 2L13 4L15 3.5L15.5 5.5L17.5 5.5L17 7.5L19 8.5L18 10.5L20 12L18 13.5L19 15.5L17 16.5L17.5 18.5L15.5 18.5L15 20.5L13 20L12 22L11 20L9 20.5L8.5 18.5L6.5 18.5L7 16.5L5 15.5L6 13.5L4 12L6 10.5L5 8.5L7 7.5L6.5 5.5L8.5 5.5L9 3.5L11 4Z"/>
        <circle cx="12" cy="12" r="3"/>
        <circle cx="12" cy="12" r="1" fill="${color}"/>
      </svg>`,

    /**
     * Live/Broadcast icon - video stream
     */
    live: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <rect x="2" y="5" width="16" height="11" rx="1"/>
        <path d="M18 9L22 7L22 14L18 12"/>
        <circle cx="6" cy="8" r="1.5" fill="${color}"/>
        <path d="M9 8L14 8" stroke-width="1" opacity="0.5"/>
        <path d="M9 11L12 11" stroke-width="1" opacity="0.5"/>
        <path d="M4 19L20 19"/>
        <path d="M8 16L8 19"/>
        <path d="M16 16L16 19"/>
      </svg>`,

    /**
     * News/Document icon
     */
    news: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M4 4C4 3 5 2 6 2L14 2L20 8L20 20C20 21 19 22 18 22L6 22C5 22 4 21 4 20Z"/>
        <path d="M14 2L14 8L20 8"/>
        <line x1="8" y1="12" x2="16" y2="12"/>
        <line x1="8" y1="15" x2="14" y2="15"/>
        <line x1="8" y1="18" x2="16" y2="18"/>
      </svg>`,

    /**
     * Calendar/Event icon
     */
    event: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="4" width="18" height="18" rx="1"/>
        <line x1="3" y1="9" x2="21" y2="9"/>
        <line x1="8" y1="2" x2="8" y2="6"/>
        <line x1="16" y1="2" x2="16" y2="6"/>
        <circle cx="12" cy="15" r="3"/>
        <circle cx="12" cy="15" r="1" fill="${color}"/>
      </svg>`,

    /**
     * Video/Watch icon
     */
    video: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <rect x="2" y="4" width="16" height="12" rx="1"/>
        <path d="M18 8L22 6L22 14L18 12"/>
        <path d="M8 8L8 12L11 10Z" fill="${color}"/>
        <circle cx="5" cy="7" r="1" fill="${color}"/>
        <path d="M6 16L6 18"/>
        <path d="M14 16L14 18"/>
        <path d="M4 18L16 18"/>
      </svg>`,

    /**
     * Link/External icon
     */
    link: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M10 14L8 16C6 18 3 18 3 15C3 12 6 12 8 10L10 8"/>
        <path d="M14 10L16 8C18 6 21 6 21 9C21 12 18 12 16 14L14 16"/>
        <line x1="9" y1="15" x2="15" y2="9"/>
      </svg>`,

    /**
     * Close/X icon
     */
    close: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="6" y1="6" x2="18" y2="18"/>
        <line x1="18" y1="6" x2="6" y2="18"/>
      </svg>`,

    /**
     * Checkmark icon - milestone complete
     */
    check: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M5 12L10 17L19 7"/>
      </svg>`,

    /**
     * Checkmark in circle - confirmed/complete
     */
    checkCircle: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="9"/>
        <path d="M8 12L11 15L16 9"/>
      </svg>`,

    /**
     * Warning/Alert triangle
     */
    warning: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 3L22 20L2 20Z"/>
        <line x1="12" y1="9" x2="12" y2="14"/>
        <circle cx="12" cy="17" r="1" fill="${color}"/>
      </svg>`,

    /**
     * Sound/Speaker icon
     */
    sound: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M4 9L4 15L8 15L14 19L14 5L8 9Z"/>
        <path d="M17 8C18 9 19 10.5 19 12C19 13.5 18 15 17 16"/>
        <path d="M20 6C22 8 23 10 23 12C23 14 22 16 20 18" stroke-width="1"/>
      </svg>`,

    /**
     * Mute icon
     */
    mute: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M4 9L4 15L8 15L14 19L14 5L8 9Z"/>
        <line x1="18" y1="9" x2="22" y2="15"/>
        <line x1="22" y1="9" x2="18" y2="15"/>
      </svg>`,

    /**
     * Refresh/Sync icon
     */
    refresh: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M4 12C4 7.5 7.5 4 12 4C15 4 17.5 5.5 19 8"/>
        <path d="M20 12C20 16.5 16.5 20 12 20C9 20 6.5 18.5 5 16"/>
        <path d="M19 4L19 8L15 8"/>
        <path d="M5 20L5 16L9 16"/>
      </svg>`,

    /**
     * Location/Pin icon
     */
    location: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 2C8 2 5 5 5 9C5 14 12 22 12 22C12 22 19 14 19 9C19 5 16 2 12 2Z"/>
        <circle cx="12" cy="9" r="3"/>
        <circle cx="12" cy="9" r="1" fill="${color}"/>
      </svg>`,

    /**
     * Vehicle/Spacecraft generic icon
     */
    vehicle: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M8 20L8 8C8 4 10 2 12 2C14 2 16 4 16 8L16 20"/>
        <path d="M7 20L17 20C17 20 18 21 18 22L6 22C6 21 7 20 7 20Z"/>
        <circle cx="12" cy="8" r="2"/>
        <line x1="8" y1="14" x2="16" y2="14" stroke-width="0.75" opacity="0.5"/>
      </svg>`,

    /**
     * Orbit/Trajectory icon
     */
    orbit: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="4"/>
        <ellipse cx="12" cy="12" rx="9" ry="4" transform="rotate(-20 12 12)"/>
        <circle cx="19" cy="8" r="1.5" fill="${color}"/>
        <circle cx="5" cy="14" r="0.75" fill="${color}" opacity="0.5"/>
      </svg>`,

    /**
     * Moon icon
     */
    moon: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="9"/>
        <circle cx="9" cy="8" r="2" stroke-width="0.75"/>
        <circle cx="14" cy="14" r="2.5" stroke-width="0.75"/>
        <circle cx="8" cy="15" r="1" stroke-width="0.75"/>
        <circle cx="16" cy="8" r="1" stroke-width="0.75"/>
      </svg>`,

    /**
     * Earth icon
     */
    earth: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="9"/>
        <ellipse cx="12" cy="12" rx="9" ry="3"/>
        <ellipse cx="12" cy="12" rx="9" ry="6" stroke-width="0.75" opacity="0.5"/>
        <ellipse cx="12" cy="12" rx="3" ry="9"/>
      </svg>`,

    // ===== MILESTONE/STATUS ICONS =====

    /**
     * Milestone completed - filled circle with check
     */
    milestoneComplete: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="8" fill="${color}" stroke="none"/>
        <path d="M8 12L11 15L16 9" stroke="#0a0e27" stroke-width="2"/>
      </svg>`,

    /**
     * Milestone active - pulsing circle
     */
    milestoneActive: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="8"/>
        <circle cx="12" cy="12" r="5" stroke-width="0.75"/>
        <circle cx="12" cy="12" r="3" fill="${color}"/>
      </svg>`,

    /**
     * Milestone pending - empty circle
     */
    milestonePending: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="8"/>
        <circle cx="12" cy="12" r="4" stroke-width="0.75" opacity="0.4"/>
      </svg>`,

    // ===== NOTIFICATION TOAST ICONS =====

    /**
     * Success/Complete notification
     */
    success: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="9"/>
        <path d="M8 12L11 15L16 9"/>
        <circle cx="12" cy="12" r="6" stroke-width="0.5" opacity="0.3"/>
      </svg>`,

    /**
     * Alert/Error notification
     */
    alert: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="9"/>
        <line x1="12" y1="8" x2="12" y2="13"/>
        <circle cx="12" cy="16" r="1" fill="${color}"/>
      </svg>`,

    /**
     * Antenna/Signal icon - for data transmission
     */
    antenna: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 14L12 22"/>
        <path d="M8 22L16 22"/>
        <circle cx="12" cy="8" r="6"/>
        <circle cx="12" cy="8" r="3" stroke-width="0.75"/>
        <circle cx="12" cy="8" r="1" fill="${color}"/>
        <path d="M6 3L8 5"/>
        <path d="M18 3L16 5"/>
      </svg>`,

    /**
     * Clipboard/Document - for status updates
     */
    clipboard: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <rect x="5" y="4" width="14" height="18" rx="1"/>
        <path d="M9 2L9 4L15 4L15 2"/>
        <rect x="8" y="2" width="8" height="3" rx="0.5"/>
        <line x1="8" y1="10" x2="16" y2="10"/>
        <line x1="8" y1="13" x2="14" y2="13"/>
        <line x1="8" y1="16" x2="16" y2="16"/>
      </svg>`,

    /**
     * Arrow right - for navigation/links
     */
    arrowRight: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M5 12L19 12"/>
        <path d="M14 7L19 12L14 17"/>
      </svg>`,

    /**
     * Recovery/Landing target
     */
    target: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="9"/>
        <circle cx="12" cy="12" r="6"/>
        <circle cx="12" cy="12" r="3"/>
        <circle cx="12" cy="12" r="1" fill="${color}"/>
        <path d="M12 3L12 6"/>
        <path d="M12 18L12 21"/>
        <path d="M3 12L6 12"/>
        <path d="M18 12L21 12"/>
      </svg>`,

    /**
     * Fuel/Propellant gauge
     */
    fuel: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <rect x="6" y="4" width="8" height="16" rx="1"/>
        <path d="M14 8L17 6L17 10L14 8"/>
        <rect x="8" y="12" width="4" height="6" fill="${color}" opacity="0.3"/>
        <line x1="8" y1="8" x2="12" y2="8" stroke-width="0.75"/>
        <line x1="8" y1="10" x2="12" y2="10" stroke-width="0.75"/>
        <path d="M17 10L17 16L19 18"/>
      </svg>`,

    /**
     * Telemetry/Data stream
     */
    telemetry: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="3" width="18" height="18" rx="1"/>
        <path d="M3 12L6 12L8 8L10 16L12 10L14 14L16 12L18 12L21 12"/>
        <circle cx="8" cy="8" r="1" fill="${color}"/>
        <circle cx="12" cy="10" r="1" fill="${color}"/>
      </svg>`,

    /**
     * Comms/Communication
     */
    comms: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M4 18L4 10C4 6 7 3 12 3C17 3 20 6 20 10L20 18"/>
        <rect x="2" y="18" width="4" height="4" rx="0.5"/>
        <rect x="18" y="18" width="4" height="4" rx="0.5"/>
        <path d="M8 10C8 8 10 6 12 6C14 6 16 8 16 10" stroke-width="1"/>
        <circle cx="12" cy="10" r="2"/>
      </svg>`,

    /**
     * GO status indicator
     */
    statusGo: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="6" width="18" height="12" rx="2"/>
        <path d="M8 12L11 15L16 9"/>
        <circle cx="19" cy="8" r="1" fill="${color}"/>
      </svg>`,

    /**
     * NO-GO status indicator
     */
    statusNoGo: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="6" width="18" height="12" rx="2"/>
        <line x1="9" y1="9" x2="15" y2="15"/>
        <line x1="15" y1="9" x2="9" y2="15"/>
        <circle cx="19" cy="8" r="1" fill="${color}"/>
      </svg>`,

    /**
     * Default fallback icon
     */
    default: (size = 24, color = 'currentColor') => `
      <svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="9"/>
        <circle cx="12" cy="12" r="3"/>
      </svg>`
  },

  /**
   * Get list of all available icon names
   */
  getAvailableIcons() {
    return Object.keys(this.icons).filter(k => k !== 'default');
  }
};

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
  module.exports = UIIcons;
}
