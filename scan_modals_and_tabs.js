const fs = require('fs');
const content = fs.readFileSync('app/src/main/assets/index.html', 'utf8');

// 1. Find all modal definitions and their trigger functions
const modalTriggers = [];
const modalRegex = /function\s+(open[A-Za-z0-9_]*Modal[A-Za-z0-9_]*|show[A-Za-z0-9_]*Modal[A-Za-z0-9_]*|open[A-Za-z0-9_]*Sheet[A-Za-z0-9_]*|open[A-Za-z0-9_]*Dialog[A-Za-z0-9_]*)\s*\(/g;
let m;
while ((m = modalRegex.exec(content)) !== null) {
  modalTriggers.push(m[1]);
}
console.log('Modal trigger functions (' + modalTriggers.length + '):', modalTriggers);

// 2. Find all modals in HTML string or DOM creation
const modalHtmlMatches = content.matchAll(/id=["']([a-zA-Z0-9_\-]+modal[a-zA-Z0-9_\-]*)["']/gi);
const modalIds = new Set();
for (const match of modalHtmlMatches) {
  modalIds.add(match[1]);
}
console.log('\nModal IDs in markup (' + modalIds.size + '):', Array.from(modalIds));

// 3. Find all dynamically generated modals (e.g. document.createElement or innerHTML with modal)
const dynamicModals = [];
const dynRegex = /id=["']([a-zA-Z0-9_\-]+(?:modal|sheet|overlay|dialog|popup)[a-zA-Z0-9_\-]*)["']/gi;
const allPopups = new Set();
while ((m = dynRegex.exec(content)) !== null) {
  allPopups.add(m[1]);
}
console.log('\nAll popups/sheets/modals/overlays (' + allPopups.size + '):', Array.from(allPopups));

// 4. Find all sub-tabs in views
// In driver_dashboard:
const driverTabs = content.match(/gh_driver_tab\s*===\s*['"]([a-zA-Z0-9_]+)['"]/g);
console.log('\nDriver cockpit tabs:', driverTabs);

// In market view tabs:
const marketTabs = content.match(/data-mandi-tab=["']([a-zA-Z0-9_]+)["']/g);
console.log('Market tabs:', marketTabs);

// In community view tabs:
const commTabs = content.match(/data-comm-tab=["']([a-zA-Z0-9_]+)["']/g);
console.log('Community tabs:', commTabs);
