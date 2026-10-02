const fs = require('fs');

function applySingleLanguagePurity(filePath) {
    let src = fs.readFileSync(filePath, 'utf8');

    // 1. Enrich ONBOARDING_I18N with full permission keys for all languages
    const permI18nAdditions = `
  "perm_badge_1": { "en": "🔒 Permissions (1/3)", "te": "🔒 అనుమతులు (1/3)", "hi": "🔒 अनुमतियाँ (1/3)" },
  "perm_badge_2": { "en": "📍 Permissions (2/3)", "te": "📍 అనుమతులు (2/3)", "hi": "📍 अनुमतियाँ (2/3)" },
  "perm_badge_3": { "en": "🔔 Permissions (3/3)", "te": "🔔 అనుమతులు (3/3)", "hi": "🔔 अनुमतियाँ (3/3)" },
  "skip_btn": { "en": "Skip", "te": "దాటవేయి", "hi": "छोड़ें" },
  "perm_camera_tag": { "en": "📷 SMART SCANNER (1/3)", "te": "📷 AI పంట స్కానర్ (1/3)", "hi": "📷 AI फसल स्कैनर (1/3)" },
  "perm_camera_heading": { "en": "Camera Access & Crop Scanner", "te": "కెమెరా అనుమతి & పంట స్కానర్", "hi": "कैमरा अनुमति व फसल स्कैनर" },
  "perm_camera_desc": { "en": "Allow camera access to instantly snap crop leaves, identify pest infestations, fungal blights, and receive precision dosage recommendations.", "te": "ఆకు ఫోటో తీసి తెగుళ్లు, పురుగులు, పోషక లోపాలను తక్షణమే గుర్తించి సరైన మందుల మోతాదు పొందడానికి కెమెరా అనుమతించండి.", "hi": "पत्तियों की फोटो खींचकर रोग, कीट और पोषण की कमी पहचानने हेतु कैमरा अनुमति दें।" },
  "perm_camera_btn": { "en": "Allow Camera Access →", "te": "కెమెరా అనుమతించండి →", "hi": "कैमरा अनुमति दें →" },
  "perm_location_tag": { "en": "📍 MANDI & WEATHER (2/3)", "te": "📍 మండి & వాతావరణం (2/3)", "hi": "📍 मंडी व मौसम (2/3)" },
  "perm_location_heading": { "en": "GPS Location for Local Mandi Rates", "te": "స్థానిక మార్కెట్ ధరల కోసం GPS లొకేషన్", "hi": "स्थानीय मंडी भाव हेतु GPS लोकेशन" },
  "perm_location_desc": { "en": "Get hyper-local APMC Mandi daily arrival rates, crop logistics truck pairing, and accurate micro-climate rain advisories.", "te": "మీ ప్రాంత సమీప APMC మార్కెట్ ధరలు, గ్రామ్‌హాల్ రవాణా మరియు వర్ష సూచనల కోసం లొకేషన్ అనుమతించండి.", "hi": "नजदीकी APMC मंडी के ताज़ा भाव, वाहन बुकिंग और सटीक मौसम पूर्वानुमान हेतु लोकेशन अनुमति दें।" },
  "perm_location_btn": { "en": "Allow Location Access →", "te": "లొకేషన్ అనుమతించండి →", "hi": "लोकेशन अनुमति दें →" },
  "perm_notif_tag": { "en": "🔔 SMART ALERTS (3/3)", "te": "🔔 పంట హెచ్చరికలు (3/3)", "hi": "🔔 स्मार्ट अलर्ट (3/3)" },
  "perm_notif_heading": { "en": "Real-Time Pest & Weather Alerts", "te": "నిజ-సమయ తెగుళ్లు & వాతావరణ హెచ్చరికలు", "hi": "फसल कीट व मौसम लाइव अलर्ट" },
  "perm_notif_desc": { "en": "Stay alerted on sudden pest outbreaks in your mandal, best pesticide spray timing windows, and surge mandi price jumps.", "te": "మీ మండలంలో వ్యాపించే తెగుళ్ల హెచ్చరికలు, మందుల పిచికారీ సరైన సమయం మరియు మార్కెట్ ధరల పెరుగుదల సమాచారం అందుకోండి.", "hi": "क्षेत्रीय कीट प्रकोप, कीटनाशक छिड़काव का सही समय और मंडी भाव बढ़ने की सूचना तुरंत प्राप्त करें।" },
  "perm_notif_btn": { "en": "Enable Smart Notifications →", "te": "నోటిఫికేషన్లు ప్రారంభించండి →", "hi": "सूचनाएं चालू करें →" },
  "crops_title": { "en": "Select Your Crops", "te": "మీ పంటలను ఎంచుకోండి", "hi": "अपनी फसलें चुनें" },
  "crops_sub": { "en": "You can change this anytime.", "te": "మీరు దీన్ని ఎప్పుడైనా మార్చవచ్చు.", "hi": "आप इसे कभी भी बदल सकते हैं।" },
  "crops_search_placeholder": { "en": "Search crops (e.g. Cotton, Chilli, Wheat)...", "te": "పంటలను వెతకండి (ఉదా: పత్తి, మిరప, గోధుమ)...", "hi": "फसल खोजें (उदा: कपास, मिर्च, गेहूं)..." },
  "crops_selected_suffix": { "en": "Crops Selected", "te": "పంటలు ఎంచుకోబడ్డాయి", "hi": "फसलें चुनी गईं" },
  "crops_next_btn": { "en": "Continue", "te": "కొనసాగించండి", "hi": "आगे बढ़ें" },`;

    if (!src.includes('"perm_badge_1"')) {
        src = src.replace('const ONBOARDING_I18N = {', 'const ONBOARDING_I18N = {\n' + permI18nAdditions);
    }

    // 2. Localized crop display name helper
    const localizedCropFn = `
function getLocalizedCropName(slugOrKey) {
  if (!slugOrKey) return 'Crop';
  const lang = (typeof currentLang !== 'undefined' ? currentLang : 'te') || 'te';

  // 1. Direct match in CROP_TRANSLATIONS
  if (typeof CROP_TRANSLATIONS !== 'undefined' && CROP_TRANSLATIONS[slugOrKey] && CROP_TRANSLATIONS[slugOrKey][lang]) {
    const val = CROP_TRANSLATIONS[slugOrKey][lang];
    if (val && !val.includes('/')) return val;
    if (val && val.includes('/')) {
      const parts = val.split('/').map(s => s.trim());
      return lang === 'te' ? parts[0] : (lang === 'hi' ? parts[0] : parts[0]);
    }
  }

  // 2. Match in MASTER_120_CROPS
  if (typeof MASTER_120_CROPS !== 'undefined') {
    const found = MASTER_120_CROPS.find(c => c.key === slugOrKey || c.slug === slugOrKey);
    if (found && found.name) {
      const m = found.name.match(/^(.*?)\\s*\\((.*?)\\s*\\/\\s*(.*?)\\)$/);
      if (m) {
        if (lang === 'te') return m[2].trim();
        if (lang === 'hi') return m[3].trim();
        if (lang === 'en') return m[1].trim();
      }
      return found.name.split(' (')[0];
    }
  }

  return slugOrKey.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
}
`;

    // Replace getLocalizedCropName if it exists
    const cropFnStart = "function getLocalizedCropName(slug) {";
    if (src.includes(cropFnStart)) {
        const endPos = src.indexOf("return slug.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');\n}");
        if (endPos !== -1) {
            src = src.substring(0, src.indexOf(cropFnStart)) + localizedCropFn + src.substring(endPos + 83);
        }
    }

    // 3. Update renderCameraPermissionScreen, renderLocationPermissionScreen, renderNotificationPermissionScreen
    const camPermOld = `<!-- Top Bar -->
      <div style="position:relative;z-index:10;display:flex;align-items:center;justify-content:space-between;padding:max(52px, env(safe-area-inset-top, 52px)) 20px 0;">
        <div style="background:rgba(30, 41, 59, 0.72);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);color:#FFFFFF;padding:7px 16px;border-radius:999px;font-size:13px;font-weight:700;display:flex;align-items:center;gap:6px;box-shadow:0 4px 12px rgba(0,0,0,0.18);">
          🔒 Permissions (1/3)
        </div>
        <button onclick="skipCameraPermission()" style="background:#FFFFFF;color:#16A34A;border:none;padding:7px 20px;border-radius:999px;font-size:13px;font-weight:800;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,0.18);">
          Skip
        </button>
      </div>

      <!-- Bottom Sheet Card -->
      <div style="position:relative;z-index:10;background:#FFFFFF;border-radius:32px 32px 0 0;padding:28px 24px 34px;box-shadow:0 -12px 36px rgba(0,0,0,0.22);">
        <div style="display:inline-flex;align-items:center;gap:6px;background:#DCFCE7;color:#15803D;padding:6px 14px;border-radius:999px;font-size:12px;font-weight:800;margin-bottom:12px;letter-spacing:0.3px;">
          📷 SMART SCANNER (1/3)
        </div>
        <div style="font-size:24px;font-weight:900;color:#0F172A;line-height:1.2;letter-spacing:-0.4px;margin-bottom:10px;">
          Camera Access & Crop Scanner
        </div>
        <div style="font-size:14px;color:#64748B;line-height:1.55;font-weight:600;margin-bottom:24px;">
          Allow camera access to instantly snap crop leaves, identify pest infestations, fungal blights, and receive precision dosage recommendations.
        </div>
        <button onclick="grantCameraPermission()" class="shiny-btn" style="width:100%;padding:16px;background:#16A34A;color:#FFFFFF;border:none;border-radius:18px;font-size:16px;font-weight:900;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:10px;box-shadow:0 8px 24px rgba(22,163,74,0.35);">
          Allow Camera Access →
        </button>`;

    const camPermNew = `<!-- Top Bar -->
      <div style="position:relative;z-index:10;display:flex;align-items:center;justify-content:space-between;padding:max(52px, env(safe-area-inset-top, 52px)) 20px 0;">
        <div style="background:rgba(30, 41, 59, 0.72);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);color:#FFFFFF;padding:7px 16px;border-radius:999px;font-size:13px;font-weight:700;display:flex;align-items:center;gap:6px;box-shadow:0 4px 12px rgba(0,0,0,0.18);">
          \${OB_TL('perm_badge_1')}
        </div>
        <button onclick="skipCameraPermission()" style="background:#FFFFFF;color:#16A34A;border:none;padding:7px 20px;border-radius:999px;font-size:13px;font-weight:800;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,0.18);">
          \${OB_TL('skip_btn')}
        </button>
      </div>

      <!-- Bottom Sheet Card -->
      <div style="position:relative;z-index:10;background:#FFFFFF;border-radius:32px 32px 0 0;padding:28px 24px 34px;box-shadow:0 -12px 36px rgba(0,0,0,0.22);">
        <div style="display:inline-flex;align-items:center;gap:6px;background:#DCFCE7;color:#15803D;padding:6px 14px;border-radius:999px;font-size:12px;font-weight:800;margin-bottom:12px;letter-spacing:0.3px;">
          \${OB_TL('perm_camera_tag')}
        </div>
        <div style="font-size:24px;font-weight:900;color:#0F172A;line-height:1.2;letter-spacing:-0.4px;margin-bottom:10px;">
          \${OB_TL('perm_camera_heading')}
        </div>
        <div style="font-size:14px;color:#64748B;line-height:1.55;font-weight:600;margin-bottom:24px;">
          \${OB_TL('perm_camera_desc')}
        </div>
        <button onclick="grantCameraPermission()" class="shiny-btn" style="width:100%;padding:16px;background:#16A34A;color:#FFFFFF;border:none;border-radius:18px;font-size:16px;font-weight:900;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:10px;box-shadow:0 8px 24px rgba(22,163,74,0.35);">
          \${OB_TL('perm_camera_btn')}
        </button>`;

    if (src.includes(camPermOld)) {
        src = src.replace(camPermOld, camPermNew);
    }

    const locPermOld = `<!-- Top Bar -->
      <div style="position:relative;z-index:10;display:flex;align-items:center;justify-content:space-between;padding:max(52px, env(safe-area-inset-top, 52px)) 20px 0;">
        <div style="background:rgba(30, 41, 59, 0.72);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);color:#FFFFFF;padding:7px 16px;border-radius:999px;font-size:13px;font-weight:700;display:flex;align-items:center;gap:6px;box-shadow:0 4px 12px rgba(0,0,0,0.18);">
          📍 Permissions (2/3)
        </div>
        <button onclick="skipLocationPermission()" style="background:#FFFFFF;color:#16A34A;border:none;padding:7px 20px;border-radius:999px;font-size:13px;font-weight:800;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,0.18);">
          Skip
        </button>
      </div>

      <!-- Bottom Sheet Card -->
      <div style="position:relative;z-index:10;background:#FFFFFF;border-radius:32px 32px 0 0;padding:28px 24px 34px;box-shadow:0 -12px 36px rgba(0,0,0,0.22);">
        <div style="display:inline-flex;align-items:center;gap:6px;background:#DCFCE7;color:#15803D;padding:6px 14px;border-radius:999px;font-size:12px;font-weight:800;margin-bottom:12px;letter-spacing:0.3px;">
          📍 HYPER-LOCAL MANDI (2/3)
        </div>
        <div style="font-size:24px;font-weight:900;color:#0F172A;line-height:1.2;letter-spacing:-0.4px;margin-bottom:10px;">
          GPS Location for Mandi Rates
        </div>
        <div style="font-size:14px;color:#64748B;line-height:1.55;font-weight:600;margin-bottom:24px;">
          Get hyper-local APMC Mandi daily arrival rates, crop logistics truck pairing, and accurate micro-climate rain advisories.
        </div>
        <button onclick="grantLocationPermission()" class="shiny-btn" style="width:100%;padding:16px;background:#16A34A;color:#FFFFFF;border:none;border-radius:18px;font-size:16px;font-weight:900;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:10px;box-shadow:0 8px 24px rgba(22,163,74,0.35);">
          Allow Location Access →
        </button>`;

    const locPermNew = `<!-- Top Bar -->
      <div style="position:relative;z-index:10;display:flex;align-items:center;justify-content:space-between;padding:max(52px, env(safe-area-inset-top, 52px)) 20px 0;">
        <div style="background:rgba(30, 41, 59, 0.72);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);color:#FFFFFF;padding:7px 16px;border-radius:999px;font-size:13px;font-weight:700;display:flex;align-items:center;gap:6px;box-shadow:0 4px 12px rgba(0,0,0,0.18);">
          \${OB_TL('perm_badge_2')}
        </div>
        <button onclick="skipLocationPermission()" style="background:#FFFFFF;color:#16A34A;border:none;padding:7px 20px;border-radius:999px;font-size:13px;font-weight:800;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,0.18);">
          \${OB_TL('skip_btn')}
        </button>
      </div>

      <!-- Bottom Sheet Card -->
      <div style="position:relative;z-index:10;background:#FFFFFF;border-radius:32px 32px 0 0;padding:28px 24px 34px;box-shadow:0 -12px 36px rgba(0,0,0,0.22);">
        <div style="display:inline-flex;align-items:center;gap:6px;background:#DCFCE7;color:#15803D;padding:6px 14px;border-radius:999px;font-size:12px;font-weight:800;margin-bottom:12px;letter-spacing:0.3px;">
          \${OB_TL('perm_location_tag')}
        </div>
        <div style="font-size:24px;font-weight:900;color:#0F172A;line-height:1.2;letter-spacing:-0.4px;margin-bottom:10px;">
          \${OB_TL('perm_location_heading')}
        </div>
        <div style="font-size:14px;color:#64748B;line-height:1.55;font-weight:600;margin-bottom:24px;">
          \${OB_TL('perm_location_desc')}
        </div>
        <button onclick="grantLocationPermission()" class="shiny-btn" style="width:100%;padding:16px;background:#16A34A;color:#FFFFFF;border:none;border-radius:18px;font-size:16px;font-weight:900;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:10px;box-shadow:0 8px 24px rgba(22,163,74,0.35);">
          \${OB_TL('perm_location_btn')}
        </button>`;

    if (src.includes(locPermOld)) {
        src = src.replace(locPermOld, locPermNew);
    }

    const notifPermOld = `<!-- Top Bar -->
      <div style="position:relative;z-index:10;display:flex;align-items:center;justify-content:space-between;padding:max(52px, env(safe-area-inset-top, 52px)) 20px 0;">
        <div style="background:rgba(30, 41, 59, 0.72);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);color:#FFFFFF;padding:7px 16px;border-radius:999px;font-size:13px;font-weight:700;display:flex;align-items:center;gap:6px;box-shadow:0 4px 12px rgba(0,0,0,0.18);">
          🔔 Permissions (3/3)
        </div>
        <button onclick="skipNotificationPermission()" style="background:#FFFFFF;color:#16A34A;border:none;padding:7px 20px;border-radius:999px;font-size:13px;font-weight:800;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,0.18);">
          Skip
        </button>
      </div>

      <!-- Bottom Sheet Card -->
      <div style="position:relative;z-index:10;background:#FFFFFF;border-radius:32px 32px 0 0;padding:28px 24px 34px;box-shadow:0 -12px 36px rgba(0,0,0,0.22);">
        <div style="display:inline-flex;align-items:center;gap:6px;background:#DCFCE7;color:#15803D;padding:6px 14px;border-radius:999px;font-size:12px;font-weight:800;margin-bottom:12px;letter-spacing:0.3px;">
          🔔 REAL-TIME PEST ALERTS (3/3)
        </div>
        <div style="font-size:24px;font-weight:900;color:#0F172A;line-height:1.2;letter-spacing:-0.4px;margin-bottom:10px;">
          Instant Crop Disease Warnings
        </div>
        <div style="font-size:14px;color:#64748B;line-height:1.55;font-weight:600;margin-bottom:24px;">
          Stay alerted on sudden pest outbreaks in your mandal, best pesticide spray timing windows, and surge mandi price jumps.
        </div>
        <button onclick="grantNotificationPermission()" class="shiny-btn" style="width:100%;padding:16px;background:#16A34A;color:#FFFFFF;border:none;border-radius:18px;font-size:16px;font-weight:900;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:10px;box-shadow:0 8px 24px rgba(22,163,74,0.35);">
          Enable Smart Notifications →
        </button>`;

    const notifPermNew = `<!-- Top Bar -->
      <div style="position:relative;z-index:10;display:flex;align-items:center;justify-content:space-between;padding:max(52px, env(safe-area-inset-top, 52px)) 20px 0;">
        <div style="background:rgba(30, 41, 59, 0.72);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);color:#FFFFFF;padding:7px 16px;border-radius:999px;font-size:13px;font-weight:700;display:flex;align-items:center;gap:6px;box-shadow:0 4px 12px rgba(0,0,0,0.18);">
          \${OB_TL('perm_badge_3')}
        </div>
        <button onclick="skipNotificationPermission()" style="background:#FFFFFF;color:#16A34A;border:none;padding:7px 20px;border-radius:999px;font-size:13px;font-weight:800;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,0.18);">
          \${OB_TL('skip_btn')}
        </button>
      </div>

      <!-- Bottom Sheet Card -->
      <div style="position:relative;z-index:10;background:#FFFFFF;border-radius:32px 32px 0 0;padding:28px 24px 34px;box-shadow:0 -12px 36px rgba(0,0,0,0.22);">
        <div style="display:inline-flex;align-items:center;gap:6px;background:#DCFCE7;color:#15803D;padding:6px 14px;border-radius:999px;font-size:12px;font-weight:800;margin-bottom:12px;letter-spacing:0.3px;">
          \${OB_TL('perm_notif_tag')}
        </div>
        <div style="font-size:24px;font-weight:900;color:#0F172A;line-height:1.2;letter-spacing:-0.4px;margin-bottom:10px;">
          \${OB_TL('perm_notif_heading')}
        </div>
        <div style="font-size:14px;color:#64748B;line-height:1.55;font-weight:600;margin-bottom:24px;">
          \${OB_TL('perm_notif_desc')}
        </div>
        <button onclick="grantNotificationPermission()" class="shiny-btn" style="width:100%;padding:16px;background:#16A34A;color:#FFFFFF;border:none;border-radius:18px;font-size:16px;font-weight:900;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:10px;box-shadow:0 8px 24px rgba(22,163,74,0.35);">
          \${OB_TL('perm_notif_btn')}
        </button>`;

    if (src.includes(notifPermOld)) {
        src = src.replace(notifPermOld, notifPermNew);
    }

    // 4. Update Crop Selection Bottom Bar
    const cropNextOld = `\${OB_TL('crops_next_btn') || 'Next'} (\${plantixFlowState.selectedCrops.length})`;
    const cropNextNew = `\${OB_TL('crops_next_btn')} (\${plantixFlowState.selectedCrops.length})`;
    src = src.replace(cropNextOld, cropNextNew);

    // 5. Farmer Profile Localization & Clean Logout Button
    const profLandOld = `['2.5','Land (Ac)','#86EFAC'],['850','Soil Health','#FFFFFF'],['A+','Grade','#FFFFFF']`;
    const profLandNew = `[
      ['2.5', TL('Land (Ac)', 'భూమి (ఎకరాలు)', 'जमीन (एकड़)'), '#86EFAC'],
      ['850', TL('Soil Health', 'నేల ఆరోగ్యం', 'मृदा स्वास्थ्य'), '#FFFFFF'],
      ['A+', TL('Grade', 'గ్రేడ్', 'ग्रेड'), '#FFFFFF']
    ]`;
    src = src.replace(profLandOld, profLandNew);

    const profMenuOld = `['M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2M9 5a2 2 0 0 0 2 2h2a2 2 0 0 0 2-2M9 5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2','AgriStack Identity','TS-WGL-8941 · Verified', 'openAgriStackModal()'],
            ['M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z','KCC Loan Status','Sanctioned: ₹1.25L', 'openKccLoanModal()'],
            ['M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z|M9 22V12h6v10','Farm Documents','RoR, Pattadar Passbook', 'openFarmDocsModal()'],
            ['M3 3v18h18|M18 17V9|M13 17V5|M8 17v-3','Settings','App preferences', 'openLanguageSelectorModal()'],
            ['M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0zm-5 0a4 4 0 1 1-8 0 4 4 0 0 1 8 0z','Help & Support','24/7 agriculture helpline', 'openSupportModal()']`;

    const profMenuNew = `[
            ['M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2M9 5a2 2 0 0 0 2 2h2a2 2 0 0 0 2-2M9 5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2', TL('AgriStack Identity', 'అగ్రిస్టాక్ గుర్తింపు', 'एग्रीस्टैक पहचान'), TL('TS-WGL-8941 · Verified', 'TS-WGL-8941 · ధృవీకరించబడింది', 'TS-WGL-8941 · सत्यापित'), 'openAgriStackModal()'],
            ['M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z', TL('KCC Loan Status', 'KCC రుణ స్థితి', 'KCC ऋण स्थिति'), TL('Sanctioned: ₹1.25L', 'మంజూరైనది: ₹1.25L', 'स्वीकृत: ₹1.25L'), 'openKccLoanModal()'],
            ['M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z|M9 22V12h6v10', TL('Farm Documents', 'పొలం పత్రాలు', 'कृषि दस्तावेज़'), TL('RoR, Pattadar Passbook', 'పట్టాదారు పాస్‌బుక్, RoR', 'पट्टा पासबुक, खतौनी'), 'openFarmDocsModal()'],
            ['M3 3v18h18|M18 17V9|M13 17V5|M8 17v-3', TL('Settings', 'సెట్టింగ్స్', 'सेटिंग्स'), TL('App preferences', 'యాప్ ప్రాధాన్యతలు', 'ऐप सेटिंग्स'), 'openLanguageSelectorModal()'],
            ['M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0zm-5 0a4 4 0 1 1-8 0 4 4 0 0 1 8 0z', TL('Help & Support', 'సహాయం & మద్దతు', 'सहायता व संपर्क'), TL('24/7 agriculture helpline', '24/7 వ్యవసాయ హెల్ప్‌లైన్', '24/7 कृषि हेल्पलाइन'), 'openSupportModal()']
          ]`;

    if (src.includes(profMenuOld)) {
        src = src.replace(profMenuOld, profMenuNew);
    }

    const farmerLogoutOld = `Log Out / నిష్క్రమించు`;
    const farmerLogoutNew = `\${TL('Log Out', 'లాగ్ అవుట్', 'लॉग आउट')}`;
    src = src.replaceAll(farmerLogoutOld, farmerLogoutNew);

    const driverLogoutOld = `Driver Log Out / లాగ్ అవుట్`;
    const driverLogoutNew = `\${TL('Driver Log Out', 'డ్రైవర్ లాగ్ అవుట్', 'ड्राइवर लॉग आउट')}`;
    src = src.replaceAll(driverLogoutOld, driverLogoutNew);

    // 6. GramHaul Screen Single-Language Labels
    const ghBadgeOld = `<span style="font-size:13.5px;font-weight:900;color:#16A34A;">GramHaul Mandi Dispatch</span>`;
    const ghBadgeNew = `<span style="font-size:13.5px;font-weight:900;color:#16A34A;">\${TL('GramHaul Mandi Dispatch', 'గ్రామ్‌హాల్ మండి రవాణా', 'ग्रामहॉल मंडी परिवहन')}</span>`;
    src = src.replace(ghBadgeOld, ghBadgeNew);

    const ghGeofenceOld = `10 KM Proximity Geofenced`;
    const ghGeofenceNew = `\${TL('10 KM Proximity Geofenced', '10 కి.మీ పరిధిలో వాహనాలు', '10 किमी दायरे में वाहन')}`;
    src = src.replace(ghGeofenceOld, ghGeofenceNew);

    const ghFromOld = `<span style="font-size:11px;font-weight:800;color:#64748B;letter-spacing:0.4px;">FROM (PICKUP FARM)</span>`;
    const ghFromNew = `<span style="font-size:11px;font-weight:800;color:#64748B;letter-spacing:0.4px;">\${TL('FROM (PICKUP FARM)', 'పికప్ లొకేషన్ (పొలం)', 'पिकअप स्थान (खेत)')}</span>`;
    src = src.replace(ghFromOld, ghFromNew);

    const ghToOld = `<span style="font-size:11px;font-weight:800;color:#64748B;letter-spacing:0.4px;">TO (APMC MANDI)</span>`;
    const ghToNew = `<span style="font-size:11px;font-weight:800;color:#64748B;letter-spacing:0.4px;">\${TL('TO (APMC MANDI)', 'డ్రాప్ లొకేషన్ (మండి)', 'ड्रॉप स्थान (मंडी)')}</span>`;
    src = src.replace(ghToOld, ghToNew);

    const ghCropOld = `🌱 CROP COMMODITY`;
    const ghCropNew = `🌱 \${TL('CROP COMMODITY', 'పంట రకం', 'फसल का प्रकार')}`;
    src = src.replace(ghCropOld, ghCropNew);

    const ghLoadOld = `📦 LOAD BAGS / SACKS`;
    const ghLoadNew = `📦 \${TL('LOAD BAGS / SACKS', 'బస్తాల సంఖ్య / లోడ్', 'बोरियों की संख्या / वजन')}`;
    src = src.replace(ghLoadOld, ghLoadNew);

    const ghTruckHdrOld = `🚚 CHOOSE COMMERCIAL TRUCK TYPE`;
    const ghTruckHdrNew = `🚚 \${TL('CHOOSE COMMERCIAL TRUCK TYPE', 'రవాణా వాహనాన్ని ఎంచుకోండి', 'व्यावसायिक वाहन चुनें')}`;
    src = src.replace(ghTruckHdrOld, ghTruckHdrNew);

    const aceTitleOld = `Tata Ace Gold (1.5 Ton)`;
    const aceTitleNew = `\${TL('Tata Ace Gold (1.5 Ton)', 'టాటా ఏస్ గోల్డ్ (1.5 టన్నులు)', 'टाटा ऐस गोल्ड (1.5 टन)')}`;
    src = src.replace(aceTitleOld, aceTitleNew);

    const aceSubOld = `Up to 25 Qtl · 50 Sacks · Most Popular`;
    const aceSubNew = `\${TL('Up to 25 Qtl · 50 Sacks · Most Popular', '25 క్విం. వరకు · 50 బస్తాలు · సిద్ధంగా ఉంది', '25 क्विंटल तक · 50 बोरियां · सबसे लोकप्रिय')}`;
    src = src.replace(aceSubOld, aceSubNew);

    const aceReadyOld = `✓ Ready`;
    const aceReadyNew = `\${TL('✓ Ready', '✓ సిద్ధం', '✓ तैयार')}`;
    src = src.replace(aceReadyOld, aceReadyNew);

    const boleroTitleOld = `Mahindra Bolero Maxi (2.5 Ton)`;
    const boleroTitleNew = `\${TL('Mahindra Bolero Maxi (2.5 Ton)', 'మహీంద్రా బొలెరో మ్యాక్సీ (2.5 టన్నులు)', 'महिंद्रा बोलेरो मैक्सी (2.5 टन)')}`;
    src = src.replace(boleroTitleOld, boleroTitleNew);

    const boleroSubOld = `Up to 50 Qtl · 100 Sacks · Heavy Produce`;
    const boleroSubNew = `\${TL('Up to 50 Qtl · 100 Sacks · Heavy Produce', '50 క్విం. వరకు · 100 బస్తాలు · భారీ లోడ్', '50 क्विंटल तक · 100 बोरियां · भारी उपज')}`;
    src = src.replace(boleroSubOld, boleroSubNew);

    const boleroAvailOld = `Available`;
    const boleroAvailNew = `\${TL('Available', 'అందుబాటులో ఉంది', 'उपलब्ध')}`;
    src = src.replace(boleroAvailOld, boleroAvailNew);

    const eicherTitleOld = `Eicher Pro 14ft (5.0 Ton)`;
    const eicherTitleNew = `\${TL('Eicher Pro 14ft (5.0 Ton)', 'ఐషర్ ప్రో 14ft (5.0 టన్నులు)', 'आयशर प्रो 14ft (5.0 टन)')}`;
    src = src.replace(eicherTitleOld, eicherTitleNew);

    const eicherSubOld = `Up to 100 Qtl · 200 Sacks · Bulk Mandi Load`;
    const eicherSubNew = `\${TL('Up to 100 Qtl · 200 Sacks · Bulk Mandi Load', '100 క్విం. వరకు · 200 బస్తాలు · బల్క్ లోడ్', '100 क्विंटल तक · 200 बोरियां · बल्क मंडी लोड')}`;
    src = src.replace(eicherSubOld, eicherSubNew);

    const eicherPoolOld = `Bulk Pool`;
    const eicherPoolNew = `\${TL('Bulk Pool', 'బల్క్ పూల్', 'बल्क पूल')}`;
    src = src.replace(eicherPoolOld, eicherPoolNew);

    // 7. GramHaul Dispatch Broadcast Modal Pure Localization
    const modalDispatchOld = `function renderLiveDispatchedModal(bookId, truckName, crop, sacks, fare, mandiName) {
  const modalId = 'gh-dispatched-modal';
  let modal = document.getElementById(modalId);
  if (modal) modal.remove();

  modal = document.createElement('div');
  modal.id = modalId;
  modal.style.cssText = 'position:fixed;inset:0;background:rgba(15,23,42,0.7);backdrop-filter:blur(6px);z-index:99999;display:flex;align-items:flex-end;justify-content:center;animation:fadeIn 0.2s;';
  modal.innerHTML = \`
    <div style="background:#FFFFFF;width:100%;max-width:430px;border-radius:28px 28px 0 0;padding:24px 20px 32px;box-shadow:0 -10px 40px rgba(0,0,0,0.25);animation:slideUp 0.25s ease;">
      <div style="width:36px;height:4px;background:#E2E8F0;border-radius:10px;margin:0 auto 16px;"></div>
      
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
        <div style="width:48px;height:48px;border-radius:16px;background:#DCFCE7;display:flex;align-items:center;justify-content:center;font-size:24px;">⚡</div>
        <div>
          <div style="font-size:18px;font-weight:900;color:#0F172A;">Dispatch Broadcast Sent!</div>
          <div style="font-size:12px;color:#16A34A;font-weight:800;">Booking ID: #\${bookId} · 10 KM Radius</div>
        </div>
      </div>

      <div style="background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:16px;padding:14px;margin-bottom:16px;display:flex;flex-direction:column;gap:8px;font-size:12.5px;">
        <div style="display:flex;justify-content:space-between;"><span style="color:#64748B;">Truck Category:</span><strong style="color:#0F172A;">\${truckName}</strong></div>
        <div style="display:flex;justify-content:space-between;"><span style="color:#64748B;">Produce Load:</span><strong style="color:#0F172A;">\${crop} (\${sacks} Sacks)</strong></div>
        <div style="display:flex;justify-content:space-between;"><span style="color:#64748B;">Destination:</span><strong style="color:#0F172A;">\${mandiName}</strong></div>
        <div style="display:flex;justify-content:space-between;padding-top:8px;border-top:1px solid #E2E8F0;"><span style="color:#64748B;font-weight:700;">Agreed Freight Fare:</span><strong style="color:#15803D;font-size:16px;">₹\${fare}</strong></div>
      </div>

      <div style="background:#FEF3C7;border:1px solid #FDE68A;border-radius:12px;padding:10px 14px;margin-bottom:18px;font-size:11.5px;color:#92400E;font-weight:700;display:flex;align-items:center;gap:8px;">
        <span>📡</span>
        <span>Drivers within 10 km will receive this haul request instantly on their cockpit app.</span>
      </div>

      <div style="display:flex;gap:10px;">
        <button onclick="document.getElementById('gh-dispatched-modal').remove()" style="flex:1;padding:14px;background:#F1F5F9;color:#475569;border:none;border-radius:14px;font-size:14px;font-weight:800;cursor:pointer;">
          Close
        </button>
        <button onclick="document.getElementById('gh-dispatched-modal').remove();authUserRole='driver';localStorage.setItem('nukrop_user_role','driver');openScreen('driver_dashboard',null);updateBottomDockForRole();" style="flex:1.4;padding:14px;background:#16A34A;color:#FFFFFF;border:none;border-radius:14px;font-size:14px;font-weight:900;cursor:pointer;box-shadow:0 4px 14px rgba(22,163,74,0.3);">
          View Driver Side →
        </button>
      </div>
    </div>
  \`;
  document.body.appendChild(modal);
}`;

    const modalDispatchNew = `function renderLiveDispatchedModal(bookId, truckName, crop, sacks, fare, mandiName) {
  const modalId = 'gh-dispatched-modal';
  let modal = document.getElementById(modalId);
  if (modal) modal.remove();

  modal = document.createElement('div');
  modal.id = modalId;
  modal.style.cssText = 'position:fixed;inset:0;background:rgba(15,23,42,0.7);backdrop-filter:blur(6px);z-index:99999;display:flex;align-items:flex-end;justify-content:center;animation:fadeIn 0.2s;';
  modal.innerHTML = \`
    <div style="background:#FFFFFF;width:100%;max-width:430px;border-radius:28px 28px 0 0;padding:24px 20px 32px;box-shadow:0 -10px 40px rgba(0,0,0,0.25);animation:slideUp 0.25s ease;">
      <div style="width:36px;height:4px;background:#E2E8F0;border-radius:10px;margin:0 auto 16px;"></div>
      
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
        <div style="width:48px;height:48px;border-radius:16px;background:#DCFCE7;display:flex;align-items:center;justify-content:center;font-size:24px;">⚡</div>
        <div>
          <div style="font-size:18px;font-weight:900;color:#0F172A;">\${TL('Dispatch Broadcast Sent!', 'రవాణా అభ్యర్థన పంపబడింది!', 'परिवहन अनुरोध भेजा गया!')}</div>
          <div style="font-size:12px;color:#16A34A;font-weight:800;">\${TL('Booking ID', 'బుకింగ్ ID', 'बुकिंग आईडी')}: #\${bookId} · 10 KM</div>
        </div>
      </div>

      <div style="background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:16px;padding:14px;margin-bottom:16px;display:flex;flex-direction:column;gap:8px;font-size:12.5px;">
        <div style="display:flex;justify-content:space-between;"><span style="color:#64748B;">\${TL('Truck Category:', 'వాహనం రకం:', 'वाहन प्रकार:')}</span><strong style="color:#0F172A;">\${truckName}</strong></div>
        <div style="display:flex;justify-content:space-between;"><span style="color:#64748B;">\${TL('Produce Load:', 'పంట లోడ్:', 'फसल भार:')}</span><strong style="color:#0F172A;">\${crop} (\${sacks} \${TL('Sacks', 'బస్తాలు', 'बोरियां')})</strong></div>
        <div style="display:flex;justify-content:space-between;"><span style="color:#64748B;">\${TL('Destination:', 'గమ్యస్థానం:', 'गंतव्य:')}</span><strong style="color:#0F172A;">\${mandiName}</strong></div>
        <div style="display:flex;justify-content:space-between;padding-top:8px;border-top:1px solid #E2E8F0;"><span style="color:#64748B;font-weight:700;">\${TL('Agreed Freight Fare:', 'ఖరారైన ఛార్జీ:', 'तय भाड़ा:')}</span><strong style="color:#15803D;font-size:16px;">₹\${fare}</strong></div>
      </div>

      <div style="background:#FEF3C7;border:1px solid #FDE68A;border-radius:12px;padding:10px 14px;margin-bottom:18px;font-size:11.5px;color:#92400E;font-weight:700;display:flex;align-items:center;gap:8px;">
        <span>📡</span>
        <span>\${TL('Drivers within 10 km will receive this haul request instantly on their cockpit app.', '10 కి.మీ పరిధిలోని డ్రైవర్లకు మీ అభ్యర్థన చేరింది.', '10 किमी के दायरे में ड्राइवरों को आपका अनुरोध भेज दिया गया है।')}</span>
      </div>

      <div style="display:flex;gap:10px;">
        <button onclick="document.getElementById('gh-dispatched-modal').remove()" style="flex:1;padding:14px;background:#F1F5F9;color:#475569;border:none;border-radius:14px;font-size:14px;font-weight:800;cursor:pointer;">
          \${TL('Close', 'మూసివేయి', 'बंद करें')}
        </button>
        <button onclick="document.getElementById('gh-dispatched-modal').remove();authUserRole='driver';localStorage.setItem('nukrop_user_role','driver');openScreen('driver_dashboard',null);updateBottomDockForRole();" style="flex:1.4;padding:14px;background:#16A34A;color:#FFFFFF;border:none;border-radius:14px;font-size:14px;font-weight:900;cursor:pointer;box-shadow:0 4px 14px rgba(22,163,74,0.3);">
          \${TL('View Driver Side →', 'డ్రైవర్ వీక్షణ చూడండి →', 'ड्राइवर स्क्रीन देखें →')}
        </button>
      </div>
    </div>
  \`;
  document.body.appendChild(modal);
}`;

    if (src.includes(modalDispatchOld)) {
        src = src.replace(modalDispatchOld, modalDispatchNew);
    }

    // 8. Driver Cockpit Map & Orders Single Language
    const stepperOld = `\${['En Route','Arrived','Loaded','Delivered'].map((step,i)=>`;
    const stepperNew = `\${[
      TL('En Route', 'మార్గంలో ఉంది', 'रास्ते में'),
      TL('Arrived', 'చేరుకుంది', 'पहुंचा'),
      TL('Loaded', 'లోడ్ అయింది', 'लोड हुआ'),
      TL('Delivered', 'డెలివరీ అయింది', 'वितरित')
    ].map((step,i)=>`;
    src = src.replace(stepperOld, stepperNew);

    const todayHdrOld = `<div style="font-size:10px;color:#9CA3AF;font-weight:700;text-align:center;">TODAY</div>`;
    const todayHdrNew = `<div style="font-size:10px;color:#9CA3AF;font-weight:700;text-align:center;">\${TL('TODAY', 'నేటి ఆదాయం', 'आज')}</div>`;
    src = src.replace(todayHdrOld, todayHdrNew);

    const agreedHdrOld = `Agreed Haul Fare`;
    const agreedHdrNew = `\${TL('Agreed Haul Fare', 'ఖరారైన రవాణా ఛార్జీ', 'तय भाड़ा')}`;
    src = src.replace(agreedHdrOld, agreedHdrNew);

    const verifiedOld = `★ 4.9 · Verified Farmer`;
    const verifiedNew = `★ 4.9 · \${TL('Verified Farmer', 'ధృవీకరించబడిన రైతు', 'सत्यापित किसान')}`;
    src = src.replace(verifiedOld, verifiedNew);

    const pickupHdrOld = `PICKUP (GPS)`;
    const pickupHdrNew = `\${TL('PICKUP (GPS)', 'పికప్ లొకేషన్ (పొలం)', 'पिकअप स्थान')}`;
    src = src.replace(pickupHdrOld, pickupHdrNew);

    const dropHdrOld = `DROP MANDI`;
    const dropHdrNew = `\${TL('DROP MANDI', 'డ్రాప్ లొకేషన్ (మండి)', 'ड्रॉप स्थान')}`;
    src = src.replace(dropHdrOld, dropHdrNew);

    const zeroFeeOld = `✓ Zero Platform Fee`;
    const zeroFeeNew = `✓ \${TL('Zero Platform Fee', 'సున్నా ప్లాట్‌ఫారమ్ రుసుము', 'शून्य प्लेटफ़ॉर्म शुल्क')}`;
    src = src.replace(zeroFeeOld, zeroFeeNew);

    const callFarmerOld = `Call Farmer`;
    const callFarmerNew = `\${TL('Call Farmer', 'రైతుకు కాల్', 'कॉल करें')}`;
    src = src.replace(callFarmerOld, callFarmerNew);

    const liveChatOld = `Live Chat`;
    const liveChatNew = `\${TL('Live Chat', 'లైవ్ చాట్', 'लाइव चैट')}`;
    src = src.replace(liveChatOld, liveChatNew);

    const navBtnOld = `Navigate`;
    const navBtnNew = `\${TL('Navigate', 'రూట్ మ్యాప్', 'नेविगेट')}`;
    src = src.replace(navBtnOld, navBtnNew);

    const markCompOld = `Mark Haul Completed & Collect ₹`;
    const markCompNew = `\${TL('Mark Haul Completed & Collect', 'రవాణా పూర్తి చేయండి & స్వీకరించండి', 'ट्रिप पूरी करें और प्राप्त करें')} ₹`;
    src = src.replace(markCompOld, markCompNew);

    // 9. Driver Profile Menu Localization
    const driverMenuOld = `[
            ['M12 8v4l3 3m6-3a9 9 0 1 1-18 0 9 9 0 0 1 18 0z','Haul History','All past trips & receipts', 'openDriverHaulHistoryModal()'],
            ['M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z','Insurance & FASTag','TS 03 UB 4491 · Active till Dec 2025', 'openDriverInsuranceFastagModal()'],
            ['M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 0-2-2z|M9 22V12h6v10','Vehicle Documents','RC, Permit, Fitness, PUC', 'openDriverVehicleDocsModal()'],
            ['M3 3v18h18|M18 17V9|M13 17V5|M8 17v-3','Settings','App preferences', 'openLanguageSelectorModal()'],
            ['M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0zm-5 0a4 4 0 1 1-8 0 4 4 0 0 1 8 0z','Help & Support','24/7 driver helpline', 'openSupportModal()'],
          ]`;

    const driverMenuNew = `[
            ['M12 8v4l3 3m6-3a9 9 0 1 1-18 0 9 9 0 0 1 18 0z', TL('Haul History', 'రవాణా చరిత్ర', 'ट्रिप इतिहास'), TL('All past trips & receipts', 'గత ట్రిప్పులు & రశీదులు', 'सभी पिछली ट्रिप्स व रसीदें'), 'openDriverHaulHistoryModal()'],
            ['M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z', TL('Insurance & FASTag', 'ఇన్సూరెన్స్ & ఫాస్టాగ్', 'बीमा व फास्टैग'), TL('TS 03 UB 4491 · Active till Dec 2026', 'TS 03 UB 4491 · డిసెంబర్ 2026 వరకు చెల్లుబాటు', 'TS 03 UB 4491 · वैध'), 'openDriverInsuranceFastagModal()'],
            ['M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 0-2-2z|M9 22V12h6v10', TL('Vehicle Documents', 'వాహన పత్రాలు', 'वाहन दस्तावेज़'), TL('RC, Permit, Fitness, PUC', 'RC, పర్మిట్, ఫిట్‌నెస్, PUC', 'आरसी, परमिट, फिटनेस'), 'openDriverVehicleDocsModal()'],
            ['M3 3v18h18|M18 17V9|M13 17V5|M8 17v-3', TL('Settings', 'సెట్టింగ్స్', 'सेटिंग्स'), TL('App preferences', 'యాప్ ప్రాధాన్యతలు', 'ऐप सेटिंग्स'), 'openLanguageSelectorModal()'],
            ['M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0zm-5 0a4 4 0 1 1-8 0 4 4 0 0 1 8 0z', TL('Help & Support', 'సహాయం & మద్దతు', 'सहायता व संपर्क'), TL('24/7 driver helpline', '24/7 డ్రైవర్ హెల్ప్‌లైన్', '24/7 हेल्पलाइन'), 'openSupportModal()'],
          ]`;

    if (src.includes(driverMenuOld)) {
        src = src.replace(driverMenuOld, driverMenuNew);
    }

    // Driver stats rating/hauls/acceptance
    const driverStatsOld = `['4.9','Rating'],['420','Hauls'],['98%','Acceptance']`;
    const driverStatsNew = `[
      ['4.9', TL('Rating', 'రేటింగ్', 'रेटिंग')],
      ['420', TL('Hauls', 'ట్రిప్పులు', 'ट्रिप्स')],
      ['98%', TL('Acceptance', 'అంగీకారం', 'स्वीकृति')]
    ]`;
    src = src.replace(driverStatsOld, driverStatsNew);

    // 10. Driver Bottom Navigation Tab Labels & Duty Toggle
    const driverTabsOld = `{key:'map',label:'Map',svg:'<polygon points=\"3 11 22 2 13 21 11 13 3 11\"/>'},
          {key:'earnings',label:'Earnings',svg:'<line x1=\"12\" y1=\"1\" x2=\"12\" y2=\"23\"/><path d=\"M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6\"/>'},
          {key:'profile',label:'Profile',svg:'<path d=\"M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2\"/><circle cx=\"12\" cy=\"7\" r=\"4\"/>'},`;

    const driverTabsNew = `{key:'map',label:TL('Map', 'మ్యాప్', 'नक्शा'),svg:'<polygon points=\"3 11 22 2 13 21 11 13 3 11\"/>'},
          {key:'earnings',label:TL('Earnings', 'ఆదాయం', 'कमाई'),svg:'<line x1=\"12\" y1=\"1\" x2=\"12\" y2=\"23\"/><path d=\"M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6\"/>'},
          {key:'profile',label:TL('Profile', 'ప్రొఫైల్', 'प्रोफ़ाइल'),svg:'<path d=\"M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2\"/><circle cx=\"12\" cy=\"7\" r=\"4\"/>'},`;

    if (src.includes(driverTabsOld)) {
        src = src.replace(driverTabsOld, driverTabsNew);
    }

    const dutyTextOld = `\${isOnline ? 'On Duty' : 'Go Online'}`;
    const dutyTextNew = `\${isOnline ? TL('On Duty', 'డ్యూటీలో ఉన్నారు', 'ड्यूटी पर हैं') : TL('Go Online', 'ఆన్‌లైన్ వెళ్లండి', 'ऑनलाइन जाएं')}`;
    src = src.replace(dutyTextOld, dutyTextNew);

    fs.writeFileSync(filePath, src, 'utf8');
    console.log('[OK] Applied Single-Language Purity to:', filePath);
}

applySingleLanguagePurity('app/src/main/assets/index.html');
applySingleLanguagePurity('nukrop_emulator.html');
