const fs = require('fs');

const src = fs.readFileSync('app/src/main/assets/index.html', 'utf8');

// 1. Farmer profile rating block
let posP = src.indexOf("profile: () => {");
if (posP === -1) posP = src.indexOf("profile:");
console.log('--- Farmer profile rating block ---');
console.log(src.substring(posP, posP + 1800));

// 2. Driver profile tab block
let posD = src.indexOf("const profileTab = `");
console.log('--- Driver profileTab block ---');
console.log(src.substring(posD, posD + 2500));

// 3. Driver bottom nav block
let posB = src.indexOf("const bottomNav = `");
console.log('--- Driver bottomNav block ---');
console.log(src.substring(posB, posB + 1500));

// 4. Gramhaul booking sheet block
let posG = src.indexOf("gramhaul: () => {");
if (posG === -1) posG = src.indexOf("gramhaul:");
console.log('--- Gramhaul booking sheet block ---');
console.log(src.substring(posG + 1500, posG + 3500));
