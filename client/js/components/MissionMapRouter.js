/**
 * ArtemisOps - Mission Map Router
 * 
 * Factory class that automatically selects and instantiates the appropriate
 * orbital map component based on mission type.
 * 
 * Supported mission types:
 * - artemis-ii: Lunar free return trajectory (ArtemisIIMap)
 * - artemis-iii, artemis-iv+: NRHO + lunar landing (ArtemisIIIMap)
 * - iss-expedition: Earth orbit live tracking (ISSMap)
 * - earth-orbit: Generic Earth orbit missions (ISSMap variant)
 * 
 * @version 1.0.0
 */

class MissionMapRouter {
  /**
   * Mission type to map class mapping
   */
  static MISSION_TYPES = {
    // Artemis lunar missions
    'artemis-i': 'lunar-flyby',
    'artemis-ii': 'lunar-flyby',
    'artemis-iii': 'lunar-landing',
    'artemis-iv': 'lunar-landing',
    'artemis-v': 'lunar-landing',
    
    // ISS missions
    'iss-expedition': 'earth-orbit-live',
    'iss': 'earth-orbit-live',
    
    // Commercial crew
    'crew-dragon': 'earth-orbit',
    'starliner': 'earth-orbit',
    
    // Other
    'lunar-gateway': 'nrho',
    'generic': 'earth-orbit'
  };
  
  /**
   * Map class registry
   */
  static MAP_CLASSES = {
    'lunar-flyby': 'ArtemisIIMap',
    'lunar-landing': 'ArtemisIIIMap',
    'earth-orbit-live': 'ISSMap',
    'earth-orbit': 'ISSMap',
    'nrho': 'ArtemisIIIMap'
  };
  
  /**
   * Create the appropriate map component for a mission
   * 
   * @param {string} containerId - DOM element ID for the map
   * @param {string|Object} mission - Mission type string or mission data object
   * @param {Object} options - Additional options for the map component
   * @returns {OrbitalMap} The instantiated map component
   */
  static createMap(containerId, mission, options = {}) {
    // Determine mission type
    let missionType;
    let missionData = null;
    
    if (typeof mission === 'string') {
      missionType = mission.toLowerCase();
    } else if (typeof mission === 'object' && mission !== null) {
      missionType = (mission.type || mission.id || mission.name || 'generic').toLowerCase();
      missionData = mission;
    } else {
      missionType = 'generic';
    }
    
    // Clean up mission type (handle variations)
    missionType = this.normalizeMissionType(missionType);
    
    // Get the map class to use
    const mapCategory = this.MISSION_TYPES[missionType] || 'earth-orbit';
    const mapClassName = this.MAP_CLASSES[mapCategory];
    
    // Check if the map class exists
    const MapClass = this.getMapClass(mapClassName);
    if (!MapClass) {
      console.error(`Map class ${mapClassName} not found. Falling back to base OrbitalMap.`);
      return new OrbitalMap(containerId, options);
    }
    
    // Create the map instance
    const mapInstance = new MapClass(containerId, options);
    
    // Set mission data if provided
    if (missionData) {
      mapInstance.setMissionData(missionData);
    }
    
    return mapInstance;
  }
  
  /**
   * Normalize mission type string to match known types
   * @param {string} missionType 
   * @returns {string}
   */
  static normalizeMissionType(missionType) {
    // Remove spaces, dashes variations
    const normalized = missionType.toLowerCase().replace(/[\s_]/g, '-');
    
    // Handle common variations
    const aliases = {
      'artemis2': 'artemis-ii',
      'artemis-2': 'artemis-ii',
      'artemisii': 'artemis-ii',
      'artemis3': 'artemis-iii',
      'artemis-3': 'artemis-iii',
      'artemisiii': 'artemis-iii',
      'artemis4': 'artemis-iv',
      'artemis-4': 'artemis-iv',
      'artemisiv': 'artemis-iv',
      'international-space-station': 'iss-expedition',
      'space-station': 'iss-expedition',
      'crewdragon': 'crew-dragon',
      'spacex-crew': 'crew-dragon',
      'boeing-starliner': 'starliner'
    };
    
    return aliases[normalized] || normalized;
  }
  
  /**
   * Get the map class by name
   * @param {string} className 
   * @returns {Function|null}
   */
  static getMapClass(className) {
    // Try to get from global scope
    if (typeof window !== 'undefined' && window[className]) {
      return window[className];
    }
    
    // Try to require (Node.js environment)
    try {
      if (typeof require !== 'undefined') {
        return require(`./${className}`);
      }
    } catch (e) {
      // Ignore require errors in browser
    }
    
    return null;
  }
  
  /**
   * Initialize map and return a promise
   * 
   * @param {string} containerId 
   * @param {string|Object} mission 
   * @param {Object} options 
   * @returns {Promise<OrbitalMap>}
   */
  static async createAndInit(containerId, mission, options = {}) {
    const map = this.createMap(containerId, mission, options);
    await map.init();
    return map;
  }
  
  /**
   * Get information about supported mission types
   * @returns {Object}
   */
  static getSupportedMissions() {
    return {
      types: Object.keys(this.MISSION_TYPES),
      categories: {
        'lunar-flyby': ['artemis-i', 'artemis-ii'],
        'lunar-landing': ['artemis-iii', 'artemis-iv', 'artemis-v'],
        'earth-orbit-live': ['iss-expedition', 'iss'],
        'earth-orbit': ['crew-dragon', 'starliner', 'generic'],
        'nrho': ['lunar-gateway']
      }
    };
  }
  
  /**
   * Check if a mission type is supported
   * @param {string} missionType 
   * @returns {boolean}
   */
  static isSupported(missionType) {
    const normalized = this.normalizeMissionType(missionType);
    return normalized in this.MISSION_TYPES;
  }
  
  /**
   * Get the map category for a mission type
   * @param {string} missionType 
   * @returns {string}
   */
  static getMapCategory(missionType) {
    const normalized = this.normalizeMissionType(missionType);
    return this.MISSION_TYPES[normalized] || 'generic';
  }
}

// Convenience function for quick map creation
async function createMissionMap(containerId, mission, options = {}) {
  return MissionMapRouter.createAndInit(containerId, mission, options);
}

// Export for ES modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { MissionMapRouter, createMissionMap };
}
