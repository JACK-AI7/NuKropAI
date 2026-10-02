const fs = require('fs');

function cleanAndLocalizeAll(filePath) {
    let src = fs.readFileSync(filePath, 'utf8');

    // 1. Precise replacement of getLocalizedCropName
    const cropFnOldStart = 'function getLocalizedCropName(';
    const cropFnOldEnd = '/* ═════════════════ 🇮🇳 PAN-INDIAN';
    const c1 = src.indexOf(cropFnOldStart);
    const c2 = src.indexOf(cropFnOldEnd, c1);
    
    if (c1 !== -1 && c2 !== -1) {
        const replacementCropFn = `function getLocalizedCropName(slugOrKey) {
  if (!slugOrKey) return 'Crop';
  const lang = (typeof currentLang !== 'undefined' ? currentLang : 'te') || 'te';

  // 1. Direct match in MASTER_120_CROPS
  if (typeof MASTER_120_CROPS !== 'undefined') {
    const found = MASTER_120_CROPS.find(c => c.key === slugOrKey || c.slug === slugOrKey);
    if (found && found.name) {
      const m = found.name.match(/^(.*?)\\s*\\(\\s*(.*?)\\s*\\/\\s*(.*?)\\s*\\)$/);
      if (m) {
        if (lang === 'te') return m[2].trim();
        if (lang === 'hi') return m[3].trim();
        if (lang === 'en') return m[1].trim();
      }
      return found.name.split(' (')[0];
    }
  }

  // 2. Direct match in CROP_TRANSLATIONS
  const aliasMap = {
    'chilli': 'birds-eye-chili', 'chili': 'birds-eye-chili',
    'paddy': 'rice', 'maize': 'corn', 'groundnut': 'peanut',
    'brinjal': 'eggplant', 'apple': 'generic-apple',
    'banana': 'plantain', 'cabbage': 'green-cabbage',
    'coriander': 'cilantro', 'potato': 'russet-potato',
    'capsicum': 'green-bell-pepper', 'millet': 'sorghum-millet'
  };
  const key = aliasMap[slugOrKey] || slugOrKey;
  if (typeof CROP_TRANSLATIONS !== 'undefined') {
    if (CROP_TRANSLATIONS[key] && CROP_TRANSLATIONS[key][lang]) {
      const val = CROP_TRANSLATIONS[key][lang];
      if (val && !val.includes('/')) return val;
      if (val && val.includes('/')) return val.split('/')[0].trim();
    }
    if (CROP_TRANSLATIONS[slugOrKey] && CROP_TRANSLATIONS[slugOrKey][lang]) {
      const val = CROP_TRANSLATIONS[slugOrKey][lang];
      if (val && !val.includes('/')) return val;
      if (val && val.includes('/')) return val.split('/')[0].trim();
    }
  }

  return slugOrKey.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
}

`;
        src = src.substring(0, c1) + replacementCropFn + src.substring(c2);
        console.log('Replaced getLocalizedCropName in:', filePath);
    }

    // 2. Update ONBOARDING_I18N with complete keys
    const obI18nKeys = {
      "perm_badge_1": { "en": "🔒 Permissions (1/3)", "te": "🔒 అనుమతులు (1/3)", "hi": "🔒 अनुमतियाँ (1/3)" },
      "perm_badge_2": { "en": "📍 Permissions (2/3)", "te": "📍 అనుమతులు (2/3)", "hi": "📍 अनुमतियाँ (2/3)" },
      "perm_badge_3": { "en": "🔔 Permissions (3/3)", "te": "🔔 అనుమతులు (3/3)", "hi": "🔔 अनुमतियाँ (3/3)" },
      "skip_btn": { "en": "Skip", "te": "దాటవేయి", "hi": "छोड़ें" },
      "perm_camera_tag": { "en": "📷 SMART SCANNER (1/3)", "te": "📷 AI పంట స్కానర్ (1/3)", "hi": "📷 AI फसल स्कैनर (1/3)" },
      "perm_camera_heading": { "en": "Camera Access & Crop Scanner", "te": "కెమెరా అనుమతి & పంట స్కానర్", "hi": "कैमरा अनुमति व फसल स्कैनर" },
      "perm_camera_desc": { "en": "Allow camera access to instantly snap crop leaves, identify pest infestations, fungal blights, and receive precision dosage recommendations.", "te": "ఆకు ఫోటో తీసి తెగుళ్లు, పురుగులు, పోషక లోపాలను తక్షణమే గుర్తించి సరైన మందుల మోతాదు పొందడానికి కెమెరా అనుమతించండి.", "hi": "पत्तियों की फोटो खींचकर रोग, कीट और पोषण की कमी पहचानने हेतु कैमरा अनुमति दें।" },
      "perm_camera_btn": { "en": "Allow Camera Access →", "te": "కెమెరా అనుమతించండి →", "hi": "कैमरा अनुमति दें →" },
      "perm_location_tag": { "en": "📍 MANDI & WEATHER (2/3)", "te": "📍 మండి & వాతావరణం (2/3)", "hi": "📍 मंडी व मौसम (2/3)" },
      "perm_location_heading": { "en": "GPS Location for Mandi Rates", "te": "స్థానిక మార్కెట్ ధరల కోసం GPS లొకేషన్", "hi": "स्थानीय मंडी भाव हेतु GPS लोकेशन" },
      "perm_location_desc": { "en": "Get hyper-local APMC Mandi daily arrival rates, crop logistics truck pairing, and accurate micro-climate rain advisories.", "te": "మీ ప్రాంత సమీప APMC మార్కెట్ ధరలు, గ్రామ్‌హాల్ రవాణా మరియు వర్ష సూచనల కోసం లొకేషన్ అనుమతించండి.", "hi": "नजदीकी APMC मंडी के ताज़ा भाव, वाहन बुकिंग और सटीक मौसम पूर्वानुमान हेतु लोकेशन अनुमति दें।" },
      "perm_location_btn": { "en": "Allow Location Access →", "te": "లొకేషన్ అనుమతించండి →", "hi": "लोकेशन अनुमति दें →" },
      "perm_notif_tag": { "en": "🔔 SMART ALERTS (3/3)", "te": "🔔 పంట హెచ్చరికలు (3/3)", "hi": "🔔 स्मार्ट अलर्ट (3/3)" },
      "perm_notif_heading": { "en": "Instant Crop Disease Warnings", "te": "నిజ-సమయ తెగుళ్లు & వాతావరణ హెచ్చరికలు", "hi": "फसल कीट व मौसम लाइव अलर्ट" },
      "perm_notif_desc": { "en": "Stay alerted on sudden pest outbreaks in your mandal, best pesticide spray timing windows, and surge mandi price jumps.", "te": "మీ మండలంలో వ్యాపించే తెగుళ్ల హెచ్చరికలు, మందుల పిచికారీ సరైన సమయం మరియు మార్కెట్ ధరల పెరుగుదల సమాచారం అందుకోండి.", "hi": "क्षेत्रीय कीट प्रकोप, कीटनाशक छिड़काव का सही समय और मंडी भाव बढ़ने की सूचना तुरंत प्राप्त करें।" },
      "perm_notif_btn": { "en": "Enable Smart Notifications →", "te": "నోటిఫికేషన్లు ప్రారంభించండి →", "hi": "सूचनाएं चालू करें →" },
      "crops_title": { "en": "Select Your Crops", "te": "మీ పంటలను ఎంచుకోండి", "hi": "अपनी फसलें चुनें" },
      "crops_sub": { "en": "You can change this anytime.", "te": "మీరు దీన్ని ఎప్పుడైనా మార్చవచ్చు.", "hi": "आप इसे कभी भी बदल सकते हैं।" },
      "crops_search_placeholder": { "en": "Search crops (e.g. Cotton, Chilli, Wheat)...", "te": "పంటలను వెతకండి (ఉదా: పత్తి, మిరప, గోధుమ)...", "hi": "फसल खोजें (उदा: कपास, मिर्च, गेहूं)..." },
      "crops_selected_suffix": { "en": "Crops Selected", "te": "పంటలు ఎంచుకోబడ్డాయి", "hi": "फसलें चुनी गईं" },
      "crops_next_btn": { "en": "Continue", "te": "కొనసాగించండి", "hi": "आगे बढ़ें" }
    };

    // Replace the permission screens precisely
    const permCodeBlock = `function renderCameraPermissionScreen(container) {
  NuKropAnalytics.track('onboarding_camera_permission');

  const dotsHtml = \`
    <div style="width:24px;height:5px;border-radius:999px;background:#16A34A;"></div>
    <div style="width:5px;height:5px;border-radius:50%;background:#E2E8F0;"></div>
    <div style="width:5px;height:5px;border-radius:50%;background:#E2E8F0;"></div>
  \`;

  container.innerHTML = \`
    <div style="width:100%;height:100%;position:relative;overflow:hidden;display:flex;flex-direction:column;justify-content:space-between;box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">
      
      <!-- Fullscreen Background Image -->
      <div style="position:absolute;inset:0;background-image:url('images/perm_camera_scan.jpg');background-size:cover;background-position:center;z-index:1;"></div>
      <div style="position:absolute;inset:0;background:linear-gradient(180deg, rgba(15,23,42,0.4) 0%, rgba(15,23,42,0.04) 35%, rgba(15,23,42,0.45) 100%);z-index:2;pointer-events:none;"></div>

      <!-- Top Bar -->
      <div style="position:relative;z-index:10;display:flex;align-items:center;justify-content:space-between;padding:max(52px, env(safe-area-inset-top, 52px)) 20px 0;">
        <div style="background:rgba(30, 41, 59, 0.72);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);color:#FFFFFF;padding:7px 16px;border-radius:999px;font-size:13px;font-weight:700;display:flex;align-items:center;gap:6px;box-shadow:0 4px 12px rgba(0,0,0,0.18);">
          \${OB_TL('perm_badge_1')}
        </div>
        <button onclick="skipCameraPermission()" style="background:#FFFFFF;color:#16A34A;border:none;padding:7px 20px;border-radius:999px;font-size:13px;font-weight:800;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,0.18);">
          \${OB_TL('skip_btn')}
        </button>
      </div>

      <!-- Bottom Sheet Card -->
      <div style="position:relative;z-index:10;background:#FFFFFF;border-radius:36px 36px 0 0;padding:28px 24px 24px;box-shadow:0 -12px 40px rgba(0,0,0,0.22);box-sizing:border-box;">
        
        <!-- Category Pill -->
        <div style="display:inline-flex;align-items:center;gap:6px;background:#DCFCE7;color:#15803D;padding:6px 14px;border-radius:999px;font-size:11.5px;font-weight:800;text-transform:uppercase;letter-spacing:0.4px;margin-bottom:12px;">
          \${OB_TL('perm_camera_tag')}
        </div>

        <!-- Title -->
        <div style="font-size:24px;font-weight:900;color:#0F172A;line-height:1.25;letter-spacing:-0.4px;margin-bottom:8px;">
          \${OB_TL('perm_camera_heading')}
        </div>

        <!-- Subtitle -->
        <div style="font-size:13.5px;color:#64748B;font-weight:500;line-height:1.5;margin-bottom:24px;">
          \${OB_TL('perm_camera_desc')}
        </div>

        <!-- Full Width Green Button -->
        <button onclick="grantCameraPermission()" class="shiny-btn" style="width:100%;padding:16px;background:#16A34A;color:#FFFFFF;border:none;border-radius:18px;font-size:16px;font-weight:900;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:10px;box-shadow:0 8px 24px rgba(22,163,74,0.35);">
          \${OB_TL('perm_camera_btn')}
        </button>

        <!-- Progress Dots -->
        <div style="display:flex;justify-content:center;gap:6px;margin-top:20px;">
          \${dotsHtml}
        </div>
      </div>
    </div>
  \`;
}

function grantCameraPermission() {
  plantixFlowState.cameraAllowed = true;
  if (window.AndroidBridge && typeof AndroidBridge.requestCameraPermission === 'function') {
    AndroidBridge.requestCameraPermission();
  }
  plantixFlowState.currentScreen = 'perm_location';
  renderPlantixFlow();
}

function skipCameraPermission() {
  plantixFlowState.cameraAllowed = false;
  plantixFlowState.currentScreen = 'perm_location';
  renderPlantixFlow();
}

function renderLocationPermissionScreen(container) {
  NuKropAnalytics.track('onboarding_location_permission');

  const dotsHtml = \`
    <div style="width:5px;height:5px;border-radius:50%;background:#E2E8F0;"></div>
    <div style="width:24px;height:5px;border-radius:999px;background:#16A34A;"></div>
    <div style="width:5px;height:5px;border-radius:50%;background:#E2E8F0;"></div>
  \`;

  container.innerHTML = \`
    <div style="width:100%;height:100%;position:relative;overflow:hidden;display:flex;flex-direction:column;justify-content:space-between;box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">
      
      <!-- Fullscreen Background Image -->
      <div style="position:absolute;inset:0;background-image:url('images/perm_location_gps.jpg');background-size:cover;background-position:center;z-index:1;"></div>
      <div style="position:absolute;inset:0;background:linear-gradient(180deg, rgba(15,23,42,0.4) 0%, rgba(15,23,42,0.04) 35%, rgba(15,23,42,0.45) 100%);z-index:2;pointer-events:none;"></div>

      <!-- Top Bar -->
      <div style="position:relative;z-index:10;display:flex;align-items:center;justify-content:space-between;padding:max(52px, env(safe-area-inset-top, 52px)) 20px 0;">
        <div style="background:rgba(30, 41, 59, 0.72);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);color:#FFFFFF;padding:7px 16px;border-radius:999px;font-size:13px;font-weight:700;display:flex;align-items:center;gap:6px;box-shadow:0 4px 12px rgba(0,0,0,0.18);">
          \${OB_TL('perm_badge_2')}
        </div>
        <button onclick="skipLocationPermission()" style="background:#FFFFFF;color:#16A34A;border:none;padding:7px 20px;border-radius:999px;font-size:13px;font-weight:800;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,0.18);">
          \${OB_TL('skip_btn')}
        </button>
      </div>

      <!-- Bottom Sheet Card -->
      <div style="position:relative;z-index:10;background:#FFFFFF;border-radius:36px 36px 0 0;padding:28px 24px 24px;box-shadow:0 -12px 40px rgba(0,0,0,0.22);box-sizing:border-box;">
        
        <!-- Category Pill -->
        <div style="display:inline-flex;align-items:center;gap:6px;background:#DCFCE7;color:#15803D;padding:6px 14px;border-radius:999px;font-size:11.5px;font-weight:800;text-transform:uppercase;letter-spacing:0.4px;margin-bottom:12px;">
          \${OB_TL('perm_location_tag')}
        </div>

        <!-- Title -->
        <div style="font-size:24px;font-weight:900;color:#0F172A;line-height:1.25;letter-spacing:-0.4px;margin-bottom:8px;">
          \${OB_TL('perm_location_heading')}
        </div>

        <!-- Subtitle -->
        <div style="font-size:13.5px;color:#64748B;font-weight:500;line-height:1.5;margin-bottom:24px;">
          \${OB_TL('perm_location_desc')}
        </div>

        <!-- Full Width Green Button -->
        <button onclick="grantLocationPermission()" class="shiny-btn" style="width:100%;padding:16px;background:#16A34A;color:#FFFFFF;border:none;border-radius:18px;font-size:16px;font-weight:900;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:10px;box-shadow:0 8px 24px rgba(22,163,74,0.35);">
          \${OB_TL('perm_location_btn')}
        </button>

        <!-- Progress Dots -->
        <div style="display:flex;justify-content:center;gap:6px;margin-top:20px;">
          \${dotsHtml}
        </div>
      </div>
    </div>
  \`;
}

function grantLocationPermission() {
  plantixFlowState.locationAllowed = true;
  if (window.AndroidBridge && typeof AndroidBridge.requestLocationPermission === 'function') {
    AndroidBridge.requestLocationPermission();
  }
  plantixFlowState.currentScreen = 'perm_notifications';
  renderPlantixFlow();
}

function skipLocationPermission() {
  plantixFlowState.locationAllowed = false;
  plantixFlowState.currentScreen = 'perm_notifications';
  renderPlantixFlow();
}

function renderNotificationPermissionScreen(container) {
  NuKropAnalytics.track('onboarding_notifications_permission');

  const dotsHtml = \`
    <div style="width:5px;height:5px;border-radius:50%;background:#E2E8F0;"></div>
    <div style="width:5px;height:5px;border-radius:50%;background:#E2E8F0;"></div>
    <div style="width:24px;height:5px;border-radius:999px;background:#16A34A;"></div>
  \`;

  container.innerHTML = \`
    <div style="width:100%;height:100%;position:relative;overflow:hidden;display:flex;flex-direction:column;justify-content:space-between;box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">
      
      <!-- Fullscreen Background Image -->
      <div style="position:absolute;inset:0;background-image:url('images/perm_notification_bell.jpg');background-size:cover;background-position:center;z-index:1;"></div>
      <div style="position:absolute;inset:0;background:linear-gradient(180deg, rgba(15,23,42,0.4) 0%, rgba(15,23,42,0.04) 35%, rgba(15,23,42,0.45) 100%);z-index:2;pointer-events:none;"></div>

      <!-- Top Bar -->
      <div style="position:relative;z-index:10;display:flex;align-items:center;justify-content:space-between;padding:max(52px, env(safe-area-inset-top, 52px)) 20px 0;">
        <div style="background:rgba(30, 41, 59, 0.72);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);color:#FFFFFF;padding:7px 16px;border-radius:999px;font-size:13px;font-weight:700;display:flex;align-items:center;gap:6px;box-shadow:0 4px 12px rgba(0,0,0,0.18);">
          \${OB_TL('perm_badge_3')}
        </div>
        <button onclick="skipNotificationPermission()" style="background:#FFFFFF;color:#16A34A;border:none;padding:7px 20px;border-radius:999px;font-size:13px;font-weight:800;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,0.18);">
          \${OB_TL('skip_btn')}
        </button>
      </div>

      <!-- Bottom Sheet Card -->
      <div style="position:relative;z-index:10;background:#FFFFFF;border-radius:36px 36px 0 0;padding:28px 24px 24px;box-shadow:0 -12px 40px rgba(0,0,0,0.22);box-sizing:border-box;">
        
        <!-- Category Pill -->
        <div style="display:inline-flex;align-items:center;gap:6px;background:#DCFCE7;color:#15803D;padding:6px 14px;border-radius:999px;font-size:11.5px;font-weight:800;text-transform:uppercase;letter-spacing:0.4px;margin-bottom:12px;">
          \${OB_TL('perm_notif_tag')}
        </div>

        <!-- Title -->
        <div style="font-size:24px;font-weight:900;color:#0F172A;line-height:1.25;letter-spacing:-0.4px;margin-bottom:8px;">
          \${OB_TL('perm_notif_heading')}
        </div>

        <!-- Subtitle -->
        <div style="font-size:13.5px;color:#64748B;font-weight:500;line-height:1.5;margin-bottom:24px;">
          \${OB_TL('perm_notif_desc')}
        </div>

        <!-- Full Width Green Button -->
        <button onclick="grantNotificationPermission()" class="shiny-btn" style="width:100%;padding:16px;background:#16A34A;color:#FFFFFF;border:none;border-radius:18px;font-size:16px;font-weight:900;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:10px;box-shadow:0 8px 24px rgba(22,163,74,0.35);">
          \${OB_TL('perm_notif_btn')}
        </button>

        <!-- Progress Dots -->
        <div style="display:flex;justify-content:center;gap:6px;margin-top:20px;">
          \${dotsHtml}
        </div>
      </div>
    </div>
  \`;
}

function grantNotificationPermission() {
  plantixFlowState.notificationsAllowed = true;
  if (window.AndroidBridge && typeof AndroidBridge.requestNotificationPermission === 'function') {
    AndroidBridge.requestNotificationPermission();
  } else {
    try {
      if (typeof Notification !== 'undefined' && Notification.requestPermission) {
        Notification.requestPermission();
      }
    } catch(e) {}
  }
  plantixFlowState.currentScreen = 'crops';
  renderPlantixFlow();
}

function skipNotificationPermission() {
  plantixFlowState.notificationsAllowed = false;
  plantixFlowState.currentScreen = 'crops';
  renderPlantixFlow();
}

`;

    const pStart = src.indexOf('function renderCameraPermissionScreen(container) {');
    const pEnd = src.indexOf('function renderPlantixCropsScreen(container) {');
    if (pStart !== -1 && pEnd !== -1) {
        src = src.substring(0, pStart) + permCodeBlock + src.substring(pEnd);
        console.log('Replaced permission block in:', filePath);
    }

    fs.writeFileSync(filePath, src, 'utf8');
    console.log('[OK] Clean and Localized applied to:', filePath);
}

cleanAndLocalizeAll('app/src/main/assets/index.html');
cleanAndLocalizeAll('nukrop_emulator.html');
