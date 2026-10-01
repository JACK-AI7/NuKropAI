import os, sys, re

sys.stdout.reconfigure(encoding='utf-8')

# ═════════════════════════════════════════════════════════════════════════
# HIGH-END SVG ICON LIBRARY (Apple SF / Linear / Lucide Ultra-Crisp Icons)
# ═════════════════════════════════════════════════════════════════════════

ICONS = {
    # Navigation & Core
    "home": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9.5L12 3l9 6.5V20a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
    "scanner": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/><path d="M8 8l2 2m0-2l-2 2" stroke="#22C55E" stroke-width="2"/></svg>',
    "market": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
    "gramhaul": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>',
    "agristack": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>',
    "equipment": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
    "loan": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/><path d="M12 18V6"/></svg>',
    "chat": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/></svg>',
    "khata": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/><path d="M6 6h10"/><path d="M6 10h10"/><path d="M6 14h6"/></svg>',
    "bioshield": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
    "biorx": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 2v7.31M14 2v7.31"/><path d="M8.5 2h7"/><path d="M14 9.3a6.5 6.5 0 1 1-4 0"/><path d="M5.52 16h12.96"/></svg>',
    "community": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    
    # Common UI Elements
    "close_x": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>',
    "refresh": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>',
    "bell": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>',
    "pin": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
    "phone": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
    "check": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
    "check_circle": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
    "swap": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M7 16V4M7 4L3 8M7 4L11 8M17 8V20M17 20L21 16M17 20L13 16"/></svg>',
    "gps_target": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="3"/><line x1="12" y1="2" x2="12" y2="6"/><line x1="12" y1="18" x2="12" y2="22"/><line x1="2" y1="12" x2="6" y2="12"/><line x1="18" y1="12" x2="22" y2="12"/></svg>',
    "credit_card": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/></svg>',
    
    # Crop Freight Chips SVGs
    "cotton_svg": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 20h10"/><path d="M10 20c5.5-2.5.8-6.4 3-10"/><path d="M9.5 9.4c1.1.8 1.8 2.2 2.3 3.7-2 .4-3.5.4-4.8-.3-1.2-.6-2.3-1.9-3-4.2 2.8-.5 4.4 0 5.5.8z"/><path d="M14.1 6a7 7 0 0 1 1.1 4c-1.2.1-2.8-.6-3.5-1.5-.7-1-1.3-2.7-1.1-4.8 1.7.2 3 .9 3.5 2.3z"/></svg>',
    "chilli_svg": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/></svg>',
    "tomato_svg": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="14" r="8"/><path d="M12 6V2"/><path d="M8.5 4.5C10 5.5 11 6 12 6c1 0 2-.5 3.5-1.5"/></svg>',
    
    # Golden Vector Stars for Rating
    "star_gold": '<svg width="26" height="26" viewBox="0 0 24 24" fill="#FBBF24" stroke="#D97706" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'
}

# ═════════════════════════════════════════════════════════════════════════
# UPGRADED SIDEBAR WITH LUXURY ICONS
# ═════════════════════════════════════════════════════════════════════════
NEW_SIDEBAR_NAV = """
      <div style="display:grid;grid-template-columns:1fr;gap:6px;" id="side-nav-group">
        <button class="panel-nav-btn active" id="btn-home" onclick="openScreen('home',null);syncSideNav('btn-home')" style="display:flex;align-items:center;gap:10px;padding:10px 14px;border-radius:14px;font-weight:700;">
          """ + ICONS["home"] + """
          <span>Home Dashboard</span>
        </button>
        <button class="panel-nav-btn" id="btn-scanner" onclick="openScreen('scanner',null);syncSideNav('btn-scanner')" style="display:flex;align-items:center;gap:10px;padding:10px 14px;border-radius:14px;font-weight:700;">
          """ + ICONS["scanner"] + """
          <span>AI Crop & Soil Scanner</span>
        </button>
        <button class="panel-nav-btn" id="btn-market" onclick="openScreen('market',null);syncSideNav('btn-market')" style="display:flex;align-items:center;gap:10px;padding:10px 14px;border-radius:14px;font-weight:700;">
          """ + ICONS["market"] + """
          <span>Live Mandi Rates</span>
        </button>
        <button class="panel-nav-btn" id="btn-gramhaul" onclick="openScreen('gramhaul',null);syncSideNav('btn-gramhaul')" style="display:flex;align-items:center;gap:10px;padding:10px 14px;border-radius:14px;font-weight:700;">
          """ + ICONS["gramhaul"] + """
          <span>Mandi Truck Sharing</span>
        </button>
        <button class="panel-nav-btn" id="btn-agristack" onclick="openScreen('agristack',null);syncSideNav('btn-agristack')" style="display:flex;align-items:center;gap:10px;padding:10px 14px;border-radius:14px;font-weight:700;">
          """ + ICONS["agristack"] + """
          <span>Farmer ID & Credit</span>
        </button>
        <button class="panel-nav-btn" id="btn-equipment" onclick="openScreen('equipment',null);syncSideNav('btn-equipment')" style="display:flex;align-items:center;gap:10px;padding:10px 14px;border-radius:14px;font-weight:700;">
          """ + ICONS["equipment"] + """
          <span>Rent Machinery</span>
        </button>
        <button class="panel-nav-btn" id="btn-loan" onclick="openScreen('loan',null);syncSideNav('btn-loan')" style="display:flex;align-items:center;gap:10px;padding:10px 14px;border-radius:14px;font-weight:700;">
          """ + ICONS["loan"] + """
          <span>Loans & Subsidies</span>
        </button>
        <button class="panel-nav-btn" id="btn-chat" onclick="openScreen('chat',null);syncSideNav('btn-chat')" style="display:flex;align-items:center;gap:10px;padding:10px 14px;border-radius:14px;font-weight:700;">
          """ + ICONS["chat"] + """
          <span>24/7 AI Farm Advisor</span>
        </button>
        <button class="panel-nav-btn" id="btn-khata" onclick="openScreen('khata',null);syncSideNav('btn-khata')" style="display:flex;align-items:center;gap:10px;padding:10px 14px;border-radius:14px;font-weight:700;">
          """ + ICONS["khata"] + """
          <span>Farm Khata Ledger</span>
        </button>
        <button class="panel-nav-btn" id="btn-bioshield" onclick="openScreen('bioshield',null);syncSideNav('btn-bioshield')" style="display:flex;align-items:center;gap:10px;padding:10px 14px;border-radius:14px;font-weight:700;">
          """ + ICONS["bioshield"] + """
          <span>Pest & Disease Alerts</span>
        </button>
        <button class="panel-nav-btn" id="btn-biorx" onclick="openScreen('biorx',null);syncSideNav('btn-biorx')" style="display:flex;align-items:center;gap:10px;padding:10px 14px;border-radius:14px;font-weight:700;">
          """ + ICONS["biorx"] + """
          <span>Organic Bio-Medicines</span>
        </button>
      </div>"""


def process_file(filepath):
    print(f"Upgrading icons across {filepath} to high-end SVGs...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace Side Nav Group emojis with sleek SVGs
    side_nav_pattern = r'<div style="display:grid;grid-template-columns:1fr;gap:6px;" id="side-nav-group">[\s\S]*?</div>\s*</div>\s*</div>'
    replacement_side = NEW_SIDEBAR_NAV.strip() + "\n    </div>\n  </div>"
    if re.search(side_nav_pattern, content):
        content = re.sub(side_nav_pattern, replacement_side, content, count=1)
        print("Updated side navigation bar with high-end SVG icons!")

    # 2. Replace Modal Close Buttons `✕` with sleek Lucide Close SVG
    # We match `<button onclick="close...Modal... style="...">✕</button>`
    close_svg = """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>"""
    content = re.sub(r'(<button\s+onclick="[^"]*close[^"]*Modal[^"]*"[^>]*>)✕(<\/button>)', r'\1' + close_svg + r'\2', content)
    content = re.sub(r'(<button\s+onclick="[^"]*dismissPushToast[^"]*"[^>]*>)✕(<\/button>)', r'\1' + close_svg + r'\2', content)
    content = re.sub(r'(<button\s+onclick="document\.getElementById\(\'google-auth-modal\'\)\.remove\(\)"[^>]*>)✕(<\/button>)', r'\1' + close_svg + r'\2', content)
    content = re.sub(r'(<button\s+onclick="document\.getElementById\(\'google-auth-modal\'\)\?\.remove\(\)"[^>]*>)✕(<\/button>)', r'\1' + close_svg + r'\2', content)

    # 3. Upgrade GramHaul Crop Chips and Components
    # Replace Cotton emoji with cotton_svg
    content = content.replace(
        '<span>🌾</span>\n              <span>Cotton · 40 Qtl</span>',
        f'<span style="color:#16A34A;display:flex;">{ICONS["cotton_svg"]}</span>\n              <span>Cotton · 40 Qtl</span>'
    )
    content = content.replace(
        '<span>🌶️</span>\n              <span>Chilli · 25 Bags (2.5T)</span>',
        f'<span style="color:#DC2626;display:flex;">{ICONS["chilli_svg"]}</span>\n              <span>Chilli · 25 Bags (2.5T)</span>'
    )
    content = content.replace(
        '<span>🍅</span>\n              <span>Tomato · 60 Crates</span>',
        f'<span style="color:#EA580C;display:flex;">{ICONS["tomato_svg"]}</span>\n              <span>Tomato · 60 Crates</span>'
    )

    # Replace GramHaul Swap ⇅ with SVG
    content = content.replace(
        '<button onclick="swapGramhaulLocations()" style="position:absolute;right:0;width:32px;height:32px;border-radius:50%;background:#F8FAFC;border:1px solid #E2E8F0;display:flex;align-items:center;justify-content:center;color:#64748B;cursor:pointer;">\n              ⇅\n            </button>',
        f'<button onclick="swapGramhaulLocations()" style="position:absolute;right:0;width:32px;height:32px;border-radius:50%;background:#F8FAFC;border:1px solid #E2E8F0;display:flex;align-items:center;justify-content:center;color:#64748B;cursor:pointer;">\n              {ICONS["swap"]}\n            </button>'
    )

    # Replace GramHaul Phase 3 Stars ★ with Golden SVG Stars
    star_svg = ICONS["star_gold"]
    old_stars = """<div style="display:flex;justify-content:center;gap:8px;font-size:26px;color:#16A34A;cursor:pointer;margin-bottom:12px;">
              <span onclick="setGramhaulRating(1)">★</span>
              <span onclick="setGramhaulRating(2)">★</span>
              <span onclick="setGramhaulRating(3)">★</span>
              <span onclick="setGramhaulRating(4)">★</span>
              <span onclick="setGramhaulRating(5)">★</span>
            </div>"""
    new_stars = f"""<div style="display:flex;justify-content:center;gap:10px;cursor:pointer;margin-bottom:14px;">
              <span onclick="setGramhaulRating(1)" style="display:inline-flex;transition:transform 0.15s ease;" onmouseenter="this.style.transform='scale(1.2)'" onmouseleave="this.style.transform='scale(1)'">{star_svg}</span>
              <span onclick="setGramhaulRating(2)" style="display:inline-flex;transition:transform 0.15s ease;" onmouseenter="this.style.transform='scale(1.2)'" onmouseleave="this.style.transform='scale(1)'">{star_svg}</span>
              <span onclick="setGramhaulRating(3)" style="display:inline-flex;transition:transform 0.15s ease;" onmouseenter="this.style.transform='scale(1.2)'" onmouseleave="this.style.transform='scale(1)'">{star_svg}</span>
              <span onclick="setGramhaulRating(4)" style="display:inline-flex;transition:transform 0.15s ease;" onmouseenter="this.style.transform='scale(1.2)'" onmouseleave="this.style.transform='scale(1)'">{star_svg}</span>
              <span onclick="setGramhaulRating(5)" style="display:inline-flex;transition:transform 0.15s ease;" onmouseenter="this.style.transform='scale(1.2)'" onmouseleave="this.style.transform='scale(1)'">{star_svg}</span>
            </div>"""
    content = content.replace(old_stars, new_stars)

    # Replace GramHaul Phase 3 Credit Card Emoji 💳 with SVG
    content = content.replace(
        '<span style="font-size:18px;">💳</span>',
        f'<span style="display:flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:10px;background:#E0F2FE;">{ICONS["credit_card"]}</span>'
    )

    # Replace Mandi refresh button 🔄 with SVG
    old_refresh = '<button id="home-mandi-refresh-btn" onclick="event.stopPropagation();refreshMandiRatesLive();" style="background:#F1F5F9;border:1px solid #E2E8F0;border-radius:10px;width:32px;height:32px;display:flex;align-items:center;justify-content:center;font-size:13px;cursor:pointer;color:#0F172A;transition:all 0.15s ease;">🔄</button>'
    new_refresh = f'<button id="home-mandi-refresh-btn" onclick="event.stopPropagation();refreshMandiRatesLive();" style="background:#F1F5F9;border:1px solid #E2E8F0;border-radius:10px;width:32px;height:32px;display:flex;align-items:center;justify-content:center;cursor:pointer;color:#0F172A;transition:all 0.15s ease;">{ICONS["refresh"]}</button>'
    content = content.replace(old_refresh, new_refresh)

    # Replace Driver Dashboard buttons 📞 and ✅
    content = re.sub(
        r'<button\s+onclick="openDriverCallModal\(([^)]+)\)"\s+style="([^"]+)">📞<\/button>',
        rf'<button onclick="openDriverCallModal(\1)" style="\2;display:inline-flex;align-items:center;justify-content:center;">{ICONS["phone"]}</button>',
        content
    )
    content = re.sub(
        r'<button\s+onclick="acceptHaulBooking\(([^)]+)\)"\s+style="([^"]+)">✅<\/button>',
        rf'<button onclick="acceptHaulBooking(\1)" style="\2;display:inline-flex;align-items:center;justify-content:center;">{ICONS["check_circle"]}</button>',
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully updated {filepath}!")

if __name__ == '__main__':
    process_file('app/src/main/assets/index.html')
    process_file('nukrop_emulator.html')
