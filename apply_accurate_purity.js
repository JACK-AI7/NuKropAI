const fs = require('fs');

function applyAccurateLanguagePurity(filePath) {
    let src = fs.readFileSync(filePath, 'utf8');

    // 1. Replace getLocalizedCropName
    const cropFnTarget = `function getLocalizedCropName(slug) {
  if (!slug) return 'Crop';
  const aliasMap = {
    'chilli': 'birds-eye-chili',
    'chili': 'birds-eye-chili',
    'paddy': 'rice',
    'maize': 'corn',
    'groundnut': 'peanut',
    'brinjal': 'eggplant',
    'apple': 'generic-apple',
    'banana': 'plantain',
    'cabbage': 'green-cabbage',
    'coriander': 'cilantro',
    'potato': 'russet-potato',
    'capsicum': 'green-bell-pepper',
    'millet': 'sorghum-millet'
  };
  const key = aliasMap[slug] || slug;
  if (CROP_TRANSLATIONS[key] && CROP_TRANSLATIONS[key][currentLang]) {
    return CROP_TRANSLATIONS[key][currentLang];
  }
  if (CROP_TRANSLATIONS[slug] && CROP_TRANSLATIONS[slug][currentLang]) {
    return CROP_TRANSLATIONS[slug][currentLang];
  }
  return slug.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
}`;

    const newCropFn = `function getLocalizedCropName(slugOrKey) {
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
}`;

    if (src.includes(cropFnTarget)) {
        src = src.replace(cropFnTarget, newCropFn);
    } else {
        // Find function getLocalizedCropName and replace its body
        const fnIdx = src.indexOf('function getLocalizedCropName(');
        if (fnIdx !== -1) {
            const endIdx = src.indexOf('}\n\n\n\n\n/* ═════════════════ 🇮🇳 PAN-INDIAN', fnIdx);
            if (endIdx !== -1) {
                src = src.substring(0, fnIdx) + newCropFn + src.substring(endIdx + 1);
            }
        }
    }

    // 2. Replace renderCameraPermissionScreen
    const camPermIdx = src.indexOf('function renderCameraPermissionScreen(container) {');
    if (camPermIdx !== -1) {
        const camPermEnd = src.indexOf('function grantCameraPermission()', camPermIdx);
        if (camPermEnd !== -1) {
            const newCamPerm = `function renderCameraPermissionScreen(container) {
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
        </button>
        <div style="display:flex;justify-content:center;gap:6px;margin-top:20px;">
          \${dotsHtml}
        </div>
      </div>
    </div>
  \`;
}

`;
            src = src.substring(0, camPermIdx) + newCamPerm + src.substring(camPermEnd);
        }
    }

    // 3. Replace renderLocationPermissionScreen
    const locPermIdx = src.indexOf('function renderLocationPermissionScreen(container) {');
    if (locPermIdx !== -1) {
        const locPermEnd = src.indexOf('function grantLocationPermission()', locPermIdx);
        if (locPermEnd !== -1) {
            const newLocPerm = `function renderLocationPermissionScreen(container) {
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
        </button>
        <div style="display:flex;justify-content:center;gap:6px;margin-top:20px;">
          \${dotsHtml}
        </div>
      </div>
    </div>
  \`;
}

`;
            src = src.substring(0, locPermIdx) + newLocPerm + src.substring(locPermEnd);
        }
    }

    // 4. Replace renderNotificationPermissionScreen
    const notifPermIdx = src.indexOf('function renderNotificationPermissionScreen(container) {');
    if (notifPermIdx !== -1) {
        const notifPermEnd = src.indexOf('function grantNotificationPermission()', notifPermIdx);
        if (notifPermEnd !== -1) {
            const newNotifPerm = `function renderNotificationPermissionScreen(container) {
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
        </button>
        <div style="display:flex;justify-content:center;gap:6px;margin-top:20px;">
          \${dotsHtml}
        </div>
      </div>
    </div>
  \`;
}

`;
            src = src.substring(0, notifPermIdx) + newNotifPerm + src.substring(notifPermEnd);
        }
    }

    // 5. Update renderPlantixCropsScreen crop count and button
    const cropsSubSearch = `<div style="font-size:12.5px;color:#64748B;font-weight:600;margin-top:2px;">
          \${OB_TL('crops_sub')} (\${MASTER_120_CROPS.length} OpenFarm crops)
        </div>`;
    const cropsSubReplace = `<div style="font-size:12.5px;color:#64748B;font-weight:600;margin-top:2px;">
          \${OB_TL('crops_sub')} (\${MASTER_120_CROPS.length} \${(typeof currentLang!=='undefined'&&currentLang==='te')?'పంటలు':((typeof currentLang!=='undefined'&&currentLang==='hi')?'फसलें':'crops')})
        </div>`;
    if (src.includes(cropsSubSearch)) {
        src = src.replace(cropsSubSearch, cropsSubReplace);
    }

    fs.writeFileSync(filePath, src, 'utf8');
    console.log('[OK] Applied Accurate Language Purity to:', filePath);
}

applyAccurateLanguagePurity('app/src/main/assets/index.html');
applyAccurateLanguagePurity('nukrop_emulator.html');
