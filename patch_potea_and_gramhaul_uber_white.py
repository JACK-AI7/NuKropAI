import os, re, sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. LUXURY POTEA LOGIN & ONBOARDING / PERMISSIONS CSS & JS
MASTER_OVERLAY_CSS = """
<!-- ══════════════════════════════════════════════════════════════ -->
<!-- NUKROPAI V5 LUXURY OVERLAY SUITE: ONBOARDING, PERMS, POTEA LOGIN -->
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
/* POTEA LUXURY LOGIN SCREEN (WHITE THEME, OFFICIAL LOGO & ICONS) */
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

.login-v5-logo-container {
  width: 68px;
  height: 68px;
  border-radius: 22px;
  background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
  border: 1.5px solid #A7F3D0;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 24px rgba(22, 163, 74, 0.18);
  margin-bottom: 12px;
}

.login-v5-title {
  font-size: 27px;
  font-weight: 900;
  color: #0F172A;
  letter-spacing: -0.6px;
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
  gap: 8px;
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
  font-size: 12.5px;
  font-weight: 800;
  border-radius: 10px;
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

/* Social Login - 2 Balanced Luxury Buttons (Google & Apple) */
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
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.login-v5-social-btn {
  height: 52px;
  border: 1.5px solid #E2E8F0;
  border-radius: 16px;
  background: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
  font-size: 13.5px;
  font-weight: 800;
  color: #0F172A;
}
.login-v5-social-btn:active {
  transform: scale(0.96);
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

# 2. OVERLAY JAVASCRIPT CONTROLLER (POTEA LOGIN + REAL SVGS)
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
        <svg width="18" height="18" viewBox="0 0 64 64" fill="none">
          <path d="M54 10C36 10 20 22 14 38C12 43 11 48 10 54C16 53 21 52 26 50C42 44 54 28 54 10Z" fill="#22C55E"/>
          <path d="M10 54C22 42 34 30 50 14" stroke="#DCFCE7" stroke-width="4" stroke-linecap="round"/>
        </svg>
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
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
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

/* 3. Open Potea Luxury Login Screen (With Official NuKropAI Logo & Real Vector SVGs) */
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
    <!-- Top Header with Official NuKropAI Brand Logo -->
    <div class="login-v5-header">
      <div class="login-v5-logo-container">
        <svg width="44" height="44" viewBox="0 0 64 64" fill="none">
          <path d="M54 10C36 10 20 22 14 38C12 43 11 48 10 54C16 53 21 52 26 50C42 44 54 28 54 10Z" fill="url(#nkLogoGradMain)"/>
          <path d="M10 54C22 42 34 30 50 14" stroke="#DCFCE7" stroke-width="3.5" stroke-linecap="round"/>
          <defs>
            <linearGradient id="nkLogoGradMain" x1="10" y1="54" x2="54" y2="10" gradientUnits="userSpaceOnUse">
              <stop stop-color="#15803D"/>
              <stop offset="0.5" stop-color="#16A34A"/>
              <stop offset="1" stop-color="#22C55E"/>
            </linearGradient>
          </defs>
        </svg>
      </div>
      <h1 class="login-v5-title">NuKrop<span style="color: #16A34A;">AI</span></h1>
      <div class="login-v5-subtitle">Smart Agriculture · Powered by AI</div>
    </div>

    <!-- Center Form Area -->
    <div style="margin: 16px 0;">
      <!-- Role Switcher with High-Res SVGs -->
      <div class="login-v5-role-switch">
        <button class="login-v5-role-tab ${isFarmer ? 'active' : ''}" onclick="setLoginRole('farmer')">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          Farmer
        </button>
        <button class="login-v5-role-tab ${!isFarmer ? 'active' : ''}" onclick="setLoginRole('driver')">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>
          Truck Driver
        </button>
      </div>

      <!-- Auth Method Switcher with High-Res SVGs -->
      <div class="login-v5-method-switch">
        <button class="login-v5-method-tab ${isPhone ? 'active' : ''}" onclick="setLoginMethod('phone')">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"/><line x1="12" y1="18" x2="12.01" y2="18"/></svg>
          Mobile Number
        </button>
        <button class="login-v5-method-tab ${!isPhone ? 'active' : ''}" onclick="setLoginMethod('email')">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
          Email Address
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
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2" style="margin-right:2px;"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
          <input id="login-email-input" type="email" class="login-v5-input" placeholder="farmer@example.com" />
        </div>
      `}

      <div class="login-v5-input-box">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2" style="margin-right:2px;"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
        <input id="login-pass-input" type="password" class="login-v5-input" placeholder="Enter password or 4-digit PIN" />
        <button type="button" onclick="togglePasswordVisibility()" style="background:none;border:none;cursor:pointer;padding:0 4px;color:#64748B;display:flex;align-items:center;">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
        </button>
      </div>

      <!-- Checkboxes -->
      <div class="login-v5-check-row" onclick="toggleRememberCheckbox()">
        <div id="login-remember-cb" class="login-v5-checkbox ${rememberMe ? 'checked' : ''}">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="3.5"><polyline points="20 6 9 17 4 12"/></svg>
        </div>
        <div class="login-v5-check-label">Remember my login credentials</div>
      </div>

      <div class="login-v5-check-row" onclick="toggleTermsCheckbox()">
        <div id="login-terms-cb" class="login-v5-checkbox ${termsAccepted ? 'checked' : ''}">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="3.5"><polyline points="20 6 9 17 4 12"/></svg>
        </div>
        <div class="login-v5-check-label">
          I agree to NuKropAI <a href="javascript:void(0)">Privacy Policy</a> & <a href="javascript:void(0)">Terms of Service</a>
        </div>
      </div>

      <!-- Primary Action Button -->
      <button class="onboard-v5-primary-pill-btn" style="margin-top: 18px;" onclick="handlePrimaryLoginSubmit()">
        Sign In →
      </button>

      <!-- Social Login Section (Google and Apple Only - Facebook Removed) -->
      <div class="login-v5-divider">
        <div class="login-v5-divider-line"></div>
        <span class="login-v5-divider-text">or continue with</span>
        <div class="login-v5-divider-line"></div>
      </div>

      <!-- High-Res Vector SVG Social Buttons (Google & Apple Only) -->
      <div class="login-v5-social-grid">
        <!-- Google Real 4-Color SVG Button -->
        <button class="login-v5-social-btn" onclick="openInAppGoogleAuthModal()" aria-label="Sign in with Google">
          <svg width="22" height="22" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.82-2.4 3.68v3.05h3.88c2.27-2.09 3.66-5.17 3.66-9.17z"/>
            <path fill="#34A853" d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.12 0-5.77-2.1-6.72-4.93H1.25v3.15C3.26 21.36 7.33 24 12 24z"/>
            <path fill="#FBBC05" d="M5.28 14.27c-.25-.72-.38-1.49-.38-2.27s.13-1.55.38-2.27V6.58H1.25C.45 8.18 0 9.98 0 12s.45 3.82 1.25 5.42l4.03-3.15z"/>
            <path fill="#EA4335" d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.33 0 3.26 2.64 1.25 6.58l4.03 3.15c.95-2.83 3.6-4.98 6.72-4.98z"/>
          </svg>
          <span>Google</span>
        </button>

        <!-- Apple Vector SVG Button -->
        <button class="login-v5-social-btn" onclick="openPostLoginSuccessModal('Apple User', selectedLoginRole)" aria-label="Sign in with Apple">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="#000000">
            <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M15.97 6.88c.61-.75 1.04-1.8 0.92-2.88-.93.04-2.02.62-2.66 1.37-.56.65-.96 1.7-0.84 2.76 1.05.08 2.07-.53 2.58-1.25z"/>
          </svg>
          <span>Apple</span>
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

function selectGramhaulRideTier(tier) {
  const t1 = document.getElementById('gh-tier-1');
  const t2 = document.getElementById('gh-tier-2');
  const t3 = document.getElementById('gh-tier-3');
  const btn = document.querySelector('[onclick*="confirmGramhaulBooking"]');
  if (t1) {
    t1.style.background = tier === 1 ? '#F0FDF4' : '#FFFFFF';
    t1.style.borderColor = tier === 1 ? '#16A34A' : '#E2E8F0';
    t1.style.boxShadow = tier === 1 ? '0 4px 14px rgba(22,163,74,0.12)' : '0 2px 8px rgba(15,23,42,0.04)';
  }
  if (t2) {
    t2.style.background = tier === 2 ? '#F0FDF4' : '#FFFFFF';
    t2.style.borderColor = tier === 2 ? '#16A34A' : '#E2E8F0';
    t2.style.boxShadow = tier === 2 ? '0 4px 14px rgba(22,163,74,0.12)' : '0 2px 8px rgba(15,23,42,0.04)';
  }
  if (t3) {
    t3.style.background = tier === 3 ? '#F0FDF4' : '#FFFFFF';
    t3.style.borderColor = tier === 3 ? '#16A34A' : '#E2E8F0';
    t3.style.boxShadow = tier === 3 ? '0 4px 14px rgba(22,163,74,0.12)' : '0 2px 8px rgba(15,23,42,0.04)';
  }
  if (btn) {
    if (tier === 1) btn.innerHTML = '<span>Confirm Tata Ace · ₹450</span> <span>→</span>';
    if (tier === 2) btn.innerHTML = '<span>Confirm Mahindra Bolero · ₹650</span> <span>→</span>';
    if (tier === 3) btn.innerHTML = '<span>Confirm Eicher Pro 5T · ₹1,100</span> <span>→</span>';
  }
}

function confirmGramhaulBooking() {
  const sheet = document.getElementById('gh-active-trip-sheet');
  if (sheet) {
    sheet.scrollIntoView({ behavior: 'smooth' });
    sheet.style.boxShadow = '0 0 0 3px rgba(22, 163, 74, 0.4)';
    setTimeout(() => { sheet.style.boxShadow = '0 8px 30px rgba(15,23,42,0.08)'; }, 1500);
  }
}

</script>
"""

# 3. REDESIGNED GRAMHAUL LOGISTICS VIEW (UBER-STYLE WHITE THEME AS IN REFERENCE IMAGE)
NEW_GRAMHAUL_VIEW_CODE = """
  /* ── 2. GRAMHAUL FREIGHT POOL & ON-DEMAND TRANSPORT (UBER-STYLE WHITE THEME) ── */
  gramhaul: () => {
    const t = I18N[currentLang] || I18N.en;
    const isTe = currentLang === 'te';
    const isHi = currentLang === 'hi';

    const headerTitle = TL('GramHaul Logistics', 'గ్రామ్‌హాల్ లాజిస్టిక్స్', 'ग्रामहॉल लॉजिस्टिक्स');
    const headerSub = TL('On-Demand Farm-to-Mandi Fleet · 4.8 km', 'ఆన్-డిమాండ్ ఫార్మ్-టు-మండి రవాణా · 4.8 కి.మీ', 'ऑन-डिमांड खेत-से-मंडी ढुलाई');

    return `
    <div style="background:#F8FAF8;min-height:100%;padding-bottom:100px;font-family:-apple-system,BlinkMacSystemFont,'Plus Jakarta Sans','Inter',sans-serif;">
      <!-- 1. Header Bar -->
      <div style="background:#FFFFFF;padding:14px 18px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #EEF2F6;position:sticky;top:0;z-index:40;">
        <div style="display:flex;align-items:center;gap:12px;">
          <button onclick="openScreen('home',null);syncSideNav('btn-home')" style="background:#F1F5F9;border:none;cursor:pointer;width:36px;height:36px;border-radius:12px;display:flex;align-items:center;justify-content:center;color:#0F172A;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
          </button>
          <div>
            <div style="font-size:16px;font-weight:900;color:#0F172A;letter-spacing:-0.3px;">${headerTitle}</div>
            <div style="font-size:11px;color:#64748B;font-weight:600;">${headerSub}</div>
          </div>
        </div>
        <div style="display:flex;gap:6px;">
          <button onclick="openScreen('driver_dashboard',null)" style="background:#DCFCE7;border:1px solid #86EFAC;color:#15803D;padding:6px 12px;border-radius:12px;font-size:11.5px;font-weight:800;cursor:pointer;display:flex;align-items:center;gap:4px;">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>
            Driver
          </button>
        </div>
      </div>

      <div style="padding:16px 16px 0;">
        <!-- 2. Pickup & Drop Route Card (Uber-Style Floating Glass) -->
        <div style="background:#FFFFFF;border:1.5px solid #E2E8F0;border-radius:22px;padding:16px;box-shadow:0 4px 20px -2px rgba(15,23,42,0.06);margin-bottom:16px;">
          <!-- Pickup Row -->
          <div style="display:flex;align-items:center;gap:12px;">
            <div style="width:12px;height:12px;border-radius:50%;background:#94A3B8;flex-shrink:0;border:2px solid #E2E8F0;"></div>
            <div style="flex:1;">
              <div style="font-size:10.5px;font-weight:800;color:#94A3B8;text-transform:uppercase;letter-spacing:0.4px;">Pickup Location</div>
              <div style="font-size:13.5px;font-weight:800;color:#0F172A;">🌾 Ramesh Rao's Farm, Narsampet Rural</div>
            </div>
          </div>

          <!-- Divider Line with swap icon -->
          <div style="display:flex;align-items:center;margin:8px 0 8px 5px;position:relative;">
            <div style="width:2px;height:24px;background:#CBD5E1;"></div>
            <div style="flex:1;height:1px;background:#F1F5F9;margin-left:17px;"></div>
            <button style="position:absolute;right:0;width:32px;height:32px;border-radius:50%;background:#F8FAFC;border:1px solid #E2E8F0;display:flex;align-items:center;justify-content:center;color:#64748B;cursor:pointer;">
              ⇅
            </button>
          </div>

          <!-- Drop Row -->
          <div style="display:flex;align-items:center;gap:12px;">
            <div style="width:12px;height:12px;border-radius:50%;background:#16A34A;flex-shrink:0;box-shadow:0 0 0 3px #DCFCE7;"></div>
            <div style="flex:1;">
              <div style="font-size:10.5px;font-weight:800;color:#16A34A;text-transform:uppercase;letter-spacing:0.4px;">Drop Location</div>
              <div style="font-size:13.5px;font-weight:800;color:#0F172A;">📍 Warangal Enamamula APMC Yard (Gate 3)</div>
            </div>
          </div>

          <!-- Quick Location Shortcuts -->
          <div style="display:flex;gap:8px;margin-top:14px;padding-top:12px;border-top:1px solid #F1F5F9;overflow-x:auto;">
            <button style="background:#F8FAFC;border:1px solid #E2E8F0;padding:6px 12px;border-radius:10px;font-size:11.5px;font-weight:700;color:#475569;display:flex;align-items:center;gap:4px;white-space:nowrap;cursor:pointer;">
              🏠 My Farm (12 min)
            </button>
            <button style="background:#F0FDF4;border:1px solid #86EFAC;padding:6px 12px;border-radius:10px;font-size:11.5px;font-weight:800;color:#15803D;display:flex;align-items:center;gap:4px;white-space:nowrap;cursor:pointer;">
              🏢 Warangal APMC (4.8 km)
            </button>
            <button style="background:#F8FAFC;border:1px solid #E2E8F0;padding:6px 12px;border-radius:10px;font-size:11.5px;font-weight:700;color:#475569;display:flex;align-items:center;gap:4px;white-space:nowrap;cursor:pointer;">
              🏭 Bowenpally Mandi (128 km)
            </button>
          </div>
        </div>

        <!-- 3. Clean Light-Theme GPS Map Vector (Uber Navigation View) -->
        <div style="background:#FFFFFF;border:1.5px solid #E2E8F0;border-radius:22px;padding:14px;box-shadow:0 4px 16px -2px rgba(15,23,42,0.06);margin-bottom:18px;position:relative;overflow:hidden;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
            <div style="display:flex;align-items:center;gap:6px;font-size:12px;font-weight:800;color:#0F172A;">
              <span style="width:8px;height:8px;border-radius:50%;background:#16A34A;display:inline-block;box-shadow:0 0 8px #16A34A;"></span>
              Live GPS Fleet Telemetry
            </div>
            <div style="background:#DCFCE7;color:#15803D;font-size:10.5px;font-weight:800;padding:3px 8px;border-radius:8px;">
              3 Trucks Nearby
            </div>
          </div>

          <!-- Map Surface Visual -->
          <div style="height:170px;background:#F8FAFC;border-radius:16px;position:relative;overflow:hidden;border:1px solid #E2E8F0;">
            <!-- Subtle Grid Pattern -->
            <div style="position:absolute;inset:0;background-image:linear-gradient(#EEF2F6 1px, transparent 1px), linear-gradient(90deg, #EEF2F6 1px, transparent 1px);background-size:24px 24px;opacity:0.8;"></div>
            
            <!-- Road Paths SVG -->
            <svg style="position:absolute;inset:0;width:100%;height:100%;">
              <!-- Secondary Roads -->
              <path d="M 20 150 Q 150 90 260 140 T 400 60" stroke="#CBD5E1" stroke-width="8" fill="none" stroke-linecap="round"/>
              <!-- Active GPS Route (Vibrant Emerald Neon Laser) -->
              <path d="M 50 130 L 120 130 L 190 70 L 290 70 L 360 30" stroke="#16A34A" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M 50 130 L 120 130 L 190 70 L 290 70 L 360 30" stroke="#86EFAC" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>

            <!-- Origin Marker (Farm) -->
            <div style="position:absolute;left:40px;top:118px;display:flex;flex-direction:column;align-items:center;">
              <div style="background:#16A34A;color:#FFF;font-size:9px;font-weight:900;padding:2px 6px;border-radius:6px;box-shadow:0 2px 6px rgba(22,163,74,0.4);white-space:nowrap;margin-bottom:2px;">
                🌾 Your Farm
              </div>
              <div style="width:14px;height:14px;border-radius:50%;background:#FFFFFF;border:3px solid #16A34A;box-shadow:0 0 10px rgba(22,163,74,0.5);"></div>
            </div>

            <!-- Moving Truck Marker on Route -->
            <div style="position:absolute;left:180px;top:54px;display:flex;flex-direction:column;align-items:center;animation:pulse 2s infinite;">
              <div style="background:#0F172A;color:#FFF;font-size:9px;font-weight:800;padding:2px 6px;border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,0.25);white-space:nowrap;margin-bottom:2px;">
                🚛 Tata Ace (8 min)
              </div>
              <div style="width:26px;height:26px;border-radius:50%;background:#16A34A;display:flex;align-items:center;justify-content:center;color:#FFF;font-size:12px;box-shadow:0 4px 12px rgba(22,163,74,0.5);">
                🚚
              </div>
            </div>

            <!-- Destination Marker (APMC Mandi) -->
            <div style="position:absolute;right:30px;top:18px;display:flex;flex-direction:column;align-items:center;">
              <div style="background:#DC2626;color:#FFF;font-size:9px;font-weight:900;padding:2px 6px;border-radius:6px;box-shadow:0 2px 6px rgba(220,38,38,0.4);white-space:nowrap;margin-bottom:2px;">
                🏢 APMC Mandi
              </div>
              <div style="width:14px;height:14px;border-radius:50%;background:#FFFFFF;border:3px solid #DC2626;box-shadow:0 0 10px rgba(220,38,38,0.5);"></div>
            </div>

            <!-- Floating Recenter Button -->
            <button style="position:absolute;right:10px;bottom:10px;width:34px;height:34px;border-radius:10px;background:#FFFFFF;border:1px solid #CBD5E1;box-shadow:0 2px 8px rgba(0,0,0,0.1);display:flex;align-items:center;justify-content:center;color:#0F172A;cursor:pointer;">
              ⌖
            </button>
          </div>
        </div>

        <!-- 4. "Choose a Ride" Vehicle Tier Selector (Exact Uber/Lyft Structure in White Theme) -->
        <div style="margin-bottom:18px;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
            <h3 style="font-size:16px;font-weight:900;color:#0F172A;margin:0;letter-spacing:-0.3px;">
              ${TL('Available Farm Vehicles', 'అందుబాటులో ఉన్న వాహనాలు', 'उपलब्ध कृषि वाहन')}
            </h3>
            <span style="font-size:12px;color:#16A34A;font-weight:800;">Shared Pooling (Save 75%)</span>
          </div>

          <!-- Tier 1: Tata Ace 1.5 Ton (Standard - Active Selected) -->
          <div onclick="selectGramhaulRideTier(1)" id="gh-tier-1" style="background:#F0FDF4;border:2px solid #16A34A;border-radius:18px;padding:14px 16px;display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;cursor:pointer;box-shadow:0 4px 14px rgba(22,163,74,0.12);transition:all 0.2s ease;">
            <div style="display:flex;align-items:center;gap:14px;">
              <div style="width:48px;height:48px;border-radius:14px;background:#FFFFFF;border:1px solid #DCFCE7;display:flex;align-items:center;justify-content:center;font-size:24px;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
                🚚
              </div>
              <div>
                <div style="display:flex;align-items:center;gap:6px;">
                  <span style="font-size:14.5px;font-weight:900;color:#0F172A;">Tata Ace 1.5T</span>
                  <span style="background:#DCFCE7;color:#15803D;font-size:10px;font-weight:800;padding:2px 6px;border-radius:6px;">Popular</span>
                </div>
                <div style="font-size:12px;color:#64748B;font-weight:600;margin-top:2px;">
                  8 min away · 22/30 Bags Filled
                </div>
              </div>
            </div>
            <div style="text-align:right;">
              <div style="font-size:17px;font-weight:900;color:#15803D;">₹45 <span style="font-size:11px;color:#64748B;font-weight:600;">/bag</span></div>
              <div style="font-size:11px;color:#94A3B8;text-decoration:line-through;">₹180 /bag</div>
            </div>
          </div>

          <!-- Tier 2: Mahindra Bolero Maxi (Pickup Pro) -->
          <div onclick="selectGramhaulRideTier(2)" id="gh-tier-2" style="background:#FFFFFF;border:1.5px solid #E2E8F0;border-radius:18px;padding:14px 16px;display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;cursor:pointer;box-shadow:0 2px 8px rgba(15,23,42,0.04);transition:all 0.2s ease;">
            <div style="display:flex;align-items:center;gap:14px;">
              <div style="width:48px;height:48px;border-radius:14px;background:#F8FAFC;border:1px solid #E2E8F0;display:flex;align-items:center;justify-content:center;font-size:24px;">
                🛻
              </div>
              <div>
                <div style="font-size:14.5px;font-weight:900;color:#0F172A;">Mahindra Bolero 2.5T</div>
                <div style="font-size:12px;color:#64748B;font-weight:600;margin-top:2px;">
                  14 min away · 15/45 Bags Filled
                </div>
              </div>
            </div>
            <div style="text-align:right;">
              <div style="font-size:17px;font-weight:900;color:#0F172A;">₹65 <span style="font-size:11px;color:#64748B;font-weight:600;">/bag</span></div>
              <div style="font-size:11px;color:#94A3B8;text-decoration:line-through;">₹240 /bag</div>
            </div>
          </div>

          <!-- Tier 3: Eicher Pro 5T Express (Heavy Duty) -->
          <div onclick="selectGramhaulRideTier(3)" id="gh-tier-3" style="background:#FFFFFF;border:1.5px solid #E2E8F0;border-radius:18px;padding:14px 16px;display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;cursor:pointer;box-shadow:0 2px 8px rgba(15,23,42,0.04);transition:all 0.2s ease;">
            <div style="display:flex;align-items:center;gap:14px;">
              <div style="width:48px;height:48px;border-radius:14px;background:#F8FAFC;border:1px solid #E2E8F0;display:flex;align-items:center;justify-content:center;font-size:24px;">
                🚛
              </div>
              <div>
                <div style="font-size:14.5px;font-weight:900;color:#0F172A;">Eicher Pro 5T Express</div>
                <div style="font-size:12px;color:#64748B;font-weight:600;margin-top:2px;">
                  22 min away · Direct APMC Mandi
                </div>
              </div>
            </div>
            <div style="text-align:right;">
              <div style="font-size:17px;font-weight:900;color:#0F172A;">₹110 <span style="font-size:11px;color:#64748B;font-weight:600;">/bag</span></div>
              <div style="font-size:11px;color:#94A3B8;text-decoration:line-through;">₹380 /bag</div>
            </div>
          </div>

          <!-- Primary Booking Action Button -->
          <button onclick="confirmGramhaulBooking()" style="width:100%;height:54px;border-radius:18px;background:linear-gradient(135deg, #16A34A, #15803D);color:#FFFFFF;font-size:16px;font-weight:900;border:none;cursor:pointer;box-shadow:0 8px 24px rgba(22,163,74,0.35);display:flex;align-items:center;justify-content:center;gap:8px;transition:all 0.2s ease;">
            <span>Confirm Tata Ace · ₹450</span>
            <span>→</span>
          </button>
        </div>

        <!-- 5. Active Trip & Live Driver Tracker Drawer (Exact Screen 2 of Reference Image) -->
        <div id="gh-active-trip-sheet" style="background:#FFFFFF;border:1.5px solid #E2E8F0;border-radius:24px;padding:18px 16px;box-shadow:0 8px 30px rgba(15,23,42,0.08);margin-top:16px;">
          <!-- Driver Status Green Pill Header -->
          <div style="background:#16A34A;color:#FFFFFF;border-radius:14px;padding:10px 14px;display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;box-shadow:0 4px 12px rgba(22,163,74,0.25);">
            <div style="display:flex;align-items:center;gap:8px;font-size:13.5px;font-weight:800;">
              <span>🚚</span>
              <span>Your driver is on the way</span>
            </div>
            <div style="background:rgba(255,255,255,0.25);padding:3px 8px;border-radius:8px;font-size:11.5px;font-weight:900;">
              8 min
            </div>
          </div>

          <!-- Driver Profile & Vehicle Row -->
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;">
            <div style="display:flex;align-items:center;gap:12px;">
              <div style="width:48px;height:48px;border-radius:50%;background:linear-gradient(135deg, #D97706, #B45309);display:flex;align-items:center;justify-content:center;color:#FFF;font-size:18px;font-weight:900;box-shadow:0 4px 12px rgba(217,119,6,0.3);">
                S
              </div>
              <div>
                <div style="display:flex;align-items:center;gap:6px;">
                  <span style="font-size:15px;font-weight:900;color:#0F172A;">Suresh Yadav</span>
                  <span style="color:#D97706;font-size:12px;font-weight:800;">★ 4.9</span>
                </div>
                <div style="font-size:12px;color:#64748B;font-weight:600;">Tata Ace 1.5T · 142 trips</div>
              </div>
            </div>
            <div style="background:#F1F5F9;border:1px solid #E2E8F0;border-radius:8px;padding:4px 8px;font-size:11px;font-weight:800;color:#0F172A;letter-spacing:0.5px;">
              TS 03 UB 4491
            </div>
          </div>

          <!-- 4 Quick Circular Action Buttons -->
          <div style="display:grid;grid-template-columns:repeat(4, 1fr);gap:10px;margin-bottom:16px;">
            <button onclick="alert('Calling Driver Suresh Yadav (+91 98765 44910)...')" style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:14px;padding:10px 0;display:flex;flex-direction:column;align-items:center;gap:4px;cursor:pointer;">
              <span style="font-size:16px;">📞</span>
              <span style="font-size:10.5px;font-weight:800;color:#475569;">Call</span>
            </button>
            <button onclick="alert('Opening in-app chat with driver...')" style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:14px;padding:10px 0;display:flex;flex-direction:column;align-items:center;gap:4px;cursor:pointer;">
              <span style="font-size:16px;">💬</span>
              <span style="font-size:10.5px;font-weight:800;color:#475569;">Message</span>
            </button>
            <button onclick="alert('Live GPS link copied to share on WhatsApp!')" style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:14px;padding:10px 0;display:flex;flex-direction:column;align-items:center;gap:4px;cursor:pointer;">
              <span style="font-size:16px;">🔗</span>
              <span style="font-size:10.5px;font-weight:800;color:#475569;">Share</span>
            </button>
            <button onclick="if(confirm('Cancel this freight booking?')) alert('Trip cancelled.');" style="background:#FEF2F2;border:1px solid #FECACA;border-radius:14px;padding:10px 0;display:flex;flex-direction:column;align-items:center;gap:4px;cursor:pointer;">
              <span style="font-size:16px;color:#DC2626;">✕</span>
              <span style="font-size:10.5px;font-weight:800;color:#DC2626;">Cancel</span>
            </button>
          </div>

          <!-- Journey Progress Timeline -->
          <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:16px;padding:12px 14px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;font-size:11.5px;font-weight:800;">
              <span style="color:#16A34A;">Pickup in 8 min</span>
              <span style="color:#64748B;">Arrive Mandi by 4:45 PM</span>
            </div>
            <div style="height:6px;background:#E2E8F0;border-radius:6px;overflow:hidden;">
              <div style="width:35%;height:100%;background:#16A34A;border-radius:6px;"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
    `;
  },
"""

def replace_gramhaul_in_file(filepath):
    print(f"Updating GramHaul view and master suite in {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace the gramhaul view function in APP_VIEWS
    pattern = r'gramhaul\s*:\s*\(\)\s*=>\s*\{.*?(?=\n\s*\/\* ── [3-9]\.|\n\s*agristack\s*:\s*\(\)\s*=>)'
    if re.search(pattern, content, flags=re.DOTALL):
        content = re.sub(pattern, NEW_GRAMHAUL_VIEW_CODE.strip(), content, count=1, flags=re.DOTALL)
        print("Replaced gramhaul view successfully!")
    else:
        print("Warning: regex didn't match gramhaul block, attempting surgical replacement")
        start = content.find('gramhaul: () =>')
        if start != -1:
            end = content.find('/* ── 5. FARMER ID', start)
            if end == -1:
                end = content.find('agristack:', start)
            if end != -1:
                content = content[:start] + NEW_GRAMHAUL_VIEW_CODE.strip() + '\n\n  ' + content[end:]
                print("Surgically replaced gramhaul block!")

    # 2. Replace Master Overlay CSS and JS
    content = re.sub(r'<!-- ══════════════════════════════════════════════════════════════ -->\s*<!-- NUKROPAI V5 LUXURY OVERLAY SUITE.*?<\/script>', '', content, flags=re.DOTALL)
    if '</body>' in content:
        content = content.replace('</body>', MASTER_OVERLAY_CSS + '\n' + MASTER_OVERLAY_JS + '\n</body>')
    else:
        content = content + '\n' + MASTER_OVERLAY_CSS + '\n' + MASTER_OVERLAY_JS

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Saved {filepath}!")

if __name__ == '__main__':
    replace_gramhaul_in_file('app/src/main/assets/index.html')
    replace_gramhaul_in_file('nukrop_emulator.html')
