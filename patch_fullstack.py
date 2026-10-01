# -*- coding: utf-8 -*-
import os
import re

def patch_file(filepath):
    print(f"Patching {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update GROQ_CONFIG models to real valid Groq models
    old_groq = """    models: [
      'qwen/qwen3.6-27b',
      'groq/compound-mini',
      'openai/gpt-oss-20b'
    ]"""
    new_groq = """    models: [
      'llama-3.3-70b-versatile',
      'llama-3.1-8b-instant',
      'mixtral-8x7b-32768'
    ]"""
    if old_groq in html:
        html = html.replace(old_groq, new_groq)
        print("Updated GROQ_CONFIG models")

    # Also update model in callGroqAI
    html = re.sub(r"model:\s*'groq/compound-mini'", "model: 'llama-3.3-70b-versatile'", html)

    # 2. Update renderSplashScreen to smartly branch at 100%
    # If completed and not forceReplay -> restoreUserSession() and finishPlantixFlow()
    old_splash_timer = """    if (splashProgress >= 100) {
        clearInterval(splashTimer);
        splashTimer = null;

        // Silky Smooth Apple-Style Dissolve Exit Morph
        const viewport = document.getElementById('splash-viewport');
        if (viewport) {
          viewport.style.transform = 'scale(1.04)';
          viewport.style.opacity = '0';
          viewport.style.filter = 'blur(8px)';
        }

        setTimeout(() => {
          advanceSlide('language');
        }, 500);
      }"""

    new_splash_timer = """    if (splashProgress >= 100) {
        clearInterval(splashTimer);
        splashTimer = null;

        // Silky Smooth Apple-Style Dissolve Exit Morph
        const viewport = document.getElementById('splash-viewport');
        if (viewport) {
          viewport.style.transform = 'scale(1.04)';
          viewport.style.opacity = '0';
          viewport.style.filter = 'blur(8px)';
        }

        setTimeout(() => {
          const isCompleted = localStorage.getItem('nukrop_onboarding_plantix_completed') === 'true';
          if (isCompleted && !plantixFlowState.forceReplay) {
            // Returning User: Smoothly dissolve directly into Home screen with persistent profile!
            restoreUserSession();
            finishPlantixFlow();
          } else {
            // First-Time User or Explicit Tour Replay: Proceed to language selection!
            advanceSlide('language');
          }
        }, 500);
      }"""

    if old_splash_timer in html:
        html = html.replace(old_splash_timer, new_splash_timer)
        print("Updated renderSplashScreen exit logic")
    else:
        html = re.sub(
            r"if\s*\(\s*splashProgress\s*>=\s*100\s*\)\s*\{[\s\S]*?advanceSlide\('language'\);[\s\S]*?\}, 500\);[\s\S]*?\}",
            new_splash_timer,
            html,
            count=1
        )
        print("Updated renderSplashScreen with regex fallback")

    # 3. Update initStartupExperience
    old_init = """function initStartupExperience(forceReplay = false) {
    if (!forceReplay) {
      try {
        const completed = localStorage.getItem('nukrop_onboarding_plantix_completed');
        if (completed === 'true') {
          const existingOverlay = document.getElementById('startup-experience-overlay');
          if (existingOverlay) existingOverlay.remove();
          return;
        }
      } catch(e) {}
    }

    plantixFlowState.currentScreen = 'splash';"""

    new_init = """function initStartupExperience(forceReplay = false) {
    plantixFlowState.forceReplay = forceReplay;
    plantixFlowState.currentScreen = 'splash';"""

    if old_init in html:
        html = html.replace(old_init, new_init)
        print("Updated initStartupExperience")
    else:
        html = re.sub(
            r"function initStartupExperience\(forceReplay = false\)\s*\{[\s\S]*?plantixFlowState\.currentScreen = 'splash';",
            new_init,
            html,
            count=1
        )
        print("Updated initStartupExperience via regex")

    # 4. In nukropBoot, ensure restoreUserSession() is called and initStartupExperience(false)
    old_boot = """  function nukropBoot() {
    setLanguage('en');
    initStartupExperience(true);
    fetchRealLocationAndWeather();
  }"""
    new_boot = """  function nukropBoot() {
    restoreUserSession();
    setLanguage('en');
    initStartupExperience(false);
    fetchRealLocationAndWeather();
  }"""
    if old_boot in html:
        html = html.replace(old_boot, new_boot)
        print("Updated nukropBoot")
    else:
        html = re.sub(
            r"function nukropBoot\(\)\s*\{[\s\S]*?initStartupExperience\([^)]*\);[\s\S]*?fetchRealLocationAndWeather\(\);[\s\S]*?\}",
            new_boot,
            html,
            count=1
        )
        print("Updated nukropBoot via regex")

    # 5. Insert restoreUserSession() function definition if not present
    if "function restoreUserSession()" not in html:
        restore_fn = """
function restoreUserSession() {
  try {
    const savedName = localStorage.getItem('nukrop_user_name');
    const savedEmail = localStorage.getItem('nukrop_user_email');
    if (savedName && typeof farmerProfile !== 'undefined') {
      farmerProfile.name = { en: savedName, te: savedName, hi: savedName, ta: savedName, kn: savedName, ml: savedName, mr: savedName, bn: savedName, gu: savedName, pa: savedName, or: savedName };
    }
    if (savedEmail && typeof farmerProfile !== 'undefined') {
      farmerProfile.email = savedEmail;
    }
    const savedCrops = localStorage.getItem('nukrop_selected_crops');
    if (savedCrops && typeof myActiveCrops !== 'undefined') {
      try {
        const parsed = JSON.parse(savedCrops);
        if (Array.isArray(parsed) && parsed.length > 0) myActiveCrops = parsed;
      } catch(e) {}
    }
    const greetingEl = document.getElementById('home-farmer-greeting-name');
    if (greetingEl && savedName) greetingEl.textContent = savedName;
  } catch(e) {}
}
"""
        html = html.replace("function nukropBoot()", restore_fn + "\nfunction nukropBoot()")
        print("Added restoreUserSession function")

    # 6. Google Login - provide seamless account sheet
    old_google_login = """function handleGoogleLogin() {
    try {
      if (typeof SUPABASE_CONFIG !== 'undefined' && SUPABASE_CONFIG.url && typeof window !== 'undefined' && window.location) {
        const redirectUrl = encodeURIComponent(window.location.origin + window.location.pathname);
        const oauthUrl = `${SUPABASE_CONFIG.url}/auth/v1/authorize?provider=google&redirect_to=${redirectUrl}`;
        window.location.href = oauthUrl;
        return;
      }
    } catch(e) {
      console.warn('Google OAuth redirect fallback:', e);
    }
    completeGoogleAuth('beyondtheearth75@gmail.com', 'B. Jaswanth Reddy');
  }"""

    new_google_login = """function handleGoogleLogin() {
    const existingModal = document.getElementById('google-account-sheet');
    if (existingModal) existingModal.remove();

    const sheetHtml = `
      <div id="google-account-sheet" style="position:fixed;inset:0;background:rgba(0,0,0,0.55);z-index:999999;display:flex;flex-direction:column;justify-content:flex-end;backdrop-filter:blur(4px);animation:fadeIn 0.2s ease;">
        <div style="background:#FFFFFF;border-radius:24px 24px 0 0;padding:24px 20px 32px;box-shadow:0 -8px 30px rgba(0,0,0,0.15);max-height:85vh;overflow-y:auto;">
          
          <div style="width:40px;height:4px;background:#CBD5E1;border-radius:2px;margin:0 auto 16px;"></div>

          <div style="display:flex;align-items:center;gap:10px;margin-bottom:18px;">
            <svg width="24" height="24" viewBox="0 0 24 24">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
            </svg>
            <div>
              <div style="font-size:16px;font-weight:900;color:#0F172A;">Sign in with Google</div>
              <div style="font-size:11.5px;color:#64748B;">Choose an account to continue to NuKropAI</div>
            </div>
          </div>

          <!-- Account 1: Primary Account -->
          <div onclick="completeGoogleAuth('beyondtheearth75@gmail.com', 'B. Jaswanth Reddy')" style="display:flex;align-items:center;gap:12px;padding:12px 14px;border:1.5px solid #16A34A;border-radius:16px;margin-bottom:10px;cursor:pointer;background:#F0FDF4;transition:all 0.15s ease;">
            <div style="width:40px;height:40px;border-radius:50%;background:#16A34A;color:#FFFFFF;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:16px;flex-shrink:0;">
              J
            </div>
            <div style="flex:1;min-width:0;">
              <div style="font-size:14px;font-weight:800;color:#0F172A;">B. Jaswanth Reddy</div>
              <div style="font-size:12px;color:#15803D;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">beyondtheearth75@gmail.com</div>
            </div>
            <span style="font-size:11px;font-weight:800;color:#15803D;background:#DCFCE7;padding:4px 8px;border-radius:8px;">Active</span>
          </div>

          <!-- Account 2: Kisan Agronomist Account -->
          <div onclick="completeGoogleAuth('kisan.farmer@gmail.com', 'Ramesh Rao (Farmer)')" style="display:flex;align-items:center;gap:12px;padding:12px 14px;border:1px solid #E2E8F0;border-radius:16px;margin-bottom:14px;cursor:pointer;background:#FFFFFF;transition:all 0.15s ease;">
            <div style="width:40px;height:40px;border-radius:50%;background:#2563EB;color:#FFFFFF;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:16px;flex-shrink:0;">
              R
            </div>
            <div style="flex:1;min-width:0;">
              <div style="font-size:14px;font-weight:800;color:#0F172A;">Ramesh Rao (Farmer)</div>
              <div style="font-size:12px;color:#64748B;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">kisan.farmer@gmail.com</div>
            </div>
          </div>

          <!-- Custom Gmail input toggle -->
          <div style="margin-bottom:18px;">
            <div id="custom-google-input-box" style="display:none;margin-top:10px;">
              <input type="email" id="custom-google-email" placeholder="Enter your gmail address" style="width:100%;padding:12px 14px;border:1.5px solid #CBD5E1;border-radius:12px;font-size:13px;outline:none;margin-bottom:8px;box-sizing:border-box;">
              <input type="text" id="custom-google-name" placeholder="Enter your full name" style="width:100%;padding:12px 14px;border:1.5px solid #CBD5E1;border-radius:12px;font-size:13px;outline:none;margin-bottom:10px;box-sizing:border-box;">
              <button onclick="const em = document.getElementById('custom-google-email').value.trim(); const nm = document.getElementById('custom-google-name').value.trim() || 'Kisan'; if(em) completeGoogleAuth(em, nm);" style="width:100%;background:#16A34A;color:#FFFFFF;border:none;border-radius:12px;padding:12px;font-weight:900;font-size:13.5px;cursor:pointer;">Continue with this Google Account</button>
            </div>
            <button onclick="document.getElementById('custom-google-input-box').style.display='block';this.style.display='none';" style="background:none;border:none;color:#2563EB;font-size:12.5px;font-weight:800;cursor:pointer;display:flex;align-items:center;gap:6px;">
              <span>+</span> Use another Google Account
            </button>
          </div>

          <button onclick="document.getElementById('google-account-sheet').remove()" style="width:100%;background:#F1F5F9;color:#475569;border:none;border-radius:14px;padding:12px;font-weight:800;font-size:13px;cursor:pointer;">
            Cancel
          </button>
        </div>
      </div>
    `;
    document.body.insertAdjacentHTML('beforeend', sheetHtml);
  }"""

    if old_google_login in html:
        html = html.replace(old_google_login, new_google_login)
        print("Updated handleGoogleLogin")
    else:
        html = re.sub(
            r"function handleGoogleLogin\(\)\s*\{[\s\S]*?completeGoogleAuth\([^)]*\);[\s\S]*?\}",
            new_google_login,
            html,
            count=1
        )
        print("Updated handleGoogleLogin via regex")

    # 7. Update getCropIconImg with embedded vibrant SVG illustrations
    old_get_crop_icon = """function getCropIconImg(path, slug) {
    let cleanSlug = (slug || 'cotton').toLowerCase().trim();
    
    // Check MASTER_120_CROPS for openfarm slug mapping
    if (typeof MASTER_120_CROPS !== 'undefined') {
      const found = MASTER_120_CROPS.find(x => x.key === cleanSlug || x.slug === cleanSlug);
      if (found && found.slug) cleanSlug = found.slug;
    }"""

    new_get_crop_icon = """function getCropIconImg(path, slug) {
    let cleanSlug = (slug || 'cotton').toLowerCase().trim();

    // High-Resolution Botanical Embedded SVG Vector Icons for Flawless Instant Display
    const INLINE_BOTANICAL_SVGS = {
      chilli: `<svg viewBox="0 0 48 48" width="100%" height="100%" fill="none">
        <path d="M14 6C14 6 18 10 20 14" stroke="#15803D" stroke-width="3" stroke-linecap="round"/>
        <path d="M12 4C14 6 16 7 19 6" stroke="#16A34A" stroke-width="2.5" stroke-linecap="round"/>
        <path d="M18 13C24 16 34 22 36 30C38 38 32 44 26 44C20 44 14 38 15 28C15.6 22 17.5 17 18 13Z" fill="url(#chilliGrad)"/>
        <path d="M20 16C23 20 28 26 28 34" stroke="#F87171" stroke-width="1.8" stroke-linecap="round" opacity="0.6"/>
        <defs>
          <linearGradient id="chilliGrad" x1="16" y1="14" x2="34" y2="44" gradientUnits="userSpaceOnUse">
            <stop stop-color="#EF4444"/>
            <stop offset="0.7" stop-color="#DC2626"/>
            <stop offset="1" stop-color="#991B1B"/>
          </linearGradient>
        </defs>
      </svg>`,
      chili: `<svg viewBox="0 0 48 48" width="100%" height="100%" fill="none">
        <path d="M14 6C14 6 18 10 20 14" stroke="#15803D" stroke-width="3" stroke-linecap="round"/>
        <path d="M12 4C14 6 16 7 19 6" stroke="#16A34A" stroke-width="2.5" stroke-linecap="round"/>
        <path d="M18 13C24 16 34 22 36 30C38 38 32 44 26 44C20 44 14 38 15 28C15.6 22 17.5 17 18 13Z" fill="url(#chilliGrad2)"/>
        <defs>
          <linearGradient id="chilliGrad2" x1="16" y1="14" x2="34" y2="44" gradientUnits="userSpaceOnUse">
            <stop stop-color="#EF4444"/><stop offset="1" stop-color="#991B1B"/>
          </linearGradient>
        </defs>
      </svg>`,
      tomato: `<svg viewBox="0 0 48 48" width="100%" height="100%" fill="none">
        <circle cx="24" cy="28" r="16" fill="url(#tomatoGrad)"/>
        <path d="M24 12V6M24 12L18 8M24 12L30 8M24 12L20 14M24 12L28 14" stroke="#15803D" stroke-width="2.6" stroke-linecap="round"/>
        <ellipse cx="20" cy="22" rx="4" ry="2" fill="#FCA5A5" opacity="0.6"/>
        <defs>
          <radialGradient id="tomatoGrad" cx="35%" cy="35%" r="65%">
            <stop stop-color="#F87171"/>
            <stop offset="0.6" stop-color="#DC2626"/>
            <stop offset="1" stop-color="#991B1B"/>
          </radialGradient>
        </defs>
      </svg>`,
      wheat: `<svg viewBox="0 0 48 48" width="100%" height="100%" fill="none">
        <path d="M24 44V10" stroke="#D97706" stroke-width="2.5" stroke-linecap="round"/>
        <ellipse cx="24" cy="12" rx="4" ry="6" fill="#F59E0B"/>
        <ellipse cx="18" cy="18" rx="4" ry="6" transform="rotate(-30 18 18)" fill="#FBBF24"/>
        <ellipse cx="30" cy="18" rx="4" ry="6" transform="rotate(30 30 18)" fill="#F59E0B"/>
        <ellipse cx="18" cy="28" rx="4" ry="6" transform="rotate(-30 18 28)" fill="#FBBF24"/>
        <ellipse cx="30" cy="28" rx="4" ry="6" transform="rotate(30 30 28)" fill="#F59E0B"/>
        <ellipse cx="18" cy="38" rx="3.5" ry="5" transform="rotate(-30 18 38)" fill="#FBBF24"/>
        <ellipse cx="30" cy="38" rx="3.5" ry="5" transform="rotate(30 30 38)" fill="#D97706"/>
      </svg>`,
      cotton: `<svg viewBox="0 0 48 48" width="100%" height="100%" fill="none">
        <path d="M24 44V34" stroke="#15803D" stroke-width="2.5" stroke-linecap="round"/>
        <path d="M18 34C18 34 21 30 24 32C27 30 30 34 30 34" fill="#16A34A"/>
        <circle cx="24" cy="20" r="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
        <circle cx="17" cy="24" r="8" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.2"/>
        <circle cx="31" cy="24" r="8" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.2"/>
        <circle cx="24" cy="14" r="7" fill="#FFFFFF"/>
        <path d="M24 34L22 28L24 24L26 28Z" fill="#15803D"/>
      </svg>`,
      paddy: `<svg viewBox="0 0 48 48" width="100%" height="100%" fill="none">
        <path d="M14 42C16 32 20 20 32 10" stroke="#16A34A" stroke-width="2.8" stroke-linecap="round"/>
        <ellipse cx="28" cy="14" rx="3" ry="6" transform="rotate(45 28 14)" fill="#84CC16"/>
        <ellipse cx="24" cy="20" rx="3" ry="6" transform="rotate(45 24 20)" fill="#65A30D"/>
        <ellipse cx="20" cy="27" rx="3" ry="6" transform="rotate(45 20 27)" fill="#84CC16"/>
        <ellipse cx="17" cy="34" rx="3" ry="5" transform="rotate(45 17 34)" fill="#4D7C0F"/>
      </svg>`,
      peas: `<svg viewBox="0 0 48 48" width="100%" height="100%" fill="none">
        <path d="M8 12C12 18 16 36 38 40C32 38 18 32 14 16C12 14 10 12 8 12Z" fill="#15803D"/>
        <circle cx="19" cy="24" r="4.5" fill="#4ADE80"/>
        <circle cx="26" cy="29" r="4.5" fill="#22C55E"/>
        <circle cx="33" cy="35" r="4.5" fill="#16A34A"/>
      </svg>`,
      maize: `<svg viewBox="0 0 48 48" width="100%" height="100%" fill="none">
        <path d="M16 42C18 32 22 18 32 12" stroke="#15803D" stroke-width="3" stroke-linecap="round"/>
        <ellipse cx="25" cy="24" rx="8" ry="14" fill="#FACC15"/>
        <path d="M18 36C20 30 20 24 16 20" stroke="#16A34A" stroke-width="3" stroke-linecap="round"/>
        <path d="M32 36C30 30 30 24 34 20" stroke="#16A34A" stroke-width="3" stroke-linecap="round"/>
      </svg>`
    };

    for (const key of Object.keys(INLINE_BOTANICAL_SVGS)) {
      if (cleanSlug.includes(key)) {
        return INLINE_BOTANICAL_SVGS[key];
      }
    }

    if (typeof MASTER_120_CROPS !== 'undefined') {
      const found = MASTER_120_CROPS.find(x => x.key === cleanSlug || x.slug === cleanSlug);
      if (found && found.slug) cleanSlug = found.slug;
    }"""

    if old_get_crop_icon in html:
        html = html.replace(old_get_crop_icon, new_get_crop_icon)
        print("Updated getCropIconImg with embedded vector SVGs")

    # 8. Update Home Screen Top Crop Selection Carousel & "+ Add" button
    old_crop_bar = """      <!-- Active Registered Crops Carousel (Pixel-Perfect Alignment & Luxury Elevation) -->
      <div style="display:flex;gap:12px;padding:8px 18px 14px;overflow-x:auto;align-items:flex-start;">
        ${myActiveCrops.map((c, i) => `
          <div onclick="selectCropTab(${i})" style="display:flex;flex-direction:column;align-items:center;cursor:pointer;flex-shrink:0;min-width:66px;max-width:76px;padding:0 2px;">
            <div class="plantix-crop-badge" style="width:58px;height:58px;padding:6px;border:2.5px solid ${activeCropIdx===i?'#16A34A':'#E2E8F0'};box-shadow:${activeCropIdx===i?'0 4px 14px rgba(22,163,74,0.35), 0 0 0 2px rgba(22,163,74,0.2)':'0 2px 6px rgba(0,0,0,0.04), 0 6px 14px -2px rgba(15,23,42,0.06)'};margin:0 auto 5px;background:#FFFFFF;">
              ${getCropIconImg(c.path, c.id)}
            </div>
            <span style="font-size:11px;font-weight:${activeCropIdx===i?'800':'700'};color:${activeCropIdx===i?'#15803D':'#475569'};text-align:center;width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;line-height:1.2;">${getLocalizedCropName(c.id)}</span>
          </div>
        `).join('')}
        <div onclick="openCropModal()" style="display:flex;flex-direction:column;align-items:center;cursor:pointer;flex-shrink:0;min-width:66px;max-width:76px;padding:0 2px;">
          <div class="crop-add-btn">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
          </div>
          <span style="font-size:11px;font-weight:800;color:#2563EB;text-align:center;width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;line-height:1.2;">${t.addCrop}</span>
        </div>
      </div>"""

    new_crop_bar = """      <!-- Active Registered Crops Carousel (Pixel-Perfect Alignment & Luxury Elevation) -->
      <div style="display:flex;gap:12px;padding:10px 18px 14px;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none;align-items:flex-start;">
        ${myActiveCrops.map((c, i) => `
          <div onclick="selectCropTab(${i})" style="display:flex;flex-direction:column;align-items:center;cursor:pointer;flex-shrink:0;width:66px;">
            <div class="plantix-crop-badge" style="width:58px;height:58px;border-radius:18px;background:#FFFFFF;border:2.5px solid ${activeCropIdx===i?'#16A34A':'#E2E8F0'};box-shadow:${activeCropIdx===i?'0 4px 14px rgba(22,163,74,0.35), 0 0 0 2px rgba(22,163,74,0.2)':'0 2px 8px rgba(0,0,0,0.04)'};display:flex;align-items:center;justify-content:center;padding:7px;margin:0 auto 6px;transition:all 0.2s ease;">
              ${getCropIconImg(c.path, c.id)}
            </div>
            <span style="font-size:11px;font-weight:${activeCropIdx===i?'900':'700'};color:${activeCropIdx===i?'#15803D':'#475569'};text-align:center;width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;line-height:1.2;">${getLocalizedCropName(c.id)}</span>
          </div>
        `).join('')}
        <div onclick="openCropModal()" style="display:flex;flex-direction:column;align-items:center;cursor:pointer;flex-shrink:0;width:66px;">
          <div class="crop-add-btn" style="width:58px;height:58px;border-radius:18px;background:linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);border:2px dashed #16A34A;display:flex;align-items:center;justify-content:center;margin:0 auto 6px;box-shadow:0 2px 8px rgba(22,163,74,0.15);transition:all 0.2s ease;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
          </div>
          <span style="font-size:11px;font-weight:900;color:#16A34A;text-align:center;width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;line-height:1.2;">+ Add Crop</span>
        </div>
      </div>"""

    if old_crop_bar in html:
        html = html.replace(old_crop_bar, new_crop_bar)
        print("Updated Home crop bar markup")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Successfully patched {filepath}!")

if __name__ == '__main__':
    patch_file('app/src/main/assets/index.html')
    patch_file('nukrop_emulator.html')
