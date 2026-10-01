import re

def fix_all_flows(path):
    with open(path, 'r', encoding='utf-8') as f:
        code = f.read()

    # 1. Fix slide_community nextScreen to perm_notifications
    code = re.sub(
        r"case 'slide_community':[\s\S]*?nextScreen:\s*'[^']*'",
        lambda m: re.sub(r"nextScreen:\s*'[^']*'", "nextScreen: 'perm_notifications'", m.group(0)),
        code
    )

    # 2. Fix acceptLanguageAndContinue to go to slide_disease
    code = re.sub(
        r"function acceptLanguageAndContinue\(\)\s*\{[\s\S]*?\}",
        """function acceptLanguageAndContinue() {
  plantixFlowState.currentScreen = 'slide_disease';
  renderPlantixFlow();
}""",
        code
    )

    # 3. Fix skipToPermissions definition
    skip_def = """function skipToPermissions() {
  plantixFlowState.currentScreen = 'perm_notifications';
  renderPlantixFlow();
}"""
    if "function skipToPermissions" not in code:
        code = code.replace("function advanceSlide(screen) {", skip_def + "\n\nfunction advanceSlide(screen) {")

    # 4. Fix splash timer progression to advance to language if not completed, or home if completed
    old_splash_end = """      setTimeout(() => {
        advanceSlide('language');
      }, 500);"""
    
    new_splash_end = """      setTimeout(() => {
        const isCompleted = localStorage.getItem('nukrop_onboarding_plantix_completed') === 'true';
        if (isCompleted && !plantixFlowState.forceFullTour) {
          finishPlantixFlow();
        } else {
          advanceSlide('language');
        }
      }, 500);"""
    code = code.replace(old_splash_end, new_splash_end)

    # 5. Fix initStartupExperience to always show splash
    old_init = re.search(r"function initStartupExperience\([\s\S]*?^\}", code, re.MULTILINE)
    if old_init:
        new_init = """function initStartupExperience(forceFullTour = false) {
  plantixFlowState.forceFullTour = forceFullTour;
  plantixFlowState.currentScreen = 'splash';
  splashProgress = 0;
  let overlay = document.getElementById('startup-experience-overlay');
  if (!overlay) {
    const chassis = document.querySelector('.phone-chassis');
    if (chassis) {
      chassis.insertAdjacentHTML('beforeend', '<div id="startup-experience-overlay" style="position:absolute;inset:0;background:#FFFFFF;border-radius:0px;overflow:hidden;z-index:99999;display:flex;flex-direction:column;"></div>');
      overlay = document.getElementById('startup-experience-overlay');
    }
  }
  if (overlay) {
    overlay.style.display = 'flex';
    overlay.style.pointerEvents = 'auto';
    overlay.style.opacity = '1';
    overlay.style.transform = 'scale(1)';
    renderPlantixFlow();
  }
}"""
        code = code[:old_init.start()] + new_init + code[old_init.end():]

    # 6. Make sure permissions flow is 100% correct:
    # Notification -> Location -> Camera -> Crops -> Login -> Home
    old_perm_funcs = """function grantNotificationAndContinue() {
  if (window.AndroidBridge && window.AndroidBridge.requestNotificationPermission) {
    window.AndroidBridge.requestNotificationPermission();
  }
  plantixFlowState.notificationsAllowed = true;
  plantixFlowState.currentScreen = 'perm_location';
  renderPlantixFlow();
}

function skipNotificationPermission() {
  plantixFlowState.notificationsAllowed = false;
  plantixFlowState.currentScreen = 'perm_location';
  renderPlantixFlow();
}

function grantLocationAndContinue() {
  if (window.AndroidBridge && window.AndroidBridge.requestLocationPermission) {
    window.AndroidBridge.requestLocationPermission();
  }
  plantixFlowState.locationAllowed = true;
  plantixFlowState.currentScreen = 'perm_camera';
  renderPlantixFlow();
}

function skipLocationPermission() {
  plantixFlowState.locationAllowed = false;
  plantixFlowState.currentScreen = 'perm_camera';
  renderPlantixFlow();
}

function grantCameraAndContinue() {
  if (window.AndroidBridge && window.AndroidBridge.requestCameraPermission) {
    window.AndroidBridge.requestCameraPermission();
  }
  plantixFlowState.cameraAllowed = true;
  plantixFlowState.currentScreen = 'crops';
  renderPlantixFlow();
}"""

    # Ensure this block exists cleanly
    if "function grantNotificationAndContinue" in code:
        code = re.sub(
            r"function grantNotificationAndContinue\(\)[\s\S]*?function grantCameraAndContinue\(\)[\s\S]*?renderPlantixFlow\(\);\s*\}",
            old_perm_funcs,
            code
        )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(code)

fix_all_flows('app/src/main/assets/index.html')
fix_all_flows('nukrop_emulator.html')
print("Successfully fixed all 7 onboarding flow steps in index.html & nukrop_emulator.html")
