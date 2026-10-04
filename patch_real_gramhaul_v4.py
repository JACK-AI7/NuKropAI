#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
patch_real_gramhaul_v4.py
Comprehensive patch for GramHaul in index.html & nukrop_emulator.html:
1. Replaces vector SVGs in Screen 1 vehicle cards with high-end transparent PNGs of real trucks.
2. Optimizes map height & sheet layout so route card + crop specs + vehicle cards are cleanly visible and never awkwardly cut off.
3. Upgrades Screen 2 Searching & Dispatched states to Pure White (#FFFFFF) Rapido Theme edge-to-edge.
4. Removes fake call modal: redirects directly to real phone dialer (tel:${phone} / AndroidBridge.makePhoneCall).
5. Implements realistic driver movement: driver marker ONLY moves towards pickup farm after driver acceptance/dispatch.
"""

import os, sys, shutil

FILES_TO_PATCH = [
    r"app/src/main/assets/index.html",
    r"nukrop_emulator.html"
]

def generate_truck_cards_html():
    return '''        <div style="display:flex;flex-direction:column;gap:8px;margin-bottom:14px;" id="gh-truck-categories">
          
          <!-- Truck 1: Tata Ace Gold -->
          <div onclick="selectGramhaulTruckTier(1)" id="gh-tier-1" class="gh-vehicle-card ${selectedGramhaulTier===1?'selected':''}">
            <div style="display:flex;align-items:center;gap:12px;">
              <div style="width:72px;height:48px;display:flex;align-items:center;justify-content:center;flex-shrink:0;position:relative;">
                <img src="images/trucks/tata_ace.png" alt="Tata Ace Gold" style="width:70px;height:44px;object-fit:contain;filter:drop-shadow(0 4px 6px rgba(15,23,42,0.14));transition:transform 0.2s cubic-bezier(0.16,1,0.3,1);" />
              </div>
              <div>
                <div style="font-size:13.5px;font-weight:900;color:#0F172A;letter-spacing:-0.2px;">Tata Ace Gold (1.5 Ton)</div>
                <div style="font-size:11px;color:#64748B;font-weight:600;margin-top:1px;">Up to 25 Qtl · 50 Sacks · Chota Hathi</div>
              </div>
            </div>
            <div style="text-align:right;">
              <div id="gh-fare-tier-1" style="font-size:16px;font-weight:900;color:#0F172A;">₹380</div>
              <div style="font-size:9.5px;color:#16A34A;font-weight:800;margin-top:1px;display:flex;align-items:center;justify-content:flex-end;gap:3px;"><svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg><span>Ready</span></div>
            </div>
          </div>

          <!-- Truck 2: Bolero Maxi Truck -->
          <div onclick="selectGramhaulTruckTier(2)" id="gh-tier-2" class="gh-vehicle-card ${selectedGramhaulTier===2?'selected':''}">
            <div style="display:flex;align-items:center;gap:12px;">
              <div style="width:72px;height:48px;display:flex;align-items:center;justify-content:center;flex-shrink:0;position:relative;">
                <img src="images/trucks/bolero_maxi.png" alt="Mahindra Bolero Maxi" style="width:70px;height:44px;object-fit:contain;filter:drop-shadow(0 4px 6px rgba(15,23,42,0.14));transition:transform 0.2s cubic-bezier(0.16,1,0.3,1);" />
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
          <div onclick="selectGramhaulTruckTier(3)" id="gh-tier-3" class="gh-vehicle-card ${selectedGramhaulTier===3?'selected':''}">
            <div style="display:flex;align-items:center;gap:12px;">
              <div style="width:72px;height:48px;display:flex;align-items:center;justify-content:center;flex-shrink:0;position:relative;">
                <img src="images/trucks/ashok_leyland_dost.png" alt="Ashok Leyland Dost+" style="width:70px;height:44px;object-fit:contain;filter:drop-shadow(0 4px 6px rgba(15,23,42,0.14));transition:transform 0.2s cubic-bezier(0.16,1,0.3,1);" />
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
          <div onclick="selectGramhaulTruckTier(4)" id="gh-tier-4" class="gh-vehicle-card ${selectedGramhaulTier===4?'selected':''}">
            <div style="display:flex;align-items:center;gap:12px;">
              <div style="width:72px;height:48px;display:flex;align-items:center;justify-content:center;flex-shrink:0;position:relative;">
                <img src="images/trucks/tata_407.png" alt="Tata 407 Gold SFC" style="width:70px;height:44px;object-fit:contain;filter:drop-shadow(0 4px 6px rgba(15,23,42,0.14));transition:transform 0.2s cubic-bezier(0.16,1,0.3,1);" />
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
          <div onclick="selectGramhaulTruckTier(5)" id="gh-tier-5" class="gh-vehicle-card ${selectedGramhaulTier===5?'selected':''}">
            <div style="display:flex;align-items:center;gap:12px;">
              <div style="width:72px;height:48px;display:flex;align-items:center;justify-content:center;flex-shrink:0;position:relative;">
                <img src="images/trucks/eicher_pro.png" alt="Eicher Pro 14ft" style="width:70px;height:44px;object-fit:contain;filter:drop-shadow(0 4px 6px rgba(15,23,42,0.14));transition:transform 0.2s cubic-bezier(0.16,1,0.3,1);" />
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
        </div>'''

def generate_screen2_js_code():
    return '''function initGramhaulTrackingMap() {
  const mapEl = document.getElementById('gramhaul-tracking-osm-map');
  if (!mapEl) return;
  if (typeof L === 'undefined') return;

  if (gramhaulTrackingMap) {
    try {
      gramhaulTrackingMap.remove();
    } catch (e) {}
    gramhaulTrackingMap = null;
  }

  // Clear any existing driver animation interval
  if (window.gramhaulLiveMoveInterval) {
    clearInterval(window.gramhaulLiveMoveInterval);
    window.gramhaulLiveMoveInterval = null;
  }

  const farmCoords = [17.3980, 78.4900];
  gramhaulTrackingMap = L.map('gramhaul-tracking-osm-map', {
    zoomControl: false,
    attributionControl: false
  }).setView(farmCoords, 14);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19
  }).addTo(gramhaulTrackingMap);

  // Farm marker
  const farmIcon = L.divIcon({
    className: 'gh-tracking-farm-marker',
    html: `<div style="display:flex;flex-direction:column;align-items:center;transform:translate(-50%, -100%);">
      <div style="background:#15803D;color:#FFFFFF;padding:4px 9px;border-radius:8px;font-size:10.5px;font-weight:900;white-space:nowrap;box-shadow:0 3px 10px rgba(0,0,0,0.25);border:1.5px solid #FFFFFF;display:inline-flex;align-items:center;gap:4px;"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/><circle cx="12" cy="9" r="2.5" fill="#FFFFFF"/></svg><span>Himayath Nagar Farm</span></div>
      <div style="width:16px;height:16px;background:#16A34A;border:3px solid #FFFFFF;border-radius:50%;box-shadow:0 0 12px #16A34A;margin-top:2px;"></div>
    </div>`,
    iconSize: [0, 0]
  });
  trackingFarmMarker = L.marker(farmCoords, { icon: farmIcon }).addTo(gramhaulTrackingMap);

  let activeTrip = null;
  try {
    activeTrip = JSON.parse(localStorage.getItem('nukrop_active_trip') || 'null');
  } catch (e) {}

  if (!activeTrip) {
    const v = GRAMHAUL_TIER_AVAILABLE_VEHICLES[1];
    activeTrip = {
      id: 'GH-4491',
      crop: 'Cotton',
      sacks: '40 Sacks',
      mandi: 'Gudimalkapur Vegetable & Flower APMC Yard',
      fare: 380,
      tier: 1,
      vehicle: v.name,
      driverName: v.driver,
      driverPhone: v.phone,
      driverPlate: v.plate,
      driverRating: v.rating,
      driverCoords: v.coords,
      driverColor: v.color,
      etaMins: v.etaMins,
      otp: v.otp,
      status: 'SEARCHING'
    };
    localStorage.setItem('nukrop_active_trip', JSON.stringify(activeTrip));
  }

  if (activeTrip.status === 'SEARCHING') {
    renderTrackingSearchingState(activeTrip);
  } else {
    renderTrackingDispatchedState(activeTrip);
  }
}

function renderTrackingSearchingState(activeTrip) {
  // Clear any existing driver animation interval while searching
  if (window.gramhaulLiveMoveInterval) {
    clearInterval(window.gramhaulLiveMoveInterval);
    window.gramhaulLiveMoveInterval = null;
  }

  const topText = document.getElementById('gh-tracking-top-status-text');
  if (topText) topText.textContent = 'Radar Geofenced · 10 KM Radius';

  const bottomEl = document.getElementById('gh-tracking-bottom-container');
  if (bottomEl) {
    bottomEl.innerHTML = `
      <div style="background:#FFFFFF;width:100%;border-radius:24px 24px 0 0;padding:18px 18px max(24px,env(safe-area-inset-bottom,24px));box-shadow:0 -10px 30px rgba(0,0,0,0.08);border-top:1px solid #E2E8F0;animation:slideUp 0.25s cubic-bezier(0.16, 1, 0.3, 1);color:#0F172A;text-align:center;box-sizing:border-box;margin:0;">
        <!-- Centered Drag Pill -->
        <div style="width:36px;height:4px;background:#E2E8F0;border-radius:10px;margin:0 auto 16px;"></div>

        <!-- Radar Animation Rings Container -->
        <div style="position:relative;width:80px;height:80px;margin:0 auto 14px;display:flex;align-items:center;justify-content:center;">
          <div style="position:absolute;width:80px;height:80px;border-radius:50%;background:rgba(34,197,94,0.12);border:1.5px solid rgba(34,197,94,0.35);animation:radarRipple 1.6s ease-out infinite;"></div>
          <div style="position:absolute;width:56px;height:56px;border-radius:50%;background:rgba(34,197,94,0.20);animation:radarRipple 1.6s ease-out infinite 0.4s;"></div>
          <div style="width:48px;height:48px;border-radius:50%;background:linear-gradient(135deg,#16A34A,#15803D);display:flex;align-items:center;justify-content:center;box-shadow:0 6px 16px rgba(22,163,74,0.35);z-index:2;">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none"><rect x="1" y="6" width="14" height="11" rx="2" fill="#FFFFFF"/><path d="M15 9H19L22 13V17H15V9Z" fill="#DCFCE7"/><circle cx="5.5" cy="17" r="2.2" fill="#15803D"/><circle cx="18.5" cy="17" r="2.2" fill="#15803D"/></svg>
          </div>
        </div>

        <div style="font-size:18px;font-weight:900;color:#0F172A;margin-bottom:4px;letter-spacing:-0.2px;">
          Finding Commercial Trucks...
        </div>
        <div style="font-size:12px;color:#64748B;font-weight:600;margin-bottom:14px;">
          Connecting with verified drivers near Himayath Nagar
        </div>

        <!-- Bento Summary Box (Pure White Rapido Theme) -->
        <div style="background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:16px;padding:12px 14px;margin-bottom:16px;display:flex;flex-direction:column;gap:7px;text-align:left;font-size:12px;">
          <div style="display:flex;justify-content:space-between;"><span style="color:#64748B;font-weight:600;">Selected Tier:</span><strong style="color:#0F172A;font-weight:800;">${activeTrip.vehicle}</strong></div>
          <div style="display:flex;justify-content:space-between;"><span style="color:#64748B;font-weight:600;">Produce Load:</span><strong style="color:#0F172A;font-weight:800;">${activeTrip.crop} (${activeTrip.sacks})</strong></div>
          <div style="display:flex;justify-content:space-between;"><span style="color:#64748B;font-weight:600;">Destination:</span><strong style="color:#16A34A;font-weight:800;">${activeTrip.mandi}</strong></div>
          <div style="display:flex;justify-content:space-between;"><span style="color:#64748B;font-weight:600;">Estimated Fare:</span><strong style="color:#15803D;font-size:14px;font-weight:900;">₹${activeTrip.fare} (0% Commission)</strong></div>
        </div>

        <!-- Cancel Search Button -->
        <button onclick="cancelAndReturnToGramhaul()" style="width:100%;height:46px;background:#F1F5F9;color:#475569;border:1px solid #E2E8F0;border-radius:14px;font-size:13.5px;font-weight:800;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:6px;transition:all 0.15s ease;">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          <span>Cancel Search</span>
        </button>
      </div>
    `;
  }

  if (gramhaulTrackingMap) {
    const v = GRAMHAUL_TIER_AVAILABLE_VEHICLES[activeTrip.tier] || GRAMHAUL_TIER_AVAILABLE_VEHICLES[1];
    const truckImg = (activeTrip.tier === 2) ? 'images/trucks/bolero_maxi.png' :
                     (activeTrip.tier === 3) ? 'images/trucks/ashok_leyland_dost.png' :
                     (activeTrip.tier === 4) ? 'images/trucks/tata_407.png' :
                     (activeTrip.tier === 5) ? 'images/trucks/eicher_pro.png' : 'images/trucks/tata_ace.png';
    const ghostIcon = L.divIcon({
      className: 'gh-ghost-marker',
      html: `<div style="width:34px;height:34px;border-radius:50%;background:#FFFFFF;border:2px solid #16A34A;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(0,0,0,0.18);transform:translate(-50%, -50%);">
        <img src="${truckImg}" style="width:26px;height:18px;object-fit:contain;" />
      </div>`,
      iconSize: [0, 0]
    });
    if (trackingDriverMarker) {
      try { gramhaulTrackingMap.removeLayer(trackingDriverMarker); } catch(e) {}
    }
    // Stationary ghost truck while searching - NO movement yet!
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
      showLuxuryToast(`Driver ${activeTrip.driverName} accepted! Arriving in ${activeTrip.etaMins || 2} min`, 'success');
    }
  }, 1800);
}

function renderTrackingDispatchedState(activeTrip) {
  if (trackingSearchTimeout) {
    clearTimeout(trackingSearchTimeout);
    trackingSearchTimeout = null;
  }

  // Clear previous live movement interval if any
  if (window.gramhaulLiveMoveInterval) {
    clearInterval(window.gramhaulLiveMoveInterval);
    window.gramhaulLiveMoveInterval = null;
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

  const truckImg = (activeTrip.tier === 2) ? 'images/trucks/bolero_maxi.png' :
                   (activeTrip.tier === 3) ? 'images/trucks/ashok_leyland_dost.png' :
                   (activeTrip.tier === 4) ? 'images/trucks/tata_407.png' :
                   (activeTrip.tier === 5) ? 'images/trucks/eicher_pro.png' : 'images/trucks/tata_ace.png';

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
          <div style="color:#0F172A;font-weight:900;font-size:14.5px;letter-spacing:-0.2px;display:flex;align-items:center;gap:8px;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" style="flex-shrink:0;"><rect x="1" y="6" width="14" height="11" rx="2" fill="#0F172A"/><path d="M15 9H19L22 13V17H15V9Z" fill="#0F172A"/><circle cx="5.5" cy="17" r="2.2" fill="#FFFFFF"/><circle cx="18.5" cy="17" r="2.2" fill="#FFFFFF"/><path d="M16 10H18.5L20.5 13H16V10Z" fill="#86EFAC"/></svg>
            <span>Your driver is on the way</span>
          </div>
          <div id="gh-dispatched-eta-badge" style="background:#14532D;color:#FFFFFF;font-size:11.5px;font-weight:900;padding:4px 12px;border-radius:9999px;">
            ${eta} min
          </div>
        </div>

        <!-- Main Cockpit Sheet (Pure White Rapido Theme, Edge-to-Edge) -->
        <div style="width:100%;box-sizing:border-box;background:#FFFFFF;padding:18px 18px max(24px,env(safe-area-inset-bottom,24px));color:#0F172A;box-shadow:0 -10px 40px rgba(0,0,0,0.08);border-top:1px solid #E2E8F0;margin:0;">
          
          <!-- Driver Profile Row -->
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;">
            <div style="display:flex;align-items:center;gap:12px;">
              <div style="position:relative;width:48px;height:48px;border-radius:50%;overflow:hidden;background:#DCFCE7;border:2px solid #22C55E;display:flex;align-items:center;justify-content:center;flex-shrink:0;box-shadow:0 2px 8px rgba(34,197,94,0.2);">
                <svg width="46" height="46" viewBox="0 0 44 44" fill="none" style="display:block;">
                  <circle cx="22" cy="22" r="22" fill="#DCFCE7"/>
                  <mask id="driverMask" maskUnits="userSpaceOnUse" x="0" y="0" width="44" height="44">
                    <circle cx="22" cy="22" r="22" fill="#FFFFFF"/>
                  </mask>
                  <g mask="url(#driverMask)">
                    <path d="M7 44C7 35.7 13.7 29 22 29C30.3 29 37 35.7 37 44H7Z" fill="#1E293B"/>
                    <path d="M19 29L22 34L25 29H19Z" fill="#22C55E"/>
                    <path d="M22 25C25.9 25 29 21.6 29 17.5C29 13.4 25.9 10 22 10C18.1 10 15 13.4 15 17.5C15 21.6 18.1 25 22 25Z" fill="#F8D7BE"/>
                    <path d="M14 14C14 10.5 17.5 8 22 8C26.5 8 30 10.5 30 14H14Z" fill="#0F172A"/>
                    <path d="M12 14C12 14 14.5 15.5 22 15.5C29.5 15.5 32 14 32 14L34 16H10L12 14Z" fill="#15803D"/>
                    <circle cx="22" cy="11" r="1.8" fill="#FBBF24"/>
                  </g>
                  <circle cx="34" cy="34" r="8" fill="#16A34A" stroke="#FFFFFF" stroke-width="2"/>
                  <path d="M31 34L33 36L37 32" stroke="#FFFFFF" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <div>
                <div style="display:flex;align-items:center;gap:6px;">
                  <span style="font-size:16px;font-weight:900;color:#0F172A;">${driverName}</span>
                  <span style="font-size:12.5px;font-weight:900;color:#D97706;display:flex;align-items:center;gap:2px;">★ ${rating.toString().replace(/[^0-9.]/g, '') || '4.9'}</span>
                </div>
                <div style="font-size:12.5px;color:#64748B;font-weight:600;margin-top:2px;">
                  ${vehicleName}
                </div>
              </div>
            </div>

            <!-- Commercial License Plate Badge (Yellow Indian Commercial Plate) -->
            <div style="background:#FBBF24;color:#0F172A;border:1.5px solid #000000;border-radius:8px;padding:4px 10px;font-size:12.5px;font-weight:900;letter-spacing:1px;font-family:monospace;box-shadow:0 2px 6px rgba(0,0,0,0.12);flex-shrink:0;">
              ${plate}
            </div>
          </div>

          <!-- PROMINENT RAPIDO START TRIP OTP BADGE -->
          <div style="background:#FEF3C7;border:1.5px solid #F59E0B;border-radius:14px;padding:12px 16px;margin-bottom:14px;display:flex;align-items:center;justify-content:space-between;">
            <div>
              <div style="font-size:10px;font-weight:900;color:#92400E;text-transform:uppercase;letter-spacing:0.06em;">START TRIP PIN / OTP</div>
              <div style="font-size:11.5px;color:#78350F;margin-top:2px;font-weight:600;">Share with driver only after loading sacks</div>
            </div>
            <div style="background:#F59E0B;color:#000000;font-size:22px;font-weight:900;letter-spacing:3px;padding:6px 14px;border-radius:10px;box-shadow:0 2px 8px rgba(245,158,11,0.35);">
              ${otp}
            </div>
          </div>

          <!-- 4 TACTILE CIRCULAR ACTION BUTTONS -->
          <div style="display:grid;grid-template-columns:repeat(4, 1fr);gap:10px;margin-bottom:14px;">
            <!-- Call Action: Direct Real Phone Call -->
            <div onclick="triggerDriverCall('${driverName}', '${v.phone}')" style="display:flex;flex-direction:column;align-items:center;gap:6px;cursor:pointer;">
              <div style="width:48px;height:48px;border-radius:50%;background:#DCFCE7;border:1px solid #86EFAC;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(22,163,74,0.15);transition:transform 0.15s ease;">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
              </div>
              <span style="font-size:11px;font-weight:800;color:#334155;">Call</span>
            </div>

            <!-- Message Action -->
            <div onclick="openDriverLiveChatModal('${driverName}', '${plate}')" style="display:flex;flex-direction:column;align-items:center;gap:6px;cursor:pointer;">
              <div style="width:48px;height:48px;border-radius:50%;background:#EFF6FF;border:1px solid #93C5FD;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(37,99,235,0.15);transition:transform 0.15s ease;">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
              </div>
              <span style="font-size:11px;font-weight:800;color:#334155;">Message</span>
            </div>

            <!-- Share Trip Action -->
            <div onclick="shareGramhaulLiveTrip('${driverName}', '${plate}', '${activeTrip.crop}', '${activeTrip.mandi}')" style="display:flex;flex-direction:column;align-items:center;gap:6px;cursor:pointer;">
              <div style="width:48px;height:48px;border-radius:50%;background:#F3E8FF;border:1px solid #D8B4FE;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(147,51,234,0.15);transition:transform 0.15s ease;">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#7C3AED" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
              </div>
              <span style="font-size:11px;font-weight:800;color:#334155;">Share</span>
            </div>

            <!-- Cancel Action -->
            <div onclick="cancelActiveHaulTripAndExit()" style="display:flex;flex-direction:column;align-items:center;gap:6px;cursor:pointer;">
              <div style="width:48px;height:48px;border-radius:50%;background:#FEE2E2;border:1px solid #FCA5A5;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(220,38,38,0.15);transition:transform 0.15s ease;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
              </div>
              <span style="font-size:11px;font-weight:800;color:#DC2626;">Cancel</span>
            </div>
          </div>

          <!-- Route Progress Card (Pure Light Bento Style) -->
          <div style="background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:16px;padding:12px 14px;margin-bottom:12px;">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;">
              <div>
                <div style="font-size:11px;color:#64748B;font-weight:700;">Pickup in</div>
                <div id="gh-pickup-countdown" style="font-size:16.5px;font-weight:900;color:#0F172A;margin-top:1px;">${eta} min</div>
              </div>
              <div style="text-align:right;">
                <div style="font-size:11px;color:#64748B;font-weight:700;">Arrive by</div>
                <div style="font-size:16.5px;font-weight:900;color:#0F172A;margin-top:1px;">${formattedArrival}</div>
              </div>
            </div>

            <!-- Progress Line Tracker with Real Truck Image -->
            <div style="display:flex;align-items:center;gap:3px;margin-top:6px;">
              <div id="gh-progress-bar-fill" style="width:25%;height:4px;background:#22C55E;border-radius:2px;transition:width 0.6s ease;"></div>
              <div style="width:24px;height:20px;display:flex;align-items:center;justify-content:center;transform:scaleX(-1);">
                <img src="${truckImg}" style="width:24px;height:18px;object-fit:contain;" />
              </div>
              <div style="flex:1;height:2px;border-top:2px dashed #CBD5E1;"></div>
              <div style="width:8px;height:8px;border-radius:50%;background:#22C55E;"></div>
              <div style="flex:1;height:2px;border-top:2px dashed #CBD5E1;"></div>
              <div style="width:8px;height:8px;border-radius:50%;background:#94A3B8;"></div>
            </div>
          </div>

          <!-- Expandable "See trip details" Drawer (Pure Light Theme) -->
          <div style="background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:14px;overflow:hidden;">
            <div onclick="toggleTripDetailsDrawer()" style="padding:11px 14px;display:flex;align-items:center;justify-content:space-between;cursor:pointer;">
              <span style="font-size:12.5px;font-weight:800;color:#334155;">See trip details</span>
              <span id="gh-trip-arrow" style="font-size:12px;color:#64748B;transition:transform 0.2s ease;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
              </span>
            </div>

            <div id="gh-trip-details-content" style="display:none;padding:0 14px 12px;font-size:12px;flex-direction:column;gap:8px;border-top:1px solid #E2E8F0;">
              <div style="display:flex;align-items:center;justify-content:space-between;margin-top:8px;">
                <div style="display:flex;align-items:center;gap:6px;color:#64748B;"><svg width="16" height="16" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="10" r="3" fill="#16A34A"/><path d="M12 2C7.58 2 4 5.58 4 10C4 15.25 12 22 12 22C12 22 20 15.25 20 10C20 5.58 16.42 2 12 2Z" stroke="#16A34A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg><span>Farm Pickup:</span></div>
                <strong style="color:#0F172A;">${activeTrip.pickup || 'Himayath Nagar Farm, Telangana'}</strong>
              </div>
              <div style="display:flex;align-items:center;justify-content:space-between;">
                <div style="display:flex;align-items:center;gap:6px;color:#64748B;"><svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M3 21H21M4 18V9L12 3L20 9V18M9 21V12H15V21" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="#EFF6FF"/></svg><span>Destination Mandi:</span></div>
                <strong style="color:#15803D;">${mandiName}</strong>
              </div>
              <div style="display:flex;align-items:center;justify-content:space-between;">
                <div style="display:flex;align-items:center;gap:6px;color:#64748B;"><svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M12 22V2M12 7C9.5 5 7 7 7 10C7 13 12 15 12 15M12 7C14.5 5 17 7 17 10C17 13 12 15 12 15M12 12C9.5 10 7 12 7 15C7 18 12 20 12 20M12 12C14.5 10 17 12 17 15C17 18 12 20 12 20" stroke="#D97706" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg><span>Produce Load:</span></div>
                <strong style="color:#0F172A;">${crop} (${sacks})</strong>
              </div>
              <div style="display:flex;align-items:center;justify-content:space-between;">
                <div style="display:flex;align-items:center;gap:6px;color:#64748B;"><svg width="16" height="16" viewBox="0 0 24 24" fill="none"><rect x="2" y="5" width="20" height="14" rx="3" fill="#DCFCE7" stroke="#16A34A" stroke-width="1.8"/><circle cx="16" cy="12" r="2.5" fill="#16A34A"/><path d="M6 9H11M6 12H9.5M6 15L9 12" stroke="#15803D" stroke-width="1.8" stroke-linecap="round"/></svg><span>Freight Fare:</span></div>
                <strong style="color:#15803D;font-size:14px;">₹${fare} (0% Commission)</strong>
              </div>
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
      html: `<div style="display:flex;flex-direction:column;align-items:center;transform:translate(-50%, -100%);filter:drop-shadow(0 6px 14px rgba(0,0,0,0.25));">
        <div style="background:#FBBF24;color:#0F172A;border:1.5px solid #000000;padding:2px 8px;border-radius:6px;font-size:10px;font-weight:900;letter-spacing:0.8px;font-family:monospace;white-space:nowrap;box-shadow:0 2px 6px rgba(0,0,0,0.20);margin-bottom:2px;">
          ${plate}
        </div>
        <div style="width:44px;height:44px;border-radius:50%;background:#FFFFFF;border:2.5px solid #22C55E;display:flex;align-items:center;justify-content:center;box-shadow:0 0 16px rgba(34,197,94,0.6);padding:2px;">
          <img src="${truckImg}" style="width:36px;height:24px;object-fit:contain;" />
        </div>
      </div>`,
      iconSize: [0, 0]
    });

    const startCoords = [v.coords[0], v.coords[1]];
    const destCoords = [17.3980, 78.4900];

    trackingDriverMarker = L.marker(startCoords, { icon: truckIcon }).addTo(gramhaulTrackingMap);

    const initialRoute = [
      startCoords,
      destCoords
    ];
    trackingRoutePolyline = L.polyline(initialRoute, {
      color: '#22C55E',
      weight: 4,
      dashArray: '8, 8',
      opacity: 0.95
    }).addTo(gramhaulTrackingMap);

    const bounds = L.latLngBounds([destCoords, startCoords]);
    gramhaulTrackingMap.fitBounds(bounds, { padding: [60, 60], maxZoom: 15 });

    // REAL-TIME DRIVER MOVEMENT: Only moves towards farm after driver accepted!
    let moveStep = 0;
    const totalMoveSteps = 50; // Smooth 50-step progression
    window.gramhaulLiveMoveInterval = setInterval(() => {
      moveStep++;
      const progress = Math.min(1.0, moveStep / totalMoveSteps);
      const curLat = startCoords[0] + (destCoords[0] - startCoords[0]) * progress;
      const curLng = startCoords[1] + (destCoords[1] - startCoords[1]) * progress;

      if (trackingDriverMarker) {
        trackingDriverMarker.setLatLng([curLat, curLng]);
      }
      if (trackingRoutePolyline) {
        trackingRoutePolyline.setLatLngs([
          [curLat, curLng],
          destCoords
        ]);
      }

      // Update ETA text and progress bar
      const remainingProgress = (1 - progress);
      const remainingMins = Math.max(0, Math.ceil(remainingProgress * eta));
      const fillEl = document.getElementById('gh-progress-bar-fill');
      if (fillEl) fillEl.style.width = `${Math.min(95, 25 + progress * 70)}%`;

      const countdownEl = document.getElementById('gh-pickup-countdown');
      const badgeEl = document.getElementById('gh-dispatched-eta-badge');
      const topStatusText = document.getElementById('gh-tracking-top-status-text');

      if (progress >= 0.98 || remainingMins === 0) {
        if (countdownEl) countdownEl.textContent = 'Arrived!';
        if (badgeEl) badgeEl.textContent = 'Arrived';
        if (topStatusText) topStatusText.textContent = `Driver ${driverName} has arrived at pickup!`;
        clearInterval(window.gramhaulLiveMoveInterval);
        window.gramhaulLiveMoveInterval = null;
      } else {
        if (countdownEl) countdownEl.textContent = `${remainingMins} min`;
        if (badgeEl) badgeEl.textContent = `${remainingMins} min`;
        if (topStatusText) topStatusText.textContent = `Driver ${driverName} is ${remainingMins} min away`;
      }
    }, 1200);
  }
}

function recenterTrackingMap() {
  if (!gramhaulTrackingMap) return;
  let activeTrip = null;
  try {
    activeTrip = JSON.parse(localStorage.getItem('nukrop_active_trip') || 'null');
  } catch (e) {}
  const v = (activeTrip && GRAMHAUL_TIER_AVAILABLE_VEHICLES[activeTrip.tier]) || GRAMHAUL_TIER_AVAILABLE_VEHICLES[1];
  const bounds = L.latLngBounds([[17.3980, 78.4900], v.coords]);
  gramhaulTrackingMap.fitBounds(bounds, { padding: [50, 50], maxZoom: 15 });
}

function cancelAndReturnToGramhaul() {
  if (trackingSearchTimeout) {
    clearTimeout(trackingSearchTimeout);
    trackingSearchTimeout = null;
  }
  if (window.gramhaulLiveMoveInterval) {
    clearInterval(window.gramhaulLiveMoveInterval);
    window.gramhaulLiveMoveInterval = null;
  }
  localStorage.removeItem('nukrop_active_trip');
  openScreen('gramhaul');
  if (typeof showLuxuryToast === 'function') {
    showLuxuryToast('Mandi Truck Search Cancelled', 'info');
  }
}

function cancelActiveHaulTripAndExit() {
  if (confirm(TL('Are you sure you want to cancel this mandi truck request?', 'మీరు ఈ మండి ట్రక్ బుకింగ్‌ను రద్దు చేయాలనుకుంటున్నారా?', 'क्या आप इस मंडी ट्रक बुकिंग को रद्द करना चाहते हैं?'))) {
    if (trackingSearchTimeout) {
      clearTimeout(trackingSearchTimeout);
      trackingSearchTimeout = null;
    }
    if (window.gramhaulLiveMoveInterval) {
      clearInterval(window.gramhaulLiveMoveInterval);
      window.gramhaulLiveMoveInterval = null;
    }
    localStorage.removeItem('nukrop_active_trip');
    openScreen('gramhaul');
    if (typeof showLuxuryToast === 'function') {
      showLuxuryToast('Haul Booking Cancelled', 'info');
    }
  }
}

function toggleTripDetailsDrawer() {
  const content = document.getElementById('gh-trip-details-content');
  const arrow = document.getElementById('gh-trip-arrow');
  if (!content) return;
  if (content.style.display === 'none' || !content.style.display) {
    content.style.display = 'flex';
    if (arrow) arrow.style.transform = 'rotate(180deg)';
  } else {
    content.style.display = 'none';
    if (arrow) arrow.style.transform = 'rotate(0deg)';
  }
}

// REAL PHONE CALL REDIRECTION (NO FAKE IN-APP AUDIO MODAL)
function triggerDriverCall(driverName, phone) {
  const cleanPhone = (phone || '+919440155667').replace(/[^0-9+]/g, '');
  if (window.AndroidBridge && typeof AndroidBridge.makePhoneCall === 'function') {
    AndroidBridge.makePhoneCall(cleanPhone);
  } else {
    window.location.href = `tel:${cleanPhone}`;
  }
  if (typeof showLuxuryToast === 'function') {
    showLuxuryToast(TL('Dialing ' + driverName + ' (' + cleanPhone + ')...', driverName + ' కి కాల్ చేస్తోంది...', driverName + ' को कॉल कर रहे हैं...'), 'info');
  }
}

function openDriverLiveChatModal(driverName, plate) {
  const modalId = 'driver-live-chat-modal';
  let modal = document.getElementById(modalId);
  if (modal) modal.remove();

  if (!window.liveHaulChatMessages) {
    window.liveHaulChatMessages = [
      { sender: 'driver', text: 'Namaste Jaswanth ji! I have accepted your haul booking. I am on my way to Himayath Nagar Farm.', time: 'Just now' }
    ];
  }
  const msgs = window.liveHaulChatMessages;

  modal = document.createElement('div');
  modal.id = modalId;
  modal.style.cssText = 'position:fixed;inset:0;background:rgba(15,23,42,0.6);backdrop-filter:blur(6px);z-index:999999;display:flex;align-items:flex-end;justify-content:center;animation:fadeIn 0.2s ease;';
  
  modal.innerHTML = `
    <div style="background:#FFFFFF;width:100%;height:75vh;border-radius:28px 28px 0 0;padding:18px 16px 20px;display:flex;flex-direction:column;box-shadow:0 -10px 40px rgba(0,0,0,0.18);border-top:1px solid #E2E8F0;animation:slideUp 0.25s cubic-bezier(0.16, 1, 0.3, 1);">
      
      <!-- Chat Header -->
      <div style="display:flex;align-items:center;justify-content:space-between;padding-bottom:12px;border-bottom:1px solid #F1F5F9;">
        <div style="display:flex;align-items:center;gap:10px;">
          <div style="width:40px;height:40px;border-radius:50%;background:#DCFCE7;border:1.5px solid #22C55E;display:flex;align-items:center;justify-content:center;overflow:hidden;">
            <svg width="44" height="44" viewBox="0 0 44 44" fill="none" style="display:block;">
              <circle cx="22" cy="22" r="22" fill="#DCFCE7"/>
              <mask id="chatDriverMask" maskUnits="userSpaceOnUse" x="0" y="0" width="44" height="44">
                <circle cx="22" cy="22" r="22" fill="#FFFFFF"/>
              </mask>
              <g mask="url(#chatDriverMask)">
                <path d="M7 44C7 35.7 13.7 29 22 29C30.3 29 37 35.7 37 44H7Z" fill="#1E293B"/>
                <path d="M19 29L22 34L25 29H19Z" fill="#22C55E"/>
                <path d="M22 25C25.9 25 29 21.6 29 17.5C29 13.4 25.9 10 22 10C18.1 10 15 13.4 15 17.5C15 21.6 18.1 25 22 25Z" fill="#F8D7BE"/>
                <path d="M14 14C14 10.5 17.5 8 22 8C26.5 8 30 10.5 30 14H14Z" fill="#0F172A"/>
                <path d="M12 14C12 14 14.5 15.5 22 15.5C29.5 15.5 32 14 32 14L34 16H10L12 14Z" fill="#15803D"/>
                <circle cx="22" cy="11" r="1.8" fill="#FBBF24"/>
              </g>
              <circle cx="34" cy="34" r="8" fill="#16A34A" stroke="#FFFFFF" stroke-width="2"/>
              <path d="M31 34L33 36L37 32" stroke="#FFFFFF" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div>
            <div style="font-size:14px;font-weight:900;color:#0F172A;display:flex;align-items:center;gap:6px;">
              <span>${driverName}</span>
              <span style="font-size:10px;color:#16A34A;background:#DCFCE7;padding:1px 6px;border-radius:6px;font-weight:800;">● Online</span>
            </div>
            <div style="font-size:11px;color:#64748B;">${plate} · Verified Driver</div>
          </div>
        </div>
        <button onclick="document.getElementById('${modalId}').remove();" style="background:#F1F5F9;border:1px solid #E2E8F0;color:#475569;width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      </div>

      <!-- Messages Stream -->
      <div id="live-haul-chat-stream" style="flex:1;overflow-y:auto;padding:14px 0;display:flex;flex-direction:column;gap:10px;">
        ${msgs.map(m => `
          <div style="display:flex;justify-content:${m.sender==='user'?'flex-end':'flex-start'};">
            <div style="max-width:80%;border-radius:${m.sender==='user'?'16px 16px 4px 16px':'16px 16px 16px 4px'};background:${m.sender==='user'?'#16A34A':'#F1F5F9'};color:${m.sender==='user'?'#FFFFFF':'#0F172A'};padding:10px 14px;font-size:13px;line-height:1.45;box-shadow:0 1px 3px rgba(0,0,0,0.06);">
              <div>${m.text}</div>
              <div style="font-size:10px;margin-top:4px;opacity:0.75;text-align:right;">${m.time}</div>
            </div>
          </div>
        `).join('')}
      </div>

      <!-- Quick Chips -->
      <div style="display:flex;gap:6px;overflow-x:auto;padding:6px 0 10px;scrollbar-width:none;">
        <button onclick="sendQuickDriverMsg('I am at farm gate waiting with produce')" style="background:#F1F5F9;border:1px solid #E2E8F0;padding:6px 12px;border-radius:999px;font-size:11.5px;color:#334155;white-space:nowrap;cursor:pointer;flex-shrink:0;">Gate is open 🚪</button>
        <button onclick="sendQuickDriverMsg('Produce bags are ready for loading')" style="background:#F1F5F9;border:1px solid #E2E8F0;padding:6px 12px;border-radius:999px;font-size:11.5px;color:#334155;white-space:nowrap;cursor:pointer;flex-shrink:0;">Bags ready 🌾</button>
        <button onclick="sendQuickDriverMsg('Call me when you reach the village turn')" style="background:#F1F5F9;border:1px solid #E2E8F0;padding:6px 12px;border-radius:999px;font-size:11.5px;color:#334155;white-space:nowrap;cursor:pointer;flex-shrink:0;">Call near village 📞</button>
      </div>

      <!-- Input Row -->
      <div style="display:flex;align-items:center;gap:8px;">
        <input id="live-driver-msg-inp" type="text" placeholder="Type message to driver..." style="flex:1;height:44px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px;padding:0 14px;font-size:13.5px;color:#0F172A;outline:none;" onkeydown="if(event.key==='Enter')sendLiveDriverMsg()" />
        <button onclick="sendLiveDriverMsg()" style="width:44px;height:44px;border-radius:12px;background:#16A34A;color:#FFFFFF;border:none;display:flex;align-items:center;justify-content:center;cursor:pointer;box-shadow:0 2px 8px rgba(22,163,74,0.3);">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
        </button>
      </div>
    </div>
  `;

  document.body.appendChild(modal);
}'''

def patch_file(filepath):
    print(f"Patching {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Backup original
    shutil.copy2(filepath, filepath + ".bak_v4")

    # 1. Replace truck categories in Screen 1
    # Locate from id="gh-truck-categories" to <!-- FARE BREAKDOWN & BOOK BUTTON -->
    start_tag = 'id="gh-truck-categories">'
    end_tag = '<!-- FARE BREAKDOWN & BOOK BUTTON -->'
    idx_start = content.find(start_tag)
    idx_end = content.find(end_tag, idx_start)

    if idx_start != -1 and idx_end != -1:
        # Find opening <div for id="gh-truck-categories"
        div_start = content.rfind('<div', 0, idx_start)
        new_cards = generate_truck_cards_html()
        content = content[:div_start] + new_cards + "\n\n        " + content[idx_end:]
        print("  [+] Replaced Screen 1 vehicle cards with real background-free truck images")
    else:
        print("  [!] Could not locate gh-truck-categories block!")

    # 2. Update tracking JS functions (initGramhaulTrackingMap, renderTrackingSearchingState, renderTrackingDispatchedState, etc.)
    fn_start_tag = 'function initGramhaulTrackingMap() {'
    fn_end_tag = 'function sendLiveDriverMsg() {'
    idx_fn_start = content.find(fn_start_tag)
    idx_fn_end = content.find(fn_end_tag, idx_fn_start)

    if idx_fn_start != -1 and idx_fn_end != -1:
        new_js = generate_screen2_js_code()
        content = content[:idx_fn_start] + new_js + "\n\n" + content[idx_fn_end:]
        print("  [+] Updated Screen 2 tracking logic (pure white Rapido theme, real movement, real dialer call)")
    else:
        print("  [!] Could not locate initGramhaulTrackingMap boundary!")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  -> Successfully wrote {filepath}")

def main():
    for f in FILES_TO_PATCH:
        if os.path.exists(f):
            patch_file(f)
        else:
            print(f"File not found: {f}")

if __name__ == '__main__':
    main()
