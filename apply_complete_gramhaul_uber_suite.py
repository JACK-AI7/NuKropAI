import os, re, sys

sys.stdout.reconfigure(encoding='utf-8')

# Truck SVGs
TATA_ACE_SVG = '''<svg width="68" height="42" viewBox="0 0 120 70" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="38" y="18" width="76" height="32" rx="3" fill="#F8FAFC" stroke="#94A3B8" stroke-width="1.5"/>
  <path d="M40 22H112M40 32H112M40 42H112" stroke="#CBD5E1" stroke-width="1"/>
  <path d="M40 18 Q 75 10 112 18" fill="#16A34A" fill-opacity="0.25" stroke="#16A34A" stroke-width="1.5"/>
  <path d="M12 48 L12 28 C12 24 16 20 22 18 L34 18 C37 18 38 20 38 24 L38 48 Z" fill="#FFFFFF" stroke="#64748B" stroke-width="1.5"/>
  <path d="M16 28 L24 20 L34 20 L34 30 L16 30 Z" fill="#38BDF8" fill-opacity="0.5" stroke="#0284C7" stroke-width="1"/>
  <rect x="8" y="40" width="5" height="7" rx="1.5" fill="#FBBF24" stroke="#D97706" stroke-width="0.8"/>
  <rect x="8" y="47" width="30" height="5" rx="2" fill="#334155"/>
  <rect x="15" y="49" width="98" height="4" fill="#1E293B"/>
  <circle cx="28" cy="52" r="11" fill="#0F172A"/>
  <circle cx="28" cy="52" r="6" fill="#94A3B8"/>
  <circle cx="28" cy="52" r="2.5" fill="#0F172A"/>
  <circle cx="94" cy="52" r="11" fill="#0F172A"/>
  <circle cx="94" cy="52" r="6" fill="#94A3B8"/>
  <circle cx="94" cy="52" r="2.5" fill="#0F172A"/>
</svg>'''

BOLERO_MAXI_SVG = '''<svg width="68" height="42" viewBox="0 0 130 70" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="46" y="24" width="78" height="26" rx="2" fill="#F1F5F9" stroke="#94A3B8" stroke-width="1.5"/>
  <rect x="50" y="28" width="70" height="18" fill="#E2E8F0"/>
  <path d="M8 48 L8 32 C8 30 10 28 14 26 L26 18 C28 16 32 16 36 16 L44 16 C46 16 46 18 46 22 L46 48 Z" fill="#FFFFFF" stroke="#475569" stroke-width="1.5"/>
  <path d="M16 28 L27 19 L36 19 L36 30 L14 30 Z" fill="#38BDF8" fill-opacity="0.5" stroke="#0284C7" stroke-width="1"/>
  <rect x="38" y="19" width="6" height="11" fill="#38BDF8" fill-opacity="0.4" stroke="#0284C7" stroke-width="0.8"/>
  <rect x="6" y="34" width="4" height="10" fill="#CBD5E1" stroke="#475569" stroke-width="1"/>
  <rect x="5" y="44" width="40" height="6" rx="2" fill="#1E293B"/>
  <rect x="10" y="49" width="112" height="4" fill="#0F172A"/>
  <circle cx="28" cy="52" r="11.5" fill="#0F172A"/>
  <circle cx="28" cy="52" r="6.5" fill="#64748B"/>
  <circle cx="28" cy="52" r="2.5" fill="#0F172A"/>
  <circle cx="102" cy="52" r="11.5" fill="#0F172A"/>
  <circle cx="102" cy="52" r="6.5" fill="#64748B"/>
  <circle cx="102" cy="52" r="2.5" fill="#0F172A"/>
</svg>'''

EICHER_PRO_SVG = '''<svg width="68" height="42" viewBox="0 0 140 70" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="44" y="10" width="90" height="40" rx="3" fill="#F8FAFC" stroke="#64748B" stroke-width="1.5"/>
  <path d="M46 16 H132 M46 26 H132 M46 36 H132 M46 46 H132" stroke="#E2E8F0" stroke-width="1.5"/>
  <path d="M72 10 V50 M104 10 V50" stroke="#CBD5E1" stroke-width="1.5"/>
  <path d="M8 48 L8 22 C8 16 12 12 18 12 L42 12 C44 12 44 14 44 18 L44 48 Z" fill="#15803D" stroke="#14532D" stroke-width="1.5"/>
  <path d="M12 26 L16 16 L34 16 L34 28 L12 28 Z" fill="#E0F2FE" fill-opacity="0.8" stroke="#0284C7" stroke-width="1"/>
  <rect x="36" y="16" width="6" height="12" fill="#E0F2FE" fill-opacity="0.6" stroke="#0284C7" stroke-width="0.8"/>
  <rect x="6" y="42" width="38" height="8" rx="2" fill="#1E293B"/>
  <rect x="6" y="38" width="5" height="5" fill="#FBBF24"/>
  <rect x="12" y="49" width="122" height="5" fill="#0F172A"/>
  <circle cx="26" cy="52" r="12" fill="#0F172A"/>
  <circle cx="26" cy="52" r="7" fill="#CBD5E1"/>
  <circle cx="26" cy="52" r="3" fill="#0F172A"/>
  <circle cx="94" cy="52" r="12" fill="#0F172A"/>
  <circle cx="94" cy="52" r="7" fill="#CBD5E1"/>
  <circle cx="94" cy="52" r="3" fill="#0F172A"/>
  <circle cx="120" cy="52" r="12" fill="#0F172A"/>
  <circle cx="120" cy="52" r="7" fill="#CBD5E1"/>
  <circle cx="120" cy="52" r="3" fill="#0F172A"/>
</svg>'''

GRAMHAUL_FULL_VIEW = """
  /* ── 2. GRAMHAUL LOGISTICS: UBER-STYLE WHITE THEME ON-DEMAND DISPATCH ── */
  gramhaul: () => {
    const t = I18N[currentLang] || I18N.en;
    const isTe = currentLang === 'te';
    const isHi = currentLang === 'hi';

    const headerTitle = TL('GramHaul Logistics', 'గ్రామ్‌హాల్ లాజిస్టిక్స్', 'ग्रामहॉल लॉजिस्टिक्स');
    const headerSub = TL('Live GPS Fleet · Farm-to-Mandi', 'లైవ్ GPS రవాణా · ఫార్మ్-టు-మండి', 'लाइव GPS ढुलाई');

    return `
    <div style="background:#F8FAF8;min-height:100%;padding-bottom:110px;font-family:-apple-system,BlinkMacSystemFont,'Plus Jakarta Sans','Inter',sans-serif;">
      <!-- 1. Header Bar -->
      <div style="background:#FFFFFF;padding:14px 18px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #EEF2F6;position:sticky;top:0;z-index:40;">
        <div style="display:flex;align-items:center;gap:12px;">
          <button onclick="openScreen('home',null);syncSideNav('btn-home')" style="background:#F1F5F9;border:none;cursor:pointer;width:36px;height:36px;border-radius:12px;display:flex;align-items:center;justify-content:center;color:#0F172A;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
          </button>
          <div>
            <div style="font-size:16.5px;font-weight:900;color:#0F172A;letter-spacing:-0.3px;">${headerTitle}</div>
            <div style="font-size:11px;color:#64748B;font-weight:600;">${headerSub}</div>
          </div>
        </div>
        <div style="display:flex;gap:6px;">
          <button onclick="openScreen('driver_dashboard',null)" style="background:#DCFCE7;border:1px solid #86EFAC;color:#15803D;padding:6px 12px;border-radius:12px;font-size:11.5px;font-weight:800;cursor:pointer;display:flex;align-items:center;gap:4px;">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>
            Driver Mode
          </button>
        </div>
      </div>

      <div style="padding:16px 16px 0;">
        <!-- 2. Pickup & Drop Route Card (Uber-Style Floating White Card) -->
        <div style="background:#FFFFFF;border:1.5px solid #E2E8F0;border-radius:22px;padding:16px;box-shadow:0 4px 20px -2px rgba(15,23,42,0.06);margin-bottom:16px;">
          <!-- Pickup Row -->
          <div style="display:flex;align-items:center;gap:12px;">
            <div style="width:12px;height:12px;border-radius:50%;background:#94A3B8;flex-shrink:0;border:2px solid #E2E8F0;"></div>
            <div style="flex:1;">
              <div style="font-size:10px;font-weight:800;color:#94A3B8;text-transform:uppercase;letter-spacing:0.5px;">Pickup location</div>
              <div style="font-size:13.5px;font-weight:800;color:#0F172A;">🌾 Ramesh Rao's Farm, Narsampet Rural</div>
            </div>
          </div>

          <!-- Connecting line with Swap button -->
          <div style="display:flex;align-items:center;margin:6px 0 6px 5px;position:relative;">
            <div style="width:2px;height:22px;background:#CBD5E1;"></div>
            <div style="flex:1;height:1px;background:#F1F5F9;margin-left:17px;"></div>
            <button onclick="swapGramhaulLocations()" style="position:absolute;right:0;width:32px;height:32px;border-radius:50%;background:#F8FAFC;border:1px solid #E2E8F0;display:flex;align-items:center;justify-content:center;color:#64748B;cursor:pointer;">
              ⇅
            </button>
          </div>

          <!-- Drop Row -->
          <div style="display:flex;align-items:center;gap:12px;">
            <div style="width:12px;height:12px;border-radius:50%;background:#16A34A;flex-shrink:0;box-shadow:0 0 0 3px #DCFCE7;"></div>
            <div style="flex:1;">
              <div style="font-size:10px;font-weight:800;color:#16A34A;text-transform:uppercase;letter-spacing:0.5px;">Drop location</div>
              <div style="font-size:13.5px;font-weight:800;color:#0F172A;">📍 Warangal Enamamula APMC Yard (Gate 3)</div>
            </div>
          </div>

          <!-- Quick Location Chips -->
          <div style="display:flex;gap:8px;margin-top:14px;padding-top:12px;border-top:1px solid #F1F5F9;overflow-x:auto;">
            <button style="background:#F8FAFC;border:1px solid #E2E8F0;padding:6px 12px;border-radius:10px;font-size:11.5px;font-weight:700;color:#475569;display:flex;align-items:center;gap:4px;white-space:nowrap;cursor:pointer;">
              🏠 My Farm (12 min)
            </button>
            <button style="background:#F0FDF4;border:1px solid #86EFAC;padding:6px 12px;border-radius:10px;font-size:11.5px;font-weight:800;color:#15803D;display:flex;align-items:center;gap:4px;white-space:nowrap;cursor:pointer;">
              🏢 Warangal APMC (4.8 km)
            </button>
            <button style="background:#F8FAFC;border:1px solid #E2E8F0;padding:6px 12px;border-radius:10px;font-size:11.5px;font-weight:700;color:#475569;display:flex;align-items:center;gap:4px;white-space:nowrap;cursor:pointer;">
              🏭 Bowenpally Mandi (128 km)
            </button>
          </div>
        </div>

        <!-- 3. Real OpenStreetMap / Leaflet High-Res Live Navigation Surface -->
        <div style="background:#FFFFFF;border:1.5px solid #E2E8F0;border-radius:22px;padding:14px;box-shadow:0 4px 16px -2px rgba(15,23,42,0.06);margin-bottom:18px;position:relative;overflow:hidden;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
            <div style="display:flex;align-items:center;gap:6px;font-size:12px;font-weight:800;color:#0F172A;">
              <span style="width:8px;height:8px;border-radius:50%;background:#16A34A;display:inline-block;box-shadow:0 0 8px #16A34A;"></span>
              Live GPS Fleet Telemetry
            </div>
            <div style="background:#DCFCE7;color:#15803D;font-size:10.5px;font-weight:800;padding:3px 8px;border-radius:8px;">
              3 Trucks Nearby
            </div>
          </div>

          <!-- Clean Map Vector Viewport -->
          <div style="height:175px;background:#F8FAFC;border-radius:16px;position:relative;overflow:hidden;border:1px solid #E2E8F0;">
            <div style="position:absolute;inset:0;background-image:linear-gradient(#EEF2F6 1px, transparent 1px), linear-gradient(90deg, #EEF2F6 1px, transparent 1px);background-size:24px 24px;opacity:0.8;"></div>
            
            <svg style="position:absolute;inset:0;width:100%;height:100%;">
              <path d="M 20 150 Q 150 90 260 140 T 400 60" stroke="#CBD5E1" stroke-width="8" fill="none" stroke-linecap="round"/>
              <path d="M 50 130 L 120 130 L 190 70 L 290 70 L 360 30" stroke="#16A34A" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M 50 130 L 120 130 L 190 70 L 290 70 L 360 30" stroke="#86EFAC" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>

            <!-- Origin Marker (Farm) -->
            <div style="position:absolute;left:40px;top:118px;display:flex;flex-direction:column;align-items:center;">
              <div style="background:#16A34A;color:#FFF;font-size:9px;font-weight:900;padding:2px 6px;border-radius:6px;box-shadow:0 2px 6px rgba(22,163,74,0.4);white-space:nowrap;margin-bottom:2px;">
                🌾 Your Farm
              </div>
              <div style="width:14px;height:14px;border-radius:50%;background:#FFFFFF;border:3px solid #16A34A;box-shadow:0 0 10px rgba(22,163,74,0.5);"></div>
            </div>

            <!-- Moving Truck Marker on Route -->
            <div style="position:absolute;left:180px;top:54px;display:flex;flex-direction:column;align-items:center;">
              <div style="background:#0F172A;color:#FFF;font-size:9px;font-weight:800;padding:2px 6px;border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,0.25);white-space:nowrap;margin-bottom:2px;">
                🚚 Tata Ace (8 min)
              </div>
              <div style="width:26px;height:26px;border-radius:50%;background:#16A34A;display:flex;align-items:center;justify-content:center;color:#FFF;font-size:12px;box-shadow:0 4px 12px rgba(22,163,74,0.5);">
                🚚
              </div>
            </div>

            <!-- Destination Marker (APMC Mandi) -->
            <div style="position:absolute;right:30px;top:18px;display:flex;flex-direction:column;align-items:center;">
              <div style="background:#DC2626;color:#FFF;font-size:9px;font-weight:900;padding:2px 6px;border-radius:6px;box-shadow:0 2px 6px rgba(220,38,38,0.4);white-space:nowrap;margin-bottom:2px;">
                🏢 APMC Mandi
              </div>
              <div style="width:14px;height:14px;border-radius:50%;background:#FFFFFF;border:3px solid #DC2626;box-shadow:0 0 10px rgba(220,38,38,0.5);"></div>
            </div>

            <button style="position:absolute;right:10px;bottom:10px;width:34px;height:34px;border-radius:10px;background:#FFFFFF;border:1px solid #CBD5E1;box-shadow:0 2px 8px rgba(0,0,0,0.1);display:flex;align-items:center;justify-content:center;color:#0F172A;cursor:pointer;">
              ⌖
            </button>
          </div>
        </div>

        <!-- 4. "Choose a ride" Vehicle Tier Selector (With Real High-End Truck Renders) -->
        <div style="margin-bottom:18px;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
            <h3 style="font-size:16.5px;font-weight:900;color:#0F172A;margin:0;letter-spacing:-0.3px;">
              ${TL('Choose a Vehicle', 'వాహనాన్ని ఎంచుకోండి', 'वाहन चुनें')}
            </h3>
            <span style="font-size:12px;color:#16A34A;font-weight:800;">Shared Pooling (Save 75%)</span>
          </div>

          <!-- Tier 1: Tata Ace 1.5 Ton (Standard - Active Selected) -->
          <div onclick="selectGramhaulRideTier(1)" id="gh-tier-1" style="background:#F0FDF4;border:2px solid #16A34A;border-radius:20px;padding:12px 16px;display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;cursor:pointer;box-shadow:0 4px 14px rgba(22,163,74,0.12);transition:all 0.2s ease;">
            <div style="display:flex;align-items:center;gap:12px;">
              <div style="width:72px;display:flex;align-items:center;justify-content:center;">
                """ + TATA_ACE_SVG + """
              </div>
              <div>
                <div style="display:flex;align-items:center;gap:6px;">
                  <span style="font-size:15px;font-weight:900;color:#0F172A;">Tata Ace 1.5T</span>
                  <span style="background:#DCFCE7;color:#15803D;font-size:10px;font-weight:800;padding:2px 6px;border-radius:6px;">Popular</span>
                </div>
                <div style="font-size:12px;color:#64748B;font-weight:600;margin-top:2px;">
                  8 min away · 22/30 Bags Filled
                </div>
              </div>
            </div>
            <div style="text-align:right;">
              <div style="font-size:17px;font-weight:900;color:#15803D;">₹45 <span style="font-size:11px;color:#64748B;font-weight:600;">/bag</span></div>
              <div style="font-size:11px;color:#94A3B8;text-decoration:line-through;">₹180 /bag</div>
            </div>
          </div>

          <!-- Tier 2: Mahindra Bolero Maxi Truck (Pickup Pro) -->
          <div onclick="selectGramhaulRideTier(2)" id="gh-tier-2" style="background:#FFFFFF;border:1.5px solid #E2E8F0;border-radius:20px;padding:12px 16px;display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;cursor:pointer;box-shadow:0 2px 8px rgba(15,23,42,0.04);transition:all 0.2s ease;">
            <div style="display:flex;align-items:center;gap:12px;">
              <div style="width:72px;display:flex;align-items:center;justify-content:center;">
                """ + BOLERO_MAXI_SVG + """
              </div>
              <div>
                <div style="font-size:15px;font-weight:900;color:#0F172A;">Mahindra Bolero 2.5T</div>
                <div style="font-size:12px;color:#64748B;font-weight:600;margin-top:2px;">
                  14 min away · 15/45 Bags Filled
                </div>
              </div>
            </div>
            <div style="text-align:right;">
              <div style="font-size:17px;font-weight:900;color:#0F172A;">₹65 <span style="font-size:11px;color:#64748B;font-weight:600;">/bag</span></div>
              <div style="font-size:11px;color:#94A3B8;text-decoration:line-through;">₹240 /bag</div>
            </div>
          </div>

          <!-- Tier 3: Eicher Pro 5T Express (Heavy Duty Lorry) -->
          <div onclick="selectGramhaulRideTier(3)" id="gh-tier-3" style="background:#FFFFFF;border:1.5px solid #E2E8F0;border-radius:20px;padding:12px 16px;display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;cursor:pointer;box-shadow:0 2px 8px rgba(15,23,42,0.04);transition:all 0.2s ease;">
            <div style="display:flex;align-items:center;gap:12px;">
              <div style="width:72px;display:flex;align-items:center;justify-content:center;">
                """ + EICHER_PRO_SVG + """
              </div>
              <div>
                <div style="font-size:15px;font-weight:900;color:#0F172A;">Eicher Pro 5T Express</div>
                <div style="font-size:12px;color:#64748B;font-weight:600;margin-top:2px;">
                  22 min away · Direct APMC Mandi
                </div>
              </div>
            </div>
            <div style="text-align:right;">
              <div style="font-size:17px;font-weight:900;color:#0F172A;">₹110 <span style="font-size:11px;color:#64748B;font-weight:600;">/bag</span></div>
              <div style="font-size:11px;color:#94A3B8;text-decoration:line-through;">₹380 /bag</div>
            </div>
          </div>

          <!-- Primary CTA Button (Confirm Tata Ace · ₹450) -->
          <button id="gh-confirm-booking-btn" onclick="confirmGramhaulBooking()" style="width:100%;height:54px;border-radius:18px;background:linear-gradient(135deg, #16A34A, #15803D);color:#FFFFFF;font-size:16px;font-weight:900;border:none;cursor:pointer;box-shadow:0 8px 24px rgba(22,163,74,0.35);display:flex;align-items:center;justify-content:center;gap:8px;transition:all 0.2s ease;">
            <span>Confirm Tata Ace · ₹450</span>
            <span>→</span>
          </button>
        </div>

        <!-- 5. Active Driver On-The-Way Dispatch Sheet (Exact Screen 2 of Reference Image) -->
        <div id="gh-active-trip-sheet" style="background:#FFFFFF;border:1.5px solid #E2E8F0;border-radius:24px;padding:18px 16px;box-shadow:0 8px 30px rgba(15,23,42,0.08);margin-bottom:16px;">
          <!-- Green Header Banner -->
          <div style="background:#16A34A;color:#FFFFFF;border-radius:14px;padding:10px 14px;display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;box-shadow:0 4px 12px rgba(22,163,74,0.25);">
            <div style="display:flex;align-items:center;gap:8px;font-size:13.5px;font-weight:800;">
              <span>🚚</span>
              <span>Your driver is on the way</span>
            </div>
            <div style="background:rgba(255,255,255,0.25);padding:3px 8px;border-radius:8px;font-size:11.5px;font-weight:900;">
              8 min
            </div>
          </div>

          <!-- Driver Profile Card -->
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;">
            <div style="display:flex;align-items:center;gap:12px;">
              <div style="width:50px;height:50px;border-radius:50%;background:linear-gradient(135deg, #D97706, #B45309);display:flex;align-items:center;justify-content:center;color:#FFF;font-size:18px;font-weight:900;box-shadow:0 4px 12px rgba(217,119,6,0.3);border:2px solid #FFF;">
                S
              </div>
              <div>
                <div style="display:flex;align-items:center;gap:6px;">
                  <span style="font-size:15px;font-weight:900;color:#0F172A;">Suresh Yadav</span>
                  <span style="color:#D97706;font-size:12px;font-weight:800;">★ 4.9</span>
                </div>
                <div style="font-size:12px;color:#64748B;font-weight:600;">Tata Ace 1.5T · White</div>
              </div>
            </div>
            <div style="background:#F1F5F9;border:1px solid #E2E8F0;border-radius:8px;padding:5px 9px;font-size:11.5px;font-weight:900;color:#0F172A;letter-spacing:0.5px;">
              TS 03 UB 4491
            </div>
          </div>

          <!-- 4 Circular Action Buttons -->
          <div style="display:grid;grid-template-columns:repeat(4, 1fr);gap:10px;margin-bottom:16px;">
            <button onclick="alert('Calling Driver Suresh Yadav (+91 98765 44910)...')" style="background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:14px;padding:10px 0;display:flex;flex-direction:column;align-items:center;gap:4px;cursor:pointer;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2.2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
              <span style="font-size:11px;font-weight:800;color:#334155;">Call</span>
            </button>
            <button onclick="alert('Opening in-app chat with driver...')" style="background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:14px;padding:10px 0;display:flex;flex-direction:column;align-items:center;gap:4px;cursor:pointer;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2.2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
              <span style="font-size:11px;font-weight:800;color:#334155;">Message</span>
            </button>
            <button onclick="alert('Live GPS tracking link copied!')" style="background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:14px;padding:10px 0;display:flex;flex-direction:column;align-items:center;gap:4px;cursor:pointer;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2.2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
              <span style="font-size:11px;font-weight:800;color:#334155;">Share</span>
            </button>
            <button onclick="if(confirm('Cancel this freight booking?')) alert('Trip cancelled.');" style="background:#FEF2F2;border:1.5px solid #FECACA;border-radius:14px;padding:10px 0;display:flex;flex-direction:column;align-items:center;gap:4px;cursor:pointer;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="2.2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
              <span style="font-size:11px;font-weight:800;color:#DC2626;">Cancel</span>
            </button>
          </div>

          <!-- Journey Progress Timeline -->
          <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:16px;padding:12px 14px;margin-bottom:12px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;font-size:11.5px;font-weight:800;">
              <span style="color:#16A34A;">Pickup in 8 min</span>
              <span style="color:#64748B;">Arrive Mandi 9:52 AM</span>
            </div>
            <div style="height:6px;background:#E2E8F0;border-radius:6px;overflow:hidden;position:relative;">
              <div style="width:40%;height:100%;background:#16A34A;border-radius:6px;"></div>
            </div>
          </div>

          <!-- Expandable Trip Details & Fare Breakdown Accordion (Screen 3 of Reference Image) -->
          <div style="border-top:1px solid #EEF2F6;padding-top:12px;">
            <div onclick="toggleTripDetailsAccordion()" style="display:flex;justify-content:space-between;align-items:center;cursor:pointer;user-select:none;">
              <span style="font-size:13.5px;font-weight:800;color:#0F172A;">See trip details &amp; fare breakdown</span>
              <span id="trip-details-chevron" style="font-size:14px;color:#64748B;font-weight:800;">⌄</span>
            </div>

            <div id="trip-details-content" style="display:block;margin-top:12px;background:#F8FAFC;border-radius:14px;padding:12px;">
              <div style="display:flex;justify-content:space-between;margin-bottom:6px;font-size:12.5px;color:#64748B;">
                <span>Total freight fare (10 Bags)</span>
                <span style="font-size:14px;font-weight:900;color:#0F172A;">₹450.00</span>
              </div>
              <div style="display:flex;justify-content:space-between;margin-bottom:4px;font-size:11.5px;color:#94A3B8;">
                <span>Base fare</span>
                <span>₹150.00</span>
              </div>
              <div style="display:flex;justify-content:space-between;margin-bottom:4px;font-size:11.5px;color:#94A3B8;">
                <span>Distance (4.8 km)</span>
                <span>₹180.00</span>
              </div>
              <div style="display:flex;justify-content:space-between;margin-bottom:10px;font-size:11.5px;color:#94A3B8;">
                <span>Loading helper service</span>
                <span>₹120.00</span>
              </div>

              <!-- Payment Method -->
              <div style="border-top:1px solid #E2E8F0;padding-top:8px;margin-bottom:12px;display:flex;justify-content:space-between;align-items:center;">
                <div style="display:flex;align-items:center;gap:6px;font-size:12px;font-weight:800;color:#0F172A;">
                  <span>💳</span>
                  <span>UPI / Kisan DBT ···· 4242</span>
                </div>
                <span style="color:#16A34A;font-size:11.5px;font-weight:800;">Verified ✓</span>
              </div>

              <!-- Star Rating Section -->
              <div style="border-top:1px solid #E2E8F0;padding-top:10px;text-align:center;">
                <div style="font-size:12.5px;font-weight:800;color:#0F172A;margin-bottom:6px;">How was your ride?</div>
                <div style="display:flex;justify-content:center;gap:8px;font-size:24px;color:#16A34A;cursor:pointer;margin-bottom:8px;">
                  <span>★</span><span>★</span><span>★</span><span>★</span><span>★</span>
                </div>
                <button onclick="alert('Trip feedback submitted successfully!')" style="width:100%;height:44px;background:#16A34A;color:#FFF;border:none;border-radius:12px;font-size:13.5px;font-weight:800;cursor:pointer;">
                  Submit Rating &amp; Finish
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    `;
  },
"""

def apply_update(filepath):
    print(f"Applying complete GramHaul Uber suite with real truck SVGs to {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace gramhaul view in APP_VIEWS
    pattern = r'gramhaul\s*:\s*\(\)\s*=>\s*\{.*?(?=\n\s*\/\* ── [3-9]\.|\n\s*agristack\s*:\s*\(\)\s*=>)'
    if re.search(pattern, content, flags=re.DOTALL):
        content = re.sub(pattern, GRAMHAUL_FULL_VIEW.strip(), content, count=1, flags=re.DOTALL)
        print("Replaced gramhaul view via regex!")
    else:
        start = content.find('gramhaul: () =>')
        if start != -1:
            end = content.find('/* ── 5. FARMER ID', start)
            if end == -1:
                end = content.find('agristack:', start)
            if end != -1:
                content = content[:start] + GRAMHAUL_FULL_VIEW.strip() + '\n\n  ' + content[end:]
                print("Replaced gramhaul view surgically!")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath}!")

if __name__ == '__main__':
    apply_update('app/src/main/assets/index.html')
    apply_update('nukrop_emulator.html')
