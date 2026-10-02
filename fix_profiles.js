const fs = require('fs');

function fixFile(file) {
  let content = fs.readFileSync(file, 'utf8');

  // Fix Driver Profile switch button
  content = content.replace(/<button onclick="switchUserRole\('farmer'\)".*?Farmer View.*?<\/button>/s, '');
  
  // Fix Farmer Profile switch button
  content = content.replace(/<button onclick="switchUserRole\('driver'\)".*?Driver View.*?<\/button>/s, '');
  
  content = content.replace(/\['M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2\|M23 21v-2a4 4 0 0 0-3-3\.87\|M16 3\.13a4 4 0 0 1 0 7\.75','Refer & Earn','\?500 per driver referred'\]/g, 
    "['M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z|M3.27 6.96L12 12.01l8.73-5.05|M12 22.08V12','Fuel & Fleet Telematics','OBD-II, 16.4 km/L']");

  content = content.replace(/\['M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2\|M23 21v-2a4 4 0 0 0-3-3\.87\|M16 3\.13a4 4 0 0 1 0 7\.75','Refer & Earn','\?500 per farmer referred'\]/g, 
    "['M3 3v18h18|M18 17V9|M13 17V5|M8 17v-3','Mandi Intelligence','Agmarknet Live Rates']");

  content = content.replace(/\['M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2\|M23 21v-2a4 4 0 0 0-3-3\.87\|M16 3\.13a4 4 0 0 1 0 7\.75','Refer & Earn','.*?referred'\]/g, 
    "['M3 3v18h18|M18 17V9|M13 17V5|M8 17v-3','Settings','App preferences']");

  const driverLogout = `</div>
      <div style="padding:0 16px 20px;">
        <button onclick="localStorage.removeItem('nukrop_user_role'); window.location.reload();" style="width:100%;padding:14px;border-radius:14px;background:#FEF2F2;color:#DC2626;font-size:14px;font-weight:900;border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;box-shadow:0 4px 14px rgba(220,38,38,0.2);">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
          Log Out
        </button>
      </div>`;
      
  content = content.replace(/<\/div>\s*<\/div>\s*<\/div>\s*`;\s*\},\s*profile:\s*\(\)\s*=>\s*\{/g, driverLogout + "\n    </div>\n    `;\n  },\n\n  profile: () => {");
  content = content.replace(/<\/div>\s*<\/div>\s*`;\s*\},\s*\};/g, driverLogout + "\n    </div>\n    `;\n  },\n};");
  
  fs.writeFileSync(file, content, 'utf8');
}

['app/src/main/assets/index.html', 'nukrop_emulator.html'].forEach(fixFile);
console.log('Done');
