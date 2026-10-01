import os, sys, re
sys.stdout.reconfigure(encoding='utf-8')

# ═══════════════════════════════════════════════════════════════════════════════
# UBER-DRIVER-GRADE GRAMHAUL COCKPIT — NuKropAI v5.0
# Inspired by: Citymobil / Yandex Go driver UI reference images provided by user
# ═══════════════════════════════════════════════════════════════════════════════

DRIVER_COCKPIT_V5 = """driver_dashboard: () => {
    let activeTrip = null;
    try {
      const tripRaw = localStorage.getItem('nukrop_active_trip');
      if (tripRaw) activeTrip = JSON.parse(tripRaw);
    } catch(e) {}

    const driverName   = localStorage.getItem('nukrop_driver_name') || 'Suresh Yadav';
    const vehiclePlate = localStorage.getItem('nukrop_driver_plate') || 'TS 03 UB 4491';
    const vehicleType  = localStorage.getItem('nukrop_driver_vehicle') || 'Tata Ace 1.5T';
    const isOnline     = (localStorage.getItem('gh_driver_online') || 'true') === 'true';

    const tripId     = activeTrip ? activeTrip.id : 'GH-4192';
    const tripCrop   = activeTrip ? (activeTrip.crop + ' (' + activeTrip.weight + ')') : 'Cotton (పత్తి) · 40 Quintals DCH-32';
    const tripPickup = activeTrip ? (typeof currentGramhaulFarmAddress !== 'undefined' ? currentGramhaulFarmAddress : "Ramesh Rao's Farm, Sy.No 142/A") : "Ramesh Rao's Farm, Sy.No 142/A, Narsampet Rural";
    const tripLandmark = typeof currentGramhaulFarmLandmark !== 'undefined' ? currentGramhaulFarmLandmark : 'Near Big Banyan Tree & Power Transformer';
    const tripDrop   = activeTrip ? activeTrip.mandi : 'Warangal Enamamula APMC Yard (Gate 3)';
    const tripFare   = activeTrip ? activeTrip.fare : '1,850';
    const tripEtaMins = '8';
    const tripDistKm = '4.8';

    const weekEarnings  = '₹12,640';
    const todayEarnings = '₹3,450';
    const todayTrips    = '4';
    const driverRating  = '4.9';

    const onlineStatus = isOnline
      ? `<div style="display:flex;align-items:center;gap:10px;background:#0F172A;border-radius:100px;padding:8px 16px 8px 8px;box-shadow:0 4px 20px rgba(0,0,0,0.35);cursor:pointer;" onclick="toggleGhDriverOnline()">
           <div style="width:36px;height:36px;border-radius:50%;background:#16A34A;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 4px rgba(22,163,74,0.25);">
             <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
           </div>
           <div>
             <div style="font-size:13.5px;font-weight:900;color:#FFFFFF;">На лінії · On Duty</div>
             <div style="font-size:10px;color:#94A3B8;font-weight:600;">Tap to go offline</div>
           </div>
           <svg style="margin-left:4px;" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#94A3B8" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
         </div>`
      : `<div style="display:flex;align-items:center;gap:10px;background:#0F172A;border-radius:100px;padding:8px 16px 8px 8px;box-shadow:0 4px 20px rgba(0,0,0,0.35);cursor:pointer;" onclick="toggleGhDriverOnline()">
           <div style="width:36px;height:36px;border-radius:50%;background:#DC2626;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 4px rgba(220,38,38,0.25);">
             <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
           </div>
           <div>
             <div style="font-size:13.5px;font-weight:900;color:#FFFFFF;">Офлайн · Offline</div>
             <div style="font-size:10px;color:#94A3B8;font-weight:600;">Tap to go online</div>
           </div>
           <svg style="margin-left:4px;" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#94A3B8" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
         </div>`;

    const activeTripHtml = activeTrip ? `
      <!-- ═══ LIVE ACTIVE HAUL CARD (Uber-style) ═══ -->
      <div style="background:#FFFFFF;border-radius:24px;overflow:hidden;box-shadow:0 4px 24px rgba(15,23,42,0.10);margin-bottom:16px;">

        <!-- Map Strip -->
        <div id="driver-live-map" style="width:100%;height:180px;background:linear-gradient(135deg,#E8F5E9,#F1F8E9);position:relative;overflow:hidden;">
          <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;">
            <div style="text-align:center;color:#64748B;">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2"><circle cx="12" cy="10" r="3"/><path d="M12 2a8 8 0 0 1 8 8c0 5.25-8 13-8 13S4 15.25 4 10a8 8 0 0 1 8-8z"/></svg>
              <div style="font-size:10px;font-weight:700;color:#16A34A;margin-top:4px;">Map Loading...</div>
            </div>
          </div>
          <!-- Decline pill -->
          <button onclick="driverDeclineHaul()" style="position:absolute;top:10px;left:10px;background:rgba(15,23,42,0.7);border:none;border-radius:100px;padding:5px 14px;color:#FFFFFF;font-size:11.5px;font-weight:800;cursor:pointer;backdrop-filter:blur(6px);">
            Decline
          </button>
        </div>

        <!-- Trip Request Bottom Sheet -->
        <div style="padding:14px 16px 16px;">
          <!-- Tag + ETA headline -->
          <div style="display:flex;align-items:center;gap:6px;margin-bottom:6px;">
            <span style="background:#F0FDF4;color:#16A34A;font-size:10px;font-weight:900;padding:3px 8px;border-radius:6px;border:1px solid #BBF7D0;">⚡ No Platform Fee</span>
            <span style="background:#FEF3C7;color:#D97706;font-size:10px;font-weight:900;padding:3px 8px;border-radius:6px;border:1px solid #FDE68A;">LIVE TRIP #${tripId}</span>
          </div>
          <div style="display:flex;align-items:flex-end;justify-content:space-between;margin-bottom:12px;">
            <div>
              <div style="font-size:26px;font-weight:900;color:#0F172A;letter-spacing:-0.5px;">${tripEtaMins} min · ${tripDistKm} km</div>
              <div style="font-size:12px;color:#64748B;font-weight:600;margin-top:2px;">to Farmer Pickup Location</div>
            </div>
            <div style="text-align:right;">
              <div style="font-size:22px;font-weight:900;color:#16A34A;">₹${tripFare}</div>
              <div style="font-size:10px;color:#64748B;font-weight:600;">Haul Fare</div>
            </div>
          </div>

          <!-- Route Info -->
          <div style="background:#F8FAFC;border-radius:16px;padding:12px 14px;margin-bottom:12px;">
            <div style="display:flex;gap:10px;margin-bottom:8px;">
              <div style="display:flex;flex-direction:column;align-items:center;padding-top:3px;">
                <div style="width:10px;height:10px;border-radius:50%;background:#16A34A;border:2px solid #FFFFFF;box-shadow:0 0 0 2px #16A34A;"></div>
                <div style="width:1.5px;height:24px;background:#CBD5E1;margin:2px 0;"></div>
                <div style="width:10px;height:10px;border-radius:50%;background:#DC2626;border:2px solid #FFFFFF;box-shadow:0 0 0 2px #DC2626;"></div>
              </div>
              <div style="flex:1;">
                <div style="margin-bottom:12px;">
                  <div style="font-size:10px;color:#64748B;font-weight:800;text-transform:uppercase;letter-spacing:0.5px;">Farmer Exact Pickup (GPS)</div>
                  <div style="font-size:13px;font-weight:800;color:#0F172A;margin-top:1px;">${tripPickup}</div>
                  <div style="font-size:11px;color:#64748B;margin-top:1px;">${tripLandmark}</div>
                </div>
                <div>
                  <div style="font-size:10px;color:#64748B;font-weight:800;text-transform:uppercase;letter-spacing:0.5px;">Drop APMC Mandi</div>
                  <div style="font-size:13px;font-weight:800;color:#0F172A;margin-top:1px;">${tripDrop}</div>
                </div>
              </div>
            </div>

            <!-- Cargo Badges -->
            <div style="display:flex;gap:6px;flex-wrap:wrap;padding-top:8px;border-top:1px solid #F1F5F9;">
              <span style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:8px;padding:4px 8px;font-size:10.5px;font-weight:700;color:#334155;">🌾 ${tripCrop}</span>
              <span style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:8px;padding:4px 8px;font-size:10.5px;font-weight:700;color:#334155;">👤 Ramesh Rao</span>
              <span style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:8px;padding:4px 8px;font-size:10.5px;font-weight:700;color:#334155;">📞 +91 94401 22910</span>
            </div>
          </div>

          <!-- Driver Action Buttons (Uber style) -->
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:10px;">
            <button onclick="driverCallFarmer('+919440122910')" style="height:46px;background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:14px;font-size:12.5px;font-weight:800;color:#0F172A;display:flex;align-items:center;justify-content:center;gap:8px;cursor:pointer;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2.5"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12 19.79 19.79 0 0 1 1.61 3.4 2 2 0 0 1 3.6 1.2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.82a16 16 0 0 0 6 6l.91-.91a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
              Call Farmer
            </button>
            <button onclick="messageGramhaulDriver()" style="height:46px;background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:14px;font-size:12.5px;font-weight:800;color:#0F172A;display:flex;align-items:center;justify-content:center;gap:8px;cursor:pointer;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2.5"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
              Live Chat
            </button>
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
            <button onclick="driverOpenGpsNav(17.9689, 79.5941)" style="height:50px;background:#16A34A;color:#FFFFFF;border:none;border-radius:16px;font-size:13px;font-weight:900;display:flex;align-items:center;justify-content:center;gap:8px;cursor:pointer;box-shadow:0 6px 20px rgba(22,163,74,0.35);">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.5"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg>
              Start GPS Nav
            </button>
            <button onclick="driverShowPaymentScreen('${tripId}', '${tripFare}')" style="height:50px;background:#0F172A;color:#FFFFFF;border:none;border-radius:16px;font-size:13px;font-weight:900;display:flex;align-items:center;justify-content:center;gap:8px;cursor:pointer;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
              Mark Delivered
            </button>
          </div>
        </div>
      </div>` : `
      <!-- ═══ HAUL REQUESTS POOL (Online / Waiting state) ═══ -->
      <div style="margin-bottom:16px;" id="gh-available-hauls">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
          <div style="font-size:15px;font-weight:900;color:#0F172A;">Available Haul Requests</div>
          <span style="background:#DCFCE7;color:#15803D;font-size:10px;font-weight:800;padding:3px 8px;border-radius:6px;border:1px solid #86EFAC;">2 Ready</span>
        </div>

        <!-- Haul Request Card 1 -->
        <div style="background:#FFFFFF;border-radius:20px;overflow:hidden;box-shadow:0 2px 16px rgba(15,23,42,0.08);margin-bottom:10px;">
          <div style="height:100px;background:linear-gradient(135deg,#E8F5E9,#F1F8E9);position:relative;">
            <button onclick="declineHaulRequest('GH-8824')" style="position:absolute;top:8px;left:8px;background:rgba(15,23,42,0.65);border:none;border-radius:100px;padding:4px 12px;color:#FFFFFF;font-size:11px;font-weight:800;cursor:pointer;backdrop-filter:blur(6px);">Decline −12</button>
            <div style="position:absolute;top:8px;right:8px;background:#F0FDF4;border-radius:8px;padding:3px 8px;border:1px solid #BBF7D0;">
              <span style="font-size:10px;font-weight:900;color:#16A34A;">🌶️ Chilli Cargo</span>
            </div>
          </div>
          <div style="padding:12px 14px 14px;">
            <div style="display:flex;align-items:flex-end;justify-content:space-between;margin-bottom:8px;">
              <div>
                <div style="font-size:22px;font-weight:900;color:#0F172A;letter-spacing:-0.3px;">5 min · 5.8 km</div>
                <div style="font-size:11.5px;color:#64748B;font-weight:600;">to Farmer Pickup</div>
              </div>
              <div style="text-align:right;">
                <div style="font-size:20px;font-weight:900;color:#16A34A;">₹4,200</div>
                <div style="background:#FEF3C7;border-radius:6px;padding:1px 6px;font-size:9.5px;font-weight:800;color:#D97706;margin-top:2px;">×2.4 surge</div>
              </div>
            </div>
            <div style="background:#F8FAFC;border-radius:12px;padding:10px 12px;margin-bottom:10px;">
              <div style="display:flex;gap:8px;align-items:flex-start;margin-bottom:6px;">
                <div style="width:8px;height:8px;border-radius:50%;background:#16A34A;margin-top:4px;flex-shrink:0;"></div>
                <div style="font-size:12px;font-weight:700;color:#334155;">K. Anjaiah Farm, Hasanparthy (5.8 km away)</div>
              </div>
              <div style="display:flex;gap:8px;align-items:flex-start;">
                <div style="width:8px;height:8px;border-radius:50%;background:#DC2626;margin-top:4px;flex-shrink:0;"></div>
                <div style="font-size:12px;font-weight:700;color:#334155;">Khammam Spices APMC Mandi (Gate 1)</div>
              </div>
              <div style="margin-top:8px;padding-top:8px;border-top:1px solid #F1F5F9;font-size:11px;color:#64748B;">🌶️ Teja Chilli · 25 Bags · 2.5 Ton</div>
            </div>
            <button onclick="driverAcceptHaulRequest('GH-8824','4200')" style="width:100%;height:50px;border-radius:16px;background:#16A34A;color:#FFFFFF;font-size:15px;font-weight:900;border:none;cursor:pointer;box-shadow:0 6px 20px rgba(22,163,74,0.35);display:flex;align-items:center;justify-content:center;gap:8px;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
              Accept Haul · ₹4,200
            </button>
          </div>
        </div>

        <!-- Haul Request Card 2 -->
        <div style="background:#FFFFFF;border-radius:20px;overflow:hidden;box-shadow:0 2px 16px rgba(15,23,42,0.08);margin-bottom:10px;">
          <div style="height:80px;background:linear-gradient(135deg,#FFF7ED,#FEF3C7);position:relative;">
            <button onclick="declineHaulRequest('GH-5512')" style="position:absolute;top:8px;left:8px;background:rgba(15,23,42,0.65);border:none;border-radius:100px;padding:4px 12px;color:#FFFFFF;font-size:11px;font-weight:800;cursor:pointer;backdrop-filter:blur(6px);">Decline</button>
            <div style="position:absolute;top:8px;right:8px;background:#FEF3C7;border-radius:8px;padding:3px 8px;border:1px solid #FDE68A;">
              <span style="font-size:10px;font-weight:900;color:#D97706;">🌾 Paddy Cargo</span>
            </div>
          </div>
          <div style="padding:12px 14px 14px;">
            <div style="display:flex;align-items:flex-end;justify-content:space-between;margin-bottom:8px;">
              <div>
                <div style="font-size:20px;font-weight:900;color:#0F172A;letter-spacing:-0.3px;">12 min · 9.2 km</div>
                <div style="font-size:11.5px;color:#64748B;font-weight:600;">to Farmer Pickup</div>
              </div>
              <div style="text-align:right;">
                <div style="font-size:18px;font-weight:900;color:#16A34A;">₹2,800</div>
                <div style="background:#F0FDF4;border-radius:6px;padding:1px 6px;font-size:9.5px;font-weight:800;color:#16A34A;margin-top:2px;">×1.8</div>
              </div>
            </div>
            <div style="font-size:11.5px;color:#64748B;margin-bottom:10px;">Jangaon → Warangal APMC · Paddy 30 Bags</div>
            <button onclick="driverAcceptHaulRequest('GH-5512','2800')" style="width:100%;height:46px;border-radius:14px;background:#0F172A;color:#FFFFFF;font-size:13.5px;font-weight:900;border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
              Accept · ₹2,800
            </button>
          </div>
        </div>
      </div>`;

    return \`
    <div style="background:#F4F6F9;min-height:100%;padding-bottom:100px;font-family:-apple-system,BlinkMacSystemFont,'Plus Jakarta Sans','Inter',sans-serif;">

      <!-- ═══ TOP STATUS BAR — Uber Driver Style ═══ -->
      <div style="padding:12px 16px 14px;background:#FFFFFF;border-bottom:1px solid #F1F5F9;">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
          <div style="display:flex;align-items:center;gap:8px;">
            <div style="width:38px;height:38px;border-radius:12px;background:#0F172A;display:flex;align-items:center;justify-content:center;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><rect x="1" y="3" width="15" height="13" rx="2" stroke="#16A34A" stroke-width="2"/><path d="M16 8h4l3 5v4h-7V8z" stroke="#16A34A" stroke-width="2" stroke-linejoin="round"/><circle cx="5.5" cy="18.5" r="2.5" stroke="#16A34A" stroke-width="2"/><circle cx="18.5" cy="18.5" r="2.5" stroke="#16A34A" stroke-width="2"/></svg>
            </div>
            <div>
              <div style="font-size:14px;font-weight:900;color:#0F172A;">GramHaul Cockpit</div>
              <div style="font-size:10.5px;color:#64748B;font-weight:600;">\${driverName} · \${vehicleType} · \${vehiclePlate}</div>
            </div>
          </div>
          <button onclick="switchUserRole('farmer')" style="background:#F1F5F9;border:none;border-radius:100px;padding:6px 12px;color:#0F172A;font-size:11px;font-weight:800;cursor:pointer;display:flex;align-items:center;gap:5px;">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            Farmer View
          </button>
        </div>

        <!-- Online / Offline Toggle Pill -->
        <div style="display:flex;justify-content:center;">
          \${onlineStatus}
        </div>
      </div>

      <!-- ═══ EARNINGS DASHBOARD STRIP ═══ -->
      <div style="padding:14px 16px 0;">
        <div style="background:#FFFFFF;border-radius:20px;padding:14px 16px;box-shadow:0 2px 12px rgba(15,23,42,0.06);margin-bottom:14px;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
            <div style="font-size:13px;font-weight:900;color:#0F172A;">This Week's Earnings</div>
            <div style="display:flex;gap:4px;">
              <button style="background:#0F172A;color:#FFFFFF;border:none;border-radius:100px;padding:3px 10px;font-size:10px;font-weight:800;cursor:pointer;">Week</button>
              <button style="background:#F1F5F9;color:#64748B;border:none;border-radius:100px;padding:3px 10px;font-size:10px;font-weight:700;cursor:pointer;">Month</button>
            </div>
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;">
            <div style="text-align:center;">
              <div style="font-size:10px;color:#94A3B8;font-weight:700;margin-bottom:2px;">TODAY</div>
              <div style="font-size:20px;font-weight:900;color:#16A34A;letter-spacing:-0.3px;">\${todayEarnings}</div>
            </div>
            <div style="text-align:center;border-left:1px solid #F1F5F9;border-right:1px solid #F1F5F9;">
              <div style="font-size:10px;color:#94A3B8;font-weight:700;margin-bottom:2px;">WEEK</div>
              <div style="font-size:20px;font-weight:900;color:#0F172A;letter-spacing:-0.3px;">\${weekEarnings}</div>
            </div>
            <div style="text-align:center;">
              <div style="font-size:10px;color:#94A3B8;font-weight:700;margin-bottom:2px;">TRIPS</div>
              <div style="font-size:20px;font-weight:900;color:#0F172A;letter-spacing:-0.3px;">\${todayTrips}</div>
            </div>
          </div>
          <!-- Earnings Bar Chart (simple) -->
          <div style="display:flex;align-items:flex-end;gap:4px;height:36px;margin-top:12px;padding-top:8px;border-top:1px solid #F8FAFC;">
            <div style="flex:1;background:#DCFCE7;border-radius:4px 4px 0 0;height:40%;"></div>
            <div style="flex:1;background:#DCFCE7;border-radius:4px 4px 0 0;height:60%;"></div>
            <div style="flex:1;background:#16A34A;border-radius:4px 4px 0 0;height:90%;"></div>
            <div style="flex:1;background:#DCFCE7;border-radius:4px 4px 0 0;height:55%;"></div>
            <div style="flex:1;background:#DCFCE7;border-radius:4px 4px 0 0;height:45%;"></div>
            <div style="flex:1;background:#DCFCE7;border-radius:4px 4px 0 0;height:75%;"></div>
            <div style="flex:1;background:#16A34A;border-radius:4px 4px 0 0;height:100%;"></div>
          </div>
        </div>

        <!-- ═══ ACTIVE TRIP OR HAUL REQUESTS ═══ -->
        \${activeTripHtml}

        <!-- ═══ VEHICLE & FASTAG DIAGNOSTICS ═══ -->
        <div style="background:#FFFFFF;border-radius:20px;padding:14px 16px;box-shadow:0 2px 12px rgba(15,23,42,0.06);margin-bottom:14px;">
          <div style="font-size:13px;font-weight:900;color:#0F172A;margin-bottom:12px;display:flex;align-items:center;gap:8px;">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><rect x="1" y="3" width="15" height="13" rx="2" stroke="#16A34A" stroke-width="2"/><path d="M16 8h4l3 5v4h-7V8z" stroke="#16A34A" stroke-width="2" stroke-linejoin="round"/><circle cx="5.5" cy="18.5" r="2.5" stroke="#16A34A" stroke-width="2"/><circle cx="18.5" cy="18.5" r="2.5" stroke="#16A34A" stroke-width="2"/></svg>
            Vehicle & FASTag
          </div>
          <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #F8FAFC;">
            <span style="font-size:12px;color:#64748B;">Diesel Level</span>
            <div style="display:flex;align-items:center;gap:8px;">
              <div style="width:60px;height:5px;background:#F1F5F9;border-radius:10px;overflow:hidden;">
                <div style="width:78%;height:100%;background:#16A34A;border-radius:10px;"></div>
              </div>
              <span style="font-size:12px;font-weight:800;color:#16A34A;">78%</span>
            </div>
          </div>
          <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #F8FAFC;">
            <span style="font-size:12px;color:#64748B;">FASTag Balance</span>
            <span style="font-size:12px;font-weight:800;color:#0F172A;">₹1,450.00</span>
          </div>
          <div style="display:flex;justify-content:space-between;padding:8px 0;">
            <span style="font-size:12px;color:#64748B;">Next Service</span>
            <span style="font-size:12px;font-weight:800;color:#16A34A;">1,400 km away</span>
          </div>
        </div>

        <!-- ═══ TRIP HISTORY (Ledger-style) ═══ -->
        <div style="background:#FFFFFF;border-radius:20px;padding:14px 16px;box-shadow:0 2px 12px rgba(15,23,42,0.06);margin-bottom:14px;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
            <div style="font-size:13px;font-weight:900;color:#0F172A;">Today's Haul History</div>
            <button style="font-size:11px;color:#16A34A;font-weight:800;background:none;border:none;cursor:pointer;">See All →</button>
          </div>
          <div style="display:flex;flex-direction:column;gap:0;">
            <div style="display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid #F8FAFC;">
              <div style="width:38px;height:38px;border-radius:12px;background:#F0FDF4;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><rect x="1" y="3" width="15" height="13" rx="2" stroke="#16A34A" stroke-width="1.5"/><path d="M16 8h4l3 5v4h-7V8z" stroke="#16A34A" stroke-width="1.5"/></svg>
              </div>
              <div style="flex:1;">
                <div style="font-size:12.5px;font-weight:800;color:#0F172A;">Cotton → Warangal APMC</div>
                <div style="font-size:10.5px;color:#94A3B8;font-weight:600;">09:12 AM · #GH-4121</div>
              </div>
              <div style="font-size:13.5px;font-weight:900;color:#16A34A;">₹1,683</div>
            </div>
            <div style="display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid #F8FAFC;">
              <div style="width:38px;height:38px;border-radius:12px;background:#FFF7ED;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><rect x="1" y="3" width="15" height="13" rx="2" stroke="#D97706" stroke-width="1.5"/><path d="M16 8h4l3 5v4h-7V8z" stroke="#D97706" stroke-width="1.5"/></svg>
              </div>
              <div style="flex:1;">
                <div style="font-size:12.5px;font-weight:800;color:#0F172A;">Chilli → Khammam APMC</div>
                <div style="font-size:10.5px;color:#94A3B8;font-weight:600;">07:35 AM · #GH-4108</div>
              </div>
              <div style="font-size:13.5px;font-weight:900;color:#16A34A;">₹890</div>
            </div>
            <div style="display:flex;align-items:center;gap:12px;padding:10px 0;">
              <div style="width:38px;height:38px;border-radius:12px;background:#F0FDF4;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><rect x="1" y="3" width="15" height="13" rx="2" stroke="#16A34A" stroke-width="1.5"/><path d="M16 8h4l3 5v4h-7V8z" stroke="#16A34A" stroke-width="1.5"/></svg>
              </div>
              <div style="flex:1;">
                <div style="font-size:12.5px;font-weight:800;color:#0F172A;">Paddy → Jangaon APMC</div>
                <div style="font-size:10.5px;color:#94A3B8;font-weight:600;">06:50 AM · #GH-4099</div>
              </div>
              <div style="font-size:13.5px;font-weight:900;color:#16A34A;">₹877</div>
            </div>
          </div>
        </div>

        <!-- ═══ DRIVER PROFILE FOOTER CARD ═══ -->
        <div style="background:#0F172A;border-radius:20px;padding:16px;box-shadow:0 4px 20px rgba(15,23,42,0.20);margin-bottom:14px;">
          <div style="display:flex;align-items:center;gap:12px;">
            <div style="width:50px;height:50px;border-radius:16px;background:linear-gradient(135deg,#D97706,#B45309);display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:900;color:#FFFFFF;flex-shrink:0;">S</div>
            <div style="flex:1;">
              <div style="font-size:15px;font-weight:900;color:#FFFFFF;">\${driverName}</div>
              <div style="font-size:11px;color:#94A3B8;font-weight:600;">\${vehicleType} · \${vehiclePlate}</div>
              <div style="display:flex;align-items:center;gap:4px;margin-top:2px;">
                <svg width="11" height="11" viewBox="0 0 24 24" fill="#FBBF24" stroke="none"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
                <span style="font-size:11px;color:#FBBF24;font-weight:800;">\${driverRating} · 420 trips</span>
              </div>
            </div>
            <div style="text-align:right;">
              <div style="font-size:10px;color:#94A3B8;font-weight:700;">RATING</div>
              <div style="font-size:22px;font-weight:900;color:#34D399;">\${driverRating}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
    \`;
  },"""


# ═══════════════════════════════════════════════════════════════════════════════
# NEW JS FUNCTIONS for Driver Cockpit (Toggle Online, Accept, Decline, Payment)
# ═══════════════════════════════════════════════════════════════════════════════

DRIVER_COCKPIT_JS = """
/* ════════════════════════════════════════════════
   GRAMHAUL DRIVER COCKPIT v5.0 — Uber-Grade UI
   ════════════════════════════════════════════════ */

function toggleGhDriverOnline() {
  const current = (localStorage.getItem('gh_driver_online') || 'true') === 'true';
  const next = !current;
  localStorage.setItem('gh_driver_online', String(next));
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
  if (typeof openScreen === 'function') openScreen('driver_dashboard', null);
}

function declineHaulRequest(tripId) {
  const el = document.getElementById('gh-available-hauls');
  if (el) {
    el.innerHTML = `
      <div style="background:#FFFFFF;border-radius:20px;padding:28px 20px;text-align:center;box-shadow:0 2px 12px rgba(15,23,42,0.06);">
        <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2" style="margin-bottom:10px;"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
        <div style="font-size:15px;font-weight:900;color:#0F172A;margin-bottom:4px;">Waiting for Haul Requests</div>
        <div style="font-size:12px;color:#64748B;">Nearby farmer haul requests will appear here. Stay online!</div>
      </div>`;
  }
}

function driverShowPaymentScreen(tripId, fare) {
  const modalHtml = `
    <div id="gh-driver-payment-modal" style="position:fixed;inset:0;background:rgba(15,23,42,0.65);z-index:9999;backdrop-filter:blur(4px);display:flex;align-items:flex-end;justify-content:center;">
      <div style="background:#FFFFFF;width:100%;max-width:440px;border-radius:28px 28px 0 0;padding:22px 20px 32px;box-shadow:0 -10px 40px rgba(0,0,0,0.25);animation:modalSlideUp 0.22s cubic-bezier(0.16,1,0.3,1);">
        <div style="width:40px;height:4px;background:#E2E8F0;border-radius:10px;margin:0 auto 18px;"></div>

        <!-- Payment Method -->
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px;">
          <div style="width:40px;height:40px;border-radius:12px;background:#F0FDF4;display:flex;align-items:center;justify-content:center;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
          </div>
          <div>
            <div style="font-size:11px;color:#64748B;font-weight:700;">PAYMENT FROM FARMER</div>
            <div style="font-size:14px;font-weight:900;color:#0F172A;">UPI / Cash Collection</div>
          </div>
        </div>

        <!-- Amount -->
        <div style="text-align:center;margin-bottom:20px;padding:16px;background:#F8FAFC;border-radius:18px;">
          <div style="font-size:12px;color:#64748B;font-weight:700;margin-bottom:4px;">COLLECT FROM FARMER</div>
          <div style="font-size:42px;font-weight:900;color:#0F172A;letter-spacing:-1px;">₹${fare}</div>
          <div style="display:flex;justify-content:center;gap:8px;margin-top:10px;">
            <span style="background:#DCFCE7;color:#16A34A;font-size:10px;font-weight:800;padding:3px 8px;border-radius:6px;">₹${Math.round(parseInt(fare)*0.7)} Base Fare</span>
            <span style="background:#FEF3C7;color:#D97706;font-size:10px;font-weight:800;padding:3px 8px;border-radius:6px;">₹${Math.round(parseInt(fare)*0.3)} Surge</span>
          </div>
        </div>

        <!-- Waiting Fee -->
        <div style="display:flex;justify-content:space-between;align-items:center;padding:12px 14px;background:#F8FAFC;border-radius:14px;margin-bottom:8px;">
          <div>
            <div style="font-size:12.5px;font-weight:800;color:#0F172A;">Paid Wait Time</div>
            <div style="font-size:11px;color:#64748B;">+12 min loading help</div>
          </div>
          <div style="display:flex;align-items:center;gap:8px;">
            <button style="width:28px;height:28px;border-radius:50%;border:1.5px solid #E2E8F0;background:#FFFFFF;font-size:16px;font-weight:900;cursor:pointer;display:flex;align-items:center;justify-content:center;color:#64748B;">−</button>
            <span style="font-size:14px;font-weight:800;color:#0F172A;min-width:40px;text-align:center;">₹120</span>
            <button style="width:28px;height:28px;border-radius:50%;border:1.5px solid #16A34A;background:#16A34A;font-size:16px;font-weight:900;cursor:pointer;display:flex;align-items:center;justify-content:center;color:#FFFFFF;">+</button>
          </div>
        </div>

        <div style="display:flex;justify-content:space-between;padding:8px 14px;font-size:12px;margin-bottom:16px;">
          <span style="color:#64748B;">You will earn</span>
          <span style="font-weight:900;color:#16A34A;font-size:14px;">₹${parseInt(fare) + 120} →</span>
        </div>

        <button onclick="driverCompleteHaulTrip('${tripId}', '${fare}')" style="width:100%;height:54px;border-radius:18px;background:#16A34A;color:#FFFFFF;font-size:16px;font-weight:900;border:none;cursor:pointer;box-shadow:0 6px 24px rgba(22,163,74,0.40);">
          Complete Haul & Collect Payment
        </button>
        <button onclick="document.getElementById('gh-driver-payment-modal').remove()" style="width:100%;height:44px;border-radius:14px;background:#FFFFFF;border:1.5px solid #E2E8F0;color:#64748B;font-size:13px;font-weight:700;cursor:pointer;margin-top:8px;">
          Back to Active Trip
        </button>
      </div>
    </div>
  `;
  document.body.insertAdjacentHTML('beforeend', modalHtml);
}

"""


def apply_uber_cockpit_upgrade(filepath):
    print(f"Upgrading {filepath} with Uber-grade Driver Cockpit v5.0...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace driver_dashboard view
    pattern_driver = r'driver_dashboard\s*:\s*\(\)\s*=>\s*\{.*?(?=\n\s*/\* ── [0-9]+\.|\n\s*profile\s*:\s*\(\)\s*=>)'
    if re.search(pattern_driver, content, flags=re.DOTALL):
        content = re.sub(pattern_driver, DRIVER_COCKPIT_V5.strip(), content, count=1, flags=re.DOTALL)
        print("  ✓ Replaced driver_dashboard view!")
    else:
        print("  ✗ driver_dashboard view NOT matched - check pattern")

    # 2. Remove any previous driver cockpit JS block
    dc_marker = "/* ════════════════════════════════════════════════\n   GRAMHAUL DRIVER COCKPIT"
    idx = content.find(dc_marker)
    if idx != -1:
        last_script = content.rfind('</script>')
        content = content[:idx] + content[last_script:]
        print("  ✓ Removed previous Driver Cockpit JS block!")

    # 3. Inject new driver cockpit JS before </script>
    last_script_idx = content.rfind('</script>')
    if last_script_idx != -1:
        content = content[:last_script_idx] + '\n\n' + DRIVER_COCKPIT_JS.strip() + '\n\n' + content[last_script_idx:]
        print("  ✓ Injected Driver Cockpit JS v5.0!")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✓ Saved {filepath} successfully!")


if __name__ == '__main__':
    apply_uber_cockpit_upgrade('app/src/main/assets/index.html')
    apply_uber_cockpit_upgrade('nukrop_emulator.html')
    print("\nAll upgrades complete! Run: node syntax check then playwright capture.")
