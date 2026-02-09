const fs = require('fs');
const path = require('path');

const TABLER_DIR = '/tmp/spaceicons-build/node_modules/@tabler/icons/icons';

// Complete emoji → Tabler icon mapping from ArtemisOps audit
// Format: 'icon-key': { tabler: 'tabler-name', emoji: 'original', type: 'outline'|'filled' }
const ICON_MAP = {
    // === Navigation / Core UI ===
    'rocket':              { tabler: 'rocket', emoji: '🚀' },
    'settings':            { tabler: 'settings', emoji: '⚙' },
    'target':              { tabler: 'target', emoji: '🎯' },
    'search':              { tabler: 'search', emoji: '🔍' },
    'refresh':             { tabler: 'refresh', emoji: '🔄' },
    'link':                { tabler: 'link', emoji: '🔗' },
    'plus':                { tabler: 'plus', emoji: '➕' },
    'pencil':              { tabler: 'pencil', emoji: '✏' },
    'folder':              { tabler: 'folder', emoji: '📁' },
    'clipboard-list':      { tabler: 'clipboard-list', emoji: '📋' },
    'chart-bar':           { tabler: 'chart-bar', emoji: '📊' },
    'device-tv':           { tabler: 'device-tv', emoji: '📺' },
    'device-desktop':      { tabler: 'device-desktop', emoji: '🖥' },
    'camera':              { tabler: 'camera', emoji: '📷' },
    'news':                { tabler: 'news', emoji: '📰' },
    'speakerphone':        { tabler: 'speakerphone', emoji: '📢' },
    'bulb':                { tabler: 'bulb', emoji: '💡' },
    'palette':             { tabler: 'palette', emoji: '🎨' },

    // === Space / Science ===
    'satellite':           { tabler: 'satellite', emoji: '🛰' },
    'antenna':             { tabler: 'antenna', emoji: '📡' },
    'world':               { tabler: 'world', emoji: '🌍' },
    'world-alt':           { tabler: 'world', emoji: '🌎' },
    'compass':             { tabler: 'compass', emoji: '🧭' },
    'map-pin':             { tabler: 'map-pin', emoji: '📍' },
    'bolt':                { tabler: 'bolt', emoji: '⚡' },
    'ufo':                 { tabler: 'ufo', emoji: '🛸' },
    'user-circle':         { tabler: 'user-circle', emoji: '👨‍🚀' },
    'flame':               { tabler: 'flame', emoji: '🐉' },
    'flask':               { tabler: 'flask', emoji: '⚗' },
    'radiation':           { tabler: 'radioactive', emoji: '☢' },
    'magnet':              { tabler: 'magnet', emoji: '🧲' },
    'robot':               { tabler: 'robot', emoji: '🦾' },

    // === Weather ===
    'sun':                 { tabler: 'sun', emoji: '☀' },
    'cloud':               { tabler: 'cloud', emoji: '☁' },
    'cloud-rain':          { tabler: 'cloud-rain', emoji: '🌧' },
    'cloud-sun':           { tabler: 'sun-high', emoji: '🌤' },
    'moon':                { tabler: 'moon', emoji: '🌙' },
    'moon-filled':         { tabler: 'moon', emoji: '🌕', type: 'filled' },
    'temperature':         { tabler: 'temperature', emoji: '🌡' },
    'droplet':             { tabler: 'droplet', emoji: '💧' },
    'wind':                { tabler: 'wind', emoji: '💨' },
    'snowflake':           { tabler: 'snowflake', emoji: '❄' },
    'wave-sine':           { tabler: 'wave-sine', emoji: '🌊' },
    'sparkles':            { tabler: 'sparkles', emoji: '✨' },

    // === Status / Feedback ===
    'check':               { tabler: 'check', emoji: '✓' },
    'circle-check':        { tabler: 'circle-check', emoji: '✅' },
    'x':                   { tabler: 'x', emoji: '✗' },
    'x-close':             { tabler: 'x', emoji: '❌' },
    'alert-triangle':      { tabler: 'alert-triangle', emoji: '⚠' },
    'alert-circle':        { tabler: 'alert-circle', emoji: '🚨' },
    'help':                { tabler: 'help', emoji: '❓' },
    'circle-filled':       { tabler: 'circle', emoji: '●', type: 'filled' },
    'circle':              { tabler: 'circle', emoji: '○' },
    'point-filled':        { tabler: 'point', emoji: '🔴', type: 'filled' },

    // === Audio / Media ===
    'volume':              { tabler: 'volume', emoji: '🔊' },
    'volume-off':          { tabler: 'volume-off', emoji: '🔇' },

    // === Layout / Controls ===
    'clock':               { tabler: 'clock', emoji: '🕐' },
    'adjustments-horizontal': { tabler: 'adjustments-horizontal', emoji: '🎛' },
    'arrows-maximize':     { tabler: 'arrows-maximize', emoji: '⛶' },
    'tool':                { tabler: 'tool', emoji: '🛠' },
};

const output = {};
let found = 0;
let missing = 0;

Object.entries(ICON_MAP).forEach(([key, cfg]) => {
    const type = cfg.type || 'outline';
    const svgPath = path.join(TABLER_DIR, type, `${cfg.tabler}.svg`);

    if (fs.existsSync(svgPath)) {
        let svg = fs.readFileSync(svgPath, 'utf8');
        // Set stroke-width to 1.5 for HUD look
        svg = svg.replace(/stroke-width="2"/g, 'stroke-width="1.5"');
        output[key] = svg.trim();
        found++;
    } else {
        console.error(`MISSING: ${key} → ${type}/${cfg.tabler}.svg`);
        missing++;
    }
});

console.log(`\nFound: ${found}, Missing: ${missing}`);

// Build output JS file
const outFile = '/mnt/c/Users/john_/dev/ArtemisOps/client/js/icons.js';

let js = '/**\n';
js += ' * ArtemisOps Icon Library - Tabler Icons (MIT License)\n';
js += ' * https://tabler.io/icons\n';
js += ' * Generated: ' + new Date().toISOString().split('T')[0] + '\n';
js += ' * Icons: ' + found + ' inline SVGs, stroke-width: 1.5\n';
js += ' *\n';
js += ' * Usage: element.innerHTML = ICONS[\'rocket\'];\n';
js += ' *        `${ICONS.rocket}` in template literals\n';
js += ' */\n\n';
js += 'const ICONS = {\n';

const entries = Object.entries(output);
entries.forEach(([key, svg], i) => {
    const escaped = svg.replace(/\\/g, '\\\\').replace(/`/g, '\\`').replace(/\$/g, '\\$');
    js += `    '${key}': \`${escaped}\``;
    if (i < entries.length - 1) js += ',';
    js += '\n';
});

js += '};\n';

fs.writeFileSync(outFile, js, 'utf8');
console.log(`Written to ${outFile}`);
