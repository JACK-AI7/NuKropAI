import sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Replace showPushNotificationToast JS function
start_pos = text.find('function showPushNotificationToast(payload) {')
end_pos = text.find('function handleDynamicToastAction()')

if start_pos != -1 and end_pos != -1:
    new_fn_code = """function showPushNotificationToast(payload) {
  // Suppress in-app toasts during splash/onboarding experience
  const startupOverlay = document.getElementById('startup-experience-overlay');
  if (startupOverlay && startupOverlay.style.display !== 'none' && !localStorage.getItem('nukrop_onboarding_completed')) {
    return;
  }
  lastToastPayload = payload;
  const sysTitle = (payload && payload.title) || 'NuKropAI Notification';
  const sysMsg = (payload && payload.msg) || '';

  // 1. Post Real Native Android OS Notification in phone status bar / lock screen
  if (window.AndroidBridge && typeof window.AndroidBridge.postSystemNotification === 'function') {
    try {
      window.AndroidBridge.postSystemNotification(sysTitle, sysMsg);
    } catch(e) {
      console.warn('postSystemNotification failed:', e);
    }
    return;
  }

  const toast = document.getElementById('global-push-toast');
  const titleEl = document.getElementById('toast-title');
  const msgEl = document.getElementById('toast-msg');
  const appNameEl = document.getElementById('toast-app-name');
  const timeEl = document.getElementById('toast-time');
  const iconPlate = document.getElementById('toast-icon-plate');
  const iconSvg = document.getElementById('toast-icon-svg');
  const actionBtn = document.getElementById('toast-action-btn');

  if (!toast) return;

  // Clean title from any raw emojis
  let rawTitle = (payload && payload.title) || '';
  let cleanTitle = rawTitle.replace(/^[📈🚨🔔📄🛒📦⚠️🚚🌾🏛️⚡]+\s*/, '').trim();
  if (!cleanTitle) cleanTitle = rawTitle;

  if (titleEl) titleEl.textContent = cleanTitle;
  if (msgEl) msgEl.textContent = (payload && payload.msg) || '';
  if (timeEl) timeEl.textContent = TL('Just now', 'ఇప్పుడే', 'अभी');

  if (payload && payload.type === 'prescription_saved') {
    if (appNameEl) appNameEl.textContent = TL('DIGITAL HEALTH PASSPORT', 'డిజిటల్ హెల్త్ పాస్‌పోర్ట్', 'डिजिटल हेल्थ पासपोर्ट');
    if (iconPlate) iconPlate.style.background = 'linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%)';
    if (iconSvg) iconSvg.innerHTML = '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>';
    if (actionBtn) actionBtn.innerHTML = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" style="flex-shrink:0;"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg> <span>${TL('View Prescriptions', 'ప్రిస్క్రిప్షన్లు చూడండి', 'पर्चा देखें')}</span>`;
  } else if (payload && payload.type === 'order_created') {
    if (appNameEl) appNameEl.textContent = TL('AGRI-STORE ORDER', 'ఆర్డర్ ధృవీకరణ', 'दवा ऑर्डर पुष्टि');
    if (iconPlate) iconPlate.style.background = 'linear-gradient(135deg, #0284C7 0%, #0369A1 100%)';
    if (iconSvg) iconSvg.innerHTML = '<circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>';
    if (actionBtn) actionBtn.innerHTML = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" style="flex-shrink:0;"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg> <span>${TL('View in Farm Khata', 'ఖాతాలో చూడండి', 'खाते में देखें')}</span>`;
  } else if (payload && payload.type === 'price_surge') {
    if (appNameEl) appNameEl.textContent = TL('NUKROP LIVE SURGE TRIGGER', 'లైవ్ ధర పెరుగుదల హెచ్చరిక', 'लाइव भाव वृद्धि अलर्ट');
    if (iconPlate) iconPlate.style.background = 'linear-gradient(135deg, #16A34A 0%, #15803D 100%)';
    if (iconSvg) iconSvg.innerHTML = '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/>';
    if (actionBtn) actionBtn.innerHTML = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" style="flex-shrink:0;"><rect x="1" y="6" width="14" height="11" rx="2"/><polygon points="15 8 19 8 22 11 22 17 15 17 15 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg> <span>${TL('Book Mandi Truck', 'మండి ట్రక్ బుక్ చేయండి', 'मंडी ट्रक बुक करें')}</span>`;
  } else {
    if (appNameEl) appNameEl.textContent = TL('NUKROP AGRI ALERT', 'వ్యవసాయ హెచ్చరిక', 'कृषि अलर्ट');
    if (iconPlate) iconPlate.style.background = 'linear-gradient(135deg, #D97706 0%, #B45309 100%)';
    if (iconSvg) iconSvg.innerHTML = '<path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/>';
    if (actionBtn) actionBtn.innerHTML = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" style="flex-shrink:0;"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg> <span>${TL('View Alerts', 'అలర్ట్స్ చూడండి', 'अलर्ट देखें')}</span>`;
  }

  toast.style.display = 'block';

  if (pushToastTimeout) clearTimeout(pushToastTimeout);
  pushToastTimeout = setTimeout(() => {
    dismissPushToast();
  }, 7000);
}

"""
    text = text[:start_pos] + new_fn_code + text[end_pos:]
    print("✅ Replaced showPushNotificationToast function")

# 2. Remove any remaining automated fake surge timeouts
text = text.replace("""          // 4. Live APMC Market Price Alert Notification
          setTimeout(() => {
            showPushNotificationToast({
              title: '📈 ' + TL('Warangal APMC Live Cotton Rate', 'వరంగల్ APMC పత్తి తాజా ధర', 'वारंगल कपास मंडी ताजा भाव'),
              msg: '₹7,850/Qtl (▲ +₹180/Qtl) · ' + TL('Demand bullish. Good day to harvest & sell.', 'డిమాండ్ పెరిగింది. అమ్మకానికి అనుకూలం.', 'मांग में तेजी। बिक्री का अनुकूल समय।'),
              type: 'price_surge'
            });
          }, 3500);""", "// Automated surge removed")

with open('app/src/main/assets/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("✅ Successfully updated index.html!")
