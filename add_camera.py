import re

def add_camera_perm_screen(path):
    with open(path, 'r', encoding='utf-8') as f:
        code = f.read()

    cam_func = """function renderCameraPermissionScreen(container) {
  NuKropAnalytics.track('onboarding_camera_permission');

  container.innerHTML = `
    <div style="width:100%;height:100%;display:flex;flex-direction:column;box-sizing:border-box;padding:24px;">
      <div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;">
        <div style="position:relative;width:260px;height:240px;margin:0 auto 16px;display:flex;align-items:center;justify-content:center;">
          <svg width="240" height="200" viewBox="0 0 240 200" fill="none">
            <rect x="30" y="30" width="180" height="140" rx="28" fill="#F0FDF4" stroke="#86EFAC" stroke-width="2"/>
            <rect x="45" y="45" width="150" height="110" rx="20" fill="#DCFCE7"/>
            <circle cx="120" cy="100" r="36" fill="#FFFFFF" stroke="#16A34A" stroke-width="3"/>
            <circle cx="120" cy="100" r="22" fill="#22C55E"/>
            <circle cx="112" cy="92" r="6" fill="#FFFFFF" opacity="0.8"/>
            <rect x="75" y="22" width="30" height="12" rx="4" fill="#16A34A"/>
            <circle cx="165" cy="65" r="5" fill="#EF4444"/>
          </svg>
        </div>

        <div style="font-size:22px;font-weight:900;color:#0F172A;letter-spacing:-0.4px;margin-bottom:8px;max-width:270px;line-height:1.3;">
          ${TL('AI Camera Scanner', 'కెమెరా అనుమతి', 'कैमरा स्कैनर अनुमति')}
        </div>
        <div style="font-size:13px;color:#64748B;font-weight:600;max-width:270px;line-height:1.45;margin-bottom:24px;">
          ${TL('Take photos of your crops or soil to get instant disease detection and organic treatment advice.', 'తక్షణ వ్యాధి నిర్ధారణ మరియు సేంద్రీయ నివారణ చర్యల కోసం పంట ఫోటోలను తీయండి.', 'रोग की तुरंत पहचान और जैविक उपचार के लिए फसलों की फोटो खींचें।')}
        </div>
      </div>

      <div style="padding:10px 0;display:flex;flex-direction:column;gap:10px;align-items:center;">
        <button onclick="grantCameraAndContinue()" style="width:100%;background:#16A34A;color:#FFFFFF;border:none;border-radius:24px;padding:14px;font-size:15px;font-weight:900;cursor:pointer;box-shadow:0 4px 14px rgba(22,163,74,0.3);letter-spacing:0.02em;">
          ${TL('Allow Camera Access', 'కెమెరా అనుమతించు', 'कैमरा चालू करें')}
        </button>
        <button onclick="advanceSlide('crops')" style="background:none;border:none;color:#64748B;font-size:13px;font-weight:800;cursor:pointer;padding:6px;">
          ${OB_TL('skip')}
        </button>
      </div>
    </div>
  `;
}
"""

    if "function renderCameraPermissionScreen" not in code:
        code = code.replace("function renderPlantixCropsScreen", cam_func + "\n\nfunction renderPlantixCropsScreen")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(code)

add_camera_perm_screen('app/src/main/assets/index.html')
add_camera_perm_screen('nukrop_emulator.html')
print("Successfully added renderCameraPermissionScreen!")
