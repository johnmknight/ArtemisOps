/**
 * SpaceIcons - Semiotic Standard for Commercial Trans-Stellar Utility Lifter
 * Based on Ron Cobb's iconic signage system designed for Alien (1979)
 * Source: https://github.com/banastas/SemioticStandard.org (MIT License)
 * Generated: 2026-02-09
 * Icons: 34 pictograms with original color coding
 *
 * Color coding:
 *   Red    rgb(160,0,0)   - Pressurized areas, safety borders
 *   Green  rgb(0,68,17)   - Organic, medical (autodoc, coffee, galley)
 *   Blue   rgb(10,10,112) - Cold/cryo (refrigeration, cryogenic vault)
 *   Grey   rgb(96,96,96)  - Technical systems (computer, ladderway)
 *   Orange rgb(255,176,0) - Hazard/warning (exhaust, radiation)
 *   Black  - Structural elements (bulkhead, non-pressurised)
 *
 * Usage: <div class="spaceicon">${SPACE_ICONS['coffee']}</div>
 */

const SPACE_ICONS = {
    'airlock': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M85,82C85,84.8 82.8,87 80,87L20,87C17.2,87 15,84.8 15,82L15,77L5,77L5,87C5,92.5 9.5,97 15,97L85,97C90.5,97 95,92.5 95,87L95,77L85,77L85,82Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <rect x="5" y="27" width="10" height="45" style="fill:rgb(160,0,0);"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <rect x="85" y="27" width="10" height="45" style="fill:rgb(160,0,0);"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M85,2L15,2C9.5,2 5,6.5 5,12L5,22L15,22L15,17C15,14.2 17.2,12 20,12L80,12C82.8,12 85,14.2 85,17L85,22L95,22L95,12C95,6.5 90.5,2 85,2Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M80,19.5C80,18.1 78.9,17 77.5,17L20,17L80,77L80,19.5Z" style="fill:black;fill-rule:nonzero;"/>
    </g>
</svg>`,
    'area-shielded-from-radiation': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M85,2L15,2C9.5,2 5,6.5 5,12L5,87C5,92.5 9.5,97 15,97L85,97C90.5,97 95,92.5 95,87L95,12C95,6.5 90.5,2 85,2ZM70,74.5C70,75.9 68.9,77 67.5,77L55,77L55,44.5L45,44.5L45,77L32.5,77C31.1,77 30,75.9 30,74.5L30,24.5C30,23.1 31.1,22 32.5,22L67.5,22C68.9,22 70,23.1 70,24.5L70,74.5Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <circle cx="50" cy="34.5" r="7.5" style="fill:rgb(160,0,0);"/>
    </g>
</svg>`,
    'artificial-gravity-absent': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <circle cx="50" cy="74.5" r="7.5" style="fill:rgb(160,0,0);"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M75,27L67.5,19.5L50,37L32.5,19.5L25,27L45,47L45,52L25,52L25,62L75,62L75,52L55,52L55,47L75,27Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M85,2L15,2C9.5,2 5,6.5 5,12L5,87C5,92.5 9.5,97 15,97L85,97C90.5,97 95,92.5 95,87L95,12C95,6.5 90.5,2 85,2ZM85,82C85,84.8 82.8,87 80,87L20,87C17.2,87 15,84.8 15,82L15,17C15,14.2 17.2,12 20,12L80,12C82.8,12 85,14.2 85,17L85,82Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
</svg>`,
    'artificial-gravity-area-non-pressurised-suit-required': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M85,2L15,2C9.5,2 5,6.5 5,12L5,72L20,72L20,79.5C20,80.9 21.1,82 22.5,82L37.5,82L37.5,64.5C37.5,63.1 36.4,62 35,62L32.5,62C31.1,62 30,60.9 30,59.5L30,39.5C30,38.1 31.1,37 32.5,37L35,37C36.4,37 37.5,35.9 37.5,34.5L37.5,32C37.5,25 43.3,19.3 50.4,19.5C57.2,19.7 62.5,25.4 62.5,32.3L62.5,34.5C62.5,35.9 63.6,37 65,37L67.5,37C68.9,37 70,38.1 70,39.5L70,59.5C70,60.9 68.9,62 67.5,62L65,62C63.6,62 62.5,63.1 62.5,64.5L62.5,82L77.5,82C78.9,82 80,80.9 80,79.5L80,72L95,72L95,12C95,6.5 90.5,2 85,2Z" style="fill:black;fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <circle cx="50" cy="32" r="7.5" style="fill:rgb(160,0,0);"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M85,82C85,84.8 82.8,87 80,87L20,87C17.2,87 15,84.8 15,82L15,77L5,77L5,87C5,92.5 9.5,97 15,97L85,97C90.5,97 95,92.5 95,87L95,77L85,77L85,82Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
</svg>`,
    'astronic-system-electronics': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M20,79.5C20,80.9 21.1,82 22.5,82L77.5,82C78.9,82 80,80.9 80,79.5L80,49.5L20,49.5L20,79.5ZM35,62L65,62L65,69.5L35,69.5L35,62Z" style="fill:rgb(96,96,96);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M85,2L15,2C9.5,2 5,6.5 5,12L5,47L15,47L15,17C15,14.2 17.2,12 20,12L80,12C82.8,12 85,14.2 85,17L85,47L95,47L95,12C95,6.5 90.5,2 85,2Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M85,82C85,84.8 82.8,87 80,87L20,87C17.2,87 15,84.8 15,82L15,52L5,52L5,87C5,92.5 9.5,97 15,97L85,97C90.5,97 95,92.5 95,87L95,52L85,52L85,82Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M46.25,17L46.25,27.017L35,27.017L35,34.517L46.25,34.517L46.25,44.5L53.75,44.5L53.75,34.517L65,34.517L65,27.017L53.75,27.017L53.75,17L46.25,17Z" style="fill:rgb(96,96,96);fill-rule:nonzero;"/>
    </g>
</svg>`,
    'autodoc': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,4.91497e-31,4.91497e-31,10,7.90479e-14,30)">
        <path d="M85,2L15,2C9.5,2 5,6.5 5,12L5,87C5,92.5 9.5,97 15,97L85,97C90.5,97 95,92.5 95,87L95,12C95,6.5 90.5,2 85,2ZM85,82C85,84.8 82.8,87 80,87L20,87C17.2,87 15,84.8 15,82L15,17C15,14.2 17.2,12 20,12L80,12C82.8,12 85,14.2 85,17L85,82Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-8.96788e-31,-7.94339e-31,10,0,30)">
        <path d="M20,19.5L20,39.5L40,39.5L40,17L22.5,17C21.1,17 20,18.1 20,19.5Z" style="fill:rgb(0,68,17);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-8.96788e-31,-7.94339e-31,10,0,30)">
        <path d="M77.5,17L60,17L60,39.5L80,39.5L80,19.5C80,18.1 78.9,17 77.5,17Z" style="fill:rgb(0,68,17);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-8.96788e-31,-7.94339e-31,10,0,30)">
        <path d="M20,79.5C20,80.9 21.1,82 22.5,82L40,82L40,59.5L20,59.5L20,79.5Z" style="fill:rgb(0,68,17);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-8.96788e-31,-7.94339e-31,10,0,30)">
        <path d="M60,82L77.5,82C78.9,82 80,80.9 80,79.5L80,59.5L60,59.5L60,82Z" style="fill:rgb(0,68,17);fill-rule:nonzero;"/>
    </g>
</svg>`,
    'bridge': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M85,2L15,2C9.5,2 5,6.5 5,12L5,87C5,92.5 9.5,97 15,97L85,97C90.5,97 95,92.5 95,87L95,12C95,6.5 90.5,2 85,2ZM85,82C85,84.8 82.8,87 80,87L20,87C17.2,87 15,84.8 15,82L15,17C15,14.2 17.2,12 20,12L80,12C82.8,12 85,14.2 85,17L85,82Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M77.5,17L22.5,17C21.1,17 20,18.1 20,19.5L20,79.5C20,80.9 21.1,82 22.5,82L77.5,82C78.9,82 80,80.9 80,79.5L80,19.5C80,18.1 78.9,17 77.5,17ZM25,72L50,22L75,72L25,72Z" style="fill:rgb(96,96,96);fill-rule:nonzero;"/>
    </g>
</svg>`,
    'bulkhead-door': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M55,82L55,77L45,77L45,82C45,84.8 42.8,87 40,87L20,87C17.2,87 15,84.8 15,82L15,17C15,14.2 17.2,12 20,12L40,12C42.8,12 45,14.2 45,17L45,22L55,22L55,17C55,14.2 57.2,12 60,12L75,12L75,2L15,2C9.5,2 5,6.5 5,12L5,87C5,92.5 9.5,97 15,97L75,97L75,87L60,87C57.2,87 55,84.8 55,82Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <rect x="45" y="27" width="10" height="45" style="fill:rgb(160,0,0);"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M80,2L80,17L62.5,17C61.1,17 60,18.1 60,19.5L60,79.5C60,80.9 61.1,82 62.5,82L80,82L80,97L85,97C90.5,97 95,92.5 95,87L95,12C95,6.5 90.5,2 85,2L80,2Z" style="fill:black;fill-rule:nonzero;"/>
    </g>
</svg>`,
    'coffee': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,4.91497e-31,4.91497e-31,10,7.90479e-14,30)">
        <path d="M85,2L15,2C9.5,2 5,6.5 5,12L5,87C5,92.5 9.5,97 15,97L85,97C90.5,97 95,92.5 95,87L95,12C95,6.5 90.5,2 85,2ZM85,82C85,84.8 82.8,87 80,87L20,87C17.2,87 15,84.8 15,82L15,17C15,14.2 17.2,12 20,12L80,12C82.8,12 85,14.2 85,17L85,82Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,4.91497e-31,4.91497e-31,10,7.90479e-14,30)">
        <path d="M70,54.5L70,44.5C70,43.1 68.9,42 67.5,42L60,42L60,57L67.5,57C68.9,57 70,55.9 70,54.5Z" style="fill:rgb(0,68,17);fill-rule:nonzero;"/>
    </g>
    <path d="M775,200C789,200 800,211 800,225L800,825C800,839 789,850 775,850L225,850C211,850 200,839 200,825L200,225C200,211 211,200 225,200L775,200ZM725,400L250,400L250,625C250,639 261,650 275,650L725,650C739,650 750,639 750,625L750,425L749.928,425C749.89,411.258 738.742,400.109 725,400.07L725,400Z" style="fill:rgb(0,68,17);"/>
</svg>`,
    'computer-terminal': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M85,2L15,2C9.5,2 5,6.5 5,12L5,87C5,92.5 9.5,97 15,97L85,97C90.5,97 95,92.5 95,87L95,12C95,6.5 90.5,2 85,2ZM85,82C85,84.8 82.8,87 80,87L20,87C17.2,87 15,84.8 15,82L15,17C15,14.2 17.2,12 20,12L80,12C82.8,12 85,14.2 85,17L85,82Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M77.5,17L22.5,17C21.1,17 20,18.1 20,19.5L20,79.5C20,80.9 21.1,82 22.5,82L77.5,82C78.9,82 80,80.9 80,79.5L80,19.5C80,18.1 78.9,17 77.5,17ZM35,77L27.5,77C26.1,77 25,75.9 25,74.5L25,67L35,67L35,77ZM35,64.5L25,64.5L25,57C25,55.6 26.1,54.5 27.5,54.5L35,54.5L35,64.5ZM48.3,77L38.3,77L38.3,67L48.3,67L48.3,77ZM48.3,64.5L38.3,64.5L38.3,54.5L48.3,54.5L48.3,64.5ZM61.7,77L51.7,77L51.7,67L61.7,67L61.7,77ZM61.7,64.5L51.7,64.5L51.7,54.5L61.7,54.5L61.7,64.5ZM75,74.5C75,75.9 73.9,77 72.5,77L65,77L65,67L75,67L75,74.5ZM75,64.5L65,64.5L65,54.5L72.5,54.5C73.9,54.5 75,55.6 75,57L75,64.5ZM75,44.5C75,45.9 73.9,47 72.5,47L27.5,47C26.1,47 25,45.9 25,44.5L25,24.5C25,23.1 26.1,22 27.5,22L72.5,22C73.9,22 75,23.1 75,24.5L75,44.5Z" style="fill:rgb(96,96,96);fill-rule:nonzero;"/>
    </g>
</svg>`,
    'cryogenic-vault': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M85,2L15,2C9.5,2 5,6.5 5,12L5,87C5,92.5 9.5,97 15,97L85,97C90.5,97 95,92.5 95,87L95,12C95,6.5 90.5,2 85,2ZM85,82C85,84.8 82.8,87 80,87L20,87C17.2,87 15,84.8 15,82L15,17C15,14.2 17.2,12 20,12L80,12C82.8,12 85,14.2 85,17L85,82Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-25,30)">
        <circle cx="75" cy="75" r="7.5" style="fill:rgb(160,0,0);"/>
    </g>
    <g transform="matrix(9.37463,-3.69764e-31,0,10,15.6491,30)">
        <rect x="25" y="70" width="40" height="10" style="fill:rgb(160,0,0);"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M75,22L24.6,22L49.8,67L75,22Z" style="fill:rgb(10,10,112);fill-rule:nonzero;"/>
    </g>
</svg>`,
    'direction-down': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M85,2L15,2C9.5,2 5,6.5 5,12L5,87C5,92.5 9.5,97 15,97L85,97C90.5,97 95,92.5 95,87L95,12C95,6.5 90.5,2 85,2ZM85,82C85,84.8 82.8,87 80,87L20,87C17.2,87 15,84.8 15,82L15,17C15,14.2 17.2,12 20,12L80,12C82.8,12 85,14.2 85,17L85,82Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,3.9443e-31,0,-10,-1.13687e-13,1020)">
        <path d="M20,52L20,72L50,42L80,72L80,52L50,22L20,52Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
</svg>`,
    'direction-left': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M85,2L15,2C9.5,2 5,6.5 5,12L5,87C5,92.5 9.5,97 15,97L85,97C90.5,97 95,92.5 95,87L95,12C95,6.5 90.5,2 85,2ZM85,82C85,84.8 82.8,87 80,87L20,87C17.2,87 15,84.8 15,82L15,17C15,14.2 17.2,12 20,12L80,12C82.8,12 85,14.2 85,17L85,82Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(1.83697e-15,-10,10,1.83697e-15,30,1025)">
        <path d="M20,52L20,72L50,42L80,72L80,52L50,22L20,52Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
</svg>`,
    'direction-right': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M85,2L15,2C9.5,2 5,6.5 5,12L5,87C5,92.5 9.5,97 15,97L85,97C90.5,97 95,92.5 95,87L95,12C95,6.5 90.5,2 85,2ZM85,82C85,84.8 82.8,87 80,87L20,87C17.2,87 15,84.8 15,82L15,17C15,14.2 17.2,12 20,12L80,12C82.8,12 85,14.2 85,17L85,82Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(-1.83697e-15,-10,-10,1.83697e-15,970,1025)">
        <path d="M20,52L20,72L50,42L80,72L80,52L50,22L20,52Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
</svg>`,
    'direction': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M85,2L15,2C9.5,2 5,6.5 5,12L5,87C5,92.5 9.5,97 15,97L85,97C90.5,97 95,92.5 95,87L95,12C95,6.5 90.5,2 85,2ZM85,82C85,84.8 82.8,87 80,87L20,87C17.2,87 15,84.8 15,82L15,17C15,14.2 17.2,12 20,12L80,12C82.8,12 85,14.2 85,17L85,82Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M20,52L20,72L50,42L80,72L80,52L50,22L20,52Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
</svg>`,
    'exhaust': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M77.5,17C78.904,17.004 80,18.103 80,19.5L80,64.5L95,75.8L95,87C95,90.949 92.68,94.382 89.336,96.004L70,67L70,17L77.5,17Z" style="fill:rgb(255,176,0);"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M77.5,17C78.904,17.004 80,18.103 80,19.5L80,64.5L95,75.8L95,87C95,90.949 92.68,94.382 89.336,96.004L70,67L70,17L77.5,17Z" style="fill:rgb(255,176,0);"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M65,17L65,69.5L80,97L54.167,97L52.5,72L52.5,17L65,17Z" style="fill:rgb(255,176,0);"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M30,67L10.664,96.004C7.382,94.412 5.087,91.077 5.006,87.22L5,75.8L20,64.5L20,19.5C20,18.103 21.096,17.004 22.5,17L30,17L30,67Z" style="fill:rgb(255,176,0);"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M47.5,17L47.5,72L45.833,97L20,97L35,69.5L35,17L47.5,17Z" style="fill:rgb(255,176,0);"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M85,2L15,2C9.5,2 5,6.5 5,12L5,68.2L15,62L15,17C15,14.2 17.2,12 20,12L80,12C82.8,12 85,14.2 85,17L85,62L95,68.2L95,12C95,6.5 90.5,2 85,2Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
</svg>`,
    'galley': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M85,2L15,2C9.5,2 5,6.5 5,12L5,87C5,92.5 9.5,97 15,97L85,97C90.5,97 95,92.5 95,87L95,12C95,6.5 90.5,2 85,2ZM85,82C85,84.8 82.8,87 80,87L20,87C17.2,87 15,84.8 15,82L15,17C15,14.2 17.2,12 20,12L80,12C82.8,12 85,14.2 85,17L85,82Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M77.5,17L22.5,17C21.1,17 20,18.1 20,19.5L20,79.5C20,80.9 21.1,82 22.5,82L77.5,82C78.9,82 80,80.9 80,79.5L80,19.5C80,18.1 78.9,17 77.5,17ZM50,74.5C36.2,74.5 25,63.3 25,49.5C25,35.7 36.2,24.5 50,24.5C63.8,24.5 75,35.7 75,49.5C75,63.3 63.8,74.5 50,74.5Z" style="fill:rgb(0,68,17);fill-rule:nonzero;"/>
    </g>
</svg>`,
    'hazard-warning': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M95,32L95,12C95,6.5 90.5,2 85,2L65,2L65,22L35,22L35,2L15,2C9.5,2 5,6.5 5,12L5,32L30,32L30,67L5,67L5,87C5,92.5 9.5,97 15,97L35,97L35,77L65,77L65,97L85,97C90.5,97 95,92.5 95,87L95,67L70,67L70,32L95,32Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
</svg>`,
    'high-radioactivity': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M20,20.7L20,78.2L46.2,49.5L20,20.7Z" style="fill:rgb(255,170,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M80,78.2L80,20.7L53.8,49.5L80,78.2Z" style="fill:rgb(255,170,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M23.8,82L76.2,82L50,53.2L23.8,82Z" style="fill:black;fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M76.2,17L23.8,17L50,45.8L76.2,17Z" style="fill:black;fill-rule:nonzero;"/>
    </g>
    <path d="M191.055,899.233C193.951,899.737 196.94,900 200,900L800,900C802.663,900 805.271,899.801 807.812,899.417L891.201,991.064C878.622,996.8 864.667,1000 850,1000L150,1000C134.882,1000 120.519,996.6 107.639,990.526L191.055,899.233ZM930.135,90.358C942.6,107.039 950,127.697 950,150L950,900C950,922.528 942.45,943.378 929.756,960.145L846.515,868.66C848.768,862.918 850,856.627 850,850L850,200C850,193.517 848.821,187.356 846.661,181.715L930.135,90.358ZM70.677,89.286L153.776,180.614C151.339,186.551 150,193.093 150,200L150,850C150,856.239 151.092,862.181 153.1,867.647L69.497,959.146C57.254,942.552 50,922.082 50,900L50,150C50,127.217 57.722,106.149 70.677,89.286ZM850,50C864.894,50 879.054,53.3 891.785,59.205L808.232,150.649C805.559,150.222 802.81,150 800,150L200,150C197.631,150 195.304,150.158 193.03,150.463L109.473,58.631C121.876,53.087 135.595,50 150,50L850,50Z" style="fill:rgb(160,0,0);"/>
</svg>`,
    'intercom': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M85,2L15,2C9.5,2 5,6.5 5,12L5,87C5,92.5 9.5,97 15,97L85,97C90.5,97 95,92.5 95,87L95,12C95,6.5 90.5,2 85,2ZM85,82C85,84.8 82.8,87 80,87L20,87C17.2,87 15,84.8 15,82L15,17C15,14.2 17.2,12 20,12L80,12C82.8,12 85,14.2 85,17L85,82Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M39.6,17L22.5,17C21.1,17 20,18.1 20,19.5L20,57L39.6,57L50,37L39.6,17Z" style="fill:rgb(96,96,96);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M50,62L60.4,82L77.5,82C78.9,82 80,80.9 80,79.5L80,42L60.4,42L50,62Z" style="fill:rgb(96,96,96);fill-rule:nonzero;"/>
    </g>
</svg>`,
    'ladderway': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M85,2L15,2C9.5,2 5,6.5 5,12L5,87C5,92.5 9.5,97 15,97L85,97C90.5,97 95,92.5 95,87L95,12C95,6.5 90.5,2 85,2ZM85,82C85,84.8 82.8,87 80,87L20,87C17.2,87 15,84.8 15,82L15,17C15,14.2 17.2,12 20,12L80,12C82.8,12 85,14.2 85,17L85,82Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M77.5,17L70,17L70,22C70,24.8 67.8,27 65,27L35,27C32.2,27 30,24.8 30,22L30,17L22.5,17C21.1,17 20,18.1 20,19.5L20,79.5C20,80.9 21.1,82 22.5,82L30,82L30,77C30,74.2 32.2,72 35,72L65,72C67.8,72 70,74.2 70,77L70,82L77.5,82C78.9,82 80,80.9 80,79.5L80,19.5C80,18.1 78.9,17 77.5,17ZM70,57C70,59.8 67.8,62 65,62L35,62C32.2,62 30,59.8 30,57L30,42C30,39.2 32.2,37 35,37L65,37C67.8,37 70,39.2 70,42L70,57Z" style="fill:rgb(96,96,96);fill-rule:nonzero;"/>
    </g>
</svg>`,
    'laser': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M5,12L5,47L15,47L15,17C15,14.2 17.2,12 20,12L47.5,12L47.5,2L15,2C9.5,2 5,6.5 5,12Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M15,82L15,52L5,52L5,87C5,92.5 9.5,97 15,97L47.5,97L47.5,87L20,87C17.2,87 15,84.8 15,82Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M85,2L52.5,2L52.5,12L80,12C82.8,12 85,14.2 85,17L85,47L95,47L95,12C95,6.5 90.5,2 85,2Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M85,82C85,84.8 82.8,87 80,87L52.5,87L52.5,97L85,97C90.5,97 95,92.5 95,87L95,52L85,52L85,82Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M80,47L80,19.5C80,18.1 78.9,17 77.5,17L52.5,17L52.5,32L67.5,47L80,47Z" style="fill:rgb(96,96,96);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M20,19.5L20,47L32.5,47L47.5,32L47.5,17L22.5,17C21.1,17 20,18.1 20,19.5Z" style="fill:rgb(96,96,96);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M20,52L20,79.5C20,80.9 21.1,82 22.5,82L47.5,82L47.5,67L32.5,52L20,52Z" style="fill:rgb(96,96,96);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M80,79.5L80,52L67.5,52L52.5,67L52.5,82L77.5,82C78.9,82 80,80.9 80,79.5Z" style="fill:rgb(96,96,96);fill-rule:nonzero;"/>
    </g>
</svg>`,
    'life-support-system': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M85,2L15,2C9.5,2 5,6.5 5,12L5,87C5,92.5 9.5,97 15,97L85,97C90.5,97 95,92.5 95,87L95,12C95,6.5 90.5,2 85,2ZM85,82C85,84.8 82.8,87 80,87L20,87C17.2,87 15,84.8 15,82L15,17C15,14.2 17.2,12 20,12L80,12C82.8,12 85,14.2 85,17L85,82Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M35,42L30,42C27.2,42 25,39.8 25,37L25,17L22.5,17C21.1,17 20,18.1 20,19.5L20,47L35,47L35,42Z" style="fill:rgb(96,96,96);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M35,32L65,32L65,37L70,37L70,17L30,17L30,37L35,37L35,32Z" style="fill:rgb(96,96,96);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M77.5,17L75,17L75,37C75,39.8 72.8,42 70,42L65,42L65,47L80,47L80,19.5C80,18.1 78.9,17 77.5,17Z" style="fill:rgb(96,96,96);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M65,67L35,67L35,62L30,62L30,82L70,82L70,62L65,62L65,67Z" style="fill:rgb(96,96,96);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M35,57L35,52L20,52L20,79.5C20,80.9 21.1,82 22.5,82L25,82L25,62C25,59.2 27.2,57 30,57L35,57Z" style="fill:rgb(96,96,96);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M65,57L70,57C72.8,57 75,59.2 75,62L75,82L77.5,82C78.9,82 80,80.9 80,79.5L80,52L65,52L65,57Z" style="fill:rgb(96,96,96);fill-rule:nonzero;"/>
    </g>
</svg>`,
    'maintenance': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M85,2L15,2C9.5,2 5,6.5 5,12L5,87C5,92.5 9.5,97 15,97L85,97C90.5,97 95,92.5 95,87L95,12C95,6.5 90.5,2 85,2ZM85,82C85,84.8 82.8,87 80,87L20,87C17.2,87 15,84.8 15,82L15,17C15,14.2 17.2,12 20,12L80,12C82.8,12 85,14.2 85,17L85,82Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M77.5,17L75,17L75,47L65,59.5L60,59.5L60,17L40,17L40,59.5L35,59.5L25,47L25,17L22.5,17C21.1,17 20,18.1 20,19.5L20,79.5C20,80.9 21.1,82 22.5,82L42.5,82L42.5,47L57.5,47L57.5,82L77.5,82C78.9,82 80,80.9 80,79.5L80,19.5C80,18.1 78.9,17 77.5,17Z" style="fill:rgb(96,96,96);fill-rule:nonzero;"/>
    </g>
</svg>`,
    'no-pressure-gravity-suit-required': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M85,2L15,2C9.5,2 5,6.5 5,12L5,87C5,92.5 9.5,97 15,97L85,97C90.5,97 95,92.5 95,87L95,12C95,6.5 90.5,2 85,2ZM75,62C75,63.4 73.9,64.5 72.5,64.5L65,64.5C63.6,64.5 62.5,65.6 62.5,67L62.5,69.5C62.5,76.5 56.7,82.2 49.6,82C42.8,81.8 37.5,76.1 37.5,69.2L37.5,67C37.5,65.6 36.4,64.5 35,64.5L27.5,64.5C26.1,64.5 25,63.4 25,62L25,52C25,50.6 26.1,49.5 27.5,49.5L35,49.5C36.4,49.5 37.5,48.4 37.5,47L37.5,40.5C37.5,39.8 37.2,39.2 36.8,38.7L26.8,28.7C25.8,27.7 25.8,26.1 26.8,25.2L33.3,18.7C34.3,17.7 35.9,17.7 36.8,18.7L48.3,30.2C49.3,31.2 50.9,31.2 51.8,30.2L63.3,18.7C64.3,17.7 65.9,17.7 66.8,18.7L73.3,25.2C74.3,26.2 74.3,27.8 73.3,28.7L63.3,38.7C62.8,39.2 62.6,39.8 62.6,40.5L62.6,47C62.6,48.4 63.7,49.5 65.1,49.5L72.6,49.5C74,49.5 75.1,50.6 75.1,52L75.1,62L75,62Z" style="fill:black;fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <circle cx="50" cy="69.5" r="7.5" style="fill:rgb(160,0,0);"/>
    </g>
</svg>`,
    'non-pressurised-area-beyond': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M20,79.5C20,80.9 21.1,82 22.5,82L77.5,82C78.9,82 80,80.9 80,79.5L80,17L95,17L95,12C95,6.5 90.5,2 85,2L15,2C9.5,2 5,6.5 5,12L5,17L20,17L20,79.5Z" style="fill:black;fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M15,82L15,22L5,22L5,87C5,92.5 9.5,97 15,97L25,97L25,87L20,87C17.2,87 15,84.8 15,82Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <rect x="30" y="87" width="40" height="10" style="fill:rgb(160,0,0);"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M85,82C85,84.8 82.8,87 80,87L75,87L75,97L85,97C90.5,97 95,92.5 95,87L95,22L85,22L85,82Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
</svg>`,
    'photonic-system-fibre-optics': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M65,62L35,62L35,82L77.5,82C78.9,82 80,80.9 80,79.5L80,32L35,32L35,42L65,42C67.8,42 70,44.2 70,47L70,57C70,59.8 67.8,62 65,62Z" style="fill:rgb(96,96,96);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M65,57L65,47L35,47C32.2,47 30,44.8 30,42L30,32C30,29.2 32.2,27 35,27L80,27L80,19.5C80,18.1 78.9,17 77.5,17L22.5,17C21.1,17 20,18.1 20,19.5L20,79.5C20,80.9 21.1,82 22.5,82L30,82L30,62C30,59.2 32.2,57 35,57L65,57Z" style="fill:rgb(96,96,96);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M85,82C85,84.8 82.8,87 80,87L35,87L35,97L85,97C90.5,97 95,92.5 95,87L95,32L85,32L85,82Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M85,2L15,2C9.5,2 5,6.5 5,12L5,87C5,92.5 9.5,97 15,97L30,97L30,87L20,87C17.2,87 15,84.8 15,82L15,17C15,14.2 17.2,12 20,12L80,12C82.8,12 85,14.2 85,17L85,27L95,27L95,12C95,6.5 90.5,2 85,2Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
</svg>`,
    'pressure-suit-locker': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M77.5,17L22.5,17C21.1,17 20,18.1 20,19.5L20,79.5C20,80.9 21.1,82 22.5,82L37.5,82L37.5,54.5C37.5,53.1 36.4,52 35,52L27.5,52C26.1,52 25,50.9 25,49.5L25,39.5C25,38.1 26.1,37 27.5,37L35,37C36.4,37 37.5,35.9 37.5,34.5L37.5,32C37.5,25 43.3,19.3 50.4,19.5C57.2,19.7 62.5,25.4 62.5,32.3L62.5,34.5C62.5,35.9 63.6,37 65,37L72.5,37C73.9,37 75,38.1 75,39.5L75,49.5C75,50.9 73.9,52 72.5,52L65,52C63.6,52 62.5,53.1 62.5,54.5L62.5,82L77.5,82C78.9,82 80,80.9 80,79.5L80,19.5C80,18.1 78.9,17 77.5,17Z" style="fill:rgb(96,96,96);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <circle cx="50" cy="32" r="7.5" style="fill:rgb(96,96,96);"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M85,2L15,2C9.5,2 5,6.5 5,12L5,87C5,92.5 9.5,97 15,97L85,97C90.5,97 95,92.5 95,87L95,12C95,6.5 90.5,2 85,2ZM85,82C85,84.8 82.8,87 80,87L20,87C17.2,87 15,84.8 15,82L15,17C15,14.2 17.2,12 20,12L80,12C82.8,12 85,14.2 85,17L85,82Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
</svg>`,
    'pressurised-area': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,4.91497e-31,4.91497e-31,10,7.90479e-14,30)">
        <path d="M85,2L15,2C9.5,2 5,6.5 5,12L5,87C5,92.5 9.5,97 15,97L85,97C90.5,97 95,92.5 95,87L95,12C95,6.5 90.5,2 85,2ZM85,82C85,84.8 82.8,87 80,87L20,87C17.2,87 15,84.8 15,82L15,17C15,14.2 17.2,12 20,12L80,12C82.8,12 85,14.2 85,17L85,82Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
</svg>`,
    'pressurised-with-artificial-gravity': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M85,2L15,2C9.5,2 5,6.5 5,12L5,87C5,92.5 9.5,97 15,97L85,97C90.5,97 95,92.5 95,87L95,12C95,6.5 90.5,2 85,2ZM85,82C85,84.8 82.8,87 80,87L55,87L55,49.5L45,49.5L45,87L20,87C17.2,87 15,84.8 15,82L15,17C15,14.2 17.2,12 20,12L80,12C82.8,12 85,14.2 85,17L85,82Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <circle cx="50" cy="39.5" r="7.5" style="fill:rgb(160,0,0);"/>
    </g>
</svg>`,
    'radiation-hazard': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M85,2L15,2C9.5,2 5,6.5 5,12L5,87C5,92.5 9.5,97 15,97L85,97C90.5,97 95,92.5 95,87L95,12C95,6.5 90.5,2 85,2ZM85,82C85,84.8 82.8,87 80,87L20,87C17.2,87 15,84.8 15,82L15,17C15,14.2 17.2,12 20,12L80,12C82.8,12 85,14.2 85,17L85,82Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(1,0,0,1.09681,0,-60.4019)">
        <rect x="234.053" y="623.941" width="532.941" height="179.701" style="fill:black;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M77.5,17L22.5,17C21.1,17 20,18.1 20,19.5L20,79.5C20,80.9 21.1,82 22.5,82L77.5,82C78.9,82 80,80.9 80,79.5L80,19.5C80,18.1 78.9,17 77.5,17ZM57.5,74.5L25,74.5L25,64.5L57.5,64.5L57.5,74.5ZM67.5,77C63.4,77 60,73.6 60,69.5C60,65.4 63.4,62 67.5,62C71.6,62 75,65.4 75,69.5C75,73.6 71.6,77 67.5,77Z" style="fill:rgb(255,176,0);fill-rule:nonzero;"/>
    </g>
</svg>`,
    'refrigeration': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M85,2L15,2C9.5,2 5,6.5 5,12L5,87C5,92.5 9.5,97 15,97L85,97C90.5,97 95,92.5 95,87L95,12C95,6.5 90.5,2 85,2ZM85,82C85,84.8 82.8,87 80,87L20,87C17.2,87 15,84.8 15,82L15,17C15,14.2 17.2,12 20,12L80,12C82.8,12 85,14.2 85,17L85,82Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,0,30)">
        <path d="M77.5,17L22.5,17C21.1,17 20,18.1 20,19.5L20,79.5C20,80.9 21.1,82 22.5,82L77.5,82C78.9,82 80,80.9 80,79.5L80,19.5C80,18.1 78.9,17 77.5,17ZM70,72L30,72L30,27L70,27L70,72Z" style="fill:rgb(10,10,112);fill-rule:nonzero;"/>
    </g>
</svg>`,
    'storage-non-organic': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M85,2L15,2C9.5,2 5,6.5 5,12L5,87C5,92.5 9.5,97 15,97L85,97C90.5,97 95,92.5 95,87L95,12C95,6.5 90.5,2 85,2ZM85,82C85,84.8 82.8,87 80,87L20,87C17.2,87 15,84.8 15,82L15,17C15,14.2 17.2,12 20,12L80,12C82.8,12 85,14.2 85,17L85,82Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,0,30)">
        <path d="M77.5,17L22.5,17C21.1,17 20,18.1 20,19.5L20,79.5C20,80.9 21.1,82 22.5,82L77.5,82C78.9,82 80,80.9 80,79.5L80,19.5C80,18.1 78.9,17 77.5,17ZM70,72L30,72L30,27L70,27L70,72Z" style="fill:rgb(96,96,96);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <rect x="35" y="32" width="30" height="35" style="fill:rgb(96,96,96);"/>
    </g>
</svg>`,
    'storage-organic-foodstuffs': `<svg width="100%" height="100%" viewBox="0 0 1000 1050" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
    <path d="M150,1050C67.213,1050 0,982.787 0,900C0,900 0,150 0,150C0,67.213 67.212,0 150,0C150,0 850,0 850,0C932.788,0 1000,67.213 1000,150C1000,150 1000,900 1000,900C1000,982.787 932.787,1050 850,1050L150,1050Z" style="fill:white;"/>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <path d="M85,2L15,2C9.5,2 5,6.5 5,12L5,87C5,92.5 9.5,97 15,97L85,97C90.5,97 95,92.5 95,87L95,12C95,6.5 90.5,2 85,2ZM85,82C85,84.8 82.8,87 80,87L20,87C17.2,87 15,84.8 15,82L15,17C15,14.2 17.2,12 20,12L80,12C82.8,12 85,14.2 85,17L85,82Z" style="fill:rgb(160,0,0);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,0,30)">
        <path d="M77.5,17L22.5,17C21.1,17 20,18.1 20,19.5L20,79.5C20,80.9 21.1,82 22.5,82L77.5,82C78.9,82 80,80.9 80,79.5L80,19.5C80,18.1 78.9,17 77.5,17ZM70,72L30,72L30,27L70,27L70,72Z" style="fill:rgb(96,96,96);fill-rule:nonzero;"/>
    </g>
    <g transform="matrix(10,-3.9443e-31,0,10,-1.13687e-13,30)">
        <rect x="35" y="32" width="30" height="35" style="fill:rgb(0,68,17);"/>
    </g>
</svg>`
};
