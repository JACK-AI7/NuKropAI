# -*- coding: utf-8 -*-
import re

def patch_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f'Patching {filename} (len: {len(content)})...')

    # 1. Add updateBottomDockForRole function and wire it into openScreen & switchUserRole & loginAsDriver
    dock_fn_code = """
function updateBottomDockForRole() {
  const dockRow = document.querySelector('.dock-tab-row');
  const centerFab = document.querySelector('.notch-fab-circle') || document.getElementById('fab-scanner-btn');
  if (!dockRow) return;

  const role = localStorage.getItem('nukrop_user_role') || authUserRole || 'farmer';

  if (role === 'driver') {
    dockRow.innerHTML = `
      <!-- Left Side: Driver Cockpit & Haul Loads -->
      <div style="flex:2;display:flex;justify-content:space-around;padding-left:4px;">
        <div class="dock-tab-btn ${currentScreenKey==='driver_dashboard'?'active':''}" id="tab-driver-cockpit" onclick="openScreen('driver_dashboard',this)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:22px;height:22px;">
            <rect x="1" y="3" width="15" height="13"></rect>
            <polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon>
            <circle cx="5.5" cy="18.5" r="2.5"></circle>
            <circle cx="18.5" cy="18.5" r="2.5"></circle>
          </svg>
          <span id="tab-lbl-cockpit" style="font-size:10.5px;font-weight:700;">${currentLang==='te'?'కాక్‌పిట్':(currentLang==='hi'?'कॉकपिट':'Cockpit')}</span>
        </div>
        <div class="dock-tab-btn ${currentScreenKey==='gramhaul'?'active':''}" id="tab-driver-loads" onclick="openScreen('gramhaul',this)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:22px;height:22px;">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <polyline points="10 9 9 9 8 9"></polyline>
          </svg>
          <span id="tab-lbl-loads" style="font-size:10.5px;font-weight:700;">${currentLang==='te'?'ట్రిప్స్':(currentLang==='hi'?'ट्रिप्स':'Trips')}</span>
        </div>
      </div>

      <!-- Center Spacer for Floating Center FAB -->
      <div style="width:72px;flex-shrink:0;"></div>

      <!-- Right Side: Earnings & Driver Profile -->
      <div style="flex:2;display:flex;justify-content:space-around;padding-right:4px;">
        <div class="dock-tab-btn ${currentScreenKey==='khata'?'active':''}" id="tab-driver-earnings" onclick="openScreen('khata',this)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:22px;height:22px;">
            <line x1="12" y1="1" x2="12" y2="23"></line>
            <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
          </svg>
          <span id="tab-lbl-earnings" style="font-size:10.5px;font-weight:700;">${currentLang==='te'?'సంపాదన':(currentLang==='hi'?'कमाई':'Earnings')}</span>
        </div>
        <div class="dock-tab-btn ${currentScreenKey==='profile'?'active':''}" id="tab-driver-profile" onclick="openScreen('profile',this)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:22px;height:22px;">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
          <span id="tab-lbl-profile" style="font-size:10.5px;font-weight:700;">${currentLang==='te'?'ప్రొఫైల్':(currentLang==='hi'?'प्रोफ़ाइल':'Profile')}</span>
        </div>
      </div>
    `;
    if (centerFab) {
      centerFab.innerHTML = `
        <div onclick="showLuxuryToast('🗺️ GPS Turn-by-Turn Navigation Active', 'info')" style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg, #0F172A 0%, #1E293B 100%);border-radius:50%;box-shadow:0 6px 16px rgba(15,23,42,0.35);cursor:pointer;">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#22C55E" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="3 11 22 2 13 21 11 13 3 11"></polygon>
          </svg>
        </div>
      `;
    }
  } else {
    // FARMER DOCK
    dockRow.innerHTML = `
      <!-- Left Side: Home & Community -->
      <div style="flex:2;display:flex;justify-content:space-around;padding-left:4px;">
        <div class="dock-tab-btn ${currentScreenKey==='home'?'active':''}" id="tab-home" onclick="openScreen('home',this)">
          <svg viewBox="0 0 24 24" style="width:22px;height:22px;"><path d="M3 9.5L12 3l9 6.5V20a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V9.5z"/><path d="M9 22V12h6v10"/></svg>
          <span id="tab-lbl-home" style="font-size:10.5px;font-weight:700;">${currentLang==='te'?'హోమ్':(currentLang==='hi'?'होम':'Home')}</span>
        </div>
        <div class="dock-tab-btn ${currentScreenKey==='community'?'active':''}" id="tab-community" onclick="openScreen('community',this)">
          <svg viewBox="0 0 24 24" style="width:22px;height:22px;"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          <span id="tab-lbl-comm" style="font-size:10.5px;font-weight:700;">${currentLang==='te'?'రైతు వేదిక':(currentLang==='hi'?'किसान मंच':'Community')}</span>
        </div>
      </div>

      <!-- Center Spacer for FAB -->
      <div style="width:72px;flex-shrink:0;"></div>

      <!-- Right Side: Market & Profile -->
      <div style="flex:2;display:flex;justify-content:space-around;padding-right:4px;">
        <div class="dock-tab-btn ${currentScreenKey==='market'?'active':''}" id="tab-market" onclick="openScreen('market',this)">
          <svg viewBox="0 0 24 24" style="width:22px;height:22px;"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>
          <span id="tab-lbl-market" style="font-size:10.5px;font-weight:700;">${currentLang==='te'?'మార్కెట్':(currentLang==='hi'?'मंडी बाजार':'Market')}</span>
        </div>
        <div class="dock-tab-btn ${currentScreenKey==='profile'?'active':''}" id="tab-profile" onclick="openScreen('profile',this)">
          <svg viewBox="0 0 24 24" style="width:22px;height:22px;"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          <span id="tab-lbl-profile" style="font-size:10.5px;font-weight:700;">${currentLang==='te'?'ప్రొఫైల్':(currentLang==='hi'?'प्रोफ़ाइल':'Profile')}</span>
        </div>
      </div>
    `;
    if (centerFab) {
      centerFab.innerHTML = `
        <div onclick="openScreen('scanner', null)" style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg, #00A86B 0%, #059669 100%);border-radius:50%;box-shadow:0 6px 16px rgba(0,168,107,0.35);cursor:pointer;">
          ${typeof get4kLeafSvg === 'function' ? get4kLeafSvg(32) : '<span style="font-size:20px;color:#FFF;">🍃</span>'}
        </div>
      `;
    }
  }
}
"""

    if 'function updateBottomDockForRole' not in content:
        # insert before openScreen
        pos_os = content.find('function openScreen(')
        if pos_os != -1:
            content = content[:pos_os] + dock_fn_code + '\n\n' + content[pos_os:]
            print('Inserted updateBottomDockForRole function')

    # Ensure openScreen calls updateBottomDockForRole()
    if 'updateBottomDockForRole();' not in content:
        content = content.replace("if (screenKey === 'calc_budget') calcBudgetRoi();", "if (screenKey === 'calc_budget') calcBudgetRoi();\n  updateBottomDockForRole();")
        print('Hooked updateBottomDockForRole in openScreen')

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Finished patching {filename}')

patch_file('app/src/main/assets/index.html')
patch_file('nukrop_emulator.html')
