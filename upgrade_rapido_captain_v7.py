import sys, re
sys.stdout.reconfigure(encoding='utf-8')

# ═══════════════════════════════════════════════════════════════════════
#  NuKropAI GramHaul Driver App v7.0
#  UI: Rapido Captain + Yatri Saathi exact pattern
#  Colors: #1A1A1A dark, #FFCA20 yellow, #FFFFFF white
#  Layout: Fullscreen map home, bottom-sheet request, 3-tab bottom nav
# ═══════════════════════════════════════════════════════════════════════

DRIVER_V7_VIEW = r"""driver_dashboard: () => {
    const alertBanner = document.getElementById('nukrop-alert-banner');
    if (alertBanner) alertBanner.style.display = 'none';

    let activeTrip = null;
    try { activeTrip = JSON.parse(localStorage.getItem('nukrop_active_trip') || 'null'); } catch(e) {}

    const driverName   = localStorage.getItem('nukrop_driver_name')    || 'Suresh Yadav';
    const vehiclePlate = localStorage.getItem('nukrop_driver_plate')   || 'TS 03 UB 4491';
    const vehicleType  = localStorage.getItem('nukrop_driver_vehicle') || 'Tata Ace Gold 1.5T';
    const isOnline     = (localStorage.getItem('gh_driver_online') || 'true') === 'true';
    const activeTab    = localStorage.getItem('gh_driver_tab') || 'map';

    const tripId      = activeTrip?.id      || 'GH-4192';
    const tripCrop    = activeTrip ? `${activeTrip.crop} (${activeTrip.weight})` : 'Cotton (పత్తి) · 40 Quintals';
    const tripPickup  = (typeof currentGramhaulFarmAddress!=='undefined'&&activeTrip) ? currentGramhaulFarmAddress : "Ramesh Rao's Farm, Sy.No 142/A, Narsampet Rural";
    const tripLandmark= (typeof currentGramhaulFarmLandmark!=='undefined') ? currentGramhaulFarmLandmark : 'Near Big Banyan Tree & Power Transformer';
    const tripDrop    = activeTrip?.mandi  || 'Warangal Enamamula APMC Yard (Gate 3)';
    const tripFare    = activeTrip?.fare   || '1,850';

    // ─── STYLES ───────────────────────────────────────────────────────
    const CSS = `<style id="rapido-style">
      :root { --r-yellow:#FFCA20; --r-dark:#1A1A1A; --r-card:#FFFFFF; --r-bg:#F3F4F6; }
      @keyframes rapido-slideup {
        from { transform:translateY(100%); opacity:0; }
        to   { transform:translateY(0);   opacity:1; }
      }
      @keyframes rapido-fadein { from{opacity:0} to{opacity:1} }
      @keyframes rapido-pulse  {
        0%,100% { box-shadow:0 0 0 0 rgba(255,202,32,0.5); }
        50%      { box-shadow:0 0 0 14px rgba(255,202,32,0); }
      }
      @keyframes rapido-spin {
        0%   { stroke-dashoffset:80; }
        100% { stroke-dashoffset:0;  }
      }
      @keyframes rapido-wiggle {
        0%,100%{transform:rotate(0deg)} 25%{transform:rotate(-5deg)} 75%{transform:rotate(5deg)}
      }
      @keyframes barpop {
        from{transform:scaleY(0);opacity:0} to{transform:scaleY(1);opacity:1}
      }
      .r-card { background:#FFFFFF; border-radius:20px; box-shadow:0 2px 14px rgba(0,0,0,0.07); animation:rapido-fadein 0.25s ease both; }
      .r-card:nth-child(2){animation-delay:.05s} .r-card:nth-child(3){animation-delay:.10s}
      .r-sheet { animation:rapido-slideup 0.32s cubic-bezier(0.16,1,0.3,1) both; }
      .r-btn:active { transform:scale(0.95); transition:transform 0.1s; }
      .r-nav-item { transition:color 0.15s, transform 0.15s; }
      .r-nav-item:active { transform:scale(0.88); }
      .r-bar { transform-origin:bottom; animation:barpop 0.5s cubic-bezier(0.34,1.56,0.64,1) both; }
      .r-bar:nth-child(1){animation-delay:.00s} .r-bar:nth-child(2){animation-delay:.06s}
      .r-bar:nth-child(3){animation-delay:.12s} .r-bar:nth-child(4){animation-delay:.18s}
      .r-bar:nth-child(5){animation-delay:.24s} .r-bar:nth-child(6){animation-delay:.30s}
      .r-bar:nth-child(7){animation-delay:.36s}
      .r-online-pulse { animation:rapido-pulse 2s infinite; }
      .r-accept-btn {
        width:100%; height:58px; background:var(--r-yellow); color:var(--r-dark);
        font-size:17px; font-weight:900; border:none; border-radius:16px; cursor:pointer;
        display:flex; align-items:center; justify-content:center; gap:10px;
        box-shadow:0 6px 20px rgba(255,202,32,0.40); letter-spacing:-0.2px;
        transition:transform 0.15s, box-shadow 0.15s;
      }
      .r-accept-btn:active { transform:scale(0.97); box-shadow:0 3px 10px rgba(255,202,32,0.30); }
      .shimmer {
        background:linear-gradient(90deg,#F3F4F6 25%,#E9EAEC 50%,#F3F4F6 75%);
        background-size:400px 100%; animation:rapido-fadein 1.5s linear infinite alternate;
        border-radius:8px;
      }
    </style>`;

    // ═══════════════════════════════════════════════════════════════
    //  TAB: MAP (Home) — Rapido Captain main screen
    // ═══════════════════════════════════════════════════════════════
    const mapTab = `
    <!-- ── Fullscreen map canvas ── -->
    <div style="position:relative;width:100%;height:calc(100vh - 120px);min-height:480px;background:#E5EFE5;overflow:hidden;">

      <!-- OSM-style map grid -->
      <svg style="position:absolute;inset:0;width:100%;height:100%;" preserveAspectRatio="none">
        <defs>
          <pattern id="rmap-grid" width="40" height="40" patternUnits="userSpaceOnUse">
            <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#CDD8CD" stroke-width="0.8"/>
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="#EBF2EB"/>
        <rect width="100%" height="100%" fill="url(#rmap-grid)"/>
        <!-- Roads -->
        <line x1="0" y1="45%" x2="100%" y2="45%" stroke="#FFFFFF" stroke-width="12" opacity="0.9"/>
        <line x1="0" y1="60%" x2="100%" y2="60%" stroke="#FFFFFF" stroke-width="7" opacity="0.8"/>
        <line x1="30%" y1="0" x2="30%" y2="100%" stroke="#FFFFFF" stroke-width="10" opacity="0.9"/>
        <line x1="65%" y1="0" x2="65%" y2="100%" stroke="#FFFFFF" stroke-width="6" opacity="0.8"/>
        <line x1="10%" y1="0" x2="55%" y2="100%" stroke="#FFFFFF" stroke-width="5" opacity="0.7"/>
        <!-- Blocks -->
        <rect x="5%" y="5%" width="22%" height="35%" rx="3" fill="#D8E8D8" opacity="0.6"/>
        <rect x="33%" y="5%" width="28%" height="35%" rx="3" fill="#D8E8D8" opacity="0.6"/>
        <rect x="67%" y="5%" width="30%" height="35%" rx="3" fill="#D8E8D8" opacity="0.6"/>
        <rect x="5%" y="48%" width="22%" height="45%" rx="3" fill="#D8E8D8" opacity="0.6"/>
        <rect x="33%" y="48%" width="28%" height="45%" rx="3" fill="#D8E8D8" opacity="0.6"/>
        <rect x="67%" y="48%" width="30%" height="45%" rx="3" fill="#D8E8D8" opacity="0.6"/>
      </svg>

      <!-- Top map controls strip -->
      <div style="position:absolute;top:14px;left:14px;right:14px;display:flex;justify-content:space-between;align-items:flex-start;z-index:10;">
        <!-- Driver info pill -->
        <div style="background:#FFFFFF;border-radius:14px;padding:10px 14px;box-shadow:0 3px 12px rgba(0,0,0,0.12);display:flex;align-items:center;gap:10px;">
          <div style="width:36px;height:36px;border-radius:11px;background:var(--r-dark);display:flex;align-items:center;justify-content:center;font-size:16px;font-weight:900;color:var(--r-yellow);">S</div>
          <div>
            <div style="font-size:13px;font-weight:900;color:var(--r-dark);letter-spacing:-0.2px;">${driverName}</div>
            <div style="font-size:10px;color:#6B7280;font-weight:600;">${vehiclePlate}</div>
          </div>
        </div>
        <!-- Today earnings badge -->
        <div style="background:var(--r-dark);border-radius:14px;padding:10px 14px;box-shadow:0 3px 12px rgba(0,0,0,0.20);">
          <div style="font-size:10px;color:#9CA3AF;font-weight:700;text-align:center;">TODAY</div>
          <div style="font-size:16px;font-weight:900;color:var(--r-yellow);letter-spacing:-0.3px;">₹3,450</div>
        </div>
      </div>

      <!-- Map action buttons (right side) -->
      <div style="position:absolute;right:14px;bottom:${activeTrip ? '290' : '200'}px;display:flex;flex-direction:column;gap:8px;z-index:10;">
        <button class="r-btn" onclick="driverOpenGpsNav(17.9689,79.5941)" style="width:44px;height:44px;background:#FFFFFF;border:none;border-radius:13px;display:flex;align-items:center;justify-content:center;box-shadow:0 3px 10px rgba(0,0,0,0.12);cursor:pointer;">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--r-dark)" stroke-width="2.5" stroke-linecap="round"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg>
        </button>
        <button class="r-btn" style="width:44px;height:44px;background:#FFFFFF;border:none;border-radius:13px;display:flex;align-items:center;justify-content:center;box-shadow:0 3px 10px rgba(0,0,0,0.12);cursor:pointer;">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--r-dark)" stroke-width="2.5" stroke-linecap="round"><circle cx="12" cy="12" r="3"/><path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83"/></svg>
        </button>
      </div>

      <!-- Driver truck marker (center) -->
      <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);">
        <svg width="48" height="48" viewBox="0 0 48 48">
          <circle cx="24" cy="24" r="22" fill="var(--r-yellow)" opacity="0.2"/>
          <circle cx="24" cy="24" r="14" fill="var(--r-yellow)"/>
          <g transform="translate(12,12)">
            <rect x="0" y="5" width="14" height="10" rx="2" fill="var(--r-dark)"/>
            <path d="M14 8h6l4 5v3h-10V8z" fill="var(--r-dark)"/>
            <circle cx="4" cy="17" r="2.5" fill="var(--r-dark)" stroke="var(--r-yellow)" stroke-width="1.5"/>
            <circle cx="16" cy="17" r="2.5" fill="var(--r-dark)" stroke="var(--r-yellow)" stroke-width="1.5"/>
          </g>
        </svg>
      </div>

      ${activeTrip ? `
      <!-- ── ACTIVE TRIP BOTTOM SHEET ── -->
      <div class="r-sheet" style="position:absolute;bottom:0;left:0;right:0;background:#FFFFFF;border-radius:22px 22px 0 0;padding:0 0 16px;box-shadow:0 -8px 32px rgba(0,0,0,0.15);z-index:20;">
        <div style="width:36px;height:4px;background:#E5E7EB;border-radius:10px;margin:12px auto 14px;"></div>

        <!-- Status stepper -->
        <div style="padding:0 18px 12px;border-bottom:1px solid #F3F4F6;">
          <div style="display:flex;align-items:center;justify-content:space-between;">
            ${['En Route','Arrived','Loaded','Delivered'].map((step,i)=>`
              <div style="display:flex;flex-direction:column;align-items:center;gap:4px;flex:1;">
                <div style="width:${i===0?'28':'22'}px;height:${i===0?'28':'22'}px;border-radius:50%;background:${i===0?'var(--r-yellow)':'#F3F4F6'};border:2px solid ${i===0?'var(--r-yellow)':'#E5E7EB'};display:flex;align-items:center;justify-content:center;">
                  ${i===0?`<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="var(--r-dark)" stroke-width="3"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg>`:i===3?`<svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#9CA3AF" stroke-width="2.5"><polyline points="4 15 8 19 20 7"/></svg>`:`<div style="width:6px;height:6px;border-radius:50%;background:#D1D5DB;"></div>`}
                </div>
                <div style="font-size:8.5px;font-weight:${i===0?'800':'600'};color:${i===0?'var(--r-dark)':'#9CA3AF'};text-align:center;">${step}</div>
              </div>
              ${i<3?`<div style="height:1.5px;flex:1;background:${i===0?'var(--r-yellow)':'#E5E7EB'};margin-bottom:16px;"></div>`:''}
            `).join('')}
          </div>
        </div>

        <!-- Farmer + trip info -->
        <div style="padding:12px 18px;">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
            <div style="display:flex;align-items:center;gap:10px;">
              <div style="width:40px;height:40px;border-radius:13px;background:#FFFBEB;display:flex;align-items:center;justify-content:center;font-size:17px;font-weight:900;color:var(--r-dark);">R</div>
              <div>
                <div style="font-size:13.5px;font-weight:900;color:var(--r-dark);">Ramesh Rao</div>
                <div style="display:flex;align-items:center;gap:3px;">
                  <svg width="10" height="10" viewBox="0 0 24 24" fill="var(--r-yellow)" stroke="none"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                  <span style="font-size:10.5px;color:#6B7280;font-weight:700;">4.8 · Farmer</span>
                </div>
              </div>
            </div>
            <div style="text-align:right;">
              <div style="font-size:20px;font-weight:900;color:var(--r-dark);letter-spacing:-0.4px;">₹${tripFare}</div>
              <div style="font-size:10px;color:#6B7280;">Haul Fare</div>
            </div>
          </div>

          <!-- Route -->
          <div style="background:#F9FAFB;border-radius:14px;padding:10px 12px;margin-bottom:12px;">
            <div style="display:flex;gap:10px;align-items:stretch;">
              <div style="display:flex;flex-direction:column;align-items:center;gap:0;padding-top:2px;">
                <div style="width:9px;height:9px;border-radius:50%;background:#22C55E;"></div>
                <div style="width:1.5px;flex:1;background:linear-gradient(#22C55E,#EF4444);margin:3px 0;"></div>
                <div style="width:9px;height:9px;border-radius:50%;background:#EF4444;"></div>
              </div>
              <div style="flex:1;min-width:0;">
                <div style="margin-bottom:10px;">
                  <div style="font-size:10px;color:#9CA3AF;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:2px;">PICKUP (GPS)</div>
                  <div style="font-size:12.5px;font-weight:800;color:var(--r-dark);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${tripPickup}</div>
                </div>
                <div>
                  <div style="font-size:10px;color:#9CA3AF;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:2px;">DROP MANDI</div>
                  <div style="font-size:12.5px;font-weight:800;color:var(--r-dark);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${tripDrop}</div>
                </div>
              </div>
            </div>
            <div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:8px;padding-top:8px;border-top:1px solid #F0F0F0;">
              <span style="background:#FFFBEB;border:1px solid #FDE68A;border-radius:7px;padding:3px 8px;font-size:10px;font-weight:800;color:#92400E;">🌾 ${tripCrop}</span>
              <span style="background:#F0FDF4;border:1px solid #86EFAC;border-radius:7px;padding:3px 8px;font-size:10px;font-weight:800;color:#166534;">✓ Zero Platform Fee</span>
            </div>
          </div>

          <!-- Action buttons -->
          <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:10px;">
            <button onclick="driverCallFarmer('+919440122910')" class="r-btn" style="height:44px;background:#F9FAFB;border:1.5px solid #E5E7EB;border-radius:13px;font-size:11px;font-weight:800;color:var(--r-dark);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;cursor:pointer;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#22C55E" stroke-width="2.5" stroke-linecap="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12 19.79 19.79 0 0 1 1.61 3.4 2 2 0 0 1 3.6 1.2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.82a16 16 0 0 0 6 6l.91-.91a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
              Call
            </button>
            <button onclick="messageGramhaulDriver()" class="r-btn" style="height:44px;background:#F9FAFB;border:1.5px solid #E5E7EB;border-radius:13px;font-size:11px;font-weight:800;color:var(--r-dark);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;cursor:pointer;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2.5" stroke-linecap="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
              Chat
            </button>
            <button onclick="driverOpenGpsNav(17.9689,79.5941)" class="r-btn" style="height:44px;background:#FFFBEB;border:1.5px solid #FDE68A;border-radius:13px;font-size:11px;font-weight:800;color:var(--r-dark);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;cursor:pointer;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2.5" stroke-linecap="round"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg>
              Navigate
            </button>
          </div>
          <button onclick="driverShowPaymentScreen('${tripId}','${tripFare}')" class="r-btn" style="width:100%;height:52px;background:var(--r-dark);color:#FFFFFF;border:none;border-radius:15px;font-size:15px;font-weight:900;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:10px;">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--r-yellow)" stroke-width="2.5" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
            Mark as Delivered
          </button>
        </div>
      </div>
      ` : `
      <!-- ── HAUL REQUEST BOTTOM SHEET (Rapido-style slide-up) ── -->
      <div id="gh-request-sheet" class="r-sheet" style="position:absolute;bottom:0;left:0;right:0;background:#FFFFFF;border-radius:22px 22px 0 0;padding:0 0 20px;box-shadow:0 -8px 32px rgba(0,0,0,0.15);z-index:20;">
        <div style="width:36px;height:4px;background:#E5E7EB;border-radius:10px;margin:12px auto 0;"></div>

        <!-- Request incoming -->
        <div style="padding:14px 18px 0;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
            <div style="font-size:11px;font-weight:800;color:#6B7280;text-transform:uppercase;letter-spacing:0.8px;">New Haul Request</div>
            <!-- Countdown timer ring -->
            <div style="position:relative;width:38px;height:38px;">
              <svg width="38" height="38" viewBox="0 0 38 38" style="transform:rotate(-90deg);">
                <circle cx="19" cy="19" r="16" fill="none" stroke="#F3F4F6" stroke-width="3"/>
                <circle cx="19" cy="19" r="16" fill="none" stroke="var(--r-yellow)" stroke-width="3" stroke-dasharray="100" stroke-dashoffset="25" style="animation:rapido-spin 15s linear forwards;"/>
              </svg>
              <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:900;color:var(--r-dark);">15s</div>
            </div>
          </div>

          <!-- ETA + Fare Hero Row -->
          <div style="display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:14px;">
            <div>
              <div style="font-size:30px;font-weight:900;color:var(--r-dark);letter-spacing:-0.8px;line-height:1.1;">5 min · 5.8 km</div>
              <div style="font-size:12px;color:#6B7280;font-weight:600;margin-top:3px;">to Farmer Pickup</div>
            </div>
            <div style="text-align:right;">
              <div style="font-size:26px;font-weight:900;color:var(--r-dark);letter-spacing:-0.6px;">₹4,200</div>
              <div style="background:var(--r-yellow);border-radius:6px;padding:2px 8px;font-size:10px;font-weight:900;color:var(--r-dark);margin-top:3px;display:inline-block;">×2.4 SURGE</div>
            </div>
          </div>

          <!-- Route -->
          <div style="background:#F9FAFB;border-radius:14px;padding:12px 14px;margin-bottom:12px;">
            <div style="display:flex;gap:10px;align-items:stretch;">
              <div style="display:flex;flex-direction:column;align-items:center;padding-top:2px;flex-shrink:0;">
                <div style="width:10px;height:10px;border-radius:50%;background:#22C55E;"></div>
                <div style="width:1.5px;height:26px;background:linear-gradient(#22C55E,#EF4444);margin:3px 0;"></div>
                <div style="width:10px;height:10px;border-radius:50%;background:#EF4444;"></div>
              </div>
              <div style="flex:1;min-width:0;">
                <div style="margin-bottom:10px;">
                  <div style="font-size:10px;color:#9CA3AF;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:2px;">Farmer Pickup (GPS)</div>
                  <div style="font-size:13px;font-weight:800;color:var(--r-dark);">K. Anjaiah Farm, Hasanparthy</div>
                  <div style="font-size:11px;color:#9CA3AF;">5.8 km · ~12 min drive</div>
                </div>
                <div>
                  <div style="font-size:10px;color:#9CA3AF;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:2px;">Drop APMC Mandi</div>
                  <div style="font-size:13px;font-weight:800;color:var(--r-dark);">Khammam Spices APMC Mandi</div>
                  <div style="font-size:11px;color:#9CA3AF;">Gate 1 · 28 km total</div>
                </div>
              </div>
            </div>
            <div style="display:flex;gap:6px;flex-wrap:wrap;padding-top:8px;margin-top:8px;border-top:1px solid #F0F0F0;">
              <span style="background:#FFFBEB;border:1px solid #FDE68A;border-radius:7px;padding:3px 8px;font-size:10px;font-weight:800;color:#92400E;">🌶️ Teja Chilli · 2.5 Ton</span>
              <span style="background:#F0FDF4;border:1px solid #86EFAC;border-radius:7px;padding:3px 8px;font-size:10px;font-weight:800;color:#166534;">⚡ No Commission</span>
              <span style="background:#EFF6FF;border:1px solid #BFDBFE;border-radius:7px;padding:3px 8px;font-size:10px;font-weight:800;color:#1E40AF;">👤 Anjaiah</span>
            </div>
          </div>

          <!-- Accept / Decline -->
          <div style="display:grid;grid-template-columns:auto 1fr;gap:10px;align-items:center;">
            <button onclick="declineHaulRequest('GH-8824')" class="r-btn" style="height:54px;width:56px;background:#F3F4F6;border:1.5px solid #E5E7EB;border-radius:15px;display:flex;align-items:center;justify-content:center;cursor:pointer;">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#6B7280" stroke-width="2.5" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
            <button onclick="driverAcceptHaulRequest('GH-8824','4200')" class="r-accept-btn">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="var(--r-dark)" stroke-width="3" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
              Accept Haul · ₹4,200
            </button>
          </div>
        </div>
      </div>

      <!-- ── ONLINE/OFFLINE big pill (Rapido style — bottom, above request sheet) ── -->
      <div style="position:absolute;bottom:${isOnline ? '230' : '20'}px;left:50%;transform:translateX(-50%);z-index:25;">
        <button class="r-btn ${isOnline ? 'r-online-pulse' : ''}" onclick="toggleGhDriverOnline()" style="display:flex;align-items:center;gap:12px;background:${isOnline ? 'var(--r-dark)' : '#FFFFFF'};border:2px solid ${isOnline ? 'var(--r-yellow)' : '#E5E7EB'};border-radius:100px;padding:12px 22px 12px 14px;box-shadow:0 6px 24px rgba(0,0,0,0.20);cursor:pointer;">
          <div style="width:38px;height:38px;border-radius:50%;background:${isOnline ? 'var(--r-yellow)' : '#F3F4F6'};display:flex;align-items:center;justify-content:center;">
            ${isOnline
              ? `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--r-dark)" stroke-width="3" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>`
              : `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#6B7280" stroke-width="2.5" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>`
            }
          </div>
          <div style="text-align:left;">
            <div style="font-size:15px;font-weight:900;color:${isOnline ? 'var(--r-yellow)' : 'var(--r-dark)'};letter-spacing:-0.2px;">${isOnline ? 'On Duty' : 'Go Online'}</div>
            <div style="font-size:10.5px;color:${isOnline ? '#9CA3AF' : '#6B7280'};font-weight:600;">${isOnline ? 'Tap to go offline' : 'Tap to start earning'}</div>
          </div>
        </button>
      </div>
      `}
    </div>`;

    // ═══════════════════════════════════════════════════════════════
    //  TAB: EARNINGS — Rapido Captain earnings screen
    // ═══════════════════════════════════════════════════════════════
    const earningsTab = `
    <div style="background:var(--r-bg);min-height:100%;padding:16px 16px 20px;">
      <!-- Week earnings hero -->
      <div class="r-card" style="padding:20px 18px;margin-bottom:14px;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
          <div>
            <div style="font-size:11px;color:#9CA3AF;font-weight:700;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:4px;">30 Mar – 5 Apr 2025</div>
            <div style="font-size:38px;font-weight:900;color:var(--r-dark);letter-spacing:-1.5px;line-height:1;">₹60,665</div>
          </div>
          <div style="display:flex;flex-direction:column;gap:6px;text-align:right;">
            <div style="background:#F0FDF4;border-radius:10px;padding:6px 12px;">
              <div style="font-size:10px;color:#9CA3AF;font-weight:700;">Redeemable</div>
              <div style="font-size:16px;font-weight:900;color:#16A34A;">₹8,625</div>
            </div>
          </div>
        </div>
        <!-- 7-day bar chart -->
        <div style="display:flex;align-items:flex-end;gap:5px;height:72px;">
          ${[
            ['Mon','35%','#E5E7EB'],['Tue','52%','#E5E7EB'],['Wed','90%','var(--r-yellow)'],
            ['Thu','62%','#E5E7EB'],['Fri','47%','#E5E7EB'],['Sat','75%','#E5E7EB'],['Sun','100%','var(--r-yellow)']
          ].map(([day,h,bg])=>`
            <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:4px;">
              <div class="r-bar" style="width:100%;height:${h};background:${bg};border-radius:5px 5px 0 0;transform-origin:bottom;"></div>
              <div style="font-size:9px;font-weight:${bg.includes('yellow')?'900':'600'};color:${bg.includes('yellow')?'var(--r-dark)':'#9CA3AF'};">${day}</div>
            </div>
          `).join('')}
        </div>
        <!-- Stats -->
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:0;padding-top:14px;margin-top:14px;border-top:1px solid #F3F4F6;">
          <div style="text-align:center;padding:4px 0;">
            <div style="font-size:20px;font-weight:900;color:var(--r-dark);">71</div>
            <div style="font-size:10px;color:#9CA3AF;font-weight:700;">Hauls</div>
          </div>
          <div style="text-align:center;padding:4px 0;border-left:1px solid #F3F4F6;border-right:1px solid #F3F4F6;">
            <div style="font-size:20px;font-weight:900;color:var(--r-dark);">4.9</div>
            <div style="font-size:10px;color:#9CA3AF;font-weight:700;">Rating</div>
          </div>
          <div style="text-align:center;padding:4px 0;">
            <div style="font-size:20px;font-weight:900;color:#16A34A;">98%</div>
            <div style="font-size:10px;color:#9CA3AF;font-weight:700;">Accept Rate</div>
          </div>
        </div>
      </div>

      <!-- Incentives card -->
      <div class="r-card" style="padding:16px 18px;margin-bottom:14px;">
        <div style="font-size:14px;font-weight:900;color:var(--r-dark);margin-bottom:12px;display:flex;align-items:center;gap:8px;">
          <div style="width:28px;height:28px;border-radius:9px;background:#FFFBEB;display:flex;align-items:center;justify-content:center;">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="var(--r-yellow)" stroke="none"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
          </div>
          Today's Incentives
        </div>
        ${[
          ['Mandi Rush Bonus','6–9 AM Surge','₹320','earned'],
          ['10 Hauls Target','7 / 10 done','₹500','locked'],
          ['Loading Help Bonus','Per trip extra','₹120','earned'],
        ].map(([title,sub,amt,status])=>`
          <div style="display:flex;align-items:center;gap:12px;padding:9px 0;border-bottom:1px solid #F9FAFB;">
            <div style="flex:1;">
              <div style="font-size:13px;font-weight:800;color:var(--r-dark);">${title}</div>
              <div style="font-size:11px;color:#9CA3AF;">${sub}</div>
            </div>
            <div style="text-align:right;">
              <div style="font-size:14px;font-weight:900;color:${status==='earned'?'#16A34A':'#9CA3AF'};">${amt}</div>
              <div style="font-size:10px;background:${status==='earned'?'#DCFCE7':'#F3F4F6'};color:${status==='earned'?'#16A34A':'#9CA3AF'};border-radius:5px;padding:1px 6px;display:inline-block;font-weight:700;">${status}</div>
            </div>
          </div>
        `).join('')}
      </div>

      <!-- Trip ledger -->
      <div class="r-card" style="padding:16px 18px;margin-bottom:14px;">
        <div style="font-size:14px;font-weight:900;color:var(--r-dark);margin-bottom:12px;">Today's Haul Log</div>
        ${[
          ['Cotton → Warangal APMC','09:12 AM','GH-4121','₹1,683','#DCFCE7','#16A34A'],
          ['Chilli → Khammam APMC','07:35 AM','GH-4108','₹890','#FEF3C7','#D97706'],
          ['Paddy → Jangaon APMC','06:50 AM','GH-4099','₹877','#DCFCE7','#16A34A'],
        ].map(([route,time,id,fare,bg,color],i)=>`
          <div class="r-card" style="display:flex;align-items:center;gap:12px;padding:10px 0;${i<2?'border-bottom:1px solid #F9FAFB;':''}">
            <div style="width:40px;height:40px;border-radius:13px;background:${bg};display:flex;align-items:center;justify-content:center;flex-shrink:0;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="${color}" stroke-width="1.8" stroke-linecap="round"><rect x="1" y="3" width="15" height="13" rx="2"/><path d="M16 8h4l3 5v4h-7V8z"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>
            </div>
            <div style="flex:1;min-width:0;">
              <div style="font-size:13px;font-weight:800;color:var(--r-dark);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${route}</div>
              <div style="font-size:10.5px;color:#9CA3AF;font-weight:600;">${time} · #${id}</div>
            </div>
            <div style="font-size:14px;font-weight:900;color:#16A34A;flex-shrink:0;">${fare}</div>
          </div>
        `).join('')}
      </div>
    </div>`;

    // ═══════════════════════════════════════════════════════════════
    //  TAB: PROFILE — Yatri Saathi style profile + menu
    // ═══════════════════════════════════════════════════════════════
    const profileTab = `
    <div style="background:var(--r-bg);min-height:100%;padding-bottom:20px;">
      <!-- Profile hero -->
      <div style="background:var(--r-dark);padding:28px 20px 24px;">
        <div style="display:flex;align-items:center;gap:16px;margin-bottom:18px;">
          <div style="width:64px;height:64px;border-radius:20px;background:var(--r-yellow);display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:900;color:var(--r-dark);flex-shrink:0;">S</div>
          <div style="flex:1;">
            <div style="font-size:20px;font-weight:900;color:#FFFFFF;letter-spacing:-0.3px;">${driverName}</div>
            <div style="font-size:12px;color:#9CA3AF;margin-top:2px;">${vehicleType}</div>
            <div style="font-size:12px;color:#9CA3AF;">${vehiclePlate}</div>
          </div>
          <button onclick="switchUserRole('farmer')" class="r-btn" style="background:rgba(255,202,32,0.12);border:1px solid rgba(255,202,32,0.3);border-radius:12px;padding:8px 12px;color:var(--r-yellow);font-size:11px;font-weight:800;cursor:pointer;text-align:center;">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" style="display:block;margin:0 auto 3px;"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            Farmer View
          </button>
        </div>
        <!-- Rating row -->
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;">
          ${[['4.9','Rating','var(--r-yellow)'],['420','Hauls','#FFFFFF'],['98%','Acceptance','#FFFFFF']].map(([val,label,color])=>`
            <div style="background:rgba(255,255,255,0.08);border-radius:13px;padding:10px 12px;text-align:center;">
              <div style="font-size:20px;font-weight:900;color:${color};letter-spacing:-0.3px;">${val}</div>
              <div style="font-size:10px;color:#9CA3AF;font-weight:700;margin-top:2px;">${label}</div>
            </div>
          `).join('')}
        </div>
      </div>

      <!-- Menu items -->
      <div style="padding:16px 16px 0;">
        <div class="r-card" style="overflow:hidden;margin-bottom:14px;">
          ${[
            ['M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2M9 5a2 2 0 0 0 2 2h2a2 2 0 0 0 2-2M9 5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2','Haul History','All past trips & receipts'],
            ['M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z','Insurance & FASTag','TS 03 UB 4491 · Active till Dec 2025'],
            ['M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 0-2-2z|M9 22V12h6v10','Vehicle Documents','RC, Permit, Fitness, PUC'],
            ['M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2|M23 21v-2a4 4 0 0 0-3-3.87|M16 3.13a4 4 0 0 1 0 7.75','Refer & Earn','₹500 per driver referred'],
            ['M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0zm-5 0a4 4 0 1 1-8 0 4 4 0 0 1 8 0z','Help & Support','24/7 driver helpline'],
          ].map(([d,label,sub],i)=>`
            <button class="r-btn" style="width:100%;display:flex;align-items:center;gap:14px;padding:14px 18px;background:none;border:none;border-bottom:${i<4?'1px solid #F9FAFB':'none'};cursor:pointer;text-align:left;">
              <div style="width:40px;height:40px;border-radius:13px;background:#F9FAFB;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--r-dark)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  ${d.split('|').map(p=>`<path d="${p}"/>`).join('')}
                </svg>
              </div>
              <div style="flex:1;min-width:0;">
                <div style="font-size:14px;font-weight:800;color:var(--r-dark);">${label}</div>
                <div style="font-size:11px;color:#9CA3AF;margin-top:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${sub}</div>
              </div>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#D1D5DB" stroke-width="2.5" stroke-linecap="round"><polyline points="9 18 15 12 9 6"/></svg>
            </button>
          `).join('')}
        </div>

        <!-- Vehicle status card -->
        <div class="r-card" style="padding:16px 18px;margin-bottom:14px;">
          <div style="font-size:14px;font-weight:900;color:var(--r-dark);margin-bottom:12px;">Vehicle Status</div>
          ${[
            ['Diesel Level','78%',true],['FASTag Balance','₹1,450',false],
            ['Next Service','1,400 km away',false],['Insurance Valid','Till Dec 2025',false]
          ].map(([label,val,hasBar],i)=>`
            <div style="display:flex;align-items:center;padding:9px 0;${i<3?'border-bottom:1px solid #F9FAFB;':''}">
              <span style="font-size:12.5px;color:#6B7280;flex:1;">${label}</span>
              ${hasBar
                ? `<div style="display:flex;align-items:center;gap:8px;">
                     <div style="width:56px;height:5px;background:#F3F4F6;border-radius:10px;overflow:hidden;">
                       <div style="width:78%;height:100%;background:var(--r-yellow);border-radius:10px;"></div>
                     </div>
                     <span style="font-size:12.5px;font-weight:800;color:var(--r-dark);">${val}</span>
                   </div>`
                : `<span style="font-size:12.5px;font-weight:800;color:var(--r-dark);">${val}</span>`
              }
            </div>
          `).join('')}
        </div>
      </div>
    </div>`;

    // ═══════════════════════════════════════════════════════════════
    //  BOTTOM NAV — 3 tabs: Map, Earnings, Profile
    // ═══════════════════════════════════════════════════════════════
    const bottomNav = `
    <div style="position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#FFFFFF;border-top:1px solid #F3F4F6;z-index:9100;padding:6px 0 max(env(safe-area-inset-bottom),10px);box-shadow:0 -2px 16px rgba(0,0,0,0.07);">
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;">
        ${[
          {key:'map',label:'Map',svg:'<polygon points="3 11 22 2 13 21 11 13 3 11"/>'},
          {key:'earnings',label:'Earnings',svg:'<line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>'},
          {key:'profile',label:'Profile',svg:'<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>'},
        ].map(t=>`
          <button class="r-nav-item" onclick="ghDriverNavTo('${t.key}')" style="display:flex;flex-direction:column;align-items:center;gap:3px;padding:8px 4px;background:none;border:none;cursor:pointer;position:relative;">
            ${activeTab===t.key ? `<div style="position:absolute;top:0;left:50%;transform:translateX(-50%);width:32px;height:3px;background:var(--r-yellow);border-radius:0 0 4px 4px;"></div>` : ''}
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="${activeTab===t.key?'var(--r-dark)':'#9CA3AF'}" stroke-width="${activeTab===t.key?'2.5':'1.8'}" stroke-linecap="round" stroke-linejoin="round">
              ${t.svg}
            </svg>
            <span style="font-size:10.5px;font-weight:${activeTab===t.key?'900':'600'};color:${activeTab===t.key?'var(--r-dark)':'#9CA3AF'};">${t.label}</span>
          </button>
        `).join('')}
      </div>
    </div>`;

    const tabContent = activeTab==='earnings' ? earningsTab
                     : activeTab==='profile'  ? profileTab
                     : mapTab;

    setTimeout(()=>{
      const sc = document.getElementById('screen-container');
      if(sc) sc.style.paddingBottom='80px';
    },50);

    return `${CSS}
    <div style="background:var(--r-bg);min-height:100%;padding-bottom:90px;font-family:-apple-system,BlinkMacSystemFont,'Plus Jakarta Sans','Inter',sans-serif;">
      ${tabContent}
    </div>
    ${bottomNav}`;
  },"""


DRIVER_V7_JS = """
/* ═══════════════════════════════════════════════════════════════
   GRAMHAUL DRIVER v7.0 — Rapido Captain + Yatri Saathi UI
   ═══════════════════════════════════════════════════════════════ */

function ghDriverNavTo(tab) {
  localStorage.setItem('gh_driver_tab', tab);
  const sc = document.getElementById('screen-container');
  if (sc) { sc.style.transition='opacity 0.15s'; sc.style.opacity='0'; }
  setTimeout(() => {
    if (typeof openScreen === 'function') openScreen('driver_dashboard', null);
    setTimeout(() => { if (sc) { sc.style.opacity='1'; sc.scrollTop=0; } }, 50);
  }, 120);
}

function toggleGhDriverOnline() {
  const cur = (localStorage.getItem('gh_driver_online') || 'true') === 'true';
  localStorage.setItem('gh_driver_online', String(!cur));
  if (typeof openScreen === 'function') openScreen('driver_dashboard', null);
}

function driverAcceptHaulRequest(tripId, fare) {
  const trip = {
    id: tripId,
    crop: 'Teja Chilli (25 Bags)', weight: '2.5 Ton',
    mandi: 'Khammam Spices APMC Mandi (Gate 1)',
    fare: fare, status: 'en_route', bookedAt: new Date().toISOString(),
    driver: { name: 'Suresh Yadav', phone: '+91 98765 44910', vehicle: 'Tata Ace 1.5T', plate: 'TS 03 UB 4491', rating: '4.9' }
  };
  localStorage.setItem('nukrop_active_trip', JSON.stringify(trip));
  localStorage.setItem('gh_driver_tab', 'map');
  const sheet = document.getElementById('gh-request-sheet');
  if (sheet) {
    sheet.style.transition = 'transform 0.25s cubic-bezier(0.4,0,1,1), opacity 0.2s';
    sheet.style.transform = 'translateY(100%)'; sheet.style.opacity = '0';
    setTimeout(() => { if (typeof openScreen==='function') openScreen('driver_dashboard', null); }, 250);
  } else {
    if (typeof openScreen==='function') openScreen('driver_dashboard', null);
  }
}

function declineHaulRequest(tripId) {
  const sheet = document.getElementById('gh-request-sheet');
  if (sheet) {
    sheet.style.transition = 'transform 0.25s cubic-bezier(0.4,0,1,1), opacity 0.2s';
    sheet.style.transform = 'translateY(100%)'; sheet.style.opacity = '0';
    setTimeout(() => {
      if (sheet.parentNode) sheet.parentNode.removeChild(sheet);
    }, 260);
  }
}

function driverDeclineHaul() {
  localStorage.removeItem('nukrop_active_trip');
  if (typeof openScreen==='function') openScreen('driver_dashboard', null);
}

function driverShowPaymentScreen(tripId, fare) {
  const fareNum = parseInt(String(fare).replace(/[^0-9]/g,'')) || 1850;
  const base = Math.round(fareNum * 0.70);
  const surge = fareNum - base;
  let waitAmt = 120;

  const modal = document.createElement('div');
  modal.id = 'gh-pay-modal';
  modal.style.cssText = 'position:fixed;inset:0;background:rgba(26,26,26,0.55);z-index:99999;backdrop-filter:blur(4px);display:flex;align-items:flex-end;justify-content:center;animation:rapido-fadein 0.2s;';
  modal.innerHTML = `
    <div style="background:#FFFFFF;width:100%;max-width:430px;border-radius:24px 24px 0 0;padding:0 0 28px;box-shadow:0 -10px 40px rgba(0,0,0,0.18);animation:rapido-slideup 0.3s cubic-bezier(0.16,1,0.3,1);">
      <div style="width:40px;height:4px;background:#E5E7EB;border-radius:10px;margin:14px auto 18px;"></div>

      <!-- Header -->
      <div style="padding:0 20px 16px;border-bottom:1px solid #F3F4F6;display:flex;align-items:center;gap:12px;">
        <div style="width:44px;height:44px;border-radius:14px;background:#FFFBEB;display:flex;align-items:center;justify-content:center;">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2" stroke-linecap="round"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
        </div>
        <div>
          <div style="font-size:11px;color:#9CA3AF;font-weight:700;text-transform:uppercase;letter-spacing:0.8px;">Payment from Farmer</div>
          <div style="font-size:15px;font-weight:900;color:#1A1A1A;">UPI / Cash Collection</div>
        </div>
      </div>

      <!-- Amount hero -->
      <div style="padding:22px 20px 0;text-align:center;">
        <div style="font-size:11px;color:#9CA3AF;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Collect from Farmer</div>
        <div id="pay-amount-display" style="font-size:54px;font-weight:900;color:#1A1A1A;letter-spacing:-2px;line-height:1;">₹${fareNum.toLocaleString('en-IN')}</div>
        <div style="display:flex;justify-content:center;gap:8px;margin-top:10px;">
          <span style="background:#FFFBEB;color:#92400E;font-size:10.5px;font-weight:800;padding:4px 10px;border-radius:8px;border:1px solid #FDE68A;">₹${base} Base</span>
          <span style="background:#FFFBEB;color:#D97706;font-size:10.5px;font-weight:800;padding:4px 10px;border-radius:8px;border:1px solid #FDE68A;">₹${surge} Surge</span>
        </div>
      </div>

      <!-- Wait time stepper -->
      <div style="margin:16px 20px 0;background:#F9FAFB;border-radius:15px;padding:14px 16px;display:flex;justify-content:space-between;align-items:center;">
        <div>
          <div style="font-size:13px;font-weight:800;color:#1A1A1A;">Loading Wait</div>
          <div style="font-size:11px;color:#9CA3AF;">+12 min on site</div>
        </div>
        <div style="display:flex;align-items:center;gap:12px;">
          <button id="pay-minus" style="width:32px;height:32px;border-radius:50%;border:1.5px solid #E5E7EB;background:#FFFFFF;font-size:20px;font-weight:700;cursor:pointer;display:flex;align-items:center;justify-content:center;color:#6B7280;line-height:1;">−</button>
          <span id="pay-wait-display" style="font-size:15px;font-weight:900;color:#1A1A1A;min-width:48px;text-align:center;">₹120</span>
          <button id="pay-plus" style="width:32px;height:32px;border-radius:50%;border:2px solid #FFCA20;background:#FFCA20;font-size:20px;font-weight:700;cursor:pointer;display:flex;align-items:center;justify-content:center;color:#1A1A1A;line-height:1;">+</button>
        </div>
      </div>

      <div style="margin:12px 20px;display:flex;justify-content:space-between;align-items:center;">
        <span style="font-size:13px;color:#6B7280;">You will earn</span>
        <span id="pay-total-display" style="font-size:18px;font-weight:900;color:#16A34A;">₹${(fareNum+120).toLocaleString('en-IN')}</span>
      </div>

      <div style="padding:0 20px;">
        <button onclick="driverCompleteHaulTrip('${tripId}','${fareNum}')" style="width:100%;height:58px;border-radius:18px;background:#FFCA20;color:#1A1A1A;font-size:16px;font-weight:900;border:none;cursor:pointer;box-shadow:0 8px 24px rgba(255,202,32,0.40);margin-bottom:10px;display:flex;align-items:center;justify-content:center;gap:10px;letter-spacing:-0.2px;">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
          Complete Haul & Collect
        </button>
        <button onclick="document.getElementById('gh-pay-modal').remove()" style="width:100%;height:46px;border-radius:14px;background:#F3F4F6;border:none;color:#6B7280;font-size:13.5px;font-weight:700;cursor:pointer;">
          Back to Active Trip
        </button>
      </div>
    </div>`;

  document.body.appendChild(modal);

  // Wire stepper
  let wait = 120;
  document.getElementById('pay-minus').onclick = () => {
    wait = Math.max(0, wait - 30);
    document.getElementById('pay-wait-display').textContent = '\\u20B9' + wait;
    document.getElementById('pay-total-display').textContent = '\\u20B9' + (fareNum + wait).toLocaleString('en-IN');
  };
  document.getElementById('pay-plus').onclick = () => {
    wait += 30;
    document.getElementById('pay-wait-display').textContent = '\\u20B9' + wait;
    document.getElementById('pay-total-display').textContent = '\\u20B9' + (fareNum + wait).toLocaleString('en-IN');
  };
  modal.addEventListener('click', e => { if (e.target===modal) modal.remove(); });
}
"""


def apply_v7(filepath):
    print(f'\nUpgrading {filepath} → Rapido Captain v7.0...')
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    import re
    dd_m = re.search(r'driver_dashboard\s*:\s*\(\)\s*=>\s*\{', text)
    pr_m = re.search(r'\n  profile\s*:\s*\(\)\s*=>', text)
    if not dd_m or not pr_m:
        print('  ✗ Could not find view boundaries'); return False

    # Replace driver_dashboard view
    text = text[:dd_m.start()] + DRIVER_V7_VIEW.strip() + '\n\n  ' + text[pr_m.start():].lstrip()
    print('  ✓ Replaced driver_dashboard → Rapido Captain v7.0')

    # Remove old driver JS
    marker = '/* ═══════════════════════════════════════════════════════════════\n   GRAMHAUL DRIVER'
    idx = text.rfind(marker)
    if idx == -1:
        marker = '/* ════════════════════════════════════════════════\n   GRAMHAUL DRIVER'
        idx = text.rfind(marker)
    if idx != -1:
        last_script = text.rfind('</script>')
        text = text[:idx] + text[last_script:]
        print('  ✓ Removed old driver JS')

    # Inject new JS
    last_script_idx = text.rfind('</script>')
    text = text[:last_script_idx] + '\n\n' + DRIVER_V7_JS.strip() + '\n\n' + text[last_script_idx:]
    print('  ✓ Injected Rapido Captain JS v7.0')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f'  ✓ Saved {filepath}')
    return True


if __name__ == '__main__':
    ok1 = apply_v7('app/src/main/assets/index.html')
    ok2 = apply_v7('nukrop_emulator.html')
    if ok1 and ok2:
        print('\n✅ Rapido Captain v7.0 upgrade complete!')
