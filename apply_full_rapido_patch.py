#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
apply_full_rapido_patch.py
Applies full Rapido UI clone optimizations to GramHaul in index.html and nukrop_emulator.html:
1. openScreen: hides .bottom-dock-wrap when entering gramhaul, gramhaul_tracking, driver_dashboard;
   and ensures #screen-container and #screen-body are height: 100%, flex: 1, overflow: hidden, paddingBottom: 0px.
2. selectGramhaulTruckTier: updates selection highlight across #gh-tier-1 to #gh-tier-5.
3. recalcGramhaulFare: dynamically updates the prominent booking button: "Book [Tier Name] · ₹[Total] ➔".
4. executeRealGramhaulDispatch: robustly handles fare and trip dispatching to live tracking.
5. renderTrackingDispatchedState: prominently displays the Start OTP card, driver details, and actions.
6. Ensures global variables (selectedGramhaulPrice, etc.) are declared.
"""
import os, sys, shutil

def patch_file(file_path):
    print(f"Patching {file_path}...")
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Backup
    bak = file_path + ".bak_rapido2"
    shutil.copy2(file_path, bak)

    # 1. Update openScreen to include gramhaul
    old_dock_check = """  if (screenKey === 'driver_dashboard' || screenKey === 'gramhaul_tracking') {
    if (dockWrap) dockWrap.style.display = 'none';
    if (screenContainer) {
      screenContainer.style.overflow = 'hidden';
      screenContainer.style.paddingBottom = '0px';
    }
    if (container) {
      container.style.height = '100%';
      container.style.display = 'flex';
      container.style.flexDirection = 'column';
    }
  } else {
    if (dockWrap) dockWrap.style.display = 'block';
    if (screenContainer) {
      screenContainer.style.overflow = '';
      screenContainer.style.paddingBottom = '';
    }
    if (container) {
      container.style.height = '';
      container.style.display = '';
      container.style.flexDirection = '';
    }
  }"""

    new_dock_check = """  if (screenKey === 'driver_dashboard' || screenKey === 'gramhaul' || screenKey === 'gramhaul_tracking') {
    if (dockWrap) dockWrap.style.display = 'none';
    if (screenContainer) {
      screenContainer.style.overflow = 'hidden';
      screenContainer.style.paddingBottom = '0px';
      screenContainer.style.height = '100%';
    }
    if (container) {
      container.style.height = '100%';
      container.style.display = 'flex';
      container.style.flexDirection = 'column';
      container.style.flex = '1';
      container.style.position = 'relative';
      container.style.overflow = 'hidden';
    }
  } else {
    if (dockWrap) dockWrap.style.display = 'block';
    if (screenContainer) {
      screenContainer.style.overflow = '';
      screenContainer.style.paddingBottom = '';
      screenContainer.style.height = '';
    }
    if (container) {
      container.style.height = '';
      container.style.display = '';
      container.style.flexDirection = '';
      container.style.flex = '';
      container.style.position = '';
      container.style.overflow = '';
    }
  }"""

    if old_dock_check in text:
        text = text.replace(old_dock_check, new_dock_check, 1)
        print("  [+] Patched openScreen dockWrap logic")
    else:
        alt_old = "if (screenKey === 'driver_dashboard' || screenKey === 'gramhaul_tracking')"
        if alt_old in text:
            text = text.replace(alt_old, "if (screenKey === 'driver_dashboard' || screenKey === 'gramhaul' || screenKey === 'gramhaul_tracking')", 1)
            print("  [+] Replaced alt_old dock check")

    # 2. Update selectGramhaulTruckTier
    old_select_fn = """function selectGramhaulTruckTier(tier) {
  selectedGramhaulTier = tier;
  document.querySelectorAll('#gh-truck-categories .gh-vehicle-card').forEach((el, idx) => {
    if (idx + 1 === tier) {
      el.classList.add('selected');
      el.style.borderColor = '#16A34A';
      el.style.background = '#F0FDF4';
    } else {
      el.classList.remove('selected');
      el.style.borderColor = '#E2E8F0';
      el.style.background = '#FFFFFF';
    }
  });
  recalcGramhaulFare();
  updateGramhaulSelectorMapVehicles(tier);
}"""

    new_select_fn = """function selectGramhaulTruckTier(tier) {
  selectedGramhaulTier = tier;
  for (let t = 1; t <= 5; t++) {
    const el = document.getElementById('gh-tier-' + t);
    if (el) {
      if (t === tier) {
        el.classList.add('selected');
        el.style.background = '#F0FDF4';
      } else {
        el.classList.remove('selected');
        el.style.background = '#FFFFFF';
      }
    }
  }
  recalcGramhaulFare();
  updateGramhaulSelectorMapVehicles(tier);
}"""

    if old_select_fn in text:
        text = text.replace(old_select_fn, new_select_fn, 1)
        print("  [+] Patched selectGramhaulTruckTier")

    # 3. Update recalcGramhaulFare to also update the booking CTA button
    old_recalc_fare = """  const fares = { 1: f1, 2: f2, 3: f3, 4: f4, 5: f5 };
  const total = fares[selectedGramhaulTier] || f1;
  selectedGramhaulPrice = total;
  const totalEl = document.getElementById('gh-total-fare');
  if (totalEl) totalEl.textContent = '₹' + total;
}"""

    new_recalc_fare = """  const fares = { 1: f1, 2: f2, 3: f3, 4: f4, 5: f5 };
  const total = fares[selectedGramhaulTier] || f1;
  selectedGramhaulPrice = total;
  const totalEl = document.getElementById('gh-total-fare');
  if (totalEl) totalEl.textContent = '₹' + total;

  const tierNames = {
    1: 'Tata Ace Gold',
    2: 'Mahindra Bolero Maxi',
    3: 'Ashok Leyland Dost+',
    4: 'Tata 407 Gold SFC',
    5: 'Eicher Pro 14ft'
  };
  const activeTierName = tierNames[selectedGramhaulTier] || 'Tata Ace Gold';
  const btn = document.getElementById('gh-confirm-booking-btn');
  if (btn) {
    btn.innerHTML = `<span style="display:flex;align-items:center;gap:8px;"><span>Book ${activeTierName}</span></span> <span style="background:rgba(255,255,255,0.22);padding:4px 12px;border-radius:8px;font-size:15px;font-weight:900;display:flex;align-items:center;gap:6px;"><span id="gh-btn-fare-display">₹${total}</span> <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></span>`;
  }
}"""

    if old_recalc_fare in text:
        text = text.replace(old_recalc_fare, new_recalc_fare, 1)
        print("  [+] Patched recalcGramhaulFare")

    # 4. Update executeRealGramhaulDispatch to be completely robust
    old_dispatch_fn = """function executeRealGramhaulDispatch() {
  const mandi = (typeof currentGramhaulMandi !== 'undefined') ? currentGramhaulMandi : { name: 'Gudimalkapur Vegetable & Flower APMC Yard', distKm: 7.2 };
  const crop = document.getElementById('gh-crop-select')?.value || 'Cotton';
  const sacks = document.getElementById('gh-weight-inp')?.value || '40';
  const v = GRAMHAUL_TIER_AVAILABLE_VEHICLES[selectedGramhaulTier] || GRAMHAUL_TIER_AVAILABLE_VEHICLES[1];
  const fare = selectedGramhaulPrice || 380;
  const bookId = 'GH-' + Math.floor(1000 + Math.random() * 9000);"""

    new_dispatch_fn = """function executeRealGramhaulDispatch() {
  const mandi = (typeof currentGramhaulMandi !== 'undefined' && currentGramhaulMandi) ? currentGramhaulMandi : (typeof REAL_APMC_MANDIS !== 'undefined' ? REAL_APMC_MANDIS[0] : { name: 'Gudimalkapur Vegetable & Flower APMC Yard', distKm: 7.2 });
  const crop = (document.getElementById('gh-crop-select')?.value) || (typeof selectedGramhaulCrop !== 'undefined' ? selectedGramhaulCrop : 'Cotton');
  const sacks = (document.getElementById('gh-weight-inp')?.value) || '40';
  const tier = (typeof selectedGramhaulTier !== 'undefined' && selectedGramhaulTier) ? selectedGramhaulTier : 1;
  const v = (typeof GRAMHAUL_TIER_AVAILABLE_VEHICLES !== 'undefined' && GRAMHAUL_TIER_AVAILABLE_VEHICLES[tier]) ? GRAMHAUL_TIER_AVAILABLE_VEHICLES[tier] : {
    name: 'Tata Ace Gold (1.5T)',
    driver: 'Suresh Yadav',
    phone: '+91 94401 55667',
    plate: 'TS 03 UB 4491',
    rating: '★ 4.9',
    coords: [17.3940, 78.4850],
    color: '#0284C7',
    etaMins: 2,
    otp: '4491'
  };
  const fare = (typeof selectedGramhaulPrice !== 'undefined' && selectedGramhaulPrice) ? selectedGramhaulPrice : 380;
  const bookId = 'GH-' + Math.floor(1000 + Math.random() * 9000);"""

    if old_dispatch_fn in text:
        text = text.replace(old_dispatch_fn, new_dispatch_fn, 1)
        print("  [+] Patched executeRealGramhaulDispatch")

    # 5. Prominent OTP in renderTrackingDispatchedState
    old_otp_section = """          <!-- 4 Circular Tactile Action Buttons -->"""
    new_otp_section = """          <!-- PROMINENT RAPIDO START TRIP OTP BADGE -->
          <div style="background:#FEF3C7;border:1.5px solid #F59E0B;border-radius:14px;padding:10px 14px;margin-bottom:14px;display:flex;align-items:center;justify-content:space-between;">
            <div>
              <div style="font-size:10px;font-weight:900;color:#92400E;text-transform:uppercase;letter-spacing:0.06em;">START TRIP PIN / OTP</div>
              <div style="font-size:11px;color:#78350F;margin-top:2px;">Share with driver only after loading sacks</div>
            </div>
            <div style="background:#F59E0B;color:#000000;font-size:22px;font-weight:900;letter-spacing:3px;padding:5px 12px;border-radius:8px;box-shadow:0 2px 6px rgba(245,158,11,0.3);">
              ${otp}
            </div>
          </div>

          <!-- 4 Circular Tactile Action Buttons -->"""

    if old_otp_section in text and "START TRIP PIN / OTP" not in text:
        text = text.replace(old_otp_section, new_otp_section, 1)
        print("  [+] Added prominent OTP badge to tracking sheet")

    # 6. Global variable declarations
    global_vars = 'var selectedGramhaulPrice = 380;\nvar selectedGramhaulTier = 1;\nvar selectedGramhaulCrop = "Cotton";\nvar selectedGramhaulWeight = "40 Sacks";\n'
    if "var selectedGramhaulPrice = 380;" not in text:
        target_pos = text.find("const GRAMHAUL_TIER_AVAILABLE_VEHICLES =")
        if target_pos != -1:
            text = text[:target_pos] + global_vars + text[target_pos:]
            print("  [+] Added global variables")

    # 7. Add Leaflet map invalidateSize to initGramhaulRealMap
    old_map_init_end = "updateGramhaulSelectorMapVehicles(selectedGramhaulTier || 1);"
    new_map_init_end = """updateGramhaulSelectorMapVehicles(selectedGramhaulTier || 1);
    setTimeout(() => { if (gramhaulLiveMap) gramhaulLiveMap.invalidateSize(); }, 120);"""
    if old_map_init_end in text and "gramhaulLiveMap.invalidateSize()" not in text:
        text = text.replace(old_map_init_end, new_map_init_end, 1)
        print("  [+] Added gramhaulLiveMap.invalidateSize() on init")

    # 8. Enhance bottom sheet button container in APP_VIEWS.gramhaul
    old_btn_container = """        <!-- CTA: edge-to-edge green -->
        <div style="padding:12px 16px max(20px,env(safe-area-inset-bottom,20px));flex-shrink:0;background:#FFFFFF;border-top:1px solid #F1F5F9;">
          <button id="gh-confirm-booking-btn" onclick="executeRealGramhaulDispatch()"
            style="width:100%;height:52px;background:#16A34A;color:#FFFFFF;border:none;border-radius:14px;font-size:15.5px;font-weight:900;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;box-shadow:0 4px 18px rgba(22,163,74,0.4);">
            <span>Book Mandi Truck</span>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
          </button>
        </div>"""

    new_btn_container = """        <!-- Payment & Transparent Fare strip -->
        <div style="display:flex;align-items:center;justify-content:space-between;padding:8px 16px;border-top:1px solid #F1F5F9;background:#FAFAFA;font-size:11.5px;flex-shrink:0;">
          <div style="display:flex;align-items:center;gap:6px;color:#0F172A;font-weight:700;">
            <span>💵</span>
            <span>Cash / UPI to Driver directly</span>
          </div>
          <div style="color:#16A34A;font-weight:800;display:flex;align-items:center;gap:4px;">
            <span>🛡️ 0% Commission</span>
          </div>
        </div>

        <!-- CTA: edge-to-edge Rapido Button -->
        <div style="padding:10px 16px max(18px,env(safe-area-inset-bottom,18px));flex-shrink:0;background:#FFFFFF;">
          <button id="gh-confirm-booking-btn" onclick="executeRealGramhaulDispatch()"
            style="width:100%;height:52px;background:#16A34A;color:#FFFFFF;border:none;border-radius:14px;font-size:15.5px;font-weight:900;cursor:pointer;display:flex;align-items:center;justify-content:space-between;padding:0 18px;box-shadow:0 4px 18px rgba(22,163,74,0.38);transition:all 0.15s ease;">
            <span style="display:flex;align-items:center;gap:8px;">
              <span>Book Tata Ace Gold</span>
            </span>
            <span style="background:rgba(255,255,255,0.22);padding:4px 12px;border-radius:8px;font-size:15px;font-weight:900;display:flex;align-items:center;gap:6px;">
              <span id="gh-btn-fare-display">₹380</span>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
            </span>
          </button>
        </div>"""

    if old_btn_container in text:
        text = text.replace(old_btn_container, new_btn_container, 1)
        print("  [+] Enhanced CTA button and payment strip in APP_VIEWS.gramhaul")

    # 9. Improve produce chips row in top route card
    old_cargo_row = """          <!-- cargo row: crop + sacks inline -->
          <div style="display:flex;align-items:center;gap:10px;padding:8px 14px 10px;border-top:1px solid #F1F5F9;background:#FAFAFA;">
            <div onclick="openGramhaulCropSelectorModal()" style="flex:1;display:flex;align-items:center;gap:7px;cursor:pointer;min-width:0;">
              <div id="gh-selected-crop-icon" style="width:22px;height:22px;flex-shrink:0;">${getCropIconImg(null, currentCropSlug)}</div>
              <span id="gh-selected-crop-label" style="font-size:12.5px;font-weight:800;color:#0F172A;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${getLocalizedCropName(currentCropSlug)}</span>
              <input type="hidden" id="gh-crop-select" value="${currentCropSlug}" />
              <span style="font-size:10px;color:#16A34A;font-weight:700;">▾</span>
            </div>
            <div style="width:1px;height:18px;background:#E2E8F0;flex-shrink:0;"></div>
            <div style="display:flex;align-items:center;gap:4px;flex-shrink:0;">
              <span style="font-size:13px;">📦</span>
              <input id="gh-weight-inp" type="number" value="40" min="1" max="500" oninput="recalcGramhaulFare()"
                style="width:44px;border:none;background:transparent;font-size:12.5px;font-weight:800;color:#0F172A;outline:none;text-align:center;" />
              <span style="font-size:11px;color:#64748B;font-weight:600;">Sacks</span>
            </div>
          </div>"""

    new_cargo_row = """          <!-- cargo row: crop + sacks inline (Rapido-style chips) -->
          <div style="display:flex;align-items:center;gap:8px;padding:8px 12px 10px;border-top:1px solid #F1F5F9;background:#F8FAFC;">
            <div onclick="openGramhaulCropSelectorModal()" style="flex:1;display:flex;align-items:center;gap:7px;cursor:pointer;min-width:0;background:#FFFFFF;border:1px solid #E2E8F0;border-radius:10px;padding:5px 10px;box-shadow:0 1px 3px rgba(0,0,0,0.04);">
              <div id="gh-selected-crop-icon" style="width:20px;height:20px;flex-shrink:0;display:flex;align-items:center;justify-content:center;">${getCropIconImg(null, currentCropSlug)}</div>
              <span id="gh-selected-crop-label" style="font-size:12px;font-weight:800;color:#0F172A;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex:1;">${getLocalizedCropName(currentCropSlug)}</span>
              <input type="hidden" id="gh-crop-select" value="${currentCropSlug}" />
              <span style="font-size:11px;color:#16A34A;font-weight:900;">▾</span>
            </div>
            <div style="display:flex;align-items:center;gap:4px;flex-shrink:0;background:#FFFFFF;border:1px solid #E2E8F0;border-radius:10px;padding:4px 8px;box-shadow:0 1px 3px rgba(0,0,0,0.04);">
              <span style="font-size:13px;">📦</span>
              <input id="gh-weight-inp" type="number" value="40" min="1" max="500" oninput="recalcGramhaulFare()"
                style="width:38px;border:none;background:transparent;font-size:12.5px;font-weight:900;color:#0F172A;outline:none;text-align:center;padding:0;" />
              <span style="font-size:11px;color:#64748B;font-weight:700;">Sacks</span>
            </div>
          </div>"""

    if old_cargo_row in text:
        text = text.replace(old_cargo_row, new_cargo_row, 1)
        print("  [+] Polished cargo row pills")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Done patching {file_path}.\n")

patch_file("app/src/main/assets/index.html")
patch_file("nukrop_emulator.html")
