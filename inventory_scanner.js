const fs = require('fs');
const content = fs.readFileSync('app/src/main/assets/index.html', 'utf8');

console.log('=== FILE METRICS ===');
console.log('Total characters:', content.length);
console.log('Total lines:', content.split('\n').length);

console.log('\n=== APP_VIEWS KEYS ===');
const appViewsMatch = content.match(/const APP_VIEWS = \{([\s\S]*?)\n\s*(\/\*|\/\/|function|const|let|window)/);
if (appViewsMatch) {
  const viewsBlock = appViewsMatch[1];
  const lines = viewsBlock.split('\n');
  const viewKeys = [];
  lines.forEach(line => {
    const m = line.match(/^\s*([a-zA-Z0-9_]+)\s*:\s*\(/);
    if (m) viewKeys.push(m[1]);
  });
  console.log(`Found ${viewKeys.length} APP_VIEWS:`, viewKeys);
}

console.log('\n=== openScreen SWITCH CASES ===');
const openScreenMatch = content.match(/function openScreen\s*\([^)]*\)\s*\{([\s\S]*?)\n\}/);
if (openScreenMatch) {
  const cases = [];
  const lines = openScreenMatch[1].split('\n');
  lines.forEach(line => {
    const m = line.match(/case\s+['"]([a-zA-Z0-9_\-]+)['"]\s*:/);
    if (m) cases.push(m[1]);
  });
  console.log(`Found ${cases.length} cases in openScreen:`, cases);
}

console.log('\n=== PLANTIX / ONBOARDING SCREENS ===');
const plantixScreens = new Set();
const plantixMatches = content.matchAll(/currentScreen\s*===\s*['"]([a-zA-Z0-9_]+)['"]/g);
for (const m of plantixMatches) {
  plantixScreens.add(m[1]);
}
console.log(`Found ${plantixScreens.size} plantix screens:`, Array.from(plantixScreens));

console.log('\n=== ALL MODAL IDs ===');
const modalRegex = /id=["']([a-zA-Z0-9_\-]+modal[a-zA-Z0-9_\-]*)["']/gi;
const modals = new Set();
let m;
while ((m = modalRegex.exec(content)) !== null) {
  modals.add(m[1]);
}
console.log(`Found ${modals.size} modal IDs:`, Array.from(modals));

console.log('\n=== ALL OVERLAY / SHEET / DRAWER / POPUP IDs ===');
const overlayRegex = /id=["']([a-zA-Z0-9_\-]*(?:overlay|sheet|drawer|popup|dialog|banner|toast|card|view)[a-zA-Z0-9_\-]*)["']/gi;
const overlays = new Set();
while ((m = overlayRegex.exec(content)) !== null) {
  overlays.add(m[1]);
}
console.log(`Found ${overlays.size} overlay/sheet/drawer IDs:`, Array.from(overlays));

console.log('\n=== ALL BOTTOM NAVs / TABS ===');
const navMatches = content.match(/id=["'](bottom-nav[a-zA-Z0-9_\-]*|farmer-bottom-nav|driver-bottom-nav[a-zA-Z0-9_\-]*)["']/gi);
console.log('Nav matches:', navMatches);

console.log('\n=== DATA CATALOGS & CONSTANTS ===');
const catalogs = [];
const catMatches = content.matchAll(/(?:const|let|var)\s+([A-Z0-9_]{3,})\s*=\s*[\[\{]/g);
for (const cm of catMatches) {
  catalogs.push(cm[1]);
}
console.log(`Found ${catalogs.length} data catalogs/constants:`, catalogs);

console.log('\n=== SUPABASE TABLES & CHANNELS ===');
const supaTables = new Set();
const tableMatches = content.matchAll(/\.from\(['"]([a-zA-Z0-9_\-]+)['"]\)/g);
for (const tm of tableMatches) {
  supaTables.add(tm[1]);
}
console.log(`Found ${supaTables.size} Supabase tables referenced:`, Array.from(supaTables));

const supaChannels = new Set();
const chanMatches = content.matchAll(/\.channel\(['"]([a-zA-Z0-9_\-]+)['"]\)/g);
for (const ch of chanMatches) {
  supaChannels.add(ch[1]);
}
console.log(`Found ${supaChannels.size} Supabase channels referenced:`, Array.from(supaChannels));
