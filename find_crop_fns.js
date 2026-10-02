const fs = require('fs');

const src = fs.readFileSync('app/src/main/assets/index.html', 'utf8');

const cropFnMatches = [...src.matchAll(/function\s+[a-zA-Z0-9_]*Crop[a-zA-Z0-9_]*/g)];
console.log('Crop function matches:', cropFnMatches.map(m => m[0]));
