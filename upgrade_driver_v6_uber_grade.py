import sys, re
sys.stdout.reconfigure(encoding='utf-8')

# ═══════════════════════════════════════════════════════════════
# NuKropAI GramHaul Driver App v6.0 — True Uber Driver Grade
# Full functional nav, micro-interactions, SVG animations
# ═══════════════════════════════════════════════════════════════

# The full driver_dashboard view — replaces existing one
DRIVER_V6_VIEW = '''driver_dashboard: () => {
    // Auto-dismiss notification banner in driver cockpit
    const alertBanner = document.getElementById('nukrop-alert-banner');
    if (alertBanner) alertBanner.style.display = 'none';

    let activeTrip = null;
    try {
      const tripRaw = localStorage.getItem('nukrop_active_trip');
      if (tripRaw) activeTrip = JSON.parse(tripRaw);
    } catch(e) {}

    const driverName   = localStorage.getItem('nukrop_driver_name') || 'Suresh Yadav';
    const vehiclePlate = localStorage.getItem('nukrop_driver_plate') || 'TS 03 UB 4491';
    const vehicleType  = localStorage.getItem('nukrop_driver_vehicle') || 'Tata Ace 1.5T';
    const isOnline     = (localStorage.getItem('gh_driver_online') || 'true') === 'true';
    const activeTab    = localStorage.getItem('gh_driver_tab') || 'map';

    const tripId      = activeTrip ? activeTrip.id : 'GH-4192';
    const tripCrop    = activeTrip ? (activeTrip.crop + ' (' + activeTrip.weight + ')') : 'Cotton (పత్తి) · 40 Quintals DCH-32';
    const tripPickup  = activeTrip ? (typeof currentGramhaulFarmAddress !== 'undefined' ? currentGramhaulFarmAddress : "Ramesh Rao's Farm, Sy.No 142/A") : "Ramesh Rao's Farm, Sy.No 142/A, Narsampet Rural";
    const tripLandmark = typeof currentGramhaulFarmLandmark !== 'undefined' ? currentGramhaulFarmLandmark : 'Near Big Banyan Tree & Power Transformer';
    const tripDrop    = activeTrip ? activeTrip.mandi : 'Warangal Enamamula APMC Yard (Gate 3)';
    const tripFare    = activeTrip ? activeTrip.fare : '1,850';
    const tripEtaMins = '8';
    const tripDistKm  = '4.8';

    // ─── SHARED CSS (animations, micro-interactions) ───
    const sharedCSS = `
      <style>
        @keyframes pulseRing {
          0%   { box-shadow: 0 0 0 0 rgba(22,163,74,0.45); }
          70%  { box-shadow: 0 0 0 12px rgba(22,163,74,0); }
          100% { box-shadow: 0 0 0 0 rgba(22,163,74,0); }
        }
        @keyframes pulseRingRed {
          0%   { box-shadow: 0 0 0 0 rgba(220,38,38,0.45); }
          70%  { box-shadow: 0 0 0 12px rgba(220,38,38,0); }
          100% { box-shadow: 0 0 0 0 rgba(220,38,38,0); }
        }
        @keyframes slideUp {
          from { transform: translateY(30px); opacity: 0; }
          to   { transform: translateY(0); opacity: 1; }
        }
        @keyframes fadeIn {
          from { opacity: 0; } to { opacity: 1; }
        }
        @keyframes spinDot {
          0%   { transform: rotate(0deg);   }
          100% { transform: rotate(360deg); }
        }
        @keyframes shimmer {
          0%   { background-position: -400px 0; }
          100% { background-position: 400px 0; }
        }
        @keyframes barGrow {
          from { transform: scaleY(0); }
          to   { transform: scaleY(1); }
        }
        .gh-card { animation: slideUp 0.3s cubic-bezier(0.16,1,0.3,1) both; }
        .gh-card:nth-child(2) { animation-delay: 0.06s; }
        .gh-card:nth-child(3) { animation-delay: 0.12s; }
        .gh-btn-press:active { transform: scale(0.96); transition: transform 0.1s; }
        .gh-nav-tab { transition: all 0.18s cubic-bezier(0.16,1,0.3,1); }
        .gh-nav-tab:active { transform: scale(0.9); }
        .gh-nav-tab.active svg { filter: drop-shadow(0 2px 4px rgba(22,163,74,0.4)); }
        .gh-pill-online { animation: pulseRing 2s infinite; }
        .gh-pill-offline { animation: pulseRingRed 2s infinite; }
        .gh-shimmer {
          background: linear-gradient(90deg, #F1F5F9 25%, #E8EDF5 50%, #F1F5F9 75%);
          background-size: 400px 100%;
          animation: shimmer 1.4s infinite linear;
          border-radius: 8px;
        }
        .gh-bar { transform-origin: bottom; animation: barGrow 0.6s cubic-bezier(0.34,1.56,0.64,1) both; }
        .gh-bar:nth-child(1) { animation-delay: 0.0s; }
        .gh-bar:nth-child(2) { animation-delay: 0.06s; }
        .gh-bar:nth-child(3) { animation-delay: 0.12s; }
        .gh-bar:nth-child(4) { animation-delay: 0.18s; }
        .gh-bar:nth-child(5) { animation-delay: 0.24s; }
        .gh-bar:nth-child(6) { animation-delay: 0.30s; }
        .gh-bar:nth-child(7) { animation-delay: 0.36s; }
        .gh-accept-btn {
          background: #16A34A;
          border: none;
          border-radius: 18px;
          color: #FFFFFF;
          font-size: 16px;
          font-weight: 900;
          width: 100%;
          height: 56px;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 10px;
          box-shadow: 0 8px 24px rgba(22,163,74,0.40);
          transition: transform 0.15s, box-shadow 0.15s;
        }
        .gh-accept-btn:active { transform: scale(0.97); box-shadow: 0 4px 12px rgba(22,163,74,0.30); }
        .gh-accept-btn:hover { box-shadow: 0 12px 28px rgba(22,163,74,0.50); }
        .online-dot {
          width: 8px; height: 8px; border-radius: 50%; background: #16A34A;
          display: inline-block; margin-right: 6px;
          animation: pulseRing 2s infinite;
        }
      </style>
    `;

    // ─── ONLINE / OFFLINE STATUS PILL ───
    const onlinePill = isOnline
      ? `<button class="gh-btn-press" onclick="toggleGhDriverOnline()" style="display:flex;align-items:center;gap:10px;background:#0F172A;border:none;border-radius:100px;padding:8px 18px 8px 8px;box-shadow:0 4px 20px rgba(0,0,0,0.30);cursor:pointer;">
           <div class="gh-pill-online" style="width:36px;height:36px;border-radius:50%;background:#16A34A;display:flex;align-items:center;justify-content:center;">
             <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
           </div>
           <div style="text-align:left;">
             <div style="font-size:14px;font-weight:900;color:#FFFFFF;letter-spacing:-0.2px;">On Duty</div>
             <div style="font-size:10px;color:#94A3B8;font-weight:600;">Tap to go offline</div>
           </div>
           <svg style="margin-left:4px;" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#94A3B8" stroke-width="2.5" stroke-linecap="round"><polyline points="6 9 12 15 18 9"/></svg>
         </button>`
      : `<button class="gh-btn-press" onclick="toggleGhDriverOnline()" style="display:flex;align-items:center;gap:10px;background:#0F172A;border:none;border-radius:100px;padding:8px 18px 8px 8px;box-shadow:0 4px 20px rgba(0,0,0,0.30);cursor:pointer;">
           <div class="gh-pill-offline" style="width:36px;height:36px;border-radius:50%;background:#DC2626;display:flex;align-items:center;justify-content:center;">
             <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
           </div>
           <div style="text-align:left;">
             <div style="font-size:14px;font-weight:900;color:#FFFFFF;letter-spacing:-0.2px;">Offline</div>
             <div style="font-size:10px;color:#94A3B8;font-weight:600;">Tap to go online</div>
           </div>
           <svg style="margin-left:4px;" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#94A3B8" stroke-width="2.5" stroke-linecap="round"><polyline points="6 9 12 15 18 9"/></svg>
         </button>`;

    // ─── MAP TAB (Main Cockpit) ───
    const mapTabHtml = activeTrip ? `
      <div class="gh-card" style="background:#FFFFFF;border-radius:24px;overflow:hidden;box-shadow:0 4px 24px rgba(15,23,42,0.10);margin-bottom:14px;">
        <!-- Map Strip -->
        <div style="width:100%;height:190px;background:linear-gradient(145deg,#E8F5E9 0%,#F0F9F0 50%,#E8F5E9 100%);position:relative;overflow:hidden;">
          <!-- Animated map grid lines -->
          <svg style="position:absolute;inset:0;width:100%;height:100%;opacity:0.3;" preserveAspectRatio="none">
            <defs><pattern id="mgrid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M 30 0 L 0 0 0 30" fill="none" stroke="#16A34A" stroke-width="0.5"/></pattern></defs>
            <rect width="100%" height="100%" fill="url(#mgrid)"/>
          </svg>
          <!-- Route line SVG -->
          <svg style="position:absolute;inset:0;width:100%;height:100%;" viewBox="0 0 430 190">
            <defs>
              <linearGradient id="routeGrad" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0%" stop-color="#16A34A"/>
                <stop offset="100%" stop-color="#4ADE80"/>
              </linearGradient>
            </defs>
            <polyline points="60,150 120,130 180,90 250,70 330,50 390,40" fill="none" stroke="url(#routeGrad)" stroke-width="4" stroke-linecap="round" stroke-dasharray="8 4" opacity="0.8"/>
            <!-- Pickup pin -->
            <circle cx="60" cy="150" r="10" fill="#16A34A"/>
            <circle cx="60" cy="150" r="6" fill="#FFFFFF"/>
            <!-- Drop pin -->
            <circle cx="390" cy="40" r="10" fill="#DC2626"/>
            <circle cx="390" cy="40" r="6" fill="#FFFFFF"/>
            <!-- Driver truck -->
            <g transform="translate(180,82) rotate(-25)">
              <rect x="-14" y="-8" width="28" height="16" rx="4" fill="#0F172A"/>
              <rect x="-18" y="-5" width="8" height="10" rx="2" fill="#1E293B"/>
              <circle cx="-10" cy="9" r="4" fill="#0F172A" stroke="#FFFFFF" stroke-width="1.5"/>
              <circle cx="8" cy="9" r="4" fill="#0F172A" stroke="#FFFFFF" stroke-width="1.5"/>
            </g>
          </svg>
          <!-- Decline button -->
          <button onclick="driverDeclineHaul()" class="gh-btn-press" style="position:absolute;top:10px;left:10px;background:rgba(15,23,42,0.72);border:none;border-radius:100px;padding:5px 14px;color:#FFFFFF;font-size:11.5px;font-weight:800;cursor:pointer;backdrop-filter:blur(8px);">
            Decline
          </button>
          <!-- ETA badge -->
          <div style="position:absolute;bottom:10px;right:10px;background:rgba(255,255,255,0.92);border-radius:10px;padding:4px 10px;backdrop-filter:blur(8px);">
            <span style="font-size:11px;font-weight:800;color:#0F172A;">${tripEtaMins} min away</span>
          </div>
        </div>

        <div style="padding:14px 16px 16px;">
          <!-- Badges row -->
          <div style="display:flex;align-items:center;gap:6px;margin-bottom:8px;flex-wrap:wrap;">
            <span style="background:#F0FDF4;color:#16A34A;font-size:10px;font-weight:900;padding:3px 8px;border-radius:6px;border:1px solid #BBF7D0;">⚡ Zero Platform Fee</span>
            <span style="background:#FEF3C7;color:#D97706;font-size:10px;font-weight:900;padding:3px 8px;border-radius:6px;border:1px solid #FDE68A;">LIVE TRIP #${tripId}</span>
          </div>

          <!-- ETA + Fare Hero -->
          <div style="display:flex;align-items:flex-end;justify-content:space-between;margin-bottom:14px;">
            <div>
              <div style="font-size:28px;font-weight:900;color:#0F172A;letter-spacing:-0.6px;line-height:1;">${tripEtaMins} min · ${tripDistKm} km</div>
              <div style="font-size:12px;color:#64748B;font-weight:600;margin-top:3px;">to Farmer Pickup Location</div>
            </div>
            <div style="text-align:right;">
              <div style="font-size:24px;font-weight:900;color:#16A34A;letter-spacing:-0.4px;">₹${tripFare}</div>
              <div style="font-size:10px;color:#64748B;">Haul Fare</div>
            </div>
          </div>

          <!-- Route card -->
          <div style="background:#F8FAFC;border-radius:16px;padding:12px 14px;margin-bottom:14px;">
            <div style="display:flex;gap:12px;margin-bottom:10px;">
              <div style="display:flex;flex-direction:column;align-items:center;padding-top:3px;flex-shrink:0;">
                <div style="width:10px;height:10px;border-radius:50%;background:#16A34A;box-shadow:0 0 0 3px rgba(22,163,74,0.2);"></div>
                <div style="width:1.5px;height:22px;background:linear-gradient(#16A34A,#DC2626);margin:3px 0;"></div>
                <div style="width:10px;height:10px;border-radius:50%;background:#DC2626;box-shadow:0 0 0 3px rgba(220,38,38,0.2);"></div>
              </div>
              <div style="flex:1;min-width:0;">
                <div style="margin-bottom:12px;">
                  <div style="font-size:10px;color:#94A3B8;font-weight:800;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:2px;">Farmer GPS Pickup</div>
                  <div style="font-size:13px;font-weight:800;color:#0F172A;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${tripPickup}</div>
                  <div style="font-size:11px;color:#64748B;margin-top:1px;">${tripLandmark}</div>
                </div>
                <div>
                  <div style="font-size:10px;color:#94A3B8;font-weight:800;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:2px;">APMC Mandi Drop</div>
                  <div style="font-size:13px;font-weight:800;color:#0F172A;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${tripDrop}</div>
                </div>
              </div>
            </div>
            <div style="display:flex;gap:6px;flex-wrap:wrap;padding-top:10px;border-top:1px solid #F1F5F9;">
              <span style="background:#fff;border:1px solid #E2E8F0;border-radius:8px;padding:4px 9px;font-size:10.5px;font-weight:700;color:#334155;">🌾 ${tripCrop}</span>
              <span style="background:#fff;border:1px solid #E2E8F0;border-radius:8px;padding:4px 9px;font-size:10.5px;font-weight:700;color:#334155;">
                <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="vertical-align:middle;margin-right:2px;"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                Ramesh Rao
              </span>
              <span style="background:#fff;border:1px solid #E2E8F0;border-radius:8px;padding:4px 9px;font-size:10.5px;font-weight:700;color:#334155;">
                <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="vertical-align:middle;margin-right:2px;"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12 19.79 19.79 0 0 1 1.61 3.4 2 2 0 0 1 3.6 1.2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.82a16 16 0 0 0 6 6l.91-.91a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
                +91 94401 22910
              </span>
            </div>
          </div>

          <!-- Action buttons row -->
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:10px;">
            <button onclick="driverCallFarmer('+919440122910')" class="gh-btn-press" style="height:46px;background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:14px;font-size:12px;font-weight:800;color:#0F172A;display:flex;align-items:center;justify-content:center;gap:7px;cursor:pointer;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12 19.79 19.79 0 0 1 1.61 3.4 2 2 0 0 1 3.6 1.2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.82a16 16 0 0 0 6 6l.91-.91a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
              Call Farmer
            </button>
            <button onclick="messageGramhaulDriver()" class="gh-btn-press" style="height:46px;background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:14px;font-size:12px;font-weight:800;color:#0F172A;display:flex;align-items:center;justify-content:center;gap:7px;cursor:pointer;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
              Live Chat
            </button>
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
            <button onclick="driverOpenGpsNav(17.9689, 79.5941)" class="gh-btn-press" style="height:52px;background:#16A34A;color:#FFFFFF;border:none;border-radius:16px;font-size:13.5px;font-weight:900;display:flex;align-items:center;justify-content:center;gap:8px;cursor:pointer;box-shadow:0 6px 20px rgba(22,163,74,0.35);">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg>
              GPS Navigate
            </button>
            <button onclick="driverShowPaymentScreen('${tripId}', '${tripFare}')" class="gh-btn-press" style="height:52px;background:#0F172A;color:#FFFFFF;border:none;border-radius:16px;font-size:13.5px;font-weight:900;display:flex;align-items:center;justify-content:center;gap:8px;cursor:pointer;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
              Delivered
            </button>
          </div>
        </div>
      </div>` : `
      <!-- ═══ WAITING STATE — Haul Requests Pool ═══ -->
      <div id="gh-available-hauls">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
          <div style="font-size:16px;font-weight:900;color:#0F172A;letter-spacing:-0.2px;">Haul Requests</div>
          <span style="background:#DCFCE7;color:#15803D;font-size:10px;font-weight:800;padding:3px 10px;border-radius:100px;border:1px solid #86EFAC;">● 2 Nearby</span>
        </div>

        <!-- HAUL CARD 1 — HIGH PRIORITY -->
        <div class="gh-card" style="background:#FFFFFF;border-radius:22px;overflow:hidden;box-shadow:0 2px 20px rgba(15,23,42,0.09);margin-bottom:12px;">
          <!-- Mini map -->
          <div style="height:110px;background:linear-gradient(145deg,#E8F5E9,#F1F8F1);position:relative;overflow:hidden;">
            <svg style="position:absolute;inset:0;width:100%;height:100%;opacity:0.25;" preserveAspectRatio="none">
              <defs><pattern id="g1" width="25" height="25" patternUnits="userSpaceOnUse"><path d="M 25 0 L 0 0 0 25" fill="none" stroke="#16A34A" stroke-width="0.5"/></pattern></defs>
              <rect width="100%" height="100%" fill="url(#g1)"/>
            </svg>
            <svg style="position:absolute;inset:0;width:100%;height:100%;" viewBox="0 0 390 110">
              <polyline points="30,85 100,70 180,45 280,30 360,25" fill="none" stroke="#16A34A" stroke-width="3.5" stroke-dasharray="8 4" stroke-linecap="round" opacity="0.7"/>
              <circle cx="30" cy="85" r="8" fill="#16A34A"/><circle cx="30" cy="85" r="4" fill="#fff"/>
              <circle cx="360" cy="25" r="8" fill="#DC2626"/><circle cx="360" cy="25" r="4" fill="#fff"/>
            </svg>
            <button onclick="declineHaulRequest('GH-8824')" class="gh-btn-press" style="position:absolute;top:8px;left:8px;background:rgba(15,23,42,0.70);border:none;border-radius:100px;padding:4px 12px;color:#fff;font-size:11px;font-weight:800;cursor:pointer;backdrop-filter:blur(8px);">Decline −12</button>
            <div style="position:absolute;top:8px;right:8px;background:rgba(255,255,255,0.92);border-radius:8px;padding:3px 9px;backdrop-filter:blur(6px);">
              <span style="font-size:10px;font-weight:900;color:#16A34A;">🌶️ Chilli Cargo</span>
            </div>
          </div>
          <div style="padding:12px 14px 14px;">
            <div style="display:flex;align-items:flex-end;justify-content:space-between;margin-bottom:10px;">
              <div>
                <div style="font-size:24px;font-weight:900;color:#0F172A;letter-spacing:-0.5px;line-height:1.1;">5 min · 5.8 km</div>
                <div style="font-size:11.5px;color:#64748B;font-weight:600;margin-top:2px;">to Farmer Pickup</div>
              </div>
              <div style="text-align:right;">
                <div style="font-size:22px;font-weight:900;color:#16A34A;letter-spacing:-0.3px;">₹4,200</div>
                <div style="background:#FEF3C7;border-radius:6px;padding:2px 7px;font-size:9.5px;font-weight:900;color:#D97706;margin-top:2px;display:inline-block;">×2.4 surge</div>
              </div>
            </div>
            <div style="background:#F8FAFC;border-radius:13px;padding:10px 12px;margin-bottom:12px;">
              <div style="display:flex;align-items:flex-start;gap:8px;margin-bottom:7px;">
                <div style="width:8px;height:8px;border-radius:50%;background:#16A34A;flex-shrink:0;margin-top:4px;box-shadow:0 0 0 2px rgba(22,163,74,0.2);"></div>
                <div style="font-size:12.5px;font-weight:700;color:#334155;">K. Anjaiah Farm, Hasanparthy (5.8 km)</div>
              </div>
              <div style="display:flex;align-items:flex-start;gap:8px;margin-bottom:7px;">
                <div style="width:8px;height:8px;border-radius:50%;background:#DC2626;flex-shrink:0;margin-top:4px;box-shadow:0 0 0 2px rgba(220,38,38,0.2);"></div>
                <div style="font-size:12.5px;font-weight:700;color:#334155;">Khammam Spices APMC Mandi (Gate 1)</div>
              </div>
              <div style="display:flex;align-items:center;gap:6px;padding-top:8px;border-top:1px solid #F1F5F9;">
                <span style="font-size:11px;color:#64748B;font-weight:600;">🌶️ Teja Chilli · 25 Bags · 2.5 Ton</span>
                <span style="font-size:11px;color:#64748B;">·</span>
                <span style="font-size:11px;color:#64748B;font-weight:600;">👤 Anjaiah</span>
              </div>
            </div>
            <button onclick="driverAcceptHaulRequest('GH-8824','4200')" class="gh-accept-btn">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
              Accept Haul · ₹4,200
            </button>
          </div>
        </div>

        <!-- HAUL CARD 2 -->
        <div class="gh-card" style="background:#FFFFFF;border-radius:22px;overflow:hidden;box-shadow:0 2px 20px rgba(15,23,42,0.07);margin-bottom:12px;">
          <div style="height:80px;background:linear-gradient(145deg,#FFF7ED,#FEF3C7);position:relative;overflow:hidden;">
            <svg style="position:absolute;inset:0;width:100%;height:100%;" viewBox="0 0 390 80">
              <polyline points="30,60 150,50 260,25 360,20" fill="none" stroke="#D97706" stroke-width="3" stroke-dasharray="8 4" stroke-linecap="round" opacity="0.5"/>
              <circle cx="30" cy="60" r="7" fill="#16A34A"/><circle cx="30" cy="60" r="3.5" fill="#fff"/>
              <circle cx="360" cy="20" r="7" fill="#DC2626"/><circle cx="360" cy="20" r="3.5" fill="#fff"/>
            </svg>
            <button onclick="declineHaulRequest('GH-5512')" class="gh-btn-press" style="position:absolute;top:8px;left:8px;background:rgba(15,23,42,0.65);border:none;border-radius:100px;padding:4px 12px;color:#fff;font-size:11px;font-weight:800;cursor:pointer;backdrop-filter:blur(8px);">Decline</button>
            <div style="position:absolute;top:8px;right:8px;background:rgba(255,255,255,0.92);border-radius:8px;padding:3px 9px;backdrop-filter:blur(6px);">
              <span style="font-size:10px;font-weight:900;color:#D97706;">🌾 Paddy Cargo</span>
            </div>
          </div>
          <div style="padding:12px 14px 14px;">
            <div style="display:flex;align-items:flex-end;justify-content:space-between;margin-bottom:8px;">
              <div>
                <div style="font-size:21px;font-weight:900;color:#0F172A;letter-spacing:-0.4px;">12 min · 9.2 km</div>
                <div style="font-size:11px;color:#64748B;font-weight:600;">to Farmer Pickup</div>
              </div>
              <div style="text-align:right;">
                <div style="font-size:19px;font-weight:900;color:#16A34A;">₹2,800</div>
                <div style="background:#F0FDF4;border-radius:6px;padding:1px 7px;font-size:9.5px;font-weight:900;color:#16A34A;margin-top:2px;display:inline-block;">×1.8</div>
              </div>
            </div>
            <div style="font-size:12px;color:#64748B;margin-bottom:10px;">Jangaon → Warangal APMC · Paddy IR-64 · 30 Bags</div>
            <button onclick="driverAcceptHaulRequest('GH-5512','2800')" class="gh-btn-press" style="width:100%;height:48px;border-radius:15px;background:#0F172A;color:#FFFFFF;font-size:14px;font-weight:900;border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
              Accept · ₹2,800
            </button>
          </div>
        </div>
      </div>`;

    // ─── EARNINGS TAB ───
    const earningsTabHtml = `
      <div class="gh-card" style="background:#FFFFFF;border-radius:22px;padding:18px;box-shadow:0 2px 16px rgba(15,23,42,0.08);margin-bottom:14px;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
          <div style="font-size:16px;font-weight:900;color:#0F172A;letter-spacing:-0.2px;">My Earnings</div>
          <div style="display:flex;gap:4px;background:#F1F5F9;padding:3px;border-radius:100px;">
            <button id="earn-week-btn" onclick="ghSwitchEarnTab('week')" style="background:#0F172A;color:#FFFFFF;border:none;border-radius:100px;padding:4px 14px;font-size:10.5px;font-weight:800;cursor:pointer;">Week</button>
            <button id="earn-month-btn" onclick="ghSwitchEarnTab('month')" style="background:transparent;color:#64748B;border:none;border-radius:100px;padding:4px 14px;font-size:10.5px;font-weight:700;cursor:pointer;">Month</button>
          </div>
        </div>
        <!-- Big number -->
        <div style="margin-bottom:18px;">
          <div style="font-size:11px;color:#94A3B8;font-weight:800;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;">30 Mar – 5 Apr</div>
          <div style="font-size:42px;font-weight:900;color:#0F172A;letter-spacing:-1.5px;line-height:1;">₹60,665</div>
          <div style="font-size:12px;color:#64748B;margin-top:4px;">← ₹70,890 prev week  ·  <span style="color:#DC2626;">−14.4%</span></div>
        </div>
        <!-- Week bar chart -->
        <div style="display:flex;align-items:flex-end;gap:5px;height:64px;margin-bottom:10px;">
          <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:3px;">
            <div class="gh-bar" style="width:100%;background:#DCFCE7;border-radius:5px 5px 0 0;height:35%;transform-origin:bottom;"></div>
            <div style="font-size:9px;color:#94A3B8;font-weight:700;">Mon</div>
          </div>
          <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:3px;">
            <div class="gh-bar" style="width:100%;background:#DCFCE7;border-radius:5px 5px 0 0;height:50%;transform-origin:bottom;"></div>
            <div style="font-size:9px;color:#94A3B8;font-weight:700;">Tue</div>
          </div>
          <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:3px;">
            <div class="gh-bar" style="width:100%;background:#16A34A;border-radius:5px 5px 0 0;height:90%;transform-origin:bottom;"></div>
            <div style="font-size:9px;color:#16A34A;font-weight:800;">Wed</div>
          </div>
          <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:3px;">
            <div class="gh-bar" style="width:100%;background:#DCFCE7;border-radius:5px 5px 0 0;height:60%;transform-origin:bottom;"></div>
            <div style="font-size:9px;color:#94A3B8;font-weight:700;">Thu</div>
          </div>
          <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:3px;">
            <div class="gh-bar" style="width:100%;background:#DCFCE7;border-radius:5px 5px 0 0;height:45%;transform-origin:bottom;"></div>
            <div style="font-size:9px;color:#94A3B8;font-weight:700;">Fri</div>
          </div>
          <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:3px;">
            <div class="gh-bar" style="width:100%;background:#DCFCE7;border-radius:5px 5px 0 0;height:72%;transform-origin:bottom;"></div>
            <div style="font-size:9px;color:#94A3B8;font-weight:700;">Sat</div>
          </div>
          <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:3px;">
            <div class="gh-bar" style="width:100%;background:#16A34A;border-radius:5px 5px 0 0;height:100%;transform-origin:bottom;"></div>
            <div style="font-size:9px;color:#16A34A;font-weight:800;">Sun</div>
          </div>
        </div>
        <!-- Stats row -->
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;padding-top:14px;border-top:1px solid #F1F5F9;">
          <div style="text-align:center;">
            <div style="font-size:18px;font-weight:900;color:#0F172A;">71</div>
            <div style="font-size:10px;color:#94A3B8;font-weight:700;">Hauls</div>
          </div>
          <div style="text-align:center;border-left:1px solid #F1F5F9;border-right:1px solid #F1F5F9;">
            <div style="font-size:18px;font-weight:900;color:#0F172A;">4.9</div>
            <div style="font-size:10px;color:#94A3B8;font-weight:700;">Rating</div>
          </div>
          <div style="text-align:center;">
            <div style="font-size:18px;font-weight:900;color:#16A34A;">98%</div>
            <div style="font-size:10px;color:#94A3B8;font-weight:700;">Accept Rate</div>
          </div>
        </div>
      </div>

      <!-- Today's haul ledger -->
      <div class="gh-card" style="background:#FFFFFF;border-radius:22px;padding:16px 18px;box-shadow:0 2px 16px rgba(15,23,42,0.07);margin-bottom:14px;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;">
          <div style="font-size:14px;font-weight:900;color:#0F172A;">5 Apr 2025</div>
          <span style="font-size:13px;font-weight:900;color:#16A34A;">₹3,450</span>
        </div>
        ${['Cotton → Warangal APMC|09:12 AM|GH-4121|₹1,683','Chilli → Khammam APMC|07:35 AM|GH-4108|₹890','Paddy → Jangaon APMC|06:50 AM|GH-4099|₹877'].map((row,i)=>{
          const [route,time,id,fare] = row.split('|');
          return `<div class="gh-card" style="display:flex;align-items:center;gap:12px;padding:10px 0;${i<2?'border-bottom:1px solid #F8FAFC;':''}">
            <div style="width:40px;height:40px;border-radius:13px;background:#F0FDF4;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="15" height="13" rx="2"/><path d="M16 8h4l3 5v4h-7V8z"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>
            </div>
            <div style="flex:1;min-width:0;">
              <div style="font-size:13px;font-weight:800;color:#0F172A;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${route}</div>
              <div style="font-size:10.5px;color:#94A3B8;font-weight:600;margin-top:1px;">${time} · #${id}</div>
            </div>
            <div style="font-size:14px;font-weight:900;color:#16A34A;flex-shrink:0;">${fare}</div>
          </div>`;
        }).join('')}
      </div>`;

    // ─── PRE-HAULS TAB ───
    const preHaulsTabHtml = `
      <div class="gh-card" style="background:#FFFFFF;border-radius:22px;padding:18px;box-shadow:0 2px 16px rgba(15,23,42,0.08);margin-bottom:14px;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px;">
          <div style="width:40px;height:40px;border-radius:13px;background:#F0FDF4;display:flex;align-items:center;justify-content:center;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          </div>
          <div>
            <div style="font-size:15px;font-weight:900;color:#0F172A;">Pre-Booked Hauls</div>
            <div style="font-size:11px;color:#64748B;">Scheduled upcoming trips</div>
          </div>
        </div>

        ${[
          {time:'Tomorrow 06:00 AM',route:'Narsampet Farm → Warangal APMC',cargo:'Cotton 40Q · ₹2,800',tag:'Confirmed'},
          {time:'6 Apr 08:30 AM',route:'Jangaon Farm → Hyderabad Market',cargo:'Tomato 80 Bags · ₹3,500',tag:'Pending'},
          {time:'7 Apr 07:00 AM',route:'Kothagudem Farm → Khammam APMC',cargo:'Chilli 25 Bags · ₹4,200',tag:'Confirmed'},
        ].map((h,i)=>`
          <div class="gh-card" style="background:#F8FAFC;border-radius:16px;padding:13px 14px;margin-bottom:10px;">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;">
              <div style="font-size:11px;color:#64748B;font-weight:700;">${h.time}</div>
              <span style="background:${h.tag==='Confirmed'?'#DCFCE7':'#FEF3C7'};color:${h.tag==='Confirmed'?'#16A34A':'#D97706'};font-size:9.5px;font-weight:900;padding:2px 8px;border-radius:100px;border:1px solid ${h.tag==='Confirmed'?'#86EFAC':'#FDE68A'};">${h.tag}</span>
            </div>
            <div style="font-size:13px;font-weight:800;color:#0F172A;margin-bottom:3px;">${h.route}</div>
            <div style="font-size:11.5px;color:#64748B;">${h.cargo}</div>
          </div>
        `).join('')}
      </div>

      <!-- Tips box -->
      <div class="gh-card" style="background:linear-gradient(135deg,#F0FDF4,#DCFCE7);border-radius:22px;padding:16px 18px;border:1px solid #BBF7D0;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          <span style="font-size:13px;font-weight:900;color:#15803D;">Peak Haul Hours Today</span>
        </div>
        <div style="font-size:12px;color:#166534;line-height:1.5;">🕕 6–9 AM: Mandi rush · Surge ×2.4<br>🕑 2–4 PM: Afternoon harvest window · Surge ×1.8<br>🌙 After 6 PM: Overnight storage hauls available</div>
      </div>`;

    // ─── MENU TAB ───
    const menuTabHtml = `
      <div class="gh-card" style="background:#FFFFFF;border-radius:22px;overflow:hidden;box-shadow:0 2px 16px rgba(15,23,42,0.08);margin-bottom:14px;">
        <!-- Profile header -->
        <div style="background:linear-gradient(135deg,#0F172A,#1E293B);padding:20px 18px;display:flex;align-items:center;gap:14px;">
          <div style="width:56px;height:56px;border-radius:18px;background:linear-gradient(135deg,#D97706,#B45309);display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:900;color:#FFFFFF;flex-shrink:0;">S</div>
          <div style="flex:1;">
            <div style="font-size:17px;font-weight:900;color:#FFFFFF;">${driverName}</div>
            <div style="font-size:11px;color:#94A3B8;margin-top:2px;">${vehicleType} · ${vehiclePlate}</div>
            <div style="display:flex;align-items:center;gap:4px;margin-top:4px;">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="#FBBF24" stroke="none"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
              <span style="font-size:12px;color:#FBBF24;font-weight:800;">4.9 · 420 hauls</span>
            </div>
          </div>
          <button onclick="switchUserRole('farmer')" class="gh-btn-press" style="background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.2);border-radius:12px;padding:8px 12px;color:#FFFFFF;font-size:11px;font-weight:800;cursor:pointer;text-align:center;">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" style="display:block;margin:0 auto 3px;"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            Farmer View
          </button>
        </div>

        <!-- Menu items -->
        ${[
          {icon:'M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2M9 5a2 2 0 0 0 2 2h2a2 2 0 0 0 2-2M9 5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2',label:'Haul History',sub:'View all your past trips'},
          {icon:'M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z',label:'Insurance & FASTag',sub:'TS 03 UB 4491 · Active'},
          {icon:'M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2|M23 21v-2a4 4 0 0 0-3-3.87|M16 3.13a4 4 0 0 1 0 7.75',label:'Refer Fellow Drivers',sub:'Earn ₹500 per referral'},
          {icon:'M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0zm-5 0a4 4 0 1 1-8 0 4 4 0 0 1 8 0z',label:'Help & Support',sub:'24/7 Driver support'},
          {icon:'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 0 0 2.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 0 0 1.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 0 0-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 0 0-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 0 0-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 0 0-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 0 0 1.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z|M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0z',label:'Settings',sub:'Account, Vehicle, Notifications'},
        ].map((item,i)=>`
          <button class="gh-btn-press" style="width:100%;display:flex;align-items:center;gap:14px;padding:15px 18px;background:none;border:none;border-bottom:${i<4?'1px solid #F8FAFC':'none'};cursor:pointer;text-align:left;">
            <div style="width:40px;height:40px;border-radius:13px;background:#F8FAFC;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#0F172A" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                ${item.icon.split('|').map(d=>`<path d="${d}"/>`).join('')}
              </svg>
            </div>
            <div style="flex:1;">
              <div style="font-size:14px;font-weight:800;color:#0F172A;">${item.label}</div>
              <div style="font-size:11px;color:#94A3B8;margin-top:1px;">${item.sub}</div>
            </div>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#CBD5E1" stroke-width="2.5" stroke-linecap="round"><polyline points="9 18 15 12 9 6"/></svg>
          </button>
        `).join('')}
      </div>

      <!-- Vehicle card -->
      <div class="gh-card" style="background:#FFFFFF;border-radius:22px;padding:16px 18px;box-shadow:0 2px 16px rgba(15,23,42,0.07);margin-bottom:14px;">
        <div style="font-size:14px;font-weight:900;color:#0F172A;margin-bottom:14px;display:flex;align-items:center;gap:8px;">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="15" height="13" rx="2"/><path d="M16 8h4l3 5v4h-7V8z"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>
          Vehicle Status
        </div>
        ${[['Diesel Level','78%','bg:#16A34A;width:78%','#16A34A'],['FASTag Balance','₹1,450','','#0F172A'],['Next Service','1,400 km','','#16A34A'],['Insurance','Valid till Dec 2025','','#0F172A']].map(([label,val,barStyle,valColor])=>`
          <div style="display:flex;justify-content:space-between;align-items:center;padding:9px 0;border-bottom:1px solid #F8FAFC;">
            <span style="font-size:12.5px;color:#64748B;">${label}</span>
            ${barStyle ? `<div style="display:flex;align-items:center;gap:8px;"><div style="width:60px;height:5px;background:#F1F5F9;border-radius:10px;overflow:hidden;"><div style="${barStyle};height:100%;border-radius:10px;"></div></div><span style="font-size:12.5px;font-weight:800;color:${valColor};">${val}</span></div>` : `<span style="font-size:12.5px;font-weight:800;color:${valColor};">${val}</span>`}
          </div>
        `).join('')}
      </div>`;

    // ─── TAB CONTENT ROUTING ───
    const tabContent = activeTab === 'earnings' ? earningsTabHtml
                     : activeTab === 'prehauls' ? preHaulsTabHtml
                     : activeTab === 'menu'     ? menuTabHtml
                     : mapTabHtml;

    // ─── BOTTOM NAV ───
    const navTabs = [
      {key:'map',     label:'Map',       svg:'<polygon points="3 11 22 2 13 21 11 13 3 11"/>'},
      {key:'prehauls',label:'Pre-Hauls', svg:'<rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>'},
      {key:'earnings',label:'Earnings',  svg:'<line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>'},
      {key:'menu',    label:'Menu',      svg:'<line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/>'},
    ];

    const bottomNav = `
      <div style="position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#FFFFFF;border-top:1px solid #F1F5F9;display:flex;z-index:9000;padding:6px 0 max(env(safe-area-inset-bottom),10px);box-shadow:0 -4px 20px rgba(15,23,42,0.08);">
        ${navTabs.map(t=>`
          <button class="gh-nav-tab ${activeTab===t.key?'active':''}" onclick="ghDriverNavTo('${t.key}')" style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;background:none;border:none;cursor:pointer;padding:6px 2px;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="${activeTab===t.key?'none':'none'}" stroke="${activeTab===t.key?'#16A34A':'#94A3B8'}" stroke-width="${activeTab===t.key?'2.5':'1.8'}" stroke-linecap="round" stroke-linejoin="round">
              ${t.svg}
            </svg>
            <span style="font-size:10px;font-weight:${activeTab===t.key?'900':'600'};color:${activeTab===t.key?'#16A34A':'#94A3B8'};">${t.label}</span>
          </button>
        `).join('')}
      </div>`;

    setTimeout(() => {
      const sc = document.getElementById('screen-container');
      if (sc) sc.style.paddingBottom = '80px';
    }, 50);

    return `
    ${sharedCSS}
    <div style="background:#F4F6F9;min-height:100%;padding-bottom:90px;font-family:-apple-system,BlinkMacSystemFont,'Plus Jakarta Sans','Inter',sans-serif;">

      <!-- ═══ TOP STATUS BAR ═══ -->
      <div style="padding:12px 16px 14px;background:#FFFFFF;border-bottom:1px solid #F1F5F9;position:sticky;top:0;z-index:100;">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
          <div style="display:flex;align-items:center;gap:10px;">
            <div style="width:40px;height:40px;border-radius:13px;background:#0F172A;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="15" height="13" rx="2"/><path d="M16 8h4l3 5v4h-7V8z"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>
            </div>
            <div>
              <div style="font-size:14.5px;font-weight:900;color:#0F172A;letter-spacing:-0.2px;">GramHaul Driver</div>
              <div style="font-size:10.5px;color:#64748B;font-weight:600;">${driverName} · ${vehiclePlate}</div>
            </div>
          </div>
          <!-- Online earnings mini badge -->
          <div style="text-align:right;">
            <div style="font-size:16px;font-weight:900;color:#16A34A;letter-spacing:-0.3px;">₹3,450</div>
            <div style="font-size:10px;color:#94A3B8;font-weight:600;">Today</div>
          </div>
        </div>
        <!-- Status pill centered -->
        <div style="display:flex;justify-content:center;">${onlinePill}</div>
      </div>

      <!-- ═══ SCROLLABLE CONTENT ═══ -->
      <div style="padding:16px 16px 0;" id="gh-driver-content">
        ${tabContent}
      </div>
    </div>

    ${bottomNav}
    `;
  },'''


# ─── NEW DRIVER JS FUNCTIONS ───
DRIVER_V6_JS = '''
/* ════════════════════════════════════════════════════════
   GRAMHAUL DRIVER COCKPIT v6.0 — True Uber Driver Grade
   Full functional nav, micro-interactions, SVG animations
   ════════════════════════════════════════════════════════ */

function ghDriverNavTo(tab) {
  localStorage.setItem('gh_driver_tab', tab);
  if (typeof openScreen === 'function') openScreen('driver_dashboard', null);
  const sc = document.getElementById('screen-container');
  if (sc) { sc.scrollTop = 0; }
}

function ghSwitchEarnTab(period) {
  // visual swap only
  const weekBtn = document.getElementById('earn-week-btn');
  const monthBtn = document.getElementById('earn-month-btn');
  if (!weekBtn || !monthBtn) return;
  if (period === 'week') {
    weekBtn.style.background = '#0F172A'; weekBtn.style.color = '#FFFFFF';
    monthBtn.style.background = 'transparent'; monthBtn.style.color = '#64748B';
  } else {
    monthBtn.style.background = '#0F172A'; monthBtn.style.color = '#FFFFFF';
    weekBtn.style.background = 'transparent'; weekBtn.style.color = '#64748B';
  }
}

function toggleGhDriverOnline() {
  const cur = (localStorage.getItem('gh_driver_online') || 'true') === 'true';
  localStorage.setItem('gh_driver_online', String(!cur));
  if (typeof openScreen === 'function') openScreen('driver_dashboard', null);
}

function driverAcceptHaulRequest(tripId, fare) {
  const trip = {
    id: tripId,
    driver: { name: 'Suresh Yadav', phone: '+91 98765 44910', phoneRaw: '919876544910', vehicle: 'Tata Ace 1.5T', plate: 'TS 03 UB 4491', rating: '4.9' },
    crop: 'Teja Chilli (25 Bags)',
    weight: '2.5 Ton',
    mandi: 'Khammam Spices APMC Mandi (Gate 1)',
    fare: fare,
    status: 'en_route',
    bookedAt: new Date().toISOString()
  };
  localStorage.setItem('nukrop_active_trip', JSON.stringify(trip));
  localStorage.setItem('gh_driver_tab', 'map');
  // Show accept animation
  const content = document.getElementById('gh-driver-content');
  if (content) {
    content.style.opacity = '0';
    content.style.transform = 'scale(0.97)';
    content.style.transition = 'all 0.2s';
    setTimeout(() => { if (typeof openScreen === 'function') openScreen('driver_dashboard', null); }, 200);
  } else {
    if (typeof openScreen === 'function') openScreen('driver_dashboard', null);
  }
}

function declineHaulRequest(tripId) {
  const cards = document.querySelectorAll('#gh-available-hauls .gh-card');
  // Find and animate out the declined card
  if (cards.length > 0) {
    const firstCard = cards[0];
    firstCard.style.transition = 'all 0.25s cubic-bezier(0.4,0,1,1)';
    firstCard.style.opacity = '0';
    firstCard.style.transform = 'translateX(-30px)';
    setTimeout(() => {
      if (firstCard.parentNode) firstCard.parentNode.removeChild(firstCard);
    }, 250);
  }
}

function driverDeclineHaul() {
  localStorage.removeItem('nukrop_active_trip');
  localStorage.setItem('gh_driver_tab', 'map');
  if (typeof openScreen === 'function') openScreen('driver_dashboard', null);
}

function driverShowPaymentScreen(tripId, fare) {
  const fareNum = parseInt(String(fare).replace(/[^0-9]/g, '')) || 1850;
  const baseFare = Math.round(fareNum * 0.70);
  const surgeFare = fareNum - baseFare;
  const totalWithWait = fareNum + 120;

  const modal = document.createElement('div');
  modal.id = 'gh-driver-payment-modal';
  modal.style.cssText = 'position:fixed;inset:0;background:rgba(15,23,42,0.60);z-index:99999;backdrop-filter:blur(5px);display:flex;align-items:flex-end;justify-content:center;animation:fadeIn 0.2s;';
  modal.innerHTML = `
    <div style="background:#FFFFFF;width:100%;max-width:430px;border-radius:28px 28px 0 0;padding:0 0 24px;box-shadow:0 -12px 48px rgba(0,0,0,0.20);animation:slideUp 0.28s cubic-bezier(0.16,1,0.3,1);">
      <!-- Handle -->
      <div style="width:40px;height:4px;background:#E2E8F0;border-radius:10px;margin:14px auto 20px;"></div>

      <!-- Header -->
      <div style="padding:0 20px 16px;border-bottom:1px solid #F8FAFC;">
        <div style="display:flex;align-items:center;gap:12px;">
          <div style="width:44px;height:44px;border-radius:14px;background:#F0FDF4;display:flex;align-items:center;justify-content:center;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2" stroke-linecap="round"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
          </div>
          <div>
            <div style="font-size:11px;color:#94A3B8;font-weight:700;text-transform:uppercase;letter-spacing:0.8px;">Payment from Farmer</div>
            <div style="font-size:15px;font-weight:900;color:#0F172A;">UPI / Cash Collection</div>
          </div>
        </div>
      </div>

      <!-- Amount Hero -->
      <div style="padding:20px 20px 0;text-align:center;">
        <div style="font-size:11px;color:#94A3B8;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Collect from Farmer</div>
        <div style="font-size:52px;font-weight:900;color:#0F172A;letter-spacing:-2px;line-height:1;">₹${fareNum.toLocaleString('en-IN')}</div>
        <div style="display:flex;justify-content:center;gap:8px;margin-top:10px;">
          <span style="background:#DCFCE7;color:#16A34A;font-size:10.5px;font-weight:800;padding:4px 10px;border-radius:8px;">₹${baseFare} Base Fare</span>
          <span style="background:#FEF3C7;color:#D97706;font-size:10.5px;font-weight:800;padding:4px 10px;border-radius:8px;">₹${surgeFare} Surge</span>
        </div>
      </div>

      <!-- Waiting fee stepper -->
      <div style="margin:16px 20px 0;background:#F8FAFC;border-radius:16px;padding:14px 16px;display:flex;justify-content:space-between;align-items:center;">
        <div>
          <div style="font-size:13px;font-weight:800;color:#0F172A;">Loading Wait Time</div>
          <div style="font-size:11px;color:#64748B;margin-top:1px;">+12 min · Loading help</div>
        </div>
        <div style="display:flex;align-items:center;gap:10px;">
          <button onclick="this.nextSibling.textContent = '₹' + Math.max(0, parseInt(this.nextSibling.textContent.replace('₹','')) - 30)" style="width:30px;height:30px;border-radius:50%;border:1.5px solid #E2E8F0;background:#FFFFFF;font-size:18px;font-weight:700;cursor:pointer;display:flex;align-items:center;justify-content:center;color:#64748B;line-height:1;">−</button>
          <span style="font-size:15px;font-weight:900;color:#0F172A;min-width:44px;text-align:center;">₹120</span>
          <button onclick="this.previousSibling.textContent = '₹' + (parseInt(this.previousSibling.textContent.replace('₹','')) + 30)" style="width:30px;height:30px;border-radius:50%;border:1.5px solid #16A34A;background:#16A34A;font-size:18px;font-weight:700;cursor:pointer;display:flex;align-items:center;justify-content:center;color:#FFFFFF;line-height:1;">+</button>
        </div>
      </div>

      <!-- Total -->
      <div style="margin:12px 20px 0;display:flex;justify-content:space-between;align-items:center;">
        <span style="font-size:13px;color:#64748B;">You will earn total</span>
        <span style="font-size:18px;font-weight:900;color:#16A34A;">₹${totalWithWait.toLocaleString('en-IN')} →</span>
      </div>

      <!-- CTA buttons -->
      <div style="padding:16px 20px 0;">
        <button onclick="driverCompleteHaulTrip('${tripId}', '${fareNum}')" style="width:100%;height:56px;border-radius:18px;background:#16A34A;color:#FFFFFF;font-size:16px;font-weight:900;border:none;cursor:pointer;box-shadow:0 8px 24px rgba(22,163,74,0.40);display:flex;align-items:center;justify-content:center;gap:10px;margin-bottom:10px;transition:transform 0.15s;" onmousedown="this.style.transform='scale(0.97)'" onmouseup="this.style.transform=''" ontouchstart="this.style.transform='scale(0.97)'" ontouchend="this.style.transform=''">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
          Complete Haul & Collect
        </button>
        <button onclick="document.getElementById('gh-driver-payment-modal').remove()" style="width:100%;height:46px;border-radius:14px;background:#F8FAFC;border:1.5px solid #E2E8F0;color:#64748B;font-size:13.5px;font-weight:700;cursor:pointer;">
          Back to Active Trip
        </button>
      </div>
    </div>
  `;
  document.body.appendChild(modal);
  modal.addEventListener('click', (e) => { if (e.target === modal) modal.remove(); });
}
'''


def apply_driver_v6(filepath):
    print(f'\nUpgrading {filepath} → Driver v6.0...')
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # ── 1. Remove old driver_dashboard view ──
    import re
    dd_m = re.search(r'driver_dashboard\s*:\s*\(\)\s*=>\s*\{', text)
    pr_m = re.search(r'\n  profile\s*:\s*\(\)\s*=>', text)

    if not dd_m or not pr_m:
        print('  ✗ Could not find driver_dashboard / profile view boundary')
        return False

    dd_start = dd_m.start()
    pr_start = pr_m.start()

    text = text[:dd_start] + DRIVER_V6_VIEW.strip() + '\n\n  ' + text[pr_start:].lstrip()
    print('  ✓ Replaced driver_dashboard view (v6.0)')

    # ── 2. Remove old Driver Cockpit JS block ──
    marker = '/* ════════════════════════════════════════════════'
    idx = text.rfind(marker)   # last occurrence
    if idx != -1:
        last_script = text.rfind('</script>')
        text = text[:idx] + text[last_script:]
        print('  ✓ Removed old Driver JS block')

    # ── 3. Inject new Driver v6 JS ──
    last_script_idx = text.rfind('</script>')
    text = text[:last_script_idx] + '\n\n' + DRIVER_V6_JS.strip() + '\n\n' + text[last_script_idx:]
    print('  ✓ Injected Driver JS v6.0')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f'  ✓ Saved {filepath}')
    return True


if __name__ == '__main__':
    ok1 = apply_driver_v6('app/src/main/assets/index.html')
    ok2 = apply_driver_v6('nukrop_emulator.html')
    if ok1 and ok2:
        print('\n✅ Driver v6.0 upgrade complete!')
    else:
        print('\n⚠️  Check errors above')
