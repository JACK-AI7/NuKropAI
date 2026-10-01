import os
import re

files = ['app/src/main/assets/index.html', 'nukrop_emulator.html']
for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    new_profile = """profile: () => {
    const t = I18N[currentLang] || I18N.te;
    const isTe = currentLang === 'te';
    const isHi = currentLang === 'hi';

    const curName = farmerProfile.name[currentLang] || farmerProfile.name.en;
    const curVillage = farmerProfile.village[currentLang] || farmerProfile.village.en;

    return `
    <div style="background:#F3F4F6;min-height:100vh;padding-bottom:90px;">
      <!-- Profile hero -->
      <div style="background:#064E3B;padding:28px 20px 24px;border-radius:0 0 24px 24px;">
        <div style="display:flex;align-items:center;gap:16px;margin-bottom:18px;">
          <div style="width:64px;height:64px;border-radius:50%;background:#86EFAC;display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:900;color:#064E3B;flex-shrink:0;box-shadow:0 4px 12px rgba(134,239,172,0.3);">R</div>
          <div style="flex:1;">
            <div style="font-size:20px;font-weight:900;color:#FFFFFF;letter-spacing:-0.3px;">${curName}</div>
            <div style="font-size:12px;color:#A7F3D0;margin-top:2px;">ID: ${farmerProfile.farmerId}</div>
            <div style="font-size:12px;color:#A7F3D0;">📍 ${curVillage}</div>
          </div>
          <button onclick="switchUserRole('driver')" class="r-btn" style="background:rgba(134,239,172,0.12);border:1px solid rgba(134,239,172,0.3);border-radius:12px;padding:8px 12px;color:#86EFAC;font-size:11px;font-weight:800;cursor:pointer;text-align:center;">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" style="display:block;margin:0 auto 3px;"><path d="M5 17h14v-2H5v2zm0-4h14v-2H5v2zm0-4h14V7H5v2z"/><path d="M12 2L2 7l10 5 10-5-10-5z"/></svg>
            Driver View
          </button>
        </div>
        <!-- Rating row -->
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;">
          ${[['2.5','Land (Ac)','#86EFAC'],['850','Soil Health','#FFFFFF'],['A+','Grade','#FFFFFF']].map(([val,label,color])=>`
            <div style="background:rgba(255,255,255,0.12);border-radius:13px;padding:10px 12px;text-align:center;">
              <div style="font-size:20px;font-weight:900;color:${color};letter-spacing:-0.3px;">${val}</div>
              <div style="font-size:10px;color:#D1FAE5;font-weight:700;margin-top:2px;">${label}</div>
            </div>
          `).join('')}
        </div>
      </div>

      <!-- Menu items -->
      <div style="padding:16px 16px 0;">
        <div class="r-card" style="background:#FFFFFF;border-radius:20px;box-shadow:0 2px 14px rgba(0,0,0,0.07);overflow:hidden;margin-bottom:14px;">
          ${[
            ['M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2M9 5a2 2 0 0 0 2 2h2a2 2 0 0 0 2-2M9 5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2','AgriStack Identity','TS-WGL-8941 · Verified'],
            ['M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z','KCC Loan Status','Sanctioned: ₹1.25L'],
            ['M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 0-2-2z|M9 22V12h6v10','Farm Documents','RoR, Pattadar Passbook'],
            ['M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2|M23 21v-2a4 4 0 0 0-3-3.87|M16 3.13a4 4 0 0 1 0 7.75','Refer & Earn','₹500 per farmer referred'],
            ['M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0zm-5 0a4 4 0 1 1-8 0 4 4 0 0 1 8 0z','Help & Support','24/7 agriculture helpline'],
          ].map(([d,label,sub],i)=>`
            <button class="r-btn" style="width:100%;display:flex;align-items:center;gap:14px;padding:14px 18px;background:none;border:none;border-bottom:${i<4?'1px solid #F3F4F6':'none'};cursor:pointer;text-align:left;">
              <div style="width:40px;height:40px;border-radius:13px;background:#F8FAF8;border:1px solid #E2ECE2;display:flex;align-items:center;justify-content:center;flex-shrink:0;color:#064E3B;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">${d.split('|').map(p=>`<path d="${p}"/>`).join('')}</svg>
              </div>
              <div style="flex:1;">
                <div style="font-size:15px;font-weight:900;color:#0F172A;letter-spacing:-0.2px;">${label}</div>
                <div style="font-size:11.5px;color:#6B7280;font-weight:600;margin-top:2px;">${sub}</div>
              </div>
              <div style="color:#D1D5DB;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="9 18 15 12 9 6"/></svg>
              </div>
            </button>
          `).join('')}
        </div>
      </div>
    </div>
    `;
  },"""

    # Replace old profile block with new profile block
    start_idx = text.find('profile: () => {')
    end_idx = text.find('},', start_idx) + 2
    if start_idx != -1 and end_idx != -1:
        text = text[:start_idx] + new_profile + text[end_idx:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

print("Farmer profile modernized!")
