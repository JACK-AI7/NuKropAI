import os
import re

INDEX_PATH = r"app/src/main/assets/index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# ══════════════════════════════════════════════════════════════════════════
# 1. BENTO GRID ICONS UPGRADE
# ══════════════════════════════════════════════════════════════════════════
bento_pattern = re.compile(
    r'(<!-- Core Farming Operations -->.*?)(<div style="font-size:14px;font-weight:900;color:#0F172A;padding:0 18px 8px;">\s*\$\{t\.fieldCalcs\})',
    re.DOTALL
)

new_bento = """<!-- Core Farming Operations -->
    <div style="font-size:16px;font-weight:900;color:#0F172A;padding:0 18px 8px;">
      ${t.coreOps}
    </div>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:0 18px 14px;">
      <!-- 1. Mandi Truck Sharing -->
      <div class="suite-bento-tile" onclick="openScreen('gramhaul',null);syncSideNav('btn-gramhaul')">
        <div class="icon-plate" style="background:linear-gradient(135deg,#FFF7ED 0%,#FFEDD5 100%);border:1px solid #FED7AA;border-radius:18px;width:48px;height:48px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(234,88,12,0.16);">
          <svg width="28" height="28" viewBox="0 0 48 48" fill="none">
            <defs>
              <linearGradient id="gh-truck-body" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#FB923C"/>
                <stop offset="100%" stop-color="#EA580C"/>
              </linearGradient>
              <linearGradient id="gh-truck-cab" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#F97316"/>
                <stop offset="100%" stop-color="#C2410C"/>
              </linearGradient>
            </defs>
            <rect x="4" y="12" width="25" height="20" rx="3" fill="url(#gh-truck-body)"/>
            <path d="M29 17H38.5C39.6 17 40.6 17.6 41.2 18.5L44.5 24C44.8 24.6 45 25.3 45 26V32H29V17Z" fill="url(#gh-truck-cab)"/>
            <path d="M31 19.5H37.8L40.8 24H31V19.5Z" fill="#E0F2FE"/>
            <rect x="7" y="16" width="19" height="2.5" rx="1" fill="#FFEDD5" opacity="0.9"/>
            <rect x="7" y="21" width="13" height="2.5" rx="1" fill="#FFEDD5" opacity="0.9"/>
            <circle cx="12" cy="34" r="5" fill="#1E293B"/>
            <circle cx="12" cy="34" r="2.2" fill="#F8FAFC"/>
            <circle cx="36" cy="34" r="5" fill="#1E293B"/>
            <circle cx="36" cy="34" r="2.2" fill="#F8FAFC"/>
            <circle cx="43" cy="28.5" r="1.5" fill="#FEF08A"/>
          </svg>
        </div>
        <div>
          <div style="font-size:15px;font-weight:800;color:#0F172A;letter-spacing:-0.2px;line-height:1.2;">${t.truckTitle}</div>
          <div style="font-size:12px;color:#64748B;margin-top:4px;font-weight:500;">${t.truckSub}</div>
        </div>
      </div>

      <!-- 2. Farmer ID & Credit -->
      <div class="suite-bento-tile" onclick="openScreen('agristack',null);syncSideNav('btn-agristack')">
        <div class="icon-plate" style="background:linear-gradient(135deg,#EFF6FF 0%,#DBEAFE 100%);border:1px solid #BFDBFE;border-radius:18px;width:48px;height:48px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(37,99,235,0.16);">
          <svg width="28" height="28" viewBox="0 0 48 48" fill="none">
            <defs>
              <linearGradient id="gh-card-bg" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#3B82F6"/>
                <stop offset="100%" stop-color="#1D4ED8"/>
              </linearGradient>
              <linearGradient id="gh-chip-gold" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#FDE047"/>
                <stop offset="100%" stop-color="#CA8A04"/>
              </linearGradient>
            </defs>
            <rect x="4" y="9" width="40" height="30" rx="5" fill="url(#gh-card-bg)"/>
            <rect x="9" y="16" width="9" height="7.5" rx="2" fill="url(#gh-chip-gold)"/>
            <path d="M9 20H18M13.5 16V23.5" stroke="#854D0E" stroke-width="0.8"/>
            <rect x="9" y="28" width="16" height="2.5" rx="1" fill="#DBEAFE"/>
            <rect x="9" y="32" width="10" height="2" rx="1" fill="#93C5FD"/>
            <circle cx="35" cy="27" r="6" fill="#15803D" stroke="#FFFFFF" stroke-width="1.5"/>
            <path d="M32.5 27L34.2 28.8L37.8 25.2" stroke="#FFFFFF" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <div>
          <div style="font-size:15px;font-weight:800;color:#0F172A;letter-spacing:-0.2px;line-height:1.2;">${t.idTitle}</div>
          <div style="font-size:12px;color:#64748B;margin-top:4px;font-weight:500;">${t.idSub}</div>
        </div>
      </div>

      <!-- 3. Rent Machinery -->
      <div class="suite-bento-tile" onclick="openScreen('equipment',null);syncSideNav('btn-equipment')">
        <div class="icon-plate" style="background:linear-gradient(135deg,#F0FDF4 0%,#DCFCE7 100%);border:1px solid #BBF7D0;border-radius:18px;width:48px;height:48px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(22,163,74,0.16);">
          <svg width="28" height="28" viewBox="0 0 48 48" fill="none">
            <defs>
              <linearGradient id="gh-tractor-body" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#22C55E"/>
                <stop offset="100%" stop-color="#15803D"/>
              </linearGradient>
            </defs>
            <path d="M8 26H18L21 14H30V26H43V32H38V31C38 27.5 35 24.5 31 24.5C27 24.5 24 27.5 24 31V32H14V31C14 28.5 12 26.5 9.5 26.5C7 26.5 5 28.5 5 31V32H4V29L8 26Z" fill="url(#gh-tractor-body)"/>
            <path d="M23 16H28V23H20L23 16Z" fill="#E0F2FE"/>
            <rect x="37" y="12" width="2.5" height="12" rx="1" fill="#475569"/>
            <circle cx="31" cy="33" r="8.5" fill="#1E293B"/>
            <circle cx="31" cy="33" r="4.5" fill="#FACC15" stroke="#CA8A04" stroke-width="1"/>
            <circle cx="31" cy="33" r="2" fill="#1E293B"/>
            <circle cx="9.5" cy="33" r="5" fill="#1E293B"/>
            <circle cx="9.5" cy="33" r="2" fill="#FACC15"/>
          </svg>
        </div>
        <div>
          <div style="font-size:15px;font-weight:800;color:#0F172A;letter-spacing:-0.2px;line-height:1.2;">${t.rentTitle}</div>
          <div style="font-size:12px;color:#64748B;margin-top:4px;font-weight:500;">${t.rentSub}</div>
        </div>
      </div>

      <!-- 4. Loans & Subsidies -->
      <div class="suite-bento-tile" onclick="openScreen('loan',null);syncSideNav('btn-loan')">
        <div class="icon-plate" style="background:linear-gradient(135deg,#FEF2F2 0%,#FEE2E2 100%);border:1px solid #FECACA;border-radius:18px;width:48px;height:48px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(245,158,11,0.16);">
          <svg width="28" height="28" viewBox="0 0 48 48" fill="none">
            <defs>
              <linearGradient id="gh-loan-coin" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#FDE047"/>
                <stop offset="50%" stop-color="#F59E0B"/>
                <stop offset="100%" stop-color="#D97706"/>
              </linearGradient>
            </defs>
            <circle cx="24" cy="27" r="15" fill="url(#gh-loan-coin)"/>
            <circle cx="24" cy="27" r="12" stroke="#FEF08A" stroke-width="1.5" fill="none"/>
            <path d="M19 20H29M19 23.5H27M19 20V26C21 26 24 26 24 23.5M22 26L28 33" stroke="#78350F" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M24 14C24 8 29 6 29 6C29 6 29 11 25 13.5" fill="#22C55E" stroke="#15803D" stroke-width="1.2" stroke-linejoin="round"/>
            <path d="M24 14C24 9 19 7 19 7C19 7 19 12 23 13.8" fill="#16A34A" stroke="#15803D" stroke-width="1.2" stroke-linejoin="round"/>
          </svg>
        </div>
        <div>
          <div style="font-size:15px;font-weight:800;color:#0F172A;letter-spacing:-0.2px;line-height:1.2;">${t.loanTitle}</div>
          <div style="font-size:12px;color:#64748B;margin-top:4px;font-weight:500;">${t.loanSub}</div>
        </div>
      </div>

      <!-- 5. Farm Khata Ledger -->
      <div class="suite-bento-tile" onclick="openScreen('khata',null);syncSideNav('btn-khata')">
        <div class="icon-plate" style="background:linear-gradient(135deg,#F5F3FF 0%,#EDE9FE 100%);border:1px solid #DDD6FE;border-radius:18px;width:48px;height:48px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(220,38,38,0.16);">
          <svg width="28" height="28" viewBox="0 0 48 48" fill="none">
            <defs>
              <linearGradient id="gh-khata-cover" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#EF4444"/>
                <stop offset="100%" stop-color="#B91C1C"/>
              </linearGradient>
            </defs>
            <rect x="7" y="6" width="34" height="36" rx="4" fill="url(#gh-khata-cover)"/>
            <path d="M7 6H13V42H7Z" fill="#7F1D1D"/>
            <rect x="16" y="10" width="21" height="28" rx="2" fill="#FFFFFF"/>
            <line x1="20" y1="16" x2="33" y2="16" stroke="#EF4444" stroke-width="1.8" stroke-linecap="round"/>
            <line x1="20" y1="21" x2="33" y2="21" stroke="#EF4444" stroke-width="1.8" stroke-linecap="round"/>
            <line x1="20" y1="26" x2="29" y2="26" stroke="#EF4444" stroke-width="1.8" stroke-linecap="round"/>
            <circle cx="26.5" cy="32.5" r="3.5" fill="#FACC15"/>
            <path d="M25 31H28M25 32.5H27.5M25 31V34M26.5 34L28 35.5" stroke="#78350F" stroke-width="0.8" stroke-linecap="round"/>
            <path d="M13 18L13 28" stroke="#FDE047" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </div>
        <div>
          <div style="font-size:15px;font-weight:800;color:#0F172A;letter-spacing:-0.2px;line-height:1.2;">${t.khataTitle}</div>
          <div style="font-size:12px;color:#64748B;margin-top:4px;font-weight:500;">${t.khataSub}</div>
        </div>
      </div>

      <!-- 6. 24/7 AI Farm Advisor -->
      <div class="suite-bento-tile" onclick="openScreen('chat',null);syncSideNav('btn-chat')">
        <div class="icon-plate" style="background:linear-gradient(135deg,#ECFDF5 0%,#D1FAE5 100%);border:1px solid #A7F3D0;border-radius:18px;width:48px;height:48px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(16,185,129,0.18);">
          <svg width="28" height="28" viewBox="0 0 48 48" fill="none">
            <defs>
              <linearGradient id="gh-ai-head" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#34D399"/>
                <stop offset="100%" stop-color="#059669"/>
              </linearGradient>
            </defs>
            <rect x="8" y="12" width="32" height="26" rx="8" fill="url(#gh-ai-head)"/>
            <circle cx="18" cy="23" r="3.5" fill="#FFFFFF"/>
            <circle cx="30" cy="23" r="3.5" fill="#FFFFFF"/>
            <circle cx="18.8" cy="23" r="1.8" fill="#064E3B"/>
            <circle cx="30.8" cy="23" r="1.8" fill="#064E3B"/>
            <path d="M20 31C22 33 26 33 28 31" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"/>
            <path d="M24 4V12" stroke="#10B981" stroke-width="3" stroke-linecap="round"/>
            <circle cx="24" cy="4" r="3" fill="#FDE047" stroke="#059669" stroke-width="1"/>
            <rect x="4" y="21" width="4" height="8" rx="2" fill="#047857"/>
            <rect x="40" y="21" width="4" height="8" rx="2" fill="#047857"/>
          </svg>
        </div>
        <div>
          <div style="font-size:15px;font-weight:800;color:#0F172A;letter-spacing:-0.2px;line-height:1.2;">${t.aiTitle}</div>
          <div style="font-size:12px;color:#64748B;margin-top:4px;font-weight:500;">${t.aiSub}</div>
        </div>
      </div>

      <!-- 7. Pest & Disease Alerts -->
      <div class="suite-bento-tile" onclick="openScreen('bioshield',null);syncSideNav('btn-bioshield')">
        <div class="icon-plate" style="background:linear-gradient(135deg,#FEF2F2 0%,#FEE2E2 100%);border:1px solid #FECDD3;border-radius:18px;width:48px;height:48px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(220,38,38,0.15);">
          <svg width="28" height="28" viewBox="0 0 48 48" fill="none">
            <defs>
              <linearGradient id="gh-radar-grad" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#F87171"/>
                <stop offset="100%" stop-color="#DC2626"/>
              </linearGradient>
            </defs>
            <circle cx="24" cy="24" r="18" stroke="#FCA5A5" stroke-width="1.8" fill="#FEF2F2"/>
            <circle cx="24" cy="24" r="12" stroke="#F87171" stroke-width="1.8" fill="none"/>
            <circle cx="24" cy="24" r="6" fill="url(#gh-radar-grad)"/>
            <line x1="24" y1="4" x2="24" y2="44" stroke="#EF4444" stroke-width="1.5" stroke-dasharray="2 2"/>
            <line x1="4" y1="24" x2="44" y2="24" stroke="#EF4444" stroke-width="1.5" stroke-dasharray="2 2"/>
            <path d="M24 24L36 12" stroke="#B91C1C" stroke-width="2.5" stroke-linecap="round"/>
            <circle cx="36" cy="12" r="3.5" fill="#EF4444" stroke="#FFFFFF" stroke-width="1.5"/>
          </svg>
        </div>
        <div>
          <div style="font-size:15px;font-weight:800;color:#0F172A;letter-spacing:-0.2px;line-height:1.2;">${t.radarTitle}</div>
          <div style="font-size:12px;color:#64748B;margin-top:4px;font-weight:500;">${t.radarSub}</div>
        </div>
      </div>

      <!-- 8. Organic Bio-Medicines -->
      <div class="suite-bento-tile" onclick="openScreen('biorx',null);syncSideNav('btn-biorx')">
        <div class="icon-plate" style="background:linear-gradient(135deg,#F0FDF4 0%,#DCFCE7 100%);border:1px solid #86EFAC;border-radius:18px;width:48px;height:48px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(22,163,74,0.18);">
          <svg width="28" height="28" viewBox="0 0 48 48" fill="none">
            <defs>
              <linearGradient id="gh-mortar-grad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#22C55E"/>
                <stop offset="100%" stop-color="#15803D"/>
              </linearGradient>
            </defs>
            <path d="M10 26C10 36 16 41 24 41C32 41 38 36 38 26H10Z" fill="url(#gh-mortar-grad)"/>
            <rect x="8" y="22" width="32" height="5" rx="2.5" fill="#14532D"/>
            <path d="M20 7C14 9 12 16 15 21C18 23 23 21 24 18C25 15 25 10 20 7Z" fill="#4ADE80"/>
            <path d="M27 9C33 11 35 17 32 22C29 24 25 22 24 19C23 16 23 12 27 9Z" fill="#86EFAC"/>
            <path d="M30 14L37 6C38 5 40 5 41 6C42 7 42 9 41 10L35 17" stroke="#F59E0B" stroke-width="2.5" stroke-linecap="round"/>
          </svg>
        </div>
        <div>
          <div style="font-size:15px;font-weight:800;color:#0F172A;letter-spacing:-0.2px;line-height:1.2;">${t.bioTitle}</div>
          <div style="font-size:12px;color:#64748B;margin-top:4px;font-weight:500;">${t.bioSub}</div>
        </div>
      </div>
    </div>
    """

content = bento_pattern.sub(new_bento + r"\2", content)

# ══════════════════════════════════════════════════════════════════════════
# 2. SCANNER VIEW UPGRADE
# ══════════════════════════════════════════════════════════════════════════
scanner_pattern = re.compile(
    r'(scanner:\s*\(\)\s*=>\s*\{.*?)(<!-- ══════════════ TAB 2: SAVED SCANS & PRESCRIPTIONS HISTORY ══════════════ -->)',
    re.DOTALL
)

new_scanner = """scanner: () => {
    const isTe = currentLang === 'te';
    const isHi = currentLang === 'hi';
    const scanTitle = TL('AI Plant & Soil Doctor', 'AI పంట & నేల డాక్టర్', 'AI फसल व मिट्टी डॉक्टर');
    const leafBtn = TL('Leaf Doctor', 'ఆకు పరీక్ష', 'पत्ती डॉक्टर');
    const soilBtn = TL('Soil NPK', 'నేల NPK', 'मिट्टी NPK');
    const targetHint = TL('Target Crop Leaf in Frame', 'పంట ఆకును ఫ్రేమ్‌లో ఉంచండి', 'फसल की पत्ती पर फोकस करें');
    const lightHint = TL('Hold 15–25 cm in clear natural lighting', 'స్పష్టమైన సహజ వెలుతురులో 15–25 సెం.మీ దూరంలో ఉంచండి', 'अच्छी रोशनी में 15–25 सेमी की दूरी पर रखें');
    const actionBtn = TL('Scan & Diagnose with AI', 'AI తో స్కాన్ చేసి విశ్లేషించండి', 'AI से स्कैन व विश्लेषण करें');

    const scansCount = (typeof savedScansHistory !== 'undefined' && Array.isArray(savedScansHistory)) ? savedScansHistory.length : 2;
    const historyLabel = isTe ? ('భద్రపరచినవి (' + scansCount + ')') : (isHi ? ('सुरक्षित (' + scansCount + ')') : ('Saved Scans (' + scansCount + ')'));

    return `
    <!-- Top Navigation Bar -->
    <div style="background:#F8FAF8;padding:max(48px, env(safe-area-inset-top, 48px)) 18px 10px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:10;border-bottom:1px solid #E2ECE2;">
      <div style="display:flex;align-items:center;gap:10px;">
        <button onclick="openScreen('home',null);syncSideNav('btn-home')" style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;cursor:pointer;padding:6px;display:flex;align-items:center;justify-content:center;box-shadow:0 1px 3px rgba(0,0,0,0.04);">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#15803D" stroke-width="2.5" stroke-linecap="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
        </button>
        <div>
          <div style="font-size:16.5px;font-weight:900;color:#0F172A;letter-spacing:-0.3px;">${scanTitle}</div>
          <div style="font-size:10px;color:#16A34A;font-weight:800;display:flex;align-items:center;gap:4px;margin-top:1px;">
            <span style="width:6px;height:6px;background:#22C55E;border-radius:50%;display:inline-block;animation:sunGlowPulse 1.2s infinite;"></span>
            <span>TokenRouter AI + ICAR Vision 4K</span>
          </div>
        </div>
      </div>
      <div style="display:flex;background:#E2ECE2;border-radius:20px;padding:3px;gap:2px;">
        <button id="mode-crop-btn" onclick="setScanMode('crop')" style="background:${currentScanMode==='crop'?'#15803D':'transparent'};color:${currentScanMode==='crop'?'#FFFFFF':'#475569'};border:none;border-radius:14px;padding:5px 12px;font-size:11px;font-weight:800;cursor:pointer;transition:all 0.15s ease;display:flex;align-items:center;gap:4px;">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 3.5 1 9.2A7 7 0 0 1 11 20z"/><path d="M11 20v-8"/></svg>
          <span>${leafBtn}</span>
        </button>
        <button id="mode-soil-btn" onclick="setScanMode('soil')" style="background:${currentScanMode==='soil'?'#15803D':'transparent'};color:${currentScanMode==='soil'?'#FFFFFF':'#475569'};border:none;border-radius:14px;padding:5px 12px;font-size:11px;font-weight:800;cursor:pointer;transition:all 0.15s ease;display:flex;align-items:center;gap:4px;">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M10 2v7.31M14 9.3V1.99M8.5 2h7M14 9.3a6.5 6.5 0 1 1-4 0"/></svg>
          <span>${soilBtn}</span>
        </button>
      </div>
    </div>

    <!-- Scanner Mode Switcher: Live Camera vs Saved Scans History -->
    <div style="background:#F4FAF5;padding:8px 18px 10px;display:flex;gap:8px;">
      <button id="scan-tab-camera-btn" onclick="switchScannerTab('camera')" style="flex:1;background:${activeScannerTab==='camera'?'#15803D':'#FFFFFF'};color:${activeScannerTab==='camera'?'#FFFFFF':'#15803D'};border:1.2px solid #86EFAC;border-radius:12px;padding:8px 0;font-size:12px;font-weight:900;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:6px;box-shadow:0 2px 6px rgba(0,0,0,0.03);">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>
        <span>${TL('Live AI Camera', 'లైవ్ కెమెరా', 'Live Camera')}</span>
      </button>
      <button id="scan-tab-history-btn" onclick="switchScannerTab('history')" style="flex:1;background:${activeScannerTab==='history'?'#15803D':'#FFFFFF'};color:${activeScannerTab==='history'?'#FFFFFF':'#15803D'};border:1.2px solid #86EFAC;border-radius:12px;padding:8px 0;font-size:12px;font-weight:900;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:6px;box-shadow:0 2px 6px rgba(0,0,0,0.03);">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
        <span>${historyLabel}</span>
      </button>
    </div>

    <!-- ══════════════ TAB 1: LIVE CAMERA SCANNER ══════════════ -->
    <div id="scanner-camera-view" style="display:${activeScannerTab==='camera'?'block':'none'};">
      <!-- Viewfinder Hero Box -->
      <div class="viewfinder-box" style="height:350px;margin:8px 18px 12px;width:calc(100% - 36px);border-radius:24px;border:1.5px solid rgba(34,197,94,0.45);box-shadow:0 12px 36px rgba(0,0,0,0.4);">
        <!-- Top HUD Bar: Flash, Status Badge, Gallery Upload -->
        <div style="width:100%;display:flex;justify-content:space-between;align-items:center;z-index:10;">
          <button type="button" onclick="toggleScannerFlash(this)" style="background:rgba(255,255,255,0.18);border:1px solid rgba(255,255,255,0.25);color:#FFFFFF;border-radius:14px;padding:5px 12px;font-size:11px;font-weight:800;cursor:pointer;display:flex;align-items:center;gap:4px;backdrop-filter:blur(6px);">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
            <span>${TL('Flash', 'ఫ్లాష్', 'Flash')}</span>
          </button>
          <div style="display:flex;align-items:center;gap:5px;background:rgba(0,0,0,0.75);border:1px solid rgba(34,197,94,0.4);border-radius:14px;padding:4px 12px;backdrop-filter:blur(6px);">
            <span style="width:6px;height:6px;background:#22C55E;border-radius:50%;display:inline-block;box-shadow:0 0 8px #22C55E;animation:pulseDot 1.5s infinite;"></span>
            <span style="font-size:10.5px;color:#86EFAC;font-weight:800;" id="scanner-hud-status">${TL('BioShield Vision Online (60 FPS)', 'ఎడ్జ్ AI విజన్ సిద్ధం', 'Edge AI Vision Online')}</span>
          </div>
          <button type="button" onclick="document.getElementById('real-file-upload-input').click()" style="background:rgba(255,255,255,0.18);border:1px solid rgba(255,255,255,0.25);color:#FFFFFF;border-radius:14px;padding:5px 12px;font-size:11px;font-weight:800;cursor:pointer;display:flex;align-items:center;gap:4px;backdrop-filter:blur(6px);">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
            <span>${TL('Gallery', 'గ్యాలరీ', 'Gallery')}</span>
          </button>
          <input type="file" id="real-file-upload-input" accept="image/*" style="display:none;" onchange="handleRealImageUpload(event)">
        </div>

        <!-- Center Viewfinder HUD Frame with Realistic Sample Backdrop -->
        <div class="viewfinder-frame" id="vf-frame-container" onclick="handleViewfinderClick()" style="margin:8px 0;position:relative;overflow:hidden;background:#090D16;border-radius:18px;border:1px solid rgba(255,255,255,0.15);">
          <!-- High-definition simulated field crop leaf -->
          <img id="vf-default-backdrop" src="https://images.unsplash.com/photo-1598880940371-c756e015fea1?auto=format&fit=crop&w=800&q=80" alt="Plant Leaf Target" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0.9;filter:brightness(0.95);">
          <video id="vf-live-video" autoplay playsinline muted style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;border-radius:18px;z-index:2;display:none;"></video>
          <img id="vf-preview-img" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;border-radius:18px;z-index:3;display:none;" alt="Scan Preview">
          <canvas id="vf-capture-canvas" style="display:none;"></canvas>
          <div class="vf-corner vf-tl"></div>
          <div class="vf-corner vf-tr"></div>
          <div class="vf-corner vf-bl"></div>
          <div class="vf-corner vf-br"></div>
          <div class="vf-laser-line"></div>
          
          <!-- Dynamic Target Reticle Indicator -->
          <div class="vf-center-target" id="scan-target-text" style="position:absolute;bottom:12px;background:rgba(15,23,42,0.85);color:#86EFAC;padding:5px 12px;border-radius:12px;font-size:11px;font-weight:800;backdrop-filter:blur(6px);border:1px solid rgba(134,239,172,0.4);z-index:12;display:flex;align-items:center;gap:5px;">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#86EFAC" stroke-width="2.5" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="22" y1="12" x2="18" y2="12"/><line x1="6" y1="12" x2="2" y2="12"/><line x1="12" y1="6" x2="12" y2="2"/><line x1="12" y1="22" x2="12" y2="18"/></svg>
            <span>${targetHint}</span>
          </div>
        </div>

        <!-- Bottom Guidance Bar -->
        <div style="z-index:10;display:flex;align-items:center;justify-content:center;gap:6px;font-size:11px;color:#FEF08A;font-weight:700;text-shadow:0 1px 3px rgba(0,0,0,0.8);">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="#FEF08A"><path d="M12 2l2.4 7.4H22l-6.2 4.5 2.4 7.4-6.2-4.5-6.2 4.5 2.4-7.4L2 9.4h7.6z"/></svg>
          <span id="scan-guidance-text">${lightHint}</span>
        </div>
      </div>

      <!-- 3-Step Guidance Cards -->
      <div style="padding:0 18px;">
        <div style="background:#FFFFFF;border:1.2px solid #E2ECE2;border-radius:16px;padding:12px 14px;box-shadow:0 2px 8px rgba(0,0,0,0.03);display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;text-align:center;">
          <div style="border-right:1px solid #F1F5F9;padding-right:4px;">
            <div style="display:flex;align-items:center;justify-content:center;margin-bottom:4px;color:#2563EB;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21.3 8.7l-6-6a2 2 0 0 0-2.8 0L3 12.2a2 2 0 0 0 0 2.8l6 6a2 2 0 0 0 2.8 0l9.5-9.5a2 2 0 0 0 0-2.8z"/><path d="M7.5 10.5l2 2M10.5 7.5l2 2M13.5 4.5l2 2"/></svg>
            </div>
            <div style="font-size:11.5px;font-weight:900;color:#0F172A;">15–25 cm</div>
            <div style="font-size:9.5px;color:#64748B;font-weight:700;">${TL('Distance', 'దూరం ఉంచండి', 'Distance')}</div>
          </div>
          <div style="border-right:1px solid #F1F5F9;padding-right:4px;">
            <div style="display:flex;align-items:center;justify-content:center;margin-bottom:4px;color:#EA580C;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>
            </div>
            <div style="font-size:11.5px;font-weight:900;color:#0F172A;">${TL('Bright Light', 'సహజ వెలుగు', 'Bright Light')}</div>
            <div style="font-size:9.5px;color:#64748B;font-weight:700;">${TL('No Shadows', 'నీడలు లేకుండా', 'No Shadows')}</div>
          </div>
          <div>
            <div style="display:flex;align-items:center;justify-content:center;margin-bottom:4px;color:#16A34A;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2" fill="currentColor"/></svg>
            </div>
            <div style="font-size:11.5px;font-weight:900;color:#0F172A;">${TL('Clear Focus', 'స్పష్టమైన ఫోకస్', 'Clear Focus')}</div>
            <div style="font-size:9.5px;color:#64748B;font-weight:700;">${TL('On Target Spot', 'మచ్చలపై లక్ష్యం', 'On Target Spot')}</div>
          </div>
        </div>
      </div>

      <!-- Primary Action CTA Button & Camera Shutter Bar -->
      <div style="padding:14px 18px 6px;display:flex;flex-direction:column;align-items:center;gap:12px;">
        
        <!-- Large Glossy AI Camera Shutter Button -->
        <div onclick="startScannerDiagnostic()" style="width:72px;height:72px;border-radius:50%;background:linear-gradient(135deg, #15803D 0%, #16A34A 50%, #22C55E 100%);padding:4px;cursor:pointer;box-shadow:0 6px 24px rgba(22,163,74,0.45);display:flex;align-items:center;justify-content:center;transition:transform 0.15s ease;" onmousedown="this.style.transform='scale(0.92)'" onmouseup="this.style.transform='scale(1)'">
          <div style="width:100%;height:100%;border-radius:50%;border:2.5px solid #FFFFFF;display:flex;align-items:center;justify-content:center;">
            <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round"><circle cx="12" cy="12" r="3.5" fill="#FFFFFF"/><path d="M4 8V6a2 2 0 0 1 2-2h2M16 4h2a2 2 0 0 1 2 2v2M20 16v2a2 2 0 0 1-2 2h-2M8 20H6a2 2 0 0 1-2-2v-2"/></svg>
          </div>
        </div>

        <!-- Full-Width AI Scan Button -->
        <button id="run-scan-btn" onclick="startScannerDiagnostic()" class="action-btn-green" style="width:100% !important;padding:14px 0;font-size:14.5px;font-weight:900;background:linear-gradient(135deg, #15803D 0%, #16A34A 100%);color:#FFFFFF;border:none;box-shadow:0 4px 18px rgba(22,163,74,0.35);letter-spacing:0.02em;border-radius:16px;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;box-sizing:border-box;">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>
          <span>${actionBtn}</span>
        </button>
      </div>

      <!-- Live Diagnosis Output Result Container -->
      <div id="scan-diag-box" style="display:none;padding:10px 18px 90px;animation:fadeInUp 0.3s ease;">
        <div id="scan-result-content"></div>
      </div>
    </div>
"""

content = scanner_pattern.sub(new_scanner + r"\n    \2", content)

# ══════════════════════════════════════════════════════════════════════════
# 3. COMMUNITY CREATE POST MODAL UPGRADE
# ══════════════════════════════════════════════════════════════════════════
comm_modal_pattern = re.compile(
    r'(<!-- ═════════════════ KISAN COMMUNITY AUTHENTIC INSTAGRAM CREATE POST MODAL ═════════════════ -->.*?)(<!-- ═════════════════ SPRAYING SAFETY & WEATHER WINDOW MODAL ═════════════════ -->)',
    re.DOTALL
)

new_comm_modal = """<!-- ═════════════════ KISAN COMMUNITY AUTHENTIC INSTAGRAM CREATE POST MODAL ═════════════════ -->
    <div id="community-ask-modal" class="custom-modal-overlay" style="display:none;" onclick="closeAskQuestionModal(event)">
      <div class="custom-modal-sheet" onclick="event.stopPropagation()" style="max-height:88vh;overflow-y:auto;padding:18px 18px 32px;background:#FFFFFF;border-top-left-radius:28px;border-top-right-radius:28px;box-shadow:0 -10px 40px rgba(0,0,0,0.18);">
        
        <!-- 1. Header Bar -->
        <div style="display:flex;justify-content:space-between;align-items:center;padding-bottom:12px;border-bottom:1px solid #F1F5F9;flex-shrink:0;">
          <button onclick="closeAskQuestionModal(null)" style="background:none;border:none;font-size:14px;font-weight:700;color:#64748B;cursor:pointer;padding:4px 0;">
            ✕ Cancel
          </button>
          <div style="font-size:16px;font-weight:900;color:#0F172A;letter-spacing:-0.3px;" id="ca-title">New Post</div>
          <button onclick="submitNewCommunityPost()" style="background:#16A34A;color:#FFFFFF;border:none;border-radius:20px;padding:7px 16px;font-size:13px;font-weight:900;cursor:pointer;box-shadow:0 3px 10px rgba(22,163,74,0.3);display:flex;align-items:center;gap:6px;">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
            <span>Share</span>
          </button>
        </div>

        <!-- 2. Author Profile Row -->
        <div style="display:flex;align-items:center;gap:12px;margin:14px 0 10px;">
          <div style="position:relative;width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,#DCFCE7,#BBF7D0);border:2px solid #16A34A;display:flex;align-items:center;justify-content:center;color:#15803D;flex-shrink:0;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            <div style="position:absolute;bottom:-2px;right:-2px;width:16px;height:16px;border-radius:50%;background:#2563EB;border:1.5px solid #FFFFFF;display:flex;align-items:center;justify-content:center;color:#FFF;font-size:9px;font-weight:900;">✓</div>
          </div>
          <div style="flex:1;min-width:0;">
            <div style="font-size:14px;font-weight:900;color:#0F172A;display:flex;align-items:center;gap:4px;">
              <span id="comm-new-post-author-name">B. Jaswanth Reddy</span>
              <span style="color:#2563EB;font-size:13px;">✓</span>
            </div>
            <div style="display:flex;align-items:center;gap:6px;margin-top:2px;flex-wrap:wrap;">
              <span style="font-size:11px;color:#15803D;font-weight:800;background:#DCFCE7;padding:2px 8px;border-radius:10px;border:1px solid #86EFAC;display:inline-flex;align-items:center;gap:4px;">
                <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                <span>Himayath Nagar Farm</span>
              </span>
              <span style="font-size:11px;color:#64748B;font-weight:700;background:#F1F5F9;padding:2px 8px;border-radius:10px;display:inline-flex;align-items:center;gap:4px;">
                <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
                <span>Public · Kisan Network</span>
              </span>
            </div>
          </div>
        </div>

        <!-- 3. Horizontal Crop Selector Carousel Pills -->
        <div style="margin-bottom:12px;">
          <div style="font-size:11px;font-weight:800;color:#64748B;margin-bottom:6px;text-transform:uppercase;letter-spacing:0.3px;">Tag Crop / Commodity Topic:</div>
          <div id="new-post-crop-pills" style="display:flex;gap:6px;overflow-x:auto;padding-bottom:4px;-webkit-overflow-scrolling:touch;">
            <div onclick="selectCommunityPostCrop('cotton', this)" class="comm-crop-pill active" style="background:#F0FDF4;border:1.5px solid #16A34A;color:#15803D;padding:6px 12px;border-radius:20px;font-size:12px;font-weight:800;cursor:pointer;white-space:nowrap;display:flex;align-items:center;gap:4px;">🌱 Cotton</div>
            <div onclick="selectCommunityPostCrop('chilli', this)" class="comm-crop-pill" style="background:#F8FAFC;border:1.5px solid #E2E8F0;color:#475569;padding:6px 12px;border-radius:20px;font-size:12px;font-weight:800;cursor:pointer;white-space:nowrap;display:flex;align-items:center;gap:4px;">🌶️ Chilli</div>
            <div onclick="selectCommunityPostCrop('paddy', this)" class="comm-crop-pill" style="background:#F8FAFC;border:1.5px solid #E2E8F0;color:#475569;padding:6px 12px;border-radius:20px;font-size:12px;font-weight:800;cursor:pointer;white-space:nowrap;display:flex;align-items:center;gap:4px;">🌾 Paddy</div>
            <div onclick="selectCommunityPostCrop('tomato', this)" class="comm-crop-pill" style="background:#F8FAFC;border:1.5px solid #E2E8F0;color:#475569;padding:6px 12px;border-radius:20px;font-size:12px;font-weight:800;cursor:pointer;white-space:nowrap;display:flex;align-items:center;gap:4px;">🍅 Tomato</div>
            <div onclick="selectCommunityPostCrop('maize', this)" class="comm-crop-pill" style="background:#F8FAFC;border:1.5px solid #E2E8F0;color:#475569;padding:6px 12px;border-radius:20px;font-size:12px;font-weight:800;cursor:pointer;white-space:nowrap;display:flex;align-items:center;gap:4px;">🌽 Maize</div>
            <div onclick="selectCommunityPostCrop('groundnut', this)" class="comm-crop-pill" style="background:#F8FAFC;border:1.5px solid #E2E8F0;color:#475569;padding:6px 12px;border-radius:20px;font-size:12px;font-weight:800;cursor:pointer;white-space:nowrap;display:flex;align-items:center;gap:4px;">🥜 Groundnut</div>
            <div onclick="selectCommunityPostCrop('turmeric', this)" class="comm-crop-pill" style="background:#F8FAFC;border:1.5px solid #E2E8F0;color:#475569;padding:6px 12px;border-radius:20px;font-size:12px;font-weight:800;cursor:pointer;white-space:nowrap;display:flex;align-items:center;gap:4px;">🌿 Turmeric</div>
            <div onclick="selectCommunityPostCrop('biorx', this)" class="comm-crop-pill" style="background:#F8FAFC;border:1.5px solid #E2E8F0;color:#475569;padding:6px 12px;border-radius:20px;font-size:12px;font-weight:800;cursor:pointer;white-space:nowrap;display:flex;align-items:center;gap:4px;">🧪 BioRx Organic</div>
            <div onclick="selectCommunityPostCrop('equipment', this)" class="comm-crop-pill" style="background:#F8FAFC;border:1.5px solid #E2E8F0;color:#475569;padding:6px 12px;border-radius:20px;font-size:12px;font-weight:800;cursor:pointer;white-space:nowrap;display:flex;align-items:center;gap:4px;">🚜 Machinery</div>
          </div>
          <input type="hidden" id="new-post-crop" value="cotton" />
        </div>

        <!-- 4. Clean Caption Textarea -->
        <div style="margin-bottom:12px;">
          <textarea id="new-post-desc" rows="4" placeholder="What's happening on your crop field? Describe symptoms, pest attacks, soil issues, or ask for mandi advice..." style="width:100%;padding:14px;border:1.5px solid #E2E8F0;border-radius:18px;font-size:13.5px;font-weight:500;color:#0F172A;background:#FFFFFF;outline:none;box-sizing:border-box;resize:none;line-height:1.5;box-shadow:inset 0 1px 3px rgba(0,0,0,0.02);"></textarea>
          <input type="hidden" id="new-post-title" value="" />
        </div>

        <!-- 5. Media Attachment Preview Area -->
        <div id="attached-media-chips" style="margin-bottom:12px;display:flex;flex-wrap:wrap;gap:8px;"></div>

        <!-- 6. Rich Attachment Tray -->
        <div style="background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:18px;padding:10px 14px;margin-bottom:14px;display:flex;align-items:center;justify-content:space-between;">
          <span style="font-size:11.5px;font-weight:800;color:#475569;">Attach from Field:</span>
          <div style="display:flex;align-items:center;gap:8px;">
            <button type="button" onclick="attachMediaToNewPost('photo')" title="Attach Photo" style="background:#FFFFFF;border:1px solid #CBD5E1;width:40px;height:40px;border-radius:12px;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 6px rgba(0,0,0,0.04);color:#2563EB;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>
            </button>
            <button type="button" onclick="attachMediaToNewPost('video')" title="Attach Video" style="background:#FFFFFF;border:1px solid #CBD5E1;width:40px;height:40px;border-radius:12px;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 6px rgba(0,0,0,0.04);color:#7C3AED;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg>
            </button>
            <button type="button" onclick="attachMediaToNewPost('voice')" title="Record Voice Note" style="background:#FFFFFF;border:1px solid #CBD5E1;width:40px;height:40px;border-radius:12px;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 6px rgba(0,0,0,0.04);color:#16A34A;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg>
            </button>
            <button type="button" onclick="attachMediaToNewPost('location')" title="Pin Location" style="background:#FFFFFF;border:1px solid #CBD5E1;width:40px;height:40px;border-radius:12px;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 6px rgba(0,0,0,0.04);color:#DC2626;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
            </button>
          </div>
        </div>

        <!-- 7. Bottom Share Button -->
        <button onclick="submitNewCommunityPost()" style="width:100%;background:linear-gradient(135deg,#16A34A,#15803D);color:#FFFFFF;border:none;border-radius:16px;padding:14px 0;font-size:14.5px;font-weight:900;cursor:pointer;box-shadow:0 4px 16px rgba(22,163,74,0.32);display:flex;align-items:center;justify-content:center;gap:8px;">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
          <span>Share Post to Kisan Community</span>
        </button>

      </div>
    </div>
"""

content = comm_modal_pattern.sub(new_comm_modal + r"\n    \2", content)

# ══════════════════════════════════════════════════════════════════════════
# 4. SETTINGS MODAL UPGRADE
# ══════════════════════════════════════════════════════════════════════════
settings_pattern = re.compile(
    r'(function openSettingsModal\(\)\s*\{.*?)(// ── USER LOGOUT CONFIRMATION & SESSION CLEARING ──)',
    re.DOTALL
)

new_settings = """function openSettingsModal() {
  const modalId = 'app-settings-modal';
  let modal = document.getElementById(modalId);
  if (modal) modal.remove();

  // Dynamic user stats & real storage computation
  const storageBytes = JSON.stringify(localStorage).length;
  const storageKb = (storageBytes / 1024).toFixed(1);
  let completedTrips = 0;
  try {
    completedTrips = JSON.parse(localStorage.getItem('gh_driver_completed_trips') || '[]').length;
  } catch(e) {}
  const curFarmerId = localStorage.getItem('nukrop_farmer_id') || 'TS-WGL-8941';
  const curLangName = currentLang === 'te' ? 'తెలుగు (Telugu)' : (currentLang === 'hi' ? 'हिन्दी (Hindi)' : 'English');

  modal = document.createElement('div');
  modal.id = modalId;
  modal.style.cssText = 'position:fixed;inset:0;background:rgba(15,23,42,0.75);backdrop-filter:blur(6px);z-index:999999;display:flex;align-items:flex-end;justify-content:center;animation:fadeIn 0.2s;';
  modal.innerHTML = `
    <div style="background:#FFFFFF;width:100%;max-width:440px;max-height:86vh;border-radius:28px 28px 0 0;padding:24px 20px 32px;box-shadow:0 -10px 40px rgba(0,0,0,0.25);animation:slideUp 0.25s ease;display:flex;flex-direction:column;box-sizing:border-box;">
      <div style="width:36px;height:4px;background:#E2E8F0;border-radius:10px;margin:0 auto 16px;"></div>

      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;flex-shrink:0;">
        <div style="display:flex;align-items:center;gap:12px;">
          <div style="width:44px;height:44px;border-radius:14px;background:#F0FDF4;border:1px solid #BBF7D0;display:flex;align-items:center;justify-content:center;color:#15803D;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
          </div>
          <div>
            <div style="font-size:17.5px;font-weight:900;color:#0F172A;">Settings & Preferences</div>
            <div style="font-size:11px;color:#64748B;font-weight:700;">Farmer ID: ${curFarmerId} · v2.4 Pro</div>
          </div>
        </div>
        <button onclick="document.getElementById('${modalId}').remove();" style="background:#F1F5F9;border:none;width:34px;height:34px;border-radius:50%;color:#64748B;font-size:16px;cursor:pointer;display:flex;align-items:center;justify-content:center;">✕</button>
      </div>

      <div style="flex:1;overflow-y:auto;display:flex;flex-direction:column;gap:10px;padding-right:2px;">
        <div onclick="openLanguageSelectorModal();document.getElementById('${modalId}').remove();" style="background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:16px;padding:12px 14px;display:flex;align-items:center;justify-content:space-between;cursor:pointer;">
          <div style="display:flex;align-items:center;gap:12px;">
            <div style="width:38px;height:38px;border-radius:12px;background:#EFF6FF;display:flex;align-items:center;justify-content:center;color:#2563EB;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
            </div>
            <div>
              <div style="font-size:13.5px;font-weight:900;color:#0F172A;">App Language</div>
              <div style="font-size:11px;color:#16A34A;font-weight:700;">Active: ${curLangName}</div>
            </div>
          </div>
          <span style="color:#94A3B8;font-size:16px;">›</span>
        </div>

        <div onclick="openPreviousRidesModal();document.getElementById('${modalId}').remove();" style="background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:16px;padding:12px 14px;display:flex;align-items:center;justify-content:space-between;cursor:pointer;">
          <div style="display:flex;align-items:center;gap:12px;">
            <div style="width:38px;height:38px;border-radius:12px;background:#FFF7ED;display:flex;align-items:center;justify-content:center;color:#EA580C;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
            </div>
            <div>
              <div style="font-size:13.5px;font-weight:900;color:#0F172A;">Haul Ride History & Invoices</div>
              <div style="font-size:11px;color:#64748B;">${completedTrips} Trips · Real APMC Gate Passes & E-Way Bills</div>
            </div>
          </div>
          <span style="color:#94A3B8;font-size:16px;">›</span>
        </div>

        <div onclick="openPrivacyPolicyModal();document.getElementById('${modalId}').remove();" style="background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:16px;padding:12px 14px;display:flex;align-items:center;justify-content:space-between;cursor:pointer;">
          <div style="display:flex;align-items:center;gap:12px;">
            <div style="width:38px;height:38px;border-radius:12px;background:#F0FDF4;display:flex;align-items:center;justify-content:center;color:#16A34A;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            </div>
            <div>
              <div style="font-size:13.5px;font-weight:900;color:#0F172A;">Privacy Policy & Data Security</div>
              <div style="font-size:11px;color:#64748B;">DPDP Act 2023 · AgriStack Encrypted</div>
            </div>
          </div>
          <span style="color:#94A3B8;font-size:16px;">›</span>
        </div>

        <div onclick="autoDetectMandiLocation();document.getElementById('${modalId}').remove();" style="background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:16px;padding:12px 14px;display:flex;align-items:center;justify-content:space-between;cursor:pointer;">
          <div style="display:flex;align-items:center;gap:12px;">
            <div style="width:38px;height:38px;border-radius:12px;background:#FEF2F2;display:flex;align-items:center;justify-content:center;color:#DC2626;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
            </div>
            <div>
              <div style="font-size:13.5px;font-weight:900;color:#0F172A;">GPS Geofence & Location</div>
              <div style="font-size:11px;color:#64748B;">High-Accuracy Live GPS Satellites</div>
            </div>
          </div>
          <span style="color:#16A34A;font-weight:800;font-size:11px;">RE-CALIBRATE</span>
        </div>

        <div onclick="showLuxuryToast('Local Storage synced: ' + '${storageKb}' + ' KB cached successfully!','success');document.getElementById('${modalId}').remove();" style="background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:16px;padding:12px 14px;display:flex;align-items:center;justify-content:space-between;cursor:pointer;">
          <div style="display:flex;align-items:center;gap:12px;">
            <div style="width:38px;height:38px;border-radius:12px;background:#EDE9FE;display:flex;align-items:center;justify-content:center;color:#7C3AED;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>
            </div>
            <div>
              <div style="font-size:13.5px;font-weight:900;color:#0F172A;">Sync Offline Database</div>
              <div style="font-size:11px;color:#64748B;">${storageKb} KB real local memory cached</div>
            </div>
          </div>
          <span style="color:#2563EB;font-weight:800;font-size:11px;">SYNC NOW</span>
        </div>

        <div onclick="executeUserLogout();document.getElementById('${modalId}').remove();" style="background:#FEF2F2;border:1.5px solid #FECACA;border-radius:16px;padding:12px 14px;display:flex;align-items:center;justify-content:space-between;cursor:pointer;">
          <div style="display:flex;align-items:center;gap:12px;">
            <div style="width:38px;height:38px;border-radius:12px;background:#FEE2E2;display:flex;align-items:center;justify-content:center;color:#DC2626;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
            </div>
            <div>
              <div style="font-size:13.5px;font-weight:900;color:#DC2626;">Log Out Account</div>
              <div style="font-size:11px;color:#EF4444;">Sign out of NuKropAI farmer session</div>
            </div>
          </div>
          <span style="color:#DC2626;font-weight:800;font-size:11px;">LOG OUT</span>
        </div>
      </div>

      <button onclick="document.getElementById('${modalId}').remove();" style="width:100%;height:46px;border-radius:14px;background:#0F172A;color:#FFFFFF;font-size:14px;font-weight:900;border:none;cursor:pointer;margin-top:14px;flex-shrink:0;">
        Done
      </button>
    </div>
  `;
  document.body.appendChild(modal);
}
"""

content = settings_pattern.sub(new_settings + r"\n\n\2", content)

# ══════════════════════════════════════════════════════════════════════════
# 5. APP_NOTIFICATIONS & NOTIFICATION FEED UPGRADE
# ══════════════════════════════════════════════════════════════════════════
notif_pattern = re.compile(
    r'(let APP_NOTIFICATIONS = \[.*?\];)',
    re.DOTALL
)

new_notif_array = """let APP_NOTIFICATIONS = [
  // ── 🧑‍🌾 STRICT FARMER-ONLY ALERTS (NO DRIVER CONTENT) ──
  {
    id: 'notif-f-1',
    forRole: 'farmer',
    category: 'mandi',
    iconSvg: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>',
    iconBg: '#DCFCE7',
    iconColor: '#16A34A',
    title: {
      en: 'Cotton Price Hit ₹7,450/Qtl (+₹140 Today)',
      te: 'పత్తి క్వింటాల్ ధర ₹7,450 కి చేరింది (+₹140 ఈరోజు)',
      hi: 'कपास भाव ₹7,450/क्विंटल पहुंचा (+₹140 आज)'
    },
    msg: {
      en: 'Gudimalkapur & Bowenpally APMC recorded heavy buying volume. Recommended: Book Mandi Truck for best farm-gate realization.',
      te: 'గుడిమల్కాపూర్ & బోయిన్‌పల్లి యార్డులలో అధిక డిమాండ్ నమోదైంది. మంచి ధరకు గ్రామ్‌హాల్ ట్రక్ ద్వారా రవాణా చేయండి.',
      hi: 'गुडीमलकापुर व बोवेनपल्ली मंडी में भारी मांग। अच्छे भाव के लिए ग्रामहॉल ट्रक से उपज भेजें।'
    },
    time: { en: '5m ago', te: '5 నిమిషాల క్రితం', hi: '5 मिनट पहले' },
    read: false,
    screenKey: 'market',
    actionBtn: { en: 'View Mandi Rates', te: 'లైవ్ ధరలు చూడండి', hi: 'ताजा भाव देखें' }
  },
  {
    id: 'notif-f-2',
    forRole: 'farmer',
    category: 'pest',
    iconSvg: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
    iconBg: '#FEE2E2',
    iconColor: '#DC2626',
    title: {
      en: 'Regional Pink Bollworm Radar Warning',
      te: 'గులాబీ రంగు పురుగు వ్యాప్తి హెచ్చరిక',
      hi: 'गुलाबी सुंडी प्रकोप क्षेत्रीय चेतावनी'
    },
    msg: {
      en: 'Scans in regional belt detected pest emergence. Spray 5ml/L Neem Oil (10,000 ppm) during evening zero-drift window.',
      te: 'ప్రాంతీయ పరిధిలో తెగులు స్కాన్లు నమోదయ్యాయి. సాయంత్రం వేళ వేప నూనె (5ml/L) పిచికారీ చేయండి.',
      hi: 'क्षेत्रीय खेतों में सुंडी संक्रमण के लक्षण मिले हैं। शाम को 5ml/L नीम तेल का छिड़काव करें।'
    },
    time: { en: '20m ago', te: '20 నిమిషాల క్రితం', hi: '20 मिनट पहले' },
    read: false,
    screenKey: 'bioshield',
    actionBtn: { en: 'Open BioShield Radar', te: 'బయోషీల్డ్ చూడండి', hi: 'बायोशील्ड देखें' }
  },
  {
    id: 'notif-f-3',
    forRole: 'farmer',
    category: 'weather',
    iconSvg: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M20 16.58A5 5 0 0 0 18 7h-1.26A8 8 0 1 0 4 15.25"/><line x1="8" y1="19" x2="8" y2="23"/><line x1="12" y1="17" x2="12" y2="21"/><line x1="16" y1="19" x2="16" y2="23"/></svg>',
    iconBg: '#E0F2FE',
    iconColor: '#0284C7',
    title: {
      en: 'Optimal Evening Spraying Window Active',
      te: 'పిచికారీకి అనుకూల వాతావరణ సమయం',
      hi: 'शाम का अनुकूल स्प्रे समय शुरू'
    },
    msg: {
      en: 'Local Farm Sensors: Wind speed 6 km/h, 27°C. Ideal zero-drift atmospheric conditions.',
      te: 'స్థానిక వాతావరణ సెన్సార్లు: గాలి వేగం 6 km/h, 27°C. మందుల పిచికారీకి అత్యంత అనుకూలం.',
      hi: 'स्थानीय मौसम सेंसर: हवा की गति 6 किमी/घंटा, 27°C। कीटनाशक छिड़काव हेतु उत्तम परिस्थिति।'
    },
    time: { en: '1h ago', te: '1 గంట క్రితం', hi: '1 घंटा पहले' },
    read: true,
    screenKey: 'home'
  },
  {
    id: 'notif-f-4',
    forRole: 'farmer',
    category: 'scheme',
    iconSvg: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="22" x2="21" y2="22"/><line x1="6" y1="18" x2="6" y2="11"/><line x1="10" y1="18" x2="10" y2="11"/><line x1="14" y1="18" x2="14" y2="11"/><line x1="18" y1="18" x2="18" y2="11"/><polygon points="12 2 20 7 4 7"/></svg>',
    iconBg: '#FEF3C7',
    iconColor: '#D97706',
    title: {
      en: 'PM-KISAN ₹2,000 DBT Benefit Active',
      te: 'PM-కిసాన్ ₹2,000 నగదు బదిలీ జమ చేయబడింది',
      hi: 'पीएम-किसान ₹2,000 डीबीटी राशि जमा'
    },
    msg: {
      en: 'Direct Benefit Transfer successfully credited to your Aadhaar-linked Bank Account for verified land parcel.',
      te: 'ధృవీకరించబడిన భూమికి సంబంధించిన నగదు మీ ఆధార్ లింక్ అయిన బ్యాంక్ ఖాతాలో జమైంది.',
      hi: 'सत्यापित भूमि हेतु सरकारी डीबीटी राशि आपके आधार से जुड़े बैंक खाते में जमा हो गई है।'
    },
    time: { en: '3h ago', te: '3 గంటల క్రితం', hi: '3 घंटे पहले' },
    read: true,
    screenKey: 'agristack'
  },

  // ── 🚚 STRICT DRIVER-ONLY LOGISTICS ALERTS ──
  {
    id: 'notif-drv-1',
    forRole: 'driver',
    category: 'haul',
    iconSvg: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>',
    iconBg: '#DCFCE7',
    iconColor: '#16A34A',
    title: {
      en: 'New Haul Request: Farm to APMC Mandi',
      te: 'కొత్త రవాణా ఆర్డర్: పొలం నుండి APMC మండికి',
      hi: 'नई ढुलाई बुकिंग: खेत से मंडी यार्ड'
    },
    msg: {
      en: '40 Sacks Cotton (20 Qtl). Agreed Freight Fare: ₹520. Farmer ready at farm gate.',
      te: '40 బస్తాల పత్తి (20 క్వి). నిర్ణయించిన రవాణా ఛార్జ్: ₹520. రైతు పొలం గేట్ వద్ద సిద్ధంగా ఉన్నారు.',
      hi: '40 बोरी कपास (20 क्विंटल)। तय भाड़ा: ₹520। किसान खेत के गेट पर तैयार है।'
    },
    time: { en: 'Just now', te: 'ఇప్పుడే', hi: 'अभी' },
    read: false,
    screenKey: 'driver_dashboard',
    actionBtn: { en: 'View in Cockpit', te: 'కాక్‌పిట్‌లో చూడండి', hi: 'कॉकपिट देखें' }
  },
  {
    id: 'notif-drv-2',
    forRole: 'driver',
    category: 'settlement',
    iconSvg: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/><line x1="12" y1="6" x2="12" y2="8"/><line x1="12" y1="16" x2="12" y2="18"/></svg>',
    iconBg: '#FEF3C7',
    iconColor: '#D97706',
    title: {
      en: '₹680 UPI Freight Settlement Credited',
      te: '₹680 UPI రవాణా ఛార్జ్ మీ ఖాతాలో జమైంది',
      hi: '₹680 भाड़ा सीधे बैंक खाते में जमा'
    },
    msg: {
      en: 'Direct 0% commission settlement received for completed haul trip.',
      te: 'పూర్తయిన రవాణా ఆర్డర్‌కు 0% కమిషన్‌తో నేరుగా మీ బ్యాంక్ ఖాతాలో నగదు జమ అయింది.',
      hi: 'पूरी हुई ढुलाई ट्रिप का 0% कमीशन के साथ सीधे खाते में भुगतान प्राप्त हुआ।'
    },
    time: { en: '2h ago', te: '2 గంటల క్రితం', hi: '2 घंटे पहले' },
    read: true,
    screenKey: 'driver_dashboard'
  }
];"""

content = notif_pattern.sub(new_notif_array, content)

# Make sure renderPriceAlertModalDom renders n.iconSvg || n.icon
content = re.sub(
    r'<div style="width:36px;height:36px;border-radius:10px;background:\$\{n\.iconBg\};color:\$\{n\.iconColor\};display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;">\s*\$\{n\.icon\}\s*</div>',
    '<div style="width:36px;height:36px;border-radius:10px;background:${n.iconBg};color:${n.iconColor};display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;">\n              ${n.iconSvg || n.icon}\n            </div>',
    content
)

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("SUCCESS: All UI Icons, Bento, Scanner, New Post, Settings, and Notifications upgraded!")
