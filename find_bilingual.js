const fs = require('fs');

const src = fs.readFileSync('app/src/main/assets/index.html', 'utf8');

// Find strings with English and Telugu/Hindi separated by slash or in same label
const regex = /['"`]([A-Za-z\s]+[\/\|][\u0C00-\u0C7F\u0900-\u097F\s]+|[\u0C00-\u0C7F\u0900-\u097F\s]+[\/\|][A-Za-z\s]+)['"`]/g;
let m;
const matches = new Set();
while ((m = regex.exec(src)) !== null) {
    matches.add(m[1]);
}
console.log('Bilingual slash strings found:', [...matches]);
