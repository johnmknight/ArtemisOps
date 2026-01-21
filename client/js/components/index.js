/**
 * ArtemisOps - Orbital Map Components
 * 
 * This module exports all orbital map components for use in the main application.
 * 
 * Components:
 * - OrbitalMap: Base class for all orbital visualizations
 * - ArtemisIIMap: Artemis II free return trajectory
 * - ArtemisIIIMap: Artemis III NRHO + lunar landing
 * - ISSMap: Real-time ISS tracking with Leaflet
 * - MissionMapRouter: Factory for auto-selecting the right map
 * 
 * Usage:
 * ```html
 * <!-- Include Leaflet for ISSMap -->
 * <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
 * <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
 * 
 * <!-- Include components -->
 * <script src="js/components/OrbitalMap.js"></script>
 * <script src="js/components/ArtemisIIMap.js"></script>
 * <script src="js/components/ArtemisIIIMap.js"></script>
 * <script src="js/components/ISSMap.js"></script>
 * <script src="js/components/MissionMapRouter.js"></script>
 * ```
 * 
 * Quick Start:
 * ```javascript
 * // Using MissionMapRouter (recommended)
 * const map = await MissionMapRouter.createAndInit('map-container', 'artemis-ii');
 * 
 * // Or manually
 * const issMap = new ISSMap('iss-container');
 * await issMap.init();
 * ```
 * 
 * @version 1.0.0
 */

// Component registry for dynamic loading
const OrbitalMapComponents = {
  OrbitalMap: typeof OrbitalMap !== 'undefined' ? OrbitalMap : null,
  ArtemisIIMap: typeof ArtemisIIMap !== 'undefined' ? ArtemisIIMap : null,
  ArtemisIIIMap: typeof ArtemisIIIMap !== 'undefined' ? ArtemisIIIMap : null,
  ISSMap: typeof ISSMap !== 'undefined' ? ISSMap : null,
  MissionMapRouter: typeof MissionMapRouter !== 'undefined' ? MissionMapRouter : null
};

/**
 * Load all orbital map components dynamically
 * @param {string} basePath - Base path to components directory
 * @returns {Promise<Object>} - Loaded components
 */
async function loadOrbitalMapComponents(basePath = './js/components') {
  const components = [
    'OrbitalMap',
    'ArtemisIIMap',
    'ArtemisIIIMap',
    'ISSMap',
    'MissionMapRouter'
  ];
  
  const loadPromises = components.map(async (name) => {
    if (window[name]) return; // Already loaded
    
    try {
      const script = document.createElement('script');
      script.src = `${basePath}/${name}.js`;
      
      await new Promise((resolve, reject) => {
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
      });
    } catch (error) {
      console.error(`Failed to load ${name}:`, error);
    }
  });
  
  await Promise.all(loadPromises);
  
  return {
    OrbitalMap: window.OrbitalMap,
    ArtemisIIMap: window.ArtemisIIMap,
    ArtemisIIIMap: window.ArtemisIIIMap,
    ISSMap: window.ISSMap,
    MissionMapRouter: window.MissionMapRouter,
    createMissionMap: window.createMissionMap
  };
}

/**
 * Check if Leaflet is loaded (required for ISSMap)
 * @returns {boolean}
 */
function isLeafletLoaded() {
  return typeof L !== 'undefined';
}

/**
 * Load Leaflet library if not already loaded
 * @returns {Promise<void>}
 */
async function loadLeaflet() {
  if (isLeafletLoaded()) return;
  
  // Load CSS
  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
  link.crossOrigin = '';
  document.head.appendChild(link);
  
  // Load JS
  const script = document.createElement('script');
  script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
  script.crossOrigin = '';
  
  await new Promise((resolve, reject) => {
    script.onload = resolve;
    script.onerror = reject;
    document.head.appendChild(script);
  });
}

// Export for Node.js/CommonJS
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    OrbitalMapComponents,
    loadOrbitalMapComponents,
    isLeafletLoaded,
    loadLeaflet
  };
}
