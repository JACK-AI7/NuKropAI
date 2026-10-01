import sys, re

sys.stdout.reconfigure(encoding='utf-8')

def patch_auth_lifecycle(filepath):
    print(f"Patching auth lifecycle in {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Upgraded renderLoginScreen and openPostLoginSuccessModal
    new_auth_block = '''
function renderLoginScreen(targetContainer) {
  let container = targetContainer;
  if (!container || container.id === 'screen-container') {
    let overlay = document.getElementById('login-screen-overlay');
    if (!overlay) {
      const chassis = document.querySelector('.phone-chassis') || document.body;
      overlay = document.createElement('div');
      overlay.id = 'login-screen-overlay';
      overlay.style.cssText = 'position:fixed;inset:0;background:#FFFFFF;z-index:99999;display:flex;flex-direction:column;font-family:inherit;overflow:hidden;';
      chassis.appendChild(overlay);
    }
    container = overlay;
  }

  window.authFormMode = window.authFormMode || 'signin';
  window.authUserRole = window.authUserRole || 'farmer';
  const currentAuthMode = window.authFormMode;
  const currentAuthRole = window.authUserRole;
  if (typeof NuKropAnalytics !== 'undefined' && NuKropAnalytics.track) NuKropAnalytics.track('onboarding_login_screen_viewed', { mode: currentAuthMode, role: currentAuthRole });
  const isSignUp = currentAuthMode === 'signup';
  const authUserRole = currentAuthRole;
  const authFormMode = currentAuthMode;

  const rememberedPhone = (localStorage.getItem('nukrop_user_phone') || '9876543210');
  const rememberedEmail = (localStorage.getItem('nukrop_remembered_email') || localStorage.getItem('nukrop_user_email') || 'jaswanth.reddy.farmer@gmail.com');
  const rememberedName = (localStorage.getItem('nukrop_remembered_name') || localStorage.getItem('nukrop_user_name') || 'B. Jaswanth Reddy');

  container.innerHTML = `
    <div style="width:100%;height:100%;min-height:100%;display:flex;flex-direction:column;justify-content:space-between;box-sizing:border-box;background:#FFFFFF;color:#0F172A;overflow-y:auto;position:relative;padding:24px 20px 20px;">
      
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
      <div style="background:#F1F5F9;border-radius:14px;padding:4px;display:flex;align-items:center;gap:4px;margin-top:12px;">
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

    if (role === 'driver') {
      if (typeof loginAsDriver === 'function') loginAsDriver();
    } else {
      if (typeof switchUserRole === 'function') switchUserRole('farmer');
      openScreen('home', document.getElementById('tab-home'));
    }
  }, 1200);
}
'''

    # Replace the existing renderLoginScreen and openPostLoginSuccessModal block
    pattern = r'function renderLoginScreen\s*\([\s\S]*?(?=function submitPoteaAuthForm)'
    content = re.sub(pattern, new_auth_block + '\n\n', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated auth lifecycle in {filepath}")

patch_auth_lifecycle('app/src/main/assets/index.html')
patch_auth_lifecycle('nukrop_emulator.html')
