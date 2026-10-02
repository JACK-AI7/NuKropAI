const fs = require('fs');

function applyFinalLanguagePolishing(filePath) {
    let src = fs.readFileSync(filePath, 'utf8');

    // 1. Farmer Profile Rating Row fix
    const farmerRatingOld = `<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;">
          \${[[
      ['2.5', TL('Land (Ac)', 'భూమి (ఎకరాలు)', 'जमीन (एकड़)'), '#86EFAC'],
      ['850', TL('Soil Health', 'నేల ఆరోగ్యం', 'मृदा स्वास्थ्य'), '#FFFFFF'],
      ['A+', TL('Grade', 'గ్రేడ్', 'ग्रेड'), '#FFFFFF']
    ]].map(([val,label,color])=>\`
            <div style="background:rgba(255,255,255,0.12);border-radius:13px;padding:10px 12px;text-align:center;">
              <div style="font-size:20px;font-weight:900;color:\${color};letter-spacing:-0.3px;">\${val}</div>
              <div style="font-size:10px;color:#D1FAE5;font-weight:700;margin-top:2px;">\${label}</div>
            </div>
          \`).join('')}
        </div>`;

    const farmerRatingNew = `<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;">
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
        </div>`;

    if (src.includes(farmerRatingOld)) {
        src = src.replace(farmerRatingOld, farmerRatingNew);
    }

    // 2. Driver Profile Tab Menu & Rating Row
    const driverProfileOld = `<!-- Rating row -->
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;">
          \${[['4.9','Rating','var(--r-yellow)'],['420','Hauls','#FFFFFF'],['98%','Acceptance','#FFFFFF']].map(([val,label,color])=>\`
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
            ['M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2M9 5a2 2 0 0 0 2 2h2a2 2 0 0 0 2-2M9 5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2','Haul History','All past trips & receipts', 'openDriverHaulHistoryModal()'],
            ['M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z','Insurance & FASTag','TS 03 UB 4491 · Active till Dec 2025', 'openDriverInsuranceFastagModal()'],
            ['M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 0-2-2z|M9 22V12h6v10','Vehicle Documents','RC, Permit, Fitness, PUC', 'openDriverVehicleDocsModal()'],
            ['M3 3v18h18|M18 17V9|M13 17V5|M8 17v-3','Settings','App preferences', 'openLanguageSelectorModal()'],
            ['M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0zm-5 0a4 4 0 1 1-8 0 4 4 0 0 1 8 0z','Help & Support','24/7 driver helpline', 'openSupportModal()'],
          ]`;

    const driverProfileNew = `<!-- Rating row -->
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
          ]`;

    if (src.includes(driverProfileOld)) {
        src = src.replace(driverProfileOld, driverProfileNew);
    }

    // 3. Driver Cockpit Bottom Nav
    const driverBottomNavOld = `\${[
          {key:'map',label:'Map',svg:'<polygon points="3 11 22 2 13 21 11 13 3 11"/>'},
          {key:'earnings',label:'Earnings',svg:'<line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>'},
          {key:'profile',label:'Profile',svg:'<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>'},
        ].map(t=>\``;

    const driverBottomNavNew = `\${[
          {key:'map',label:TL('Map', 'మ్యాప్', 'नक्शा'),svg:'<polygon points="3 11 22 2 13 21 11 13 3 11"/>'},
          {key:'earnings',label:TL('Earnings', 'ఆదాయం', 'कमाई'),svg:'<line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>'},
          {key:'profile',label:TL('Profile', 'ప్రొఫైల్', 'प्रोफ़ाइल'),svg:'<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>'},
        ].map(t=>\``;

    if (src.includes(driverBottomNavOld)) {
        src = src.replace(driverBottomNavOld, driverBottomNavNew);
    }

    // 4. Driver Cockpit Verified Farmer string
    src = src.replaceAll('★ 4.9 · Verified Farmer', `★ 4.9 · \${TL('Verified Farmer', 'ధృవీకరించబడిన రైతు', 'सत्यापित किसान')}`);

    // 5. GramHaul Booking Sheet Strings
    src = src.replaceAll('<span style="font-size:11px;font-weight:800;color:#64748B;letter-spacing:0.4px;">FROM (PICKUP FARM)</span>', `<span style="font-size:11px;font-weight:800;color:#64748B;letter-spacing:0.4px;">\${TL('FROM (PICKUP FARM)', 'పికప్ లొకేషన్ (పొలం)', 'पिकअप स्थान (खेत)')}</span>`);
    src = src.replaceAll('<span style="font-size:11px;font-weight:800;color:#64748B;letter-spacing:0.4px;">TO (APMC MANDI)</span>', `<span style="font-size:11px;font-weight:800;color:#64748B;letter-spacing:0.4px;">\${TL('TO (APMC MANDI)', 'డ్రాప్ లొకేషన్ (మండి)', 'ड्रॉप स्थान (मंडी)')}</span>`);
    src = src.replaceAll('🌾 CROP COMMODITY', `🌾 \${TL('CROP COMMODITY', 'పంట రకం', 'फसल का प्रकार')}`);
    src = src.replaceAll('📦 LOAD BAGS / SACKS', `📦 \${TL('LOAD BAGS / SACKS', 'బస్తాల సంఖ్య / లోడ్', 'बोरियों की संख्या / वजन')}`);
    src = src.replaceAll('🚚 CHOOSE COMMERCIAL TRUCK TYPE', `🚚 \${TL('CHOOSE COMMERCIAL TRUCK TYPE', 'రవాణా వాహనాన్ని ఎంచుకోండి', 'व्यावसायिक वाहन चुनें')}`);
    src = src.replaceAll('>Edit</button>', `>\${TL('Edit', 'మార్చు', 'बदलें')}</button>`);
    src = src.replaceAll('Cotton (పత్తి)', `\${getLocalizedCropName('cotton')}`);
    src = src.replaceAll('>Available</span>', `>\${TL('Available', 'అందుబాటులో ఉంది', 'उपलब्ध')}</span>`);
    src = src.replaceAll('>Bulk Pool</span>', `>\${TL('Bulk Pool', 'బల్క్ పూల్', 'बल्क पूल')}</span>`);
    src = src.replaceAll('143 OpenFarm crops', `143 \${(typeof currentLang!=='undefined'&&currentLang==='te')?'పంటలు':((typeof currentLang!=='undefined'&&currentLang==='hi')?'फसलें':'crops')}`);

    fs.writeFileSync(filePath, src, 'utf8');
    console.log('[OK] Applied final language polishing to:', filePath);
}

applyFinalLanguagePolishing('app/src/main/assets/index.html');
applyFinalLanguagePolishing('nukrop_emulator.html');
