/**
 * ArtemisOps — Theme Switcher
 * client/js/ao-theme-switcher.js
 *
 * Usage:
 *   import AoTheme from '/js/ao-theme-switcher.js';
 *   AoTheme.set('expanse');     // switch theme
 *   AoTheme.get();              // returns current theme name
 *   AoTheme.cycle();            // step through available themes
 *   AoTheme.available           // array of theme names
 *
 * Themes are applied to <html data-theme="...">
 * Theme persisted to localStorage under key 'ao-theme'.
 * Iframes registered via AoTheme.registerFrame(iframe) receive
 * the same theme broadcast via postMessage.
 */

const AoTheme = (() => {
  const STORAGE_KEY = 'ao-theme';
  const DEFAULT     = 'nominal';

  const available = ['nominal', 'expanse', 'hazard', 'stealth'];
  const labels = {
    nominal: 'Mission Blue',
    expanse: 'Amber / The Expanse',
    hazard:  'Red Alert',
    stealth: 'Stealth Dark',
  };

  const frames = new Set();

  function get() {
    return document.documentElement.getAttribute('data-theme') || DEFAULT;
  }

  function set(name) {
    if (!available.includes(name)) {
      console.warn(`[AoTheme] Unknown theme: "${name}". Available: ${available.join(', ')}`);
      return;
    }
    document.documentElement.setAttribute('data-theme', name);
    try { localStorage.setItem(STORAGE_KEY, name); } catch (_) {}
    broadcast(name);
    document.dispatchEvent(new CustomEvent('ao-theme-change', { detail: { theme: name } }));
  }

  function cycle() {
    const idx = available.indexOf(get());
    set(available[(idx + 1) % available.length]);
  }

  function restore() {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved && available.includes(saved)) set(saved);
    } catch (_) {}
  }

  function registerFrame(iframe) {
    frames.add(iframe);
    // Immediately sync current theme
    try {
      iframe.contentWindow.postMessage({ type: 'ao-theme', theme: get() }, '*');
    } catch (_) {}
  }

  function broadcast(name) {
    for (const f of frames) {
      try { f.contentWindow.postMessage({ type: 'ao-theme', theme: name }, '*'); } catch (_) {}
    }
  }

  /** Listen for theme messages in child iframes */
  function listenAsChild() {
    window.addEventListener('message', (e) => {
      if (e.data?.type === 'ao-theme' && available.includes(e.data.theme)) {
        document.documentElement.setAttribute('data-theme', e.data.theme);
      }
    });
  }

  return { available, labels, get, set, cycle, restore, registerFrame, broadcast, listenAsChild };
})();

export default AoTheme;
