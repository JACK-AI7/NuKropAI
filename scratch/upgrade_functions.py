import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

SVG_DRIVER_AVATAR = '''<svg width="46" height="46" viewBox="0 0 44 44" fill="none" style="display:block;">
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
</svg>'''

SVG_DRIVER_AVATAR_LARGE = '''<svg width="78" height="78" viewBox="0 0 44 44" fill="none" style="display:block;">
  <circle cx="22" cy="22" r="22" fill="#DCFCE7"/>
  <mask id="driverMaskLg" maskUnits="userSpaceOnUse" x="0" y="0" width="44" height="44">
    <circle cx="22" cy="22" r="22" fill="#FFFFFF"/>
  </mask>
  <g mask="url(#driverMaskLg)">
    <path d="M7 44C7 35.7 13.7 29 22 29C30.3 29 37 35.7 37 44H7Z" fill="#1E293B"/>
    <path d="M19 29L22 34L25 29H19Z" fill="#22C55E"/>
    <path d="M22 25C25.9 25 29 21.6 29 17.5C29 13.4 25.9 10 22 10C18.1 10 15 13.4 15 17.5C15 21.6 18.1 25 22 25Z" fill="#F8D7BE"/>
    <path d="M14 14C14 10.5 17.5 8 22 8C26.5 8 30 10.5 30 14H14Z" fill="#0F172A"/>
    <path d="M12 14C12 14 14.5 15.5 22 15.5C29.5 15.5 32 14 32 14L34 16H10L12 14Z" fill="#15803D"/>
    <circle cx="22" cy="11" r="1.8" fill="#FBBF24"/>
  </g>
  <circle cx="34" cy="34" r="8" fill="#16A34A" stroke="#FFFFFF" stroke-width="2"/>
  <path d="M31 34L33 36L37 32" stroke="#FFFFFF" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
</svg>'''

SVG_RADAR_TRUCK = '''<svg width="28" height="28" viewBox="0 0 28 28" fill="none" style="display:block;">
  <rect x="2" y="8" width="16" height="12" rx="2.5" fill="#FFFFFF"/>
  <path d="M18 11H22.5L25.5 15.5V20H18V11Z" fill="#DCFCE7"/>
  <path d="M19 12.5H22L24.5 15.5H19V12.5Z" fill="#16A34A"/>
  <circle cx="7" cy="20" r="3" fill="#15803D" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="21" cy="20" r="3" fill="#15803D" stroke="#FFFFFF" stroke-width="1.5"/>
</svg>'''

SVG_CALL = '''<svg width="22" height="22" viewBox="0 0 24 24" fill="none" style="display:block;"><path d="M22 16.92V19.92C22.0011 20.1985 21.9441 20.4742 21.8325 20.7294C21.7209 20.9845 21.5573 21.2136 21.3521 21.4019C21.1468 21.5901 20.9046 21.7335 20.6407 21.8228C20.3769 21.912 20.0974 21.9452 19.82 21.92C16.7428 21.5856 13.787 20.5342 11.19 18.85C8.77382 17.3147 6.72533 15.2662 5.18999 12.85C3.49997 10.2412 2.44824 7.27099 2.11999 4.17997C2.095 3.90354 2.12787 3.62486 2.21651 3.36173C2.30516 3.0986 2.44766 2.85686 2.63503 2.65171C2.82241 2.44655 3.05051 2.28257 3.30456 2.17013C3.55861 2.05769 3.83307 2.00003 4.10999 2H7.10999C7.5953 1.99522 8.06579 2.16708 8.43376 2.48353C8.80173 2.80007 9.04207 3.23945 9.10999 3.71997C9.23662 4.68007 9.47144 5.62273 9.80999 6.52997C9.9446 6.88789 9.97366 7.27689 9.8939 7.65089C9.81415 8.02488 9.62886 8.36814 9.35999 8.63997L8.08999 9.90997C9.51355 12.4135 11.5864 14.4864 14.09 15.91L15.36 14.64C15.6318 14.3711 15.9751 14.1858 16.3491 14.1061C16.7231 14.0263 17.1121 14.0554 17.47 14.19C18.3773 14.5285 19.3199 14.7634 20.28 14.89C20.7658 14.9585 21.2094 15.2032 21.5265 15.5776C21.8437 15.9519 22.0121 16.4305 22 16.92Z" fill="#16A34A"/></svg>'''

SVG_MSG = '''<svg width="22" height="22" viewBox="0 0 24 24" fill="none" style="display:block;"><path d="M21 11.5C21.0034 12.8199 20.6951 14.1219 20.1 15.3C19.3944 16.7118 18.3098 17.8992 16.9674 18.7293C15.6251 19.5594 14.0782 19.9994 12.5 20C11.1801 20.0034 9.87812 19.6951 8.7 19.1L3 21L4.9 15.3C4.30493 14.1219 3.99656 12.8199 4 11.5C4.00061 9.92179 4.44061 8.37488 5.27072 7.03258C6.10083 5.69028 7.28825 4.6056 8.7 3.90003C9.87812 3.30496 11.1801 2.99659 12.5 3.00003H13C15.0843 3.11502 17.053 3.99479 18.5291 5.47089C20.0052 6.94699 20.885 8.91568 21 11V11.5Z" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="#EFF6FF"/><circle cx="8.5" cy="11.5" r="1.2" fill="#2563EB"/><circle cx="12.5" cy="11.5" r="1.2" fill="#2563EB"/><circle cx="16.5" cy="11.5" r="1.2" fill="#2563EB"/></svg>'''

SVG_SHARE = '''<svg width="22" height="22" viewBox="0 0 24 24" fill="none" style="display:block;"><circle cx="18" cy="5" r="3" fill="#8B5CF6" stroke="#8B5CF6" stroke-width="1.5"/><circle cx="6" cy="12" r="3" fill="#8B5CF6" stroke="#8B5CF6" stroke-width="1.5"/><circle cx="18" cy="19" r="3" fill="#8B5CF6" stroke="#8B5CF6" stroke-width="1.5"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49" stroke="#8B5CF6" stroke-width="2" stroke-linecap="round"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49" stroke="#8B5CF6" stroke-width="2" stroke-linecap="round"/></svg>'''

SVG_CANCEL = '''<svg width="22" height="22" viewBox="0 0 24 24" fill="none" style="display:block;"><circle cx="12" cy="12" r="10" fill="#FEE2E2"/><path d="M15 9L9 15M9 9L15 15" stroke="#EF4444" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'''

SVG_PIN_FARM = '''<svg width="18" height="18" viewBox="0 0 24 24" fill="none" style="flex-shrink:0;"><circle cx="12" cy="10" r="3" fill="#22C55E"/><path d="M12 2C7.58 2 4 5.58 4 10C4 15.25 12 22 12 22C12 22 20 15.25 20 10C20 5.58 16.42 2 12 2Z" stroke="#22C55E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'''

SVG_APMC_MANDI = '''<svg width="18" height="18" viewBox="0 0 24 24" fill="none" style="flex-shrink:0;"><path d="M3 21H21M4 18V9L12 3L20 9V18M9 21V12H15V21" stroke="#3B82F6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="#EFF6FF"/></svg>'''

SVG_PRODUCE_LOAD = '''<svg width="18" height="18" viewBox="0 0 24 24" fill="none" style="flex-shrink:0;"><path d="M12 22V2M12 7C9.5 5 7 7 7 10C7 13 12 15 12 15M12 7C14.5 5 17 7 17 10C17 13 12 15 12 15M12 12C9.5 10 7 12 7 15C7 18 12 20 12 20M12 12C14.5 10 17 12 17 15C17 18 12 20 12 20" stroke="#F59E0B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'''

SVG_FARE_CURRENCY = '''<svg width="18" height="18" viewBox="0 0 24 24" fill="none" style="flex-shrink:0;"><rect x="2" y="5" width="20" height="14" rx="3" fill="#DCFCE7" stroke="#16A34A" stroke-width="1.8"/><circle cx="16" cy="12" r="2.5" fill="#16A34A"/><path d="M6 9H11M6 12H9.5M6 15L9 12" stroke="#15803D" stroke-width="1.8" stroke-linecap="round"/></svg>'''

SVG_LOCK_SHIELD = '''<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#92400E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>'''

SVG_TRUCK_BANNER = '''<svg width="22" height="22" viewBox="0 0 24 24" fill="none" style="flex-shrink:0;"><rect x="1" y="6" width="14" height="11" rx="2" fill="#0F172A"/><path d="M15 9H19L22 13V17H15V9Z" fill="#0F172A"/><circle cx="5.5" cy="17" r="2.2" fill="#FFFFFF"/><circle cx="18.5" cy="17" r="2.2" fill="#FFFFFF"/><path d="M16 10H18.5L20.5 13H16V10Z" fill="#86EFAC"/></svg>'''

def generate_searching_function():
    return '''function renderTrackingSearchingState(activeTrip) {
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
          <div style="width:48px;height:48px;border-radius:50%;background:linear-gradient(135deg,#16A34A,#15803D);display:flex;align-items:center;justify-content:center;box-shadow:0 0 20px rgba(34,197,94,0.6);z-index:2;">
            ''' + SVG_RADAR_TRUCK + '''
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

        <button onclick="cancelAndReturnToGramhaul()" style="width:100%;height:48px;background:#334155;color:#F1F5F9;border:none;border-radius:14px;font-size:14px;font-weight:800;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;transition:background 0.15s ease;">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#F1F5F9" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
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
      showLuxuryToast(`Driver ${activeTrip.driverName} accepted! Arriving in ${activeTrip.etaMins || 2} min`, 'success');
    }
  }, 1800);
}'''

def generate_dispatched_function():
    return '''function renderTrackingDispatchedState(activeTrip) {
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
          <div style="color:#0F172A;font-weight:900;font-size:14.5px;letter-spacing:-0.2px;display:flex;align-items:center;gap:8px;">
            ''' + SVG_TRUCK_BANNER + '''
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
              <div style="position:relative;width:48px;height:48px;border-radius:50%;overflow:hidden;background:#DCFCE7;border:2px solid #22C55E;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                ''' + SVG_DRIVER_AVATAR + '''
              </div>
              <div>
                <div style="display:flex;align-items:center;gap:6px;">
                  <span style="font-size:16px;font-weight:900;color:#FFFFFF;">${driverName}</span>
                  <span style="font-size:12.5px;font-weight:900;color:#F59E0B;display:flex;align-items:center;gap:3px;">
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="#F59E0B"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
                    <span>${rating.toString().replace(/[^0-9.]/g, '') || '4.9'}</span>
                  </span>
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
          <div style="background:#FEF3C7;border:1.5px solid #F59E0B;border-radius:14px;padding:12px 16px;display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;box-shadow:0 4px 14px rgba(245,158,11,0.18);">
            <div>
              <div style="display:flex;align-items:center;gap:6px;">
                ''' + SVG_LOCK_SHIELD + '''
                <div style="font-size:11px;font-weight:900;color:#92400E;text-transform:uppercase;letter-spacing:0.8px;">Start Trip OTP</div>
              </div>
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
              <div style="width:48px;height:48px;border-radius:50%;background:#DCFCE7;border:1px solid #86EFAC;display:flex;align-items:center;justify-content:center;box-shadow:0 3px 10px rgba(22,163,74,0.25);transition:transform 0.15s ease;">
                ''' + SVG_CALL + '''
              </div>
              <span style="font-size:11px;color:#CBD5E1;font-weight:700;">Call</span>
            </div>

            <!-- Message Action -->
            <div onclick="openDriverLiveChatModal('${driverName}', '${plate}')" style="display:flex;flex-direction:column;align-items:center;gap:6px;cursor:pointer;">
              <div style="width:48px;height:48px;border-radius:50%;background:#EFF6FF;border:1px solid #BFDBFE;display:flex;align-items:center;justify-content:center;box-shadow:0 3px 10px rgba(37,99,235,0.25);transition:transform 0.15s ease;">
                ''' + SVG_MSG + '''
              </div>
              <span style="font-size:11px;color:#CBD5E1;font-weight:700;">Message</span>
            </div>

            <!-- Share Action -->
            <div onclick="shareLiveHaulTrip('${activeTrip.id || 'GH-4491'}')" style="display:flex;flex-direction:column;align-items:center;gap:6px;cursor:pointer;">
              <div style="width:48px;height:48px;border-radius:50%;background:#F3E8FF;border:1px solid #DDD6FE;display:flex;align-items:center;justify-content:center;box-shadow:0 3px 10px rgba(139,92,246,0.25);transition:transform 0.15s ease;">
                ''' + SVG_SHARE + '''
              </div>
              <span style="font-size:11px;color:#CBD5E1;font-weight:700;">Share</span>
            </div>

            <!-- Cancel Action -->
            <div onclick="cancelActiveHaulTripAndExit()" style="display:flex;flex-direction:column;align-items:center;gap:6px;cursor:pointer;">
              <div style="width:48px;height:48px;border-radius:50%;background:#FEE2E2;border:1px solid #FECACA;display:flex;align-items:center;justify-content:center;box-shadow:0 3px 10px rgba(239,68,68,0.25);transition:transform 0.15s ease;">
                ''' + SVG_CANCEL + '''
              </div>
              <span style="font-size:11px;color:#CBD5E1;font-weight:700;">Cancel</span>
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
              <div style="width:20px;height:20px;animation:truckDrive 2s ease-in-out infinite;transform:scaleX(-1);display:flex;align-items:center;justify-content:center;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><rect x="1" y="6" width="14" height="11" rx="2" fill="#16A34A"/><path d="M15 9H19L22 13V17H15V9Z" fill="#15803D"/><circle cx="5.5" cy="17" r="2.2" fill="#0F172A"/><circle cx="18.5" cy="17" r="2.2" fill="#0F172A"/></svg>
              </div>
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
              <span id="gh-trip-arrow" style="font-size:12px;color:#94A3B8;transition:transform 0.2s ease;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#94A3B8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
              </span>
            </div>

            <div id="gh-trip-details-content" style="display:none;padding:0 14px 14px;font-size:12px;flex-direction:column;gap:8px;border-top:1px solid #334155;">
              <div style="display:flex;align-items:center;justify-content:space-between;margin-top:8px;">
                <div style="display:flex;align-items:center;gap:6px;color:#94A3B8;">''' + SVG_PIN_FARM + '''<span>Farm Pickup:</span></div>
                <strong style="color:#FFFFFF;">${activeTrip.pickup || 'Himayath Nagar Farm, Telangana'}</strong>
              </div>
              <div style="display:flex;align-items:center;justify-content:space-between;">
                <div style="display:flex;align-items:center;gap:6px;color:#94A3B8;">''' + SVG_APMC_MANDI + '''<span>Destination Mandi:</span></div>
                <strong style="color:#22C55E;">${mandiName}</strong>
              </div>
              <div style="display:flex;align-items:center;justify-content:space-between;">
                <div style="display:flex;align-items:center;gap:6px;color:#94A3B8;">''' + SVG_PRODUCE_LOAD + '''<span>Produce Load:</span></div>
                <strong style="color:#FFFFFF;">${crop} (${sacks})</strong>
              </div>
              <div style="display:flex;align-items:center;justify-content:space-between;">
                <div style="display:flex;align-items:center;gap:6px;color:#94A3B8;">''' + SVG_FARE_CURRENCY + '''<span>Freight Fare:</span></div>
                <strong style="color:#22C55E;font-size:14px;">₹${fare} (0% Commission)</strong>
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
      html: `<div style="display:flex;flex-direction:column;align-items:center;transform:translate(-50%, -100%);filter:drop-shadow(0 6px 14px rgba(0,0,0,0.35));">
        <div style="background:#FBBF24;color:#0F172A;border:1.5px solid #000000;padding:2px 8px;border-radius:6px;font-size:10px;font-weight:900;letter-spacing:0.8px;font-family:monospace;white-space:nowrap;box-shadow:0 2px 6px rgba(0,0,0,0.25);margin-bottom:2px;">
          ${plate}
        </div>
        <div style="width:42px;height:42px;border-radius:50%;background:#FFFFFF;border:2.5px solid #22C55E;display:flex;align-items:center;justify-content:center;box-shadow:0 0 16px rgba(34,197,94,0.7);">
          <svg width="24" height="24" viewBox="0 0 28 28" fill="none">
            <rect x="3" y="9" width="15" height="11" rx="2" fill="#16A34A"/>
            <path d="M18 12H22L24.5 15.5V20H18V12Z" fill="#15803D"/>
            <rect x="19" y="13.5" width="3" height="2.5" rx="0.5" fill="#BBF7D0"/>
            <circle cx="7.5" cy="20" r="2.5" fill="#0F172A" stroke="#FFFFFF" stroke-width="1"/>
            <circle cx="20.5" cy="20" r="2.5" fill="#0F172A" stroke="#FFFFFF" stroke-width="1"/>
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

def generate_call_function():
    return '''function triggerDriverCall(driverName, phone) {
  const modalId = 'driver-live-call-modal';
  let modal = document.getElementById(modalId);
  if (modal) modal.remove();

  activeHaulCallSeconds = 0;

  modal = document.createElement('div');
  modal.id = modalId;
  modal.style.cssText = 'position:fixed;inset:0;background:rgba(15,23,42,0.92);backdrop-filter:blur(10px);z-index:999999;display:flex;align-items:center;justify-content:center;animation:fadeIn 0.2s ease;';
  
  modal.innerHTML = `
    <div style="width:100%;max-width:380px;text-align:center;padding:24px;color:#FFFFFF;">
      <div style="width:96px;height:96px;border-radius:50%;background:#DCFCE7;border:3px solid #22C55E;margin:0 auto 16px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 30px rgba(34,197,94,0.4);">
        ''' + SVG_DRIVER_AVATAR_LARGE + '''
      </div>

      <div style="font-size:20px;font-weight:900;color:#FFFFFF;margin-bottom:4px;">${driverName}</div>
      <div style="font-size:13px;color:#22C55E;font-weight:700;margin-bottom:8px;">● Connected via NuKropAI Secure Call</div>
      <div id="haul-call-duration" style="font-size:15px;color:#94A3B8;font-weight:800;letter-spacing:1px;margin-bottom:30px;">00:01</div>

      <div style="display:flex;justify-content:center;gap:20px;margin-bottom:32px;">
        <button style="width:54px;height:54px;border-radius:50%;background:rgba(255,255,255,0.12);border:none;color:#FFFFFF;cursor:pointer;display:flex;align-items:center;justify-content:center;">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg>
        </button>
        <button style="width:54px;height:54px;border-radius:50%;background:rgba(255,255,255,0.12);border:none;color:#FFFFFF;cursor:pointer;display:flex;align-items:center;justify-content:center;">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"/></svg>
        </button>
      </div>

      <button onclick="endDriverLiveCall('${modalId}')" style="width:68px;height:68px;border-radius:50%;background:#EF4444;border:none;color:#FFFFFF;cursor:pointer;box-shadow:0 8px 24px rgba(239,68,68,0.4);display:inline-flex;align-items:center;justify-content:center;transition:transform 0.15s ease;">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>
      <div style="font-size:12px;color:#94A3B8;margin-top:10px;font-weight:700;">End Call</div>
    </div>
  `;

  document.body.appendChild(modal);

  if (activeHaulCallTimer) clearInterval(activeHaulCallTimer);
  activeHaulCallTimer = setInterval(() => {
    activeHaulCallSeconds++;
    const durEl = document.getElementById('haul-call-duration');
    if (durEl) {
      const m = String(Math.floor(activeHaulCallSeconds / 60)).padStart(2, '0');
      const s = String(activeHaulCallSeconds % 60).padStart(2, '0');
      durEl.textContent = `${m}:${s}`;
    }
  }, 1000);
}'''

def generate_chat_function():
    return '''function openDriverLiveChatModal(driverName, plate) {
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
  modal.style.cssText = 'position:fixed;inset:0;background:rgba(15,23,42,0.7);backdrop-filter:blur(6px);z-index:999999;display:flex;align-items:flex-end;justify-content:center;animation:fadeIn 0.2s ease;';
  
  modal.innerHTML = `
    <div style="background:#0F172A;width:100%;height:75vh;border-radius:28px 28px 0 0;padding:18px 16px 20px;display:flex;flex-direction:column;box-shadow:0 -10px 40px rgba(0,0,0,0.5);border-top:1px solid #334155;animation:slideUp 0.25s cubic-bezier(0.16, 1, 0.3, 1);">
      
      <!-- Chat Header -->
      <div style="display:flex;align-items:center;justify-content:space-between;padding-bottom:12px;border-bottom:1px solid #1E293B;">
        <div style="display:flex;align-items:center;gap:10px;">
          <div style="width:40px;height:40px;border-radius:50%;background:#DCFCE7;border:1.5px solid #22C55E;display:flex;align-items:center;justify-content:center;overflow:hidden;">
            ''' + SVG_DRIVER_AVATAR + '''
          </div>
          <div>
            <div style="font-size:14px;font-weight:900;color:#FFFFFF;display:flex;align-items:center;gap:6px;">
              <span>${driverName}</span>
              <span style="font-size:10px;color:#22C55E;background:#14532D;padding:1px 6px;border-radius:6px;font-weight:800;">● Online</span>
            </div>
            <div style="font-size:11px;color:#94A3B8;">${plate} · Tata Ace Gold</div>
          </div>
        </div>
        <button onclick="document.getElementById('${modalId}').remove();" style="background:#1E293B;border:1px solid #334155;color:#94A3B8;width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#94A3B8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      </div>

      <!-- Messages Stream -->
      <div id="live-haul-chat-stream" style="flex:1;overflow-y:auto;padding:14px 0;display:flex;flex-direction:column;gap:10px;">
        ${msgs.map(m => `
          <div style="display:flex;justify-content:${m.sender === 'farmer' ? 'flex-end' : 'flex-start'};">
            <div style="max-width:80%;background:${m.sender === 'farmer' ? '#16A34A' : '#1E293B'};color:#FFFFFF;padding:10px 14px;border-radius:${m.sender === 'farmer' ? '16px 16px 2px 16px' : '16px 16px 16px 2px'};font-size:12.5px;line-height:1.4;box-shadow:0 2px 6px rgba(0,0,0,0.2);">
              <div>${m.text}</div>
              <div style="font-size:9.5px;color:rgba(255,255,255,0.6);text-align:right;margin-top:4px;">${m.time}</div>
            </div>
          </div>
        `).join('')}
      </div>

      <!-- Quick Reply Preset Chips -->
      <div style="display:flex;gap:6px;overflow-x:auto;padding-bottom:10px;scrollbar-width:none;-webkit-overflow-scrolling:touch;">
        <button onclick="sendQuickChatMessage('Farm Gate is open')" style="background:#1E293B;color:#CBD5E1;border:1px solid #334155;border-radius:20px;padding:6px 12px;font-size:11px;font-weight:700;white-space:nowrap;cursor:pointer;">Gate is open</button>
        <button onclick="sendQuickChatMessage('40 Sacks ready at entrance')" style="background:#1E293B;color:#CBD5E1;border:1px solid #334155;border-radius:20px;padding:6px 12px;font-size:11px;font-weight:700;white-space:nowrap;cursor:pointer;">40 Sacks ready</button>
        <button onclick="sendQuickChatMessage('Call me when you reach main road')" style="background:#1E293B;color:#CBD5E1;border:1px solid #334155;border-radius:20px;padding:6px 12px;font-size:11px;font-weight:700;white-space:nowrap;cursor:pointer;">Call at turn</button>
      </div>

      <!-- Message Input Bar -->
      <div style="display:flex;gap:8px;align-items:center;">
        <input id="haul-chat-input" placeholder="Type a message to Suresh..." style="flex:1;background:#1E293B;border:1px solid #334155;border-radius:20px;padding:10px 14px;color:#FFFFFF;font-size:13px;outline:none;" onkeypress="if(event.key==='Enter')sendLiveHaulChatMessage()" />
        <button onclick="sendLiveHaulChatMessage()" style="width:42px;height:42px;border-radius:50%;background:#16A34A;border:none;color:#FFFFFF;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 3px 10px rgba(22,163,74,0.4);transition:transform 0.15s ease;">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
        </button>
      </div>

    </div>
  `;

  document.body.appendChild(modal);
  const stream = document.getElementById('live-haul-chat-stream');
  if (stream) stream.scrollTop = stream.scrollHeight;
}'''

print("Functions generated successfully.")
