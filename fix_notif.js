const fs = require('fs');

function fixFile(file) {
  let content = fs.readFileSync(file, 'utf8');

  content = content.replace(/function triggerRealNotificationPermission\(\)\s*\{[\s\S]*?grantNotificationAndContinue\(\);\s*\}/, 
    `function triggerRealNotificationPermission() {
  plantixFlowState.notificationsAllowed = true;
  if (window.AndroidBridge && typeof AndroidBridge.requestNotificationPermission === 'function') {
    AndroidBridge.requestNotificationPermission();
  } else {
    try {
      if (typeof Notification !== 'undefined' && Notification.requestPermission) {
        Notification.requestPermission().catch(e => console.warn("Notif prompt:", e));
      }
    } catch(e) {}
  }
  grantNotificationAndContinue();
}`);

  fs.writeFileSync(file, content, 'utf8');
}

['app/src/main/assets/index.html', 'nukrop_emulator.html'].forEach(fixFile);
console.log('Notif Fixed');
