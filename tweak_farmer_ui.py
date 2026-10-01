import os
import re

files = ['app/src/main/assets/index.html', 'nukrop_emulator.html']

# Upgraded Plantix-style SVGs
ICON_AI = '''<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a2 2 0 0 1 2 2c-.11.83.34 1.57 1.13 1.88a2.3 2.3 0 0 0 2.27-.42 2 2 0 0 1 2.83 0l1.41 1.41a2 2 0 0 1 0 2.83 2.3 2.3 0 0 0-.42 2.27c.31.79 1.05 1.24 1.88 1.13a2 2 0 0 1 2 2v2a2 2 0 0 1-2 2c-.83-.11-1.57.34-1.88 1.13a2.3 2.3 0 0 0 .42 2.27 2 2 0 0 1 0 2.83l-1.41 1.41a2 2 0 0 1-2.83 0 2.3 2.3 0 0 0-2.27-.42c-.79.31-1.24 1.05-1.13 1.88a2 2 0 0 1-2 2h-2a2 2 0 0 1-2-2c.11-.83-.34-1.57-1.13-1.88a2.3 2.3 0 0 0-2.27.42 2 2 0 0 1-2.83 0l-1.41-1.41a2 2 0 0 1 0-2.83 2.3 2.3 0 0 0 .42-2.27C4.66 14.28 3.92 13.83 3.09 13.94A2 2 0 0 1 1.1 11.94v-2a2 2 0 0 1 2-2c.83.11 1.57-.34 1.88-1.13A2.3 2.3 0 0 0 4.56 4.54a2 2 0 0 1 0-2.83l1.41-1.41a2 2 0 0 1 2.83 0 2.3 2.3 0 0 0 2.27.42c.79-.31 1.24-1.05 1.13-1.88a2 2 0 0 1 2-2h2z"></path><circle cx="12" cy="12" r="3" fill="#10B981"></circle></svg>'''

ICON_RADAR = '''<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"></path><circle cx="12" cy="12" r="4" fill="#F87171"></circle><circle cx="12" cy="12" r="8" stroke-dasharray="2 4"></circle></svg>'''

ICON_BIO = '''<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z" fill="#93C5FD"></path><path d="M12 8v8M9 12h6" stroke="#1D4ED8"></path></svg>'''

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # We will replace the 3 bento-tiles in the `home` view with Plantix-style luxury cards
    
    # 1. Farm Advisor
    text = re.sub(
        r'<div class="icon-plate" style="background:linear-gradient\(135deg,#F0F9FF 0%,#E0F2FE 100%\);border:1px solid #BAE6FD;">.*?</div>',
        f'<div class="icon-plate" style="background:#ECFDF5;border:1px solid #A7F3D0;border-radius:18px;width:48px;height:48px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(16,185,129,0.15);">{ICON_AI}</div>',
        text, flags=re.DOTALL
    )
    
    # 2. Pest & Disease
    text = re.sub(
        r'<div class="icon-plate" style="background:linear-gradient\(135deg,#FFF1F2 0%,#FFE4E6 100%\);border:1px solid #FECDD3;">.*?</div>',
        f'<div class="icon-plate" style="background:#FEF2F2;border:1px solid #FECDD3;border-radius:18px;width:48px;height:48px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(220,38,38,0.12);">{ICON_RADAR}</div>',
        text, flags=re.DOTALL
    )

    # 3. Organic Bio-Medicines
    text = re.sub(
        r'<div class="icon-plate" style="background:linear-gradient\(135deg,#ECFDF5 0%,#D1FAE5 100%\);border:1px solid #A7F3D0;">.*?</div>',
        f'<div class="icon-plate" style="background:#EFF6FF;border:1px solid #BFDBFE;border-radius:18px;width:48px;height:48px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(37,99,235,0.12);">{ICON_BIO}</div>',
        text, flags=re.DOTALL
    )
    
    # Upgrade `.suite-bento-tile` class inline styles
    # Find CSS definition for .suite-bento-tile and upgrade it
    old_css = '.suite-bento-tile { background:#FFFFFF; border:1px solid #F1F5F9; border-radius:16px; padding:12px; display:flex; align-items:center; gap:12px; cursor:pointer; box-shadow:0 1px 3px rgba(0,0,0,0.02); }'
    new_css = '.suite-bento-tile { background:#FFFFFF; border:1.5px solid #F3F4F6; border-radius:24px; padding:14px 16px; display:flex; align-items:center; gap:16px; cursor:pointer; box-shadow:0 6px 16px -4px rgba(15,23,42,0.06), 0 2px 6px -1px rgba(15,23,42,0.03); transition: transform 0.2s, box-shadow 0.2s; }'
    
    text = text.replace(old_css, new_css)
    # Also upgrade text sizing inside tiles
    text = text.replace('font-size:12px;font-weight:800;color:#0F172A;', 'font-size:15px;font-weight:800;color:#0F172A;letter-spacing:-0.2px;')
    text = text.replace('font-size:10px;color:#64748B;margin-top:2px;', 'font-size:12px;color:#64748B;margin-top:4px;font-weight:500;')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

print("Plantix-style Farmer UI enhancements applied!")
