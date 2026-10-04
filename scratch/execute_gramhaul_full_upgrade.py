import sys
import os

with open(r'c:\Users\bjasw\Downloads\agriculture-ai-os\scratch\gramhaul_views_upgrade.py', 'r', encoding='utf-8') as f:
    views_code = f.read()

# Extract ACE_GOLD_SVG, BOLERO_MAXI_SVG, etc.
exec(views_code)

gramhaul_view_str = build_gramhaul_view()
gramhaul_tracking_view_str = build_gramhaul_tracking_view()

# Build the tracking functions replacement block
new_tracking_functions = '''function updateGramhaulSelectorMapVehicles(tier) {
  if (!gramhaulSelectorMap) return;
  if (gramhaulSelectorVehicleMarker) {
    try {
      gramhaulSelectorMap.removeLayer(gramhaulSelectorVehicleMarker);
    } catch(e) {}
    gramhaulSelectorVehicleMarker = null;
  }

  const v = GRAMHAUL_TIER_AVAILABLE_VEHICLES[tier] || GRAMHAUL_TIER_AVAILABLE_VEHICLES[1];
  const truckIcon = L.divIcon({
    className: 'gh-truck-marker',
    html: `<div style="display:flex;flex-direction:column;align-items:center;transform:translate(-50%, -100%);">
      <div style="background:#0F172A;color:#FFFFFF;border:1.5px solid ${v.color};padding:3px 8px;border-radius:8px;font-size:9.5px;font-weight:900;white-space:nowrap;box-shadow:0 4px 12px rgba(0,0,0,0.3);display:flex;align-items:center;gap:4px;">
        <span style="width:6px;height:6px;border-radius:50%;background:#22C55E;box-shadow:0 0 6px #22C55E;"></span>
        <span>${v.plate} · ${v.dist}</span>
      </div>
      <div style="width:38px;height:38px;border-radius:50%;background:#FFFFFF;border:2.5px solid ${v.color};display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(0,0,0,0.25);margin-top:2px;">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none"><rect x="1" y="6" width="14" height="11" rx="2" fill="${v.color}"/><path d="M15 9H19L22 13V17H15V9Z" fill="${v.color}"/><circle cx="5.5" cy="17" r="2.2" fill="#0F172A"/><circle cx="18.5" cy="17" r="2.2" fill="#0F172A"/><path d="M16 10H18.5L20.5 13H16V10Z" fill="#BAE6FD"/></svg>
      </div>
    </div>`,
    iconSize: [0, 0]
  });

  gramhaulSelectorVehicleMarker = L.marker(v.coords, { icon: truckIcon }).addTo(gramhaulSelectorMap);

  const bounds = L.latLngBounds([[17.3980, 78.4900], v.coords]);
  gramhaulSelectorMap.fitBounds(bounds, { padding: [40, 40], maxZoom: 15 });
}'''

new_searching_state_fn = '''function renderTrackingSearchingState(activeTrip) {
  const topText = document.getElementById('gh-tracking-top-status-text');
  if (topText) topText.textContent = 'Radar Geofenced · 10 KM Radius';

  const bottomEl = document.getElementById('gh-tracking-bottom-container');
  if (bottomEl) {
    bottomEl.innerHTML = `
      <div style="background:#FFFFFF;width:100%;border-radius:24px 24px 0 0;padding:20px 18px max(28px,env(safe-area-inset-bottom,28px));box-shadow:0 -10px 40px rgba(0,0,0,0.12);border-top:1px solid #E2E8F0;animation:slideUp 0.25s cubic-bezier(0.16, 1, 0.3, 1);color:#0F172A;text-align:center;box-sizing:border-box;margin:0;">
        <div style="width:38px;height:4px;background:#CBD5E1;border-radius:10px;margin:0 auto 16px;"></div>

        <!-- Radar Animation Rings Container -->
        <div style="position:relative;width:80px;height:80px;margin:0 auto 14px;display:flex;align-items:center;justify-content:center;">
          <div style="position:absolute;width:80px;height:80px;border-radius:50%;background:rgba(34,197,94,0.15);border:1.5px solid rgba(34,197,94,0.4);animation:radarRipple 1.6s ease-out infinite;"></div>
          <div style="position:absolute;width:56px;height:56px;border-radius:50%;background:rgba(34,197,94,0.25);animation:radarRipple 1.6s ease-out infinite 0.4s;"></div>
          <div style="width:50px;height:50px;border-radius:50%;background:linear-gradient(135deg,#22C55E,#16A34A);display:flex;align-items:center;justify-content:center;box-shadow:0 4px 16px rgba(34,197,94,0.4);z-index:2;">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none">
              <rect x="1" y="6" width="14" height="11" rx="2" fill="#FFFFFF"/>
              <path d="M15 9H19L22 13V17H15V9Z" fill="#F1F5F9"/>
              <circle cx="5.5" cy="17" r="2.2" fill="#0F172A"/>
              <circle cx="18.5" cy="17" r="2.2" fill="#0F172A"/>
              <path d="M16 10H18.5L20.5 13H16V10Z" fill="#38BDF8"/>
            </svg>
          </div>
        </div>

        <div style="font-size:18px;font-weight:900;color:#0F172A;margin-bottom:4px;letter-spacing:-0.2px;">
          Finding Commercial Trucks...
        </div>
        <div style="font-size:12.5px;color:#64748B;font-weight:600;margin-bottom:16px;">
          Connecting with verified drivers near Himayath Nagar
        </div>

        <div style="background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:16px;padding:12px 14px;margin-bottom:16px;display:flex;flex-direction:column;gap:7px;text-align:left;font-size:12.5px;">
          <div style="display:flex;justify-content:space-between;"><span style="color:#64748B;font-weight:600;">Selected Tier:</span><strong style="color:#0F172A;font-weight:800;">${activeTrip.vehicle}</strong></div>
          <div style="display:flex;justify-content:space-between;"><span style="color:#64748B;font-weight:600;">Produce Load:</span><strong style="color:#0F172A;font-weight:800;">${activeTrip.crop} (${activeTrip.sacks})</strong></div>
          <div style="display:flex;justify-content:space-between;"><span style="color:#64748B;font-weight:600;">Destination:</span><strong style="color:#16A34A;font-weight:800;">${activeTrip.mandi}</strong></div>
          <div style="display:flex;justify-content:space-between;"><span style="color:#64748B;font-weight:600;">Estimated Fare:</span><strong style="color:#16A34A;font-size:14.5px;font-weight:900;">₹${activeTrip.fare} (0% Commission)</strong></div>
        </div>

        <button onclick="cancelAndReturnToGramhaul()" style="width:100%;height:48px;background:#F1F5F9;color:#334155;border:1px solid #E2E8F0;border-radius:14px;font-size:14px;font-weight:800;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:6px;transition:background 0.15s ease;">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2.5" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          <span>Cancel Search</span>
        </button>
      </div>
    `;
  }

  if (gramhaulTrackingMap) {
    const v = GRAMHAUL_TIER_AVAILABLE_VEHICLES[activeTrip.tier] || GRAMHAUL_TIER_AVAILABLE_VEHICLES[1];
    const ghostIcon = L.divIcon({
      className: 'gh-ghost-marker',
      html: `<div style="width:34px;height:34px;border-radius:50%;background:#0F172A;border:2px solid #22C55E;display:flex;align-items:center;justify-content:center;box-shadow:0 0 14px rgba(34,197,94,0.6);transform:translate(-50%, -50%);">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><rect x="1" y="6" width="14" height="11" rx="2" fill="#22C55E"/><path d="M15 9H19L22 13V17H15V9Z" fill="#16A34A"/><circle cx="5.5" cy="17" r="2.2" fill="#FFFFFF"/><circle cx="18.5" cy="17" r="2.2" fill="#FFFFFF"/></svg>
      </div>`,
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
}'''

new_dispatched_state_fn = '''function renderTrackingDispatchedState(activeTrip) {
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
        <div style="width:100%;box-sizing:border-box;background:#22C55E;border-radius:24px 24px 0 0;padding:12px 18px 11px;display:flex;align-items:center;justify-content:space-between;box-shadow:0 -4px 14px rgba(34,197,94,0.25);margin:0;">
          <div style="color:#0F172A;font-weight:900;font-size:14.5px;letter-spacing:-0.2px;display:flex;align-items:center;gap:8px;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none"><rect x="1" y="6" width="14" height="11" rx="2" fill="#0F172A"/><path d="M15 9H19L22 13V17H15V9Z" fill="#0F172A"/><circle cx="5.5" cy="17" r="2.2" fill="#FFFFFF"/><circle cx="18.5" cy="17" r="2.2" fill="#FFFFFF"/><path d="M16 10H18.5L20.5 13H16V10Z" fill="#86EFAC"/></svg>
            <span>Your driver is on the way</span>
          </div>
          <div style="background:#0F172A;color:#FFFFFF;font-size:11.5px;font-weight:900;padding:4px 12px;border-radius:9999px;">
            ${eta} min
          </div>
        </div>

        <!-- Main Clean White Bento Cockpit Card (Edge-to-Edge, NO SIDE GAPS) -->
        <div style="width:100%;box-sizing:border-box;background:#FFFFFF;padding:18px 18px max(28px,env(safe-area-inset-bottom,28px));color:#0F172A;box-shadow:0 -10px 40px rgba(0,0,0,0.12);border-top:1px solid #F1F5F9;margin:0;">
          
          <!-- Driver Profile Row -->
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;">
            <div style="display:flex;align-items:center;gap:12px;">
              <div style="position:relative;width:50px;height:50px;border-radius:50%;overflow:hidden;background:#F0FDF4;border:2px solid #22C55E;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                <svg width="50" height="50" viewBox="0 0 64 64" fill="none">
                  <circle cx="32" cy="32" r="30" fill="#F0FDF4"/>
                  <!-- Uniform Cap -->
                  <path d="M18 25 C18 16 46 16 46 25 Z" fill="#1E293B"/>
                  <path d="M15 25 H49 L53 27 H11 Z" fill="#0F172A"/>
                  <!-- Face -->
                  <circle cx="32" cy="34" r="11" fill="#FDBA74"/>
                  <!-- Eyes & Mustache -->
                  <circle cx="28" cy="32" r="1.5" fill="#0F172A"/>
                  <circle cx="36" cy="32" r="1.5" fill="#0F172A"/>
                  <path d="M26 38 Q32 41 38 38" stroke="#451A03" stroke-width="2" fill="none" stroke-linecap="round"/>
                  <!-- Shoulders & Uniform -->
                  <path d="M16 54 C16 44 48 44 48 54 Z" fill="#15803D"/>
                  <path d="M28 44 L32 50 L36 44 Z" fill="#FFFFFF"/>
                  <!-- Verified Badge -->
                  <circle cx="48" cy="46" r="6" fill="#22C55E" stroke="#FFFFFF" stroke-width="1.5"/>
                  <path d="M46 46 L47.5 47.5 L50.5 44.5" stroke="#FFFFFF" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
              </div>
              <div>
                <div style="display:flex;align-items:center;gap:6px;">
                  <span style="font-size:16.5px;font-weight:900;color:#0F172A;">${driverName}</span>
                  <span style="font-size:12.5px;font-weight:900;color:#D97706;display:flex;align-items:center;gap:2px;">★ ${rating.toString().replace(/[^0-9.]/g, '') || '4.9'}</span>
                </div>
                <div style="font-size:12.5px;color:#64748B;font-weight:600;margin-top:2px;">
                  ${vehicleName}
                </div>
              </div>
            </div>

            <!-- Commercial License Plate Badge (Yellow Indian Commercial Plate) -->
            <div style="background:#FBBF24;color:#000000;border:1.5px solid #000000;border-radius:8px;padding:5px 11px;font-size:13px;font-weight:900;letter-spacing:1px;font-family:monospace;box-shadow:0 2px 6px rgba(0,0,0,0.15);flex-shrink:0;">
              ${plate}
            </div>
          </div>

          <!-- PROMINENT RAPIDO START TRIP OTP BADGE -->
          <div style="background:#FEF3C7;border:1.5px solid #F59E0B;border-radius:14px;padding:12px 16px;margin-bottom:16px;display:flex;align-items:center;justify-content:space-between;">
            <div>
              <div style="font-size:10.5px;font-weight:900;color:#92400E;text-transform:uppercase;letter-spacing:0.06em;display:flex;align-items:center;gap:4px;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#92400E" stroke-width="2.5" stroke-linecap="round"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                <span>START TRIP PIN / OTP</span>
              </div>
              <div style="font-size:11.5px;color:#78350F;margin-top:2px;font-weight:600;">Share with driver only after loading sacks</div>
            </div>
            <div style="background:#F59E0B;color:#000000;font-size:22px;font-weight:900;letter-spacing:3px;padding:6px 14px;border-radius:10px;box-shadow:0 2px 8px rgba(245,158,11,0.3);">
              ${otp}
            </div>
          </div>

          <!-- 4 Tactile Circular Action Buttons -->
          <div style="display:flex;align-items:center;justify-content:space-between;padding:0 8px;margin-bottom:16px;">
            
            <!-- Call Action -->
            <div onclick="triggerDriverCall('${driverName}', '${v.phone}')" style="display:flex;flex-direction:column;align-items:center;gap:6px;cursor:pointer;">
              <div style="width:48px;height:48px;border-radius:50%;background:#DCFCE7;border:1.5px solid #86EFAC;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(22,163,74,0.18);">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#15803D" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
              </div>
              <span style="font-size:11.5px;color:#15803D;font-weight:800;">Call</span>
            </div>

            <!-- Message Action -->
            <div onclick="openDriverLiveChatModal('${driverName}', '${plate}')" style="display:flex;flex-direction:column;align-items:center;gap:6px;cursor:pointer;">
              <div style="width:48px;height:48px;border-radius:50%;background:#EFF6FF;border:1.5px solid #93C5FD;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(37,99,235,0.15);">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
              </div>
              <span style="font-size:11.5px;color:#2563EB;font-weight:800;">Message</span>
            </div>

            <!-- Share Action -->
            <div onclick="shareLiveHaulTrip('${activeTrip.id || 'GH-4491'}')" style="display:flex;flex-direction:column;align-items:center;gap:6px;cursor:pointer;">
              <div style="width:48px;height:48px;border-radius:50%;background:#F8FAFC;border:1.5px solid #CBD5E1;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(15,23,42,0.08);">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#334155" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
              </div>
              <span style="font-size:11.5px;color:#475569;font-weight:800;">Share</span>
            </div>

            <!-- Cancel Action -->
            <div onclick="cancelActiveHaulTripAndExit()" style="display:flex;flex-direction:column;align-items:center;gap:6px;cursor:pointer;">
              <div style="width:48px;height:48px;border-radius:50%;background:#FEE2E2;border:1.5px solid #FCA5A5;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(239,68,68,0.18);">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
              </div>
              <span style="font-size:11.5px;color:#DC2626;font-weight:800;">Cancel</span>
            </div>

          </div>

          <!-- Route Progress Card -->
          <div style="background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:18px;padding:14px 16px;margin-bottom:14px;">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">
              <div>
                <div style="font-size:11px;color:#64748B;font-weight:700;">Pickup in</div>
                <div style="font-size:18px;font-weight:900;color:#0F172A;margin-top:2px;">${eta} min</div>
              </div>
              <div style="text-align:right;">
                <div style="font-size:11px;color:#64748B;font-weight:700;">Arrive by</div>
                <div style="font-size:18px;font-weight:900;color:#0F172A;margin-top:2px;">${formattedArrival}</div>
              </div>
            </div>

            <!-- Animated Progress Line Tracker with Moving Vector Truck -->
            <div style="display:flex;align-items:center;gap:4px;margin-top:8px;">
              <div style="width:28%;height:4px;background:#22C55E;border-radius:2px;"></div>
              <div style="width:20px;height:20px;animation:truckDrive 2s ease-in-out infinite;transform:scaleX(-1);display:flex;align-items:center;justify-content:center;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><rect x="1" y="6" width="14" height="11" rx="2" fill="#16A34A"/><path d="M15 9H19L22 13V17H15V9Z" fill="#15803D"/><circle cx="5.5" cy="17" r="2.2" fill="#0F172A"/><circle cx="18.5" cy="17" r="2.2" fill="#0F172A"/></svg>
              </div>
              <div style="flex:1;height:2px;border-top:2px dashed #CBD5E1;"></div>
              <div style="width:8px;height:8px;border-radius:50%;background:#22C55E;"></div>
              <div style="flex:1;height:2px;border-top:2px dashed #CBD5E1;"></div>
              <div style="width:8px;height:8px;border-radius:50%;background:#94A3B8;"></div>
            </div>
          </div>

          <!-- Expandable "See trip details" Drawer -->
          <div style="background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:14px;overflow:hidden;">
            <div onclick="toggleTripDetailsDrawer()" style="padding:12px 14px;display:flex;align-items:center;justify-content:space-between;cursor:pointer;">
              <span style="font-size:13px;font-weight:800;color:#0F172A;">See trip details</span>
              <span id="gh-trip-arrow" style="font-size:13px;color:#64748B;transition:transform 0.2s ease;">▾</span>
            </div>

            <div id="gh-trip-details-content" style="display:none;padding:0 14px 14px;font-size:12px;flex-direction:column;gap:10px;border-top:1px solid #E2E8F0;">
              <div style="display:flex;align-items:center;justify-content:space-between;margin-top:10px;">
                <div style="display:flex;align-items:center;gap:6px;color:#64748B;">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2.5" stroke-linecap="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                  <span>Farm Pickup:</span>
                </div>
                <strong style="color:#0F172A;">${activeTrip.pickup || 'Himayath Nagar Farm, Telangana'}</strong>
              </div>
              <div style="display:flex;align-items:center;justify-content:space-between;">
                <div style="display:flex;align-items:center;gap:6px;color:#64748B;">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2.2" stroke-linecap="round"><path d="M3 21h18M3 7v14M21 7v14M6 11h2M6 15h2M16 11h2M16 15h2M12 21V3l9 4M3 7l9-4"/></svg>
                  <span>Destination Mandi:</span>
                </div>
                <strong style="color:#16A34A;">${mandiName}</strong>
              </div>
              <div style="display:flex;align-items:center;justify-content:space-between;">
                <div style="display:flex;align-items:center;gap:6px;color:#64748B;">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#CA8A04" stroke-width="2.2" stroke-linecap="round"><path d="M12 22V12M12 12C12 7 7 4 2 5C2 10 5 14 12 12ZM12 12C12 7 17 4 22 5C22 10 19 14 12 12Z"/></svg>
                  <span>Produce Load:</span>
                </div>
                <strong style="color:#0F172A;">${crop} (${sacks})</strong>
              </div>
              <div style="display:flex;align-items:center;justify-content:space-between;">
                <div style="display:flex;align-items:center;gap:6px;color:#64748B;">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2.2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8M12 18V6"/></svg>
                  <span>Freight Fare:</span>
                </div>
                <strong style="color:#16A34A;font-size:14px;font-weight:900;">₹${fare} (0% Commission)</strong>
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
      html: `<div style="display:flex;flex-direction:column;align-items:center;transform:translate(-50%, -100%);">
        <div style="background:#0F172A;color:#FFFFFF;border:1.5px solid #22C55E;padding:2px 7px;border-radius:6px;font-size:9.5px;font-weight:900;white-space:nowrap;box-shadow:0 3px 10px rgba(0,0,0,0.3);letter-spacing:0.5px;">${plate}</div>
        <div style="width:40px;height:40px;border-radius:50%;background:#FFFFFF;border:2.5px solid #22C55E;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 12px rgba(34,197,94,0.45);margin-top:2px;">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <rect x="1" y="6" width="14" height="11" rx="2" fill="#16A34A"/>
            <path d="M15 9H19L22 13V17H15V9Z" fill="#15803D"/>
            <circle cx="5.5" cy="17" r="2.2" fill="#0F172A"/>
            <circle cx="18.5" cy="17" r="2.2" fill="#0F172A"/>
            <path d="M16 10H18.5L20.5 13H16V10Z" fill="#BAE6FD"/>
          </svg>
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
}'''

# Header icon in openGramhaulCropSelectorModal
old_crop_modal_header = '<div style="width:38px;height:38px;border-radius:12px;background:#DCFCE7;display:flex;align-items:center;justify-content:center;font-size:20px;">🌾</div>'
new_crop_modal_header = '''<div style="width:38px;height:38px;border-radius:12px;background:linear-gradient(135deg,#DCFCE7,#BBF7D0);display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(22,163,74,0.15);">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M12 22V12M12 12C12 7 7 4 2 5C2 10 5 14 12 12ZM12 12C12 7 17 4 22 5C22 10 19 14 12 12Z" stroke="#15803D" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </div>'''

def process_file(filepath):
    print(f"Upgrading {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Replace APP_VIEWS.gramhaul
    start_gh = text.find('/* ── 2. GRAMHAUL LOGISTICS: 38% VISIBLE MAP')
    if start_gh == -1:
        start_gh = text.find('gramhaul: () => {')
    end_gh = text.find('/* ── RAPIDO FULLSCREEN LIVE TRACKING VIEW ── */')
    if end_gh == -1:
        end_gh = text.find('gramhaul_tracking: () => {')

    if start_gh != -1 and end_gh != -1:
        print(f"Replacing gramhaul view in range [{start_gh}:{end_gh}]...")
        text = text[:start_gh] + gramhaul_view_str + text[end_gh:]
    else:
        print("Error: Could not locate gramhaul view range!")

    # 2. Replace APP_VIEWS.gramhaul_tracking
    start_ght = text.find('/* ── RAPIDO FULLSCREEN LIVE TRACKING VIEW ── */')
    end_ght = text.find('agristack: () => {')
    if start_ght != -1 and end_ght != -1:
        print(f"Replacing gramhaul_tracking view in range [{start_ght}:{end_ght}]...")
        text = text[:start_ght] + gramhaul_tracking_view_str + text[end_ght:]
    else:
        print("Error: Could not locate gramhaul_tracking view range!")

    # 3. Replace updateGramhaulSelectorMapVehicles
    start_v = text.find('function updateGramhaulSelectorMapVehicles(tier) {')
    end_v = text.find('function selectGramhaulTruckTier(tier) {')
    if start_v != -1 and end_v != -1:
        print("Replacing updateGramhaulSelectorMapVehicles...")
        text = text[:start_v] + new_tracking_functions + "\n\n" + text[end_v:]
    else:
        print("Error: Could not locate updateGramhaulSelectorMapVehicles!")

    # 4. Replace renderTrackingSearchingState
    start_srch = text.find('function renderTrackingSearchingState(activeTrip) {')
    end_srch = text.find('function renderTrackingDispatchedState(activeTrip) {')
    if start_srch != -1 and end_srch != -1:
        print("Replacing renderTrackingSearchingState...")
        text = text[:start_srch] + new_searching_state_fn + "\n\n" + text[end_srch:]
    else:
        print("Error: Could not locate renderTrackingSearchingState!")

    # 5. Replace renderTrackingDispatchedState
    start_disp = text.find('function renderTrackingDispatchedState(activeTrip) {')
    end_disp = text.find('function recenterTrackingMap() {')
    if start_disp != -1 and end_disp != -1:
        print("Replacing renderTrackingDispatchedState...")
        text = text[:start_disp] + new_dispatched_state_fn + "\n\n" + text[end_disp:]
    else:
        print("Error: Could not locate renderTrackingDispatchedState!")

    # 6. Replace old crop modal header
    if old_crop_modal_header in text:
        text = text.replace(old_crop_modal_header, new_crop_modal_header)
        print("Replaced crop modal header icon with colored SVG!")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"Finished upgrading {filepath}!")

process_file(r'c:\Users\bjasw\Downloads\agriculture-ai-os\app\src\main\assets\index.html')
process_file(r'c:\Users\bjasw\Downloads\agriculture-ai-os\nukrop_emulator.html')
print("All files upgraded successfully!")
