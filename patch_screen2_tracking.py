#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
patch_screen2_tracking.py
Updates Screen 2 (Tracking: searching + dispatched) in index.html and nukrop_emulator.html:
1. Top bar: white circular back button + white status pill + white recenter button (Rapido-exact pills).
2. max-width:430px cap removed — sheet now spans full screen width.
3. Searching radar card: full-width, rounded top corners (border-radius: 24px 24px 0 0).
4. Green banner + driver cockpit: edge-to-edge, no side gaps (width: 100%, margin: 0, padding: 0).
"""

import sys, shutil

def apply_tracking_patch(file_path):
    print(f"Applying Screen 2 patch to {file_path}...")
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Backup
    shutil.copy2(file_path, file_path + ".bak_s2")

    # 1. Update APP_VIEWS.gramhaul_tracking with Rapido-exact white top bar pills and full-width container
    OLD_TRACKING_VIEW = r"""/* ── RAPIDO FULLSCREEN LIVE TRACKING VIEW ── */
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
  },"""

    NEW_TRACKING_VIEW = r"""/* ── RAPIDO FULLSCREEN LIVE TRACKING VIEW ── */
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

        <!-- White Circular Recenter Button -->
        <button onclick="recenterTrackingMap()" style="width:40px;height:40px;border-radius:50%;background:#FFFFFF;border:none;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 12px rgba(0,0,0,0.18);cursor:pointer;font-size:18px;flex-shrink:0;">
          🎯
        </button>
      </div>

      <!-- FLOATING BOTTOM CONTAINER FOR SEARCHING RADAR OR COCKPIT SHEET (FULL WIDTH, NO MAX-WIDTH CAP) -->
      <div id="gh-tracking-bottom-container" style="position:absolute;bottom:0;left:0;right:0;width:100%;z-index:20;pointer-events:auto;display:flex;flex-direction:column;margin:0;padding:0;">
      </div>
    </div>
    `;
  },"""

    if OLD_TRACKING_VIEW in text:
        text = text.replace(OLD_TRACKING_VIEW, NEW_TRACKING_VIEW, 1)
        print("  [+] Replaced tracking top bar with white Rapido-exact pills")
    else:
        print("  [!] OLD_TRACKING_VIEW not found verbatim, checking substring...")
        # Fallback find
        idx_t = text.find("/* ── RAPIDO FULLSCREEN LIVE TRACKING VIEW ── */")
        if idx_t != -1:
            idx_e = text.find("agristack: () => {", idx_t)
            text = text[:idx_t] + NEW_TRACKING_VIEW + "\n  " + text[idx_e:]
            print("  [+] Spliced NEW_TRACKING_VIEW via boundaries")

    # 2. Update renderTrackingSearchingState and renderTrackingDispatchedState
    NEW_SEARCHING_DISPATCHED_FNS = r"""function renderTrackingSearchingState(activeTrip) {
  const topText = document.getElementById('gh-tracking-top-status-text');
  if (topText) topText.textContent = 'Radar Geofenced · 10 KM Radius';

  const bottomEl = document.getElementById('gh-tracking-bottom-container');
  if (bottomEl) {
    bottomEl.innerHTML = `
      <div style="background:#0F172A;width:100%;border-radius:24px 24px 0 0;padding:20px 18px max(28px,env(safe-area-inset-bottom,28px));box-shadow:0 -10px 40px rgba(0,0,0,0.6);border-top:1px solid #334155;animation:slideUp 0.25s cubic-bezier(0.16, 1, 0.3, 1);color:#FFFFFF;text-align:center;box-sizing:border-box;margin:0;">
        <div style="width:38px;height:4px;background:rgba(255,255,255,0.25);border-radius:10px;margin:0 auto 16px;"></div>

        <!-- Radar Animation Rings Container -->
        <div style="position:relative;width:80px;height:80px;margin:0 auto 14px;display:flex;align-items:center;justify-content:center;">
          <div style="position:absolute;width:80px;height:80px;border-radius:50%;background:rgba(34,197,94,0.15);border:1.5px solid rgba(34,197,94,0.5);animation:radarRipple 1.6s ease-out infinite;"></div>
          <div style="position:absolute;width:55px;height:55px;border-radius:50%;background:rgba(34,197,94,0.25);animation:radarRipple 1.6s ease-out infinite 0.4s;"></div>
          <div style="width:46px;height:46px;border-radius:50%;background:linear-gradient(135deg,#16A34A,#15803D);display:flex;align-items:center;justify-content:center;font-size:24px;box-shadow:0 0 20px rgba(34,197,94,0.6);z-index:2;">
            🚚
          </div>
        </div>

        <div style="font-size:17.5px;font-weight:900;color:#FFFFFF;margin-bottom:4px;letter-spacing:-0.2px;">
          Finding Commercial Trucks...
        </div>
        <div style="font-size:12px;color:#94A3B8;font-weight:600;margin-bottom:14px;">
          Connecting with verified drivers near Himayath Nagar
        </div>

        <div style="background:#1E293B;border:1px solid #334155;border-radius:14px;padding:12px 14px;margin-bottom:16px;display:flex;flex-direction:column;gap:6px;text-align:left;font-size:12px;">
          <div style="display:flex;justify-content:space-between;"><span style="color:#94A3B8;">Selected Tier:</span><strong style="color:#FFFFFF;">${activeTrip.vehicle}</strong></div>
          <div style="display:flex;justify-content:space-between;"><span style="color:#94A3B8;">Produce Load:</span><strong style="color:#FFFFFF;">${activeTrip.crop} (${activeTrip.sacks})</strong></div>
          <div style="display:flex;justify-content:space-between;"><span style="color:#94A3B8;">Destination:</span><strong style="color:#22C55E;">${activeTrip.mandi}</strong></div>
          <div style="display:flex;justify-content:space-between;"><span style="color:#94A3B8;">Estimated Fare:</span><strong style="color:#22C55E;font-size:14px;">₹${activeTrip.fare} (0% Commission)</strong></div>
        </div>

        <button onclick="cancelAndReturnToGramhaul()" style="width:100%;height:48px;background:#334155;color:#F1F5F9;border:none;border-radius:14px;font-size:14px;font-weight:800;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:6px;">
          <span>✕</span> <span>Cancel Search</span>
        </button>
      </div>
    `;
  }

  if (gramhaulTrackingMap) {
    const v = GRAMHAUL_TIER_AVAILABLE_VEHICLES[activeTrip.tier] || GRAMHAUL_TIER_AVAILABLE_VEHICLES[1];
    const ghostIcon = L.divIcon({
      className: 'gh-ghost-marker',
      html: `<div style="width:32px;height:32px;border-radius:50%;background:rgba(15,23,42,0.85);border:2px solid #22C55E;display:flex;align-items:center;justify-content:center;font-size:16px;box-shadow:0 0 12px rgba(34,197,94,0.5);transform:translate(-50%, -50%);">🚚</div>`,
      iconSize: [0, 0]
    });
    if (trackingDriverMarker) {
      try { gramhaulTrackingMap.removeLayer(trackingDriverMarker); } catch(e) {}
    }
    trackingDriverMarker = L.marker(v.coords, { icon: ghostIcon }).addTo(gramhaulTrackingMap);

    const bounds = L.latLngBounds([[17.3980, 78.4900], v.coords]);
    gramhaulTrackingMap.fitBounds(bounds, { padding: [60, 60], maxZoom: 15 });
  }

  if (trackingSearchTimeout) clearTimeout(trackingSearchTimeout);
  trackingSearchTimeout = setTimeout(() => {
    activeTrip.status = 'DISPATCHED';
    localStorage.setItem('nukrop_active_trip', JSON.stringify(activeTrip));
    renderTrackingDispatchedState(activeTrip);
    if (typeof showLuxuryToast === 'function') {
      showLuxuryToast(`✅ Driver ${activeTrip.driverName} accepted! Arriving in ${activeTrip.etaMins || 2} min`, 'success');
    }
  }, 1800);
}

function renderTrackingDispatchedState(activeTrip) {
  if (trackingSearchTimeout) {
    clearTimeout(trackingSearchTimeout);
    trackingSearchTimeout = null;
  }

  const v = GRAMHAUL_TIER_AVAILABLE_VEHICLES[activeTrip.tier] || GRAMHAUL_TIER_AVAILABLE_VEHICLES[1];
  const driverName = activeTrip.driverName || v.driver;
  const plate = activeTrip.driverPlate || v.plate;
  const vehicleName = activeTrip.vehicle || v.name;
  const rating = activeTrip.driverRating || v.rating;
  const eta = activeTrip.etaMins || v.etaMins || 2;
  const otp = activeTrip.otp || v.otp || '4491';
  const fare = activeTrip.fare || 380;
  const crop = activeTrip.crop || 'Cotton';
  const sacks = activeTrip.sacks || '40 Sacks';
  const mandiName = activeTrip.mandi || 'Gudimalkapur Vegetable & Flower APMC Yard';

  const now = new Date();
  const arrivalTime = new Date(now.getTime() + 14 * 60000);
  const formattedArrival = arrivalTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true });

  const topText = document.getElementById('gh-tracking-top-status-text');
  if (topText) topText.textContent = `Driver ${driverName} is ${eta} min away`;

  const bottomEl = document.getElementById('gh-tracking-bottom-container');
  if (bottomEl) {
    bottomEl.innerHTML = `
      <div style="width:100%;animation:slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);margin:0;padding:0;box-sizing:border-box;">
        
        <!-- Top Neon-Green Banner (Edge-to-Edge) -->
        <div style="width:100%;box-sizing:border-box;background:#22C55E;border-radius:24px 24px 0 0;padding:12px 18px 11px;display:flex;align-items:center;justify-content:space-between;box-shadow:0 -4px 14px rgba(34,197,94,0.3);margin:0;">
          <div style="color:#0F172A;font-weight:900;font-size:14.5px;letter-spacing:-0.2px;display:flex;align-items:center;gap:6px;">
            <span>🚚</span>
            <span>Your driver is on the way</span>
          </div>
          <div style="background:#14532D;color:#FFFFFF;font-size:11.5px;font-weight:900;padding:4px 12px;border-radius:9999px;">
            ${eta} min
          </div>
        </div>

        <!-- Main Dark Bento Cockpit Card (Edge-to-Edge, NO SIDE GAPS) -->
        <div style="width:100%;box-sizing:border-box;background:#0F172A;padding:18px 18px max(28px,env(safe-area-inset-bottom,28px));color:#FFFFFF;box-shadow:0 -10px 40px rgba(0,0,0,0.5);border-top:1px solid rgba(255,255,255,0.08);margin:0;">
          
          <!-- Driver Profile Row -->
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;">
            <div style="display:flex;align-items:center;gap:12px;">
              <div style="position:relative;width:50px;height:50px;border-radius:50%;overflow:hidden;background:#DCFCE7;border:2.5px solid #22C55E;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                <span style="font-size:28px;">👨🏻‍💼</span>
              </div>
              <div>
                <div style="display:flex;align-items:center;gap:6px;">
                  <span style="font-size:16px;font-weight:900;color:#FFFFFF;">${driverName}</span>
                  <span style="font-size:12.5px;font-weight:900;color:#F59E0B;display:flex;align-items:center;gap:2px;">★ ${rating.toString().replace(/[^0-9.]/g, '') || '4.9'}</span>
                </div>
                <div style="font-size:12.5px;color:#94A3B8;font-weight:600;margin-top:2px;">
                  ${vehicleName}
                </div>
              </div>
            </div>

            <!-- Commercial License Plate Badge (Yellow Indian Commercial Plate) -->
            <div style="background:#FBBF24;color:#0F172A;border:1.5px solid #000000;border-radius:8px;padding:4px 10px;font-size:12.5px;font-weight:900;letter-spacing:1px;font-family:monospace;box-shadow:0 2px 6px rgba(0,0,0,0.3);flex-shrink:0;">
              ${plate}
            </div>
          </div>

          <!-- PROMINENT RAPIDO START TRIP OTP BADGE -->
          <div style="background:#FEF3C7;border:1.5px solid #F59E0B;border-radius:14px;padding:12px 16px;margin-bottom:16px;display:flex;align-items:center;justify-content:space-between;">
            <div>
              <div style="font-size:10px;font-weight:900;color:#92400E;text-transform:uppercase;letter-spacing:0.06em;">START TRIP PIN / OTP</div>
              <div style="font-size:11.5px;color:#78350F;margin-top:2px;font-weight:600;">Share with driver only after loading sacks</div>
            </div>
            <div style="background:#F59E0B;color:#000000;font-size:22px;font-weight:900;letter-spacing:3px;padding:6px 14px;border-radius:10px;box-shadow:0 2px 8px rgba(245,158,11,0.35);">
              ${otp}
            </div>
          </div>

          <!-- 4 Tactile Circular Action Buttons -->
          <div style="display:flex;align-items:center;justify-content:space-between;padding:0 8px;margin-bottom:16px;">
            
            <!-- Call Action -->
            <div onclick="triggerDriverCall('${driverName}', '${v.phone}')" style="display:flex;flex-direction:column;align-items:center;gap:6px;cursor:pointer;">
              <div style="width:48px;height:48px;border-radius:50%;background:#1E293B;border:1px solid #334155;display:flex;align-items:center;justify-content:center;font-size:18px;color:#FFFFFF;box-shadow:0 3px 10px rgba(0,0,0,0.2);">
                📞
              </div>
              <span style="font-size:11px;color:#94A3B8;font-weight:700;">Call</span>
            </div>

            <!-- Message Action -->
            <div onclick="openDriverLiveChatModal('${driverName}', '${plate}')" style="display:flex;flex-direction:column;align-items:center;gap:6px;cursor:pointer;">
              <div style="width:48px;height:48px;border-radius:50%;background:#1E293B;border:1px solid #334155;display:flex;align-items:center;justify-content:center;font-size:18px;color:#FFFFFF;box-shadow:0 3px 10px rgba(0,0,0,0.2);">
                💬
              </div>
              <span style="font-size:11px;color:#94A3B8;font-weight:700;">Message</span>
            </div>

            <!-- Share Action -->
            <div onclick="shareLiveHaulTrip('${activeTrip.id || 'GH-4491'}')" style="display:flex;flex-direction:column;align-items:center;gap:6px;cursor:pointer;">
              <div style="width:48px;height:48px;border-radius:50%;background:#1E293B;border:1px solid #334155;display:flex;align-items:center;justify-content:center;font-size:18px;color:#FFFFFF;box-shadow:0 3px 10px rgba(0,0,0,0.2);">
                🔗
              </div>
              <span style="font-size:11px;color:#94A3B8;font-weight:700;">Share</span>
            </div>

            <!-- Cancel Action -->
            <div onclick="cancelActiveHaulTripAndExit()" style="display:flex;flex-direction:column;align-items:center;gap:6px;cursor:pointer;">
              <div style="width:48px;height:48px;border-radius:50%;background:#1E293B;border:1px solid #334155;display:flex;align-items:center;justify-content:center;font-size:18px;color:#EF4444;box-shadow:0 3px 10px rgba(0,0,0,0.2);">
                ✕
              </div>
              <span style="font-size:11px;color:#94A3B8;font-weight:700;">Cancel</span>
            </div>

          </div>

          <!-- Route Progress Card -->
          <div style="background:#111C38;border:1px solid #1E293B;border-radius:18px;padding:14px 16px;margin-bottom:14px;">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">
              <div>
                <div style="font-size:11px;color:#94A3B8;font-weight:700;">Pickup in</div>
                <div style="font-size:17px;font-weight:900;color:#FFFFFF;margin-top:2px;">${eta} min</div>
              </div>
              <div style="text-align:right;">
                <div style="font-size:11px;color:#94A3B8;font-weight:700;">Arrive by</div>
                <div style="font-size:17px;font-weight:900;color:#FFFFFF;margin-top:2px;">${formattedArrival}</div>
              </div>
            </div>

            <!-- Animated Progress Line Tracker -->
            <div style="display:flex;align-items:center;gap:3px;margin-top:8px;">
              <div style="width:25%;height:4px;background:#22C55E;border-radius:2px;"></div>
              <div style="font-size:16px;animation:truckDrive 2s ease-in-out infinite;transform:scaleX(-1);">🚚</div>
              <div style="flex:1;height:2px;border-top:2px dashed #334155;"></div>
              <div style="width:8px;height:8px;border-radius:50%;background:#22C55E;"></div>
              <div style="flex:1;height:2px;border-top:2px dashed #334155;"></div>
              <div style="width:8px;height:8px;border-radius:50%;background:#475569;"></div>
            </div>
          </div>

          <!-- Expandable "See trip details" Drawer -->
          <div style="background:#1E293B;border:1px solid #334155;border-radius:14px;overflow:hidden;">
            <div onclick="toggleTripDetailsDrawer()" style="padding:12px 14px;display:flex;align-items:center;justify-content:space-between;cursor:pointer;">
              <span style="font-size:12.5px;font-weight:800;color:#E2E8F0;">See trip details</span>
              <span id="gh-trip-arrow" style="font-size:12px;color:#94A3B8;transition:transform 0.2s ease;">▾</span>
            </div>

            <div id="gh-trip-details-content" style="display:none;padding:0 14px 14px;font-size:12px;flex-direction:column;gap:8px;border-top:1px solid #334155;">
              <div style="display:flex;justify-content:space-between;margin-top:8px;"><span style="color:#94A3B8;">📍 Farm Pickup:</span><strong style="color:#FFFFFF;">${activeTrip.pickup || 'Himayath Nagar Farm, Telangana'}</strong></div>
              <div style="display:flex;justify-content:space-between;"><span style="color:#94A3B8;">🏢 Destination Mandi:</span><strong style="color:#22C55E;">${mandiName}</strong></div>
              <div style="display:flex;justify-content:space-between;"><span style="color:#94A3B8;">🌾 Produce Load:</span><strong style="color:#FFFFFF;">${crop} (${sacks})</strong></div>
              <div style="display:flex;justify-content:space-between;"><span style="color:#94A3B8;">💰 Freight Fare:</span><strong style="color:#22C55E;font-size:14px;">₹${fare} (0% Commission)</strong></div>
            </div>
          </div>

        </div>
      </div>
    `;
  }

  if (gramhaulTrackingMap) {
    if (trackingDriverMarker) {
      try { gramhaulTrackingMap.removeLayer(trackingDriverMarker); } catch(e) {}
    }
    if (trackingRoutePolyline) {
      try { gramhaulTrackingMap.removeLayer(trackingRoutePolyline); } catch(e) {}
    }

    const truckIcon = L.divIcon({
      className: 'gh-live-dispatched-truck',
      html: `<div style="display:flex;flex-direction:column;align-items:center;transform:translate(-50%, -100%);">
        <div style="background:#FFFFFF;color:#0F172A;border:1.5px solid #22C55E;padding:2px 7px;border-radius:6px;font-size:9.5px;font-weight:900;white-space:nowrap;box-shadow:0 3px 10px rgba(0,0,0,0.3);letter-spacing:0.5px;">${plate}</div>
        <div style="width:38px;height:38px;border-radius:50%;background:#0F172A;border:2.5px solid #22C55E;display:flex;align-items:center;justify-content:center;font-size:20px;box-shadow:0 0 16px rgba(34,197,94,0.6);margin-top:2px;">
          🚚
        </div>
      </div>`,
      iconSize: [0, 0]
    });

    trackingDriverMarker = L.marker(v.coords, { icon: truckIcon }).addTo(gramhaulTrackingMap);

    const routePoints = [
      v.coords,
      [(v.coords[0] + 17.3980) / 2 + 0.001, (v.coords[1] + 78.4900) / 2],
      [17.3980, 78.4900]
    ];
    trackingRoutePolyline = L.polyline(routePoints, {
      color: '#22C55E',
      weight: 4,
      dashArray: '8, 8',
      opacity: 0.9
    }).addTo(gramhaulTrackingMap);

    const bounds = L.latLngBounds([[17.3980, 78.4900], v.coords]);
    gramhaulTrackingMap.fitBounds(bounds, { padding: [60, 60], maxZoom: 15 });
  }
}"""

    idx_fns_start = text.find("function renderTrackingSearchingState")
    idx_fns_end = text.find("function recenterTrackingMap")
    if idx_fns_start != -1 and idx_fns_end != -1:
        text = text[:idx_fns_start] + NEW_SEARCHING_DISPATCHED_FNS + "\n\n" + text[idx_fns_end:]
        print("  [+] Successfully updated renderTrackingSearchingState and renderTrackingDispatchedState (edge-to-edge, no side gaps, full width)")
    else:
        print("  [!] Could not locate functions block between renderTrackingSearchingState and recenterTrackingMap")

    # 3. Remove any remaining max-width:430px in chat modal
    if 'max-width:430px;' in text:
        text = text.replace('max-width:430px;', '')
        print("  [+] Removed max-width:430px from modal styles")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"DONE patching Screen 2 for {file_path}.\n")

apply_tracking_patch("app/src/main/assets/index.html")
apply_tracking_patch("nukrop_emulator.html")
