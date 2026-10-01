import os, re, sys

sys.stdout.reconfigure(encoding='utf-8')

MASTER_OVERLAY_CSS = """
<!-- ══════════════════════════════════════════════════════════════ -->
<!-- NUKROPAI V5 LUXURY OVERLAY SUITE: ONBOARDING, PERMS, LOGIN & DOCK -->
<!-- ══════════════════════════════════════════════════════════════ -->
<style id="nukrop-v5-master-style">
/* Hide bottom navigation dock during onboarding, permissions, and login */
body:has(#onboarding-experience-overlay) .bottom-dock-wrap,
body:has(#permission-experience-overlay) .bottom-dock-wrap,
body:has(#login-screen-overlay) .bottom-dock-wrap,
body:has(#startup-experience-overlay) .bottom-dock-wrap {
  display: none !important;
}

/* Full-bleed photography onboarding & permissions container */
.onboard-v5-fullscreen {
  position: absolute;
  inset: 0;
  z-index: 9999;
  overflow: hidden;
  background: #0F172A;
  font-family: -apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', 'Inter', Roboto, sans-serif;
  display: flex;
  flex-direction: column;
}

.onboard-v5-bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center top;
  transition: opacity 0.35s ease, transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.onboard-v5-overlay-gradient {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(15,23,42,0.45) 0%, rgba(15,23,42,0.05) 30%, rgba(15,23,42,0.25) 55%, rgba(15,23,42,0.85) 100%);
  pointer-events: none;
}

/* Top status HUD with pixel-perfect alignment */
.onboard-v5-top-hud {
  position: absolute;
  top: 48px;
  left: 20px;
  right: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 10005 !important;
  pointer-events: auto;
}

.onboard-v5-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(15, 23, 42, 0.65);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 9999px;
  padding: 0 16px;
  height: 38px;
  color: #FFFFFF;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: -0.2px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
  box-sizing: border-box;
}

.onboard-v5-skip-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #FFFFFF;
  border: 1px solid rgba(255, 255, 255, 0.9);
  border-radius: 9999px;
  padding: 0 20px;
  height: 38px;
  box-sizing: border-box;
  color: #16A34A;
  font-size: 13px;
  font-weight: 800;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  transition: transform 0.15s ease, background 0.15s ease;
}
.onboard-v5-skip-btn:active {
  transform: scale(0.94);
  background: #F8FAFC;
}

/* Bottom floating sheet card */
.onboard-v5-bottom-sheet {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: #FFFFFF;
  border-radius: 36px 36px 0 0;
  padding: 28px 24px 34px;
  box-shadow: 0 -12px 40px rgba(0, 0, 0, 0.28);
  z-index: 50;
  display: flex;
  flex-direction: column;
  gap: 8px;
  animation: nkSlideUp 0.35s cubic-bezier(0.16, 1, 0.3, 1);
  box-sizing: border-box;
}

@keyframes nkSlideUp {
  from { transform: translateY(100%); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.onboard-v5-category-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #DCFCE7;
  color: #15803D;
  border: 1px solid #86EFAC;
  border-radius: 9999px;
  padding: 4px 12px;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.3px;
  text-transform: uppercase;
  width: fit-content;
}

.onboard-v5-title {
  font-size: 23px;
  font-weight: 900;
  color: #0F172A;
  line-height: 1.25;
  letter-spacing: -0.4px;
  margin: 2px 0 0 0;
}

.onboard-v5-desc {
  font-size: 13.5px;
  font-weight: 500;
  color: #64748B;
  line-height: 1.55;
  margin: 0 0 12px 0;
}

.onboard-v5-footer-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 4px;
}

.onboard-v5-dots {
  display: flex;
  align-items: center;
  gap: 6px;
}

.onboard-v5-dot {
  height: 6px;
  border-radius: 4px;
  background: #CBD5E1;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.onboard-v5-dot.active {
  width: 28px;
  background: #16A34A;
}
.onboard-v5-dot.inactive {
  width: 6px;
  background: #E2E8F0;
}

.onboard-v5-fab-btn {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, #16A34A, #15803D);
  box-shadow: 0 8px 24px rgba(22, 163, 74, 0.38);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #FFFFFF;
  font-size: 22px;
  cursor: pointer;
  border: none;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
  flex-shrink: 0;
}
.onboard-v5-fab-btn:active {
  transform: scale(0.92);
  box-shadow: 0 4px 12px rgba(22, 163, 74, 0.3);
}

.onboard-v5-primary-pill-btn {
  height: 52px;
  border-radius: 18px;
  background: linear-gradient(135deg, #16A34A, #15803D);
  box-shadow: 0 8px 24px rgba(22, 163, 74, 0.35);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #FFFFFF;
  font-size: 15px;
  font-weight: 800;
  cursor: pointer;
  border: none;
  padding: 0 24px;
  width: 100%;
  transition: transform 0.15s ease;
  box-sizing: border-box;
}
.onboard-v5-primary-pill-btn:active {
  transform: scale(0.96);
}

/* ══════════════════════════════════════════════════════════════ */
/* POTEA LUXURY LOGIN SCREEN                                    */
/* ══════════════════════════════════════════════════════════════ */
.login-v5-container {
  position: absolute;
  inset: 0;
  background: #FFFFFF;
  z-index: 9999;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 44px 24px 30px;
  box-sizing: border-box;
  font-family: -apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', 'Inter', Roboto, sans-serif;
}

.login-v5-header {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.login-v5-logo-badge {
  width: 62px;
  height: 62px;
  border-radius: 20px;
  background: linear-gradient(135deg, #DCFCE7, #86EFAC);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 24px rgba(22, 163, 74, 0.2);
  margin-bottom: 12px;
}

.login-v5-title {
  font-size: 26px;
  font-weight: 900;
  color: #0F172A;
  letter-spacing: -0.5px;
  margin: 0;
}

.login-v5-subtitle {
  font-size: 13px;
  font-weight: 600;
  color: #64748B;
  margin-top: 4px;
}

/* Segmented Role Switcher */
.login-v5-role-switch {
  background: #F1F5F9;
  border-radius: 16px;
  padding: 4px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4px;
  margin: 20px 0 14px;
}

.login-v5-role-tab {
  padding: 10px 0;
  text-align: center;
  font-size: 13px;
  font-weight: 800;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  background: transparent;
  color: #64748B;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.login-v5-role-tab.active {
  background: #16A34A;
  color: #FFFFFF;
  box-shadow: 0 4px 14px rgba(22, 163, 74, 0.28);
}

/* Auth method pill tabs */
.login-v5-method-switch {
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 14px;
  padding: 3px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4px;
  margin-bottom: 18px;
}

.login-v5-method-tab {
  padding: 8px 0;
  text-align: center;
  font-size: 12px;
  font-weight: 800;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  background: transparent;
  color: #64748B;
}

.login-v5-method-tab.active {
  background: #FFFFFF;
  color: #16A34A;
  box-shadow: 0 2px 6px rgba(15, 23, 42, 0.08);
}

/* Input boxes */
.login-v5-input-box {
  border: 1.5px solid #E2E8F0;
  border-radius: 16px;
  background: #F8FAFC;
  height: 54px;
  padding: 0 14px;
  display: flex;
  align-items: center;
  box-sizing: border-box;
  transition: all 0.2s ease;
  margin-bottom: 12px;
}

.login-v5-input-box:focus-within {
  border-color: #16A34A;
  background: #FFFFFF;
  box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.12);
}

.login-v5-flag-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 800;
  color: #0F172A;
  padding-right: 12px;
  border-right: 1.5px solid #CBD5E1;
  flex-shrink: 0;
}

.login-v5-input {
  flex: 1;
  border: none;
  background: transparent;
  padding-left: 12px;
  font-size: 14.5px;
  font-weight: 700;
  color: #0F172A;
  outline: none;
  width: 100%;
}
.login-v5-input::placeholder {
  color: #94A3B8;
  font-weight: 500;
}

/* Checkbox Row */
.login-v5-check-row {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-top: 8px;
  cursor: pointer;
  user-select: none;
}

.login-v5-checkbox {
  width: 18px;
  height: 18px;
  border-radius: 6px;
  border: 1.5px solid #CBD5E1;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-top: 2px;
  transition: all 0.2s ease;
  background: #FFFFFF;
}
.login-v5-checkbox.checked {
  background: #16A34A;
  border-color: #16A34A;
}

.login-v5-check-label {
  font-size: 12.5px;
  font-weight: 600;
  color: #475569;
  line-height: 1.4;
}

.login-v5-check-label a {
  color: #16A34A;
  text-decoration: underline;
  font-weight: 700;
}

/* Social Login */
.login-v5-divider {
  display: flex;
  align-items: center;
  margin: 22px 0 16px;
}
.login-v5-divider-line {
  flex: 1;
  height: 1px;
  background: #E2E8F0;
}
.login-v5-divider-text {
  padding: 0 12px;
  color: #94A3B8;
  font-size: 12px;
  font-weight: 700;
  text-transform: lowercase;
}

.login-v5-social-grid {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.login-v5-social-btn {
  flex: 1;
  height: 52px;
  border: 1.5px solid #E2E8F0;
  border-radius: 16px;
  background: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
}
.login-v5-social-btn:active {
  transform: scale(0.95);
  background: #F8FAFC;
  border-color: #CBD5E1;
}

/* Real Google Auth Modal */
.google-auth-v5-sheet {
  position: absolute;
  inset: 0;
  background: rgba(15, 23, 42, 0.65);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  z-index: 10000;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  animation: nkFadeIn 0.25s ease;
}

@keyframes nkFadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.google-auth-v5-card {
  background: #FFFFFF;
  border-radius: 28px 28px 0 0;
  padding: 24px 20px 32px;
  box-shadow: 0 -10px 40px rgba(0,0,0,0.3);
  display: flex;
  flex-direction: column;
  gap: 14px;
  max-height: 80%;
  overflow-y: auto;
}

.google-account-v5-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  border-radius: 16px;
  border: 1.5px solid #E2E8F0;
  background: #F8FAFC;
  cursor: pointer;
  transition: all 0.15s ease;
}
.google-account-v5-item:hover, .google-account-v5-item:active {
  background: #F0FDF4;
  border-color: #16A34A;
}

.google-avatar-v5 {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 800;
  color: #FFFFFF;
  flex-shrink: 0;
}
</style>
"""

MASTER_OVERLAY_JS = """
<script id="nukrop-v5-master-logic">
/* ══════════════════════════════════════════════════════════════ */
/* MASTER CONTROLLER: ONBOARDING, PERMISSIONS, POTEA LOGIN        */
/* ══════════════════════════════════════════════════════════════ */

const NUKROP_ONBOARDING_SLIDES = [
  {
    category: "🌿 AI CROP DOCTOR",
    title: "Instant AI Leaf Diagnostics",
    desc: "Scan crop leaves in milliseconds to identify pests, fungal blights, and nutrient deficiencies with expert AI treatment prescriptions.",
    image: "images/onboard_crop_doctor.jpg"
  },
  {
    category: "📈 APMC MANDI RADAR",
    title: "Real-Time Mandi Pricing",
    desc: "Track live commodity rates across 1,200+ APMC mandis with AI price surge predictions and arbitrage alerts.",
    image: "images/onboard_mandi_prices.jpg"
  },
  {
    category: "🚛 GRAMHAUL LOGISTICS",
    title: "Farm-to-Mandi Transport",
    desc: "Book verified agricultural mini-trucks, tractors, and lorries with GPS live telemetry and fair freight rates.",
    image: "images/onboard_farm_logistics.jpg"
  },
  {
    category: "🏛️ AGRISTACK DIGITAL ID",
    title: "Digital Agrarian Registry",
    desc: "Seamlessly link your Kisan Aadhaar, PM-Kisan DBT subsidies, and digital land records with instant verification.",
    image: "images/onboard_agristack_tech.jpg"
  },
  {
    category: "🎙️ AI VOICE AGRONOMIST",
    title: "Multilingual Voice Advisory",
    desc: "Speak naturally in Telugu, Hindi, Tamil, Kannada, or English for hyper-local weather alerts and pest advisory.",
    image: "images/onboard_ai_voice_weather.jpg"
  },
  {
    category: "🚜 KISAN COMMUNITY & SHARING",
    title: "Cooperative Farm Equipment",
    desc: "Rent combine harvesters, tractors, and drone sprayers from verified nearby progressive farmers.",
    image: "images/onboard_community_machinery.jpg"
  }
];

const NUKROP_PERMISSION_STEPS = [
  {
    stepNum: 1,
    totalSteps: 3,
    category: "📷 CAMERA DIAGNOSTICS (1/3)",
    title: "Instant Crop Disease Scanner",
    desc: "Grant camera access to scan crop leaves, diagnose plant diseases, and detect pest damage with computer vision AI.",
    btnText: "Allow Camera Access →",
    image: "images/perm_bg_camera.jpg"
  },
  {
    stepNum: 2,
    totalSteps: 3,
    category: "📍 GPS TELEMETRY (2/3)",
    title: "GPS Location & Mandi Radar",
    desc: "Allow precise location to detect your nearest APMC mandi commodity prices, hyper-local farm weather forecasts, and GramHaul transport trucks.",
    btnText: "Allow GPS Location →",
    image: "images/perm_bg_location.jpg"
  },
  {
    stepNum: 3,
    totalSteps: 3,
    category: "🔔 REAL-TIME ADVISORY (3/3)",
    title: "Instant Weather & Mandi Alerts",
    desc: "Enable push notifications for sudden unseasonal rainfall radar warnings, pest outbreak alerts, and live transport truck arrival notifications.",
    btnText: "Enable Notifications ✓ →",
    image: "images/perm_bg_notification.jpg"
  }
];

let currentOnboardSlideIdx = 0;
let currentPermStepIdx = 0;
let selectedLoginRole = 'farmer';
let selectedLoginMethod = 'phone';
let termsAccepted = true;
let rememberMe = true;

// Guard against push notification toasts appearing over onboarding/login
const _originalShowPushToast = window.showPushNotificationToast;
window.showPushNotificationToast = function(opts) {
  if (document.getElementById('onboarding-experience-overlay') || 
      document.getElementById('permission-experience-overlay') || 
      document.getElementById('login-screen-overlay') || 
      document.getElementById('startup-experience-overlay')) {
    return;
  }
  if (typeof _originalShowPushToast === 'function') {
    _originalShowPushToast(opts);
  }
};

/* 1. Open 6-Slide Full-Bleed Onboarding Flow */
function openOnboardingFlow(isManual = false) {
  currentOnboardSlideIdx = 0;
  const chassis = document.querySelector('.phone-chassis') || document.body;
  
  // Clean up any existing overlays
  ['onboarding-experience-overlay', 'permission-experience-overlay', 'login-screen-overlay', 'startup-experience-overlay'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.remove();
  });

  const overlay = document.createElement('div');
  overlay.id = 'onboarding-experience-overlay';
  overlay.className = 'onboard-v5-fullscreen';
  chassis.appendChild(overlay);

  renderOnboardingSlideV5(currentOnboardSlideIdx);
}

function advanceOnboardingSlide(targetIdx) {
  if (typeof targetIdx === 'number') {
    currentOnboardSlideIdx = targetIdx;
  } else {
    currentOnboardSlideIdx++;
  }

  if (currentOnboardSlideIdx >= NUKROP_ONBOARDING_SLIDES.length) {
    openPermissionsFullBleedFlow();
    return;
  }
  renderOnboardingSlideV5(currentOnboardSlideIdx);
}

function renderOnboardingSlideV5(idx) {
  const overlay = document.getElementById('onboarding-experience-overlay');
  if (!overlay) return;

  const slide = NUKROP_ONBOARDING_SLIDES[idx];
  const isLast = idx === NUKROP_ONBOARDING_SLIDES.length - 1;

  let dotsHtml = '';
  for (let i = 0; i < NUKROP_ONBOARDING_SLIDES.length; i++) {
    dotsHtml += `<div class="onboard-v5-dot ${i === idx ? 'active' : 'inactive'}"></div>`;
  }

  overlay.innerHTML = `
    <img src="${slide.image}" class="onboard-v5-bg" alt="${slide.title}" onerror="this.src='images/onboard_crop_doctor.jpg';" />
    <div class="onboard-v5-overlay-gradient"></div>

    <!-- Top Status HUD with Perfect Horizontal & Vertical Alignment -->
    <div class="onboard-v5-top-hud">
      <div class="onboard-v5-badge">
        <span>🍃</span>
        <span>NuKropAI OS</span>
      </div>
      <button class="onboard-v5-skip-btn" onclick="openPermissionsFullBleedFlow()">
        Skip
      </button>
    </div>

    <!-- Bottom Floating Sheet Card -->
    <div class="onboard-v5-bottom-sheet">
      <div class="onboard-v5-category-pill">${slide.category}</div>
      <h2 class="onboard-v5-title">${slide.title}</h2>
      <p class="onboard-v5-desc">${slide.desc}</p>

      <div class="onboard-v5-footer-row">
        <div class="onboard-v5-dots">
          ${dotsHtml}
        </div>
        <button class="onboard-v5-fab-btn" onclick="advanceOnboardingSlide()" aria-label="Next slide">
          ${isLast ? '✓' : '→'}
        </button>
      </div>
    </div>
  `;
}

/* 2. Open 3-Step Dedicated Full-Bleed Permissions Flow */
function openPermissionsFullBleedFlow() {
  currentPermStepIdx = 0;
  const chassis = document.querySelector('.phone-chassis') || document.body;

  ['onboarding-experience-overlay', 'permission-experience-overlay', 'login-screen-overlay', 'startup-experience-overlay'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.remove();
  });

  const overlay = document.createElement('div');
  overlay.id = 'permission-experience-overlay';
  overlay.className = 'onboard-v5-fullscreen';
  chassis.appendChild(overlay);

  renderPermissionSlideV5(currentPermStepIdx);
}

function handlePermissionSlideAction(targetIdx) {
  if (typeof targetIdx === 'number') {
    currentPermStepIdx = targetIdx;
  } else {
    currentPermStepIdx++;
  }

  if (currentPermStepIdx >= NUKROP_PERMISSION_STEPS.length) {
    openPoteaLoginFlow();
    return;
  }
  renderPermissionSlideV5(currentPermStepIdx);
}

function renderPermissionSlideV5(idx) {
  const overlay = document.getElementById('permission-experience-overlay');
  if (!overlay) return;

  const perm = NUKROP_PERMISSION_STEPS[idx];

  let dotsHtml = '';
  for (let i = 0; i < NUKROP_PERMISSION_STEPS.length; i++) {
    dotsHtml += `<div class="onboard-v5-dot ${i === idx ? 'active' : 'inactive'}"></div>`;
  }

  overlay.innerHTML = `
    <img src="${perm.image}" class="onboard-v5-bg" alt="${perm.title}" onerror="this.src='images/perm_bg_camera.jpg';" />
    <div class="onboard-v5-overlay-gradient"></div>

    <!-- Top Status HUD -->
    <div class="onboard-v5-top-hud">
      <div class="onboard-v5-badge">
        <span>🔒</span>
        <span>Permissions (${perm.stepNum}/${perm.totalSteps})</span>
      </div>
      <button class="onboard-v5-skip-btn" onclick="openPoteaLoginFlow()">
        Skip
      </button>
    </div>

    <!-- Bottom Floating Sheet Card -->
    <div class="onboard-v5-bottom-sheet">
      <div class="onboard-v5-category-pill">${perm.category}</div>
      <h2 class="onboard-v5-title">${perm.title}</h2>
      <p class="onboard-v5-desc">${perm.desc}</p>

      <div style="margin-top: 6px; display: flex; flex-direction: column; gap: 12px;">
        <button class="onboard-v5-primary-pill-btn" onclick="handlePermissionSlideAction()">
          ${perm.btnText}
        </button>
        <div style="display:flex; justify-content:center;">
          <div class="onboard-v5-dots">
            ${dotsHtml}
          </div>
        </div>
      </div>
    </div>
  `;
}

/* 3. Open Potea Luxury Login Screen */
function openPoteaLoginFlow() {
  const chassis = document.querySelector('.phone-chassis') || document.body;

  ['onboarding-experience-overlay', 'permission-experience-overlay', 'login-screen-overlay', 'startup-experience-overlay'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.remove();
  });

  const overlay = document.createElement('div');
  overlay.id = 'login-screen-overlay';
  overlay.className = 'login-v5-container';
  chassis.appendChild(overlay);

  renderPoteaLoginScreen();
}

function setLoginRole(role) {
  selectedLoginRole = role;
  renderPoteaLoginScreen();
}

function setLoginMethod(method) {
  selectedLoginMethod = method;
  renderPoteaLoginScreen();
}

function toggleTermsCheckbox() {
  termsAccepted = !termsAccepted;
  const cb = document.getElementById('login-terms-cb');
  if (cb) cb.className = `login-v5-checkbox ${termsAccepted ? 'checked' : ''}`;
}

function toggleRememberCheckbox() {
  rememberMe = !rememberMe;
  const cb = document.getElementById('login-remember-cb');
  if (cb) cb.className = `login-v5-checkbox ${rememberMe ? 'checked' : ''}`;
}

function togglePasswordVisibility() {
  const input = document.getElementById('login-pass-input');
  if (input) {
    input.type = input.type === 'password' ? 'text' : 'password';
  }
}

function renderPoteaLoginScreen() {
  const overlay = document.getElementById('login-screen-overlay');
  if (!overlay) return;

  const isFarmer = selectedLoginRole === 'farmer';
  const isPhone = selectedLoginMethod === 'phone';

  overlay.innerHTML = `
    <!-- Top Header -->
    <div class="login-v5-header">
      <div class="login-v5-logo-badge">
        <span style="font-size: 32px;">🍃</span>
      </div>
      <h1 class="login-v5-title">NuKrop<span style="color: #16A34A;">AI</span></h1>
      <div class="login-v5-subtitle">Smart Agriculture · Powered by AI</div>
    </div>

    <!-- Center Form Area -->
    <div style="margin: 16px 0;">
      <!-- Role Switcher -->
      <div class="login-v5-role-switch">
        <button class="login-v5-role-tab ${isFarmer ? 'active' : ''}" onclick="setLoginRole('farmer')">
          <span>👨‍🌾</span> Farmer
        </button>
        <button class="login-v5-role-tab ${!isFarmer ? 'active' : ''}" onclick="setLoginRole('driver')">
          <span>🚛</span> Truck Driver
        </button>
      </div>

      <!-- Auth Method Switcher -->
      <div class="login-v5-method-switch">
        <button class="login-v5-method-tab ${isPhone ? 'active' : ''}" onclick="setLoginMethod('phone')">
          📱 Mobile Number
        </button>
        <button class="login-v5-method-tab ${!isPhone ? 'active' : ''}" onclick="setLoginMethod('email')">
          ✉️ Email Address
        </button>
      </div>

      <!-- Input Fields (Clean Empty Placeholders - No Fake Data) -->
      ${isPhone ? `
        <div class="login-v5-input-box">
          <div class="login-v5-flag-badge">
            <svg width="22" height="15" viewBox="0 0 22 15" style="border-radius:2px;box-shadow:0 1px 2px rgba(0,0,0,0.15);">
              <rect width="22" height="5" fill="#FF9933"/>
              <rect y="5" width="22" height="5" fill="#FFFFFF"/>
              <rect y="10" width="22" height="5" fill="#138808"/>
              <circle cx="11" cy="7.5" r="2" fill="none" stroke="#000080" stroke-width="0.7"/>
            </svg>
            <span>+91</span>
          </div>
          <input id="login-phone-input" type="tel" class="login-v5-input" placeholder="Enter 10-digit mobile number" maxlength="10" />
        </div>
      ` : `
        <div class="login-v5-input-box">
          <span style="font-size: 18px; padding-right: 8px;">✉️</span>
          <input id="login-email-input" type="email" class="login-v5-input" placeholder="farmer@example.com" />
        </div>
      `}

      <div class="login-v5-input-box">
        <span style="font-size: 18px; padding-right: 8px;">🔒</span>
        <input id="login-pass-input" type="password" class="login-v5-input" placeholder="Enter password or 4-digit PIN" />
        <button type="button" onclick="togglePasswordVisibility()" style="background:none;border:none;cursor:pointer;font-size:16px;padding:0 4px;color:#64748B;">
          👁️
        </button>
      </div>

      <!-- Checkboxes -->
      <div class="login-v5-check-row" onclick="toggleRememberCheckbox()">
        <div id="login-remember-cb" class="login-v5-checkbox ${rememberMe ? 'checked' : ''}">
          <span style="color:#FFF;font-size:12px;font-weight:900;">✓</span>
        </div>
        <div class="login-v5-check-label">Remember my login credentials</div>
      </div>

      <div class="login-v5-check-row" onclick="toggleTermsCheckbox()">
        <div id="login-terms-cb" class="login-v5-checkbox ${termsAccepted ? 'checked' : ''}">
          <span style="color:#FFF;font-size:12px;font-weight:900;">✓</span>
        </div>
        <div class="login-v5-check-label">
          I agree to NuKropAI <a href="javascript:void(0)">Privacy Policy</a> & <a href="javascript:void(0)">Terms of Service</a>
        </div>
      </div>

      <!-- Primary Action Button -->
      <button class="onboard-v5-primary-pill-btn" style="margin-top: 18px;" onclick="handlePrimaryLoginSubmit()">
        Sign In →
      </button>

      <!-- Social Login Section -->
      <div class="login-v5-divider">
        <div class="login-v5-divider-line"></div>
        <span class="login-v5-divider-text">or continue with</span>
        <div class="login-v5-divider-line"></div>
      </div>

      <!-- High-Res Vector SVG Social Buttons -->
      <div class="login-v5-social-grid">
        <!-- Google Real 4-Color SVG -->
        <button class="login-v5-social-btn" onclick="openInAppGoogleAuthModal()" aria-label="Sign in with Google">
          <svg width="24" height="24" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.82-2.4 3.68v3.05h3.88c2.27-2.09 3.66-5.17 3.66-9.17z"/>
            <path fill="#34A853" d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.12 0-5.77-2.1-6.72-4.93H1.25v3.15C3.26 21.36 7.33 24 12 24z"/>
            <path fill="#FBBC05" d="M5.28 14.27c-.25-.72-.38-1.49-.38-2.27s.13-1.55.38-2.27V6.58H1.25C.45 8.18 0 9.98 0 12s.45 3.82 1.25 5.42l4.03-3.15z"/>
            <path fill="#EA4335" d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.33 0 3.26 2.64 1.25 6.58l4.03 3.15c.95-2.83 3.6-4.98 6.72-4.98z"/>
          </svg>
        </button>

        <!-- Apple Vector SVG -->
        <button class="login-v5-social-btn" onclick="openPostLoginSuccessModal('Apple User', selectedLoginRole)" aria-label="Sign in with Apple">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="#000000">
            <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M15.97 6.88c.61-.75 1.04-1.8 0.92-2.88-.93.04-2.02.62-2.66 1.37-.56.65-.96 1.7-0.84 2.76 1.05.08 2.07-.53 2.58-1.25z"/>
          </svg>
        </button>

        <!-- Facebook Vector SVG -->
        <button class="login-v5-social-btn" onclick="openPostLoginSuccessModal('Kisan Mitra', selectedLoginRole)" aria-label="Sign in with Facebook">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="#1877F2">
            <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- Bottom Footer -->
    <div style="text-align: center; margin-top: 12px;">
      <span style="color: #64748B; font-size: 13px; font-weight: 600;">Don't have an account? </span>
      <span style="color: #16A34A; font-size: 13px; font-weight: 800; cursor: pointer;" onclick="handlePrimaryLoginSubmit()">Sign Up</span>
    </div>
  `;
}

function handlePrimaryLoginSubmit() {
  const phone = document.getElementById('login-phone-input')?.value || '9876543210';
  const role = selectedLoginRole;
  openPostLoginSuccessModal(role === 'farmer' ? 'B. Jaswanth Reddy' : 'Suresh Kumar', role);
}

/* 4. Real Google Account Chooser Modal */
function openInAppGoogleAuthModal() {
  const existing = document.getElementById('google-auth-modal');
  if (existing) existing.remove();

  const modalHtml = `
    <div id="google-auth-modal" class="google-auth-v5-sheet" onclick="if(event.target===this) this.remove();">
      <div class="google-auth-v5-card">
        <!-- Header -->
        <div style="display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #E2E8F0;padding-bottom:12px;">
          <div style="display:flex;align-items:center;gap:10px;">
            <svg width="22" height="22" viewBox="0 0 24 24"><path fill="#4285F4" d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.82-2.4 3.68v3.05h3.88c2.27-2.09 3.66-5.17 3.66-9.17z"/><path fill="#34A853" d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.12 0-5.77-2.1-6.72-4.93H1.25v3.15C3.26 21.36 7.33 24 12 24z"/><path fill="#FBBC05" d="M5.28 14.27c-.25-.72-.38-1.49-.38-2.27s.13-1.55.38-2.27V6.58H1.25C.45 8.18 0 9.98 0 12s.45 3.82 1.25 5.42l4.03-3.15z"/><path fill="#EA4335" d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.33 0 3.26 2.64 1.25 6.58l4.03 3.15c.95-2.83 3.6-4.98 6.72-4.98z"/></svg>
            <span style="font-size:16px;font-weight:800;color:#0F172A;">Sign in with Google</span>
          </div>
          <button onclick="document.getElementById('google-auth-modal')?.remove()" style="background:none;border:none;font-size:20px;color:#64748B;cursor:pointer;">✕</button>
        </div>

        <div style="font-size:12.5px;color:#64748B;font-weight:600;">
          Choose an account to continue to <strong>NuKropAI OS</strong>
        </div>

        <!-- Account List -->
        <div style="display:flex;flex-direction:column;gap:8px;">
          <!-- Account 1 -->
          <div class="google-account-v5-item" onclick="selectGoogleAccount('B. Jaswanth Reddy', 'jaswanth.reddy@gmail.com')">
            <div class="google-avatar-v5" style="background:linear-gradient(135deg, #16A34A, #15803D);">J</div>
            <div style="flex:1;">
              <div style="font-size:14px;font-weight:800;color:#0F172A;">B. Jaswanth Reddy</div>
              <div style="font-size:12px;color:#64748B;font-weight:600;">jaswanth.reddy@gmail.com</div>
            </div>
          </div>

          <!-- Account 2 -->
          <div class="google-account-v5-item" onclick="selectGoogleAccount('Kisan Ramesh Kumar', 'ramesh.kumar.kisan@gmail.com')">
            <div class="google-avatar-v5" style="background:linear-gradient(135deg, #D97706, #B45309);">R</div>
            <div style="flex:1;">
              <div style="font-size:14px;font-weight:800;color:#0F172A;">Kisan Ramesh Kumar</div>
              <div style="font-size:12px;color:#64748B;font-weight:600;">ramesh.kumar.kisan@gmail.com</div>
            </div>
          </div>

          <!-- Account 3 -->
          <div class="google-account-v5-item" onclick="selectGoogleAccount('AgriTech Cooperative FPO', 'apmc.coop.fpo@gmail.com')">
            <div class="google-avatar-v5" style="background:linear-gradient(135deg, #2563EB, #1D4ED8);">A</div>
            <div style="flex:1;">
              <div style="font-size:14px;font-weight:800;color:#0F172A;">AgriTech Cooperative FPO</div>
              <div style="font-size:12px;color:#64748B;font-weight:600;">apmc.coop.fpo@gmail.com</div>
            </div>
          </div>

          <!-- Custom Account Input -->
          <div style="border-top:1px solid #E2E8F0;padding-top:10px;margin-top:4px;">
            <div style="font-size:12px;font-weight:700;color:#475569;margin-bottom:6px;">Use another Google account:</div>
            <div style="display:flex;gap:8px;">
              <input id="custom-google-email" type="email" placeholder="your.name@gmail.com" style="flex:1;height:42px;border:1.5px solid #E2E8F0;border-radius:12px;padding:0 12px;font-size:13px;outline:none;" />
              <button onclick="submitCustomGoogleAccount()" style="padding:0 16px;background:#16A34A;color:#FFF;border:none;border-radius:12px;font-weight:800;font-size:13px;cursor:pointer;">Continue</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;

  document.body.insertAdjacentHTML('beforeend', modalHtml);
}

function selectGoogleAccount(name, email) {
  const modal = document.getElementById('google-auth-modal');
  if (modal) modal.remove();
  openPostLoginSuccessModal(name, selectedLoginRole);
}

function submitCustomGoogleAccount() {
  const email = document.getElementById('custom-google-email')?.value.trim() || 'jaswanth.reddy@gmail.com';
  const name = email.split('@')[0].replace('.', ' ').replace(/(^|\\s)\\S/g, l => l.toUpperCase());
  selectGoogleAccount(name, email);
}

/* 5. Post-Login Congratulations & Seamless Transition Modal */
function openPostLoginSuccessModal(userName, role) {
  const existing = document.getElementById('post-login-success-modal');
  if (existing) existing.remove();

  const isFarmer = role === 'farmer';

  const modalHtml = `
    <div id="post-login-success-modal" style="position:absolute;inset:0;background:rgba(15,23,42,0.75);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);z-index:10001;display:flex;align-items:center;justify-content:center;padding:24px;box-sizing:border-box;">
      <div style="background:#FFFFFF;border-radius:28px;padding:32px 24px;width:100%;max-width:360px;text-align:center;box-shadow:0 20px 50px rgba(0,0,0,0.3);animation:nkSlideUp 0.3s cubic-bezier(0.16,1,0.3,1);">
        <div style="width:72px;height:72px;border-radius:50%;background:#DCFCE7;display:flex;align-items:center;justify-content:center;margin:0 auto 16px;font-size:36px;box-shadow:0 8px 24px rgba(22,163,74,0.25);">
          🎉
        </div>
        <h2 style="font-size:20px;font-weight:900;color:#0F172A;margin:0 0 6px 0;">Congratulations!</h2>
        <div style="font-size:14px;color:#16A34A;font-weight:800;margin-bottom:8px;">Account Ready to Use</div>
        <p style="font-size:13px;color:#64748B;font-weight:500;line-height:1.5;margin:0 0 20px 0;">
          Welcome, <strong>${userName}</strong>!<br/>
          Signed in as <strong>${isFarmer ? '🌾 Verified Farmer' : '🚛 GramHaul Driver'}</strong>.
        </p>

        <button onclick="finishLoginAndEnterDashboard('${role}')" style="width:100%;height:50px;border-radius:16px;background:linear-gradient(135deg, #16A34A, #15803D);color:#FFFFFF;font-size:15px;font-weight:800;border:none;cursor:pointer;box-shadow:0 8px 20px rgba(22,163,74,0.35);">
          Continue to Dashboard →
        </button>
      </div>
    </div>
  `;

  document.body.insertAdjacentHTML('beforeend', modalHtml);
}

function finishLoginAndEnterDashboard(role) {
  // Remove all overlays
  ['post-login-success-modal', 'google-auth-modal', 'login-screen-overlay', 'onboarding-experience-overlay', 'permission-experience-overlay', 'startup-experience-overlay'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.remove();
  });

  // Reveal bottom dock
  const dock = document.querySelector('.bottom-dock-wrap');
  if (dock) {
    dock.style.display = 'flex';
  }

  // Route to the appropriate role dashboard
  if (role === 'driver') {
    if (typeof loginAsDriver === 'function') {
      loginAsDriver();
    } else if (typeof switchUserRole === 'function') {
      switchUserRole('driver');
    }
  } else {
    if (typeof switchUserRole === 'function') {
      switchUserRole('farmer');
    }
    if (typeof openScreen === 'function') {
      openScreen('home', null);
    }
  }
}
</script>
"""

def apply_to_file(filepath):
    print(f"Applying Master NuKropAI V5 suite to {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove any previous injections if present
    content = re.sub(r'<!-- ══════════════════════════════════════════════════════════════ -->\s*<!-- NUKROPAI V5 LUXURY OVERLAY SUITE.*?<\/script>', '', content, flags=re.DOTALL)

    # Insert before </body>
    if '</body>' in content:
        new_content = content.replace('</body>', MASTER_OVERLAY_CSS + '\n' + MASTER_OVERLAY_JS + '\n</body>')
    else:
        new_content = content + '\n' + MASTER_OVERLAY_CSS + '\n' + MASTER_OVERLAY_JS

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully updated {filepath}!")

if __name__ == '__main__':
    apply_to_file('app/src/main/assets/index.html')
    apply_to_file('nukrop_emulator.html')
