import os, sys, re

sys.stdout.reconfigure(encoding='utf-8')

js_code = r'''
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
  NuKropAnalytics.track('onboarding_started', { manualTrigger: isManual });

  const chassis = document.querySelector('.phone-chassis');
  if (!chassis) return;

  const existing = document.getElementById('onboarding-experience-overlay');
  if (existing) existing.remove();

  const overlayHtml = `
    <div id="onboarding-experience-overlay" style="position:absolute;inset:0;background:#0F172A;border-radius:40px;overflow:hidden;z-index:9999;display:flex;flex-direction:column;font-family:inherit;">
      
      <!-- Slide Container -->
      <div id="ob-slides-viewport" style="position:relative;width:100%;height:100%;overflow:hidden;display:flex;">
        ${ONBOARDING_SLIDES_DATA.map((slide, idx) => `
          <div id="ob-slide-${idx}" class="ob-carousel-slide ${idx === 0 ? 'active' : ''}" style="background-image: url('${slide.image}');">
            <div class="ob-gradient-vignette"></div>
            
            <!-- Top Controls (Floating Skip Button) -->
            <div style="position:relative;z-index:12;padding:20px 20px 0;display:flex;justify-content:flex-end;align-items:center;">
              <button onclick="openPermissionsSuiteModal()" style="background:rgba(255,255,255,0.9);backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,0.4);border-radius:20px;padding:6px 16px;font-size:12px;font-weight:800;color:#15803D;cursor:pointer;box-shadow:0 4px 12px rgba(0,0,0,0.15);">
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
    // Reached end of onboarding -> transition to dedicated visual permissions modal!
    openPermissionsSuiteModal();
    return;
  }

  // Deactivate current
  const curSlide = document.getElementById(`ob-slide-${window.currentOnboardingSlide}`);
  if (curSlide) curSlide.classList.remove('active');

  // Activate next
  window.currentOnboardingSlide = nextIndex;
  const nextSlide = document.getElementById(`ob-slide-${window.currentOnboardingSlide}`);
  if (nextSlide) nextSlide.classList.add('active');

  NuKropAnalytics.track('onboarding_slide_viewed', { slideIndex: nextIndex });
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

  const chassis = document.querySelector('.phone-chassis');
  if (!chassis) return;

  const permHtml = `
    <div id="permissions-suite-modal" style="position:absolute;inset:0;background:#FFFFFF;border-radius:40px;overflow:hidden;z-index:9999;display:flex;flex-direction:column;font-family:inherit;padding:28px 20px 24px;box-sizing:border-box;justify-content:space-between;">
      
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

  // Navigate to Potea-style Login
  if (typeof renderLoginScreen === 'function') {
    renderLoginScreen(document.getElementById('screen-container'));
  }
}

function skipPermissionsAndProceed() {
  localStorage.setItem('onboarding_completed', 'true');
  const permModal = document.getElementById('permissions-suite-modal');
  if (permModal) permModal.remove();

  if (typeof renderLoginScreen === 'function') {
    renderLoginScreen(document.getElementById('screen-container'));
  }
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

function openPostLoginSuccessModal(name, role) {
  const chassis = document.querySelector('.phone-chassis') || document.body;
  const modalHtml = `
    <div id="post-login-success-modal" style="position:absolute;inset:0;background:rgba(0,0,0,0.65);backdrop-filter:blur(6px);z-index:999999;display:flex;align-items:center;justify-content:center;padding:24px;box-sizing:border-box;">
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
    const m = document.getElementById('post-login-success-modal');
    if (m) m.remove();
    if (role === 'driver') {
      window.isDriverMode = true;
      if (typeof switchAppRole === 'function') switchAppRole('driver');
    } else {
      window.isDriverMode = false;
      if (typeof switchAppRole === 'function') switchAppRole('farmer');
    }
  }, 1200);
}
'''

print("JavaScript module prepared successfully.")
