const fs = require('fs');

function applyCleanViews(filePath) {
    let src = fs.readFileSync(filePath, 'utf8');

    // 1. Full clean APP_VIEWS.profile
    const cleanProfileView = `profile: () => {
    const t = I18N[currentLang] || I18N.te;
    const isTe = currentLang === 'te';
    const isHi = currentLang === 'hi';

    const curName = farmerProfile.name[currentLang] || farmerProfile.name.en;
    const curVillage = farmerProfile.village[currentLang] || farmerProfile.village.en;

    return \`
    <div style="background:#F3F4F6;min-height:100vh;padding-bottom:90px;">
      <!-- Profile hero -->
      <div style="background:#064E3B;padding:max(48px, env(safe-area-inset-top, 48px)) 20px 24px;border-radius:0 0 24px 24px;">
        <div style="display:flex;align-items:center;gap:16px;margin-bottom:18px;">
          <div style="width:64px;height:64px;border-radius:50%;background:#86EFAC;display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:900;color:#064E3B;flex-shrink:0;box-shadow:0 4px 12px rgba(134,239,172,0.3);">R</div>
          <div style="flex:1;">
            <div style="font-size:20px;font-weight:900;color:#FFFFFF;letter-spacing:-0.3px;">\${curName}</div>
            <div style="font-size:12px;color:#A7F3D0;margin-top:2px;">ID: \${farmerProfile.farmerId}</div>
            <div style="font-size:12px;color:#A7F3D0;">📍 \${curVillage}</div>
          </div>
        </div>
        <!-- Rating row -->
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;">
          \${[
            ['2.5', TL('Land (Ac)', 'భూమి (ఎకరాలు)', 'जमीन (एकड़)'), '#86EFAC'],
            ['850', TL('Soil Health', 'నేల ఆరోగ్యం', 'मृदा स्वास्थ्य'), '#FFFFFF'],
            ['A+', TL('Grade', 'గ్రేడ్', 'ग्रेड'), '#FFFFFF']
          ].map(([val,label,color])=>\`
            <div style="background:rgba(255,255,255,0.12);border-radius:13px;padding:10px 12px;text-align:center;">
              <div style="font-size:20px;font-weight:900;color:\${color};letter-spacing:-0.3px;">\${val}</div>
              <div style="font-size:10px;color:#D1FAE5;font-weight:700;margin-top:2px;">\${label}</div>
            </div>
          \`).join('')}
        </div>
      </div>

      <!-- Menu items -->
      <div style="padding:16px 16px 0;">
        <div class="r-card" style="background:#FFFFFF;border-radius:20px;box-shadow:0 2px 14px rgba(0,0,0,0.07);overflow:hidden;margin-bottom:14px;">
          \${[
            ['M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2M9 5a2 2 0 0 0 2 2h2a2 2 0 0 0 2-2M9 5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2', TL('AgriStack Identity', 'అగ్రిస్టాక్ గుర్తింపు', 'एग्रीस्टैक पहचान'), TL('TS-WGL-8941 · Verified', 'TS-WGL-8941 · ధృవీకరించబడింది', 'TS-WGL-8941 · सत्यापित'), 'openAgriStackModal()'],
            ['M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z', TL('KCC Loan Status', 'KCC రుణ స్థితి', 'KCC ऋण स्थिति'), TL('Sanctioned: ₹1.25L', 'మంజూరైనది: ₹1.25L', 'स्वीकृत: ₹1.25L'), 'openKccLoanModal()'],
            ['M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z|M9 22V12h6v10', TL('Farm Documents', 'పొలం పత్రాలు', 'कृषि दस्तावेज़'), TL('RoR, Pattadar Passbook', 'పట్టాదారు పాస్‌బుక్, RoR', 'पट्टा पासबुक, खतौनी'), 'openFarmDocsModal()'],
            ['M3 3v18h18|M18 17V9|M13 17V5|M8 17v-3', TL('Settings', 'సెట్టింగ్స్', 'सेटिंग्स'), TL('App preferences', 'యాప్ ప్రాధాన్యతలు', 'ऐप सेटिंग्स'), 'openLanguageSelectorModal()'],
            ['M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0zm-5 0a4 4 0 1 1-8 0 4 4 0 0 1 8 0z', TL('Help & Support', 'సహాయం & మద్దతు', 'सहायता व संपर्क'), TL('24/7 agriculture helpline', '24/7 వ్యవసాయ హెల్ప్‌లైన్', '24/7 कृषि हेल्पलाइन'), 'openSupportModal()']
          ].map(([d,label,sub,action],i)=>\`
            <button onclick="\${action||''}" class="r-btn" style="width:100%;display:flex;align-items:center;gap:14px;padding:14px 18px;background:none;border:none;border-bottom:\${i<4?'1px solid #F9FAFB':'none'};cursor:pointer;text-align:left;">
              <div style="width:40px;height:40px;border-radius:13px;background:#F9FAFB;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#064E3B" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  \${d.split('|').map(p=>\`<path d="\${p}"/>\`).join('')}
                </svg>
              </div>
              <div style="flex:1;min-width:0;">
                <div style="font-size:14px;font-weight:800;color:#111827;">\${label}</div>
                <div style="font-size:11px;color:#6B7280;margin-top:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">\${sub}</div>
              </div>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#D1D5DB" stroke-width="2.5" stroke-linecap="round"><polyline points="9 18 15 12 9 6"/></svg>
            </button>
          \`).join('')}
        </div>
      </div>

      <!-- Farmer Log Out Button -->
      <div style="padding:0 16px 20px;">
        <button onclick="executeUserLogout()" style="width:100%;padding:14px;border-radius:14px;background:#FEF2F2;color:#DC2626;font-size:14px;font-weight:900;border:1.5px solid #FECACA;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;box-shadow:0 4px 14px rgba(220,38,38,0.15);">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
          \${TL('Log Out', 'లాగ్ అవుట్', 'लॉग आउट')}
        </button>
      </div>
    </div>\`;
  }`;

    const profP1 = src.indexOf('profile: () => {');
    const profP2 = src.indexOf('driver_dashboard: () => {', profP1);
    if (profP1 !== -1 && profP2 !== -1) {
        src = src.substring(0, profP1) + cleanProfileView + ',\n\n  ' + src.substring(profP2);
        console.log('Replaced profile view in:', filePath);
    }

    // 2. Clean driver profileTab and bottomNav inside driver_dashboard
    const driverProfTabSearchStart = 'const profileTab = `';
    const driverProfTabSearchEnd = 'const bottomNav = `';
    const dp1 = src.indexOf(driverProfTabSearchStart);
    const dp2 = src.indexOf(driverProfTabSearchEnd, dp1);

    if (dp1 !== -1 && dp2 !== -1) {
        const cleanDriverProfileTab = `const profileTab = \`
    <div style="background:var(--r-bg);min-height:100%;padding-bottom:20px;">
      <!-- Profile hero -->
      <div style="background:var(--r-dark);padding:max(48px, env(safe-area-inset-top, 48px)) 20px 24px;">
        <div style="display:flex;align-items:center;gap:16px;margin-bottom:18px;">
          <div style="width:64px;height:64px;border-radius:50%;background:var(--r-yellow);display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:900;color:var(--r-dark);flex-shrink:0;">S</div>
          <div style="flex:1;">
            <div style="font-size:20px;font-weight:900;color:#FFFFFF;letter-spacing:-0.3px;">\${driverName}</div>
            <div style="font-size:12px;color:#9CA3AF;margin-top:2px;">\${vehicleType}</div>
            <div style="font-size:12px;color:#9CA3AF;">\${vehiclePlate}</div>
          </div>
        </div>
        <!-- Rating row -->
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;">
          \${[
            ['4.9', TL('Rating', 'రేటింగ్', 'रेटिंग'), 'var(--r-yellow)'],
            ['420', TL('Hauls', 'ట్రిప్పులు', 'ट्रिप्स'), '#FFFFFF'],
            ['98%', TL('Acceptance', 'అంగీకారం', 'स्वीकृति'), '#FFFFFF']
          ].map(([val,label,color])=>\`
            <div style="background:rgba(255,255,255,0.08);border-radius:13px;padding:10px 12px;text-align:center;">
              <div style="font-size:20px;font-weight:900;color:\${color};letter-spacing:-0.3px;">\${val}</div>
              <div style="font-size:10px;color:#9CA3AF;font-weight:700;margin-top:2px;">\${label}</div>
            </div>
          \`).join('')}
        </div>
      </div>

      <!-- Menu items -->
      <div style="padding:16px 16px 0;">
        <div class="r-card" style="overflow:hidden;margin-bottom:14px;">
          \${[
            ['M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2M9 5a2 2 0 0 0 2 2h2a2 2 0 0 0 2-2M9 5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2', TL('Haul History', 'రవాణా చరిత్ర', 'ट्रिप इतिहास'), TL('All past trips & receipts', 'గత ట్రిప్పులు & రశీదులు', 'सभी पिछली ट्रिप्स व रसीदें'), 'openDriverHaulHistoryModal()'],
            ['M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z', TL('Insurance & FASTag', 'ఇన్సూరెన్స్ & ఫాస్టాగ్', 'बीमा व फास्टैग'), TL('TS 03 UB 4491 · Active till Dec 2026', 'TS 03 UB 4491 · డిసెంబర్ 2026 వరకు చెల్లుబాటు', 'TS 03 UB 4491 · वैध'), 'openDriverInsuranceFastagModal()'],
            ['M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 0-2-2z|M9 22V12h6v10', TL('Vehicle Documents', 'వాహన పత్రాలు', 'वाहन दस्तावेज़'), TL('RC, Permit, Fitness, PUC', 'RC, పర్మిట్, ఫిట్‌నెస్, PUC', 'आरसी, परमिट, फिटनेस'), 'openDriverVehicleDocsModal()'],
            ['M3 3v18h18|M18 17V9|M13 17V5|M8 17v-3', TL('Settings', 'సెట్టింగ్స్', 'सेटिंग्स'), TL('App preferences', 'యాప్ ప్రాధాన్యతలు', 'ऐप सेटिंग्स'), 'openLanguageSelectorModal()'],
            ['M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0zm-5 0a4 4 0 1 1-8 0 4 4 0 0 1 8 0z', TL('Help & Support', 'సహాయం & మద్దతు', 'सहायता व संपर्क'), TL('24/7 driver helpline', '24/7 డ్రైవర్ హెల్ప్‌లైన్', '24/7 हेल्पलाइन'), 'openSupportModal()']
          ].map(([d,label,sub,action],i)=>\`
            <button onclick="\${action||''}" class="r-btn" style="width:100%;display:flex;align-items:center;gap:14px;padding:14px 18px;background:none;border:none;border-bottom:\${i<4?'1px solid #F9FAFB':'none'};cursor:pointer;text-align:left;">
              <div style="width:40px;height:40px;border-radius:13px;background:#F9FAFB;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--r-dark)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  \${d.split('|').map(p=>\`<path d="\${p}"/>\`).join('')}
                </svg>
              </div>
              <div style="flex:1;min-width:0;">
                <div style="font-size:14px;font-weight:800;color:var(--r-dark);">\${label}</div>
                <div style="font-size:11px;color:#9CA3AF;margin-top:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">\${sub}</div>
              </div>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#D1D5DB" stroke-width="2.5" stroke-linecap="round"><polyline points="9 18 15 12 9 6"/></svg>
            </button>
          \`).join('')}
        </div>

        <!-- Driver Log Out Button -->
        <div style="padding:0 16px 20px;">
          <button onclick="executeUserLogout()" style="width:100%;padding:14px;border-radius:14px;background:#FEF2F2;color:#DC2626;font-size:14px;font-weight:900;border:1.5px solid #FECACA;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;box-shadow:0 4px 14px rgba(220,38,38,0.15);">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
            \${TL('Driver Log Out', 'డ్రైవర్ లాగ్ అవుట్', 'ड्राइवर लॉग आउट')}
          </button>
        </div>
      </div>
    </div>\`;\n\n    `;
        src = src.substring(0, dp1) + cleanDriverProfileTab + src.substring(dp2);
        console.log('Replaced driver profile tab in:', filePath);
    }

    // 3. Driver Bottom Nav tabs
    const bNavStart = 'const bottomNav = `';
    const bNavEnd = 'const tabContent = activeTab===\'earnings\'';
    const bn1 = src.indexOf(bNavStart);
    const bn2 = src.indexOf(bNavEnd, bn1);

    if (bn1 !== -1 && bn2 !== -1) {
        const cleanBottomNav = `const bottomNav = \`
    <div style="position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#FFFFFF;border-top:1px solid #F3F4F6;z-index:9100;padding:6px 0 max(env(safe-area-inset-bottom),10px);box-shadow:0 -2px 16px rgba(0,0,0,0.07);">
      \${(!activeTrip && activeTab === 'map') ? \`
      <!-- CENTERED ON DUTY TOGGLE -->
      <div style="position:absolute; top:-28px; left:50%; transform:translateX(-50%);">
        <button class="r-btn \${isOnline ? 'r-online-pulse' : ''}" onclick="toggleGhDriverOnline()" style="display:flex;align-items:center;gap:10px;background:\${isOnline ? 'var(--r-dark)' : '#FFFFFF'};border:2px solid \${isOnline ? 'var(--r-yellow)' : '#E5E7EB'};border-radius:100px;padding:8px 16px 8px 8px;box-shadow:0 6px 20px rgba(0,0,0,0.15);cursor:pointer; height:46px;">
          <div style="width:28px;height:28px;border-radius:50%;background:\${isOnline ? 'var(--r-yellow)' : '#F3F4F6'};display:flex;align-items:center;justify-content:center;">
            \${isOnline
              ? \`<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--r-dark)" stroke-width="3" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>\`
              : \`<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#6B7280" stroke-width="2.5" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>\`
            }
          </div>
          <div style="text-align:left;">
            <div style="font-size:14px;font-weight:900;color:\${isOnline ? 'var(--r-yellow)' : 'var(--r-dark)'};letter-spacing:-0.2px;line-height:1.2;">\${isOnline ? TL('On Duty', 'డ్యూటీలో ఉన్నారు', 'ड्यूटी पर हैं') : TL('Go Online', 'ఆన్‌లైన్ వెళ్లండి', 'ऑनलाइन जाएं')}</div>
          </div>
        </button>
      </div>
      \` : ''}
            
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;">
        \${[
          {key:'map',label:TL('Map', 'మ్యాప్', 'नक्शा'),svg:'<polygon points="3 11 22 2 13 21 11 13 3 11"/>'},
          {key:'earnings',label:TL('Earnings', 'ఆదాయం', 'कमाई'),svg:'<line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>'},
          {key:'profile',label:TL('Profile', 'ప్రొఫైల్', 'प्रोफ़ाइल'),svg:'<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>'},
        ].map(t=>\`
          <button class="r-nav-item" onclick="ghDriverNavTo('\${t.key}')" style="display:flex;flex-direction:column;align-items:center;gap:3px;padding:8px 4px;background:none;border:none;cursor:pointer;position:relative;">
            \${activeTab===t.key ? \`<div style="position:absolute;top:0;left:50%;transform:translateX(-50%);width:32px;height:3px;background:var(--r-yellow);border-radius:0 0 4px 4px;"></div>\` : ''}
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="\${activeTab===t.key?'var(--r-dark)':'#9CA3AF'}" stroke-width="\${activeTab===t.key?'2.5':'1.8'}" stroke-linecap="round" stroke-linejoin="round">
              \${t.svg}
            </svg>
            <span style="font-size:10.5px;font-weight:\${activeTab===t.key?'900':'600'};color:\${activeTab===t.key?'var(--r-dark)':'#9CA3AF'};">\${t.label}</span>
          </button>
        \`).join('')}
      </div>
    </div>\`;\n\n    `;
        src = src.substring(0, bn1) + cleanBottomNav + src.substring(bn2);
        console.log('Replaced driver bottomNav in:', filePath);
    }

    fs.writeFileSync(filePath, src, 'utf8');
    console.log('[OK] Clean views applied to:', filePath);
}

applyCleanViews('app/src/main/assets/index.html');
applyCleanViews('nukrop_emulator.html');
