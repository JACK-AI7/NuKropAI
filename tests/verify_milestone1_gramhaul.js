/**
 * Milestone 1 Verification Suite: Real GramHaul Leaflet Map & Supabase Truck Listings
 */

const fs = require('fs');
const path = require('path');
const assert = require('assert');
const vm = require('vm');

console.log('================================================================================');
console.log('🚚 MILESTONE 1 VERIFICATION: GRAMHAUL LEAFLET MAP & SUPABASE TRUCK LISTINGS');
console.log('================================================================================\n');

let passed = 0;
let total = 0;

function test(name, fn) {
  total++;
  try {
    fn();
    console.log(`  ✔ [PASS] ${name}`);
    passed++;
  } catch (err) {
    console.error(`  ✖ [FAIL] ${name}: ${err.message}`);
    throw err;
  }
}

// 1. Audit Migration File
test('M1.1: SQL Migration backend/migrations/003_gramhaul_truck_listings.sql exists and is valid', () => {
  const migPath = path.join(__dirname, '..', 'backend', 'migrations', '003_gramhaul_truck_listings.sql');
  assert.ok(fs.existsSync(migPath), 'Migration file must exist');
  const sql = fs.readFileSync(migPath, 'utf8');

  assert.ok(sql.includes('CREATE TABLE IF NOT EXISTS public.truck_listings'), 'Must create public.truck_listings');
  assert.ok(sql.includes('ALTER TABLE public.truck_listings ENABLE ROW LEVEL SECURITY'), 'Must enable RLS');
  assert.ok(sql.includes('CREATE POLICY "Allow public read on truck_listings"'), 'Must have SELECT policy');
  assert.ok(sql.includes('CREATE POLICY "Allow public insert on truck_listings"'), 'Must have INSERT policy');
  assert.ok(sql.includes('CREATE INDEX IF NOT EXISTS idx_truck_listings_status'), 'Must have status index');
  assert.ok(sql.includes('TRK-8419') && sql.includes('Warangal Enumamula'), 'Must seed Warangal truck');
  assert.ok(sql.includes('TRK-4920') && sql.includes('Bowenpally APMC'), 'Must seed Bowenpally truck');
  assert.ok(sql.includes('TRK-1102') && sql.includes('Mulugu Hub'), 'Must seed Mulugu truck');
  assert.ok(sql.includes('TRK-3391') && sql.includes('Kazipet'), 'Must seed Kazipet truck');
});

// 2. Audit backend/supabase_setup.sql and backend/schema.sql
test('M1.2: backend/supabase_setup.sql and backend/schema.sql include truck_listings schema', () => {
  const setupSql = fs.readFileSync(path.join(__dirname, '..', 'backend', 'supabase_setup.sql'), 'utf8');
  assert.ok(setupSql.includes('truck_listings'), 'backend/supabase_setup.sql must include truck_listings');

  const schemaSql = fs.readFileSync(path.join(__dirname, '..', 'backend', 'schema.sql'), 'utf8');
  assert.ok(schemaSql.includes('truck_listings'), 'backend/schema.sql must include truck_listings');
});

// 3. Test both HTML files for absence of fake SVG radar and presence of Leaflet map container
const targetFiles = [
  path.join(__dirname, '..', 'nukrop_emulator.html'),
  path.join(__dirname, '..', 'app', 'src', 'main', 'assets', 'index.html')
];

targetFiles.forEach((targetPath) => {
  const relName = path.relative(path.join(__dirname, '..'), targetPath);

  test(`M1.3 [${relName}]: Fake SVG radar #gramhaul-radar-svg is completely removed`, () => {
    const html = fs.readFileSync(targetPath, 'utf8');
    assert.ok(!html.includes('id="gramhaul-radar-svg"'), 'Must NOT contain #gramhaul-radar-svg');
    assert.ok(!html.includes('id=\'gramhaul-radar-svg\''), 'Must NOT contain #gramhaul-radar-svg');
    assert.ok(!html.includes('class="radar-sweep"'), 'Must NOT contain radar-sweep class');
  });

  test(`M1.4 [${relName}]: Interactive Leaflet map container #gramhaul-osm-map is present`, () => {
    const html = fs.readFileSync(targetPath, 'utf8');
    assert.ok(html.includes('id="gramhaul-osm-map"') || html.includes('id="gramhaul-real-osm-map"'), 'Must contain #gramhaul-osm-map or #gramhaul-real-osm-map element');
    assert.ok(html.includes('id="gramhaul-map-wrapper"'), 'Must contain #gramhaul-map-wrapper');
    assert.ok(html.includes('recenterGramhaulMap()'), 'Must contain floating recenter map button');
    assert.ok(html.includes('@keyframes pulseRing'), 'Must contain pulseRing animation');
    assert.ok(html.includes('@keyframes pulseDot'), 'Must contain pulseDot animation');
  });

  test(`M1.5 [${relName}]: Leaflet Map initialization and marker plotting functions exist`, () => {
    const html = fs.readFileSync(targetPath, 'utf8');
    assert.ok(html.includes('function initGramhaulOpenStreetMap'), 'Must define initGramhaulOpenStreetMap');
    assert.ok(html.includes('function plotGramhaulMapMarkers'), 'Must define plotGramhaulMapMarkers');
    assert.ok(html.includes('function computeDistanceKm'), 'Must define computeDistanceKm');
    assert.ok(html.includes('function createTruckIcon'), 'Must define createTruckIcon');
    assert.ok(html.includes('function recenterGramhaulMap'), 'Must define recenterGramhaulMap');
  });

  test(`M1.6 [${relName}]: Supabase PostgREST truck fetching and listing functions exist`, () => {
    const html = fs.readFileSync(targetPath, 'utf8');
    assert.ok(html.includes('function getInitialSeedTrucks'), 'Must define getInitialSeedTrucks');
    assert.ok(html.includes('async function fetchGramhaulTrucks'), 'Must define fetchGramhaulTrucks');
    assert.ok(html.includes('async function submitDriverTruckListing'), 'Must define submitDriverTruckListing');
    assert.ok(html.includes('function refreshGramhaulLocation'), 'Must define refreshGramhaulLocation');
    assert.ok(html.includes('function confirmGramhaulBooking'), 'Must define confirmGramhaulBooking');
    assert.ok(html.includes('/rest/v1/truck_listings'), 'Must connect to Supabase PostgREST endpoint');
  });

  test(`M1.7 [${relName}]: openScreen(\'gramhaul\') initiates map mount and data fetch`, () => {
    const html = fs.readFileSync(targetPath, 'utf8');
    assert.ok(
      html.includes("if (screenKey === 'gramhaul') fetchGramhaulTrucks();") ||
      html.includes("if (screenKey === 'gramhaul')"),
      'Must hook screenKey === gramhaul in openScreen'
    );
    assert.ok(
      html.includes('initGramhaulOpenStreetMap();') && html.includes('invalidateSize()'),
      'Must call initGramhaulOpenStreetMap and invalidateSize in openScreen'
    );
  });
});

// 4. Dynamic Execution & Functional Validation in VM Sandbox
test('M1.8: VM Sandbox execution - initGramhaulOpenStreetMap and Haversine computeDistanceKm', () => {
  const emuHtml = fs.readFileSync(path.join(__dirname, '..', 'nukrop_emulator.html'), 'utf8');

  // Extract script logic containing GramHaul functions
  const scriptMatches = [...emuHtml.matchAll(/<script(?:\s+[^>]*)?>([\s\S]*?)<\/script>/gi)];
  const targetScript = scriptMatches.find(m => m[1].includes('computeDistanceKm'));
  assert.ok(targetScript, 'Script block containing computeDistanceKm must exist');

  // Mock minimal DOM & Leaflet in VM
  let tileLayersAdded = 0;
  let markersAdded = [];
  let polylinesAdded = [];
  let flyToCalled = null;
  let invalidateSizeCalled = false;

  const mockL = {
    map: function(id, opts) {
      return {
        id, opts,
        remove: function() {},
        flyTo: function(coords, zoom) { flyToCalled = { coords, zoom }; },
        invalidateSize: function() { invalidateSizeCalled = true; },
        removeLayer: function() {}
      };
    },
    tileLayer: function(url, opts) {
      return {
        addTo: function(m) { tileLayersAdded++; return this; }
      };
    },
    divIcon: function(opts) { return opts; },
    marker: function(coords, opts) {
      const m = {
        coords, opts,
        addTo: function(m) { markersAdded.push(this); return this; },
        bindPopup: function(html) { this.popupHtml = html; return this; },
        openPopup: function() { this.popupOpened = true; return this; }
      };
      return m;
    },
    polyline: function(coords, opts) {
      const p = {
        coords, opts,
        addTo: function(m) { polylinesAdded.push(this); return this; }
      };
      return p;
    }
  };

  const mockDomElements = {
    'gramhaul-osm-map': { id: 'gramhaul-osm-map' },
    'gramhaul-trucks-container': { innerHTML: '' },
    'gramhaul-active-count-badge': { textContent: '' },
    'gramhaul-coords-text': { textContent: '' },
    'gramhaul-loc-name': { textContent: '' },
    'gramhaul-hud-status': { textContent: '' }
  };

  const sandbox = {
    console,
    L: mockL,
    document: {
      getElementById: (id) => mockDomElements[id] || null,
      querySelector: () => null,
      querySelectorAll: () => []
    },
    setTimeout: setTimeout,
    clearTimeout: clearTimeout,
    setInterval: setInterval,
    clearInterval: clearInterval,
    fetch: async () => ({ ok: true, json: async () => [] }),
    localStorage: {
      getItem: (k) => null,
      setItem: () => {},
      removeItem: () => {},
      clear: () => {}
    },
    navigator: { onLine: true, geolocation: { getCurrentPosition: () => {} } },
    window: {},
    globalThis: {},
    TL: (en, te, hi) => en,
    currentLang: 'en',
    SUPABASE_CONFIG: {
      url: 'https://whqndfphlyeqivnfsfpg.supabase.co',
      anonKey: 'mock-anon-key'
    },
    currentGeoPosition: { lat: 17.9689, lng: 79.5941, locName: 'Warangal Rural' },
    farmKhataTransactions: [],
    showPushNotificationToast: () => {},
    alert: () => {}
  };

  vm.createContext(sandbox);

  // Run the script code in VM
  vm.runInContext(targetScript[1], sandbox);

  // Verify computeDistanceKm (Haversine formula)
  const dist = sandbox.computeDistanceKm(17.9689, 79.5941, 18.0000, 79.6000);
  assert.ok(dist > 3.0 && dist < 4.0, `Haversine distance should be ~3.5km, got ${dist}`);

  // Verify getInitialSeedTrucks
  const seeds = sandbox.getInitialSeedTrucks(17.9689, 79.5941);
  assert.strictEqual(seeds.length, 4, 'Must return 4 seed trucks');
  assert.strictEqual(seeds[0].id, 'TRK-8419');
  assert.strictEqual(seeds[0].destination, 'Warangal Enumamula APMC Yard');

  // Verify initGramhaulOpenStreetMap mounts map and markers
  sandbox.initGramhaulOpenStreetMap(17.9689, 79.5941);
  const mapInst = vm.runInContext('gramhaulMapInstance', sandbox);
  assert.ok(mapInst, 'Map instance must be initialized');
  assert.strictEqual(tileLayersAdded, 1, 'Tile layer must be added');
  assert.ok(markersAdded.length >= 1, 'Farm marker and truck markers must be plotted');
  assert.strictEqual(polylinesAdded.length, 1, 'Mandi route polyline must be plotted');

  // Verify recenterGramhaulMap
  sandbox.recenterGramhaulMap();
  assert.ok(flyToCalled, 'flyTo must be called on recenter');
  assert.strictEqual(flyToCalled.coords[0], 17.9689);
  assert.strictEqual(flyToCalled.coords[1], 79.5941);
});

// 5. Parity verification between nukrop_emulator.html and app/src/main/assets/index.html
test('M1.9: Strict parity of GramHaul functions across both files', () => {
  const emuHtml = fs.readFileSync(path.join(__dirname, '..', 'nukrop_emulator.html'), 'utf8');
  const idxHtml = fs.readFileSync(path.join(__dirname, '..', 'app', 'src', 'main', 'assets', 'index.html'), 'utf8');

  const requiredTokens = [
    'initGramhaulOpenStreetMap',
    'plotGramhaulMapMarkers',
    'computeDistanceKm',
    'createTruckIcon',
    'recenterGramhaulMap',
    'getInitialSeedTrucks',
    'fetchGramhaulTrucks',
    'submitDriverTruckListing',
    'refreshGramhaulLocation',
    'confirmGramhaulBooking',
    'updateGramhaulActiveCount',
    'updateGramhaulLocHUD',
    'openAddTruckDriverModal',
    'closeAddTruckDriverModal'
  ];

  requiredTokens.forEach(token => {
    assert.ok(emuHtml.includes(token), `nukrop_emulator.html must contain ${token}`);
    assert.ok(idxHtml.includes(token), `app/src/main/assets/index.html must contain ${token}`);
  });
});

console.log(`\n================================================================================`);
console.log(`🎉 ALL ${passed}/${total} MILESTONE 1 VERIFICATIONS PASSED WITH ZERO ERRORS!`);
console.log(`================================================================================\n`);
