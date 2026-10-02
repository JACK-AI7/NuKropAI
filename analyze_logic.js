const fs = require('fs');
const content = fs.readFileSync('app/src/main/assets/index.html', 'utf8');

// Extract all localStorage keys
const lsKeys = new Set();
const lsMatches = content.matchAll(/localStorage\.(?:getItem|setItem|removeItem)\(['"]([a-zA-Z0-9_\-]+)['"]/g);
for (const m of lsMatches) {
  lsKeys.add(m[1]);
}
console.log('LocalStorage keys (' + lsKeys.size + '):', Array.from(lsKeys));

// Extract all top-level functions
const fnRegex = /(?:function\s+([a-zA-Z0-9_]+)\s*\(|const\s+([a-zA-Z0-9_]+)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>)/g;
const fns = new Set();
let match;
while ((match = fnRegex.exec(content)) !== null) {
  fns.add(match[1] || match[2]);
}
console.log('\nTotal functions in application:', fns.size);

// Categorize key functions
const navFns = Array.from(fns).filter(f => f.toLowerCase().includes('screen') || f.toLowerCase().includes('nav') || f.toLowerCase().includes('tab') || f.toLowerCase().includes('flow'));
console.log('Navigation / Flow functions (' + navFns.length + '):', navFns);

const modalFns = Array.from(fns).filter(f => f.toLowerCase().includes('modal') || f.toLowerCase().includes('sheet') || f.toLowerCase().includes('dialog'));
console.log('Modal functions (' + modalFns.length + '):', modalFns);

const haulFns = Array.from(fns).filter(f => f.toLowerCase().includes('haul') || f.toLowerCase().includes('truck') || f.toLowerCase().includes('driver'));
console.log('Haul / Driver functions (' + haulFns.length + '):', haulFns);

const aiFns = Array.from(fns).filter(f => f.toLowerCase().includes('scan') || f.toLowerCase().includes('camera') || f.toLowerCase().includes('ai') || f.toLowerCase().includes('leaf') || f.toLowerCase().includes('pest') || f.toLowerCase().includes('disease'));
console.log('AI / Scanner functions (' + aiFns.length + '):', aiFns);
