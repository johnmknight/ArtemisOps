// ao-base.js — Reverse proxy subpath detection for ArtemisOps
// Include this script BEFORE any fetch calls in every page.
// Detects the nginx proxy prefix (e.g. '/artemis') and provides
// AO_BASE for prepending to all API and WebSocket URLs.
const AO_BASE = (() => {
  // Check parent frame first (tabs are iframes), fall back to own location
  let path;
  try { path = window.parent.location.pathname; } catch(e) { path = window.location.pathname; }
  const seg = path.split('/')[1] || '';
  const excluded = ['api','static','client','tabs','ws','js','css','assets','data','components','mockups','images'];
  if (!seg || seg.includes('.') || excluded.includes(seg)) return '';
  return '/' + seg;
})();

// Monkey-patch fetch to auto-prepend AO_BASE to root-relative URLs
const _origFetch = window.fetch;
window.fetch = function(url, opts) {
  if (typeof url === 'string' && url.startsWith('/') && !url.startsWith('//') && AO_BASE) {
    url = AO_BASE + url;
  }
  return _origFetch.call(this, url, opts);
};
