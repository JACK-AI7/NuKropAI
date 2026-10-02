const fs = require('fs');

function fixFile(file) {
  let content = fs.readFileSync(file, 'utf8');

  // Find REAL_DRIVERS_FLEET declaration and change to let
  content = content.replace(/const REAL_DRIVERS_FLEET = \{/, 'let REAL_DRIVERS_FLEET = {');

  // Replace fetchRealTruckListings to actually overwrite the fleet and re-render the list if it's on screen
  const replacement = `async function fetchRealTruckListings() {
  try {
    const res = await fetch(\`\${SUPABASE_REST_URL}/truck_listings?status=eq.ACTIVE&order=created_at.desc\`, {
      headers: SUPABASE_REST_HEADERS
    });
    if (res.ok) {
      const data = await res.json();
      if (Array.isArray(data) && data.length > 0) {
        let newFleet = {};
        data.forEach((t, i) => {
          newFleet['real_'+i] = {
            id: t.id,
            name: t.driver_name || 'Driver ' + (i+1),
            phone: t.driver_phone || 'N/A',
            vehicle: t.vehicle_model || 'Truck',
            plate: t.vehicle_plate || 'N/A',
            rating: '5.0',
            trips: 0,
            etaMins: Math.floor(Math.random()*15)+5
          };
        });
        REAL_DRIVERS_FLEET = newFleet;
        
        // Re-render UI list if we are on the book screen
        const listEl = document.getElementById('gh-driver-list');
        if (listEl && typeof currentGramhaulMandi !== 'undefined') {
          listEl.innerHTML = Object.entries(REAL_DRIVERS_FLEET).map(([key, d], i) => \`
            <div onclick="selectGramhaulDriver('\${key}')" id="gh-truck-\${key}" class="gh-truck-card \${i===0?'gh-selected':''}" style="background:\${i===0?'#F0FDF4':'#FAFAFA'};border:1.5px solid \${i===0?'#16A34A':'#E2E8F0'};border-radius:14px;padding:11px 13px;display:flex;align-items:center;gap:12px;cursor:pointer;\${i===0?'box-shadow:0 3px 10px rgba(22,163,74,0.15);':''}">
              <div style="width:42px;height:42px;border-radius:13px;background:linear-gradient(135deg,\${i===0?'#16A34A,#15803D':i===1?'#2563EB,#1D4ED8':'#7C3AED,#6D28D9'});display:flex;align-items:center;justify-content:center;color:#FFFFFF;font-size:17px;font-weight:900;flex-shrink:0;letter-spacing:-0.5px;">\${d.name[0]}</div>
              <div style="flex:1;min-width:0;">
                <div style="font-size:13px;font-weight:900;color:#0F172A;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">\${d.name}</div>
                <div style="font-size:10px;color:#64748B;font-weight:600;">\${d.vehicle}  \${d.plate}</div>
                <div style="display:flex;align-items:center;gap:8px;margin-top:2px;">
                  <span style="font-size:10px;color:#16A34A;font-weight:800;">? \${d.rating}</span>
                  <span style="font-size:10px;color:#6B7280;font-weight:700;">?? \${d.etaMins} min</span>
                </div>
              </div>
              <div style="text-align:right;flex-shrink:0;">
                <div id="gh-fare-\${key}" style="font-size:16px;font-weight:900;color:#0F172A;letter-spacing:-0.3px;">?\${Math.round(currentGramhaulMandi.distKm * (11 + i*2) + 200)}</div>
                <div style="font-size:9px;color:\${i===0?'#16A34A':'#94A3B8'};font-weight:800;">\${i===0?'Nearest':'Available'}</div>
              </div>
            </div>\`).join('');
            selectGramhaulDriver('real_0'); // Auto-select first
        }
        return data;
      }
    }
  } catch (err) {}
  
  // Return empty array instead of fake data
  REAL_DRIVERS_FLEET = {};
  const listEl = document.getElementById('gh-driver-list');
  if (listEl) {
     listEl.innerHTML = '<div style="padding:20px;text-align:center;color:#64748B;font-size:12px;font-weight:700;">No live drivers nearby.</div>';
  }
  return [];
}`;
  content = content.replace(/async function fetchRealTruckListings\(\) \{[\s\S]*?return \[\s*\{\s*driver_id: 'drv_suresh'[\s\S]*?\];\s*\}/, replacement);

  fs.writeFileSync(file, content, 'utf8');
}

['app/src/main/assets/index.html', 'nukrop_emulator.html'].forEach(fixFile);
console.log('UI Patched');
