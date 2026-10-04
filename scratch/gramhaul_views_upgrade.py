# Script to upgrade GramHaul with high-end icons and layout polish across index.html and nukrop_emulator.html

import re

# Vehicle SVGs
ACE_GOLD_SVG = '''<svg viewBox="0 0 84 52" fill="none" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;">
  <defs>
    <linearGradient id="aceCabin" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="70%" stop-color="#F8FAFC"/>
      <stop offset="100%" stop-color="#CBD5E1"/>
    </linearGradient>
    <linearGradient id="aceBed" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#16A34A"/>
      <stop offset="100%" stop-color="#14532D"/>
    </linearGradient>
    <linearGradient id="aceGlass" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#BAE6FD"/>
      <stop offset="60%" stop-color="#38BDF8"/>
      <stop offset="100%" stop-color="#0284C7"/>
    </linearGradient>
  </defs>
  <!-- Sacks in Cargo Bed -->
  <g fill="#D97706" stroke="#92400E" stroke-width="0.8">
    <ellipse cx="14" cy="18" rx="8" ry="4.5"/>
    <ellipse cx="26" cy="17" rx="8" ry="4.5"/>
    <ellipse cx="38" cy="18" rx="8" ry="4.5"/>
    <ellipse cx="20" cy="13" rx="7" ry="4" fill="#F59E0B"/>
    <ellipse cx="32" cy="13" rx="7" ry="4" fill="#F59E0B"/>
  </g>
  <!-- Cargo Bed -->
  <rect x="4" y="20" width="46" height="18" rx="2" fill="url(#aceBed)" stroke="#0F172A" stroke-width="1.8"/>
  <line x1="4" y1="28" x2="50" y2="28" stroke="#15803D" stroke-width="1.2"/>
  <line x1="20" y1="20" x2="20" y2="38" stroke="#15803D" stroke-width="1.2"/>
  <line x1="35" y1="20" x2="35" y2="38" stroke="#15803D" stroke-width="1.2"/>
  <!-- Cabin Body -->
  <path d="M50 20 H68 C74 20 78 24 79 30 L80 38 H50 V20 Z" fill="url(#aceCabin)" stroke="#0F172A" stroke-width="1.8"/>
  <!-- Blue Commercial Decal Stripe -->
  <path d="M50 32 H78 L79 35 H50 V32 Z" fill="#0284C7"/>
  <!-- Windshield -->
  <path d="M54 22 H67 C71 22 74 25 75 29 H54 V22 Z" fill="url(#aceGlass)" stroke="#0F172A" stroke-width="1.2"/>
  <line x1="58" y1="23" x2="63" y2="28" stroke="#FFFFFF" stroke-width="1.5" stroke-linecap="round" opacity="0.85"/>
  <!-- Headlight & Grille -->
  <circle cx="76" cy="34" r="2.5" fill="#FEF08A" stroke="#CA8A04" stroke-width="0.8"/>
  <rect x="73" y="32" width="2" height="4" rx="0.5" fill="#F59E0B"/>
  <rect x="62" y="23" width="2" height="4" rx="1" fill="#0F172A"/>
  <rect x="74" y="37" width="7" height="3" rx="1.5" fill="#1E293B"/>
  <!-- Wheels -->
  <circle cx="18" cy="38" r="7" fill="#0F172A"/>
  <circle cx="18" cy="38" r="4.2" fill="#94A3B8"/>
  <circle cx="18" cy="38" r="1.8" fill="#0F172A"/>
  <circle cx="66" cy="38" r="7" fill="#0F172A"/>
  <circle cx="66" cy="38" r="4.2" fill="#94A3B8"/>
  <circle cx="66" cy="38" r="1.8" fill="#0F172A"/>
</svg>'''

BOLERO_MAXI_SVG = '''<svg viewBox="0 0 84 52" fill="none" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;">
  <defs>
    <linearGradient id="bolRed" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#EF4444"/>
      <stop offset="60%" stop-color="#DC2626"/>
      <stop offset="100%" stop-color="#991B1B"/>
    </linearGradient>
    <linearGradient id="bolBed" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="100%" stop-color="#E2E8F0"/>
    </linearGradient>
  </defs>
  <!-- Produce Cargo & Crates -->
  <g fill="#EA580C" stroke="#9A3412" stroke-width="0.8">
    <rect x="10" y="12" width="12" height="8" rx="1.5"/>
    <rect x="24" y="12" width="12" height="8" rx="1.5" fill="#F59E0B"/>
    <rect x="17" y="6" width="12" height="8" rx="1.5" fill="#16A34A" stroke="#14532D"/>
  </g>
  <!-- Tubular Ladder Frame / Roll-Cage -->
  <path d="M6 19 H48 V10 H42" stroke="#64748B" stroke-width="1.8" stroke-linecap="round" fill="none"/>
  <!-- Cargo Bed -->
  <rect x="4" y="18" width="46" height="20" rx="2" fill="url(#bolBed)" stroke="#0F172A" stroke-width="1.8"/>
  <line x1="4" y1="27" x2="50" y2="27" stroke="#CBD5E1" stroke-width="1.5"/>
  <!-- Bolero Cabin -->
  <path d="M50 18 H66 L78 28 V38 H50 V18 Z" fill="url(#bolRed)" stroke="#0F172A" stroke-width="1.8"/>
  <rect x="70" y="28" width="10" height="10" fill="url(#bolRed)" stroke="#0F172A" stroke-width="1.2"/>
  <path d="M54 20 H64 L72 28 H54 V20 Z" fill="#BAE6FD" stroke="#0F172A" stroke-width="1.2"/>
  <rect x="76" y="30" width="3" height="6" fill="#1E293B"/>
  <circle cx="78" cy="29" r="2.2" fill="#FEF08A"/>
  <rect x="75" y="37" width="6" height="3" rx="1" fill="#0F172A"/>
  <circle cx="18" cy="38" r="7.5" fill="#0F172A"/>
  <circle cx="18" cy="38" r="4.5" fill="#E2E8F0"/>
  <circle cx="18" cy="38" r="2" fill="#DC2626"/>
  <circle cx="66" cy="38" r="7.5" fill="#0F172A"/>
  <circle cx="66" cy="38" r="4.5" fill="#E2E8F0"/>
  <circle cx="66" cy="38" r="2" fill="#DC2626"/>
</svg>'''

DOST_PLUS_SVG = '''<svg viewBox="0 0 84 52" fill="none" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;">
  <defs>
    <linearGradient id="dostGreen" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#22C55E"/>
      <stop offset="60%" stop-color="#16A34A"/>
      <stop offset="100%" stop-color="#15803D"/>
    </linearGradient>
  </defs>
  <!-- Full Produce Cover Tarpaulin -->
  <path d="M8 12 Q28 6 48 12 L48 18 H8 Z" fill="#2563EB" stroke="#1E40AF" stroke-width="1.2"/>
  <path d="M12 18 L24 10 M26 18 L38 10" stroke="#93C5FD" stroke-width="1" opacity="0.6"/>
  <!-- Cargo Bed -->
  <rect x="4" y="17" width="46" height="21" rx="2" fill="#F8FAFC" stroke="#0F172A" stroke-width="1.8"/>
  <line x1="4" y1="26" x2="50" y2="26" stroke="#E2E8F0" stroke-width="1.5"/>
  <!-- Dost Aerodynamic Cabin -->
  <path d="M50 17 H66 C72 17 76 20 78 26 L80 38 H50 V17 Z" fill="url(#dostGreen)" stroke="#0F172A" stroke-width="1.8"/>
  <path d="M54 19 H65 C68 19 72 22 74 26 H54 V19 Z" fill="#E0F2FE" stroke="#0F172A" stroke-width="1.2"/>
  <ellipse cx="77" cy="32" rx="2.5" ry="3" fill="#FEF08A" stroke="#CA8A04" stroke-width="0.8"/>
  <rect x="75" y="37" width="6" height="3" rx="1" fill="#1E293B"/>
  <circle cx="18" cy="38" r="7.2" fill="#0F172A"/>
  <circle cx="18" cy="38" r="4.2" fill="#CBD5E1"/>
  <circle cx="18" cy="38" r="1.8" fill="#16A34A"/>
  <circle cx="66" cy="38" r="7.2" fill="#0F172A"/>
  <circle cx="66" cy="38" r="4.2" fill="#CBD5E1"/>
  <circle cx="66" cy="38" r="1.8" fill="#16A34A"/>
</svg>'''

TATA_407_SVG = '''<svg viewBox="0 0 84 52" fill="none" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;">
  <defs>
    <linearGradient id="t407Cab" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FBBF24"/>
      <stop offset="60%" stop-color="#F59E0B"/>
      <stop offset="100%" stop-color="#D97706"/>
    </linearGradient>
    <linearGradient id="t407Bed" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FEF3C7"/>
      <stop offset="100%" stop-color="#FDE68A"/>
    </linearGradient>
  </defs>
  <!-- Towering High-Load Sacks -->
  <g fill="#CA8A04" stroke="#854D0E" stroke-width="0.8">
    <ellipse cx="14" cy="11" rx="8" ry="4.5"/>
    <ellipse cx="28" cy="10" rx="9" ry="4.5"/>
    <ellipse cx="42" cy="11" rx="8" ry="4.5"/>
    <ellipse cx="22" cy="6" rx="8" ry="4" fill="#EAB308"/>
    <ellipse cx="36" cy="6" rx="8" ry="4" fill="#EAB308"/>
  </g>
  <!-- Traditional Timber-Reinforced Cargo Bed -->
  <rect x="4" y="14" width="48" height="24" rx="2" fill="url(#t407Bed)" stroke="#0F172A" stroke-width="1.8"/>
  <line x1="4" y1="22" x2="52" y2="22" stroke="#B45309" stroke-width="1.5"/>
  <line x1="4" y1="30" x2="52" y2="30" stroke="#B45309" stroke-width="1.5"/>
  <!-- Forward-Control 407 Cabin -->
  <path d="M52 14 H68 C74 14 78 18 79 24 L80 38 H52 V14 Z" fill="url(#t407Cab)" stroke="#0F172A" stroke-width="1.8"/>
  <path d="M56 16 H67 C71 16 74 19 75 24 H56 V16 Z" fill="#BAE6FD" stroke="#0F172A" stroke-width="1.2"/>
  <circle cx="76" cy="32" r="3" fill="#FFFFFF" stroke="#0F172A" stroke-width="1"/>
  <circle cx="76" cy="32" r="1.5" fill="#FEF08A"/>
  <rect x="74" y="37" width="8" height="4" rx="1.5" fill="#1E293B"/>
  <circle cx="18" cy="38" r="7.8" fill="#0F172A"/>
  <circle cx="18" cy="38" r="4.6" fill="#D97706"/>
  <circle cx="18" cy="38" r="1.8" fill="#0F172A"/>
  <circle cx="66" cy="38" r="7.8" fill="#0F172A"/>
  <circle cx="66" cy="38" r="4.6" fill="#D97706"/>
  <circle cx="66" cy="38" r="1.8" fill="#0F172A"/>
</svg>'''

EICHER_PRO_SVG = '''<svg viewBox="0 0 84 52" fill="none" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;">
  <defs>
    <linearGradient id="eichBlue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#3B82F6"/>
      <stop offset="50%" stop-color="#2563EB"/>
      <stop offset="100%" stop-color="#1D4ED8"/>
    </linearGradient>
    <linearGradient id="eichBox" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F1F5F9"/>
      <stop offset="100%" stop-color="#CBD5E1"/>
    </linearGradient>
  </defs>
  <!-- 14ft Freight Cargo Box -->
  <rect x="3" y="9" width="50" height="29" rx="2" fill="url(#eichBox)" stroke="#0F172A" stroke-width="1.8"/>
  <rect x="3" y="22" width="50" height="3" fill="#FACC15"/>
  <!-- Roof Wind Deflector & Blue Tilt-Cab -->
  <path d="M53 9 H68 L78 20 V38 H53 V9 Z" fill="url(#eichBlue)" stroke="#0F172A" stroke-width="1.8"/>
  <path d="M56 12 H67 L74 21 H56 V12 Z" fill="#DBEAFE" stroke="#0F172A" stroke-width="1.2"/>
  <rect x="56" y="9" width="13" height="3" fill="#0F172A"/>
  <rect x="74" y="27" width="3.5" height="6" rx="1" fill="#FEF08A" stroke="#CA8A04" stroke-width="0.8"/>
  <rect x="72" y="36" width="9" height="4" rx="1.5" fill="#0F172A"/>
  <!-- 3 Heavy Axle Wheels (Dual Rear Axle) -->
  <circle cx="14" cy="38" r="7.5" fill="#0F172A"/>
  <circle cx="14" cy="38" r="4.2" fill="#94A3B8"/>
  <circle cx="28" cy="38" r="7.5" fill="#0F172A"/>
  <circle cx="28" cy="38" r="4.2" fill="#94A3B8"/>
  <circle cx="68" cy="38" r="7.5" fill="#0F172A"/>
  <circle cx="68" cy="38" r="4.2" fill="#94A3B8"/>
</svg>'''

def build_gramhaul_view():
    return f"""  /* ── 2. GRAMHAUL LOGISTICS: 38% VISIBLE MAP + PRO TRUCK CATEGORIES (MATCHING v2_02_gramhaul_selector_tier1) ── */
  gramhaul: () => {{
    const t = I18N[currentLang] || I18N.en;
    setTimeout(initGramhaulRealMap, 80);

    const farmAddr = currentGramhaulFarmAddress || "Himayath Nagar Farm, Telangana";
    const mandi = currentGramhaulMandi || (typeof REAL_APMC_MANDIS !== 'undefined' ? REAL_APMC_MANDIS[0] : {{name:'Gudimalkapur Vegetable & Flower APMC Yard', shortName:'Gudimalkapur APMC', distKm:7.2, tag:'7.2 km · Nearest', id:'gudimalkapur'}});
    const mandiList = typeof REAL_APMC_MANDIS !== 'undefined' ? REAL_APMC_MANDIS : [
      {{ id: 'gudimalkapur', name: 'Gudimalkapur APMC', shortName: 'Gudimalkapur APMC', distKm: 7.2, tag: '7.2 km · Nearest' }},
      {{ id: 'bowenpally', name: 'Bowenpally Wholesale APMC', shortName: 'Bowenpally APMC', distKm: 9.8, tag: '9.8 km' }},
      {{ id: 'moinabad', name: 'Moinabad Regional APMC', shortName: 'Moinabad APMC', distKm: 24.5, tag: '24.5 km' }}
    ];

    const currentCropSlug = typeof selectedGramhaulCropSlug !== 'undefined' ? selectedGramhaulCropSlug : 'cotton';

    return `
    <style>
    .gh-vehicle-card {{ transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1); border: 1.5px solid #E2E8F0; background: #FFFFFF; border-radius: 18px; padding: 12px 14px; cursor: pointer; display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; box-shadow: 0 1px 3px rgba(15,23,42,0.04); }}
    .gh-vehicle-card:active {{ transform: scale(0.98); }}
    .gh-vehicle-card.selected {{ border-color: #22C55E !important; background: #F0FDF4 !important; box-shadow: 0 4px 18px rgba(34,197,94,0.18) !important; }}
    </style>

    <div style="position:relative;width:100%;height:100%;display:flex;flex-direction:column;background:#F8FAF8;overflow:hidden;font-family:'Plus Jakarta Sans',-apple-system,BlinkMacSystemFont,sans-serif;">
      
      <!-- TOP 38%: DEDICATED UNOBSTRUCTED LEAFLET OSM MAP -->
      <div style="position:relative;width:100%;height:38vh;min-height:230px;background:#E5EFE5;flex-shrink:0;overflow:hidden;">
        
        <!-- Interactive Leaflet Map -->
        <div id="gramhaul-real-osm-map" style="position:absolute;inset:0;width:100%;height:100%;z-index:1;"></div>
        
        <!-- Top Bar with Safe Area -->
        <div style="position:absolute;top:max(14px, calc(var(--sat) - 20px));left:12px;right:12px;display:flex;justify-content:space-between;align-items:center;z-index:20;">
          <button onclick="openScreen(authUserRole==='driver'?'driver_dashboard':'home',null);updateBottomDockForRole()" style="background:#FFFFFF;border:1px solid #E2E8F0;width:40px;height:40px;border-radius:13px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 14px rgba(0,0,0,0.10);cursor:pointer;flex-shrink:0;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#0F172A" stroke-width="2.5" stroke-linecap="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
          </button>
          
          <div style="background:linear-gradient(135deg,#FFFFFF 0%,#F0FDF4 100%);border:1px solid #BBF7D0;padding:7px 16px;border-radius:999px;box-shadow:0 4px 14px rgba(0,0,0,0.08);display:flex;align-items:center;gap:8px;">
            <div style="width:20px;height:20px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <rect x="2" y="7" width="13" height="10" rx="1.5" fill="#16A34A"/>
                <path d="M15 10H18.5L21.5 13.5V17H15V10Z" fill="#15803D"/>
                <circle cx="6" cy="17" r="2.2" fill="#0F172A"/>
                <circle cx="17.5" cy="17" r="2.2" fill="#0F172A"/>
                <path d="M15.5 11H18L20 13.5H15.5V11Z" fill="#BAE6FD"/>
              </svg>
            </div>
            <span style="font-size:13.5px;font-weight:900;color:#15803D;letter-spacing:-0.2px;">${{TL('GramHaul Mandi Dispatch', 'గ్రామ్‌హౌల్ మండి రవాణా', 'ग्रामहॉल मंडी परिवहन')}}</span>
          </div>

          <div style="display:flex;align-items:center;gap:6px;">
            <button onclick="openPreviousRidesModal()" title="Ride History" style="background:#FFFFFF;border:1px solid #E2E8F0;width:40px;height:40px;border-radius:13px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 14px rgba(0,0,0,0.08);cursor:pointer;flex-shrink:0;">
              <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="#334155" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><line x1="10" y1="9" x2="8" y2="9"/></svg>
            </button>
            <button onclick="openGramhaulPickupLocationModal()" title="Edit Pickup" style="background:linear-gradient(135deg,#16A34A,#15803D);border:none;width:40px;height:40px;border-radius:13px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 14px rgba(22,163,74,0.35);cursor:pointer;flex-shrink:0;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"><circle cx="12" cy="10" r="3"/><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/></svg>
            </button>
          </div>
        </div>

        <!-- Live GPS Dispatch Pill -->
        <div style="position:absolute;bottom:10px;left:12px;z-index:20;background:rgba(15,23,42,0.88);backdrop-filter:blur(8px);color:#FFFFFF;padding:6px 14px;border-radius:999px;font-size:11px;font-weight:800;display:flex;align-items:center;gap:7px;box-shadow:0 2px 10px rgba(0,0,0,0.25);border:1px solid rgba(255,255,255,0.12);">
          <span style="width:7px;height:7px;border-radius:50%;background:#4ADE80;box-shadow:0 0 8px #4ADE80;display:inline-block;animation:radarPulse 1.4s infinite;"></span>
          ${{TL('10 KM Proximity Geofenced', '10 కి.మీ పరిధిలో వాహనాలు', '10 किमी दायरे में वाहन')}}
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
                  <div style="font-size:9.5px;color:#64748B;font-weight:800;letter-spacing:0.04em;text-transform:uppercase;">${{TL('FROM (PICKUP FARM)', 'నుండి (పొలం చిరునామా)', 'से (खेत का पता)')}}</div>
                  <div id="gh-pickup-location-label" style="font-size:13px;font-weight:900;color:#0F172A;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-top:1px;">${{farmAddr}}</div>
                </div>
                <button onclick="openGramhaulPickupLocationModal()" style="background:#F0FDF4;color:#15803D;border:1px solid #BBF7D0;border-radius:10px;padding:5px 12px;font-size:11px;font-weight:900;cursor:pointer;flex-shrink:0;transition:all 0.15s ease;display:flex;align-items:center;gap:4px;">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#15803D" stroke-width="2.5" stroke-linecap="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                  <span>${{TL('Edit', 'మార్చు', 'बदलें')}}</span>
                </button>
              </div>

              <!-- Content Separator -->
              <div style="height:1px;background:#F1F5F9;"></div>

              <!-- Destination Drop Mandi Row -->
              <div style="flex:1;min-width:0;">
                <div style="font-size:9.5px;color:#64748B;font-weight:800;letter-spacing:0.04em;text-transform:uppercase;">${{TL('TO (DESTINATION APMC MANDI)', 'చేరుకోవాల్సిన మండి (APMC)', 'मंडी गंतव्य (APMC)')}}</div>
                <div style="display:flex;align-items:center;gap:6px;margin-top:1px;">
                  <select id="gh-mandi-select" onchange="updateGramhaulMandi(this.value)" style="width:100%;border:none;background:transparent;font-size:13.5px;font-weight:900;color:#0F172A;outline:none;cursor:pointer;padding:0;letter-spacing:-0.2px;">
                    ${{mandiList.map((m,i) => `<option value="${{i}}">${{m.shortName}} · ${{m.distKm}} km</option>`).join('')}}
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- COMMODITY SPECS: 140+ CROPS MODAL PICKER + SACKS -->
        <div style="display:grid;grid-template-columns:1.2fr 1fr;gap:10px;margin-bottom:12px;">
          <div>
            <div style="display:flex;align-items:center;gap:5px;font-size:10px;font-weight:800;color:#475569;text-transform:uppercase;margin-bottom:5px;">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M12 22V12M12 12C12 7 7 4 2 5C2 10 5 14 12 12ZM12 12C12 7 17 4 22 5C22 10 19 14 12 12Z" stroke="#16A34A" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>
              <span>${{TL('Crop Commodity', 'పంట రకం', 'फसल का प्रकार')}}</span>
            </div>
            <div onclick="openGramhaulCropSelectorModal()" style="width:100%;height:46px;background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:13px;padding:0 10px;display:flex;align-items:center;justify-content:space-between;cursor:pointer;box-sizing:border-box;box-shadow:0 1px 3px rgba(0,0,0,0.02);">
              <div style="display:flex;align-items:center;gap:8px;min-width:0;">
                <div id="gh-selected-crop-icon" style="width:26px;height:26px;flex-shrink:0;">${{getCropIconImg(null, currentCropSlug)}}</div>
                <span id="gh-selected-crop-label" style="font-size:13px;font-weight:900;color:#0F172A;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${{getLocalizedCropName(currentCropSlug)}}</span>
              </div>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2.5" stroke-linecap="round"><polyline points="6 9 12 15 18 9"/></svg>
            </div>
            <input type="hidden" id="gh-crop-select" value="${{currentCropSlug}}" />
          </div>
          <div>
            <div style="display:flex;align-items:center;gap:5px;font-size:10px;font-weight:800;color:#475569;text-transform:uppercase;margin-bottom:5px;">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M6 8V6C6 4.34315 7.34315 3 9 3H15C16.6569 3 18 4.34315 18 6V8M3 8H21L19.5 20C19.5 21.1046 18.6046 22 17.5 22H6.5C5.39543 22 4.5 21.1046 4.5 20L3 8Z" stroke="#D97706" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
              <span>${{TL('Bags / Sacks', 'బస్తాల సంఖ్య', 'बोरी / कट्टे')}}</span>
            </div>
            <input id="gh-weight-inp" type="number" value="40" min="1" max="500" oninput="recalcGramhaulFare()" style="width:100%;height:46px;background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:13px;padding:0 12px;font-size:13.5px;font-weight:800;color:#0F172A;outline:none;box-sizing:border-box;box-shadow:0 1px 3px rgba(0,0,0,0.02);" placeholder="e.g. 40" />
          </div>
        </div>

        <!-- REAL COMMERCIAL TRUCK FLEET (5 REALISTIC VEHICLE TIERS) -->
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
          <div style="display:flex;align-items:center;gap:6px;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><rect x="1" y="6" width="14" height="11" rx="2" fill="#16A34A"/><path d="M15 9H19L22 13V17H15V9Z" fill="#15803D"/><circle cx="5.5" cy="17" r="2.2" fill="#0F172A"/><circle cx="18.5" cy="17" r="2.2" fill="#0F172A"/></svg>
            <span style="font-size:11px;font-weight:900;color:#334155;text-transform:uppercase;letter-spacing:0.4px;">${{TL('Choose Commercial Truck', 'వాహనాన్ని ఎంచుకోండి', 'वाणिज्यिक ट्रक चुनें')}}</span>
          </div>
          <span style="font-size:10.5px;color:#16A34A;font-weight:800;">${{TL('5 Verified Tiers', '5 ధృవీకరించిన రకాలు', '5 सत्यापित श्रेणियां')}}</span>
        </div>
        
        <div style="display:flex;flex-direction:column;gap:6px;margin-bottom:14px;" id="gh-truck-categories">
          
          <!-- Truck 1: Tata Ace Gold -->
          <div onclick="selectGramhaulTruckTier(1)" id="gh-tier-1" class="gh-vehicle-card ${{selectedGramhaulTier===1?'selected':''}}">
            <div style="display:flex;align-items:center;gap:12px;">
              <div style="width:58px;height:44px;border-radius:13px;background:linear-gradient(135deg,#DCFCE7 0%,#F0FDF4 100%);border:1px solid #BBF7D0;padding:2px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                {ACE_GOLD_SVG}
              </div>
              <div>
                <div style="font-size:13.5px;font-weight:900;color:#0F172A;letter-spacing:-0.2px;">Tata Ace Gold (1.5 Ton)</div>
                <div style="font-size:11px;color:#64748B;font-weight:600;margin-top:1px;">Up to 25 Qtl · 50 Sacks · Chota Hathi</div>
              </div>
            </div>
            <div style="text-align:right;">
              <div id="gh-fare-tier-1" style="font-size:16px;font-weight:900;color:#0F172A;">₹380</div>
              <div style="font-size:9.5px;color:#16A34A;font-weight:800;margin-top:1px;">✓ Ready</div>
            </div>
          </div>

          <!-- Truck 2: Bolero Maxi Truck -->
          <div onclick="selectGramhaulTruckTier(2)" id="gh-tier-2" class="gh-vehicle-card ${{selectedGramhaulTier===2?'selected':''}}">
            <div style="display:flex;align-items:center;gap:12px;">
              <div style="width:58px;height:44px;border-radius:13px;background:linear-gradient(135deg,#EFF6FF 0%,#DBEAFE 100%);border:1px solid #BFDBFE;padding:2px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                {BOLERO_MAXI_SVG}
              </div>
              <div>
                <div style="font-size:13.5px;font-weight:900;color:#0F172A;letter-spacing:-0.2px;">Mahindra Bolero Maxi (2.5 Ton)</div>
                <div style="font-size:11px;color:#64748B;font-weight:600;margin-top:1px;">Up to 50 Qtl · 100 Sacks · Heavy Produce</div>
              </div>
            </div>
            <div style="text-align:right;">
              <div id="gh-fare-tier-2" style="font-size:16px;font-weight:900;color:#0F172A;">₹560</div>
              <div style="font-size:9.5px;color:#2563EB;font-weight:800;margin-top:1px;">Available</div>
            </div>
          </div>

          <!-- Truck 3: Ashok Leyland Dost+ -->
          <div onclick="selectGramhaulTruckTier(3)" id="gh-tier-3" class="gh-vehicle-card ${{selectedGramhaulTier===3?'selected':''}}">
            <div style="display:flex;align-items:center;gap:12px;">
              <div style="width:58px;height:44px;border-radius:13px;background:linear-gradient(135deg,#F0FDF4 0%,#DCFCE7 100%);border:1px solid #86EFAC;padding:2px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                {DOST_PLUS_SVG}
              </div>
              <div>
                <div style="font-size:13.5px;font-weight:900;color:#0F172A;letter-spacing:-0.2px;">Ashok Leyland Dost+ (3.0 Ton)</div>
                <div style="font-size:11px;color:#64748B;font-weight:600;margin-top:1px;">Up to 60 Qtl · 120 Sacks · Fast Haul</div>
              </div>
            </div>
            <div style="text-align:right;">
              <div id="gh-fare-tier-3" style="font-size:16px;font-weight:900;color:#0F172A;">₹680</div>
              <div style="font-size:9.5px;color:#16A34A;font-weight:800;margin-top:1px;">Available</div>
            </div>
          </div>

          <!-- Truck 4: Tata 407 Gold -->
          <div onclick="selectGramhaulTruckTier(4)" id="gh-tier-4" class="gh-vehicle-card ${{selectedGramhaulTier===4?'selected':''}}">
            <div style="display:flex;align-items:center;gap:12px;">
              <div style="width:58px;height:44px;border-radius:13px;background:linear-gradient(135deg,#FFFBEB 0%,#FEF3C7 100%);border:1px solid #FDE68A;padding:2px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                {TATA_407_SVG}
              </div>
              <div>
                <div style="font-size:13.5px;font-weight:900;color:#0F172A;letter-spacing:-0.2px;">Tata 407 Gold SFC (4.5 Ton)</div>
                <div style="font-size:11px;color:#64748B;font-weight:600;margin-top:1px;">Up to 85 Qtl · 170 Sacks · Mandi Legend</div>
              </div>
            </div>
            <div style="text-align:right;">
              <div id="gh-fare-tier-4" style="font-size:16px;font-weight:900;color:#0F172A;">₹820</div>
              <div style="font-size:9.5px;color:#D97706;font-weight:800;margin-top:1px;">Heavy Duty</div>
            </div>
          </div>

          <!-- Truck 5: Eicher Pro 14ft -->
          <div onclick="selectGramhaulTruckTier(5)" id="gh-tier-5" class="gh-vehicle-card ${{selectedGramhaulTier===5?'selected':''}}">
            <div style="display:flex;align-items:center;gap:12px;">
              <div style="width:58px;height:44px;border-radius:13px;background:linear-gradient(135deg,#FAF5FF 0%,#F3E8FF 100%);border:1px solid #E9D5FF;padding:2px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                {EICHER_PRO_SVG}
              </div>
              <div>
                <div style="font-size:13.5px;font-weight:900;color:#0F172A;letter-spacing:-0.2px;">Eicher Pro 14ft (5.5 Ton)</div>
                <div style="font-size:11px;color:#64748B;font-weight:600;margin-top:1px;">Up to 120 Qtl · 240 Sacks · Bulk Freight</div>
              </div>
            </div>
            <div style="text-align:right;">
              <div id="gh-fare-tier-5" style="font-size:16px;font-weight:900;color:#0F172A;">₹1,150</div>
              <div style="font-size:9.5px;color:#7C3AED;font-weight:800;margin-top:1px;">Bulk Pool</div>
            </div>
          </div>
        </div>

        <!-- FARE BREAKDOWN & BOOK BUTTON -->
        <div style="background:#F0FDF4;border:1px solid #86EFAC;border-radius:14px;padding:12px 14px;margin-bottom:14px;display:flex;justify-content:space-between;align-items:center;">
          <div style="display:flex;align-items:center;gap:10px;">
            <div style="width:36px;height:36px;border-radius:10px;background:#DCFCE7;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#15803D" stroke-width="2.2" stroke-linecap="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            </div>
            <div>
              <div style="font-size:10.5px;color:#16A34A;font-weight:800;text-transform:uppercase;">${{TL('Transparent Mandi Freight', 'పారదర్శక మండి రవాణా ఛార్జీ', 'पारदर्शी मंडी भाड़ा')}}</div>
              <div style="font-size:11px;color:#64748B;">${{TL('0% Commission · Pay Driver directly', '0% కమీషన్ · డ్రైవర్‌కే నేరుగా చెల్లించండి', '0% कमीशन · ड्राइवर को सीधे भुगतान')}}</div>
            </div>
          </div>
          <div id="gh-total-fare" style="font-size:20px;font-weight:900;color:#15803D;">₹380</div>
        </div>

        <button id="gh-confirm-booking-btn" onclick="executeRealGramhaulDispatch()" style="width:100%;height:52px;background:linear-gradient(135deg,#16A34A,#15803D);color:#FFFFFF;border:none;border-radius:16px;font-size:16px;font-weight:900;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;box-shadow:0 8px 24px rgba(22,163,74,0.35);">
          <span>${{TL('Request Mandi Truck Now', 'మండి ట్రక్కును బుక్ చేయండి', 'मंडी ट्रक बुक करें')}}</span>
          <span>→</span>
        </button>
      </div>
    </div>
    `;
  }},
"""

def build_gramhaul_tracking_view():
    return """  /* ── RAPIDO FULLSCREEN LIVE TRACKING VIEW ── */
  gramhaul_tracking: () => {
    setTimeout(initGramhaulTrackingMap, 80);
    return `
    <style>
    @keyframes radarPulse { 0%,100% { transform:scale(1); opacity:0.9; } 50% { transform:scale(1.35); opacity:0.3; } }
    @keyframes radarRipple { 0% { transform:scale(0.5); opacity:0.9; } 100% { transform:scale(1.6); opacity:0; } }
    @keyframes truckDrive { 0%,100% { transform:translateX(0) scaleX(-1); } 50% { transform:translateX(5px) scaleX(-1); } }
    @keyframes slideUp { from { transform:translateY(60px); opacity:0; } to { transform:translateY(0); opacity:1; } }
    </style>

    <div style="position:relative;width:100%;height:100%;display:flex;flex-direction:column;background:#0F172A;overflow:hidden;font-family:'Plus Jakarta Sans',-apple-system,BlinkMacSystemFont,sans-serif;">
      
      <!-- FULLSCREEN 100% UNOBSTRUCTED LEAFLET OSM MAP -->
      <div id="gramhaul-tracking-osm-map" style="position:absolute;inset:0;width:100%;height:100%;z-index:1;"></div>

      <!-- FLOATING TOP BAR: WHITE CIRCULAR BACK BUTTON + WHITE STATUS PILL + WHITE RECENTER BUTTON (RAPIDO-EXACT) -->
      <div style="position:absolute;top:max(14px, calc(var(--sat) - 20px));left:12px;right:12px;display:flex;justify-content:space-between;align-items:center;z-index:20;pointer-events:auto;">
        <!-- White Circular Back Button -->
        <button onclick="openScreen('gramhaul', null)" style="width:40px;height:40px;border-radius:50%;background:#FFFFFF;border:none;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 12px rgba(0,0,0,0.18);cursor:pointer;flex-shrink:0;">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#0F172A" stroke-width="2.5" stroke-linecap="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
        </button>

        <!-- White Status Pill in Center -->
        <div id="gh-tracking-top-status-pill" style="background:#FFFFFF;border-radius:999px;padding:8px 16px;display:flex;align-items:center;gap:8px;box-shadow:0 2px 14px rgba(0,0,0,0.16);flex-shrink:0;">
          <span id="gh-tracking-status-dot" style="width:8px;height:8px;border-radius:50%;background:#22C55E;box-shadow:0 0 8px #22C55E;display:inline-block;animation:radarPulse 1.4s infinite;flex-shrink:0;"></span>
          <span id="gh-tracking-top-status-text" style="font-size:12.5px;font-weight:800;color:#0F172A;white-space:nowrap;">Radar Geofenced · 10 KM Radius</span>
        </div>

        <!-- White Circular Recenter Button with High-End GPS Crosshair SVG -->
        <button onclick="recenterTrackingMap()" title="Recenter" style="width:40px;height:40px;border-radius:50%;background:#FFFFFF;border:none;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 12px rgba(0,0,0,0.18);cursor:pointer;flex-shrink:0;">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2.5" stroke-linecap="round"><circle cx="12" cy="12" r="7"/><circle cx="12" cy="12" r="3" fill="#2563EB"/><line x1="12" y1="2" x2="12" y2="5"/><line x1="12" y1="19" x2="12" y2="22"/><line x1="2" y1="12" x2="5" y2="12"/><line x1="19" y1="12" x2="22" y2="12"/></svg>
        </button>
      </div>

      <!-- FLOATING BOTTOM CONTAINER FOR SEARCHING RADAR OR COCKPIT SHEET (FULL WIDTH, NO MAX-WIDTH CAP) -->
      <div id="gh-tracking-bottom-container" style="position:absolute;bottom:0;left:0;right:0;width:100%;z-index:20;pointer-events:auto;display:flex;flex-direction:column;margin:0;padding:0;">
      </div>
    </div>
    `;
  },
"""

print("Views ready for insertion!")
