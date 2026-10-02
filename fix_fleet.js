const fs = require('fs');

function fixFile(file) {
  let content = fs.readFileSync(file, 'utf8');

  // Change const to let and empty it
  content = content.replace(/const REAL_DRIVERS_FLEET = \{[\s\S]*?\n\};\n/, 'let REAL_DRIVERS_FLEET = {};\nlet _ghRealDriversFetched = false;\n');
  
  // After fetchRealTruckListings definition, let's inject a global fetch
  // Wait, let's modify fetchRealTruckListings itself to populate REAL_DRIVERS_FLEET.
  
  // First, find fetchRealTruckListings and modify its fallback to return empty array instead of fake data
  content = content.replace(/return\s*\[\s*\{\s*driver_id:\s*'drv_suresh'[\s\S]*?\];/g, 'return [];');

  // In openGramhaulBookSheet or when GH is opened, we should fetch and populate.
  // I will just add a global poll or initialize it in renderGramhaul()
  
  fs.writeFileSync(file, content, 'utf8');
}

['app/src/main/assets/index.html', 'nukrop_emulator.html'].forEach(fixFile);
console.log('Fleet Fixed');
