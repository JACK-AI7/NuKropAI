import sys, os, re

sys.stdout.reconfigure(encoding='utf-8')

unified_module = r"""
<style>
/* ══════════════════════════════════════════════════════
   FULL-BLEED ONBOARDING & PERMISSION DESIGN SYSTEM
══════════════════════════════════════════════════════ */
#onboarding-experience-overlay,
#permission-experience-overlay,
#login-screen-overlay {
  position: fixed !important;
  inset: 0 !important;
  width: 100% !important;
  height: 100% !important;
  z-index: 999999 !important;
  display: flex !important;
  flex-direction: column !important;
  font-family: inherit !important;
  overflow: hidden !important;
  background: #0F172A !important;
}

#login-screen-overlay {
  background: #FFFFFF !important;
  overflow-y: auto !important;
}

.ob-carousel-slide {
  position: absolute !important;
  inset: 0 !important;
  width: 100% !important;
  height: 100% !important;
  opacity: 0 !important;
  visibility: hidden !important;
  pointer-events: none !important;
  transition: opacity 0.35s cubic-bezier(0.4, 0, 0.2, 1), transform 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important;
  transform: scale(1.02) !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: space-between !important;
  background-size: cover !important;
  background-position: center top !important;
  background-repeat: no-repeat !important;
  z-index: 1 !important;
}

.ob-carousel-slide.active {
  opacity: 1 !important;
  visibility: visible !important;
  pointer-events: auto !important;
  transform: scale(1) !important;
  z-index: 10 !important;
}

.ob-top-hud {
  position: relative !important;
  z-index: 35 !important;
  padding: 44px 20px 0 !important;
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
}

.ob-badge-pill {
  background: rgba(0, 0, 0, 0.45) !important;
  backdrop-filter: blur(12px) !important;
  border: 1px solid rgba(255, 255, 255, 0.25) !important;
  border-radius: 20px !important;
  padding: 5px 12px !important;
  font-size: 11px !important;
  font-weight: 800 !important;
  color: #FFFFFF !important;
  display: flex !important;
  align-items: center !important;
  gap: 6px !important;
  letter-spacing: 0.3px !important;
}

.ob-skip-btn {
  background: rgba(255, 255, 255, 0.92) !important;
  backdrop-filter: blur(12px) !important;
  border: 1px solid rgba(255, 255, 255, 0.6) !important;
  border-radius: 20px !important;
  padding: 6px 16px !important;
  font-size: 12px !important;
  font-weight: 800 !important;
  color: #15803D !important;
  cursor: pointer !important;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.18) !important;
  transition: transform 0.15s ease !important;
}
.ob-skip-btn:active {
  transform: scale(0.92) !important;
}

.ob-gradient-vignette {
  position: absolute !important;
  inset: 0 !important;
  background: linear-gradient(180deg, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0.02) 28%, rgba(0,0,0,0.15) 60%, rgba(0,0,0,0.88) 100%) !important;
  pointer-events: none !important;
}

.ob-sheet-card {
  position: absolute !important;
  bottom: 0 !important;
  left: 0 !important;
  right: 0 !important;
  z-index: 25 !important;
  background: #FFFFFF !important;
  border-radius: 32px 32px 0 0 !important;
  padding: 24px 22px 26px !important;
  box-shadow: 0 -12px 40px rgba(0,0,0,0.25) !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 12px !important;
  min-height: 215px !important;
  justify-content: space-between !important;
}

.ob-indicator-pill {
  height: 6px !important;
  border-radius: 6px !important;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
}
.ob-indicator-pill.active {
  width: 24px !important;
  background: #16A34A !important;
}
.ob-indicator-pill.inactive {
  width: 6px !important;
  background: #CBD5E1 !important;
}

.ob-fab-btn {
  width: 52px !important;
  height: 52px !important;
  border-radius: 50% !important;
  background: linear-gradient(135deg, #16A34A, #15803D) !important;
  color: #FFFFFF !important;
  border: none !important;
  cursor: pointer !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  font-size: 20px !important;
  font-weight: 900 !important;
  box-shadow: 0 6px 20px rgba(22, 163, 74, 0.45) !important;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
}
.ob-fab-btn:active {
  transform: scale(0.92) !important;
}
.ob-fab-btn.expanded {
  width: auto !important;
  padding: 0 22px !important;
  border-radius: 26px !important;
  font-size: 14px !important;
  font-weight: 900 !important;
  gap: 6px !important;
}
</style>

<script>
// ══════════════════════════════════════════════════════
// MASTER FULL-BLEED ONBOARDING & FULL-BLEED PERMISSIONS
// ══════════════════════════════════════════════════════
window.currentOnboardingSlide = 0;
window.currentPermissionSlide = 0;

const ONBOARDING_SLIDES_DATA = [
  {
    image: 'images/onboard_crop_doctor.jpg',
    badge: '🌿 AI CROP DOCTOR',
    title: 'Instant AI Leaf Diagnostics',
    description: 'Scan crop leaves in milliseconds to identify pests, fungal blights, and nutrient deficiencies with expert AI treatment prescriptions.'
  },
  {
    image: 'images/onboard_mandi_prices.jpg',
    badge: '📊 APMC COMMODITY ARBITRAGE',
    title: 'Live APMC Mandi Rates',
    description: 'Track real-time prices across 2,400+ mandis with AI-powered maximum profit forecasts to sell your harvest at peak market value.'
  },
  {
    image: 'images/onboard_farm_logistics.jpg',
    badge: '🚚 GRAMHAUL LOGISTICS',
    title: 'Farm-to-Mandi Direct Transport',
    description: 'Book verified mini-trucks and heavy transport directly from your farm gate with transparent per-km rates and live GPS tracking.'
  },
  {
    image: 'images/onboard_agristack_tech.jpg',
    badge: '📜 AGRISTACK & PM-KISAN',
    title: 'AgriStack Passbook & Subsidies',
    description: 'Access digital RoR 1-B land records, Kisan Credit Card loans, and direct government DBT subsidy disbursements without middlemen.'
  },
  {
    image: 'images/onboard_ai_voice_weather.jpg',
    badge: '🎙 MULTILINGUAL AI AGRONOMIST',
    title: 'Voice Agronomist & Spray Radar',
    description: 'Speak in Telugu, Hindi, Tamil, or Kannada to receive hyper-local micro-weather forecasts, rainfall radar, and optimal spray timings.'
  },
  {
    image: 'images/onboard_community_machinery.jpg',
    badge: '🤝 KISAN COMMUNITY & CHC',
    title: 'Kisan Community & Machinery Sharing',
    description: 'Connect with progressive farmers across India and rent modern tractors and combine harvesters at affordable cooperative rates.'
  }
];

const PERMISSIONS_SLIDES_DATA = [
  {
    type: 'camera',
    image: 'images/perm_bg_camera.jpg',
    badge: '📸 HARDWARE SENSOR (1/3)',
    title: 'Camera & Leaf Diagnostics',
    description: 'Allow camera access so NuKropAI can instantly scan diseased crop leaves, detect pests, and provide real-time diagnostic prescriptions.',
    btnText: 'Allow Camera Access',
    action: () => requestAppHardwarePermission('camera')
  },
  {
    type: 'location',
    image: 'images/perm_bg_location.jpg',
    badge: '📍 GPS TELEMETRY (2/3)',
    title: 'GPS Location & Mandi Radar',
    description: 'Allow precise location to detect your nearest APMC mandi commodity prices, hyper-local farm weather forecasts, and GramHaul transport trucks.',
    btnText: 'Allow GPS Location',
    action: () => requestAppHardwarePermission('location')
  },
  {
    type: 'notification',
    image: 'images/perm_bg_notification.jpg',
    badge: '🔔 EMERGENCY ALERTS (3/3)',
    title: 'Pest Warnings & Price Spikes',
    description: 'Enable instant push advisories for incoming rainstorms, emergency locust outbreaks, and peak APMC mandi selling prices.',
    btnText: 'Enable Notifications ✓',
    action: () => requestAppHardwarePermission('notification')
  }
];

function openOnboardingFlow(isManual = false) {
  window.currentOnboardingSlide = 0;
  if (typeof NuKropAnalytics !== 'undefined' && NuKropAnalytics.track) NuKropAnalytics.track('onboarding_started', { manualTrigger: isManual });

  const chassis = document.querySelector('.phone-chassis') || document.body;
  
  // Clean all overlays
  ['onboarding-experience-overlay', 'permission-experience-overlay', 'startup-experience-overlay', 'global-push-toast', 'login-screen-overlay'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.remove();
  });

  const dock = document.querySelector('.bottom-dock-wrap');
  if (dock) dock.style.display = 'none';

  const overlayHtml = `
    <div id="onboarding-experience-overlay">
      <div id="ob-slides-viewport">
        ${ONBOARDING_SLIDES_DATA.map((slide, idx) => `
          <div id="ob-slide-${idx}" class="ob-carousel-slide ${idx === 0 ? 'active' : ''}" style="background-image: url('${slide.image}');">
            <div class="ob-gradient-vignette"></div>
            
            <!-- Top HUD: Perfectly Aligned Status Area (Image 1 Style) -->
            <div class="ob-top-hud">
              <div class="ob-badge-pill">
                <span>🍃</span>
                <span>NuKropAI OS</span>
              </div>
              <button onclick="openPermissionsFullBleedFlow()" class="ob-skip-btn">
                Skip
              </button>
            </div>

            <!-- Bottom Floating Sheet Card (Image 1 Style) -->
            <div class="ob-sheet-card">
              <div>
                <div style="display:inline-block;background:#DCFCE7;color:#15803D;font-size:10.5px;font-weight:900;padding:3px 10px;border-radius:10px;border:1px solid #86EFAC;margin-bottom:8px;letter-spacing:0.3px;">
                  ${slide.badge}
                </div>
                <div style="font-size:22px;font-weight:900;color:#0F172A;line-height:1.2;letter-spacing:-0.4px;">
                  ${slide.title}
                </div>
                <div style="font-size:13px;color:#475569;margin-top:8px;line-height:1.45;font-weight:500;">
                  ${slide.description}
                </div>
              </div>

              <!-- Bottom Row: Elongated Active Indicator & Green FAB Arrow -->
              <div style="display:flex;justify-content:space-between;align-items:center;padding-top:8px;margin-top:auto;">
                <!-- 6-Dot Indicator Pill -->
                <div style="display:flex;align-items:center;gap:6px;">
                  ${ONBOARDING_SLIDES_DATA.map((_, dotIdx) => `
                    <div id="ob-dot-${idx}-${dotIdx}" class="ob-indicator-pill ${dotIdx === idx ? 'active' : 'inactive'}"></div>
                  `).join('')}
                </div>

                <!-- Circular Emerald Arrow FAB Button -->
                <button onclick="advanceOnboardingSlide(${idx + 1})" class="ob-fab-btn ${idx === ONBOARDING_SLIDES_DATA.length - 1 ? 'expanded' : ''}">
                  ${idx === ONBOARDING_SLIDES_DATA.length - 1 ? '<span>Get Started</span> <span style="font-size:18px;">✓</span>' : '<span>→</span>'}
                </button>
              </div>
            </div>

          </div>
        `).join('')}
      </div>
    </div>
  `;

  chassis.insertAdjacentHTML('beforeend', overlayHtml);
}

function advanceOnboardingSlide(nextIndex) {
  if (nextIndex >= ONBOARDING_SLIDES_DATA.length) {
    openPermissionsFullBleedFlow();
    return;
  }

  for (let i = 0; i < ONBOARDING_SLIDES_DATA.length; i++) {
    const s = document.getElementById(`ob-slide-${i}`);
    if (s) {
      if (i === nextIndex) {
        s.classList.add('active');
      } else {
        s.classList.remove('active');
      }
    }
  }

  window.currentOnboardingSlide = nextIndex;
  if (typeof NuKropAnalytics !== 'undefined' && NuKropAnalytics.track) NuKropAnalytics.track('onboarding_slide_viewed', { slideIndex: nextIndex });
}

function skipOnboarding() {
  openPermissionsFullBleedFlow();
}

// ══════════════════════════════════════════════════════
// FULL-BLEED 3-STEP PERMISSIONS FLOW (Exact Onboarding Style)
// ══════════════════════════════════════════════════════
function openPermissionsFullBleedFlow() {
  window.currentPermissionSlide = 0;

  const existingOb = document.getElementById('onboarding-experience-overlay');
  if (existingOb) existingOb.remove();
  const existingPerm = document.getElementById('permission-experience-overlay');
  if (existingPerm) existingPerm.remove();

  const dock = document.querySelector('.bottom-dock-wrap');
  if (dock) dock.style.display = 'none';

  const chassis = document.querySelector('.phone-chassis') || document.body;

  const permHtml = `
    <div id="permission-experience-overlay">
      <div id="perm-slides-viewport" style="position:relative;width:100%;height:100%;overflow:hidden;">
        ${PERMISSIONS_SLIDES_DATA.map((perm, idx) => `
          <div id="perm-slide-${idx}" class="ob-carousel-slide ${idx === 0 ? 'active' : ''}" style="background-image: url('${perm.image}');">
            <div class="ob-gradient-vignette"></div>
            
            <!-- Top HUD -->
            <div class="ob-top-hud">
              <div class="ob-badge-pill">
                <span>🔒</span>
                <span>Permissions (${idx + 1}/3)</span>
              </div>
              <button onclick="renderLoginScreen()" class="ob-skip-btn">
                Skip
              </button>
            </div>

            <!-- Bottom Floating Sheet Card (Exact Same Onboarding Style) -->
            <div class="ob-sheet-card">
              <div>
                <div style="display:inline-block;background:#DCFCE7;color:#15803D;font-size:10.5px;font-weight:900;padding:3px 10px;border-radius:10px;border:1px solid #86EFAC;margin-bottom:8px;letter-spacing:0.3px;">
                  ${perm.badge}
                </div>
                <div style="font-size:22px;font-weight:900;color:#0F172A;line-height:1.2;letter-spacing:-0.4px;">
                  ${perm.title}
                </div>
                <div style="font-size:13px;color:#475569;margin-top:8px;line-height:1.45;font-weight:500;">
                  ${perm.description}
                </div>
              </div>

              <!-- Bottom Controls -->
              <div style="display:flex;justify-content:space-between;align-items:center;padding-top:8px;margin-top:auto;">
                <!-- 3-Dot Indicator Pill -->
                <div style="display:flex;align-items:center;gap:6px;">
                  ${PERMISSIONS_SLIDES_DATA.map((_, dotIdx) => `
                    <div class="ob-indicator-pill ${dotIdx === idx ? 'active' : 'inactive'}"></div>
                  `).join('')}
                </div>

                <!-- Action Button -->
                <button onclick="handlePermissionSlideAction(${idx})" class="ob-fab-btn expanded">
                  <span>${perm.btnText}</span>
                  <span style="font-size:16px;">→</span>
                </button>
              </div>
            </div>

          </div>
        `).join('')}
      </div>
    </div>
  `;

  chassis.insertAdjacentHTML('beforeend', permHtml);
}

function handlePermissionSlideAction(slideIdx) {
  const perm = PERMISSIONS_SLIDES_DATA[slideIdx];
  if (perm && perm.action) perm.action();

  const nextIdx = slideIdx + 1;
  if (nextIdx >= PERMISSIONS_SLIDES_DATA.length) {
    // All 3 permissions completed -> navigate to Login
    localStorage.setItem('nukrop_permissions_granted', 'true');
    localStorage.setItem('onboarding_completed', 'true');
    const overlay = document.getElementById('permission-experience-overlay');
    if (overlay) overlay.remove();
    renderLoginScreen();
    return;
  }

  // Advance to next permission slide
  for (let i = 0; i < PERMISSIONS_SLIDES_DATA.length; i++) {
    const s = document.getElementById(`perm-slide-${i}`);
    if (s) {
      if (i === nextIdx) {
        s.classList.add('active');
      } else {
        s.classList.remove('active');
      }
    }
  }
  window.currentPermissionSlide = nextIdx;
}

function requestAppHardwarePermission(type) {
  if (type === 'camera') {
    if (window.AndroidBridge && window.AndroidBridge.requestCameraPermission) {
      window.AndroidBridge.requestCameraPermission();
    } else if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ video: true }).catch(() => {});
    }
    window.appPermissionsState.camera = true;
  } else if (type === 'location') {
    if (window.AndroidBridge && window.AndroidBridge.requestLocationPermission) {
      window.AndroidBridge.requestLocationPermission();
    } else if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(() => {}, () => {});
    }
    window.appPermissionsState.location = true;
  } else if (type === 'notification') {
    if (window.Notification && Notification.requestPermission) {
      Notification.requestPermission().catch(() => {});
    }
    window.appPermissionsState.notification = true;
  }
}

// ══════════════════════════════════════════════════════
// POTEA-STYLE AUTHENTICATION & LOGIN (Image 2 Style)
// (With Zero Bottom Navbar & Real SVG Brand Logos)
// ══════════════════════════════════════════════════════
window.loginInputType = 'phone';

function toggleLoginInputType(type) {
  window.loginInputType = type;
  const phoneRow = document.getElementById('auth-phone-row');
  const emailRow = document.getElementById('auth-email-row');
  const btnPhone = document.getElementById('toggle-btn-phone');
  const btnEmail = document.getElementById('toggle-btn-email');

  if (type === 'phone') {
    if (phoneRow) phoneRow.style.display = 'flex';
    if (emailRow) emailRow.style.display = 'none';
    if (btnPhone) {
      btnPhone.style.background = '#FFFFFF';
      btnPhone.style.color = '#15803D';
      btnPhone.style.boxShadow = '0 2px 8px rgba(0,0,0,0.08)';
    }
    if (btnEmail) {
      btnEmail.style.background = 'transparent';
      btnEmail.style.color = '#64748B';
      btnEmail.style.boxShadow = 'none';
    }
  } else {
    if (phoneRow) phoneRow.style.display = 'none';
    if (emailRow) emailRow.style.display = 'flex';
    if (btnEmail) {
      btnEmail.style.background = '#FFFFFF';
      btnEmail.style.color = '#15803D';
      btnEmail.style.boxShadow = '0 2px 8px rgba(0,0,0,0.08)';
    }
    if (btnPhone) {
      btnPhone.style.background = 'transparent';
      btnPhone.style.color = '#64748B';
      btnPhone.style.boxShadow = 'none';
    }
  }
}

function togglePasswordVisibility() {
  const pwdInput = document.getElementById('auth-pwd-input');
  const eyeIcon = document.getElementById('pwd-eye-icon');
  if (!pwdInput) return;

  if (pwdInput.type === 'password') {
    pwdInput.type = 'text';
    if (eyeIcon) eyeIcon.innerText = '🙈';
  } else {
    pwdInput.type = 'password';
    if (eyeIcon) eyeIcon.innerText = '👁';
  }
}

function renderLoginScreen() {
  // Completely hide bottom dock during login
  const dock = document.querySelector('.bottom-dock-wrap');
  if (dock) dock.style.display = 'none';

  let overlay = document.getElementById('login-screen-overlay');
  if (!overlay) {
    const chassis = document.querySelector('.phone-chassis') || document.body;
    overlay = document.createElement('div');
    overlay.id = 'login-screen-overlay';
    overlay.style.cssText = 'position:fixed;inset:0;background:#FFFFFF;z-index:999999;display:flex;flex-direction:column;font-family:inherit;overflow-y:auto;';
    chassis.appendChild(overlay);
  }

  window.authFormMode = window.authFormMode || 'signin';
  window.authUserRole = window.authUserRole || 'farmer';
  const currentAuthMode = window.authFormMode;
  const currentAuthRole = window.authUserRole;
  if (typeof NuKropAnalytics !== 'undefined' && NuKropAnalytics.track) NuKropAnalytics.track('onboarding_login_screen_viewed', { mode: currentAuthMode, role: currentAuthRole });
  const isSignUp = currentAuthMode === 'signup';
  const authUserRole = currentAuthRole;

  const rememberedPhone = (localStorage.getItem('nukrop_user_phone') || '9876543210');
  const rememberedEmail = (localStorage.getItem('nukrop_remembered_email') || localStorage.getItem('nukrop_user_email') || 'jaswanth.reddy.farmer@gmail.com');

  overlay.innerHTML = `
    <div style="width:100%;min-height:100%;display:flex;flex-direction:column;justify-content:space-between;box-sizing:border-box;background:#FFFFFF;color:#0F172A;position:relative;padding:36px 20px 24px;">
      
      <!-- Top Branding Section (Potea Green Leaf Emblem) -->
      <div style="display:flex;flex-direction:column;align-items:center;text-align:center;margin-top:8px;">
        <div style="width:64px;height:64px;border-radius:50%;background:linear-gradient(135deg, #DCFCE7 0%, #F0FDF4 100%);border:2px solid #86EFAC;display:flex;align-items:center;justify-content:center;box-shadow:0 8px 24px rgba(0,168,107,0.16);margin-bottom:8px;">
          ${typeof get4kLeafSvg === 'function' ? get4kLeafSvg(40) : '<span style="font-size:26px;">🍃</span>'}
        </div>
        <div style="font-size:25px;font-weight:900;color:#0F172A;letter-spacing:-0.5px;line-height:1.1;">
          NuKrop<span style="color:#00A86B;">AI</span>
        </div>
        <div style="font-size:12px;color:#64748B;font-weight:600;margin-top:2px;">
          ${authUserRole === 'driver' ? 'GramHaul Driver Partner Portal' : 'Smart Agriculture · Powered by AI'}
        </div>
      </div>

      <!-- Segmented Mode Switcher: [ Farmer ] [ Truck Driver ] -->
      <div style="background:#F1F5F9;border-radius:14px;padding:4px;display:flex;align-items:center;gap:4px;margin-top:16px;">
        <button onclick="setAuthUserRole('farmer')" style="flex:1;background:${authUserRole === 'farmer' ? '#16A34A' : 'transparent'};color:${authUserRole === 'farmer' ? '#FFFFFF' : '#475569'};border:none;border-radius:10px;padding:9px 0;font-size:13px;font-weight:800;cursor:pointer;transition:all 0.15s ease;display:flex;align-items:center;justify-content:center;gap:6px;">
          <span>🧑‍🌾</span><span>Farmer</span>
        </button>
        <button onclick="setAuthUserRole('driver')" style="flex:1;background:${authUserRole === 'driver' ? '#0F172A' : 'transparent'};color:${authUserRole === 'driver' ? '#FFFFFF' : '#475569'};border:none;border-radius:10px;padding:9px 0;font-size:13px;font-weight:800;cursor:pointer;transition:all 0.15s ease;display:flex;align-items:center;justify-content:center;gap:6px;">
          <span>🚚</span><span>Truck Driver</span>
        </button>
      </div>

      <!-- Auth Sub-mode: [ Mobile Number ] [ Email ] Toggle -->
      <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px;padding:3px;display:flex;align-items:center;gap:3px;margin-top:12px;">
        <button id="toggle-btn-phone" onclick="toggleLoginInputType('phone')" style="flex:1;background:#FFFFFF;color:#15803D;border:none;border-radius:9px;padding:8px 0;font-size:12px;font-weight:800;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
          🇮🇳 Mobile Number
        </button>
        <button id="toggle-btn-email" onclick="toggleLoginInputType('email')" style="flex:1;background:transparent;color:#64748B;border:none;border-radius:9px;padding:8px 0;font-size:12px;font-weight:700;cursor:pointer;">
          ✉ Email Address
        </button>
      </div>

      <!-- Input Form -->
      <div style="display:flex;flex-direction:column;gap:12px;margin-top:14px;">
        
        <!-- Mobile Input Row (Image 2 Potea Style with +91 Flag) -->
        <div id="auth-phone-row" style="display:flex;align-items:center;gap:10px;background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:16px;padding:4px 14px;">
          <div style="display:flex;align-items:center;gap:4px;padding-right:10px;border-right:1px solid #CBD5E1;color:#0F172A;font-weight:800;font-size:13.5px;">
            <span>🇮🇳</span>
            <span>+91</span>
          </div>
          <input id="auth-phone-input" type="tel" maxlength="10" placeholder="98765 43210" value="${rememberedPhone}" style="flex:1;border:none;background:transparent;padding:12px 0;font-size:14px;font-weight:700;color:#0F172A;outline:none;" />
        </div>

        <!-- Email Input Row (Alternative) -->
        <div id="auth-email-row" style="display:none;align-items:center;gap:10px;background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:16px;padding:4px 14px;">
          <span style="font-size:16px;color:#64748B;">✉</span>
          <input id="auth-email-input" type="email" placeholder="kisan.farmer@gmail.com" value="${rememberedEmail}" style="flex:1;border:none;background:transparent;padding:12px 0;font-size:13.5px;font-weight:700;color:#0F172A;outline:none;" />
        </div>

        <!-- Password / Security PIN Input -->
        <div style="display:flex;align-items:center;gap:10px;background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:16px;padding:4px 14px;">
          <span style="font-size:15px;color:#64748B;">🔒</span>
          <input id="auth-pwd-input" type="password" placeholder="Enter Password or 4-digit PIN" value="123456" style="flex:1;border:none;background:transparent;padding:12px 0;font-size:13.5px;font-weight:700;color:#0F172A;outline:none;" />
          <button type="button" onclick="togglePasswordVisibility()" style="background:none;border:none;cursor:pointer;font-size:16px;color:#64748B;padding:4px;">
            <span id="pwd-eye-icon">👁</span>
          </button>
        </div>

        <!-- Remember Me & Legal Privacy Checkbox (Mandatory DPDP Act 2023) -->
        <div style="display:flex;flex-direction:column;gap:8px;padding:4px 2px;">
          <label style="display:flex;align-items:center;gap:8px;font-size:12px;color:#475569;font-weight:600;cursor:pointer;">
            <input type="checkbox" id="auth-remember-check" checked style="width:16px;height:16px;accent-color:#16A34A;cursor:pointer;" />
            <span>Remember my login credentials</span>
          </label>

          <label style="display:flex;align-items:flex-start;gap:8px;font-size:11.5px;color:#475569;font-weight:600;cursor:pointer;line-height:1.35;">
            <input type="checkbox" id="auth-privacy-check" checked style="width:16px;height:16px;accent-color:#16A34A;cursor:pointer;margin-top:1px;" />
            <span>
              I agree to NuKropAI <span onclick="openPrivacyModal()" style="color:#15803D;text-decoration:underline;font-weight:800;">Privacy Policy</span> &amp; <span onclick="openTermsModal()" style="color:#15803D;text-decoration:underline;font-weight:800;">Terms of Service</span>
            </span>
          </label>
        </div>

        <!-- Primary Action Button (Image 2 Potea Emerald Button) -->
        <button onclick="submitPoteaAuthForm()" style="width:100%;height:52px;border-radius:26px;background:linear-gradient(135deg, #16A34A, #15803D);color:#FFFFFF;border:none;font-size:15px;font-weight:900;cursor:pointer;box-shadow:0 8px 24px rgba(22,163,74,0.35);margin-top:4px;display:flex;align-items:center;justify-content:center;gap:8px;">
          <span>${isSignUp ? 'Create Account' : 'Sign In'}</span>
          <span style="font-size:16px;">→</span>
        </button>

      </div>

      <!-- Social Login Section (With Real SVG Logos) -->
      <div style="margin-top:18px;text-align:center;">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px;">
          <div style="flex:1;height:1px;background:#E2E8F0;"></div>
          <span style="font-size:11.5px;color:#94A3B8;font-weight:700;">or continue with</span>
          <div style="flex:1;height:1px;background:#E2E8F0;"></div>
        </div>

        <!-- Real Brand Vector Logos (Google, Apple, Facebook) -->
        <div style="display:flex;justify-content:center;gap:18px;">
          <!-- Google SVG Logo -->
          <button onclick="openInAppGoogleAuthModal()" title="Continue with Google" style="width:62px;height:52px;border-radius:16px;border:1.5px solid #E2E8F0;background:#FFFFFF;display:flex;align-items:center;justify-content:center;cursor:pointer;box-shadow:0 2px 8px rgba(15,23,42,0.04);transition:all 0.15s ease;">
            <svg width="24" height="24" viewBox="0 0 24 24">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
            </svg>
          </button>

          <!-- Authentic Apple SVG Logo -->
          <button onclick="alert('Apple Sign-In initialized securely.')" title="Continue with Apple" style="width:62px;height:52px;border-radius:16px;border:1.5px solid #E2E8F0;background:#FFFFFF;display:flex;align-items:center;justify-content:center;cursor:pointer;box-shadow:0 2px 8px rgba(15,23,42,0.04);transition:all 0.15s ease;">
            <svg width="22" height="22" viewBox="0 0 170 170">
              <path fill="#000000" d="M150.37 130.25c-2.45 5.66-5.35 10.87-8.71 15.66-4.58 6.53-8.33 11.05-11.22 13.56-4.48 4.12-9.28 6.23-14.42 6.35-3.69 0-8.14-1.05-13.32-3.18-5.19-2.12-9.97-3.17-14.34-3.17-4.58 0-9.49 1.05-14.75 3.17-5.26 2.13-9.5 3.24-12.74 3.35-4.35.13-9.16-1.9-14.42-6.08-3.69-3.08-7.69-7.89-12-14.42-6.53-9.88-11.57-20.91-15.13-33.09-3.56-12.18-5.34-23.75-5.34-34.71 0-14.42 3.69-26.4 11.08-35.95 7.39-9.55 16.73-14.42 28.02-14.61 4.58 0 9.88 1.25 15.9 3.75 6.02 2.5 9.94 3.75 11.75 3.75 1.58 0 5.63-1.32 12.15-3.96 6.52-2.64 12.15-3.8 16.89-3.48 12.44.63 22.37 5.34 29.8 14.13-10.87 6.61-16.19 15.65-15.95 27.13.24 8.94 3.75 16.48 10.53 22.62 6.78 6.14 14.88 9.55 24.3 10.23-2.12 6.33-4.58 12.67-7.39 19.01zM119.22 33.09c0-7.39 2.65-14.28 7.95-20.67 5.3-6.39 11.95-10.3 19.95-11.73.63 2.12.95 4.35.95 6.7 0 7.39-2.8 14.35-8.4 20.88-5.6 6.53-12.55 10.3-20.85 11.31-.48-2.12-.6-4.28-.6-6.49z"/>
            </svg>
          </button>

          <!-- Authentic Meta Facebook SVG Logo -->
          <button onclick="alert('Facebook Login initialized securely.')" title="Continue with Facebook" style="width:62px;height:52px;border-radius:16px;border:1.5px solid #E2E8F0;background:#FFFFFF;display:flex;align-items:center;justify-content:center;cursor:pointer;box-shadow:0 2px 8px rgba(15,23,42,0.04);transition:all 0.15s ease;">
            <svg width="24" height="24" viewBox="0 0 24 24">
              <path fill="#1877F2" d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
            </svg>
          </button>
        </div>
      </div>

      <!-- Footer Mode Switch -->
      <div style="text-align:center;margin-top:18px;">
        <span onclick="setAuthFormMode('${isSignUp ? 'signin' : 'signup'}')" style="font-size:12.5px;color:#15803D;font-weight:800;cursor:pointer;">
          ${isSignUp ? 'Already have an account? Sign In' : 'Don’t have an account? Sign Up'}
        </span>
      </div>

    </div>
  `;
}

function openPostLoginSuccessModal(name, role) {
  const chassis = document.querySelector('.phone-chassis') || document.body;
  const modalHtml = `
    <div id="post-login-success-modal" style="position:fixed;inset:0;background:rgba(0,0,0,0.65);backdrop-filter:blur(6px);z-index:9999999;display:flex;align-items:center;justify-content:center;padding:24px;box-sizing:border-box;">
      <div style="background:#FFFFFF;border-radius:28px;padding:32px 24px;width:100%;max-width:320px;text-align:center;box-shadow:0 20px 50px rgba(0,0,0,0.25);animation:nkFadeIn 0.3s ease;">
        <div style="width:72px;height:72px;border-radius:50%;background:linear-gradient(135deg, #22C55E, #16A34A);display:flex;align-items:center;justify-content:center;margin:0 auto 16px;box-shadow:0 8px 24px rgba(34,197,94,0.35);">
          <svg width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
        </div>
        <div style="font-size:20px;font-weight:900;color:#0F172A;line-height:1.2;">Congratulations!</div>
        <div style="font-size:13px;color:#475569;margin-top:8px;line-height:1.45;font-weight:600;">
          Welcome back, <b style="color:#15803D;">${name || 'Farmer'}</b>! Your verified account is ready.
        </div>
        <div style="margin-top:20px;display:flex;align-items:center;justify-content:center;gap:8px;color:#16A34A;font-size:12.5px;font-weight:800;">
          <div style="width:16px;height:16px;border:2px solid #16A34A;border-top-color:transparent;border-radius:50%;animation:spin 1s linear infinite;"></div>
          <span>Redirecting to Dashboard...</span>
        </div>
      </div>
    </div>
  `;
  chassis.insertAdjacentHTML('beforeend', modalHtml);

  setTimeout(() => {
    ['post-login-success-modal', 'login-screen-overlay', 'startup-experience-overlay', 'onboarding-experience-overlay', 'permission-experience-overlay', 'permissions-suite-modal'].forEach(id => {
      const el = document.getElementById(id);
      if (el) el.remove();
    });

    const dock = document.querySelector('.bottom-dock-wrap');
    if (dock) dock.style.display = 'flex';

    if (role === 'driver') {
      if (typeof loginAsDriver === 'function') loginAsDriver();
    } else {
      if (typeof switchUserRole === 'function') switchUserRole('farmer');
      if (typeof openScreen === 'function') openScreen('home', document.getElementById('tab-home'));
    }
  }, 1200);
}
</script>
"""

def update_file(filepath):
    print(f"Applying master unified module to {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()

    # Remove any previous injected scripts
    c = re.sub(r'<script>\s*// ═+\s*NUKROPAI FULL-BLEED 6-FEATURE ONBOARDING CAROUSEL[\s\S]*?</script>', '', c)
    c = re.sub(r'<script>\s*// ═+\s*MASTER FULL-BLEED ONBOARDING[\s\S]*?</script>', '', c)
    c = re.sub(r'<style>\s*/\* ═+\s*FULL-BLEED ONBOARDING[\s\S]*?</style>', '', c)

    # Append before </body>
    c = c.replace('</body>', f'{unified_module}\n</body>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"Done updating {filepath}")

update_file('app/src/main/assets/index.html')
update_file('nukrop_emulator.html')
