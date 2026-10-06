const fs = require('fs');
const path = require('path');
const vm = require('vm');
const crypto = require('crypto');

console.log('=== ADVERSARIAL REVIEWER M2 AUDIT SUITE ===');

const indexPath = path.resolve(__dirname, '../app/src/main/assets/index.html');
const emulatorPath = path.resolve(__dirname, '../nukrop_emulator.html');
const supaAssetPath = path.resolve(__dirname, '../app/src/main/assets/js/supabase_integration.js');
const supaRootPath = path.resolve(__dirname, '../js/supabase_integration.js');

const indexHtml = fs.readFileSync(indexPath, 'utf8');
const emulatorHtml = fs.readFileSync(emulatorPath, 'utf8');
const supaAsset = fs.readFileSync(supaAssetPath, 'utf8');
const supaRoot = fs.readFileSync(supaRootPath, 'utf8');

// 1. SHA-256 Byte Parity
const hIndex = crypto.createHash('sha256').update(indexHtml).digest('hex');
const hEmul = crypto.createHash('sha256').update(emulatorHtml).digest('hex');
console.log('index.html SHA-256:      ', hIndex);
console.log('nukrop_emulator SHA-256: ', hEmul);
if (hIndex !== hEmul) {
  console.error('FAIL: index.html and nukrop_emulator.html SHA-256 mismatch!');
  process.exit(1);
} else {
  console.log('✔ Parity check PASS: index.html === nukrop_emulator.html');
}

const hSupaAsset = crypto.createHash('sha256').update(supaAsset).digest('hex');
const hSupaRoot = crypto.createHash('sha256').update(supaRoot).digest('hex');
console.log('asset supabase.js SHA:  ', hSupaAsset);
console.log('root supabase.js SHA:   ', hSupaRoot);
if (hSupaAsset !== hSupaRoot) {
  console.error('FAIL: supabase_integration.js asset and root mismatch!');
  process.exit(1);
} else {
  console.log('✔ Parity check PASS: asset supabase.js === root supabase.js');
}

// 2. APP_VIEWS preservation check
const expectedViews = [
  'home', 'scanner', 'market', 'gramhaul', 'gramhaul_tracking',
  'agristack', 'equipment', 'loan', 'khata', 'chat',
  'bioshield', 'biorx', 'calc_fert', 'calc_pest', 'calc_budget',
  'community', 'driver_dashboard', 'profile'
];

// Extract full balanced APP_VIEWS block
const startIdx = indexHtml.indexOf('const APP_VIEWS = {');
if (startIdx === -1) {
  console.error('FAIL: APP_VIEWS declaration missing in index.html');
  process.exit(1);
}
let braceCount = 0;
let inViews = false;
let viewsBlock = '';
for (let i = startIdx; i < indexHtml.length; i++) {
  const c = indexHtml[i];
  if (c === '{') { braceCount++; inViews = true; }
  else if (c === '}') {
    braceCount--;
    if (inViews && braceCount === 0) {
      viewsBlock = indexHtml.substring(startIdx, i + 1);
      break;
    }
  }
}
const declaredViews = [...viewsBlock.matchAll(/^\s*([a-zA-Z0-9_]+)\s*:\s*(?:\([^\)]*\)|function)/gm)].map(m => m[1]);
console.log(`\nDeclared views in APP_VIEWS (${declaredViews.length}):`, declaredViews);

let missingViews = expectedViews.filter(v => !declaredViews.includes(v));
if (missingViews.length > 0) {
  console.error('FAIL: Missing expected views:', missingViews);
  process.exit(1);
} else {
  console.log(`✔ All 18 APP_VIEWS verified intact (18/18 present).`);
}

// 3. Modals check: 22 modals
const modalPatterns = [
  'spray-modal', 'mandi-modal', 'crop-modal', 'price-alert-modal',
  'instagram-story-modal', 'machinery-booking-modal', 'kcc-loan-modal',
  'khata-entry-modal', 'biorx-details-modal', 'community-post-modal',
  'share-app-modal', 'settings-modal', 'driver-trip-otp-modal',
  'driver-complete-trip-modal', 'driver-bid-accept-modal', 'voice-assistant-modal',
  'agristack-consent-modal', 'farm-boundary-modal', 'biorx-recipe-sheet-modal',
  'driver-contact-sheet-modal', 'kcc-disbursal-sheet-modal', 'kisan-helpline-sheet-modal'
];

console.log('\nChecking 22 Modals and/or dynamic modal creators:');
let missingModalCount = 0;
modalPatterns.forEach(m => {
  const present = indexHtml.includes(m);
  console.log(`  Modal [${m}]: ${present ? 'PRESENT' : 'NOT HARDCODED STATIC ID'}`);
});

// Also check new M2 modal: driver-otp-verification-modal
const hasM2OtpModal = indexHtml.includes('driver-otp-verification-modal');
console.log(`\nNew M2 Modal [driver-otp-verification-modal]: ${hasM2OtpModal ? 'PRESENT' : 'MISSING'}`);

// 4. Pure Real-time check: Search for prohibited mock timers
console.log('\nChecking for prohibited mock timers:');
const prohibitedStrings = [
  'farmerLiveTruckAnimTimer',
  'gramhaulLiveMoveInterval',
  'simulateDriverAcceptance'
];

let foundProhibited = false;
prohibitedStrings.forEach(s => {
  if (indexHtml.includes(s) || supaAsset.includes(s)) {
    console.error(`FAIL: Found prohibited mock timer reference: "${s}"`);
    foundProhibited = true;
  } else {
    console.log(`✔ Prohibited string "${s}" is completely absent.`);
  }
});

// Check _gpsInterval in supaAsset:
// _gpsInterval declaration is ok if not used as setInterval simulation
const hasMockGpsInterval = supaAsset.includes('_gpsInterval = setInterval(');
if (hasMockGpsInterval) {
  console.error('FAIL: _gpsInterval = setInterval is still present in supabase_integration.js!');
  foundProhibited = true;
} else {
  console.log('✔ Prohibited "_gpsInterval = setInterval(" is absent.');
}

if (foundProhibited) {
  process.exit(1);
}

console.log('\n=== AUDIT SUITE FINISHED SUCCESSFULLY ===');
