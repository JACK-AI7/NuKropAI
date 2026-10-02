const fs = require('fs');

function fixFile(file) {
  let content = fs.readFileSync(file, 'utf8');

  // Fix Splash -> Language transition
  content = content.replace(/onclick="advanceSlide\('slide_disease'\)"/g, `onclick="advanceSlide('language')"`);

  // Fix Language -> Onboarding transition
  content = content.replace(/function acceptLanguageAndContinue\(\)\s*\{\s*plantixFlowState\.currentScreen = 'login';/g, 
    "function acceptLanguageAndContinue() { plantixFlowState.currentScreen = 'slide_disease';");

  // Fix Camera permission logic
  content = content.replace(/function triggerRealCameraPermission\(\)\s*\{[\s\S]*?grantCameraAndContinue\(\);\s*\}/, 
    `function triggerRealCameraPermission() {
  plantixFlowState.cameraAllowed = true;
  if (window.AndroidBridge && typeof AndroidBridge.requestCameraPermission === 'function') {
    AndroidBridge.requestCameraPermission();
  } else {
    try {
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
          .then(stream => stream.getTracks().forEach(t => t.stop()))
          .catch(e => console.warn("Camera OS prompt:", e));
      }
    } catch(e) {}
  }
  grantCameraAndContinue();
}`);

  // Fix Location permission logic
  content = content.replace(/function triggerRealLocationPermission\(\)\s*\{[\s\S]*?grantLocationAndContinue\(\);\s*\}/, 
    `function triggerRealLocationPermission() {
  plantixFlowState.locationAllowed = true;
  if (window.AndroidBridge && typeof AndroidBridge.requestLocationPermission === 'function') {
    AndroidBridge.requestLocationPermission();
  } else {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(() => {}, () => {});
    }
  }
  grantLocationAndContinue();
}`);

  fs.writeFileSync(file, content, 'utf8');
}

['app/src/main/assets/index.html', 'nukrop_emulator.html'].forEach(fixFile);
console.log('Flow Fixed');
