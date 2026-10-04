#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
restore_and_perfect_gramhaul.py
Restores and perfects the GramHaul first screen to match v2_02_gramhaul_selector_tier1.png EXACTLY:
1. Top 38% dedicated Leaflet OSM map with back button, center pill (గ్రామ్‌హౌల్ మండి రవాణా / GramHaul Mandi Dispatch),
   receipts, GPS location edit button, 10km proximity geofenced pill, and real vehicle pins on map.
2. Bottom 62% clean scrollable booking card with 24px rounded top corners:
   - FROM -> TO Route Card with vertical dashed timeline and 'మార్చు ✏️' button.
   - CROP COMMODITY (🌾 పత్తి ▾) and BAGS / SACKS (40) side-by-side.
   - 5 Commercial Truck Cards (Tata Ace Gold, Mahindra Bolero, Ashok Leyland Dost+, Tata 407, Eicher Pro 14ft)
     with colored badge icons, detailed subtitles, live fares, and status tags.
   - Transparent Mandi Freight breakdown card.
   - Prominent green 'Request Mandi Truck Now →' CTA button.
   - Crucially: padding-bottom: 130px; so that when scrolled, the button and fare card scroll ALL THE WAY UP,
     comfortably clear of the bottom dock with plenty of space to see and tap!
3. Dock display logic:
   - gramhaul: dock is VISIBLE (display: block/flex) exactly as in v2_02_gramhaul_selector_tier1.png.
   - gramhaul_tracking: dock is HIDDEN (display: none) for fullscreen live GPS tracking.
   - driver_dashboard: dock is HIDDEN (has its own cockpit nav).
4. No variable declaration collisions (SyntaxError free).
"""

import sys, shutil

def apply_to_file(file_path):
    print(f"Applying to {file_path}...")
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Backup
    shutil.copy2(file_path, file_path + ".bak_v2")

    # 1. Ensure global variable selectedGramhaulPrice is declared cleanly without redeclaring crop/weight
    # Remove any problematic declarations if present
    bad_decl = 'var selectedGramhaulPrice = 380;\nvar selectedGramhaulTier = 1;\nvar selectedGramhaulCrop = "Cotton";\nvar selectedGramhaulWeight = "40 Sacks";\n'
    clean_decl = 'var selectedGramhaulPrice = 380;\nvar selectedGramhaulTier = 1;\n'
    if bad_decl in text:
        text = text.replace(bad_decl, clean_decl)
        print("  [+] Cleaned duplicate variable declarations")
    elif "var selectedGramhaulPrice = 380;" not in text:
        target_pos = text.find("const GRAMHAUL_TIER_AVAILABLE_VEHICLES =")
        if target_pos != -1:
            text = text[:target_pos] + clean_decl + text[target_pos:]
            print("  [+] Added clean global variables")

    # 2. Update openScreen dock handling:
    # On 'gramhaul', dockWrap MUST be visible (display: 'block') so it matches v2_02_gramhaul_selector_tier1.png!
    # On 'gramhaul_tracking' or 'driver_dashboard', dockWrap is hidden!
    old_dock_patterns = [
        """  if (screenKey === 'driver_dashboard' || screenKey === 'gramhaul' || screenKey === 'gramhaul_tracking') {
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
  }""",
        """  if (screenKey === 'driver_dashboard' || screenKey === 'gramhaul_tracking') {
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
  }"""
    ]

    target_dock_block = """  if (screenKey === 'driver_dashboard' || screenKey === 'gramhaul_tracking') {
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
  } else if (screenKey === 'gramhaul') {
    if (dockWrap) dockWrap.style.display = 'block';
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
  }"""

    replaced_dock = False
    for pat in old_dock_patterns:
        if pat in text:
            text = text.replace(pat, target_dock_block, 1)
            replaced_dock = True
            print("  [+] Successfully updated openScreen dock & layout logic for gramhaul")
            break

    if not replaced_dock:
        print("  [!] Direct dock pattern match failed, checking if already updated...")

    # 3. Splice APP_VIEWS.gramhaul to match v2_02_gramhaul_selector_tier1.png EXACTLY!
    V2_GRAMHAUL_CODE = r"""/* ── 4. MANDI TRUCK SHARING ── */

  /* ── 2. GRAMHAUL LOGISTICS: 38% VISIBLE MAP + PRO TRUCK CATEGORIES (MATCHING v2_02_gramhaul_selector_tier1) ── */
  gramhaul: () => {
    const t = I18N[currentLang] || I18N.en;
    setTimeout(initGramhaulRealMap, 80);

    const farmAddr = currentGramhaulFarmAddress || "Himayath Nagar Farm, Telangana";
    const mandi = currentGramhaulMandi || (typeof REAL_APMC_MANDIS !== 'undefined' ? REAL_APMC_MANDIS[0] : {name:'Gudimalkapur Vegetable & Flower APMC Yard', shortName:'Gudimalkapur APMC', distKm:7.2, tag:'7.2 km · Nearest', id:'gudimalkapur'});
    const mandiList = typeof REAL_APMC_MANDIS !== 'undefined' ? REAL_APMC_MANDIS : [
      { id: 'gudimalkapur', name: 'Gudimalkapur APMC', shortName: 'Gudimalkapur APMC', distKm: 7.2, tag: '7.2 km · Nearest' },
      { id: 'bowenpally', name: 'Bowenpally Wholesale APMC', shortName: 'Bowenpally APMC', distKm: 9.8, tag: '9.8 km' },
      { id: 'moinabad', name: 'Moinabad Regional APMC', shortName: 'Moinabad APMC', distKm: 24.5, tag: '24.5 km' }
    ];

    const currentCropSlug = typeof selectedGramhaulCropSlug !== 'undefined' ? selectedGramhaulCropSlug : 'cotton';

    return `
    <style>
    .gh-vehicle-card { transition: all 0.18s ease; border: 1.5px solid #E2E8F0; background: #FFFFFF; border-radius: 18px; padding: 12px 16px; cursor: pointer; display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }
    .gh-vehicle-card:active { transform: scale(0.98); }
    .gh-vehicle-card.selected { border-color: #22C55E !important; background: #F0FDF4 !important; box-shadow: 0 4px 14px rgba(34,197,94,0.18) !important; }
    </style>

    <div style="position:relative;width:100%;height:100%;display:flex;flex-direction:column;background:#F8FAF8;overflow:hidden;font-family:'Plus Jakarta Sans',-apple-system,BlinkMacSystemFont,sans-serif;">
      
      <!-- TOP 38%: DEDICATED UNOBSTRUCTED LEAFLET OSM MAP -->
      <div style="position:relative;width:100%;height:38vh;min-height:230px;background:#E5EFE5;flex-shrink:0;overflow:hidden;">
        
        <!-- Interactive Leaflet Map -->
        <div id="gramhaul-real-osm-map" style="position:absolute;inset:0;width:100%;height:100%;z-index:1;"></div>
        
        <!-- Top Bar with Safe Area -->
        <div style="position:absolute;top:max(14px, calc(var(--sat) - 20px));left:12px;right:12px;display:flex;justify-content:space-between;align-items:center;z-index:20;">
          <button onclick="openScreen(authUserRole==='driver'?'driver_dashboard':'home',null);updateBottomDockForRole()" style="background:#FFFFFF;border:none;width:40px;height:40px;border-radius:13px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 14px rgba(0,0,0,0.14);cursor:pointer;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#0F172A" stroke-width="2.5" stroke-linecap="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
          </button>
          <div style="background:rgba(255,255,255,0.95);backdrop-filter:blur(8px);padding:7px 16px;border-radius:999px;box-shadow:0 4px 14px rgba(0,0,0,0.12);display:flex;align-items:center;gap:6px;">
            <span style="font-size:15px;">🚜</span>
            <span style="font-size:13.5px;font-weight:900;color:#16A34A;">${TL('GramHaul Mandi Dispatch', 'గ్రామ్‌హౌల్ మండి రవాణా', 'ग्रामहॉल मंडी परिवहन')}</span>
          </div>
          <div style="display:flex;align-items:center;gap:6px;">
            <button onclick="openPreviousRidesModal()" title="Ride History" style="background:#FFFFFF;border:1px solid #E2E8F0;width:40px;height:40px;border-radius:13px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 14px rgba(0,0,0,0.12);cursor:pointer;font-size:17px;">
              🧾
            </button>
            <button onclick="openGramhaulPickupLocationModal()" title="Edit Pickup" style="background:#16A34A;border:none;width:40px;height:40px;border-radius:13px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 14px rgba(22,163,74,0.35);cursor:pointer;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"><circle cx="12" cy="10" r="3"/><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/></svg>
            </button>
          </div>
        </div>

        <!-- Live GPS Dispatch Pill -->
        <div style="position:absolute;bottom:10px;left:12px;z-index:20;background:rgba(15,23,42,0.85);backdrop-filter:blur(6px);color:#FFFFFF;padding:5px 12px;border-radius:999px;font-size:10.5px;font-weight:800;display:flex;align-items:center;gap:6px;box-shadow:0 2px 10px rgba(0,0,0,0.25);">
          <span style="width:7px;height:7px;border-radius:50%;background:#4ADE80;box-shadow:0 0 6px #4ADE80;"></span>
          ${TL('10 KM Proximity Geofenced', '10 కి.మీ పరిధిలో వాహనాలు', '10 किमी दायरे में वाहन')}
        </div>
      </div>

      <!-- BOTTOM 62%: CLEAN SCROLLABLE BOOKING CARD -->
      <div style="flex:1;background:#FFFFFF;border-radius:24px 24px 0 0;box-shadow:0 -6px 24px rgba(0,0,0,0.08);overflow-y:auto;padding:16px 18px 140px;box-sizing:border-box;">
        
        <!-- ROUTE CARD: FROM -> TO WITH PERFECT VERTICAL TIMELINE -->
        <div style="background:#FFFFFF;border:1.5px solid #E2E8F0;border-radius:18px;padding:14px 16px;margin-bottom:14px;box-shadow:0 2px 10px rgba(0,0,0,0.03);">
          <div style="display:flex;gap:12px;">
            <!-- Left Vertical Timeline Track (Perfect Alignment) -->
            <div style="display:flex;flex-direction:column;align-items:center;width:16px;padding-top:4px;flex-shrink:0;">
              <!-- Green Pickup Dot -->
              <div style="width:12px;height:12px;border-radius:50%;background:#16A34A;border:2.5px solid #DCFCE7;box-shadow:0 0 0 1px #16A34A;flex-shrink:0;"></div>
              <!-- Vertical Dashed Connecting Line -->
              <div style="width:2px;height:38px;background:repeating-linear-gradient(to bottom, #94A3B8 0, #94A3B8 4px, transparent 4px, transparent 8px);margin:3px 0;"></div>
              <!-- Red Drop Square Pin -->
              <div style="width:12px;height:12px;border-radius:3px;background:#DC2626;border:2.5px solid #FEE2E2;box-shadow:0 0 0 1px #DC2626;flex-shrink:0;"></div>
            </div>

            <!-- Right Content Rows -->
            <div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:10px;">
              <!-- Pickup Farm Row -->
              <div style="display:flex;align-items:center;justify-content:space-between;gap:8px;">
                <div style="flex:1;min-width:0;">
                  <div style="font-size:9.5px;color:#64748B;font-weight:800;letter-spacing:0.04em;text-transform:uppercase;">${TL('FROM (PICKUP FARM)', 'నుండి (పొలం చిరునామా)', 'से (खेत का पता)')}</div>
                  <div id="gh-pickup-location-label" style="font-size:13px;font-weight:900;color:#0F172A;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-top:1px;">${farmAddr}</div>
                </div>
                <button onclick="openGramhaulPickupLocationModal()" style="background:#F0FDF4;color:#15803D;border:1px solid #BBF7D0;border-radius:10px;padding:5px 12px;font-size:11px;font-weight:900;cursor:pointer;flex-shrink:0;transition:all 0.15s ease;">${TL('Edit ✏️', 'మార్చు ✏️', 'बदलें ✏️')}</button>
              </div>

              <!-- Content Separator -->
              <div style="height:1px;background:#F1F5F9;"></div>

              <!-- Destination Drop Mandi Row -->
              <div style="flex:1;min-width:0;">
                <div style="font-size:9.5px;color:#64748B;font-weight:800;letter-spacing:0.04em;text-transform:uppercase;">${TL('TO (DESTINATION APMC MANDI)', 'చేరుకోవాల్సిన మండి (APMC)', 'मंडी गंतव्य (APMC)')}</div>
                <div style="display:flex;align-items:center;gap:6px;margin-top:1px;">
                  <select id="gh-mandi-select" onchange="updateGramhaulMandi(this.value)" style="width:100%;border:none;background:transparent;font-size:13.5px;font-weight:900;color:#0F172A;outline:none;cursor:pointer;padding:0;letter-spacing:-0.2px;">
                    ${mandiList.map((m,i) => `<option value="${i}">${m.shortName} · ${m.distKm} km</option>`).join('')}
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- COMMODITY SPECS: 140+ CROPS MODAL PICKER + SACKS -->
        <div style="display:grid;grid-template-columns:1.2fr 1fr;gap:10px;margin-bottom:12px;">
          <div>
            <div style="font-size:10px;font-weight:800;color:#475569;text-transform:uppercase;margin-bottom:4px;">${TL('🌱 Crop Commodity', '🌱 పంట రకం', '🌱 फसल का प्रकार')}</div>
            <div onclick="openGramhaulCropSelectorModal()" style="width:100%;height:44px;background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:12px;padding:0 10px;display:flex;align-items:center;justify-content:space-between;cursor:pointer;box-sizing:border-box;">
              <div style="display:flex;align-items:center;gap:8px;min-width:0;">
                <div id="gh-selected-crop-icon" style="width:24px;height:24px;flex-shrink:0;">${getCropIconImg(null, currentCropSlug)}</div>
                <span id="gh-selected-crop-label" style="font-size:12.5px;font-weight:900;color:#0F172A;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${getLocalizedCropName(currentCropSlug)}</span>
              </div>
              <span style="font-size:10px;color:#16A34A;font-weight:800;flex-shrink:0;">▾</span>
            </div>
            <input type="hidden" id="gh-crop-select" value="${currentCropSlug}" />
          </div>
          <div>
            <div style="font-size:10px;font-weight:800;color:#475569;text-transform:uppercase;margin-bottom:4px;">${TL('📦 Bags / Sacks', '📦 బస్తాల సంఖ్య', '📦 बोरी / कट्टे')}</div>
            <input id="gh-weight-inp" type="number" value="40" min="1" max="500" oninput="recalcGramhaulFare()" style="width:100%;height:44px;background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:12px;padding:0 12px;font-size:13px;font-weight:800;color:#0F172A;outline:none;box-sizing:border-box;" placeholder="e.g. 40" />
          </div>
        </div>

        <!-- REAL COMMERCIAL TRUCK FLEET (5 REALISTIC VEHICLE TIERS) -->
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
          <div style="font-size:10.5px;font-weight:800;color:#475569;text-transform:uppercase;letter-spacing:0.4px;">${TL('🚚 Choose Commercial Truck', '🚚 వాహనాన్ని ఎంచుకోండి', '🚚 वाणिज्यिक ट्रक चुनें')}</div>
          <span style="font-size:10px;color:#16A34A;font-weight:800;">${TL('5 Verified Tiers', '5 ధృవీకరించిన రకాలు', '5 सत्यापित श्रेणियां')}</span>
        </div>
        
        <div style="display:flex;flex-direction:column;gap:6px;margin-bottom:14px;" id="gh-truck-categories">
          
          <!-- Truck 1: Tata Ace Gold -->
          <div onclick="selectGramhaulTruckTier(1)" id="gh-tier-1" class="gh-vehicle-card ${selectedGramhaulTier===1?'selected':''}">
            <div style="display:flex;align-items:center;gap:12px;">
              <div style="width:52px;height:42px;border-radius:12px;background:#DCFCE7;padding:4px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                <svg viewBox="0 0 70 44" style="width:100%;height:100%;"><rect x="4" y="16" width="36" height="18" rx="2" fill="#E2E8F0" stroke="#0F172A" stroke-width="1.8"/><path d="M40 18h16l8 10v6H40V18z" fill="#0284C7" stroke="#0F172A" stroke-width="1.8"/><path d="M45 20h9l5 7h-14V20z" fill="#E0F2FE"/><circle cx="16" cy="34" r="5" fill="#1E293B" stroke="#0F172A" stroke-width="1.5"/><circle cx="16" cy="34" r="2" fill="#94A3B8"/><circle cx="54" cy="34" r="5" fill="#1E293B" stroke="#0F172A" stroke-width="1.5"/><circle cx="54" cy="34" r="2" fill="#94A3B8"/><line x1="4" y1="23" x2="40" y2="23" stroke="#CBD5E1" stroke-width="1.5"/><circle cx="62" cy="30" r="1.5" fill="#FBBF24"/></svg>
              </div>
              <div>
                <div style="font-size:13px;font-weight:900;color:#0F172A;">Tata Ace Gold (1.5 Ton)</div>
                <div style="font-size:10.5px;color:#64748B;font-weight:600;">Up to 25 Qtl · 50 Sacks · Chota Hathi</div>
              </div>
            </div>
            <div style="text-align:right;">
              <div id="gh-fare-tier-1" style="font-size:15px;font-weight:900;color:#0F172A;">₹380</div>
              <div style="font-size:9.5px;color:#16A34A;font-weight:800;">✓ Ready</div>
            </div>
          </div>

          <!-- Truck 2: Bolero Maxi Truck -->
          <div onclick="selectGramhaulTruckTier(2)" id="gh-tier-2" class="gh-vehicle-card ${selectedGramhaulTier===2?'selected':''}">
            <div style="display:flex;align-items:center;gap:12px;">
              <div style="width:52px;height:42px;border-radius:12px;background:#EFF6FF;padding:4px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                <svg viewBox="0 0 70 44" style="width:100%;height:100%;"><rect x="4" y="14" width="38" height="20" rx="2" fill="#F8FAFC" stroke="#0F172A" stroke-width="1.8"/><path d="M42 16h14l8 8v10H42V16z" fill="#DC2626" stroke="#0F172A" stroke-width="1.8"/><path d="M46 18h8l6 6h-14V18z" fill="#FEE2E2"/><circle cx="16" cy="34" r="5.5" fill="#1E293B" stroke="#0F172A" stroke-width="1.5"/><circle cx="16" cy="34" r="2.2" fill="#E2E8F0"/><circle cx="54" cy="34" r="5.5" fill="#1E293B" stroke="#0F172A" stroke-width="1.5"/><circle cx="54" cy="34" r="2.2" fill="#E2E8F0"/><rect x="6" y="8" width="34" height="6" fill="#64748B" rx="1"/><circle cx="62" cy="28" r="1.5" fill="#FEF08A"/></svg>
              </div>
              <div>
                <div style="font-size:13px;font-weight:900;color:#0F172A;">Mahindra Bolero Maxi (2.5 Ton)</div>
                <div style="font-size:10.5px;color:#64748B;font-weight:600;">Up to 50 Qtl · 100 Sacks · Heavy Produce</div>
              </div>
            </div>
            <div style="text-align:right;">
              <div id="gh-fare-tier-2" style="font-size:15px;font-weight:900;color:#0F172A;">₹560</div>
              <div style="font-size:9.5px;color:#2563EB;font-weight:800;">Available</div>
            </div>
          </div>

          <!-- Truck 3: Ashok Leyland Dost+ -->
          <div onclick="selectGramhaulTruckTier(3)" id="gh-tier-3" class="gh-vehicle-card ${selectedGramhaulTier===3?'selected':''}">
            <div style="display:flex;align-items:center;gap:12px;">
              <div style="width:52px;height:42px;border-radius:12px;background:#F0FDF4;padding:4px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                <svg viewBox="0 0 70 44" style="width:100%;height:100%;"><rect x="4" y="14" width="38" height="20" rx="2" fill="#E2E8F0" stroke="#0F172A" stroke-width="1.8"/><path d="M42 16h15l7 9v9H42V16z" fill="#16A34A" stroke="#0F172A" stroke-width="1.8"/><path d="M46 18h9l5 7h-14V18z" fill="#DCFCE7"/><circle cx="16" cy="34" r="5.5" fill="#1E293B" stroke="#0F172A" stroke-width="1.5"/><circle cx="16" cy="34" r="2.2" fill="#CBD5E1"/><circle cx="54" cy="34" r="5.5" fill="#1E293B" stroke="#0F172A" stroke-width="1.5"/><circle cx="54" cy="34" r="2.2" fill="#CBD5E1"/><line x1="6" y1="20" x2="40" y2="20" stroke="#94A3B8" stroke-width="1.5"/><circle cx="62" cy="29" r="1.5" fill="#FEF08A"/></svg>
              </div>
              <div>
                <div style="font-size:13px;font-weight:900;color:#0F172A;">Ashok Leyland Dost+ (3.0 Ton)</div>
                <div style="font-size:10.5px;color:#64748B;font-weight:600;">Up to 60 Qtl · 120 Sacks · Fast Haul</div>
              </div>
            </div>
            <div style="text-align:right;">
              <div id="gh-fare-tier-3" style="font-size:15px;font-weight:900;color:#0F172A;">₹680</div>
              <div style="font-size:9.5px;color:#16A34A;font-weight:800;">Available</div>
            </div>
          </div>

          <!-- Truck 4: Tata 407 Gold -->
          <div onclick="selectGramhaulTruckTier(4)" id="gh-tier-4" class="gh-vehicle-card ${selectedGramhaulTier===4?'selected':''}">
            <div style="display:flex;align-items:center;gap:12px;">
              <div style="width:52px;height:42px;border-radius:12px;background:#FFFBEB;padding:4px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                <svg viewBox="0 0 70 44" style="width:100%;height:100%;"><rect x="4" y="10" width="40" height="24" rx="2" fill="#FEF3C7" stroke="#0F172A" stroke-width="1.8"/><path d="M44 14h14l8 8v12H44V14z" fill="#D97706" stroke="#0F172A" stroke-width="1.8"/><path d="M48 16h8l6 6h-14V16z" fill="#FEF3C7"/><circle cx="16" cy="34" r="6" fill="#1E293B" stroke="#0F172A" stroke-width="1.5"/><circle cx="16" cy="34" r="2.5" fill="#D97706"/><circle cx="54" cy="34" r="6" fill="#1E293B" stroke="#0F172A" stroke-width="1.5"/><circle cx="54" cy="34" r="2.5" fill="#D97706"/><line x1="6" y1="18" x2="42" y2="18" stroke="#B45309" stroke-width="1.5"/><circle cx="64" cy="28" r="1.8" fill="#FFFFFF"/></svg>
              </div>
              <div>
                <div style="font-size:13px;font-weight:900;color:#0F172A;">Tata 407 Gold SFC (4.5 Ton)</div>
                <div style="font-size:10.5px;color:#64748B;font-weight:600;">Up to 85 Qtl · 170 Sacks · Mandi Legend</div>
              </div>
            </div>
            <div style="text-align:right;">
              <div id="gh-fare-tier-4" style="font-size:15px;font-weight:900;color:#0F172A;">₹820</div>
              <div style="font-size:9.5px;color:#D97706;font-weight:800;">Heavy Duty</div>
            </div>
          </div>

          <!-- Truck 5: Eicher Pro 14ft -->
          <div onclick="selectGramhaulTruckTier(5)" id="gh-tier-5" class="gh-vehicle-card ${selectedGramhaulTier===5?'selected':''}">
            <div style="display:flex;align-items:center;gap:12px;">
              <div style="width:52px;height:42px;border-radius:12px;background:#FAF5FF;padding:4px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                <svg viewBox="0 0 70 44" style="width:100%;height:100%;"><rect x="4" y="8" width="42" height="26" rx="2" fill="#F1F5F9" stroke="#0F172A" stroke-width="1.8"/><path d="M46 12h14l6 10v12H46V12z" fill="#2563EB" stroke="#0F172A" stroke-width="1.8"/><path d="M50 14h9l4 8h-13V14z" fill="#DBEAFE"/><circle cx="14" cy="34" r="6" fill="#1E293B" stroke="#0F172A" stroke-width="1.5"/><circle cx="14" cy="34" r="2.5" fill="#94A3B8"/><circle cx="26" cy="34" r="6" fill="#1E293B" stroke="#0F172A" stroke-width="1.5"/><circle cx="26" cy="34" r="2.5" fill="#94A3B8"/><circle cx="56" cy="34" r="6" fill="#1E293B" stroke="#0F172A" stroke-width="1.5"/><circle cx="56" cy="34" r="2.5" fill="#94A3B8"/><line x1="6" y1="16" x2="44" y2="16" stroke="#94A3B8" stroke-width="1.5"/><circle cx="64" cy="27" r="1.8" fill="#FDE047"/></svg>
              </div>
              <div>
                <div style="font-size:13px;font-weight:900;color:#0F172A;">Eicher Pro 14ft (5.5 Ton)</div>
                <div style="font-size:10.5px;color:#64748B;font-weight:600;">Up to 120 Qtl · 240 Sacks · Bulk Freight</div>
              </div>
            </div>
            <div style="text-align:right;">
              <div id="gh-fare-tier-5" style="font-size:15px;font-weight:900;color:#0F172A;">₹1,150</div>
              <div style="font-size:9.5px;color:#7C3AED;font-weight:800;">Bulk Pool</div>
            </div>
          </div>
        </div>

        <!-- FARE BREAKDOWN & BOOK BUTTON -->
        <div style="background:#F0FDF4;border:1px solid #86EFAC;border-radius:14px;padding:12px 14px;margin-bottom:14px;display:flex;justify-content:space-between;align-items:center;">
          <div>
            <div style="font-size:10.5px;color:#16A34A;font-weight:800;text-transform:uppercase;">${TL('Transparent Mandi Freight', 'పారదర్శక మండి రవాణా ఛార్జీ', 'पारदर्शी मंडी भाड़ा')}</div>
            <div style="font-size:11px;color:#64748B;">${TL('0% Commission · Pay Driver directly', '0% కమీషన్ · డ్రైవర్‌కే నేరుగా చెల్లించండి', '0% कमीशन · ड्राइवर को सीधे भुगतान')}</div>
          </div>
          <div id="gh-total-fare" style="font-size:20px;font-weight:900;color:#15803D;">₹380</div>
        </div>

        <button id="gh-confirm-booking-btn" onclick="executeRealGramhaulDispatch()" style="width:100%;height:52px;background:linear-gradient(135deg,#16A34A,#15803D);color:#FFFFFF;border:none;border-radius:16px;font-size:16px;font-weight:900;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;box-shadow:0 8px 24px rgba(22,163,74,0.35);">
          <span>${TL('Request Mandi Truck Now', 'మండి ట్రక్కును బుక్ చేయండి', 'मंडी ट्रक बुक करें')}</span>
          <span>→</span>
        </button>
      </div>
    </div>
    `;
  },

  /* ── RAPIDO FULLSCREEN LIVE TRACKING VIEW ── */
  gramhaul_tracking: () => {
    setTimeout(initGramhaulTrackingMap, 80);
    return `
    <div style="position:relative;width:100%;height:100%;display:flex;flex-direction:column;background:#0F172A;overflow:hidden;font-family:'Plus Jakarta Sans',-apple-system,BlinkMacSystemFont,sans-serif;">
      
      <!-- FULLSCREEN 100% UNOBSTRUCTED LEAFLET OSM MAP -->
      <div id="gramhaul-tracking-osm-map" style="position:absolute;inset:0;width:100%;height:100%;z-index:1;"></div>

      <!-- FLOATING TOP BAR -->
      <div style="position:absolute;top:max(14px, calc(var(--sat) - 20px));left:12px;right:12px;display:flex;justify-content:space-between;align-items:center;z-index:20;pointer-events:auto;">
        <button onclick="openScreen('gramhaul', null)" style="width:42px;height:42px;border-radius:14px;background:rgba(15,23,42,0.88);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,0.15);color:#FFFFFF;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 16px rgba(0,0,0,0.3);cursor:pointer;font-size:18px;">
          ←
        </button>
        <div id="gh-tracking-top-status-pill" style="background:rgba(15,23,42,0.88);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,0.15);border-radius:999px;padding:7px 14px;display:flex;align-items:center;gap:8px;box-shadow:0 4px 16px rgba(0,0,0,0.3);">
          <span style="width:8px;height:8px;border-radius:50%;background:#22C55E;box-shadow:0 0 8px #22C55E;animation:pulse 1.2s infinite;"></span>
          <span id="gh-tracking-top-status-text" style="font-size:12px;font-weight:900;color:#FFFFFF;letter-spacing:-0.2px;">Radar Geofenced · 10 KM Radius</span>
        </div>
        <button onclick="recenterTrackingMap()" style="width:42px;height:42px;border-radius:14px;background:rgba(15,23,42,0.88);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,0.15);color:#FFFFFF;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 16px rgba(0,0,0,0.3);cursor:pointer;font-size:18px;">
          🎯
        </button>
      </div>

      <!-- FLOATING BOTTOM CONTAINER FOR SEARCHING RADAR OR COCKPIT SHEET -->
      <div id="gh-tracking-bottom-container" style="position:absolute;bottom:0;left:0;right:0;z-index:20;pointer-events:auto;display:flex;flex-direction:column;align-items:center;">
      </div>
    </div>
    `;
  },
"""

    START_MARKER = "/* ── 4. MANDI TRUCK SHARING ── */"
    END_MARKER   = "  agristack: () => {"
    i1 = text.find(START_MARKER)
    i2 = text.find(END_MARKER)
    assert i1 > 0, "START_MARKER not found"
    assert i2 > i1, "END_MARKER not found after START_MARKER"

    text = text[:i1] + V2_GRAMHAUL_CODE + "\n  " + text[i2:]
    print("  [+] Spliced APP_VIEWS.gramhaul and gramhaul_tracking matching v2_02_gramhaul_selector_tier1")

    # 4. Update selectGramhaulTruckTier to update both .selected class on #gh-tier-1..5 and map vehicle
    select_fn = """function selectGramhaulTruckTier(tier) {
  selectedGramhaulTier = tier;
  for (let t = 1; t <= 5; t++) {
    const el = document.getElementById('gh-tier-' + t);
    if (el) {
      if (t === tier) {
        el.classList.add('selected');
        el.style.borderColor = '#22C55E';
        el.style.background = '#F0FDF4';
      } else {
        el.classList.remove('selected');
        el.style.borderColor = '#E2E8F0';
        el.style.background = '#FFFFFF';
      }
    }
  }
  recalcGramhaulFare();
  updateGramhaulSelectorMapVehicles(tier);
}"""

    # Look for existing selectGramhaulTruckTier function
    s_idx = text.find("function selectGramhaulTruckTier")
    if s_idx != -1:
        e_idx = text.find("function updateGramhaulMandi", s_idx)
        if e_idx != -1:
            text = text[:s_idx] + select_fn + "\n\n" + text[e_idx:]
            print("  [+] Updated selectGramhaulTruckTier")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"DONE updating {file_path}.\n")

apply_to_file("app/src/main/assets/index.html")
apply_to_file("nukrop_emulator.html")
