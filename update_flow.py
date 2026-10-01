import re

def update_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update grantNotificationAndContinue to call AndroidBridge and go to perm_location
    old_grant_notif = """function grantNotificationAndContinue() {
  plantixFlowState.notificationsAllowed = true;
  plantixFlowState.currentScreen = 'perm_camera';
  renderPlantixFlow();
}

function skipNotificationPermission() {
  plantixFlowState.notificationsAllowed = false;
  plantixFlowState.currentScreen = 'perm_camera';
  renderPlantixFlow();
}"""

    new_grant_notif = """function grantNotificationAndContinue() {
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
}"""

    content = content.replace(old_grant_notif, new_grant_notif)

    # 2. Update grantLocationAndContinue to call AndroidBridge and go to perm_camera
    old_grant_loc = """function grantLocationAndContinue() {
  plantixFlowState.locationAllowed = true;
  plantixFlowState.currentScreen = 'perm_notifications';
  renderPlantixFlow();
}

function skipLocationPermission() {
  plantixFlowState.locationAllowed = false;
  plantixFlowState.currentScreen = 'perm_notifications';
  renderPlantixFlow();
}"""

    new_grant_loc = """function grantLocationAndContinue() {
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
}"""

    content = content.replace(old_grant_loc, new_grant_loc)

    # 3. Update grantCameraAndContinue to call AndroidBridge and go to crops
    old_grant_cam = """function grantCameraAndContinue() {
  plantixFlowState.cameraAllowed = true;
  plantixFlowState.currentScreen = 'crops';
  renderPlantixFlow();
}"""

    new_grant_cam = """function grantCameraAndContinue() {
  if (window.AndroidBridge && window.AndroidBridge.requestCameraPermission) {
    window.AndroidBridge.requestCameraPermission();
  }
  plantixFlowState.cameraAllowed = true;
  plantixFlowState.currentScreen = 'crops';
  renderPlantixFlow();
}"""

    content = content.replace(old_grant_cam, new_grant_cam)

    # 4. Update crops screen button to proceedFromCropsToLogin
    content = content.replace(
        'onclick="finishPlantixOnboarding()"',
        'onclick="proceedFromCropsToLogin()"'
    )

    # 5. Define proceedFromCropsToLogin and finishPlantixFlow
    old_finish_onboarding = """function finishPlantixOnboarding() {
  try {
    NuKropAnalytics.track('onboarding_completed', {
      lang: plantixFlowState.selectedLang,
      crops: plantixFlowState.selectedCrops,
      locationAllowed: plantixFlowState.locationAllowed,
      cameraAllowed: plantixFlowState.cameraAllowed
    });
  } catch(e) {}

  try {
    localStorage.setItem('nukrop_onboarding_plantix_completed', 'true');
  } catch(e) {}

  if (plantixFlowState.selectedCrops && plantixFlowState.selectedCrops.length > 0) {
    myActiveCrops = plantixFlowState.selectedCrops.map(cropKey => {
      const found = MASTER_120_CROPS.find(x => x.key === cropKey) || { slug: cropKey };
      const slug = found.slug || cropKey;
      return {
        id: cropKey,
        slug: slug,
        path: slug + '/' + slug + '.svg'
      };
    });
    activeCropIdx = 0;
    try {
      localStorage.setItem('nukrop_user_active_crops', JSON.stringify(myActiveCrops));
    } catch(e) {}
    if (typeof currentUserProfile !== 'undefined') {
      currentUserProfile.crops = myActiveCrops;
    }
  }

  const overlay = document.getElementById('startup-experience-overlay');
  if (overlay) {
    overlay.style.pointerEvents = 'none';
    overlay.style.transition = 'opacity 0.25s ease, transform 0.25s ease';
    overlay.style.opacity = '0';
    overlay.style.transform = 'scale(0.95)';
    setTimeout(() => {
      try { overlay.remove(); } catch(e) { overlay.style.display = 'none'; }
    }, 250);
  }

  try {
    if (typeof openScreen === 'function') {
      openScreen('home', document.getElementById('tab-home'));
    }
  } catch(e) {
    console.error('Error opening home screen:', e);
  }
}"""

    new_flow_handlers = """function proceedFromCropsToLogin() {
  if (plantixFlowState.selectedCrops && plantixFlowState.selectedCrops.length > 0) {
    myActiveCrops = plantixFlowState.selectedCrops.map(cropKey => {
      const found = MASTER_120_CROPS.find(x => x.key === cropKey) || { slug: cropKey };
      const slug = found.slug || cropKey;
      return {
        id: cropKey,
        slug: slug,
        path: slug + '/' + slug + '.svg'
      };
    });
    activeCropIdx = 0;
    try {
      localStorage.setItem('nukrop_user_active_crops', JSON.stringify(myActiveCrops));
    } catch(e) {}
    if (typeof currentUserProfile !== 'undefined') {
      currentUserProfile.crops = myActiveCrops;
    }
  }
  plantixFlowState.currentScreen = 'login';
  renderPlantixFlow();
}

function finishPlantixOnboarding() {
  proceedFromCropsToLogin();
}

function finishPlantixFlow() {
  try {
    NuKropAnalytics.track('onboarding_completed', {
      lang: plantixFlowState.selectedLang,
      crops: plantixFlowState.selectedCrops,
      locationAllowed: plantixFlowState.locationAllowed,
      cameraAllowed: plantixFlowState.cameraAllowed
    });
  } catch(e) {}

  try {
    localStorage.setItem('nukrop_onboarding_plantix_completed', 'true');
  } catch(e) {}

  const overlay = document.getElementById('startup-experience-overlay');
  if (overlay) {
    overlay.style.pointerEvents = 'none';
    overlay.style.transition = 'opacity 0.25s ease, transform 0.25s ease';
    overlay.style.opacity = '0';
    overlay.style.transform = 'scale(0.95)';
    setTimeout(() => {
      try { overlay.remove(); } catch(e) { overlay.style.display = 'none'; }
    }, 250);
  }

  try {
    if (typeof openScreen === 'function') {
      openScreen('home', document.getElementById('tab-home'));
    }
  } catch(e) {
    console.error('Error opening home screen:', e);
  }
}"""

    content = content.replace(old_finish_onboarding, new_flow_handlers)

    # 6. Update boot to run immediately
    old_boot = """// Initial Boot & Fetch Real Weather
function nukropBoot() {
  setLanguage('en');
  fetchRealLocationAndWeather();
  // initStartupExperience is triggered by MainActivity.kt after page load
  // with forceReplay=true so splash always shows.
  // Fallback: if not triggered by native in 1s, start it ourselves.
  setTimeout(function() {
    if (typeof initStartupExperience === 'function') {
      initStartupExperience(true);
    }
  }, 800);
}
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', nukropBoot);
} else {
  nukropBoot();
}"""

    new_boot = """// Initial Boot & Fetch Real Weather
function nukropBoot() {
  setLanguage('en');
  initStartupExperience();
  fetchRealLocationAndWeather();
}
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', nukropBoot);
} else {
  nukropBoot();
}"""

    content = content.replace(old_boot, new_boot)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

update_file('app/src/main/assets/index.html')
update_file('nukrop_emulator.html')
print("Updated onboarding flow in index.html and nukrop_emulator.html")
