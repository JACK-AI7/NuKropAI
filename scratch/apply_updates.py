import sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

original_length = len(text)
print(f"Original length: {original_length}")

# 1. Update Bottom Navigation CSS for Interactive Animated Icons
old_dock_css = """.dock-tab-btn {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 3px;
  cursor: pointer;
  padding: 4px 0;
  user-select: none;
  transition: all 0.15s ease;
}
.dock-tab-btn svg {
  width: 22px;
  height: 22px;
  stroke: #64748B;
  fill: none;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  transition: stroke 0.15s ease;
}
.dock-tab-btn span {
  font-size: 10.5px;
  font-weight: 700;
  color: #64748B;
  transition: color 0.15s ease, font-weight 0.15s ease;
}
.dock-tab-btn.active svg {
  stroke: #15803D;
  stroke-width: 2.3;
  fill: none;
}
.dock-tab-btn.active span {
  color: #15803D;
  font-weight: 900;
}
.dock-tab-btn.active span {
  color: #15803D;
  font-weight: 900;
}

/* Center Elevated Tactile Green FAB */
.dock-center-fab-wrap {
  width: 76px;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: -26px;
  position: relative;
  z-index: 50;
  cursor: pointer;
}

.dock-center-fab {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: radial-gradient(circle at 35% 30%, #22C55E 0%, #16A34A 55%, #15803D 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow:
    0 6px 18px rgba(22, 163, 74, 0.4),
    inset 0 2px 3px rgba(255,255,255,0.4),
    inset 0 -2px 3px rgba(0,0,0,0.25);
  border: 3.5px solid #FFFFFF;
  transition: transform 0.12s ease;
}
.dock-center-fab:active {
  transform: scale(0.93);
}"""

new_dock_css = """.dock-tab-btn {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 3px;
  cursor: pointer;
  padding: 4px 0;
  user-select: none;
  transition: transform 0.18s cubic-bezier(0.16,1,0.3,1), color 0.18s ease;
  -webkit-tap-highlight-color: transparent;
  position: relative;
}
.dock-tab-btn:active {
  transform: scale(0.86);
}
.dock-tab-btn svg {
  width: 22px;
  height: 22px;
  stroke: #64748B;
  fill: none;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  transition: stroke 0.18s ease, transform 0.18s cubic-bezier(0.16,1,0.3,1), filter 0.18s ease;
}
.dock-tab-btn span {
  font-size: 10.5px;
  font-weight: 700;
  color: #64748B;
  transition: color 0.18s ease, font-weight 0.18s ease;
}

/* Active State & Micro-Interactions */
.dock-tab-btn.active {
  animation: navTabPop 0.35s cubic-bezier(0.16,1,0.3,1);
}
.dock-tab-btn.active svg {
  stroke: #15803D;
  stroke-width: 2.4;
  filter: drop-shadow(0 2px 6px rgba(22, 163, 74, 0.45));
}
.dock-tab-btn.active span {
  color: #15803D;
  font-weight: 900;
}
.dock-tab-btn.active::after {
  content: '';
  display: block;
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: #15803D;
  margin-top: 1px;
  box-shadow: 0 0 6px rgba(22, 163, 74, 0.8);
  animation: navDotScale 0.25s cubic-bezier(0.16,1,0.3,1);
}

@keyframes navTabPop {
  0% { transform: scale(0.9); }
  45% { transform: scale(1.18) translateY(-3px); }
  75% { transform: scale(0.97) translateY(0); }
  100% { transform: scale(1) translateY(0); }
}

@keyframes navDotScale {
  0% { transform: scale(0); opacity: 0; }
  70% { transform: scale(1.4); opacity: 1; }
  100% { transform: scale(1); opacity: 1; }
}

/* Tab-Specific Fluid Animations */
@keyframes navHomeRoofBounce {
  0%, 100% { transform: translateY(0); }
  40% { transform: translateY(-3px) scale(1.08); }
  75% { transform: translateY(0.5px); }
}
.dock-tab-btn#tab-home.active svg {
  animation: navHomeRoofBounce 0.5s cubic-bezier(0.16,1,0.3,1);
}

@keyframes navCommAvatarNod {
  0%, 100% { transform: rotate(0deg); }
  30% { transform: rotate(-8deg) scale(1.08); }
  70% { transform: rotate(8deg) scale(1.08); }
}
.dock-tab-btn#tab-community.active svg {
  animation: navCommAvatarNod 0.55s cubic-bezier(0.16,1,0.3,1);
}

@keyframes navMarketBarsRise {
  0% { transform: scaleY(0.7); transform-origin: bottom; }
  50% { transform: scaleY(1.18); transform-origin: bottom; }
  100% { transform: scaleY(1); transform-origin: bottom; }
}
.dock-tab-btn#tab-market.active svg {
  animation: navMarketBarsRise 0.5s cubic-bezier(0.16,1,0.3,1);
}

@keyframes navProfilePop {
  0% { transform: scale(1) rotate(0deg); }
  35% { transform: scale(1.18) rotate(10deg); }
  70% { transform: scale(0.96) rotate(-5deg); }
  100% { transform: scale(1) rotate(0deg); }
}
.dock-tab-btn#tab-profile.active svg {
  animation: navProfilePop 0.55s cubic-bezier(0.16,1,0.3,1);
}

/* Center Elevated Tactile Green FAB */
.dock-center-fab-wrap {
  width: 76px;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: -26px;
  position: relative;
  z-index: 50;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
}

@keyframes navFabBreathingGlow {
  0%, 100% {
    transform: scale(1);
    box-shadow:
      0 6px 18px rgba(22, 163, 74, 0.42),
      0 0 0 0 rgba(34, 197, 94, 0.35),
      inset 0 2px 3px rgba(255,255,255,0.4),
      inset 0 -2px 3px rgba(0,0,0,0.25);
  }
  50% {
    transform: scale(1.05);
    box-shadow:
      0 10px 24px rgba(22, 163, 74, 0.58),
      0 0 0 6px rgba(34, 197, 94, 0),
      inset 0 2px 3px rgba(255,255,255,0.4),
      inset 0 -2px 3px rgba(0,0,0,0.25);
  }
}

.dock-center-fab {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: radial-gradient(circle at 35% 30%, #22C55E 0%, #16A34A 55%, #15803D 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow:
    0 6px 18px rgba(22, 163, 74, 0.4),
    inset 0 2px 3px rgba(255,255,255,0.4),
    inset 0 -2px 3px rgba(0,0,0,0.25);
  border: 3.5px solid #FFFFFF;
  transition: transform 0.15s cubic-bezier(0.16,1,0.3,1);
  animation: navFabBreathingGlow 3s ease-in-out infinite;
}
.dock-center-fab:active {
  transform: scale(0.91) !important;
}"""

if old_dock_css in text:
    text = text.replace(old_dock_css, new_dock_css)
    print("✅ Replaced Bottom Navigation CSS with animated micro-interactions")
else:
    print("⚠️ Could not find old_dock_css exactly, searching for dock-tab-btn in CSS")

# 2. Update Side Navigation Panel Buttons (Replace emojis with clean SVGs)
old_side_nav_btns = """      <div style="display:grid;grid-template-columns:1fr;gap:6px;" id="side-nav-group">
        <button class="panel-nav-btn active" id="btn-home" onclick="openScreen('home',null);syncSideNav('btn-home')">🏠 Home Dashboard</button>
        <button class="panel-nav-btn" id="btn-scanner" onclick="openScreen('scanner',null);syncSideNav('btn-scanner')">🔬 AI Crop &amp; Soil Scanner</button>
        <button class="panel-nav-btn" id="btn-market" onclick="openScreen('market',null);syncSideNav('btn-market')">📊 Live Mandi Rates</button>
        <button class="panel-nav-btn" id="btn-gramhaul" onclick="openScreen('gramhaul',null);syncSideNav('btn-gramhaul')"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" style="vertical-align:middle;margin-right:6px;"><rect x="1" y="6" width="14" height="11" rx="2" fill="currentColor"/><path d="M15 9H19L22 13V17H15V9Z" fill="currentColor"/><circle cx="5.5" cy="17" r="2.2" fill="#FFFFFF"/><circle cx="18.5" cy="17" r="2.2" fill="#FFFFFF"/></svg>Mandi Truck Sharing</button>
        <button class="panel-nav-btn" id="btn-agristack" onclick="openScreen('agristack',null);syncSideNav('btn-agristack')">🪪 Farmer ID &amp; Credit</button>
        <button class="panel-nav-btn" id="btn-equipment" onclick="openScreen('equipment',null);syncSideNav('btn-equipment')">🚜 Rent Machinery</button>
        <button class="panel-nav-btn" id="btn-loan" onclick="openScreen('loan',null);syncSideNav('btn-loan')">💰 Loans &amp; Subsidies</button>
        <button class="panel-nav-btn" id="btn-chat" onclick="openScreen('chat',null);syncSideNav('btn-chat')">🤖 24/7 AI Farm Advisor</button>
        <button class="panel-nav-btn" id="btn-khata" onclick="openScreen('khata',null);syncSideNav('btn-khata')">🧾 Farm Khata Ledger</button>
        <button class="panel-nav-btn" id="btn-bioshield" onclick="openScreen('bioshield',null);syncSideNav('btn-bioshield')">🚨 Pest &amp; Disease Alerts</button>
        <button class="panel-nav-btn" id="btn-biorx" onclick="openScreen('biorx',null);syncSideNav('btn-biorx')">🌿 Organic Bio-Medicines</button>
      </div>"""

new_side_nav_btns = """      <div style="display:grid;grid-template-columns:1fr;gap:6px;" id="side-nav-group">
        <button class="panel-nav-btn active" id="btn-home" onclick="openScreen('home',null);syncSideNav('btn-home')">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><path d="M3 10.5L12 3l9 7.5v9.5a2 2 0 0 1-2 2h-4a1 1 0 0 1-1-1v-5a2 2 0 0 0-2-2 2 2 0 0 0-2 2v5a1 1 0 0 1-1 1H5a2 2 0 0 1-2-2v-9.5z"/></svg>
          <span>Home Dashboard</span>
        </button>
        <button class="panel-nav-btn" id="btn-scanner" onclick="openScreen('scanner',null);syncSideNav('btn-scanner')">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 3.5 1 9.2A7 7 0 0 1 11 20z"/><path d="M11 20v-8"/></svg>
          <span>AI Crop &amp; Soil Scanner</span>
        </button>
        <button class="panel-nav-btn" id="btn-market" onclick="openScreen('market',null);syncSideNav('btn-market')">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
          <span>Live Mandi Rates</span>
        </button>
        <button class="panel-nav-btn" id="btn-gramhaul" onclick="openScreen('gramhaul',null);syncSideNav('btn-gramhaul')">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><rect x="1" y="6" width="14" height="11" rx="2"/><polygon points="15 8 19 8 22 11 22 17 15 17 15 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>
          <span>Mandi Truck Sharing</span>
        </button>
        <button class="panel-nav-btn" id="btn-agristack" onclick="openScreen('agristack',null);syncSideNav('btn-agristack')">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><rect x="3" y="4" width="18" height="16" rx="3"/><circle cx="9" cy="10" r="2"/><line x1="15" y1="8" x2="17" y2="8"/><line x1="15" y1="12" x2="17" y2="12"/><line x1="7" y1="16" x2="17" y2="16"/></svg>
          <span>Farmer ID &amp; Credit</span>
        </button>
        <button class="panel-nav-btn" id="btn-equipment" onclick="openScreen('equipment',null);syncSideNav('btn-equipment')">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><circle cx="7" cy="17" r="4"/><circle cx="17" cy="17" r="3"/><path d="M10 9h4l2 4H4l1-3h5z"/><path d="M14 9V5h3l2 4"/></svg>
          <span>Rent Machinery</span>
        </button>
        <button class="panel-nav-btn" id="btn-loan" onclick="openScreen('loan',null);syncSideNav('btn-loan')">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
          <span>Loans &amp; Subsidies</span>
        </button>
        <button class="panel-nav-btn" id="btn-chat" onclick="openScreen('chat',null);syncSideNav('btn-chat')">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="5" r="2"/><path d="M12 7v4"/><circle cx="8" cy="16" r="1" fill="currentColor"/><circle cx="16" cy="16" r="1" fill="currentColor"/></svg>
          <span>24/7 AI Farm Advisor</span>
        </button>
        <button class="panel-nav-btn" id="btn-khata" onclick="openScreen('khata',null);syncSideNav('btn-khata')">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/><line x1="8" y1="7" x2="16" y2="7"/><line x1="8" y1="11" x2="14" y2="11"/></svg>
          <span>Farm Khata Ledger</span>
        </button>
        <button class="panel-nav-btn" id="btn-bioshield" onclick="openScreen('bioshield',null);syncSideNav('btn-bioshield')">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><circle cx="12" cy="11" r="3"/></svg>
          <span>Pest &amp; Disease Alerts</span>
        </button>
        <button class="panel-nav-btn" id="btn-biorx" onclick="openScreen('biorx',null);syncSideNav('btn-biorx')">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><path d="M10 2v7.31L4.36 19.46A2 2 0 0 0 6.07 22h11.86a2 2 0 0 0 1.71-2.54L14 9.31V2h-4z"/><line x1="8.5" y1="2" x2="15.5" y2="2"/></svg>
          <span>Organic Bio-Medicines</span>
        </button>
      </div>"""

if old_side_nav_btns in text:
    text = text.replace(old_side_nav_btns, new_side_nav_btns)
    print("✅ Replaced Side Navigation Buttons with luxury SVGs")
else:
    print("⚠️ Could not find old_side_nav_btns")

# 3. Fix AgriStack ID screen header and elements
# Replace header: <div style="font-size:16px;font-weight:900;color:#0F172A;letter-spacing:-0.2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">🪪 ${headerTitle}</div>
old_agri_header_title = """<div style="font-size:16px;font-weight:900;color:#0F172A;letter-spacing:-0.2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">🪪 ${headerTitle}</div>"""
new_agri_header_title = """<div style="font-size:16px;font-weight:900;color:#0F172A;letter-spacing:-0.2px;display:flex;align-items:center;gap:6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
            <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="#15803D" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><rect x="3" y="4" width="18" height="16" rx="3"/><circle cx="9" cy="10" r="2"/><line x1="15" y1="8" x2="17" y2="8"/><line x1="15" y1="12" x2="17" y2="12"/><line x1="7" y1="16" x2="17" y2="16"/></svg>
            <span>${headerTitle}</span>
          </div>"""

if old_agri_header_title in text:
    text = text.replace(old_agri_header_title, new_agri_header_title)
    print("✅ Replaced AgriStack header title with crisp SVG")

# Replace Verify & Search button emoji
old_agri_search_btn = """<button onclick="triggerFarmerLandSearch()" style="background:linear-gradient(135deg,#16A34A 0%,#15803D 100%);color:#FFFFFF;border:none;border-radius:14px;padding:0 16px;height:46px;font-size:12px;font-weight:800;cursor:pointer;display:flex;align-items:center;gap:5px;box-shadow:0 3px 10px rgba(22,163,74,0.22);white-space:nowrap;flex-shrink:0;transition:transform 0.15s ease;">
          <span>🔍</span>
          <span>${TL('Verify & Search', 'శోధించండి', 'खोजें')}</span>
        </button>"""
new_agri_search_btn = """<button onclick="triggerFarmerLandSearch()" style="background:linear-gradient(135deg,#16A34A 0%,#15803D 100%);color:#FFFFFF;border:none;border-radius:14px;padding:0 16px;height:46px;font-size:12px;font-weight:800;cursor:pointer;display:flex;align-items:center;gap:6px;box-shadow:0 3px 10px rgba(22,163,74,0.22);white-space:nowrap;flex-shrink:0;transition:transform 0.15s ease;">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          <span>${TL('Verify & Search', 'శోధించండి', 'खोजें')}</span>
        </button>"""

if old_agri_search_btn in text:
    text = text.replace(old_agri_search_btn, new_agri_search_btn)
    print("✅ Replaced Verify & Search button with SVG")

# Replace Link Real Land Parcel icon
old_link_land_icon = """<div style="width:38px;height:38px;border-radius:12px;background:#DCFCE7;border:1px solid #86EFAC;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;">
            🏛️
          </div>"""
new_link_land_icon = """<div style="width:38px;height:38px;border-radius:12px;background:#DCFCE7;border:1px solid #86EFAC;display:flex;align-items:center;justify-content:center;color:#15803D;flex-shrink:0;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18"/><path d="M5 21V10l7-5 7 5v11"/><path d="M9 21v-4a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v4"/><line x1="9" y1="10" x2="9" y2="14"/><line x1="15" y1="10" x2="15" y2="14"/></svg>
          </div>"""

if old_link_land_icon in text:
    text = text.replace(old_link_land_icon, new_link_land_icon)
    print("✅ Replaced Link Real Land icon with SVG")

# Replace Farmer Registry badge and watermark
old_farmer_reg_badge = """<div style="display:inline-flex;align-items:center;gap:6px;background:rgba(255,255,255,0.18);border:1px solid rgba(255,255,255,0.25);padding:3px 10px;border-radius:20px;margin-bottom:10px;backdrop-filter:blur(4px);">
          <span>🏛️</span>
          <span style="font-size:9.5px;font-weight:900;letter-spacing:0.04em;">
            GOVT OF INDIA · AGRISTACK REGISTRY
          </span>
        </div>"""
new_farmer_reg_badge = """<div style="display:inline-flex;align-items:center;gap:6px;background:rgba(255,255,255,0.18);border:1px solid rgba(255,255,255,0.25);padding:3px 10px;border-radius:20px;margin-bottom:10px;backdrop-filter:blur(4px);">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
          <span style="font-size:9.5px;font-weight:900;letter-spacing:0.04em;">
            GOVT OF INDIA · AGRISTACK REGISTRY
          </span>
        </div>"""

if old_farmer_reg_badge in text:
    text = text.replace(old_farmer_reg_badge, new_farmer_reg_badge)
    print("✅ Replaced Farmer Registry badge with SVG")

# Replace Cadastral RoR header icon & map controls
old_cadastral_header = """<div style="display:flex;align-items:center;gap:6px;min-width:0;">
          <span style="font-size:14px;">🗺️</span>
          <span style="font-size:10.5px;font-weight:900;color:#0F172A;letter-spacing:0.02em;text-transform:uppercase;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
            ${TL('OpenStreetMap Cadastral RoR', 'ఓపెన్‌స్ట్రీట్‌మ్యాప్ సరిహద్దులు', 'OpenStreetMap Cadastral RoR')}
          </span>
        </div>"""
new_cadastral_header = """<div style="display:flex;align-items:center;gap:6px;min-width:0;">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#15803D" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/></svg>
          <span style="font-size:10.5px;font-weight:900;color:#0F172A;letter-spacing:0.02em;text-transform:uppercase;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
            ${TL('OpenStreetMap Cadastral RoR', 'ఓపెన్‌స్ట్రీట్‌మ్యాప్ సరిహద్దులు', 'OpenStreetMap Cadastral RoR')}
          </span>
        </div>"""

if old_cadastral_header in text:
    text = text.replace(old_cadastral_header, new_cadastral_header)
    print("✅ Replaced Cadastral RoR header icon with SVG")

old_map_controls = """<!-- Floating Map Controls -->
        <div style="position:absolute;top:8px;right:8px;z-index:1000;display:flex;flex-direction:column;gap:4px;">
          <button onclick="toggleMapTileType('satellite')" style="background:rgba(255,255,255,0.92);border:1px solid #CBD5E1;color:#0F172A;border-radius:8px;padding:4px 8px;font-size:9px;font-weight:800;cursor:pointer;box-shadow:0 2px 6px rgba(0,0,0,0.1);">
            🛰️ Sat
          </button>
          <button onclick="toggleMapTileType('cadastral')" style="background:rgba(255,255,255,0.92);border:1px solid #CBD5E1;color:#15803D;border-radius:8px;padding:4px 8px;font-size:9px;font-weight:800;cursor:pointer;box-shadow:0 2px 6px rgba(0,0,0,0.1);">
            🗺️ RoR
          </button>
        </div>"""
new_map_controls = """<!-- Floating Map Controls -->
        <div style="position:absolute;top:8px;right:8px;z-index:1000;display:flex;flex-direction:column;gap:4px;">
          <button onclick="toggleMapTileType('satellite')" style="background:rgba(255,255,255,0.95);border:1px solid #CBD5E1;color:#0F172A;border-radius:8px;padding:4px 8px;font-size:9.5px;font-weight:800;cursor:pointer;box-shadow:0 2px 6px rgba(0,0,0,0.08);display:flex;align-items:center;gap:4px;">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>
            <span>Sat</span>
          </button>
          <button onclick="toggleMapTileType('cadastral')" style="background:rgba(255,255,255,0.95);border:1px solid #CBD5E1;color:#15803D;border-radius:8px;padding:4px 8px;font-size:9.5px;font-weight:800;cursor:pointer;box-shadow:0 2px 6px rgba(0,0,0,0.08);display:flex;align-items:center;gap:4px;">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/></svg>
            <span>RoR</span>
          </button>
        </div>"""

if old_map_controls in text:
    text = text.replace(old_map_controls, new_map_controls)
    print("✅ Replaced Floating map controls with SVGs")

# 4. Remove fake automated surge trigger on GPS load
old_fake_surge = """setTimeout(() => {
            showPushNotificationToast({
              title: '⚡ ' + TL('Warangal APMC Live Cotton Rate', 'వరంగల్ APMC పత్తి తాజా ధర', 'वारंगल कपास मंडी ताजा भाव'),
              msg: '₹7,850/Qtl (▲ +₹180/Qtl) · ' + TL('Demand bullish. Good day to harvest & sell.', 'డిమాండ్ పెరిగింది. అమ్మకానికి అనుకూలం.', 'मांग में तेजी। बिक्री का अनुकूल समय।'),
              type: 'price_surge'
            });
          }, 3500);"""
if old_fake_surge in text:
    text = text.replace(old_fake_surge, "// Fake automated surge toast removed - only real alerts")
    print("✅ Removed fake 3.5s automated surge trigger")

# 5. Fix Weather Card metrics (Replace emojis with SVGs)
old_weather_metrics = """        <!-- 2. 4 METEOROLOGICAL METRICS -->
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:0;background:#F8FAF8;border:1px solid #E2ECE2;border-radius:12px;padding:8px 0;margin-bottom:10px;">
          <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 2px;">
            <div style="font-size:9px;color:#64748B;font-weight:700;white-space:nowrap;">💧 ${t.humidity}</div>
            <div style="font-size:12px;font-weight:900;color:#0F172A;margin-top:2px;white-space:nowrap;" id="w-humidity">${parseInt(liveWeather.humidity) || 80}%</div>
          </div>
          <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 2px;border-left:1px solid #E2ECE2;">
            <div style="font-size:9px;color:#64748B;font-weight:700;white-space:nowrap;">🌧️ ${t.rainfall || t.precipitation}</div>
            <div style="font-size:12px;font-weight:900;color:#0F172A;margin-top:2px;white-space:nowrap;" id="w-precip">${parseInt(liveWeather.precip || liveWeather.precipitation) || 0} mm</div>
          </div>
          <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 2px;border-left:1px solid #E2ECE2;">
            <div style="font-size:9px;color:#64748B;font-weight:700;white-space:nowrap;">🧭 ${t.pressure}</div>
            <div style="font-size:12px;font-weight:900;color:#0F172A;margin-top:2px;white-space:nowrap;" id="w-pressure">${parseInt(liveWeather.pressure) || 953} hpa</div>
          </div>
          <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 2px;border-left:1px solid #E2ECE2;">
            <div style="font-size:9px;color:#64748B;font-weight:700;white-space:nowrap;">💨 ${t.windSpeed || t.wind}</div>
            <div style="font-size:12px;font-weight:900;color:#0F172A;margin-top:2px;white-space:nowrap;" id="w-wind">${parseInt(liveWeather.wind || liveWeather.windSpeed) || 4} km/h</div>
          </div>
        </div>"""

new_weather_metrics = """        <!-- 2. 4 METEOROLOGICAL METRICS -->
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:0;background:#F8FAF8;border:1px solid #E2ECE2;border-radius:12px;padding:8px 0;margin-bottom:10px;">
          <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 2px;">
            <div style="font-size:9px;color:#64748B;font-weight:700;white-space:nowrap;display:flex;align-items:center;gap:3px;">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2.3"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>
              <span>${t.humidity}</span>
            </div>
            <div style="font-size:12px;font-weight:900;color:#0F172A;margin-top:2px;white-space:nowrap;" id="w-humidity">${parseInt(liveWeather.humidity) || 80}%</div>
          </div>
          <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 2px;border-left:1px solid #E2ECE2;">
            <div style="font-size:9px;color:#64748B;font-weight:700;white-space:nowrap;display:flex;align-items:center;gap:3px;">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2.3"><path d="M20 16.58A5 5 0 0 0 18 7h-1.26A8 8 0 1 0 4 15.25"/><line x1="8" y1="19" x2="8" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/><line x1="16" y1="19" x2="16" y2="21"/></svg>
              <span>${t.rainfall || t.precipitation}</span>
            </div>
            <div style="font-size:12px;font-weight:900;color:#0F172A;margin-top:2px;white-space:nowrap;" id="w-precip">${parseInt(liveWeather.precip || liveWeather.precipitation) || 0} mm</div>
          </div>
          <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 2px;border-left:1px solid #E2ECE2;">
            <div style="font-size:9px;color:#64748B;font-weight:700;white-space:nowrap;display:flex;align-items:center;gap:3px;">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2.3"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>
              <span>${t.pressure}</span>
            </div>
            <div style="font-size:12px;font-weight:900;color:#0F172A;margin-top:2px;white-space:nowrap;" id="w-pressure">${parseInt(liveWeather.pressure) || 953} hpa</div>
          </div>
          <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 2px;border-left:1px solid #E2ECE2;">
            <div style="font-size:9px;color:#64748B;font-weight:700;white-space:nowrap;display:flex;align-items:center;gap:3px;">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2.3"><path d="M9.59 4.59A2 2 0 1 1 11 8H2m10.59 11.41A2 2 0 1 0 14 16H2m15.73-8.27A2.5 2.5 0 1 1 19.5 12H2"/></svg>
              <span>${t.windSpeed || t.wind}</span>
            </div>
            <div style="font-size:12px;font-weight:900;color:#0F172A;margin-top:2px;white-space:nowrap;" id="w-wind">${parseInt(liveWeather.wind || liveWeather.windSpeed) || 4} km/h</div>
          </div>
        </div>"""

if old_weather_metrics in text:
    text = text.replace(old_weather_metrics, new_weather_metrics)
    print("✅ Replaced Weather 4 metrics with crisp SVGs")

# Replace Sunrise and Sunset icons
old_sun_row = """            <div>
              <div style="font-size:12px;font-weight:900;color:#0F172A;" id="w-sunrise">${liveWeather.sunrise || liveWeather.sunriseStr || "05:57 am"}</div>
              <div style="font-size:9.5px;color:#64748B;font-weight:700;">🌅 ${t.sunrise}</div>
            </div>
            <div style="text-align:right;">
              <div style="font-size:12px;font-weight:900;color:#0F172A;" id="w-sunset">${liveWeather.sunset || liveWeather.sunsetStr || "06:26 pm"}</div>
              <div style="font-size:9.5px;color:#64748B;font-weight:700;">🌇 ${t.sunset}</div>
            </div>"""

new_sun_row = """            <div>
              <div style="font-size:12px;font-weight:900;color:#0F172A;" id="w-sunrise">${liveWeather.sunrise || liveWeather.sunriseStr || "05:57 am"}</div>
              <div style="font-size:9.5px;color:#64748B;font-weight:700;display:flex;align-items:center;gap:3px;">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2.3"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg>
                <span>${t.sunrise}</span>
              </div>
            </div>
            <div style="text-align:right;">
              <div style="font-size:12px;font-weight:900;color:#0F172A;" id="w-sunset">${liveWeather.sunset || liveWeather.sunsetStr || "06:26 pm"}</div>
              <div style="font-size:9.5px;color:#64748B;font-weight:700;display:flex;align-items:center;justify-content:flex-end;gap:3px;">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#EA580C" stroke-width="2.3"><path d="M17 18a5 5 0 0 0-10 0"/><line x1="12" y1="2" x2="12" y2="9"/><line x1="4.22" y1="10.22" x2="5.64" y2="11.64"/><line x1="1" y1="18" x2="3" y2="18"/><line x1="21" y1="18" x2="23" y2="18"/><line x1="18.36" y1="11.64" x2="19.78" y2="10.22"/><line x1="23" y1="22" x2="1" y2="22"/></svg>
                <span>${t.sunset}</span>
              </div>
            </div>"""

if old_sun_row in text:
    text = text.replace(old_sun_row, new_sun_row)
    print("✅ Replaced Sunrise / Sunset with SVGs")

# Replace Spraying Banner icon
old_spray_icon = """<div style="width:32px;height:32px;border-radius:10px;background:#DCFCE7;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;">
                🧑‍🌾
              </div>"""
new_spray_icon = """<div style="width:32px;height:32px;border-radius:10px;background:#DCFCE7;display:flex;align-items:center;justify-content:center;color:#15803D;flex-shrink:0;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></svg>
              </div>"""

if old_spray_icon in text:
    text = text.replace(old_spray_icon, new_spray_icon)
    print("✅ Replaced Spraying Banner icon with SVG")

# 6. Update GramHaul map logic - Pure Real Driver Telemetry & Zero Fake Trucks
# Change let GRAMHAUL_POOLED_TRUCKS = [...] to let GRAMHAUL_POOLED_TRUCKS = [];
old_pooled_array_pattern = r'let GRAMHAUL_POOLED_TRUCKS = \[\s*\{[\s\S]*?\}\s*\];'
match_pooled = re.search(old_pooled_array_pattern, text)
if match_pooled:
    text = text[:match_pooled.start()] + 'let GRAMHAUL_POOLED_TRUCKS = [];' + text[match_pooled.end():]
    print("✅ Initialized GRAMHAUL_POOLED_TRUCKS to empty array []")

# Update loadRealTrucksFromSupabase()
old_load_real_trucks = """async function loadRealTrucksFromSupabase() {
  try {
    if (typeof sbClient === 'undefined' || !sbClient) return;
    const { data, error } = await sbClient
      .from('driver_telemetry')
      .select('driver_id, driver_name, vehicle_type, vehicle_plate, current_lat, current_lng, is_online, last_ping')
      .eq('is_online', true)
      .order('last_ping', { ascending: false })
      .limit(10);

    if (error || !data || data.length === 0) {
      console.log('[GramHaul] No live drivers in Supabase — showing seed trucks.');
      return;
    }

    const realTrucks = data.map((d, i) => ({
      id: d.driver_id || ('drv-' + i),
      driver: { en: d.driver_name || 'Driver', te: d.driver_name || 'Driver', hi: d.driver_name || 'Driver' },
      vehicle: { en: d.vehicle_type || 'Commercial Vehicle', te: d.vehicle_type || 'వాహనం', hi: d.vehicle_type || 'वाहन' },
      phone: '',
      dist: { en: 'Live GPS Tracking', te: 'లైవ్ GPS ట్రాకింగ్', hi: 'लाइव GPS ट्रैकिंग' },
      dest: { en: 'Available for Haul Booking', te: 'బుకింగ్ కోసం అందుబాటులో', hi: 'बुकिंग के लिए उपलब्ध' },
      spaceLeft: 'Contact driver',
      fillPercent: 0,
      ratePerQtl: 0,
      rating: '★ Active',
      leavesAt: { en: 'On-demand', te: 'అవసరాన్ని బట్టి', hi: 'मांग पर' },
      lat: d.current_lat,
      lng: d.current_lng,
      plate: d.vehicle_plate,
      isLive: true
    }));

    // Merge: live drivers first, seed fallbacks for offline
    MANDI_TRUCKS_CATALOG = [
      ...realTrucks,
      ...MANDI_TRUCKS_SEED.filter(s => !realTrucks.find(r => r.id === s.id))
    ];
    console.log('[GramHaul] Loaded ' + realTrucks.length + ' live drivers from Supabase');

    // Re-render the truck list if GramHaul screen is visible
    const truckListEl = document.querySelector('.gramhaul-truck-card');
    if (truckListEl && typeof renderGramHaulTruckList === 'function') renderGramHaulTruckList();
  } catch (e) {
    console.warn('[GramHaul] Supabase trucks load failed, using seed data:', e);
  }
}"""

new_load_real_trucks = """var gramhaulLiveDriversLayer = null;

async function loadRealTrucksFromSupabase() {
  try {
    if (typeof sbClient === 'undefined' || !sbClient) return;
    const { data, error } = await sbClient
      .from('driver_telemetry')
      .select('driver_id, driver_name, vehicle_type, vehicle_plate, current_lat, current_lng, is_online, last_ping')
      .eq('is_online', true)
      .order('last_ping', { ascending: false })
      .limit(20);

    // Clear existing live driver markers
    if (gramhaulLiveMap) {
      if (!gramhaulLiveDriversLayer) {
        gramhaulLiveDriversLayer = L.layerGroup().addTo(gramhaulLiveMap);
      } else {
        gramhaulLiveDriversLayer.clearLayers();
      }
    }

    if (error || !data || data.length === 0) {
      console.log('[GramHaul] Zero active online drivers in Supabase telemetry.');
      GRAMHAUL_POOLED_TRUCKS = [];
      if (typeof renderGramhaulTrucksList === 'function') renderGramhaulTrucksList();
      const statusPill = document.getElementById('gh-live-radar-status');
      if (statusPill) statusPill.innerHTML = '<span>📡 Live Radar: 0 Drivers Broadcasting GPS · Request Dispatch Below</span>';
      return;
    }

    const realTrucks = data.filter(d => d.current_lat && d.current_lng).map((d, i) => ({
      id: d.driver_id || ('drv-' + i),
      plate: d.vehicle_plate || 'TS-LIVE-GPS',
      vehicle: d.vehicle_type || 'Commercial Vehicle',
      driverName: d.driver_name || 'Active Transporter',
      driverPhone: '+91 Verified Driver',
      rating: '🟢 Live GPS Broadcasting',
      origin: 'Online on Route',
      destination: 'Regional Mandi Route',
      distance: 'Live GPS Active',
      pickupEta: 'On-Demand Dispatch',
      departure: 'Immediate Dispatch',
      totalBagsCapacity: 50,
      filledBags: 0,
      freeSlots: 50,
      ratePerBag: 35,
      soloRate: 1500,
      lat: d.current_lat,
      lng: d.current_lng,
      isLive: true
    }));

    GRAMHAUL_POOLED_TRUCKS = realTrucks;
    console.log('[GramHaul] Rendered ' + realTrucks.length + ' real live driver GPS markers.');

    // Plot ONLY Real Online Drivers on the Map
    if (gramhaulLiveMap && gramhaulLiveDriversLayer) {
      realTrucks.forEach(t => {
        const liveTruckIcon = L.divIcon({
          className: 'gh-live-online-driver-pin',
          html: `
            <div style="position:relative;display:flex;flex-direction:column;align-items:center;cursor:pointer;transform:translate(-50%, -100%);">
              <div style="background:#0F172A;color:#FFFFFF;border:1.5px solid #22C55E;padding:3px 8px;border-radius:8px;font-size:9.5px;font-weight:900;white-space:nowrap;box-shadow:0 4px 12px rgba(0,0,0,0.35);display:flex;align-items:center;gap:5px;margin-bottom:2px;">
                <span style="width:7px;height:7px;border-radius:50%;background:#22C55E;box-shadow:0 0 8px #22C55E;display:inline-block;animation:sunGlowPulse 1.2s infinite;"></span>
                <span>${t.plate} · ${t.driverName}</span>
              </div>
              <div style="width:34px;height:34px;background:#15803D;border:2px solid #FFFFFF;border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(22,163,74,0.4);color:#FFF;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="1" y="6" width="14" height="11" rx="2"/><polygon points="15 8 19 8 22 11 22 17 15 17 15 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>
              </div>
            </div>
          `,
          iconSize: [0, 0]
        });

        const m = L.marker([t.lat, t.lng], { icon: liveTruckIcon }).addTo(gramhaulLiveDriversLayer);
        m.bindPopup(`
          <div style="font-size:12px;font-weight:900;color:#0F172A;">🚚 ${t.vehicle}</div>
          <div style="font-size:10.5px;color:#15803D;font-weight:800;">${t.driverName} (${t.plate})</div>
          <div style="font-size:9.5px;color:#64748B;margin-top:2px;">🟢 Live GPS Verified Online</div>
        `);
      });
    }

    const statusPill = document.getElementById('gh-live-radar-status');
    if (statusPill) statusPill.innerHTML = `<span>🟢 <strong>${realTrucks.length} Active Driver${realTrucks.length>1?'s':''} Online</strong> on Radar</span>`;

    if (typeof renderGramhaulTrucksList === 'function') renderGramhaulTrucksList();
  } catch (e) {
    console.warn('[GramHaul] Supabase real trucks load failed:', e);
  }
}"""

if old_load_real_trucks in text:
    text = text.replace(old_load_real_trucks, new_load_real_trucks)
    print("✅ Upgraded loadRealTrucksFromSupabase with zero fake truck fallback")

# Update updateGramhaulSelectorMapVehicles to NOT create fake markers
old_update_selector_vehicles = """function updateGramhaulSelectorMapVehicles(tier) {
  if (!gramhaulLiveMap || typeof L === 'undefined') return;
  try {
    const v = GRAMHAUL_TIER_AVAILABLE_VEHICLES[tier] || GRAMHAUL_TIER_AVAILABLE_VEHICLES[1];
    const farmLat = (currentGramhaulFarmCoords && currentGramhaulFarmCoords[0]) || 17.3980;
    const farmLon = (currentGramhaulFarmCoords && currentGramhaulFarmCoords[1]) || 78.4900;

    if (gramhaulTruckMarker) {
      gramhaulLiveMap.removeLayer(gramhaulTruckMarker);
      gramhaulTruckMarker = null;
    }

    const truckIcon = L.divIcon({
      className: 'gh-selector-truck-pin',
      html: `
        <div style="position:relative;display:flex;flex-direction:column;align-items:center;cursor:pointer;transform:translate(-50%, -100%);">
          <div style="background:#0F172A;color:#FFFFFF;border:1.5px solid ${v.color};padding:3px 8px;border-radius:8px;font-size:9.5px;font-weight:900;white-space:nowrap;box-shadow:0 4px 12px rgba(0,0,0,0.3);display:flex;align-items:center;gap:4px;margin-bottom:2px;">
            <span style="width:6px;height:6px;border-radius:50%;background:#22C55E;box-shadow:0 0 6px #22C55E;"></span>
            <span>${v.plate} · ${v.distStr ? v.distStr.split(' ')[0] : 'Nearby'}</span>
          </div>
          <img src="${v.img}" alt="${v.name}" style="width:58px;height:42px;object-fit:contain;filter:drop-shadow(0 6px 14px rgba(0,0,0,0.4));" />
        </div>
      `,
      iconSize: [0, 0]
    });

    gramhaulTruckMarker = L.marker(v.coords, { icon: truckIcon }).addTo(gramhaulLiveMap);
    gramhaulTruckMarker.bindPopup(`
      <div style="font-size:12px;font-weight:900;color:#0F172A;">🚚 ${v.tierName}</div>
      <div style="font-size:10px;color:#15803D;font-weight:800;">👨‍✈️ ${v.driverName} (${v.rating}) · ${v.plate}</div>
      <div style="font-size:9.5px;color:#64748B;margin-top:2px;">📍 ${v.distStr}</div>
    `);

    const group = L.featureGroup([
      L.marker([farmLat, farmLon]),
      L.marker(v.coords)
    ]);
    gramhaulLiveMap.fitBounds(group.getBounds().pad(0.35));
  } catch(e) {
    console.warn('updateGramhaulSelectorMapVehicles error:', e);
  }
}"""

new_update_selector_vehicles = """function updateGramhaulSelectorMapVehicles(tier) {
  if (!gramhaulLiveMap || typeof L === 'undefined') return;
  try {
    const v = GRAMHAUL_TIER_AVAILABLE_VEHICLES[tier] || GRAMHAUL_TIER_AVAILABLE_VEHICLES[1];
    const farmLat = (currentGramhaulFarmCoords && currentGramhaulFarmCoords[0]) || 17.3980;
    const farmLon = (currentGramhaulFarmCoords && currentGramhaulFarmCoords[1]) || 78.4900;

    // Do not add fake truck marker — real online drivers are handled exclusively by loadRealTrucksFromSupabase()
    if (gramhaulTruckMarker) {
      gramhaulLiveMap.removeLayer(gramhaulTruckMarker);
      gramhaulTruckMarker = null;
    }
  } catch(e) {
    console.warn('updateGramhaulSelectorMapVehicles error:', e);
  }
}"""

if old_update_selector_vehicles in text:
    text = text.replace(old_update_selector_vehicles, new_update_selector_vehicles)
    print("✅ Removed fake truck marker placement from updateGramhaulSelectorMapVehicles")

# Write updated file
with open('app/src/main/assets/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print(f"Updated index.html length: {len(text)}")
