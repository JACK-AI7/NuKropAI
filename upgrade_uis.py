import os
import re

files = ['app/src/main/assets/index.html', 'nukrop_emulator.html']

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # --- 1. Upgrade GramHaul Farmer UI to match Driver Map + Bottom Sheet style ---
    gh_start = text.find('gramhaul: () => {')
    gh_end = text.find('},', gh_start) + 2

    if gh_start != -1 and gh_end != -1:
        new_gramhaul = """gramhaul: () => {
    const t = I18N[currentLang] || I18N.en;
    setTimeout(initGramhaulRealMap, 80);

    return `
    <!-- Fullscreen Map Canvas (Driver Rapido Style) -->
    <div style="position:relative;width:100%;height:100vh;background:#E5EFE5;overflow:hidden;font-family:-apple-system,BlinkMacSystemFont,sans-serif;">
      
      <!-- OSM Grid Pattern -->
      <svg style="position:absolute;inset:0;width:100%;height:100%;" preserveAspectRatio="none">
        <defs><pattern id="rmap-grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M 40 0 L 0 0 0 40" fill="none" stroke="#CDD8CD" stroke-width="0.8"/></pattern></defs>
        <rect width="100%" height="100%" fill="#EBF2EB"/><rect width="100%" height="100%" fill="url(#rmap-grid)"/>
        <line x1="0" y1="45%" x2="100%" y2="45%" stroke="#FFFFFF" stroke-width="12" opacity="0.9"/>
        <line x1="30%" y1="0" x2="30%" y2="100%" stroke="#FFFFFF" stroke-width="10" opacity="0.9"/>
      </svg>

      <!-- Top Header -->
      <div style="position:absolute;top:14px;left:14px;right:14px;display:flex;justify-content:space-between;align-items:center;z-index:10;">
        <button onclick="openScreen('home',null)" style="background:#FFFFFF;border:none;width:44px;height:44px;border-radius:13px;display:flex;align-items:center;justify-content:center;box-shadow:0 3px 12px rgba(0,0,0,0.12);cursor:pointer;">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#0F172A" stroke-width="2.5"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
        </button>
        <div style="background:#FFFFFF;padding:8px 16px;border-radius:14px;box-shadow:0 3px 12px rgba(0,0,0,0.12);font-size:14px;font-weight:900;color:#16A34A;">
          🚜 GramHaul
        </div>
      </div>

      <!-- Farmer Location Marker (Center) -->
      <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);margin-top:-60px;">
        <svg width="60" height="60" viewBox="0 0 48 48">
          <circle cx="24" cy="24" r="22" fill="#16A34A" opacity="0.2"/>
          <circle cx="24" cy="24" r="14" fill="#16A34A"/>
          <circle cx="24" cy="24" r="6" fill="#FFFFFF"/>
        </svg>
      </div>

      <!-- Bottom Sheet (Rapido Driver Style) -->
      <div class="r-sheet" style="position:absolute;bottom:0;left:0;right:0;background:#FFFFFF;border-radius:24px 24px 0 0;padding:24px 18px 30px;box-shadow:0 -8px 32px rgba(0,0,0,0.12);z-index:20;">
        <div style="font-size:22px;font-weight:900;color:#0F172A;letter-spacing:-0.5px;margin-bottom:16px;">Where to haul?</div>
        
        <!-- Route Selector -->
        <div style="background:#F9FAFB;border-radius:18px;padding:16px;margin-bottom:16px;border:1px solid #EEF2F6;">
          <div style="display:flex;align-items:center;gap:14px;margin-bottom:14px;">
            <div style="width:10px;height:10px;border-radius:50%;background:#16A34A;flex-shrink:0;"></div>
            <div style="font-size:15px;font-weight:700;color:#0F172A;flex:1;">Ramesh Rao's Farm (GPS)</div>
          </div>
          <div style="height:1px;background:#E2E8F0;margin-left:24px;margin-bottom:14px;"></div>
          <div style="display:flex;align-items:center;gap:14px;">
            <div style="width:10px;height:10px;background:#EF4444;flex-shrink:0;"></div>
            <div style="font-size:15px;font-weight:700;color:#94A3B8;flex:1;">Enter Drop Mandi...</div>
          </div>
        </div>

        <!-- Crop Select Chips -->
        <div style="display:flex;gap:10px;margin-bottom:20px;overflow-x:auto;">
          <div style="background:#F0FDF4;border:2px solid #16A34A;padding:8px 14px;border-radius:100px;font-size:13px;font-weight:900;color:#15803D;white-space:nowrap;">🌱 Cotton (40 Qtl)</div>
          <div style="background:#F1F5F9;border:1px solid #E2E8F0;padding:8px 14px;border-radius:100px;font-size:13px;font-weight:800;color:#64748B;white-space:nowrap;">🌶️ Chilli</div>
          <div style="background:#F1F5F9;border:1px solid #E2E8F0;padding:8px 14px;border-radius:100px;font-size:13px;font-weight:800;color:#64748B;white-space:nowrap;">🌾 Paddy</div>
        </div>

        <button onclick="nk_sendHaulRequest('GH-4192', {crop:'Cotton', weight:'40 Qtl', mandi:'Enamamula APMC', fare:'1850'}); alert('Haul requested! Real-time notification sent to Driver.');" class="r-accept-btn" style="width:100%;height:56px;background:#16A34A;color:#FFFFFF;border-radius:16px;font-size:18px;font-weight:900;border:none;box-shadow:0 6px 20px rgba(22,163,74,0.3);cursor:pointer;transition:transform 0.15s;">
          Request Truck · ₹1,850
        </button>
      </div>
    </div>
    `;
  },"""
        text = text[:gh_start] + new_gramhaul + text[gh_end:]


    # --- 2. Upgrade Community UI to match Plantix ---
    comm_start = text.find('function renderCommunityFeedDom() {')
    comm_end = text.find('function openCommunityFilterModal', comm_start)
    if comm_start != -1 and comm_end != -1:
        new_render = """function renderCommunityFeedDom() {
  const container = document.getElementById('comm-feed-container');
  if (!container) return;

  const filtered = currentCommunityFilter === 'all'
    ? COMMUNITY_POSTS_CATALOG
    : COMMUNITY_POSTS_CATALOG.filter(p => p.cropId === currentCommunityFilter);

  container.innerHTML = filtered.map(p => {
    const authorName = (p.author && (p.author[currentLang] || p.author.en)) || 'Farmer';
    const villageName = (p.village && (p.village[currentLang] || p.village.en)) || 'Warangal';
    const cropName = (p.cropName && (p.cropName[currentLang] || p.cropName.en)) || getLocalizedCropName(p.cropId);
    const postTitle = (p.title && (p.title[currentLang] || p.title.en)) || '';
    const postDesc = (p.text && (p.text[currentLang] || p.text.en)) || '';
    const timeAgoStr = (p.timeAgo && (p.timeAgo[currentLang] || p.timeAgo.en)) || 'Just now';

    return `
      <div style="background:#FFFFFF;border-bottom:12px solid #F3F4F6;padding:18px 18px 12px;">
        <!-- Header -->
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
          <div style="display:flex;align-items:center;gap:12px;">
            <div style="width:44px;height:44px;border-radius:50%;background:#F0FDF4;color:#16A34A;display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:900;">${authorName.charAt(0)}</div>
            <div>
              <div style="font-size:15px;font-weight:900;color:#0F172A;letter-spacing:-0.2px;">${authorName}</div>
              <div style="font-size:12px;color:#64748B;font-weight:600;margin-top:2px;">📍 ${villageName} · ${timeAgoStr}</div>
            </div>
          </div>
          <div style="background:#F0FDF4;color:#15803D;padding:4px 10px;border-radius:100px;font-size:11px;font-weight:800;">${cropName}</div>
        </div>

        <!-- Content -->
        <div style="font-size:16px;font-weight:800;color:#0F172A;margin-bottom:6px;line-height:1.3;">${postTitle}</div>
        <div style="font-size:14px;color:#475569;line-height:1.5;margin-bottom:12px;">${postDesc}</div>

        <!-- Image (if any) -->
        ${p.imgSrc ? `<div style="margin-bottom:12px;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.05);"><img src="${p.imgSrc}" style="width:100%;height:auto;display:block;"></div>` : ''}

        <!-- Actions -->
        <div style="display:flex;align-items:center;justify-content:space-between;border-top:1px solid #F1F5F9;padding-top:12px;margin-top:4px;">
          <div style="display:flex;gap:20px;">
            <button style="background:none;border:none;display:flex;align-items:center;gap:6px;color:#64748B;font-size:13px;font-weight:800;cursor:pointer;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"/></svg>
              124
            </button>
            <button style="background:none;border:none;display:flex;align-items:center;gap:6px;color:#64748B;font-size:13px;font-weight:800;cursor:pointer;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>
              32
            </button>
          </div>
          <button style="background:none;border:none;color:#16A34A;font-size:13px;font-weight:900;cursor:pointer;">Share</button>
        </div>
      </div>
    `;
  }).join('');
}
\n"""
        text = text[:comm_start] + new_render + text[comm_end:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

print("UI Replacements successful.")
