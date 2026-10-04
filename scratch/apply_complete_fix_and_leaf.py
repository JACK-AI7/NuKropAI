import os
import re

INDEX_PATH = r"app/src/main/assets/index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# ══════════════════════════════════════════════════════════════════════════
# 1. CHANGE CENTER NAVBAR FAB ICON TO CLASSIC ORGANIC LEAF
# ══════════════════════════════════════════════════════════════════════════
old_fab_pattern = re.compile(
    r'(<div class="dock-center-fab">)\s*<svg.*?</svg>\s*(</div>)',
    re.DOTALL
)

new_fab_leaf = r'''\1
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 3.5 1 9.2A7 7 0 0 1 11 20z" fill="rgba(255,255,255,0.28)"/>
              <path d="M11 20v-8"/>
              <path d="M11 15l3-2"/>
              <path d="M11 12l-2.5-1.5"/>
            </svg>
          \2'''

content = old_fab_pattern.sub(new_fab_leaf, content)

# ══════════════════════════════════════════════════════════════════════════
# 2. ENHANCE NAVBAR WITH INTERACTIVE ANIMATIONS & REACTBITS MICRO-PHYSICS
# ══════════════════════════════════════════════════════════════════════════
nav_css_upgrade = """
/* ══════════════════════════════════════════════════════════════
   REACTBITS-GRADE INTERACTIVE ANIMATED NAVIGATION BAR & FAB
   ══════════════════════════════════════════════════════════════ */
.dock-tab-btn {
  position: relative;
  transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), color 0.15s ease !important;
  -webkit-tap-highlight-color: transparent;
  user-select: none;
}
.dock-tab-btn:active {
  transform: scale(0.84) translateY(1px) !important;
}
.dock-tab-btn svg {
  transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1), stroke 0.2s ease, stroke-width 0.2s ease !important;
}
.dock-tab-btn.active svg {
  stroke: #16A34A !important;
  stroke-width: 2.4 !important;
  transform: translateY(-3px) scale(1.12) !important;
  filter: drop-shadow(0 3px 8px rgba(22,163,74,0.38)) !important;
}
.dock-tab-btn.active span {
  color: #16A34A !important;
  font-weight: 900 !important;
  transform: translateY(-1px);
}
.dock-tab-btn.active::after {
  content: '';
  position: absolute;
  bottom: -2px;
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #16A34A;
  box-shadow: 0 0 8px #22C55E, 0 0 12px rgba(34,197,94,0.6);
  animation: navDotPop 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}
@keyframes navDotPop {
  0% { transform: scale(0); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}

/* Center Organic Leaf FAB Floating Animation */
.dock-center-fab {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: radial-gradient(circle at 35% 30%, #22C55E 0%, #16A34A 55%, #15803D 100%) !important;
  box-shadow: 0 6px 20px rgba(22,163,74,0.42), 0 2px 6px rgba(0,0,0,0.08) !important;
  animation: leafFabBreathe 3s infinite ease-in-out !important;
  transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.2s ease !important;
}
.dock-center-fab:active {
  transform: scale(0.88) !important;
  box-shadow: 0 3px 10px rgba(22,163,74,0.3) !important;
}
.dock-center-fab svg {
  animation: leafSway 4s infinite ease-in-out;
  transform-origin: bottom center;
}
@keyframes leafFabBreathe {
  0%, 100% {
    box-shadow: 0 6px 20px rgba(22,163,74,0.42), 0 0 0 0 rgba(34,197,94,0.35);
  }
  50% {
    box-shadow: 0 8px 28px rgba(22,163,74,0.6), 0 0 0 7px rgba(34,197,94,0);
  }
}
@keyframes leafSway {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(-3deg); }
  75% { transform: rotate(3deg); }
}
"""

if "/* REACTBITS-GRADE INTERACTIVE ANIMATED NAVIGATION BAR & FAB */" not in content:
    content = content.replace("</style>", nav_css_upgrade + "\n</style>", 1)

# ══════════════════════════════════════════════════════════════════════════
# 3. REMOVE RAW EMOJI PREFIXES FROM PAGE HEADERS ACROSS APP
# ══════════════════════════════════════════════════════════════════════════
# Market Header: Remove 📊 emoji
content = content.replace('📊 ${mktTitle}', '${mktTitle}')
content = content.replace('📍 ${autoLocBtn}', '${autoLocBtn}')
content = content.replace('📊 Range:', '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" style="display:inline-block;vertical-align:middle;margin-right:2px;"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg> Range:')
content = content.replace('🚚 Arrivals:', '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display:inline-block;vertical-align:middle;margin-right:2px;"><rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg> Arrivals:')
content = content.replace('🚚 Book Mandi Truck', '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display:inline-block;vertical-align:middle;margin-right:4px;"><rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg> Book Mandi Truck')
content = content.replace('📈 Price Trend', '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" style="display:inline-block;vertical-align:middle;margin-right:4px;"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg> Price Trend')

# Community Header: Remove 👥 emoji
content = re.sub(
    r'<span>👥</span>\s*<span>\$\{TL\(\'Kisan Community\'',
    r'<span><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#15803D" stroke-width="2.2" stroke-linecap="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg></span>\n          <span>${TL(\'Kisan Community\'',
    content
)

# Rent Machinery Header: Remove 🚜 emoji
content = content.replace("🚜 ${TL('Rent Machinery'", "<svg width=\"20\" height=\"20\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"#15803D\" stroke-width=\"2.2\" style=\"display:inline-block;vertical-align:middle;margin-right:6px;\"><path d=\"M8 26H18L21 14H30V26H43V32\"/><circle cx=\"31\" cy=\"33\" r=\"5\"/><circle cx=\"9.5\" cy=\"33\" r=\"3.5\"/></svg>${TL('Rent Machinery'")

# ══════════════════════════════════════════════════════════════════════════
# 4. FIX COMMUNITY OPENING & FILTERING GLITCHES
# ══════════════════════════════════════════════════════════════════════════
new_set_filter_fn = """function setCommunityFilter(cat) {
  currentCommunityFilter = cat;
  const container = document.getElementById('comm-feed-container');
  if (container) {
    // Fast in-place filter update without full screen tear-down
    document.querySelectorAll('[onclick^="setCommunityFilter"]').forEach(btn => {
      const match = btn.getAttribute('onclick').match(/setCommunityFilter\\('([^']+)'\\)/);
      if (match && match[1]) {
        const isMatch = match[1] === cat;
        btn.style.background = isMatch ? '#0F172A' : '#FFFFFF';
        btn.style.color = isMatch ? '#FFFFFF' : '#475569';
        btn.style.borderColor = isMatch ? '#0F172A' : '#E2E8F0';
        btn.style.boxShadow = isMatch ? '0 2px 6px rgba(15,23,42,0.15)' : '0 1px 2px rgba(0,0,0,0.02)';
      }
    });
    renderCommunityFeedDom();
  } else {
    openScreen('community', document.getElementById('tab-community'));
  }
}"""

content = re.sub(
    r'function setCommunityFilter\(cat\)\s*\{[^}]*\}',
    new_set_filter_fn,
    content
)

# Ensure openScreen('community') ALWAYS renders feed reliably
if "if (screenKey === 'community') setTimeout(renderCommunityFeedDom, 30);" not in content:
    content = content.replace(
        "if (screenKey === 'home') updateWeatherCardDom();",
        "if (screenKey === 'home') updateWeatherCardDom();\n  if (screenKey === 'community') setTimeout(renderCommunityFeedDom, 30);",
        1
    )

# ══════════════════════════════════════════════════════════════════════════
# 5. REMOVE OLD DUPLICATE PRIVACY POLICY MODAL
# ══════════════════════════════════════════════════════════════════════════
content = re.sub(
    r'function openPrivacyPolicyModal\(\)\s*\{\s*const modal = document\.getElementById\(\'privacy-policy-modal\'\);\s*if \(modal\) modal\.style\.display = \'flex\';\s*\}',
    '// openPrivacyPolicyModal is defined in the modal suite below',
    content
)

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("SUCCESS: Center leaf icon restored, animated interactive nav added, headers cleaned, and community routing perfected!")
