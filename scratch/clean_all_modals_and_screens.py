import sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Replace modal emoji plates with SVGs
modal_icons = [
    # 1. Machinery booking
    ("""<div style="width:38px;height:38px;border-radius:10px;background:#DCFCE7;display:flex;align-items:center;justify-content:center;font-size:20px;">🚜</div>""",
     """<div style="width:38px;height:38px;border-radius:10px;background:#DCFCE7;display:flex;align-items:center;justify-content:center;color:#15803D;"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="7" cy="17" r="4"/><circle cx="17" cy="17" r="3"/><path d="M10 9h4l2 4H4l1-3h5z"/><path d="M14 9V5h3l2 4"/></svg></div>"""),

    # 2. Machinery listing
    ("""<div style="width:38px;height:38px;border-radius:10px;background:#FEF3C7;display:flex;align-items:center;justify-content:center;font-size:20px;">🚜</div>""",
     """<div style="width:38px;height:38px;border-radius:10px;background:#FEF3C7;display:flex;align-items:center;justify-content:center;color:#D97706;"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="7" cy="17" r="4"/><circle cx="17" cy="17" r="3"/><path d="M10 9h4l2 4H4l1-3h5z"/><path d="M14 9V5h3l2 4"/></svg></div>"""),

    # 3. Khata modal
    ("""<div style="width:38px;height:38px;border-radius:10px;background:#DCFCE7;display:flex;align-items:center;justify-content:center;font-size:20px;">📒</div>""",
     """<div style="width:38px;height:38px;border-radius:10px;background:#DCFCE7;display:flex;align-items:center;justify-content:center;color:#15803D;"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/><line x1="8" y1="7" x2="16" y2="7"/><line x1="8" y1="11" x2="14" y2="11"/></svg></div>"""),

    # 4. Truck booking
    ("""<div style="width:38px;height:38px;border-radius:10px;background:#FEF3C7;display:flex;align-items:center;justify-content:center;font-size:20px;">🚛</div>""",
     """<div style="width:38px;height:38px;border-radius:10px;background:#FEF3C7;display:flex;align-items:center;justify-content:center;color:#D97706;"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="1" y="6" width="14" height="11" rx="2"/><polygon points="15 8 19 8 22 11 22 17 15 17 15 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg></div>"""),

    # 5. BioRx recipe
    ("""<div style="width:38px;height:38px;border-radius:10px;background:#DCFCE7;display:flex;align-items:center;justify-content:center;font-size:20px;">🌿</div>""",
     """<div style="width:38px;height:38px;border-radius:10px;background:#DCFCE7;display:flex;align-items:center;justify-content:center;color:#15803D;"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M10 2v7.31L4.36 19.46A2 2 0 0 0 6.07 22h11.86a2 2 0 0 0 1.71-2.54L14 9.31V2h-4z"/><line x1="8.5" y1="2" x2="15.5" y2="2"/></svg></div>"""),

    # 6. Price trend
    ("""<div style="width:38px;height:38px;border-radius:10px;background:#DCFCE7;display:flex;align-items:center;justify-content:center;font-size:20px;">📈</div>""",
     """<div style="width:38px;height:38px;border-radius:10px;background:#DCFCE7;display:flex;align-items:center;justify-content:center;color:#15803D;"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg></div>"""),

    # 7. Price alert
    ("""<div style="width:38px;height:38px;border-radius:10px;background:#DCFCE7;display:flex;align-items:center;justify-content:center;font-size:20px;">🔔</div>""",
     """<div style="width:38px;height:38px;border-radius:10px;background:#DCFCE7;display:flex;align-items:center;justify-content:center;color:#15803D;"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg></div>"""),

    # 8. Profile edit modal labels
    ("""<label style="font-size:11.5px;font-weight:800;color:#0F172A;display:block;margin-bottom:4px;">👤 Farmer Full Name:</label>""",
     """<label style="font-size:11.5px;font-weight:800;color:#0F172A;display:flex;align-items:center;gap:5px;margin-bottom:4px;"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2.2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg><span>Farmer Full Name:</span></label>"""),

    ("""<label style="font-size:11.5px;font-weight:800;color:#0F172A;display:block;margin-bottom:4px;">📱 Mobile Number:</label>""",
     """<label style="font-size:11.5px;font-weight:800;color:#0F172A;display:flex;align-items:center;gap:5px;margin-bottom:4px;"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2.2"><rect x="5" y="2" width="14" height="20" rx="2"/><line x1="12" y1="18" x2="12" y2="18"/></svg><span>Mobile Number:</span></label>"""),

    ("""<label style="font-size:11.5px;font-weight:800;color:#0F172A;display:block;margin-bottom:4px;">📍 Village & Mandi Location:</label>""",
     """<label style="font-size:11.5px;font-weight:800;color:#0F172A;display:flex;align-items:center;gap:5px;margin-bottom:4px;"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2.2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg><span>Village &amp; Mandi Location:</span></label>"""),

    ("""<label style="font-size:11.5px;font-weight:800;color:#0F172A;display:block;margin-bottom:4px;">🌾 Total Land Extent (Acres):</label>""",
     """<label style="font-size:11.5px;font-weight:800;color:#0F172A;display:flex;align-items:center;gap:5px;margin-bottom:4px;"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2.2"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 3.5 1 9.2A7 7 0 0 1 11 20z"/><path d="M11 20v-8"/></svg><span>Total Land Extent (Acres):</span></label>"""),
]

for old_s, new_s in modal_icons:
    if old_s in text:
        text = text.replace(old_s, new_s)
        print("✅ Replaced modal icon / label")
    else:
        print("⚠️ Not found:", old_s[:50])

# Clean up KVK Advisory tag emoji
text = text.replace("<span>⚡ KVK Advisory</span>", """<span style="display:inline-flex;align-items:center;gap:4px;"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg><span>KVK Advisory</span></span>""")

# Clean up Crop Modal subheader emoji
text = text.replace("""id="m-crop-sub">🌱 Complete OpenFarm Crop Library""", """id="m-crop-sub"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#15803D" stroke-width="2.2" style="vertical-align:middle;margin-right:4px;"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 3.5 1 9.2A7 7 0 0 1 11 20z"/><path d="M11 20v-8"/></svg>Complete OpenFarm Crop Library""")

# Clean up Home Mandi Refresh btn emoji
text = text.replace("""title="Refresh live rate">🔄</button>""", """title="Refresh live rate"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg></button>""")

# Clean up Price Trend and Set Price Alert buttons on Home
text = text.replace("""📈 ${TL('Price Trend', 'ధరల చార్ట్', 'Price Trend')}""", """<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" style="vertical-align:middle;margin-right:3px;"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>${TL('Price Trend', 'ధరల చార్ట్', 'Price Trend')}""")

text = text.replace("""🔔 ${TL('Set Price Alert', 'అలర్ట్ సెట్', 'Set Price Alert')}""", """<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" style="vertical-align:middle;margin-right:3px;"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>${TL('Set Price Alert', 'అలర్ట్ సెట్', 'Set Price Alert')}""")

with open('app/src/main/assets/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("✅ Saved index.html")
