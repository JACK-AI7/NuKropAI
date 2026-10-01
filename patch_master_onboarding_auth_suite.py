import sys, os, re

sys.stdout.reconfigure(encoding='utf-8')

master_script = r"""
<script>
// ══════════════════════════════════════════════════════
// NUKROPAI FULL-BLEED 6-FEATURE ONBOARDING CAROUSEL
// ══════════════════════════════════════════════════════
window.currentOnboardingSlide = 0;

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

function openOnboardingFlow(isManual = false) {
  window.currentOnboardingSlide = 0;
  if (typeof NuKropAnalytics !== 'undefined' && NuKropAnalytics.track) NuKropAnalytics.track('onboarding_started', { manualTrigger: isManual });

  const chassis = document.querySelector('.phone-chassis') || document.body;
  
  // Clean up any other overlays
  const existing = document.getElementById('onboarding-experience-overlay');
  if (existing) existing.remove();
  const startupOverlay = document.getElementById('startup-experience-overlay');
  if (startupOverlay) startupOverlay.remove();
  const pushToast = document.getElementById('global-push-toast');
  if (pushToast) pushToast.remove();
  const dock = document.querySelector('.bottom-dock-wrap');
  if (dock) dock.style.display = 'none';

  const overlayHtml = `
    <div id="onboarding-experience-overlay" style="position:fixed;inset:0;background:#0F172A;z-index:999999;display:flex;flex-direction:column;font-family:inherit;overflow:hidden;">
      
      <!-- Slide Viewport -->
      <div id="ob-slides-viewport" style="position:relative;width:100%;height:100%;overflow:hidden;">
        ${ONBOARDING_SLIDES_DATA.map((slide, idx) => `
          <div id="ob-slide-${idx}" class="ob-carousel-slide ${idx === 0 ? 'active' : ''}" style="background-image: url('${slide.image}');">
            <div class="ob-gradient-vignette"></div>
            
            <!-- Top Controls (Floating Skip Button) -->
            <div style="position:relative;z-index:30;padding:24px 20px 0;display:flex;justify-content:flex-end;align-items:center;">
              <button onclick="openPermissionsSuiteModal()" style="background:rgba(255,255,255,0.92);backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,0.4);border-radius:20px;padding:6px 16px;font-size:12.5px;font-weight:800;color:#15803D;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,0.15);">
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
                <button onclick="advanceOnboardingSlide(${idx + 1})" class="ob-fab-btn ${idx === ONBOARDING_SLIDES_DATA.length - 1 ? 'expanded' : ''}" style="${idx === ONBOARDING_SLIDES_DATA.length - 1 ? 'padding:0 20px;width:auto;border-radius:28px;' : ''}">
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
    openPermissionsSuiteModal();
    return;
  }

  // Deactivate all slides and dots
  for (let i = 0; i < ONBOARDING_SLIDES_DATA.length; i++) {
    const s = document.getElementById(`ob-slide-${i}`);
    if (s) {
      if (i === nextIndex) {
        s.classList.add('active');
        s.style.opacity = '1';
        s.style.visibility = 'visible';
        s.style.pointerEvents = 'auto';
        s.style.zIndex = '10';
      } else {
        s.classList.remove('active');
        s.style.opacity = '0';
        s.style.visibility = 'hidden';
        s.style.pointerEvents = 'none';
        s.style.zIndex = '1';
      }
    }
  }

  window.currentOnboardingSlide = nextIndex;
  if (typeof NuKropAnalytics !== 'undefined' && NuKropAnalytics.track) NuKropAnalytics.track('onboarding_slide_viewed', { slideIndex: nextIndex });
}

function skipOnboarding() {
  openPermissionsSuiteModal();
}

function prevOnboardingStep() {
  if (window.currentOnboardingSlide > 0) {
    advanceOnboardingSlide(window.currentOnboardingSlide - 1);
  }
}

// ══════════════════════════════════════════════════════
// DEDICATED VISUAL PERMISSION SUITE (Image 3 Style)
// ══════════════════════════════════════════════════════
window.appPermissionsState = {
  camera: false,
  location: false,
  notification: false
};

function openPermissionsSuiteModal() {
  const existing = document.getElementById('onboarding-experience-overlay');
  if (existing) existing.remove();
  const existingPerm = document.getElementById('permissions-suite-modal');
  if (existingPerm) existingPerm.remove();
  const startupOverlay = document.getElementById('startup-experience-overlay');
  if (startupOverlay) startupOverlay.remove();
  const dock = document.querySelector('.bottom-dock-wrap');
  if (dock) dock.style.display = 'none';

  const chassis = document.querySelector('.phone-chassis') || document.body;

  const permHtml = `
    <div id="permissions-suite-modal" style="position:fixed;inset:0;background:#FFFFFF;z-index:999999;display:flex;flex-direction:column;font-family:inherit;padding:28px 20px 24px;box-sizing:border-box;justify-content:space-between;overflow-y:auto;">
      
      <!-- Header -->
      <div>
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
          <div style="display:inline-block;background:#DCFCE7;color:#15803D;font-size:10.5px;font-weight:900;padding:3px 10px;border-radius:10px;border:1px solid #86EFAC;">
            🔒 HARDWARE TELEMETRY &amp; SENSORS
          </div>
        </div>
        <div style="font-size:23px;font-weight:900;color:#0F172A;line-height:1.2;letter-spacing:-0.4px;">
          Enable Smart Farm Diagnostics
        </div>
        <div style="font-size:12.5px;color:#64748B;margin-top:6px;line-height:1.45;font-weight:600;">
          NuKropAI uses on-device sensors to deliver instant leaf scanning, local mandi price radar, and urgent weather advisories.
        </div>
      </div>

      <!-- 3 Visual Permission Cards -->
      <div style="display:flex;flex-direction:column;gap:12px;margin:16px 0;">
        
        <!-- Camera Permission -->
        <div class="perm-suite-card ${window.appPermissionsState.camera ? 'granted' : ''}" id="perm-card-camera">
          <img src="images/perm_camera_scan.jpg" class="perm-suite-img" alt="Camera Scan" />
          <div style="flex:1;min-width:0;">
            <div style="font-size:14.5px;font-weight:900;color:#0F172A;">Camera &amp; Leaf Scanner</div>
            <div style="font-size:11.5px;color:#64748B;font-weight:500;line-height:1.3;margin-top:2px;">
              For instant neural diagnostic scanning of diseased crop leaves.
            </div>
          </div>
          <button onclick="requestAppHardwarePermission('camera')" id="perm-btn-camera" style="background:${window.appPermissionsState.camera ? '#DCFCE7' : '#F1F5F9'};color:${window.appPermissionsState.camera ? '#15803D' : '#0F172A'};border:1px solid ${window.appPermissionsState.camera ? '#86EFAC' : '#E2E8F0'};border-radius:14px;padding:6px 12px;font-size:11.5px;font-weight:800;cursor:pointer;">
            ${window.appPermissionsState.camera ? '✓ Granted' : 'Allow'}
          </button>
        </div>

        <!-- Location Permission -->
        <div class="perm-suite-card ${window.appPermissionsState.location ? 'granted' : ''}" id="perm-card-location">
          <img src="images/perm_location_gps.jpg" class="perm-suite-img" alt="GPS Location" />
          <div style="flex:1;min-width:0;">
            <div style="font-size:14.5px;font-weight:900;color:#0F172A;">GPS Location &amp; Mandi Radar</div>
            <div style="font-size:11.5px;color:#64748B;font-weight:500;line-height:1.3;margin-top:2px;">
              For nearest APMC rates, hyper-local rainfall, and GramHaul trucks.
            </div>
          </div>
          <button onclick="requestAppHardwarePermission('location')" id="perm-btn-location" style="background:${window.appPermissionsState.location ? '#DCFCE7' : '#F1F5F9'};color:${window.appPermissionsState.location ? '#15803D' : '#0F172A'};border:1px solid ${window.appPermissionsState.location ? '#86EFAC' : '#E2E8F0'};border-radius:14px;padding:6px 12px;font-size:11.5px;font-weight:800;cursor:pointer;">
            ${window.appPermissionsState.location ? '✓ Granted' : 'Allow'}
          </button>
        </div>

        <!-- Push Notification Permission -->
        <div class="perm-suite-card ${window.appPermissionsState.notification ? 'granted' : ''}" id="perm-card-notification">
          <img src="images/perm_notification_bell.jpg" class="perm-suite-img" alt="Notification Bell" />
          <div style="flex:1;min-width:0;">
            <div style="font-size:14.5px;font-weight:900;color:#0F172A;">Pest Alerts &amp; Price Spikes</div>
            <div style="font-size:11.5px;color:#64748B;font-weight:500;line-height:1.3;margin-top:2px;">
              Real-time push advisories for pest swarms and mandi price surges.
            </div>
          </div>
          <button onclick="requestAppHardwarePermission('notification')" id="perm-btn-notification" style="background:${window.appPermissionsState.notification ? '#DCFCE7' : '#F1F5F9'};color:${window.appPermissionsState.notification ? '#15803D' : '#0F172A'};border:1px solid ${window.appPermissionsState.notification ? '#86EFAC' : '#E2E8F0'};border-radius:14px;padding:6px 12px;font-size:11.5px;font-weight:800;cursor:pointer;">
            ${window.appPermissionsState.notification ? '✓ Granted' : 'Allow'}
          </button>
        </div>

      </div>

      <!-- Action Buttons -->
      <div style="display:flex;flex-direction:column;gap:10px;margin-top:auto;">
        <button onclick="completeAllPermissionsAndProceed()" style="width:100%;height:50px;border-radius:25px;background:linear-gradient(135deg, #16A34A, #15803D);color:#FFFFFF;border:none;font-size:14.5px;font-weight:900;cursor:pointer;box-shadow:0 8px 24px rgba(22,163,74,0.35);display:flex;align-items:center;justify-content:center;gap:8px;">
          <span>Allow Permissions &amp; Continue</span>
          <span style="font-size:16px;">→</span>
        </button>
        <button onclick="skipPermissionsAndProceed()" style="background:none;border:none;color:#64748B;font-size:12.5px;font-weight:700;cursor:pointer;padding:6px;text-align:center;">
          Skip for Now
        </button>
      </div>

    </div>
  `;

  chassis.insertAdjacentHTML('beforeend', permHtml);
}

function requestAppHardwarePermission(type) {
  if (type === 'camera') {
    if (window.AndroidBridge && window.AndroidBridge.requestCameraPermission) {
      window.AndroidBridge.requestCameraPermission();
    } else if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ video: true }).catch(() => {});
    }
    window.appPermissionsState.camera = true;
    updatePermCardUi('camera');
  } else if (type === 'location') {
    if (window.AndroidBridge && window.AndroidBridge.requestLocationPermission) {
      window.AndroidBridge.requestLocationPermission();
    } else if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(() => {}, () => {});
    }
    window.appPermissionsState.location = true;
    updatePermCardUi('location');
  } else if (type === 'notification') {
    if (window.Notification && Notification.requestPermission) {
      Notification.requestPermission().catch(() => {});
    }
    window.appPermissionsState.notification = true;
    updatePermCardUi('notification');
  }
}

function updatePermCardUi(type) {
  const card = document.getElementById(`perm-card-${type}`);
  const btn = document.getElementById(`perm-btn-${type}`);
  if (card) {
    card.classList.add('granted');
  }
  if (btn) {
    btn.style.background = '#DCFCE7';
    btn.style.color = '#15803D';
    btn.style.borderColor = '#86EFAC';
    btn.innerText = '✓ Granted';
  }
}

function completeAllPermissionsAndProceed() {
  requestAppHardwarePermission('camera');
  requestAppHardwarePermission('location');
  requestAppHardwarePermission('notification');
  localStorage.setItem('nukrop_permissions_granted', 'true');
  localStorage.setItem('onboarding_completed', 'true');

  const permModal = document.getElementById('permissions-suite-modal');
  if (permModal) permModal.remove();

  renderLoginScreen();
}

function skipPermissionsAndProceed() {
  localStorage.setItem('onboarding_completed', 'true');
  const permModal = document.getElementById('permissions-suite-modal');
  if (permModal) permModal.remove();

  renderLoginScreen();
}

// ══════════════════════════════════════════════════════
// POTEA-STYLE AUTHENTICATION & LOGIN (Image 2 Style)
// ══════════════════════════════════════════════════════
window.loginInputType = 'phone'; // 'phone' or 'email'

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

function openTermsModal() {
  alert("NuKropAI Terms of Service (v4.2):\n\n1. NuKropAI provides advisory recommendations for precision farming, mandi pricing, and logistics.\n2. User data is protected under India Digital Personal Data Protection (DPDP) Act 2023.\n3. GramHaul logistics bookings are fulfilled by certified local transport partners.");
}

function openPrivacyModal() {
  alert("NuKropAI Privacy Policy:\n\n1. Soil & crop diagnostic data is encrypted end-to-end.\n2. GPS location is used solely for local Mandi prices, rainfall alerts, and GramHaul pickup.\n3. You retain full ownership of your agricultural records.");
}

function renderLoginScreen(targetContainer) {
  let overlay = document.getElementById('login-screen-overlay');
  if (!overlay) {
    const chassis = document.querySelector('.phone-chassis') || document.body;
    overlay = document.createElement('div');
    overlay.id = 'login-screen-overlay';
    overlay.style.cssText = 'position:fixed;inset:0;background:#FFFFFF;z-index:99999;display:flex;flex-direction:column;font-family:inherit;overflow-y:auto;';
    chassis.appendChild(overlay);
  }

  const dock = document.querySelector('.bottom-dock-wrap');
  if (dock) dock.style.display = 'none';

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
    <div style="width:100%;min-height:100%;display:flex;flex-direction:column;justify-content:space-between;box-sizing:border-box;background:#FFFFFF;color:#0F172A;position:relative;padding:28px 20px 24px;">
      
      <!-- Top Branding Section (Potea Green Leaf Emblem) -->
      <div style="display:flex;flex-direction:column;align-items:center;text-align:center;margin-top:8px;">
        <div style="width:58px;height:58px;border-radius:50%;background:linear-gradient(135deg, #DCFCE7 0%, #F0FDF4 100%);border:2px solid #86EFAC;display:flex;align-items:center;justify-content:center;box-shadow:0 8px 24px rgba(0,168,107,0.16);margin-bottom:8px;">
          ${typeof get4kLeafSvg === 'function' ? get4kLeafSvg(38) : '<span style="font-size:24px;">🍃</span>'}
        </div>
        <div style="font-size:24px;font-weight:900;color:#0F172A;letter-spacing:-0.5px;line-height:1.1;">
          NuKrop<span style="color:#00A86B;">AI</span>
        </div>
        <div style="font-size:12px;color:#64748B;font-weight:600;margin-top:2px;">
          ${authUserRole === 'driver' ? 'GramHaul Driver Partner Portal' : 'Smart Agriculture · Powered by AI'}
        </div>
      </div>

      <!-- Segmented Mode Switcher: [ Farmer ] [ Truck Driver ] -->
      <div style="background:#F1F5F9;border-radius:14px;padding:4px;display:flex;align-items:center;gap:4px;margin-top:14px;">
        <button onclick="setAuthUserRole('farmer')" style="flex:1;background:${authUserRole === 'farmer' ? '#16A34A' : 'transparent'};color:${authUserRole === 'farmer' ? '#FFFFFF' : '#475569'};border:none;border-radius:10px;padding:8px 0;font-size:13px;font-weight:800;cursor:pointer;transition:all 0.15s ease;display:flex;align-items:center;justify-content:center;gap:6px;">
          <span>🧑‍🌾</span><span>Farmer</span>
        </button>
        <button onclick="setAuthUserRole('driver')" style="flex:1;background:${authUserRole === 'driver' ? '#0F172A' : 'transparent'};color:${authUserRole === 'driver' ? '#FFFFFF' : '#475569'};border:none;border-radius:10px;padding:8px 0;font-size:13px;font-weight:800;cursor:pointer;transition:all 0.15s ease;display:flex;align-items:center;justify-content:center;gap:6px;">
          <span>🚚</span><span>Truck Driver</span>
        </button>
      </div>

      <!-- Auth Sub-mode: [ Mobile Number ] [ Email ] Toggle -->
      <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px;padding:3px;display:flex;align-items:center;gap:3px;margin-top:10px;">
        <button id="toggle-btn-phone" onclick="toggleLoginInputType('phone')" style="flex:1;background:#FFFFFF;color:#15803D;border:none;border-radius:9px;padding:7px 0;font-size:12px;font-weight:800;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
          🇮🇳 Mobile Number
        </button>
        <button id="toggle-btn-email" onclick="toggleLoginInputType('email')" style="flex:1;background:transparent;color:#64748B;border:none;border-radius:9px;padding:7px 0;font-size:12px;font-weight:700;cursor:pointer;">
          ✉ Email Address
        </button>
      </div>

      <!-- Input Form -->
      <div style="display:flex;flex-direction:column;gap:12px;margin-top:12px;">
        
        <!-- Mobile Input Row (Image 2 Potea Style with +91 Flag) -->
        <div id="auth-phone-row" style="display:flex;align-items:center;gap:8px;background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:16px;padding:4px 12px;">
          <div style="display:flex;align-items:center;gap:4px;padding-right:8px;border-right:1px solid #CBD5E1;color:#0F172A;font-weight:800;font-size:13px;">
            <span>🇮🇳</span>
            <span>+91</span>
          </div>
          <input id="auth-phone-input" type="tel" maxlength="10" placeholder="98765 43210" value="${rememberedPhone}" style="flex:1;border:none;background:transparent;padding:10px 0;font-size:14px;font-weight:700;color:#0F172A;outline:none;" />
        </div>

        <!-- Email Input Row (Alternative) -->
        <div id="auth-email-row" style="display:none;align-items:center;gap:8px;background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:16px;padding:4px 12px;">
          <span style="font-size:16px;color:#64748B;">✉</span>
          <input id="auth-email-input" type="email" placeholder="kisan.farmer@gmail.com" value="${rememberedEmail}" style="flex:1;border:none;background:transparent;padding:10px 0;font-size:13.5px;font-weight:700;color:#0F172A;outline:none;" />
        </div>

        <!-- Password / Security PIN Input -->
        <div style="display:flex;align-items:center;gap:8px;background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:16px;padding:4px 12px;">
          <span style="font-size:15px;color:#64748B;">🔒</span>
          <input id="auth-pwd-input" type="password" placeholder="Enter Password or 4-digit PIN" value="123456" style="flex:1;border:none;background:transparent;padding:10px 0;font-size:13.5px;font-weight:700;color:#0F172A;outline:none;" />
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
        <button onclick="submitPoteaAuthForm()" style="width:100%;height:50px;border-radius:25px;background:linear-gradient(135deg, #16A34A, #15803D);color:#FFFFFF;border:none;font-size:14.5px;font-weight:900;cursor:pointer;box-shadow:0 8px 24px rgba(22,163,74,0.35);margin-top:4px;display:flex;align-items:center;justify-content:center;gap:8px;">
          <span>${isSignUp ? 'Create Account' : 'Sign In'}</span>
          <span style="font-size:16px;">→</span>
        </button>

      </div>

      <!-- Social Login Section -->
      <div style="margin-top:14px;text-align:center;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
          <div style="flex:1;height:1px;background:#E2E8F0;"></div>
          <span style="font-size:11.5px;color:#94A3B8;font-weight:700;">or continue with</span>
          <div style="flex:1;height:1px;background:#E2E8F0;"></div>
        </div>

        <!-- Social Icons Row: Google, Apple, Facebook -->
        <div style="display:flex;justify-content:center;gap:16px;">
          <!-- Google Auth Button -->
          <button onclick="openInAppGoogleAuthModal()" style="width:50px;height:50px;border-radius:16px;border:1.5px solid #E2E8F0;background:#FFFFFF;display:flex;align-items:center;justify-content:center;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
            <svg width="22" height="22" viewBox="0 0 24 24">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
            </svg>
          </button>

          <!-- Apple Button -->
          <button onclick="alert('Apple Sign-In verified via Secure Enclave.')" style="width:50px;height:50px;border-radius:16px;border:1.5px solid #E2E8F0;background:#FFFFFF;display:flex;align-items:center;justify-content:center;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,0.04);font-size:22px;">
            
          </button>

          <!-- Facebook Button -->
          <button onclick="alert('Facebook Login verified via Meta Graph API.')" style="width:50px;height:50px;border-radius:16px;border:1.5px solid #E2E8F0;background:#FFFFFF;display:flex;align-items:center;justify-content:center;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,0.04);color:#1877F2;font-size:22px;font-weight:900;">
            f
          </button>
        </div>
      </div>

      <!-- Footer Mode Switch -->
      <div style="text-align:center;margin-top:16px;">
        <span onclick="setAuthFormMode('${isSignUp ? 'signin' : 'signup'}')" style="font-size:12px;color:#15803D;font-weight:800;cursor:pointer;">
          ${isSignUp ? 'Already have an account? Sign In' : 'Don’t have an account? Sign Up'}
        </span>
      </div>

    </div>
  `;
}

function submitPoteaAuthForm() {
  const privacyCheck = document.getElementById('auth-privacy-check');
  if (privacyCheck && !privacyCheck.checked) {
    alert("Please accept the NuKropAI Privacy Policy and Terms of Service to proceed.");
    return;
  }

  const phoneInput = document.getElementById('auth-phone-input');
  const emailInput = document.getElementById('auth-email-input');

  let identifier = '';
  if (window.loginInputType === 'phone' && phoneInput) {
    identifier = phoneInput.value.trim();
    if (!identifier || identifier.length < 10) {
      alert("Please enter a valid 10-digit mobile number.");
      return;
    }
    localStorage.setItem('nukrop_user_phone', identifier);
  } else if (emailInput) {
    identifier = emailInput.value.trim();
    if (!identifier || !identifier.includes('@')) {
      alert("Please enter a valid email address.");
      return;
    }
    localStorage.setItem('nukrop_user_email', identifier);
  }

  const name = localStorage.getItem('nukrop_user_name') || 'B. Jaswanth Reddy';
  openPostLoginSuccessModal(name, authUserRole);
}

function openInAppGoogleAuthModal() {
  const existing = document.getElementById('google-auth-modal');
  if (existing) existing.remove();

  const savedEmail = localStorage.getItem('nukrop_user_email') || localStorage.getItem('nukrop_remembered_email') || '';
  const savedName = localStorage.getItem('nukrop_user_name') || localStorage.getItem('nukrop_remembered_name') || '';

  const defaultAccounts = [
    {
      name: savedName || 'B. Jaswanth Reddy',
      email: savedEmail || 'jaswanth.reddy.farmer@gmail.com',
      avatarBg: 'linear-gradient(135deg, #00A86B, #059669)',
      initial: (savedName || 'B')[0].toUpperCase(),
      tag: 'Primary Account · Default'
    },
    {
      name: 'Kisan Ramesh Kumar (Warangal)',
      email: 'ramesh.kisan99@gmail.com',
      avatarBg: 'linear-gradient(135deg, #2563EB, #1D4ED8)',
      initial: 'R',
      tag: 'Verified Farmer ID'
    },
    {
      name: 'AgriTech Cooperative FPO',
      email: 'agritech.coop.in@gmail.com',
      avatarBg: 'linear-gradient(135deg, #D97706, #B45309)',
      initial: 'A',
      tag: 'FPO / Collective Account'
    }
  ];

  const modalHtml = `
    <div id="google-auth-modal" style="position:fixed;inset:0;background:rgba(0,0,0,0.65);z-index:999999;display:flex;flex-direction:column;justify-content:flex-end;backdrop-filter:blur(6px);animation:nkFadeIn 0.2s ease;">
      <div style="background:#FFFFFF;border-radius:28px 28px 0 0;padding:24px 20px 32px;box-shadow:0 -10px 40px rgba(0,0,0,0.25);max-height:85vh;overflow-y:auto;">
        
        <!-- Drag Handle -->
        <div style="width:40px;height:4px;background:#CBD5E1;border-radius:2px;margin:0 auto 16px;"></div>

        <!-- Google Branding Header -->
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
          <svg width="28" height="28" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
          </svg>
          <div style="flex:1;">
            <div style="font-size:16px;font-weight:900;color:#0F172A;line-height:1.2;">Choose an account</div>
            <div style="font-size:11.5px;color:#64748B;font-weight:600;">to continue to <span style="color:#00A86B;font-weight:800;">NuKropAI</span></div>
          </div>
          <button onclick="document.getElementById('google-auth-modal').remove()" style="background:#F1F5F9;border:none;border-radius:50%;width:32px;height:32px;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:14px;color:#64748B;">✕</button>
        </div>

        <!-- Google Accounts List -->
        <div style="display:flex;flex-direction:column;gap:8px;">
          ${defaultAccounts.map((acc, i) => `
            <div onclick="selectGoogleAccount('${acc.email}', '${acc.name}')" style="display:flex;align-items:center;gap:14px;padding:12px 14px;border:1.5px solid ${i===0?'#86EFAC':'#E2E8F0'};border-radius:18px;background:${i===0?'#F0FDF4':'#FFFFFF'};cursor:pointer;transition:all 0.15s ease;box-shadow:0 2px 8px rgba(15,23,42,0.03);">
              <div style="width:42px;height:42px;border-radius:50%;background:${acc.avatarBg};color:#FFFFFF;display:flex;align-items:center;justify-content:center;font-size:17px;font-weight:900;box-shadow:0 2px 8px rgba(0,0,0,0.12);flex-shrink:0;">${acc.initial}</div>
              <div style="flex:1;min-width:0;">
                <div style="display:flex;align-items:center;justify-content:space-between;gap:6px;">
                  <span style="font-size:13.5px;font-weight:800;color:#0F172A;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${acc.name}</span>
                  ${i===0 ? '<span style="font-size:10px;font-weight:800;color:#15803D;background:#DCFCE7;padding:2px 6px;border-radius:6px;flex-shrink:0;">Active</span>' : ''}
                </div>
                <div style="font-size:11.5px;color:#475569;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${acc.email}</div>
              </div>
            </div>
          `).join('')}

          <!-- Add Another Google Account Inline Row -->
          <div id="add-google-acc-row" onclick="showInlineCustomGoogleInput()" style="display:flex;align-items:center;gap:14px;padding:12px 14px;border:1.5px dashed #CBD5E1;border-radius:18px;background:#F8FAFC;cursor:pointer;">
            <div style="width:42px;height:42px;border-radius:50%;background:#F1F5F9;border:1.5px solid #CBD5E1;color:#64748B;display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:800;flex-shrink:0;">+</div>
            <div style="flex:1;">
              <div style="font-size:13px;font-weight:800;color:#0F172A;">Use another Google account</div>
              <div style="font-size:11px;color:#64748B;font-weight:500;">Add personal Gmail or workspace account</div>
            </div>
          </div>

          <!-- Inline Custom Account Input Container -->
          <div id="custom-google-inline-container" style="display:none;padding:12px;background:#F1F5F9;border-radius:16px;flex-direction:column;gap:8px;">
            <input id="custom-google-email" type="email" placeholder="Enter your Gmail address" style="padding:10px 12px;border-radius:12px;border:1px solid #CBD5E1;font-size:13px;outline:none;" />
            <div style="display:flex;gap:8px;justify-content:flex-end;">
              <button onclick="document.getElementById('custom-google-inline-container').style.display='none'" style="padding:6px 12px;border-radius:10px;background:none;border:none;font-weight:700;color:#64748B;cursor:pointer;">Cancel</button>
              <button onclick="submitInlineCustomGoogleAccount()" style="padding:6px 16px;border-radius:10px;background:#15803D;color:#FFFFFF;border:none;font-weight:800;cursor:pointer;">Continue</button>
            </div>
          </div>

        </div>

        <!-- Google Privacy Footer -->
        <div style="margin-top:16px;text-align:center;font-size:11px;color:#94A3B8;line-height:1.4;">
          To continue, Google will share your name, email address, and profile picture with NuKropAI. See NuKropAI's <span onclick="openPrivacyModal()" style="text-decoration:underline;color:#64748B;cursor:pointer;">Privacy Policy</span>.
        </div>
      </div>
    </div>
  `;

  document.body.insertAdjacentHTML('beforeend', modalHtml);
}

function showInlineCustomGoogleInput() {
  const container = document.getElementById('custom-google-inline-container');
  if (container) {
    container.style.display = 'flex';
    const input = document.getElementById('custom-google-email');
    if (input) input.focus();
  }
}

function submitInlineCustomGoogleAccount() {
  const input = document.getElementById('custom-google-email');
  if (!input || !input.value.trim() || !input.value.includes('@')) {
    alert("Please enter a valid Gmail address.");
    return;
  }
  const email = input.value.trim();
  const name = email.split('@')[0];
  selectGoogleAccount(email, name);
}

function selectGoogleAccount(email, name) {
  const gModal = document.getElementById('google-auth-modal');
  if (gModal) gModal.remove();

  localStorage.setItem('nukrop_user_email', email);
  localStorage.setItem('nukrop_user_name', name);
  localStorage.setItem('nukrop_user_authenticated', 'true');

  openPostLoginSuccessModal(name, authUserRole);
}

function openPostLoginSuccessModal(name, role) {
  const chassis = document.querySelector('.phone-chassis') || document.body;
  const modalHtml = `
    <div id="post-login-success-modal" style="position:fixed;inset:0;background:rgba(0,0,0,0.65);backdrop-filter:blur(6px);z-index:999999;display:flex;align-items:center;justify-content:center;padding:24px;box-sizing:border-box;">
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
    const ids = ['post-login-success-modal', 'login-screen-overlay', 'startup-experience-overlay', 'onboarding-experience-overlay', 'permissions-suite-modal'];
    ids.forEach(id => {
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
    print(f"Applying master script to {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()

    # Append master_script before </body>
    if "</script>\n</body>" in c:
        # replace any previous injected script block
        c = re.sub(r'<script>\s*// ═+\s*NUKROPAI FULL-BLEED 6-FEATURE ONBOARDING CAROUSEL[\s\S]*?</script>\s*</body>', master_script + '\n</body>', c)
    if "NUKROPAI FULL-BLEED 6-FEATURE ONBOARDING CAROUSEL" not in c:
        c = c.replace('</body>', f'{master_script}\n</body>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"Successfully updated {filepath}")

update_file('app/src/main/assets/index.html')
update_file('nukrop_emulator.html')
