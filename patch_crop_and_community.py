# -*- coding: utf-8 -*-
import os
import re

def update_files(filepath):
    print(f"Updating {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update Crop Bar Markup
    old_crop_bar_pattern = re.compile(
        r'<!-- Active Registered Crops Carousel.*?-->\s*<div[^>]*overflow-x:auto[^>]*>\s*\$\{myActiveCrops\.map[\s\S]*?openCropModal\(\)[\s\S]*?<\/div>\s*<\/div>',
        re.DOTALL
    )

    new_crop_bar = """<!-- Active Registered Crops Carousel (Pixel-Perfect Alignment & Luxury Elevation) -->
    <div style="display:flex;gap:12px;padding:10px 18px 14px;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none;align-items:flex-start;">
      ${myActiveCrops.map((c, i) => `
        <div onclick="selectCropTab(${i})" style="display:flex;flex-direction:column;align-items:center;cursor:pointer;flex-shrink:0;width:66px;">
          <div class="plantix-crop-badge" style="width:58px;height:58px;border-radius:18px;background:#FFFFFF;border:2.5px solid ${activeCropIdx===i?'#16A34A':'#E2E8F0'};box-shadow:${activeCropIdx===i?'0 4px 14px rgba(22,163,74,0.35), 0 0 0 2px rgba(22,163,74,0.2)':'0 2px 8px rgba(0,0,0,0.04)'};display:flex;align-items:center;justify-content:center;padding:7px;margin:0 auto 6px;transition:all 0.2s ease;">
            ${getCropIconImg(c.path, c.id)}
          </div>
          <span style="font-size:11px;font-weight:${activeCropIdx===i?'900':'700'};color:${activeCropIdx===i?'#15803D':'#475569'};text-align:center;width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;line-height:1.2;">${getLocalizedCropName(c.id)}</span>
        </div>
      `).join('')}
      <div onclick="openCropModal()" style="display:flex;flex-direction:column;align-items:center;cursor:pointer;flex-shrink:0;width:66px;">
        <div class="crop-add-btn" style="width:58px;height:58px;border-radius:18px;background:linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);border:2px dashed #16A34A;display:flex;align-items:center;justify-content:center;margin:0 auto 6px;box-shadow:0 2px 8px rgba(22,163,74,0.15);cursor:pointer;transition:all 0.2s ease;">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
        </div>
        <span style="font-size:11px;font-weight:900;color:#16A34A;text-align:center;width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;line-height:1.2;">+ Add Crop</span>
      </div>
    </div>"""

    if old_crop_bar_pattern.search(html):
        html = old_crop_bar_pattern.sub(new_crop_bar, html)
        print("Updated crop bar carousel")
    else:
        print("Warning: crop bar pattern not matched")

    # 2. Embed Botanical SVG illustrations inside getCropIconImg
    old_fn_start = "function getCropIconImg(path, slug) {"
    new_fn_start = """function getCropIconImg(path, slug) {
  let cleanSlug = (slug || 'cotton').toLowerCase().trim();

  const INLINE_BOTANICAL_SVGS = {
    chilli: `<svg viewBox="0 0 48 48" width="100%" height="100%" fill="none">
      <path d="M14 6C14 6 18 10 20 14" stroke="#15803D" stroke-width="3" stroke-linecap="round"/>
      <path d="M12 4C14 6 16 7 19 6" stroke="#16A34A" stroke-width="2.5" stroke-linecap="round"/>
      <path d="M18 13C24 16 34 22 36 30C38 38 32 44 26 44C20 44 14 38 15 28C15.6 22 17.5 17 18 13Z" fill="url(#chilliGrad)"/>
      <path d="M20 16C23 20 28 26 28 34" stroke="#F87171" stroke-width="1.8" stroke-linecap="round" opacity="0.6"/>
      <defs>
        <linearGradient id="chilliGrad" x1="16" y1="14" x2="34" y2="44" gradientUnits="userSpaceOnUse">
          <stop stop-color="#EF4444"/><stop offset="0.7" stop-color="#DC2626"/><stop offset="1" stop-color="#991B1B"/>
        </linearGradient>
      </defs>
    </svg>`,
    chili: `<svg viewBox="0 0 48 48" width="100%" height="100%" fill="none">
      <path d="M14 6C14 6 18 10 20 14" stroke="#15803D" stroke-width="3" stroke-linecap="round"/>
      <path d="M12 4C14 6 16 7 19 6" stroke="#16A34A" stroke-width="2.5" stroke-linecap="round"/>
      <path d="M18 13C24 16 34 22 36 30C38 38 32 44 26 44C20 44 14 38 15 28C15.6 22 17.5 17 18 13Z" fill="url(#chilliGrad2)"/>
      <defs>
        <linearGradient id="chilliGrad2" x1="16" y1="14" x2="34" y2="44" gradientUnits="userSpaceOnUse">
          <stop stop-color="#EF4444"/><stop offset="1" stop-color="#991B1B"/>
        </linearGradient>
      </defs>
    </svg>`,
    tomato: `<svg viewBox="0 0 48 48" width="100%" height="100%" fill="none">
      <circle cx="24" cy="28" r="16" fill="url(#tomatoGrad)"/>
      <path d="M24 12V6M24 12L18 8M24 12L30 8M24 12L20 14M24 12L28 14" stroke="#15803D" stroke-width="2.6" stroke-linecap="round"/>
      <ellipse cx="20" cy="22" rx="4" ry="2" fill="#FCA5A5" opacity="0.6"/>
      <defs>
        <radialGradient id="tomatoGrad" cx="35%" cy="35%" r="65%">
          <stop stop-color="#F87171"/><stop offset="0.6" stop-color="#DC2626"/><stop offset="1" stop-color="#991B1B"/>
        </radialGradient>
      </defs>
    </svg>`,
    wheat: `<svg viewBox="0 0 48 48" width="100%" height="100%" fill="none">
      <path d="M24 44V10" stroke="#D97706" stroke-width="2.5" stroke-linecap="round"/>
      <ellipse cx="24" cy="12" rx="4" ry="6" fill="#F59E0B"/>
      <ellipse cx="18" cy="18" rx="4" ry="6" transform="rotate(-30 18 18)" fill="#FBBF24"/>
      <ellipse cx="30" cy="18" rx="4" ry="6" transform="rotate(30 30 18)" fill="#F59E0B"/>
      <ellipse cx="18" cy="28" rx="4" ry="6" transform="rotate(-30 18 28)" fill="#FBBF24"/>
      <ellipse cx="30" cy="28" rx="4" ry="6" transform="rotate(30 30 28)" fill="#F59E0B"/>
      <ellipse cx="18" cy="38" rx="3.5" ry="5" transform="rotate(-30 18 38)" fill="#FBBF24"/>
      <ellipse cx="30" cy="38" rx="3.5" ry="5" transform="rotate(30 30 38)" fill="#D97706"/>
    </svg>`,
    cotton: `<svg viewBox="0 0 48 48" width="100%" height="100%" fill="none">
      <path d="M24 44V34" stroke="#15803D" stroke-width="2.5" stroke-linecap="round"/>
      <path d="M18 34C18 34 21 30 24 32C27 30 30 34 30 34" fill="#16A34A"/>
      <circle cx="24" cy="20" r="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <circle cx="17" cy="24" r="8" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.2"/>
      <circle cx="31" cy="24" r="8" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.2"/>
      <circle cx="24" cy="14" r="7" fill="#FFFFFF"/>
      <path d="M24 34L22 28L24 24L26 28Z" fill="#15803D"/>
    </svg>`,
    paddy: `<svg viewBox="0 0 48 48" width="100%" height="100%" fill="none">
      <path d="M14 42C16 32 20 20 32 10" stroke="#16A34A" stroke-width="2.8" stroke-linecap="round"/>
      <ellipse cx="28" cy="14" rx="3" ry="6" transform="rotate(45 28 14)" fill="#84CC16"/>
      <ellipse cx="24" cy="20" rx="3" ry="6" transform="rotate(45 24 20)" fill="#65A30D"/>
      <ellipse cx="20" cy="27" rx="3" ry="6" transform="rotate(45 20 27)" fill="#84CC16"/>
      <ellipse cx="17" cy="34" rx="3" ry="5" transform="rotate(45 17 34)" fill="#4D7C0F"/>
    </svg>`,
    rice: `<svg viewBox="0 0 48 48" width="100%" height="100%" fill="none">
      <path d="M14 42C16 32 20 20 32 10" stroke="#16A34A" stroke-width="2.8" stroke-linecap="round"/>
      <ellipse cx="28" cy="14" rx="3" ry="6" transform="rotate(45 28 14)" fill="#84CC16"/>
      <ellipse cx="24" cy="20" rx="3" ry="6" transform="rotate(45 24 20)" fill="#65A30D"/>
      <ellipse cx="20" cy="27" rx="3" ry="6" transform="rotate(45 20 27)" fill="#84CC16"/>
      <ellipse cx="17" cy="34" rx="3" ry="5" transform="rotate(45 17 34)" fill="#4D7C0F"/>
    </svg>`,
    peas: `<svg viewBox="0 0 48 48" width="100%" height="100%" fill="none">
      <path d="M8 12C12 18 16 36 38 40C32 38 18 32 14 16C12 14 10 12 8 12Z" fill="#15803D"/>
      <circle cx="19" cy="24" r="4.5" fill="#4ADE80"/>
      <circle cx="26" cy="29" r="4.5" fill="#22C55E"/>
      <circle cx="33" cy="35" r="4.5" fill="#16A34A"/>
    </svg>`,
    pea: `<svg viewBox="0 0 48 48" width="100%" height="100%" fill="none">
      <path d="M8 12C12 18 16 36 38 40C32 38 18 32 14 16C12 14 10 12 8 12Z" fill="#15803D"/>
      <circle cx="19" cy="24" r="4.5" fill="#4ADE80"/>
      <circle cx="26" cy="29" r="4.5" fill="#22C55E"/>
      <circle cx="33" cy="35" r="4.5" fill="#16A34A"/>
    </svg>`,
    maize: `<svg viewBox="0 0 48 48" width="100%" height="100%" fill="none">
      <path d="M16 42C18 32 22 18 32 12" stroke="#15803D" stroke-width="3" stroke-linecap="round"/>
      <ellipse cx="25" cy="24" rx="8" ry="14" fill="#FACC15"/>
      <path d="M18 36C20 30 20 24 16 20" stroke="#16A34A" stroke-width="3" stroke-linecap="round"/>
      <path d="M32 36C30 30 30 24 34 20" stroke="#16A34A" stroke-width="3" stroke-linecap="round"/>
    </svg>`
  };

  for (const key of Object.keys(INLINE_BOTANICAL_SVGS)) {
    if (cleanSlug.includes(key)) {
      return INLINE_BOTANICAL_SVGS[key];
    }
  }
"""

    if old_fn_start in html:
        html = html.replace(old_fn_start, new_fn_start)
        print("Updated getCropIconImg with embedded SVGs")

    # 3. Add rich video and image posts to COMMUNITY_POSTS_CATALOG
    old_post3 = """    {
      id: 'post-3',"""
    
    extra_posts = """    {
      id: 'post-4',
      author: { en: 'Venkat Reddy', te: 'వెంకట్ రెడ్డి', hi: 'वेंकट रेड्डी', ta: 'வெங்கட் ரெட்டி' },
      avatar: '👨‍🌾',
      avatarUrl: 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=150&auto=format&fit=crop&q=80',
      verified: true,
      verifiedBadge: 'Solar & Drip Irrigation Lead',
      village: { en: 'Mulugu (8 Acres)', te: 'ములుగు (8 ఎకరాలు)', hi: 'मुलुगु (8 एकड़)' },
      cropId: 'tomato',
      cropName: { en: 'Tomato', te: 'టమాటా', hi: 'टमाटर' },
      timeAgo: { en: '1 day ago', te: 'నిన్న', hi: 'कल' },
      title: {
        en: 'Automated Solar Drip Fertigation Tutorial — Saves 70% Water & ₹14,000 Fertilizer cost!',
        te: 'సౌర శక్తితో డ్రిప్ ఫెర్టిగేషన్ విధానం — 70% నీటి ఆదా మరియు ఎరువుల ఖర్చు తగ్గుతుంది!',
        hi: 'सौर ड्रिप फर्टिगेशन ट्यूटोरियल — 70% पानी और ₹14,000 खाद खर्च की बचत!'
      },
      text: {
        en: 'Watch my video walkthrough on venturi injector setup for water-soluble fertilizers (19:19:19). Zero electricity bills and even distribution across all rows.',
        te: 'నీటిలో కరిగే ఎరువుల కోసం వెంచురీ ఇంజెక్టర్ సెటప్ వీడియో చూడండి. కరెంట్ ఖర్చు లేదు, సమానంగా ఎరువులు అందుతాయి.',
        hi: 'पानी में घुलनशील खाद (19:19:19) के लिए वेंचुरी इंजेक्टर सेटअप वीडियो देखें। बिजली का कोई बिल नहीं और बराबर छिड़काव।'
      },
      likes: 68,
      isLiked: true,
      photos: [],
      videos: ['https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4'],
      media_url: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4',
      media_type: 'video',
      mediaLabel: { en: '1 Drip Video (HD)', te: '1 డ్రిప్ వీడియో (HD)', hi: '1 ड्रिप वीडियो (HD)' },
      isResolved: true,
      comments: [
        {
          author: { en: 'B. Jaswanth Reddy', te: 'బి. జస్వంత్ రెడ్డి', hi: 'बी. जसवंत रेड्डी' },
          avatarUrl: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80',
          role: 'Progressive Farmer',
          timeAgo: { en: '18 hours ago', te: '18 గంటల క్రితం', hi: '18 घंटे पहले' },
          text: { en: 'Excellent setup Venkat! What is the subsidy percentage under PM-KUSUM for this 5HP pump?', te: 'చాలా బాగుంది వెంకట్ గారు! 5HP పంపుకు పిఎం కుసుమ్ కింద సబ్సిడీ ఎంత వచ్చింది?', hi: 'बहुत बढ़िया सेटअप वेंकट जी! 5HP पंप पर पीएम-कुसुम के तहत सब्सिडी कितनी मिली?' }
        }
      ]
    },
    {
      id: 'post-3',"""

    if old_post3 in html and 'id: \'post-4\'' not in html:
        html = html.replace(old_post3, extra_posts)
        print("Added post-4 with video to COMMUNITY_POSTS_CATALOG")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Done updating {filepath}!")

if __name__ == '__main__':
    update_files('app/src/main/assets/index.html')
    update_files('nukrop_emulator.html')
