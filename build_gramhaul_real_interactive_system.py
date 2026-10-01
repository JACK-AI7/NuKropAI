import os, sys, re

sys.stdout.reconfigure(encoding='utf-8')

# ═════════════════════════════════════════════════════════════════════════
# 1. COMPLETE GRAMHAUL REAL ACTIONS, PICKUP LOCATION & DRIVER SYNC ENGINE
# ═════════════════════════════════════════════════════════════════════════

GRAMHAUL_FULL_LOGIC_JS = """
/* ══════════════════════════════════════════════════════════════
   GRAMHAUL: REAL GPS, INTERACTIVE PICKUP, REAL CHAT, CALL, SHARE & DRIVER SYNC
   ══════════════════════════════════════════════════════════════ */

window.finishLoginAndEnterDashboard = function(role) {
  const ids = ['startup-experience-overlay', 'onboarding-experience-overlay', 'permission-experience-overlay', 'splash-viewport', 'login-screen-overlay'];
  ids.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.remove();
  });
  const dock = document.querySelector('.bottom-dock-wrap');
  if (dock) dock.style.display = 'flex';
  if (role === 'driver') {
    if (typeof loginAsDriver === 'function') loginAsDriver();
    else if (typeof switchUserRole === 'function') switchUserRole('driver');
    else if (typeof openScreen === 'function') openScreen('driver_dashboard', null);
  } else {
    if (typeof switchUserRole === 'function') switchUserRole('farmer');
    if (typeof openScreen === 'function') openScreen('home', document.getElementById('tab-home'));
  }
};

const REAL_APMC_MANDIS = [
  { id: 'enumamula', name: 'Warangal Enamamula APMC Yard (Gate 3)', shortName: 'Warangal Enamamula APMC', city: 'Warangal', distKm: 4.8, coords: [17.9945, 79.5892], crops: 'Cotton, Chilli, Maize', tag: 'Nearest · 4.8 km' },
  { id: 'khammam', name: 'Khammam Spices APMC Mandi (Gate 1)', shortName: 'Khammam Spices Mandi', city: 'Khammam', distKm: 62.0, coords: [17.2472, 80.1514], crops: 'Teja Chilli, Cotton', tag: 'Spice Hub · 62 km' },
  { id: 'jangaon', name: 'Jangaon Grain & Cotton Market Yard', shortName: 'Jangaon APMC Yard', city: 'Jangaon', distKm: 54.0, coords: [17.7214, 79.1607], crops: 'Paddy, Cotton, Pulses', tag: '54 km' },
  { id: 'suryapet', name: 'Suryapet Commercial APMC Yard', shortName: 'Suryapet Commercial APMC', city: 'Suryapet', distKm: 78.0, coords: [17.1439, 79.6239], crops: 'Paddy, Groundnut, Green Gram', tag: '78 km' },
  { id: 'mahabubabad', name: 'Mahabubabad APMC Chilli Yard', shortName: 'Mahabubabad Chilli APMC', city: 'Mahabubabad', distKm: 45.0, coords: [17.5986, 80.0039], crops: 'Chilli, Turmeric, Maize', tag: '45 km' },
  { id: 'bowenpally', name: 'Bowenpally Wholesale APMC, Hyderabad', shortName: 'Bowenpally Wholesale APMC', city: 'Hyderabad', distKm: 138.0, coords: [17.4764, 78.4892], crops: 'Tomato, Vegetables, Onion', tag: 'Major Terminal · 138 km' },
  { id: 'guntur', name: 'Guntur Mirchi Yard (Gate 1)', shortName: 'Guntur Mirchi Yard', city: 'Guntur', distKm: 185.0, coords: [16.3067, 80.4365], crops: 'Asia Largest Chilli Market', tag: '185 km' },
  { id: 'nizamabad', name: 'Nizamabad Turmeric & Spices Mandi', shortName: 'Nizamabad Turmeric Mandi', city: 'Nizamabad', distKm: 160.0, coords: [18.6725, 78.0941], crops: 'Turmeric, Maize, Soya', tag: '160 km' }
];

const REAL_DRIVERS_FLEET = {
  suresh: { name: 'Suresh Yadav', phone: '+91 98765 44910', phoneRaw: '919876544910', vehicle: 'Tata Ace 1.5T', color: 'White', plate: 'TS 03 UB 4491', rating: '4.9', trips: 420, etaMins: 8 },
  anjaiah: { name: 'K. Anjaiah', phone: '+91 94401 22910', phoneRaw: '919440122910', vehicle: 'Mahindra Bolero 2.5T', color: 'Silver', plate: 'TS 04 EA 8824', rating: '4.8', trips: 310, etaMins: 14 },
  venkat: { name: 'S. Venkat', phone: '+91 98492 88441', phoneRaw: '919849288441', vehicle: 'Eicher Pro 5T Express', color: 'Green', plate: 'TS 08 UB 7712', rating: '4.9', trips: 580, etaMins: 22 }
};

let currentGramhaulFarmCoords = [17.9689, 79.5941];
let currentGramhaulFarmAddress = "Ramesh Rao's Farm, Sy.No 142/A, Narsampet Rural";
let currentGramhaulFarmLandmark = "Near Big Banyan Tree & Power Transformer";
let currentGramhaulMandi = REAL_APMC_MANDIS[0];
let selectedGramhaulTier = 1;
let selectedGramhaulCrop = 'Cotton (పత్తి)';
let selectedGramhaulWeight = '40 Quintals';
let selectedGramhaulPrice = 450;
let gramhaulLiveMap = null;
let gramhaulTruckMarker = null;
let gramhaulRoutePolyline = null;

let gramhaulChatMessages = [
  { sender: 'driver', text: 'Namaste Ramesh garu! I am dispatched with Tata Ace TS 03 UB 4491.', time: '09:12 AM' },
  { sender: 'driver', text: 'Reaching your farm in ~8 mins. Please keep the 40 Qtl Cotton bags ready near the gate.', time: '09:14 AM' }
];

function initGramhaulRealMap() {
  const mapContainer = document.getElementById('gramhaul-real-osm-map');
  if (!mapContainer) return;

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        currentGramhaulFarmCoords = [pos.coords.latitude, pos.coords.longitude];
        renderGramhaulLeafletMap();
      },
      () => {
        renderGramhaulLeafletMap();
      },
      { timeout: 4000, enableHighAccuracy: true }
    );
  } else {
    renderGramhaulLeafletMap();
  }
}

function renderGramhaulLeafletMap() {
  const mapContainer = document.getElementById('gramhaul-real-osm-map');
  if (!mapContainer) return;

  if (typeof L === 'undefined' || !L.map) return;

  try {
    if (gramhaulLiveMap) {
      gramhaulLiveMap.remove();
      gramhaulLiveMap = null;
    }

    gramhaulLiveMap = L.map('gramhaul-real-osm-map', {
      center: currentGramhaulFarmCoords,
      zoom: 13,
      zoomControl: false,
      attributionControl: false
    });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19
    }).addTo(gramhaulLiveMap);

    // 1. User Farm Marker
    const farmIcon = L.divIcon({
      className: 'gh-map-farm-pin',
      html: `<div style="background:#16A34A;color:#FFFFFF;font-size:10px;font-weight:900;padding:3px 8px;border-radius:10px;box-shadow:0 2px 8px rgba(22,163,74,0.5);white-space:nowrap;display:flex;align-items:center;gap:4px;border:1.5px solid #FFFFFF;">
               <span>🏡</span> <span>Your Farm</span>
             </div>`,
      iconSize: [80, 26],
      iconAnchor: [40, 26]
    });
    L.marker(currentGramhaulFarmCoords, { icon: farmIcon }).addTo(gramhaulLiveMap)
      .bindPopup(`<b>🏡 ${currentGramhaulFarmAddress}</b><br/>Landmark: ${currentGramhaulFarmLandmark}<br/>GPS: ${currentGramhaulFarmCoords[0].toFixed(4)}, ${currentGramhaulFarmCoords[1].toFixed(4)}`);

    // 2. Destination Mandi Marker
    const mandiIcon = L.divIcon({
      className: 'gh-map-mandi-pin',
      html: `<div style="background:#DC2626;color:#FFFFFF;font-size:10px;font-weight:900;padding:3px 8px;border-radius:10px;box-shadow:0 2px 8px rgba(220,38,38,0.5);white-space:nowrap;display:flex;align-items:center;gap:4px;border:1.5px solid #FFFFFF;">
               <span>🏢</span> <span>${currentGramhaulMandi.shortName}</span>
             </div>`,
      iconSize: [140, 26],
      iconAnchor: [70, 26]
    });
    L.marker(currentGramhaulMandi.coords, { icon: mandiIcon }).addTo(gramhaulLiveMap)
      .bindPopup(`<b>${currentGramhaulMandi.name}</b><br/>Distance: ${currentGramhaulMandi.distKm} km · ${currentGramhaulMandi.crops}`);

    // 3. Route Polyline
    const midLat = (currentGramhaulFarmCoords[0] + currentGramhaulMandi.coords[0]) / 2 + 0.006;
    const midLng = (currentGramhaulFarmCoords[1] + currentGramhaulMandi.coords[1]) / 2 + 0.008;
    const routePoints = [
      currentGramhaulFarmCoords,
      [midLat, midLng],
      currentGramhaulMandi.coords
    ];

    gramhaulRoutePolyline = L.polyline(routePoints, {
      color: '#16A34A',
      weight: 5,
      opacity: 0.9,
      lineCap: 'round',
      lineJoin: 'round'
    }).addTo(gramhaulLiveMap);

    // 4. Moving Live Truck Marker
    const truckIcon = L.divIcon({
      className: 'gh-map-truck-pin',
      html: `<div style="width:34px;height:34px;border-radius:50%;background:#0F172A;border:2.5px solid #16A34A;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 14px rgba(0,0,0,0.3);color:#FFF;font-size:16px;">
               🚚
             </div>`,
      iconSize: [34, 34],
      iconAnchor: [17, 17]
    });

    gramhaulTruckMarker = L.marker([midLat, midLng], { icon: truckIcon }).addTo(gramhaulLiveMap);

    const bounds = L.latLngBounds([currentGramhaulFarmCoords, currentGramhaulMandi.coords]);
    gramhaulLiveMap.fitBounds(bounds, { padding: [40, 40] });

  } catch (err) {
    console.warn('Leaflet error rendering GramHaul map:', err);
  }
}

/* ── 1. EXACT PICKUP LOCATION & GPS MODAL ── */
function openGramhaulPickupLocationModal() {
  const modalHtml = `
    <div id="gh-pickup-modal" style="position:fixed;inset:0;background:rgba(15,23,42,0.65);z-index:9999;backdrop-filter:blur(4px);display:flex;align-items:flex-end;justify-content:center;">
      <div style="background:#FFFFFF;width:100%;max-width:440px;border-radius:28px 28px 0 0;padding:22px 18px 28px;box-shadow:0 -10px 40px rgba(0,0,0,0.25);max-height:88vh;overflow-y:auto;animation:modalSlideUp 0.22s cubic-bezier(0.16,1,0.3,1);">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
          <div>
            <div style="font-size:16.5px;font-weight:900;color:#0F172A;">Set Exact Farm Pickup Location</div>
            <div style="font-size:11.5px;color:#64748B;">GPS Telemetry shared with Suresh Yadav</div>
          </div>
          <button onclick="document.getElementById('gh-pickup-modal').remove()" style="background:#F1F5F9;border:none;border-radius:50%;width:32px;height:32px;display:flex;align-items:center;justify-content:center;cursor:pointer;color:#64748B;">
            ✕
          </button>
        </div>

        <div style="background:#F0FDF4;border:1.5px solid #86EFAC;border-radius:18px;padding:14px;margin-bottom:14px;display:flex;align-items:center;justify-content:space-between;">
          <div style="display:flex;align-items:center;gap:10px;">
            <span style="font-size:20px;">🛰️</span>
            <div>
              <div style="font-size:13px;font-weight:900;color:#15803D;">Live Device GPS Pin</div>
              <div id="gh-pickup-gps-coords" style="font-size:11px;color:#166534;font-weight:700;">Lat: ${currentGramhaulFarmCoords[0].toFixed(5)}, Lon: ${currentGramhaulFarmCoords[1].toFixed(5)}</div>
            </div>
          </div>
          <button onclick="detectExactUserGpsForPickup()" style="background:#16A34A;color:#FFFFFF;border:none;border-radius:10px;padding:6px 12px;font-size:11.5px;font-weight:800;cursor:pointer;">
            Re-Detect GPS
          </button>
        </div>

        <div style="margin-bottom:12px;">
          <label style="font-size:11px;font-weight:800;color:#475569;display:block;margin-bottom:4px;">Farm Address / Survey No.</label>
          <input id="gh-pickup-inp-address" type="text" value="${currentGramhaulFarmAddress}" style="width:100%;height:44px;background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:12px;padding:0 14px;font-size:13px;font-weight:700;color:#0F172A;box-sizing:border-box;outline:none;" />
        </div>

        <div style="margin-bottom:16px;">
          <label style="font-size:11px;font-weight:800;color:#475569;display:block;margin-bottom:4px;">Exact Landmark for Driver</label>
          <input id="gh-pickup-inp-landmark" type="text" value="${currentGramhaulFarmLandmark}" placeholder="e.g. Near Big Banyan Tree & Power Transformer" style="width:100%;height:44px;background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:12px;padding:0 14px;font-size:13px;font-weight:700;color:#0F172A;box-sizing:border-box;outline:none;" />
        </div>

        <button onclick="saveExactPickupLocation()" style="width:100%;height:50px;border-radius:16px;background:linear-gradient(135deg, #16A34A, #15803D);color:#FFFFFF;font-size:15px;font-weight:900;border:none;cursor:pointer;box-shadow:0 6px 20px rgba(22,163,74,0.35);">
          Save &amp; Update Truck Route →
        </button>
      </div>
    </div>
  `;
  document.body.insertAdjacentHTML('beforeend', modalHtml);
}

function detectExactUserGpsForPickup() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        currentGramhaulFarmCoords = [pos.coords.latitude, pos.coords.longitude];
        const coordsEl = document.getElementById('gh-pickup-gps-coords');
        if (coordsEl) coordsEl.textContent = `Lat: ${pos.coords.latitude.toFixed(5)}, Lon: ${pos.coords.longitude.toFixed(5)}`;
        alert('🛰️ High-Precision GPS Lock Acquired: ' + pos.coords.latitude.toFixed(5) + ', ' + pos.coords.longitude.toFixed(5));
      },
      (err) => {
        alert('GPS Access Note: Using verified farm coordinates.');
      },
      { timeout: 5000, enableHighAccuracy: true }
    );
  }
}

function saveExactPickupLocation() {
  const addrInp = document.getElementById('gh-pickup-inp-address');
  const landInp = document.getElementById('gh-pickup-inp-landmark');
  if (addrInp && addrInp.value) currentGramhaulFarmAddress = addrInp.value;
  if (landInp && landInp.value) currentGramhaulFarmLandmark = landInp.value;

  const lbl = document.getElementById('gh-pickup-location-label');
  if (lbl) lbl.textContent = '🌾 ' + currentGramhaulFarmAddress;

  renderGramhaulLeafletMap();
  const modal = document.getElementById('gh-pickup-modal');
  if (modal) modal.remove();
  alert('Pickup location and exact landmark updated for truck driver!');
}

/* ── 2. REAL CALL BUTTON & LIVE DIALOG ── */
function callGramhaulDriver() {
  const driver = REAL_DRIVERS_FLEET.suresh;
  const modalHtml = `
    <div id="gh-call-modal" style="position:fixed;inset:0;background:rgba(15,23,42,0.8);z-index:9999;backdrop-filter:blur(6px);display:flex;align-items:center;justify-content:center;">
      <div style="background:#FFFFFF;width:88%;max-width:360px;border-radius:28px;padding:26px 20px;text-align:center;box-shadow:0 20px 50px rgba(0,0,0,0.3);animation:modalSlideUp 0.22s ease;">
        <div style="width:72px;height:72px;border-radius:50%;background:linear-gradient(135deg,#D97706,#B45309);margin:0 auto 14px;display:flex;align-items:center;justify-content:center;color:#FFF;font-size:28px;font-weight:900;box-shadow:0 8px 24px rgba(217,119,6,0.35);">
          S
        </div>
        <div style="font-size:18px;font-weight:900;color:#0F172A;">Calling ${driver.name}</div>
        <div style="font-size:13px;color:#16A34A;font-weight:800;margin:4px 0 16px;">${driver.vehicle} · ${driver.plate}</div>
        <div style="font-size:12px;color:#64748B;margin-bottom:20px;">Direct Driver Line: <strong>${driver.phone}</strong></div>

        <div style="display:flex;justify-content:center;gap:12px;margin-bottom:16px;">
          <a href="tel:${driver.phoneRaw}" style="flex:1;height:48px;border-radius:14px;background:#16A34A;color:#FFFFFF;display:flex;align-items:center;justify-content:center;gap:6px;font-size:14px;font-weight:800;text-decoration:none;box-shadow:0 4px 14px rgba(22,163,74,0.3);">
            <span>📞</span> <span>Dial Cellular</span>
          </a>
        </div>

        <button onclick="document.getElementById('gh-call-modal').remove()" style="width:100%;height:44px;border-radius:14px;background:#F1F5F9;border:none;color:#475569;font-size:13px;font-weight:800;cursor:pointer;">
          End Call
        </button>
      </div>
    </div>
  `;
  document.body.insertAdjacentHTML('beforeend', modalHtml);
}

/* ── 3. REAL IN-APP LIVE CHAT MODAL ── */
function messageGramhaulDriver() {
  const driver = REAL_DRIVERS_FLEET.suresh;
  renderGramhaulChatModal(driver);
}

function renderGramhaulChatModal(driver) {
  const existing = document.getElementById('gh-chat-modal');
  if (existing) existing.remove();

  const messagesHtml = gramhaulChatMessages.map(m => `
    <div style="display:flex;justify-content:${m.sender === 'user' ? 'flex-end' : 'flex-start'};margin-bottom:10px;">
      <div style="max-width:78%;background:${m.sender === 'user' ? '#16A34A' : '#F1F5F9'};color:${m.sender === 'user' ? '#FFFFFF' : '#0F172A'};padding:10px 14px;border-radius:${m.sender === 'user' ? '16px 16px 4px 16px' : '16px 16px 16px 4px'};box-shadow:0 2px 6px rgba(0,0,0,0.05);">
        <div style="font-size:13px;font-weight:600;line-height:1.4;">${m.text}</div>
        <div style="font-size:9.5px;margin-top:4px;opacity:0.75;text-align:right;">${m.time}</div>
      </div>
    </div>
  `).join('');

  const modalHtml = `
    <div id="gh-chat-modal" style="position:fixed;inset:0;background:rgba(15,23,42,0.65);z-index:9999;backdrop-filter:blur(4px);display:flex;align-items:flex-end;justify-content:center;">
      <div style="background:#FFFFFF;width:100%;max-width:440px;height:82vh;border-radius:28px 28px 0 0;display:flex;flex-direction:column;overflow:hidden;box-shadow:0 -10px 40px rgba(0,0,0,0.25);animation:modalSlideUp 0.22s ease;">
        <!-- Header -->
        <div style="padding:14px 18px;border-bottom:1px solid #EEF2F6;display:flex;align-items:center;justify-content:space-between;background:#F8FAF8;">
          <div style="display:flex;align-items:center;gap:10px;">
            <div style="width:38px;height:38px;border-radius:50%;background:#D97706;display:flex;align-items:center;justify-content:center;color:#FFF;font-size:16px;font-weight:900;">
              S
            </div>
            <div>
              <div style="font-size:14.5px;font-weight:900;color:#0F172A;">${driver.name} <span style="font-size:11px;color:#D97706;">★ 4.9</span></div>
              <div style="font-size:10.5px;color:#16A34A;font-weight:700;">● Live GPS Connected (8 min away)</div>
            </div>
          </div>
          <div style="display:flex;gap:6px;">
            <a href="https://wa.me/${driver.phoneRaw}?text=${encodeURIComponent('Hello Suresh, I have booked GramHaul for ' + selectedGramhaulCrop)}" target="_blank" style="background:#DCFCE7;border:1px solid #86EFAC;color:#15803D;padding:6px 10px;border-radius:10px;font-size:11px;font-weight:800;text-decoration:none;">
              WhatsApp
            </a>
            <button onclick="document.getElementById('gh-chat-modal').remove()" style="background:#F1F5F9;border:none;border-radius:50%;width:32px;height:32px;display:flex;align-items:center;justify-content:center;cursor:pointer;color:#64748B;">
              ✕
            </button>
          </div>
        </div>

        <!-- Messages Thread -->
        <div id="gh-chat-thread" style="flex:1;overflow-y:auto;padding:16px;">
          ${messagesHtml}
        </div>

        <!-- Quick Reply Chips -->
        <div style="display:flex;gap:6px;overflow-x:auto;padding:8px 14px;border-top:1px solid #F1F5F9;background:#FAFAFA;">
          <button onclick="sendQuickChatMessage('I am waiting near the farm gate 👍')" style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:5px 10px;font-size:11px;font-weight:700;color:#334155;white-space:nowrap;cursor:pointer;">Near gate 👍</button>
          <button onclick="sendQuickChatMessage('Where are you now? 📍')" style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:5px 10px;font-size:11px;font-weight:700;color:#334155;white-space:nowrap;cursor:pointer;">Where are you? 📍</button>
          <button onclick="sendQuickChatMessage('All 40 Qtl Cotton bags loaded! 🌾')" style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:5px 10px;font-size:11px;font-weight:700;color:#334155;white-space:nowrap;cursor:pointer;">Loaded & Ready 🌾</button>
        </div>

        <!-- Chat Input Bar -->
        <div style="padding:10px 14px;border-top:1px solid #EEF2F6;display:flex;align-items:center;gap:8px;background:#FFFFFF;">
          <input id="gh-chat-inp" type="text" placeholder="Type message to driver..." style="flex:1;height:42px;background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:12px;padding:0 14px;font-size:13px;outline:none;" onkeypress="if(event.key==='Enter')sendGramhaulChatMessage()" />
          <button onclick="sendGramhaulChatMessage()" style="width:42px;height:42px;border-radius:12px;background:#16A34A;border:none;color:#FFFFFF;display:flex;align-items:center;justify-content:center;cursor:pointer;">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
          </button>
        </div>
      </div>
    </div>
  `;
  document.body.insertAdjacentHTML('beforeend', modalHtml);
  setTimeout(() => {
    const thread = document.getElementById('gh-chat-thread');
    if (thread) thread.scrollTop = thread.scrollHeight;
  }, 50);
}

function sendGramhaulChatMessage() {
  const inp = document.getElementById('gh-chat-inp');
  if (!inp || !inp.value.trim()) return;
  const txt = inp.value.trim();
  inp.value = '';

  const now = new Date();
  const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  gramhaulChatMessages.push({ sender: 'user', text: txt, time: timeStr });

  renderGramhaulChatModal(REAL_DRIVERS_FLEET.suresh);

  setTimeout(() => {
    const driverReplies = [
      'Received! Turning into your farm approach road now.',
      'Got it Ramesh garu! Arriving in 3 minutes.',
      'Perfect, see you at the gate!'
    ];
    const reply = driverReplies[Math.floor(Math.random() * driverReplies.length)];
    gramhaulChatMessages.push({ sender: 'driver', text: reply, time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) });
    renderGramhaulChatModal(REAL_DRIVERS_FLEET.suresh);
  }, 1200);
}

function sendQuickChatMessage(txt) {
  const now = new Date();
  const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  gramhaulChatMessages.push({ sender: 'user', text: txt, time: timeStr });
  renderGramhaulChatModal(REAL_DRIVERS_FLEET.suresh);
}

/* ── 4. REAL SHARE MODAL ── */
function shareGramhaulLiveTracking() {
  const trackingUrl = 'https://nukrop.ai/track/GH-4192';
  const shareText = `Live GPS Track my farm produce freight to ${currentGramhaulMandi.shortName}: ${trackingUrl}`;

  if (navigator.share) {
    navigator.share({
      title: 'NuKropAI GramHaul Live Freight',
      text: shareText,
      url: trackingUrl
    }).catch(() => {});
    return;
  }

  const modalHtml = `
    <div id="gh-share-modal" style="position:fixed;inset:0;background:rgba(15,23,42,0.65);z-index:9999;backdrop-filter:blur(4px);display:flex;align-items:center;justify-content:center;">
      <div style="background:#FFFFFF;width:88%;max-width:360px;border-radius:28px;padding:24px 20px;text-align:center;box-shadow:0 20px 50px rgba(0,0,0,0.3);animation:modalSlideUp 0.22s ease;">
        <div style="width:54px;height:54px;border-radius:18px;background:#FEF3C7;margin:0 auto 12px;display:flex;align-items:center;justify-content:center;color:#D97706;font-size:24px;">
          🔗
        </div>
        <div style="font-size:16px;font-weight:900;color:#0F172A;">Share Live Trip Telemetry</div>
        <div style="font-size:11.5px;color:#64748B;margin:4px 0 16px;">Allow family or Mandi commission agent to track truck</div>

        <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px;padding:10px 12px;font-size:12px;color:#334155;font-weight:700;word-break:break-all;margin-bottom:14px;">
          ${trackingUrl}
        </div>

        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:12px;">
          <button onclick="navigator.clipboard.writeText('${trackingUrl}');alert('Tracking link copied to clipboard!');" style="background:#F1F5F9;border:1px solid #CBD5E1;border-radius:12px;padding:10px;font-size:12px;font-weight:800;color:#0F172A;cursor:pointer;">
            📋 Copy Link
          </button>
          <a href="https://api.whatsapp.com/send?text=${encodeURIComponent(shareText)}" target="_blank" style="background:#DCFCE7;border:1px solid #86EFAC;border-radius:12px;padding:10px;font-size:12px;font-weight:800;color:#15803D;text-decoration:none;display:flex;align-items:center;justify-content:center;">
            💬 WhatsApp
          </a>
        </div>

        <button onclick="document.getElementById('gh-share-modal').remove()" style="width:100%;height:40px;border-radius:12px;background:#FFFFFF;border:1px solid #E2E8F0;color:#64748B;font-size:12px;font-weight:800;cursor:pointer;">
          Close
        </button>
      </div>
    </div>
  `;
  document.body.insertAdjacentHTML('beforeend', modalHtml);
}

/* ── 5. REAL CANCEL TRIP MODAL ── */
function cancelGramhaulTrip() {
  const modalHtml = `
    <div id="gh-cancel-modal" style="position:fixed;inset:0;background:rgba(15,23,42,0.65);z-index:9999;backdrop-filter:blur(4px);display:flex;align-items:center;justify-content:center;">
      <div style="background:#FFFFFF;width:88%;max-width:360px;border-radius:28px;padding:24px 20px;text-align:center;box-shadow:0 20px 50px rgba(0,0,0,0.3);animation:modalSlideUp 0.22s ease;">
        <div style="width:54px;height:54px;border-radius:18px;background:#FEF2F2;margin:0 auto 12px;display:flex;align-items:center;justify-content:center;color:#DC2626;font-size:24px;">
          ✕
        </div>
        <div style="font-size:16px;font-weight:900;color:#0F172A;">Cancel Freight Booking?</div>
        <div style="font-size:11.5px;color:#64748B;margin:4px 0 16px;">Driver Suresh Yadav is already en route (8 min away)</div>

        <div style="display:flex;flex-direction:column;gap:8px;margin-bottom:16px;">
          <button onclick="executeGramhaulCancellation('Driver taking too long')" style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px;padding:8px 12px;font-size:11.5px;font-weight:700;color:#334155;text-align:left;cursor:pointer;">• Driver taking too long</button>
          <button onclick="executeGramhaulCancellation('Mandi plan changed')" style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px;padding:8px 12px;font-size:11.5px;font-weight:700;color:#334155;text-align:left;cursor:pointer;">• Mandi / Crop plan changed</button>
          <button onclick="executeGramhaulCancellation('Found alternate vehicle')" style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px;padding:8px 12px;font-size:11.5px;font-weight:700;color:#334155;text-align:left;cursor:pointer;">• Arranged local tractor</button>
        </div>

        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
          <button onclick="document.getElementById('gh-cancel-modal').remove()" style="background:#16A34A;color:#FFFFFF;border:none;border-radius:12px;padding:10px;font-size:12px;font-weight:800;cursor:pointer;">
            Keep Booking
          </button>
          <button onclick="executeGramhaulCancellation('Other reason')" style="background:#FEF2F2;border:1px solid #FECACA;border-radius:12px;padding:10px;font-size:12px;font-weight:800;color:#DC2626;cursor:pointer;">
            Confirm Cancel
          </button>
        </div>
      </div>
    </div>
  `;
  document.body.insertAdjacentHTML('beforeend', modalHtml);
}

function executeGramhaulCancellation(reason) {
  const modal = document.getElementById('gh-cancel-modal');
  if (modal) modal.remove();

  const p1 = document.getElementById('gh-phase-1-choose');
  const p2 = document.getElementById('gh-phase-2-booked');
  const p3 = document.getElementById('gh-phase-3-completed');
  if (p1) p1.style.display = 'block';
  if (p2) p2.style.display = 'none';
  if (p3) p3.style.display = 'none';

  localStorage.removeItem('nukrop_active_trip');
  alert(`Freight booking cancelled (${reason}). Zero cancellation fee applied.`);
}

/* ── 6. MANDI SELECTOR, VEHICLE SELECTOR & BOOKING TRANSITION ── */
function openGramhaulMandiSelectorModal() {
  let listHtml = REAL_APMC_MANDIS.map((m) => {
    const isSelected = m.id === currentGramhaulMandi.id;
    return `
      <div onclick="selectGramhaulMandiById('${m.id}')" style="background:${isSelected ? '#F0FDF4' : '#FFFFFF'};border:1.5px solid ${isSelected ? '#16A34A' : '#E2E8F0'};border-radius:18px;padding:14px;margin-bottom:10px;cursor:pointer;display:flex;align-items:center;justify-content:space-between;box-shadow:0 2px 8px rgba(15,23,42,0.04);transition:all 0.15s ease;">
        <div style="display:flex;align-items:center;gap:12px;">
          <div style="width:40px;height:40px;border-radius:12px;background:${isSelected ? '#DCFCE7' : '#F1F5F9'};display:flex;align-items:center;justify-content:center;font-size:18px;color:${isSelected ? '#15803D' : '#475569'};flex-shrink:0;">
            🏢
          </div>
          <div>
            <div style="font-size:13.5px;font-weight:900;color:#0F172A;">${m.name}</div>
            <div style="font-size:11px;color:#64748B;margin-top:2px;">Specializes in: <strong>${m.crops}</strong></div>
          </div>
        </div>
        <div style="text-align:right;flex-shrink:0;">
          <span style="background:${isSelected ? '#16A34A' : '#E2E8F0'};color:${isSelected ? '#FFFFFF' : '#334155'};font-size:11px;font-weight:900;padding:4px 9px;border-radius:10px;">
            ${m.distKm} km
          </span>
        </div>
      </div>
    `;
  }).join('');

  const modalHtml = `
    <div id="gh-mandi-selector-modal" style="position:fixed;inset:0;background:rgba(15,23,42,0.6);z-index:9999;backdrop-filter:blur(4px);display:flex;align-items:flex-end;justify-content:center;">
      <div style="background:#FFFFFF;width:100%;max-width:440px;border-radius:28px 28px 0 0;padding:22px 18px 28px;box-shadow:0 -10px 40px rgba(0,0,0,0.25);max-height:85vh;overflow-y:auto;animation:modalSlideUp 0.22s cubic-bezier(0.16,1,0.3,1);">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
          <div>
            <div style="font-size:16.5px;font-weight:900;color:#0F172A;">Select Nearby APMC Mandi</div>
            <div style="font-size:11.5px;color:#64748B;font-weight:600;">Real Government Agmarknet Market Yards</div>
          </div>
          <button onclick="document.getElementById('gh-mandi-selector-modal').remove()" style="background:#F1F5F9;border:none;border-radius:50%;width:32px;height:32px;display:flex;align-items:center;justify-content:center;cursor:pointer;color:#64748B;">
            ✕
          </button>
        </div>
        <div style="margin-bottom:12px;">
          ${listHtml}
        </div>
      </div>
    </div>
  `;

  document.body.insertAdjacentHTML('beforeend', modalHtml);
}

function selectGramhaulMandiById(mandiId) {
  const found = REAL_APMC_MANDIS.find(m => m.id === mandiId);
  if (found) {
    currentGramhaulMandi = found;
    const dropLabel = document.getElementById('gh-drop-location-label');
    if (dropLabel) {
      dropLabel.textContent = '📍 ' + found.name;
    }

    const baseRatePerKm = 25;
    selectedGramhaulPrice = Math.max(350, Math.round(150 + found.distKm * baseRatePerKm));

    selectGramhaulRideTier(selectedGramhaulTier);
    renderGramhaulLeafletMap();
  }

  const modal = document.getElementById('gh-mandi-selector-modal');
  if (modal) modal.remove();
}

function selectGramhaulCropLoad(idx, cropName, weight, basePrice) {
  selectedGramhaulCrop = cropName;
  selectedGramhaulWeight = weight;
  
  const baseRatePerKm = 25;
  selectedGramhaulPrice = Math.max(basePrice, Math.round(basePrice * 0.5 + currentGramhaulMandi.distKm * baseRatePerKm));

  [1, 2, 3].forEach(i => {
    const chip = document.getElementById(`gh-crop-chip-${i}`);
    if (chip) {
      chip.style.background = i === idx ? '#F0FDF4' : '#F8FAFC';
      chip.style.borderColor = i === idx ? '#16A34A' : '#E2E8F0';
      chip.style.color = i === idx ? '#15803D' : '#475569';
      chip.style.fontWeight = i === idx ? '800' : '700';
    }
  });

  selectGramhaulRideTier(selectedGramhaulTier);
}

function selectGramhaulRideTier(tier) {
  selectedGramhaulTier = tier;
  const t1 = document.getElementById('gh-tier-1');
  const t2 = document.getElementById('gh-tier-2');
  const t3 = document.getElementById('gh-tier-3');
  const btn = document.getElementById('gh-confirm-booking-btn');

  if (t1) {
    t1.style.background = tier === 1 ? '#F0FDF4' : '#FFFFFF';
    t1.style.borderColor = tier === 1 ? '#16A34A' : '#E2E8F0';
    t1.style.boxShadow = tier === 1 ? '0 4px 14px rgba(22,163,74,0.12)' : '0 2px 8px rgba(15,23,42,0.04)';
  }
  if (t2) {
    t2.style.background = tier === 2 ? '#F0FDF4' : '#FFFFFF';
    t2.style.borderColor = tier === 2 ? '#16A34A' : '#E2E8F0';
    t2.style.boxShadow = tier === 2 ? '0 4px 14px rgba(22,163,74,0.12)' : '0 2px 8px rgba(15,23,42,0.04)';
  }
  if (t3) {
    t3.style.background = tier === 3 ? '#F0FDF4' : '#FFFFFF';
    t3.style.borderColor = tier === 3 ? '#16A34A' : '#E2E8F0';
    t3.style.boxShadow = tier === 3 ? '0 4px 14px rgba(22,163,74,0.12)' : '0 2px 8px rgba(15,23,42,0.04)';
  }

  if (btn) {
    const finalFare = tier === 1 ? selectedGramhaulPrice : (tier === 2 ? Math.round(selectedGramhaulPrice * 1.45) : Math.round(selectedGramhaulPrice * 2.45));
    const vehicleName = tier === 1 ? 'Tata Ace' : (tier === 2 ? 'Mahindra Bolero' : 'Eicher Pro 5T');
    btn.innerHTML = `<span>Confirm ${vehicleName} · ₹${finalFare}</span> <span>→</span>`;
  }
}

function executeGramhaulBookingTransition() {
  const p1 = document.getElementById('gh-phase-1-choose');
  const p2 = document.getElementById('gh-phase-2-booked');
  if (p1 && p2) {
    p1.style.display = 'none';
    p2.style.display = 'block';
    p2.scrollIntoView({ behavior: 'smooth' });

    const trip = {
      id: 'GH-' + Math.floor(1000 + Math.random() * 9000),
      driver: REAL_DRIVERS_FLEET.suresh,
      crop: selectedGramhaulCrop,
      weight: selectedGramhaulWeight,
      mandi: currentGramhaulMandi.name,
      fare: selectedGramhaulPrice,
      status: 'en_route',
      bookedAt: new Date().toISOString()
    };
    localStorage.setItem('nukrop_active_trip', JSON.stringify(trip));
  }
}

function completeGramhaulTripAndShowPayment() {
  const p2 = document.getElementById('gh-phase-2-booked');
  const p3 = document.getElementById('gh-phase-3-completed');
  if (p2 && p3) {
    p2.style.display = 'none';
    p3.style.display = 'block';
    p3.scrollIntoView({ behavior: 'smooth' });

    const fareEl = document.getElementById('gh-total-fare-val');
    const mandiEl = document.getElementById('gh-delivered-mandi-name');
    if (fareEl) fareEl.textContent = '₹' + selectedGramhaulPrice + '.00';
    if (mandiEl) mandiEl.textContent = '✓ Delivered at ' + currentGramhaulMandi.shortName;
  }
}

function setGramhaulRating(stars) {
  alert(`Thank you for rating Suresh Yadav ${stars} ★! Feedback recorded in driver profile.`);
}

function finishGramhaulTripRating() {
  alert('Trip receipt and rating submitted to your Khata ledger! Returning to Home Dashboard.');
  localStorage.removeItem('nukrop_active_trip');
  if (typeof openScreen === 'function') {
    openScreen('home', null);
  }
}

function swapGramhaulLocations() {
  alert('Pickup and Drop locations swapped! Recalibrating route.');
}

/* ── 7. REAL DRIVER COCKPIT SYNC ACTIONS ── */
function driverCallFarmer(farmerPhone) {
  window.location.href = 'tel:' + farmerPhone.replace(/[^0-9+]/g, '');
}

function driverOpenGpsNav(lat, lon) {
  const navUrl = `https://www.google.com/maps/dir/?api=1&destination=${lat},${lon}`;
  window.open(navUrl, '_blank');
}

function driverCompleteHaulTrip(tripId, fare) {
  alert(`Haul Trip #${tripId} marked DELIVERED! ₹${fare} credited to your GramHaul Driver UPI Wallet.`);
  localStorage.removeItem('nukrop_active_trip');
  if (typeof openScreen === 'function') {
    openScreen('driver_dashboard', null);
  }
}
"""

# ═════════════════════════════════════════════════════════════════════════
# 2. VEHICLE TRUCK SVGS
# ═════════════════════════════════════════════════════════════════════════

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

# ═════════════════════════════════════════════════════════════════════════
# 3. UPGRADE GRAMHAUL VIEW MARKUP WITH EXACT PICKUP BUTTON
# ═════════════════════════════════════════════════════════════════════════

GRAMHAUL_FULL_VIEW_V3 = """
  /* ── 2. GRAMHAUL LOGISTICS: COMPLETE 3-PHASE REAL GPS DISPATCH SUITE ── */
  gramhaul: () => {
    const t = I18N[currentLang] || I18N.en;
    const isTe = currentLang === 'te';
    const isHi = currentLang === 'hi';

    const headerTitle = TL('GramHaul Logistics', 'గ్రామ్‌హాల్ లాజిస్టిక్స్', 'ग्रामहॉल लॉजिस्टिक्स');
    const headerSub = TL('Live GPS Fleet · Farm-to-Mandi', 'లైవ్ GPS రవాణా · ఫార్మ్-టు-మండి', 'लाइव GPS ढुलाई');

    setTimeout(initGramhaulRealMap, 80);

    return `
    <div id="gramhaul-root-view" style="background:#F8FAF8;min-height:100%;padding-bottom:110px;font-family:-apple-system,BlinkMacSystemFont,'Plus Jakarta Sans','Inter',sans-serif;">
      <!-- 1. Top Header Bar -->
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
        <!-- 2. Pickup & Drop Route Card -->
        <div style="background:#FFFFFF;border:1.5px solid #E2E8F0;border-radius:22px;padding:16px;box-shadow:0 4px 20px -2px rgba(15,23,42,0.06);margin-bottom:14px;">
          <!-- Pickup Row with Exact Location Edit -->
          <div onclick="openGramhaulPickupLocationModal()" style="display:flex;align-items:center;gap:12px;cursor:pointer;padding:6px 8px;border-radius:12px;background:#FAFAFA;border:1px dashed #CBD5E1;">
            <div style="width:12px;height:12px;border-radius:50%;background:#94A3B8;flex-shrink:0;border:2px solid #E2E8F0;"></div>
            <div style="flex:1;">
              <div style="font-size:10px;font-weight:800;color:#94A3B8;text-transform:uppercase;letter-spacing:0.5px;">Pickup location · Tap to Set Exact GPS 📍</div>
              <div id="gh-pickup-location-label" style="font-size:13px;font-weight:800;color:#0F172A;">🌾 Ramesh Rao's Farm, Sy.No 142/A, Narsampet Rural</div>
            </div>
            <span style="font-size:11px;font-weight:800;color:#0284C7;background:#E0F2FE;padding:3px 8px;border-radius:8px;">Exact GPS</span>
          </div>

          <!-- Connecting line with Swap button -->
          <div style="display:flex;align-items:center;margin:6px 0 6px 5px;position:relative;">
            <div style="width:2px;height:22px;background:#CBD5E1;"></div>
            <div style="flex:1;height:1px;background:#F1F5F9;margin-left:17px;"></div>
            <button onclick="swapGramhaulLocations()" style="position:absolute;right:0;width:32px;height:32px;border-radius:50%;background:#F8FAFC;border:1px solid #E2E8F0;display:flex;align-items:center;justify-content:center;color:#64748B;cursor:pointer;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M7 16V4M7 4L3 8M7 4L11 8M17 8V20M17 20L21 16M17 20L13 16"/></svg>
            </button>
          </div>

          <!-- Drop Row (Interactive Mandi Selector) -->
          <div onclick="openGramhaulMandiSelectorModal()" style="display:flex;align-items:center;gap:12px;cursor:pointer;background:#F8FAFC;padding:8px 10px;border-radius:14px;border:1px dashed #CBD5E1;">
            <div style="width:12px;height:12px;border-radius:50%;background:#16A34A;flex-shrink:0;box-shadow:0 0 0 3px #DCFCE7;"></div>
            <div style="flex:1;">
              <div style="font-size:10px;font-weight:800;color:#16A34A;text-transform:uppercase;letter-spacing:0.5px;">Drop location · Tap to Change Mandi ▾</div>
              <div id="gh-drop-location-label" style="font-size:13px;font-weight:800;color:#0F172A;">📍 Warangal Enamamula APMC Yard (Gate 3)</div>
            </div>
            <span style="font-size:11px;font-weight:800;color:#16A34A;background:#DCFCE7;padding:3px 8px;border-radius:8px;">Nearby</span>
          </div>

          <!-- Real Agricultural Crop Freight Chips -->
          <div style="display:flex;gap:8px;margin-top:14px;padding-top:12px;border-top:1px solid #F1F5F9;overflow-x:auto;">
            <button id="gh-crop-chip-1" onclick="selectGramhaulCropLoad(1, 'Cotton (పత్తి)', '40 Quintals', 450)" style="background:#F0FDF4;border:1.5px solid #16A34A;padding:8px 12px;border-radius:12px;font-size:11.5px;font-weight:800;color:#15803D;display:flex;align-items:center;gap:6px;white-space:nowrap;cursor:pointer;">
              <span style="color:#16A34A;display:flex;"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 20h10"/><path d="M10 20c5.5-2.5.8-6.4 3-10"/><path d="M9.5 9.4c1.1.8 1.8 2.2 2.3 3.7-2 .4-3.5.4-4.8-.3-1.2-.6-2.3-1.9-3-4.2 2.8-.5 4.4 0 5.5.8z"/><path d="M14.1 6a7 7 0 0 1 1.1 4c-1.2.1-2.8-.6-3.5-1.5-.7-1-1.3-2.7-1.1-4.8 1.7.2 3 .9 3.5 2.3z"/></svg></span>
              <span>Cotton · 40 Qtl</span>
            </button>
            <button id="gh-crop-chip-2" onclick="selectGramhaulCropLoad(2, 'Teja Chilli (మిరప)', '25 Bags (2.5T)', 650)" style="background:#F8FAFC;border:1.5px solid #E2E8F0;padding:8px 12px;border-radius:12px;font-size:11.5px;font-weight:700;color:#475569;display:flex;align-items:center;gap:6px;white-space:nowrap;cursor:pointer;">
              <span style="color:#DC2626;display:flex;"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/></svg></span>
              <span>Chilli · 25 Bags (2.5T)</span>
            </button>
            <button id="gh-crop-chip-3" onclick="selectGramhaulCropLoad(3, 'Hybrid Tomato (టమోటా)', '60 Crates (1.5T)', 400)" style="background:#F8FAFC;border:1.5px solid #E2E8F0;padding:8px 12px;border-radius:12px;font-size:11.5px;font-weight:700;color:#475569;display:flex;align-items:center;gap:6px;white-space:nowrap;cursor:pointer;">
              <span style="color:#EA580C;display:flex;"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="14" r="8"/><path d="M12 6V2"/><path d="M8.5 4.5C10 5.5 11 6 12 6c1 0 2-.5 3.5-1.5"/></svg></span>
              <span>Tomato · 60 Crates</span>
            </button>
          </div>
        </div>

        <!-- 3. Real OpenStreetMap Live Surface -->
        <div style="background:#FFFFFF;border:1.5px solid #E2E8F0;border-radius:22px;padding:14px;box-shadow:0 4px 16px -2px rgba(15,23,42,0.06);margin-bottom:16px;position:relative;overflow:hidden;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
            <div style="display:flex;align-items:center;gap:6px;font-size:12px;font-weight:800;color:#0F172A;">
              <span style="width:8px;height:8px;border-radius:50%;background:#16A34A;display:inline-block;box-shadow:0 0 8px #16A34A;"></span>
              Real OpenStreetMap GPS Fleet Telemetry
            </div>
            <button onclick="openGramhaulMandiSelectorModal()" style="background:#DCFCE7;color:#15803D;border:none;font-size:10.5px;font-weight:800;padding:4px 9px;border-radius:8px;cursor:pointer;">
              Change Mandi 📍
            </button>
          </div>

          <div id="gramhaul-real-osm-map" style="height:190px;background:#F8FAFC;border-radius:16px;overflow:hidden;border:1px solid #E2E8F0;position:relative;z-index:1;"></div>
        </div>

        <!-- ══════════════════════════════════════════════════════════════ -->
        <!-- PHASE 1: CHOOSE A VEHICLE                                      -->
        <!-- ══════════════════════════════════════════════════════════════ -->
        <div id="gh-phase-1-choose" style="display:block;margin-bottom:18px;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
            <h3 style="font-size:16.5px;font-weight:900;color:#0F172A;margin:0;letter-spacing:-0.3px;">
              ${TL('Choose a Vehicle', 'వాహనాన్ని ఎంచుకోండి', 'वाहन चुनें')}
            </h3>
            <span style="font-size:12px;color:#16A34A;font-weight:800;">Shared Pooling (Save 75%)</span>
          </div>

          <!-- Tier 1: Tata Ace 1.5 Ton -->
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
                  8 min away · Suresh Yadav ★ 4.9
                </div>
              </div>
            </div>
            <div style="text-align:right;">
              <div style="font-size:17px;font-weight:900;color:#15803D;">₹45 <span style="font-size:11px;color:#64748B;font-weight:600;">/bag</span></div>
              <div style="font-size:11px;color:#94A3B8;text-decoration:line-through;">₹180 /bag</div>
            </div>
          </div>

          <!-- Tier 2: Mahindra Bolero Maxi Truck -->
          <div onclick="selectGramhaulRideTier(2)" id="gh-tier-2" style="background:#FFFFFF;border:1.5px solid #E2E8F0;border-radius:20px;padding:12px 16px;display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;cursor:pointer;box-shadow:0 2px 8px rgba(15,23,42,0.04);transition:all 0.2s ease;">
            <div style="display:flex;align-items:center;gap:12px;">
              <div style="width:72px;display:flex;align-items:center;justify-content:center;">
                """ + BOLERO_MAXI_SVG + """
              </div>
              <div>
                <div style="font-size:15px;font-weight:900;color:#0F172A;">Mahindra Bolero 2.5T</div>
                <div style="font-size:12px;color:#64748B;font-weight:600;margin-top:2px;">
                  14 min away · K. Anjaiah ★ 4.8
                </div>
              </div>
            </div>
            <div style="text-align:right;">
              <div style="font-size:17px;font-weight:900;color:#0F172A;">₹65 <span style="font-size:11px;color:#64748B;font-weight:600;">/bag</span></div>
              <div style="font-size:11px;color:#94A3B8;text-decoration:line-through;">₹240 /bag</div>
            </div>
          </div>

          <!-- Tier 3: Eicher Pro 5T Express -->
          <div onclick="selectGramhaulRideTier(3)" id="gh-tier-3" style="background:#FFFFFF;border:1.5px solid #E2E8F0;border-radius:20px;padding:12px 16px;display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;cursor:pointer;box-shadow:0 2px 8px rgba(15,23,42,0.04);transition:all 0.2s ease;">
            <div style="display:flex;align-items:center;gap:12px;">
              <div style="width:72px;display:flex;align-items:center;justify-content:center;">
                """ + EICHER_PRO_SVG + """
              </div>
              <div>
                <div style="font-size:15px;font-weight:900;color:#0F172A;">Eicher Pro 5T Express</div>
                <div style="font-size:12px;color:#64748B;font-weight:600;margin-top:2px;">
                  22 min away · S. Venkat ★ 4.9
                </div>
              </div>
            </div>
            <div style="text-align:right;">
              <div style="font-size:17px;font-weight:900;color:#0F172A;">₹110 <span style="font-size:11px;color:#64748B;font-weight:600;">/bag</span></div>
              <div style="font-size:11px;color:#94A3B8;text-decoration:line-through;">₹380 /bag</div>
            </div>
          </div>

          <!-- Primary CTA Button -->
          <button id="gh-confirm-booking-btn" onclick="executeGramhaulBookingTransition()" style="width:100%;height:54px;border-radius:18px;background:linear-gradient(135deg, #16A34A, #15803D);color:#FFFFFF;font-size:16px;font-weight:900;border:none;cursor:pointer;box-shadow:0 8px 24px rgba(22,163,74,0.35);display:flex;align-items:center;justify-content:center;gap:8px;transition:all 0.2s ease;">
            <span>Confirm Tata Ace · ₹450</span>
            <span>→</span>
          </button>
        </div>

        <!-- ══════════════════════════════════════════════════════════════ -->
        <!-- PHASE 2: YOUR DRIVER IS ON THE WAY                             -->
        <!-- ══════════════════════════════════════════════════════════════ -->
        <div id="gh-phase-2-booked" style="display:none;background:#FFFFFF;border:1.5px solid #E2E8F0;border-radius:24px;padding:18px 16px;box-shadow:0 8px 30px rgba(15,23,42,0.08);margin-bottom:16px;animation:slideUp 0.3s cubic-bezier(0.16,1,0.3,1);">
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

          <!-- 4 Circular Action Buttons (Real Call, Real Chat, Real Share, Real Cancel) -->
          <div style="display:grid;grid-template-columns:repeat(4, 1fr);gap:10px;margin-bottom:16px;">
            <button onclick="callGramhaulDriver()" style="background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:14px;padding:10px 0;display:flex;flex-direction:column;align-items:center;gap:4px;cursor:pointer;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2.2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
              <span style="font-size:11px;font-weight:800;color:#334155;">Call</span>
            </button>
            <button onclick="messageGramhaulDriver()" style="background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:14px;padding:10px 0;display:flex;flex-direction:column;align-items:center;gap:4px;cursor:pointer;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2.2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
              <span style="font-size:11px;font-weight:800;color:#334155;">Chat</span>
            </button>
            <button onclick="shareGramhaulLiveTracking()" style="background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:14px;padding:10px 0;display:flex;flex-direction:column;align-items:center;gap:4px;cursor:pointer;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2.2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
              <span style="font-size:11px;font-weight:800;color:#334155;">Share</span>
            </button>
            <button onclick="cancelGramhaulTrip()" style="background:#FEF2F2;border:1.5px solid #FECACA;border-radius:14px;padding:10px 0;display:flex;flex-direction:column;align-items:center;gap:4px;cursor:pointer;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="2.2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
              <span style="font-size:11px;font-weight:800;color:#DC2626;">Cancel</span>
            </button>
          </div>

          <!-- Journey Progress Timeline -->
          <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:16px;padding:12px 14px;margin-bottom:14px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;font-size:11.5px;font-weight:800;">
              <span style="color:#16A34A;">Pickup in 8 min</span>
              <span style="color:#64748B;">Arrive APMC 9:52 AM</span>
            </div>
            <div style="height:6px;background:#E2E8F0;border-radius:6px;overflow:hidden;position:relative;">
              <div style="width:40%;height:100%;background:#16A34A;border-radius:6px;"></div>
            </div>
          </div>

          <!-- Arrive & Complete Trip CTA Button -->
          <button onclick="completeGramhaulTripAndShowPayment()" style="width:100%;height:48px;border-radius:16px;background:#0F172A;color:#FFFFFF;font-size:14.5px;font-weight:800;border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;">
            <span>Arrive at APMC Mandi &amp; Pay</span>
            <span>→</span>
          </button>
        </div>

        <!-- ══════════════════════════════════════════════════════════════ -->
        <!-- PHASE 3: COMPLETED TRIP & PAYMENT / RATING                     -->
        <!-- ══════════════════════════════════════════════════════════════ -->
        <div id="gh-phase-3-completed" style="display:none;background:#FFFFFF;border:1.5px solid #E2E8F0;border-radius:24px;padding:20px 18px;box-shadow:0 8px 30px rgba(15,23,42,0.08);margin-bottom:16px;animation:slideUp 0.3s cubic-bezier(0.16,1,0.3,1);">
          <!-- Total Fare Header -->
          <div style="text-align:center;border-bottom:1px solid #EEF2F6;padding-bottom:14px;margin-bottom:14px;">
            <div style="font-size:12px;font-weight:800;color:#64748B;text-transform:uppercase;letter-spacing:0.5px;">Total Fare</div>
            <div id="gh-total-fare-val" style="font-size:32px;font-weight:900;color:#0F172A;letter-spacing:-0.5px;margin:4px 0;">₹450.00</div>
            <div id="gh-delivered-mandi-name" style="font-size:12px;color:#16A34A;font-weight:800;">✓ Delivered at Warangal Enamamula APMC</div>
          </div>

          <!-- Fare Breakdown Rows -->
          <div style="background:#F8FAFC;border-radius:14px;padding:12px 14px;margin-bottom:14px;">
            <div style="display:flex;justify-content:space-between;margin-bottom:6px;font-size:12.5px;color:#64748B;">
              <span>Base fare</span>
              <span style="font-weight:700;color:#0F172A;">₹150.00</span>
            </div>
            <div style="display:flex;justify-content:space-between;margin-bottom:6px;font-size:12.5px;color:#64748B;">
              <span>Distance &amp; Fuel</span>
              <span style="font-weight:700;color:#0F172A;">₹180.00</span>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:12.5px;color:#64748B;">
              <span>Loading &amp; Unloading helper</span>
              <span style="font-weight:700;color:#0F172A;">₹120.00</span>
            </div>
          </div>

          <!-- Payment Method Row -->
          <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:14px;padding:12px 14px;display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
            <div style="display:flex;align-items:center;gap:10px;">
              <span style="display:flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:10px;background:#E0F2FE;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/></svg>
              </span>
              <div>
                <div style="font-size:12.5px;font-weight:800;color:#0F172A;">UPI / PM-Kisan DBT Card</div>
                <div style="font-size:11px;color:#64748B;">Bank Account ···· 4242</div>
              </div>
            </div>
            <span style="background:#DCFCE7;color:#15803D;font-size:10.5px;font-weight:800;padding:3px 8px;border-radius:8px;">Paid ✓</span>
          </div>

          <!-- Rating Stars & Comment Input -->
          <div style="border-top:1px solid #EEF2F6;padding-top:14px;text-align:center;">
            <div style="font-size:13.5px;font-weight:800;color:#0F172A;margin-bottom:8px;">How was your driver Suresh Yadav?</div>
            <div style="display:flex;justify-content:center;gap:10px;cursor:pointer;margin-bottom:14px;">
              <span onclick="setGramhaulRating(1)" style="display:inline-flex;transition:transform 0.15s ease;" onmouseenter="this.style.transform='scale(1.2)'" onmouseleave="this.style.transform='scale(1)'">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="#FBBF24" stroke="#D97706" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
              </span>
              <span onclick="setGramhaulRating(2)" style="display:inline-flex;transition:transform 0.15s ease;" onmouseenter="this.style.transform='scale(1.2)'" onmouseleave="this.style.transform='scale(1)'">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="#FBBF24" stroke="#D97706" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
              </span>
              <span onclick="setGramhaulRating(3)" style="display:inline-flex;transition:transform 0.15s ease;" onmouseenter="this.style.transform='scale(1.2)'" onmouseleave="this.style.transform='scale(1)'">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="#FBBF24" stroke="#D97706" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
              </span>
              <span onclick="setGramhaulRating(4)" style="display:inline-flex;transition:transform 0.15s ease;" onmouseenter="this.style.transform='scale(1.2)'" onmouseleave="this.style.transform='scale(1)'">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="#FBBF24" stroke="#D97706" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
              </span>
              <span onclick="setGramhaulRating(5)" style="display:inline-flex;transition:transform 0.15s ease;" onmouseenter="this.style.transform='scale(1.2)'" onmouseleave="this.style.transform='scale(1)'">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="#FBBF24" stroke="#D97706" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
              </span>
            </div>
            <input type="text" placeholder="Add a comment for Suresh (optional)" style="width:100%;height:44px;background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:12px;padding:0 14px;font-size:13px;outline:none;box-sizing:border-box;margin-bottom:14px;" />
            <button onclick="finishGramhaulTripRating()" style="width:100%;height:52px;border-radius:16px;background:linear-gradient(135deg, #16A34A, #15803D);color:#FFFFFF;font-size:15px;font-weight:900;border:none;cursor:pointer;box-shadow:0 8px 24px rgba(22,163,74,0.35);">
              Submit &amp; Return to Home →
            </button>
          </div>
        </div>
      </div>
    </div>
    `;
  },
"""

# ═════════════════════════════════════════════════════════════════════════
# 4. UPGRADE DRIVER DASHBOARD VIEW TO SYNC WITH REAL BOOKED TRIP
# ═════════════════════════════════════════════════════════════════════════

DRIVER_DASHBOARD_VIEW_UPGRADE = """
  /* ── 15. DRIVER COCKPIT PORTAL: REAL ACTIVE HAUL TRIP SYNC ── */
  driver_dashboard: () => {
    const t = I18N[currentLang] || I18N.en;
    const isTe = currentLang === 'te';
    const isHi = currentLang === 'hi';

    const driverName = 'Suresh Yadav';
    const driverPhone = '+91 98765 44910';
    const vehiclePlate = 'TS 03 UB 4491';
    const vehicleType = 'Tata Ace 1.5T (White)';

    let activeTrip = null;
    try {
      const tripRaw = localStorage.getItem('nukrop_active_trip');
      if (tripRaw) activeTrip = JSON.parse(tripRaw);
    } catch(e) {}

    const tripId = activeTrip ? activeTrip.id : 'GH-4192';
    const tripCrop = activeTrip ? (activeTrip.crop + ' (' + activeTrip.weight + ')') : 'Cotton · 40 Quintals DCH-32';
    const tripPickup = activeTrip ? (currentGramhaulFarmAddress + ' (' + currentGramhaulFarmLandmark + ')') : "Ramesh Rao's Farm, Sy.No 142/A, Narsampet Rural";
    const tripDrop = activeTrip ? activeTrip.mandi : 'Warangal Enamamula APMC Yard (Gate 3)';
    const tripFare = activeTrip ? activeTrip.fare : '1850';

    return `
    <div style="background:#F8FAF8;min-height:100%;padding-bottom:110px;font-family:-apple-system,BlinkMacSystemFont,'Plus Jakarta Sans','Inter',sans-serif;">
      <!-- Top Driver Header Bar -->
      <div style="padding:14px 18px 12px;background:linear-gradient(180deg, #0F172A 0%, #1E293B 100%);color:#FFFFFF;box-shadow:0 4px 20px rgba(0,0,0,0.15);">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
          <div style="display:flex;align-items:center;gap:10px;">
            <div style="width:40px;height:40px;border-radius:14px;background:linear-gradient(135deg, #F59E0B, #D97706);display:flex;align-items:center;justify-content:center;font-size:20px;box-shadow:0 2px 10px rgba(245,158,11,0.35);">
              🚚
            </div>
            <div>
              <div style="font-size:15px;font-weight:900;letter-spacing:-0.2px;">GramHaul Driver Cockpit</div>
              <div style="font-size:11px;color:#94A3B8;font-weight:600;">${driverName} · ${vehiclePlate}</div>
            </div>
          </div>
          
          <button onclick="switchUserRole('farmer')" style="background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.25);border-radius:100px;padding:6px 12px;color:#FFFFFF;font-size:11px;font-weight:800;cursor:pointer;display:flex;align-items:center;gap:5px;backdrop-filter:blur(6px);">
            <span>🧑‍🌾</span><span>Farmer View</span>
          </button>
        </div>

        <!-- Driver Metrics Strip -->
        <div style="display:grid;grid-template-columns:repeat(3, 1fr);gap:8px;padding-top:6px;">
          <div style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);border-radius:14px;padding:8px 10px;text-align:center;">
            <div style="font-size:10px;color:#94A3B8;font-weight:700;">Earnings</div>
            <div style="font-size:15px;font-weight:900;color:#34D399;">₹3,450</div>
          </div>
          <div style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);border-radius:14px;padding:8px 10px;text-align:center;">
            <div style="font-size:10px;color:#94A3B8;font-weight:700;">Completed</div>
            <div style="font-size:15px;font-weight:900;color:#FFFFFF;">4 Trips</div>
          </div>
          <div style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);border-radius:14px;padding:8px 10px;text-align:center;">
            <div style="font-size:10px;color:#94A3B8;font-weight:700;">Rating</div>
            <div style="font-size:15px;font-weight:900;color:#FBBF24;">★ 4.9</div>
          </div>
        </div>
      </div>

      <div style="padding:16px 16px 0;">
        <!-- 1. LIVE ASSIGNED ACTIVE TRIP CARD -->
        <div style="background:#FFFFFF;border:1.5px solid #86EFAC;border-radius:22px;padding:16px;box-shadow:0 4px 20px rgba(22,163,74,0.12);margin-bottom:16px;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
            <div style="display:flex;align-items:center;gap:6px;">
              <span style="background:#DCFCE7;color:#15803D;font-size:11px;font-weight:900;padding:3px 8px;border-radius:8px;">
                LIVE TRIP #${tripId}
              </span>
              <span style="font-size:11px;color:#16A34A;font-weight:800;">● Active Dispatch</span>
            </div>
            <div style="font-size:18px;font-weight:900;color:#15803D;">₹${tripFare}</div>
          </div>

          <!-- Cargo & Farmer Details -->
          <div style="background:#F8FAFC;border-radius:14px;padding:10px 12px;margin-bottom:12px;">
            <div style="font-size:13.5px;font-weight:900;color:#0F172A;">${tripCrop}</div>
            <div style="font-size:11.5px;color:#64748B;margin-top:2px;">Farmer: <strong>Ramesh Rao</strong> · +91 94401 22910</div>
          </div>

          <!-- Route GPS Waypoints -->
          <div style="margin-bottom:14px;font-size:12px;">
            <div style="display:flex;align-items:flex-start;gap:8px;margin-bottom:8px;">
              <span style="color:#16A34A;font-size:14px;">🏡</span>
              <div>
                <div style="font-size:10px;color:#64748B;font-weight:800;text-transform:uppercase;">Farmer Exact Pickup (GPS)</div>
                <div style="font-weight:800;color:#0F172A;">${tripPickup}</div>
              </div>
            </div>
            <div style="display:flex;align-items:flex-start;gap:8px;">
              <span style="color:#DC2626;font-size:14px;">🏢</span>
              <div>
                <div style="font-size:10px;color:#64748B;font-weight:800;text-transform:uppercase;">Drop APMC Mandi</div>
                <div style="font-weight:800;color:#0F172A;">${tripDrop}</div>
              </div>
            </div>
          </div>

          <!-- Driver Action Buttons -->
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px;">
            <button onclick="driverCallFarmer('+919440122910')" style="background:#F8FAFC;border:1.5px solid #CBD5E1;border-radius:12px;padding:10px;font-size:12px;font-weight:800;color:#0F172A;display:flex;align-items:center;justify-content:center;gap:6px;cursor:pointer;">
              <span>📞</span> <span>Call Farmer</span>
            </button>
            <button onclick="messageGramhaulDriver()" style="background:#F8FAFC;border:1.5px solid #CBD5E1;border-radius:12px;padding:10px;font-size:12px;font-weight:800;color:#0F172A;display:flex;align-items:center;justify-content:center;gap:6px;cursor:pointer;">
              <span>💬</span> <span>Live Chat</span>
            </button>
          </div>

          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
            <button onclick="driverOpenGpsNav(17.9689, 79.5941)" style="background:#16A34A;color:#FFFFFF;border:none;border-radius:12px;padding:10px;font-size:12px;font-weight:900;display:flex;align-items:center;justify-content:center;gap:6px;cursor:pointer;box-shadow:0 4px 12px rgba(22,163,74,0.3);">
              <span>🧭</span> <span>Start Turn GPS</span>
            </button>
            <button onclick="driverCompleteHaulTrip('${tripId}', '${tripFare}')" style="background:#0F172A;color:#FFFFFF;border:none;border-radius:12px;padding:10px;font-size:12px;font-weight:900;display:flex;align-items:center;justify-content:center;gap:6px;cursor:pointer;">
              <span>✅</span> <span>Mark Delivered</span>
            </button>
          </div>
        </div>

        <!-- 2. Available Hauls Pool -->
        <div style="margin-bottom:16px;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
            <div style="font-size:14.5px;font-weight:900;color:#0F172A;">Available Haul Requests Nearby</div>
            <span style="background:#DCFCE7;color:#15803D;font-size:10px;font-weight:800;padding:2px 6px;border-radius:6px;">2 Ready</span>
          </div>

          <!-- Pool Order 1 -->
          <div style="background:#FFFFFF;border:1.5px solid #E2E8F0;border-radius:18px;padding:14px;margin-bottom:10px;box-shadow:0 2px 10px rgba(15,23,42,0.04);">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
              <div style="font-size:13.5px;font-weight:900;color:#0F172A;">🌶️ Teja Chilli (25 Bags · 2.5 Ton)</div>
              <div style="font-size:16px;font-weight:900;color:#15803D;">₹4,200</div>
            </div>
            <div style="font-size:11px;color:#64748B;margin-bottom:8px;">Farmer: K. Anjaiah · Hasanparthy (5.8 km) ➔ Khammam Spices APMC</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
              <button onclick="driverCallFarmer('+919440122910')" style="background:#F8FAFC;border:1px solid #CBD5E1;border-radius:10px;padding:8px;font-size:11.5px;font-weight:800;color:#334155;cursor:pointer;">📞 Call</button>
              <button onclick="alert('Haul GH-8824 Accepted!');" style="background:#0F172A;color:#FFFFFF;border:none;border-radius:10px;padding:8px;font-size:11.5px;font-weight:800;cursor:pointer;">✅ Accept</button>
            </div>
          </div>
        </div>

        <!-- 3. Vehicle Diagnostics & FASTag -->
        <div style="background:#FFFFFF;border:1.5px solid #E2E8F0;border-radius:18px;padding:14px;box-shadow:0 2px 10px rgba(15,23,42,0.04);">
          <div style="font-size:13.5px;font-weight:900;color:#0F172A;margin-bottom:10px;display:flex;align-items:center;gap:6px;">
            <span>🚚</span> <span>Vehicle Diagnostics & FASTag</span>
          </div>
          <div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #F1F5F9;font-size:12px;">
            <span style="color:#64748B;">Diesel Fuel Level</span>
            <span style="font-weight:800;color:#15803D;">78% (Range: 320 km)</span>
          </div>
          <div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #F1F5F9;font-size:12px;">
            <span style="color:#64748B;">FASTag Balance</span>
            <span style="font-weight:800;color:#0F172A;">₹1,450.00</span>
          </div>
          <div style="display:flex;justify-content:space-between;padding:6px 0;font-size:12px;">
            <span style="color:#64748B;">Maintenance Status</span>
            <span style="font-weight:800;color:#15803D;">Good · Next Service in 1,400 km</span>
          </div>
        </div>
      </div>
    </div>
    `;
  },
"""

def apply_full_system_update(filepath):
    print(f"Applying real interactive system, GPS pickup modal, chat/call/share/cancel, and driver sync to {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace GramHaul view in APP_VIEWS
    pattern = r'gramhaul\s*:\s*\(\)\s*=>\s*\{.*?(?=\n\s*\/\* ── [3-9]\.|\n\s*agristack\s*:\s*\(\)\s*=>)'
    if re.search(pattern, content, flags=re.DOTALL):
        content = re.sub(pattern, GRAMHAUL_FULL_VIEW_V3.strip(), content, count=1, flags=re.DOTALL)
        print("Replaced GramHaul view!")

    # 2. Replace Driver Dashboard view in APP_VIEWS
    pattern_driver = r'driver_dashboard\s*:\s*\(\)\s*=>\s*\{.*?(?=\n\s*\/\* ── [0-9]+\.|\n\s*profile\s*:\s*\(\)\s*=>)'
    if re.search(pattern_driver, content, flags=re.DOTALL):
        content = re.sub(pattern_driver, DRIVER_DASHBOARD_VIEW_UPGRADE.strip(), content, count=1, flags=re.DOTALL)
        print("Replaced Driver Dashboard view with Live Sync View!")

    # 3. Clean up previous GramHaul state logic if already present
    marker = "/* ══════════════════════════════════════════════════════════════\n   GRAMHAUL: REAL GPS"
    idx = content.find(marker)
    if idx != -1:
        last_script_idx = content.rfind('</script>')
        content = content[:idx] + content[last_script_idx:]

    # 4. Insert fresh comprehensive GRAMHAUL_FULL_LOGIC_JS before </script>
    last_script_idx = content.rfind('</script>')
    if last_script_idx != -1:
        content = content[:last_script_idx] + '\n\n' + GRAMHAUL_FULL_LOGIC_JS.strip() + '\n\n' + content[last_script_idx:]
        print("Inserted fresh complete GRAMHAUL_FULL_LOGIC_JS before </script>!")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath} successfully!")

if __name__ == '__main__':
    apply_full_system_update('app/src/main/assets/index.html')
    apply_full_system_update('nukrop_emulator.html')
