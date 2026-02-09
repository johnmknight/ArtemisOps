const fs = require('fs');
const path = require('path');

const svgDir = process.argv[2] || './svg-clean';
const outFile = process.argv[3] || './spaceicons.js';

const files = fs.readdirSync(svgDir).filter(f => f.endsWith('.svg')).sort();

const icons = {};

files.forEach(file => {
    const name = file.replace('.svg', '');
    let svg = fs.readFileSync(path.join(svgDir, file), 'utf8');
    
    // Strip XML declaration and DOCTYPE
    svg = svg.replace(/<\?xml[^?]*\?>\s*/g, '');
    svg = svg.replace(/<!DOCTYPE[^>]*>\s*/g, '');
    
    // Clean up whitespace
    svg = svg.trim();
    
    icons[name] = svg;
});

// Build output
let output = '/**\n';
output += ' * SpaceIcons - Semiotic Standard for Commercial Trans-Stellar Utility Lifter\n';
output += ' * Based on Ron Cobb\'s iconic signage system designed for Alien (1979)\n';
output += ' * Source: https://github.com/banastas/SemioticStandard.org (MIT License)\n';
output += ' * Generated: ' + new Date().toISOString().split('T')[0] + '\n';
output += ' * Icons: ' + files.length + ' pictograms with original color coding\n';
output += ' *\n';
output += ' * Color coding:\n';
output += ' *   Red    rgb(160,0,0)   - Pressurized areas, safety borders\n';
output += ' *   Green  rgb(0,68,17)   - Organic, medical (autodoc, coffee, galley)\n';
output += ' *   Blue   rgb(10,10,112) - Cold/cryo (refrigeration, cryogenic vault)\n';
output += ' *   Grey   rgb(96,96,96)  - Technical systems (computer, ladderway)\n';
output += ' *   Orange rgb(255,176,0) - Hazard/warning (exhaust, radiation)\n';
output += ' *   Black  - Structural elements (bulkhead, non-pressurised)\n';
output += ' *\n';
output += ' * Usage: <div class="spaceicon">${SPACE_ICONS[\'coffee\']}</div>\n';
output += ' */\n\n';
output += 'const SPACE_ICONS = {\n';

const entries = Object.entries(icons);
entries.forEach(([name, svg], i) => {
    // Escape backticks and backslashes in SVG content
    const escaped = svg.replace(/\\/g, '\\\\').replace(/`/g, '\\`').replace(/\$/g, '\\$');
    output += `    '${name}': \`${escaped}\``;
    if (i < entries.length - 1) output += ',';
    output += '\n';
});

output += '};\n';

fs.writeFileSync(outFile, output, 'utf8');
console.log(`Generated ${outFile} with ${entries.length} icons`);
