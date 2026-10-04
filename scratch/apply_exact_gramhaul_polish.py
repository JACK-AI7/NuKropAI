#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
apply_exact_gramhaul_polish.py
Applies high-end vector icons and neat layout alignment across GramHaul Screen 1 and Screen 2 in both files.
"""

import sys, re

# High-end vehicle SVGs
ACE_GOLD_SVG = '''<svg viewBox="0 0 84 52" fill="none" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;">
  <defs>
    <linearGradient id="aceCabin" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="70%" stop-color="#F8FAFC"/>
      <stop offset="100%" stop-color="#CBD5E1"/>
    </linearGradient>
    <linearGradient id="aceBed" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#16A34A"/>
      <stop offset="100%" stop-color="#14532D"/>
    </linearGradient>
    <linearGradient id="aceGlass" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#BAE6FD"/>
      <stop offset="60%" stop-color="#38BDF8"/>
      <stop offset="100%" stop-color="#0284C7"/>
    </linearGradient>
  </defs>
  <!-- Sacks in Cargo Bed -->
  <g fill="#D97706" stroke="#92400E" stroke-width="0.8">
    <ellipse cx="14" cy="18" rx="8" ry="4.5"/>
    <ellipse cx="26" cy="17" rx="8" ry="4.5"/>
    <ellipse cx="38" cy="18" rx="8" ry="4.5"/>
    <ellipse cx="20" cy="13" rx="7" ry="4" fill="#F59E0B"/>
    <ellipse cx="32" cy="13" rx="7" ry="4" fill="#F59E0B"/>
  </g>
  <!-- Cargo Bed -->
  <rect x="4" y="20" width="46" height="18" rx="2" fill="url(#aceBed)" stroke="#0F172A" stroke-width="1.8"/>
  <line x1="4" y1="28" x2="50" y2="28" stroke="#15803D" stroke-width="1.2"/>
  <line x1="20" y1="20" x2="20" y2="38" stroke="#15803D" stroke-width="1.2"/>
  <line x1="35" y1="20" x2="35" y2="38" stroke="#15803D" stroke-width="1.2"/>
  <!-- Cabin Body -->
  <path d="M50 20 H68 C74 20 78 24 79 30 L80 38 H50 V20 Z" fill="url(#aceCabin)" stroke="#0F172A" stroke-width="1.8"/>
  <!-- Blue Commercial Decal Stripe -->
  <path d="M50 32 H78 L79 35 H50 V32 Z" fill="#0284C7"/>
  <!-- Windshield -->
  <path d="M54 22 H67 C71 22 74 25 75 29 H54 V22 Z" fill="url(#aceGlass)" stroke="#0F172A" stroke-width="1.2"/>
  <line x1="58" y1="23" x2="63" y2="28" stroke="#FFFFFF" stroke-width="1.5" stroke-linecap="round" opacity="0.85"/>
  <!-- Headlight & Grille -->
  <circle cx="76" cy="34" r="2.5" fill="#FEF08A" stroke="#CA8A04" stroke-width="0.8"/>
  <rect x="73" y="32" width="2" height="4" rx="0.5" fill="#F59E0B"/>
  <rect x="62" y="23" width="2" height="4" rx="1" fill="#0F172A"/>
  <rect x="74" y="37" width="7" height="3" rx="1.5" fill="#1E293B"/>
  <!-- Wheels -->
  <circle cx="18" cy="38" r="7" fill="#0F172A"/>
  <circle cx="18" cy="38" r="4.2" fill="#94A3B8"/>
  <circle cx="18" cy="38" r="1.8" fill="#0F172A"/>
  <circle cx="66" cy="38" r="7" fill="#0F172A"/>
  <circle cx="66" cy="38" r="4.2" fill="#94A3B8"/>
  <circle cx="66" cy="38" r="1.8" fill="#0F172A"/>
</svg>'''

BOLERO_MAXI_SVG = '''<svg viewBox="0 0 84 52" fill="none" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;">
  <defs>
    <linearGradient id="bolRed" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#EF4444"/>
      <stop offset="60%" stop-color="#DC2626"/>
      <stop offset="100%" stop-color="#991B1B"/>
    </linearGradient>
    <linearGradient id="bolBed" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="100%" stop-color="#E2E8F0"/>
    </linearGradient>
  </defs>
  <!-- Produce Cargo & Crates -->
  <g fill="#EA580C" stroke="#9A3412" stroke-width="0.8">
    <rect x="10" y="12" width="12" height="8" rx="1.5"/>
    <rect x="24" y="12" width="12" height="8" rx="1.5" fill="#F59E0B"/>
    <rect x="17" y="6" width="12" height="8" rx="1.5" fill="#16A34A" stroke="#14532D"/>
  </g>
  <!-- Tubular Ladder Frame / Roll-Cage -->
  <path d="M6 19 H48 V10 H42" stroke="#64748B" stroke-width="1.8" stroke-linecap="round" fill="none"/>
  <!-- Cargo Bed -->
  <rect x="4" y="18" width="46" height="20" rx="2" fill="url(#bolBed)" stroke="#0F172A" stroke-width="1.8"/>
  <line x1="4" y1="27" x2="50" y2="27" stroke="#CBD5E1" stroke-width="1.5"/>
  <!-- Bolero Cabin -->
  <path d="M50 18 H66 L78 28 V38 H50 V18 Z" fill="url(#bolRed)" stroke="#0F172A" stroke-width="1.8"/>
  <rect x="70" y="28" width="10" height="10" fill="url(#bolRed)" stroke="#0F172A" stroke-width="1.2"/>
  <path d="M54 20 H64 L72 28 H54 V20 Z" fill="#BAE6FD" stroke="#0F172A" stroke-width="1.2"/>
  <rect x="76" y="30" width="3" height="6" fill="#1E293B"/>
  <circle cx="78" cy="29" r="2.2" fill="#FEF08A"/>
  <rect x="75" y="37" width="6" height="3" rx="1" fill="#0F172A"/>
  <circle cx="18" cy="38" r="7.5" fill="#0F172A"/>
  <circle cx="18" cy="38" r="4.5" fill="#E2E8F0"/>
  <circle cx="18" cy="38" r="2" fill="#DC2626"/>
  <circle cx="66" cy="38" r="7.5" fill="#0F172A"/>
  <circle cx="66" cy="38" r="4.5" fill="#E2E8F0"/>
  <circle cx="66" cy="38" r="2" fill="#DC2626"/>
</svg>'''

DOST_PLUS_SVG = '''<svg viewBox="0 0 84 52" fill="none" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;">
  <defs>
    <linearGradient id="dostGreen" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#22C55E"/>
      <stop offset="60%" stop-color="#16A34A"/>
      <stop offset="100%" stop-color="#15803D"/>
    </linearGradient>
  </defs>
  <!-- Full Produce Cover Tarpaulin -->
  <path d="M8 12 Q28 6 48 12 L48 18 H8 Z" fill="#2563EB" stroke="#1E40AF" stroke-width="1.2"/>
  <path d="M12 18 L24 10 M26 18 L38 10" stroke="#93C5FD" stroke-width="1" opacity="0.6"/>
  <!-- Cargo Bed -->
  <rect x="4" y="17" width="46" height="21" rx="2" fill="#F8FAFC" stroke="#0F172A" stroke-width="1.8"/>
  <line x1="4" y1="26" x2="50" y2="26" stroke="#E2E8F0" stroke-width="1.5"/>
  <!-- Dost Aerodynamic Cabin -->
  <path d="M50 17 H66 C72 17 76 20 78 26 L80 38 H50 V17 Z" fill="url(#dostGreen)" stroke="#0F172A" stroke-width="1.8"/>
  <path d="M54 19 H65 C68 19 72 22 74 26 H54 V19 Z" fill="#E0F2FE" stroke="#0F172A" stroke-width="1.2"/>
  <ellipse cx="77" cy="32" rx="2.5" ry="3" fill="#FEF08A" stroke="#CA8A04" stroke-width="0.8"/>
  <rect x="75" y="37" width="6" height="3" rx="1" fill="#1E293B"/>
  <circle cx="18" cy="38" r="7.2" fill="#0F172A"/>
  <circle cx="18" cy="38" r="4.2" fill="#CBD5E1"/>
  <circle cx="18" cy="38" r="1.8" fill="#16A34A"/>
  <circle cx="66" cy="38" r="7.2" fill="#0F172A"/>
  <circle cx="66" cy="38" r="4.2" fill="#CBD5E1"/>
  <circle cx="66" cy="38" r="1.8" fill="#16A34A"/>
</svg>'''

TATA_407_SVG = '''<svg viewBox="0 0 84 52" fill="none" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;">
  <defs>
    <linearGradient id="t407Cab" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FBBF24"/>
      <stop offset="60%" stop-color="#F59E0B"/>
      <stop offset="100%" stop-color="#D97706"/>
    </linearGradient>
    <linearGradient id="t407Bed" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FEF3C7"/>
      <stop offset="100%" stop-color="#FDE68A"/>
    </linearGradient>
  </defs>
  <!-- Towering High-Load Sacks -->
  <g fill="#CA8A04" stroke="#854D0E" stroke-width="0.8">
    <ellipse cx="14" cy="11" rx="8" ry="4.5"/>
    <ellipse cx="28" cy="10" rx="9" ry="4.5"/>
    <ellipse cx="42" cy="11" rx="8" ry="4.5"/>
    <ellipse cx="22" cy="6" rx="8" ry="4" fill="#EAB308"/>
    <ellipse cx="36" cy="6" rx="8" ry="4" fill="#EAB308"/>
  </g>
  <!-- Traditional Timber-Reinforced Cargo Bed -->
  <rect x="4" y="14" width="48" height="24" rx="2" fill="url(#t407Bed)" stroke="#0F172A" stroke-width="1.8"/>
  <line x1="4" y1="22" x2="52" y2="22" stroke="#B45309" stroke-width="1.5"/>
  <line x1="4" y1="30" x2="52" y2="30" stroke="#B45309" stroke-width="1.5"/>
  <!-- Forward-Control 407 Cabin -->
  <path d="M52 14 H68 C74 14 78 18 79 24 L80 38 H52 V14 Z" fill="url(#t407Cab)" stroke="#0F172A" stroke-width="1.8"/>
  <path d="M56 16 H67 C71 16 74 19 75 24 H56 V16 Z" fill="#BAE6FD" stroke="#0F172A" stroke-width="1.2"/>
  <circle cx="76" cy="32" r="3" fill="#FFFFFF" stroke="#0F172A" stroke-width="1"/>
  <circle cx="76" cy="32" r="1.5" fill="#FEF08A"/>
  <rect x="74" y="37" width="8" height="4" rx="1.5" fill="#1E293B"/>
  <circle cx="18" cy="38" r="7.8" fill="#0F172A"/>
  <circle cx="18" cy="38" r="4.6" fill="#D97706"/>
  <circle cx="18" cy="38" r="1.8" fill="#0F172A"/>
  <circle cx="66" cy="38" r="7.8" fill="#0F172A"/>
  <circle cx="66" cy="38" r="4.6" fill="#D97706"/>
  <circle cx="66" cy="38" r="1.8" fill="#0F172A"/>
</svg>'''

EICHER_PRO_SVG = '''<svg viewBox="0 0 84 52" fill="none" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;">
  <defs>
    <linearGradient id="eichBlue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#3B82F6"/>
      <stop offset="50%" stop-color="#2563EB"/>
      <stop offset="100%" stop-color="#1D4ED8"/>
    </linearGradient>
    <linearGradient id="eichBox" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F1F5F9"/>
      <stop offset="100%" stop-color="#CBD5E1"/>
    </linearGradient>
  </defs>
  <!-- 14ft Freight Cargo Box -->
  <rect x="3" y="9" width="50" height="29" rx="2" fill="url(#eichBox)" stroke="#0F172A" stroke-width="1.8"/>
  <rect x="3" y="22" width="50" height="3" fill="#FACC15"/>
  <!-- Roof Wind Deflector & Blue Tilt-Cab -->
  <path d="M53 9 H68 L78 20 V38 H53 V9 Z" fill="url(#eichBlue)" stroke="#0F172A" stroke-width="1.8"/>
  <path d="M56 12 H67 L74 21 H56 V12 Z" fill="#DBEAFE" stroke="#0F172A" stroke-width="1.2"/>
  <rect x="56" y="9" width="13" height="3" fill="#0F172A"/>
  <rect x="74" y="27" width="3.5" height="6" rx="1" fill="#FEF08A" stroke="#CA8A04" stroke-width="0.8"/>
  <rect x="72" y="36" width="9" height="4" rx="1.5" fill="#0F172A"/>
  <!-- 3 Heavy Axle Wheels (Dual Rear Axle) -->
  <circle cx="14" cy="38" r="7.5" fill="#0F172A"/>
  <circle cx="14" cy="38" r="4.2" fill="#94A3B8"/>
  <circle cx="28" cy="38" r="7.5" fill="#0F172A"/>
  <circle cx="28" cy="38" r="4.2" fill="#94A3B8"/>
  <circle cx="68" cy="38" r="7.5" fill="#0F172A"/>
  <circle cx="68" cy="38" r="4.2" fill="#94A3B8"/>
</svg>'''

def patch_file(filepath):
    print(f"Applying exact polish to {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Screen 1 Header Top Bar
    old_s1_header = '''        <!-- Top Bar with Safe Area -->
        <div style="position:absolute;top:max(14px, calc(var(--sat) - 20px));left:12px;right:12px;display:flex;justify-content:space-between;align-items:center;z-index:20;">
          <button onclick="openScreen(authUserRole==='driver'?'driver_dashboard':'home',null);updateBottomDockForRole()" style="background:#FFFFFF;border:none;width:40px;height:40px;border-radius:13px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 14px rgba(0,0,0,0.14);cursor:pointer;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#0F172A" stroke-width="2.5" stroke-linecap="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
          </button>
          <div style="background:rgba(255,255,255,0.95);backdrop-filter:blur(8px);padding:7px 16px;border-radius:999px;box-shadow:0 4px 14px rgba(0,0,0,0.12);display:flex;align-items:center;gap:6px;">
            <span style="font-size:15px;">🚜</span>
            <span style="font-size:13.5px;font-weight:900;color:#16A34A;">${TL('GramHaul Mandi Dispatch', 'గ్రామ్‌హౌల్ మండి రవాణా', 'ग्रामहॉल मंडी परिवहन')}</span>
          </div>
          <div style="display:flex;align-items:center;gap:6px;">
            <button onclick="openPreviousRidesModal()" title="Ride History" style="background:#FFFFFF;border:1px solid #E2E8F0;width:40px;height:40px;border-radius:13px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 14px rgba(0,0,0,0.12);cursor:pointer;font-size:17px;">
              🧾
            </button>
            <button onclick="openGramhaulPickupLocationModal()" title="Edit Pickup" style="background:#16A34A;border:none;width:40px;height:40px;border-radius:13px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 14px rgba(22,163,74,0.35);cursor:pointer;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"><circle cx="12" cy="10" r="3"/><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/></svg>
            </button>
          </div>
        </div>'''

    new_s1_header = '''        <!-- Top Bar with Safe Area -->
        <div style="position:absolute;top:max(14px, calc(var(--sat) - 20px));left:12px;right:12px;display:flex;justify-content:space-between;align-items:center;z-index:20;">
          <button onclick="openScreen(authUserRole==='driver'?'driver_dashboard':'home',null);updateBottomDockForRole()" style="background:#FFFFFF;border:1px solid #E2E8F0;width:40px;height:40px;border-radius:13px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 14px rgba(0,0,0,0.10);cursor:pointer;flex-shrink:0;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#0F172A" stroke-width="2.5" stroke-linecap="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
          </button>
          
          <div style="background:linear-gradient(135deg,#FFFFFF 0%,#F0FDF4 100%);border:1px solid #BBF7D0;padding:7px 16px;border-radius:999px;box-shadow:0 4px 14px rgba(0,0,0,0.08);display:flex;align-items:center;gap:8px;">
            <div style="width:20px;height:20px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <rect x="2" y="7" width="13" height="10" rx="1.5" fill="#16A34A"/>
                <path d="M15 10H18.5L21.5 13.5V17H15V10Z" fill="#15803D"/>
                <circle cx="6" cy="17" r="2.2" fill="#0F172A"/>
                <circle cx="17.5" cy="17" r="2.2" fill="#0F172A"/>
                <path d="M15.5 11H18L20 13.5H15.5V11Z" fill="#BAE6FD"/>
              </svg>
            </div>
            <span style="font-size:13.5px;font-weight:900;color:#15803D;letter-spacing:-0.2px;">${TL('GramHaul Mandi Dispatch', 'గ్రామ్‌హౌల్ మండి రవాణా', 'ग्रामहॉल मंडी परिवहन')}</span>
          </div>

          <div style="display:flex;align-items:center;gap:6px;">
            <button onclick="openPreviousRidesModal()" title="Ride History" style="background:#FFFFFF;border:1px solid #E2E8F0;width:40px;height:40px;border-radius:13px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 14px rgba(0,0,0,0.08);cursor:pointer;flex-shrink:0;">
              <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="#334155" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><line x1="10" y1="9" x2="8" y2="9"/></svg>
            </button>
            <button onclick="openGramhaulPickupLocationModal()" title="Edit Pickup" style="background:linear-gradient(135deg,#16A34A,#15803D);border:none;width:40px;height:40px;border-radius:13px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 14px rgba(22,163,74,0.35);cursor:pointer;flex-shrink:0;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"><circle cx="12" cy="10" r="3"/><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/></svg>
            </button>
          </div>
        </div>'''

    if old_s1_header in text:
        text = text.replace(old_s1_header, new_s1_header)
        print("  [+] Replaced Screen 1 Header Top Bar")
    else:
        print("  [-] Could not find old_s1_header")

    # 2. Screen 1 Edit Pickup Button
    old_edit_btn = ">${TL('Edit ✏️', 'మార్చు ✏️', 'బदलें ✏️')}</button>"
    new_edit_btn = ''' style="background:#F0FDF4;color:#15803D;border:1px solid #BBF7D0;border-radius:10px;padding:5px 12px;font-size:11px;font-weight:900;cursor:pointer;flex-shrink:0;transition:all 0.15s ease;display:flex;align-items:center;gap:4px;">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#15803D" stroke-width="2.5" stroke-linecap="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                  <span>${TL('Edit', 'మార్చు', 'बदलें')}</span>
                </button>'''
    
    # Target the entire edit button tag
    pattern_edit = re.compile(r'<button onclick="openGramhaulPickupLocationModal\(\)"[^>]*>\$\{TL\(\'Edit ✏️\', \'మార్చు ✏️\', \'బద[^\']+\'\)\}</button>')
    if pattern_edit.search(text):
        text = pattern_edit.sub(r'<button onclick="openGramhaulPickupLocationModal()"' + new_edit_btn, text)
        print("  [+] Replaced Edit button with sleek SVG icon")
    else:
        print("  [-] Could not regex find Edit button")

    # 3. Commodity Specs Labels
    old_crop_label = ">${TL('🌱 Crop Commodity', '🌱 పంట రకం', '🌱 फसल का प्रकार')}</div>"
    new_crop_label = ''' style="display:flex;align-items:center;gap:5px;font-size:10px;font-weight:800;color:#475569;text-transform:uppercase;margin-bottom:5px;">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M12 22V12M12 12C12 7 7 4 2 5C2 10 5 14 12 12ZM12 12C12 7 17 4 22 5C22 10 19 14 12 12Z" stroke="#16A34A" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>
              <span>${TL('Crop Commodity', 'పంట రకం', 'फसल का प्रकार')}</span>
            </div>'''
    
    pattern_crop_label = re.compile(r'<div style="font-size:10px;font-weight:800;color:#475569;text-transform:uppercase;margin-bottom:4px;">\$\{TL\(\'🌱 Crop Commodity\', \'🌱 పంట రకం\', \'🌱 फसल का प्रकार\'\)\}</div>')
    if pattern_crop_label.search(text):
        text = pattern_crop_label.sub(r'<div' + new_crop_label, text)
        print("  [+] Replaced Crop Commodity label with SVG icon")

    pattern_sack_label = re.compile(r'<div style="font-size:10px;font-weight:800;color:#475569;text-transform:uppercase;margin-bottom:4px;">\$\{TL\(\'📦 Bags / Sacks\', \'📦 బస్తాల సంఖ్య\', \'📦 बोरी / कट्टे\'\)\}</div>')
    new_sack_label = ''' style="display:flex;align-items:center;gap:5px;font-size:10px;font-weight:800;color:#475569;text-transform:uppercase;margin-bottom:5px;">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M6 8V6C6 4.34315 7.34315 3 9 3H15C16.6569 3 18 4.34315 18 6V8M3 8H21L19.5 20C19.5 21.1046 18.6046 22 17.5 22H6.5C5.39543 22 4.5 21.1046 4.5 20L3 8Z" stroke="#D97706" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
              <span>${TL('Bags / Sacks', 'బస్తాల సంఖ్య', 'बोरी / कट्टे')}</span>
            </div>'''
    if pattern_sack_label.search(text):
        text = pattern_sack_label.sub(r'<div' + new_sack_label, text)
        print("  [+] Replaced Bags / Sacks label with SVG icon")

    # 4. Choose Commercial Truck label
    pattern_choose_truck = re.compile(r'<div style="font-size:10\.5px;font-weight:800;color:#475569;text-transform:uppercase;letter-spacing:0\.4px;">\$\{TL\(\'🚚 Choose Commercial Truck\', \'🚚 వాహనాన్ని ఎంచుకోండి\', \'🚚 वाणिज्यिक ट्रक चुनें\'\)\}</div>')
    new_choose_truck = '''<div style="display:flex;align-items:center;gap:6px;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><rect x="1" y="6" width="14" height="11" rx="2" fill="#16A34A"/><path d="M15 9H19L22 13V17H15V9Z" fill="#15803D"/><circle cx="5.5" cy="17" r="2.2" fill="#0F172A"/><circle cx="18.5" cy="17" r="2.2" fill="#0F172A"/></svg>
            <span style="font-size:11px;font-weight:900;color:#334155;text-transform:uppercase;letter-spacing:0.4px;">${TL('Choose Commercial Truck', 'వాహనాన్ని ఎంచుకోండి', 'वाणिज्यिक ट्रक चुनें')}</span>
          </div>'''
    if pattern_choose_truck.search(text):
        text = pattern_choose_truck.sub(new_choose_truck, text)
        print("  [+] Replaced Choose Commercial Truck header with SVG icon")

    # 5. Replace 5 Commercial Truck Cards in gh-truck-categories
    old_truck_categories_start = '<div style="display:flex;flex-direction:column;gap:6px;margin-bottom:14px;" id="gh-truck-categories">'
    old_truck_categories_end = '<!-- FARE BREAKDOWN & BOOK BUTTON -->'
    
    idx_tc_start = text.find(old_truck_categories_start)
    idx_tc_end = text.find(old_truck_categories_end, idx_tc_start)

    if idx_tc_start != -1 and idx_tc_end != -1:
        new_truck_categories = f'''<div style="display:flex;flex-direction:column;gap:6px;margin-bottom:14px;" id="gh-truck-categories">
          
          <!-- Truck 1: Tata Ace Gold -->
          <div onclick="selectGramhaulTruckTier(1)" id="gh-tier-1" class="gh-vehicle-card ${{selectedGramhaulTier===1?'selected':''}}">
            <div style="display:flex;align-items:center;gap:12px;">
              <div style="width:58px;height:44px;border-radius:13px;background:linear-gradient(135deg,#DCFCE7 0%,#F0FDF4 100%);border:1px solid #BBF7D0;padding:2px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                {ACE_GOLD_SVG}
              </div>
              <div>
                <div style="font-size:13.5px;font-weight:900;color:#0F172A;letter-spacing:-0.2px;">Tata Ace Gold (1.5 Ton)</div>
                <div style="font-size:11px;color:#64748B;font-weight:600;margin-top:1px;">Up to 25 Qtl · 50 Sacks · Chota Hathi</div>
              </div>
            </div>
            <div style="text-align:right;">
              <div id="gh-fare-tier-1" style="font-size:16px;font-weight:900;color:#0F172A;">₹380</div>
              <div style="font-size:9.5px;color:#16A34A;font-weight:800;margin-top:1px;">✓ Ready</div>
            </div>
          </div>

          <!-- Truck 2: Bolero Maxi Truck -->
          <div onclick="selectGramhaulTruckTier(2)" id="gh-tier-2" class="gh-vehicle-card ${{selectedGramhaulTier===2?'selected':''}}">
            <div style="display:flex;align-items:center;gap:12px;">
              <div style="width:58px;height:44px;border-radius:13px;background:linear-gradient(135deg,#EFF6FF 0%,#DBEAFE 100%);border:1px solid #BFDBFE;padding:2px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                {BOLERO_MAXI_SVG}
              </div>
              <div>
                <div style="font-size:13.5px;font-weight:900;color:#0F172A;letter-spacing:-0.2px;">Mahindra Bolero Maxi (2.5 Ton)</div>
                <div style="font-size:11px;color:#64748B;font-weight:600;margin-top:1px;">Up to 50 Qtl · 100 Sacks · Heavy Produce</div>
              </div>
            </div>
            <div style="text-align:right;">
              <div id="gh-fare-tier-2" style="font-size:16px;font-weight:900;color:#0F172A;">₹560</div>
              <div style="font-size:9.5px;color:#2563EB;font-weight:800;margin-top:1px;">Available</div>
            </div>
          </div>

          <!-- Truck 3: Ashok Leyland Dost+ -->
          <div onclick="selectGramhaulTruckTier(3)" id="gh-tier-3" class="gh-vehicle-card ${{selectedGramhaulTier===3?'selected':''}}">
            <div style="display:flex;align-items:center;gap:12px;">
              <div style="width:58px;height:44px;border-radius:13px;background:linear-gradient(135deg,#F0FDF4 0%,#DCFCE7 100%);border:1px solid #86EFAC;padding:2px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                {DOST_PLUS_SVG}
              </div>
              <div>
                <div style="font-size:13.5px;font-weight:900;color:#0F172A;letter-spacing:-0.2px;">Ashok Leyland Dost+ (3.0 Ton)</div>
                <div style="font-size:11px;color:#64748B;font-weight:600;margin-top:1px;">Up to 60 Qtl · 120 Sacks · Fast Haul</div>
              </div>
            </div>
            <div style="text-align:right;">
              <div id="gh-fare-tier-3" style="font-size:16px;font-weight:900;color:#0F172A;">₹680</div>
              <div style="font-size:9.5px;color:#16A34A;font-weight:800;margin-top:1px;">Available</div>
            </div>
          </div>

          <!-- Truck 4: Tata 407 Gold -->
          <div onclick="selectGramhaulTruckTier(4)" id="gh-tier-4" class="gh-vehicle-card ${{selectedGramhaulTier===4?'selected':''}}">
            <div style="display:flex;align-items:center;gap:12px;">
              <div style="width:58px;height:44px;border-radius:13px;background:linear-gradient(135deg,#FFFBEB 0%,#FEF3C7 100%);border:1px solid #FDE68A;padding:2px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                {TATA_407_SVG}
              </div>
              <div>
                <div style="font-size:13.5px;font-weight:900;color:#0F172A;letter-spacing:-0.2px;">Tata 407 Gold SFC (4.5 Ton)</div>
                <div style="font-size:11px;color:#64748B;font-weight:600;margin-top:1px;">Up to 85 Qtl · 170 Sacks · Mandi Legend</div>
              </div>
            </div>
            <div style="text-align:right;">
              <div id="gh-fare-tier-4" style="font-size:16px;font-weight:900;color:#0F172A;">₹820</div>
              <div style="font-size:9.5px;color:#D97706;font-weight:800;margin-top:1px;">Heavy Duty</div>
            </div>
          </div>

          <!-- Truck 5: Eicher Pro 14ft -->
          <div onclick="selectGramhaulTruckTier(5)" id="gh-tier-5" class="gh-vehicle-card ${{selectedGramhaulTier===5?'selected':''}}">
            <div style="display:flex;align-items:center;gap:12px;">
              <div style="width:58px;height:44px;border-radius:13px;background:linear-gradient(135deg,#FAF5FF 0%,#F3E8FF 100%);border:1px solid #E9D5FF;padding:2px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                {EICHER_PRO_SVG}
              </div>
              <div>
                <div style="font-size:13.5px;font-weight:900;color:#0F172A;letter-spacing:-0.2px;">Eicher Pro 14ft (5.5 Ton)</div>
                <div style="font-size:11px;color:#64748B;font-weight:600;margin-top:1px;">Up to 120 Qtl · 240 Sacks · Bulk Freight</div>
              </div>
            </div>
            <div style="text-align:right;">
              <div id="gh-fare-tier-5" style="font-size:16px;font-weight:900;color:#0F172A;">₹1,150</div>
              <div style="font-size:9.5px;color:#7C3AED;font-weight:800;margin-top:1px;">Bulk Pool</div>
            </div>
          </div>
        </div>

        '''
        text = text[:idx_tc_start] + new_truck_categories + text[idx_tc_end:]
        print("  [+] Replaced all 5 Vehicle Tier Cards with high-end vector illustrations")
    else:
        print("  [-] Could not find gh-truck-categories range")

    # 6. Screen 2 Recenter Button
    old_recenter_btn = '''<!-- White Circular Recenter Button -->
        <button onclick="recenterTrackingMap()" style="width:40px;height:40px;border-radius:50%;background:#FFFFFF;border:none;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 12px rgba(0,0,0,0.18);cursor:pointer;font-size:18px;flex-shrink:0;">
          🎯
        </button>'''
    new_recenter_btn = '''<!-- White Circular Recenter Button -->
        <button onclick="recenterTrackingMap()" title="Recenter" style="width:40px;height:40px;border-radius:50%;background:#FFFFFF;border:none;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 12px rgba(0,0,0,0.18);cursor:pointer;flex-shrink:0;">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2.5" stroke-linecap="round"><circle cx="12" cy="12" r="7"/><circle cx="12" cy="12" r="3" fill="#2563EB"/><line x1="12" y1="2" x2="12" y2="5"/><line x1="12" y1="19" x2="12" y2="22"/><line x1="2" y1="12" x2="5" y2="12"/><line x1="19" y1="12" x2="22" y2="12"/></svg>
        </button>'''
    if old_recenter_btn in text:
        text = text.replace(old_recenter_btn, new_recenter_btn)
        print("  [+] Replaced Screen 2 Recenter button with GPS crosshair SVG")

    # 7. Screen 2 Searching Center Radar Icon
    old_radar_truck = '''<div style="width:48px;height:48px;border-radius:50%;background:linear-gradient(135deg,#22C55E,#16A34A);display:flex;align-items:center;justify-content:center;font-size:24px;box-shadow:0 4px 16px rgba(34,197,94,0.4);z-index:2;">
            🚚
          </div>'''
    new_radar_truck = '''<div style="width:50px;height:50px;border-radius:50%;background:linear-gradient(135deg,#22C55E,#16A34A);display:flex;align-items:center;justify-content:center;box-shadow:0 4px 16px rgba(34,197,94,0.4);z-index:2;">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none">
              <rect x="1" y="6" width="14" height="11" rx="2" fill="#FFFFFF"/>
              <path d="M15 9H19L22 13V17H15V9Z" fill="#F1F5F9"/>
              <circle cx="5.5" cy="17" r="2.2" fill="#0F172A"/>
              <circle cx="18.5" cy="17" r="2.2" fill="#0F172A"/>
              <path d="M16 10H18.5L20.5 13H16V10Z" fill="#38BDF8"/>
            </svg>
          </div>'''
    if old_radar_truck in text:
        text = text.replace(old_radar_truck, new_radar_truck)
        print("  [+] Replaced Searching Center Radar Icon with SVG mini truck")

    # 8. Searching Cancel Button
    old_srch_cancel = '''<button onclick="cancelAndReturnToGramhaul()" style="width:100%;height:48px;background:#F1F5F9;color:#334155;border:1px solid #E2E8F0;border-radius:14px;font-size:14px;font-weight:800;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:6px;transition:background 0.15s ease;">
          <span>✕</span> <span>Cancel Search</span>
        </button>'''
    new_srch_cancel = '''<button onclick="cancelAndReturnToGramhaul()" style="width:100%;height:48px;background:#F1F5F9;color:#334155;border:1px solid #E2E8F0;border-radius:14px;font-size:14px;font-weight:800;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:6px;transition:background 0.15s ease;">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2.5" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          <span>Cancel Search</span>
        </button>'''
    if old_srch_cancel in text:
        text = text.replace(old_srch_cancel, new_srch_cancel)
        print("  [+] Replaced Searching Cancel Button with SVG")

    # 9. Dispatched Banner Truck Icon
    old_disp_banner = '''<div style="color:#0F172A;font-weight:900;font-size:14.5px;letter-spacing:-0.2px;display:flex;align-items:center;gap:6px;">
            <span>🚚</span>
            <span>Your driver is on the way</span>
          </div>'''
    new_disp_banner = '''<div style="color:#0F172A;font-weight:900;font-size:14.5px;letter-spacing:-0.2px;display:flex;align-items:center;gap:8px;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none"><rect x="1" y="6" width="14" height="11" rx="2" fill="#0F172A"/><path d="M15 9H19L22 13V17H15V9Z" fill="#0F172A"/><circle cx="5.5" cy="17" r="2.2" fill="#FFFFFF"/><circle cx="18.5" cy="17" r="2.2" fill="#FFFFFF"/><path d="M16 10H18.5L20.5 13H16V10Z" fill="#86EFAC"/></svg>
            <span>Your driver is on the way</span>
          </div>'''
    if old_disp_banner in text:
        text = text.replace(old_disp_banner, new_disp_banner)
        print("  [+] Replaced Dispatched Banner Truck Icon with SVG")

    # 10. Driver Profile Avatar
    old_driver_avatar = '''<div style="position:relative;width:50px;height:50px;border-radius:50%;overflow:hidden;background:#F0FDF4;border:2.5px solid #22C55E;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                <span style="font-size:28px;">👨🏻‍💼</span>
              </div>'''
    new_driver_avatar = '''<div style="position:relative;width:50px;height:50px;border-radius:50%;overflow:hidden;background:#F0FDF4;border:2px solid #22C55E;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                <svg width="50" height="50" viewBox="0 0 64 64" fill="none">
                  <circle cx="32" cy="32" r="30" fill="#F0FDF4"/>
                  <path d="M18 25 C18 16 46 16 46 25 Z" fill="#1E293B"/>
                  <path d="M15 25 H49 L53 27 H11 Z" fill="#0F172A"/>
                  <circle cx="32" cy="34" r="11" fill="#FDBA74"/>
                  <circle cx="28" cy="32" r="1.5" fill="#0F172A"/>
                  <circle cx="36" cy="32" r="1.5" fill="#0F172A"/>
                  <path d="M26 38 Q32 41 38 38" stroke="#451A03" stroke-width="2" fill="none" stroke-linecap="round"/>
                  <path d="M16 54 C16 44 48 44 48 54 Z" fill="#15803D"/>
                  <path d="M28 44 L32 50 L36 44 Z" fill="#FFFFFF"/>
                  <circle cx="48" cy="46" r="6" fill="#22C55E" stroke="#FFFFFF" stroke-width="1.5"/>
                  <path d="M46 46 L47.5 47.5 L50.5 44.5" stroke="#FFFFFF" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
              </div>'''
    if old_driver_avatar in text:
        text = text.replace(old_driver_avatar, new_driver_avatar)
        print("  [+] Replaced Driver Avatar with high-end portrait SVG")

    # 11. Dispatched 4 Action Buttons
    old_action_buttons = '''          <!-- 4 Tactile Circular Action Buttons -->
          <div style="display:flex;align-items:center;justify-content:space-between;padding:0 8px;margin-bottom:16px;">
            
            <!-- Call Action -->
            <div onclick="triggerDriverCall('${driverName}', '${v.phone}')" style="display:flex;flex-direction:column;align-items:center;gap:6px;cursor:pointer;">
              <div style="width:48px;height:48px;border-radius:50%;background:#F8FAFC;border:1.5px solid #E2E8F0;display:flex;align-items:center;justify-content:center;font-size:18px;color:#0F172A;box-shadow:0 2px 6px rgba(0,0,0,0.06);">
                📞
              </div>
              <span style="font-size:11.5px;color:#475569;font-weight:700;">Call</span>
            </div>

            <!-- Message Action -->
            <div onclick="openDriverLiveChatModal('${driverName}', '${plate}')" style="display:flex;flex-direction:column;align-items:center;gap:6px;cursor:pointer;">
              <div style="width:48px;height:48px;border-radius:50%;background:#F8FAFC;border:1.5px solid #E2E8F0;display:flex;align-items:center;justify-content:center;font-size:18px;color:#0F172A;box-shadow:0 2px 6px rgba(0,0,0,0.06);">
                💬
              </div>
              <span style="font-size:11.5px;color:#475569;font-weight:700;">Message</span>
            </div>

            <!-- Share Action -->
            <div onclick="shareLiveHaulTrip('${activeTrip.id || 'GH-4491'}')" style="display:flex;flex-direction:column;align-items:center;gap:6px;cursor:pointer;">
              <div style="width:48px;height:48px;border-radius:50%;background:#F8FAFC;border:1.5px solid #E2E8F0;display:flex;align-items:center;justify-content:center;font-size:18px;color:#0F172A;box-shadow:0 2px 6px rgba(0,0,0,0.06);">
                🔗
              </div>
              <span style="font-size:11.5px;color:#475569;font-weight:700;">Share</span>
            </div>

            <!-- Cancel Action -->
            <div onclick="cancelActiveHaulTripAndExit()" style="display:flex;flex-direction:column;align-items:center;gap:6px;cursor:pointer;">
              <div style="width:48px;height:48px;border-radius:50%;background:#FEE2E2;border:1.5px solid #FECACA;display:flex;align-items:center;justify-content:center;font-size:18px;color:#EF4444;box-shadow:0 2px 6px rgba(239,68,68,0.12);">
                ✕
              </div>
              <span style="font-size:11.5px;color:#EF4444;font-weight:700;">Cancel</span>
            </div>

          </div>'''

    new_action_buttons = '''          <!-- 4 Tactile Circular Action Buttons -->
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

          </div>'''
    if old_action_buttons in text:
        text = text.replace(old_action_buttons, new_action_buttons)
        print("  [+] Replaced Dispatched 4 Action Buttons with colored SVG icons")

    # 12. Dispatched Route Progress Moving Truck
    old_prog_truck = '<div style="font-size:16px;animation:truckDrive 2s ease-in-out infinite;transform:scaleX(-1);">🚚</div>'
    new_prog_truck = '''<div style="width:20px;height:20px;animation:truckDrive 2s ease-in-out infinite;transform:scaleX(-1);display:flex;align-items:center;justify-content:center;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><rect x="1" y="6" width="14" height="11" rx="2" fill="#16A34A"/><path d="M15 9H19L22 13V17H15V9Z" fill="#15803D"/><circle cx="5.5" cy="17" r="2.2" fill="#0F172A"/><circle cx="18.5" cy="17" r="2.2" fill="#0F172A"/></svg>
              </div>'''
    if old_prog_truck in text:
        text = text.replace(old_prog_truck, new_prog_truck)
        print("  [+] Replaced Route Progress Truck with moving vector SVG")

    # 13. Dispatched Trip Details Drawer Icons
    old_trip_drawer = '''            <div id="gh-trip-details-content" style="display:none;padding:0 14px 14px;font-size:12px;flex-direction:column;gap:8px;border-top:1px solid #E2E8F0;">
              <div style="display:flex;justify-content:space-between;margin-top:8px;"><span style="color:#64748B;">📍 Farm Pickup:</span><strong style="color:#0F172A;">${activeTrip.pickup || 'Himayath Nagar Farm, Telangana'}</strong></div>
              <div style="display:flex;justify-content:space-between;"><span style="color:#64748B;">🏢 Destination Mandi:</span><strong style="color:#16A34A;">${mandiName}</strong></div>
              <div style="display:flex;justify-content:space-between;"><span style="color:#64748B;">🌾 Produce Load:</span><strong style="color:#0F172A;">${crop} (${sacks})</strong></div>
              <div style="display:flex;justify-content:space-between;"><span style="color:#64748B;">💰 Freight Fare:</span><strong style="color:#16A34A;font-size:14px;font-weight:900;">₹${fare} (0% Commission)</strong></div>
            </div>'''
    new_trip_drawer = '''            <div id="gh-trip-details-content" style="display:none;padding:0 14px 14px;font-size:12px;flex-direction:column;gap:10px;border-top:1px solid #E2E8F0;">
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
            </div>'''
    if old_trip_drawer in text:
        text = text.replace(old_trip_drawer, new_trip_drawer)
        print("  [+] Replaced Trip Details Drawer Icons with colored SVG icons")

    # 14. Map Marker Icons
    # Ghost icon
    old_ghost = '''    const ghostIcon = L.divIcon({
      className: 'gh-ghost-marker',
      html: `<div style="width:32px;height:32px;border-radius:50%;background:rgba(15,23,42,0.85);border:2px solid #22C55E;display:flex;align-items:center;justify-content:center;font-size:16px;box-shadow:0 0 12px rgba(34,197,94,0.5);transform:translate(-50%, -50%);">🚚</div>`,
      iconSize: [0, 0]
    });'''
    new_ghost = '''    const ghostIcon = L.divIcon({
      className: 'gh-ghost-marker',
      html: `<div style="width:34px;height:34px;border-radius:50%;background:#0F172A;border:2px solid #22C55E;display:flex;align-items:center;justify-content:center;box-shadow:0 0 14px rgba(34,197,94,0.6);transform:translate(-50%, -50%);">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><rect x="1" y="6" width="14" height="11" rx="2" fill="#22C55E"/><path d="M15 9H19L22 13V17H15V9Z" fill="#16A34A"/><circle cx="5.5" cy="17" r="2.2" fill="#FFFFFF"/><circle cx="18.5" cy="17" r="2.2" fill="#FFFFFF"/></svg>
      </div>`,
      iconSize: [0, 0]
    });'''
    if old_ghost in text:
        text = text.replace(old_ghost, new_ghost)
        print("  [+] Replaced Tracking Ghost Marker with SVG")

    # Dispatched Live Truck Marker
    old_truck_marker = '''    const truckIcon = L.divIcon({
      className: 'gh-live-dispatched-truck',
      html: `<div style="display:flex;flex-direction:column;align-items:center;transform:translate(-50%, -100%);">
        <div style="background:#FFFFFF;color:#0F172A;border:1.5px solid #22C55E;padding:2px 7px;border-radius:6px;font-size:9.5px;font-weight:900;white-space:nowrap;box-shadow:0 3px 10px rgba(0,0,0,0.2);letter-spacing:0.5px;">${plate}</div>
        <div style="width:38px;height:38px;border-radius:50%;background:#FFFFFF;border:2.5px solid #22C55E;display:flex;align-items:center;justify-content:center;font-size:20px;box-shadow:0 2px 10px rgba(34,197,94,0.4);margin-top:2px;">
          🚚
        </div>
      </div>`,
      iconSize: [0, 0]
    });'''
    new_truck_marker = '''    const truckIcon = L.divIcon({
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
    });'''
    if old_truck_marker in text:
        text = text.replace(old_truck_marker, new_truck_marker)
        print("  [+] Replaced Dispatched Truck Map Marker with SVG")

    # 15. Selector Map Marker Icon
    old_sel_marker = '''      <div style="width:36px;height:36px;border-radius:50%;background:#FFFFFF;border:2.5px solid ${v.color};display:flex;align-items:center;justify-content:center;font-size:18px;box-shadow:0 4px 12px rgba(0,0,0,0.25);margin-top:2px;">
        🚚
      </div>'''
    new_sel_marker = '''      <div style="width:38px;height:38px;border-radius:50%;background:#FFFFFF;border:2.5px solid ${v.color};display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(0,0,0,0.25);margin-top:2px;">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none"><rect x="1" y="6" width="14" height="11" rx="2" fill="${v.color}"/><path d="M15 9H19L22 13V17H15V9Z" fill="${v.color}"/><circle cx="5.5" cy="17" r="2.2" fill="#0F172A"/><circle cx="18.5" cy="17" r="2.2" fill="#0F172A"/><path d="M16 10H18.5L20.5 13H16V10Z" fill="#BAE6FD"/></svg>
      </div>'''
    if old_sel_marker in text:
        text = text.replace(old_sel_marker, new_sel_marker)
        print("  [+] Replaced Selector Map Marker with SVG")

    # 16. Crop Selector Modal Header Icon
    old_crop_modal_header = '<div style="width:38px;height:38px;border-radius:12px;background:#DCFCE7;display:flex;align-items:center;justify-content:center;font-size:20px;">🌾</div>'
    new_crop_modal_header = '''<div style="width:38px;height:38px;border-radius:12px;background:linear-gradient(135deg,#DCFCE7,#BBF7D0);display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(22,163,74,0.15);">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M12 22V12M12 12C12 7 7 4 2 5C2 10 5 14 12 12ZM12 12C12 7 17 4 22 5C22 10 19 14 12 12Z" stroke="#15803D" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </div>'''
    if old_crop_modal_header in text:
        text = text.replace(old_crop_modal_header, new_crop_modal_header)
        print("  [+] Replaced Crop Modal Header with colored SVG icon")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"DONE patching {filepath}.\n")

patch_file('app/src/main/assets/index.html')
patch_file('nukrop_emulator.html')
print("All files patched successfully!")
