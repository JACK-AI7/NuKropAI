import sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Clean community categories
text = text.replace("'🌾 All Topics'", "'All Topics'").replace("'🌾 అన్ని అంశాలు'", "'అన్ని అంశాలు'").replace("'🌾 सभी विषय'", "'सभी विषय'")
text = text.replace("'🌱 Cotton'", "'Cotton'").replace("'🌱 పత్తి'", "'పత్తి'").replace("'🌱 कपास'", "'कपास'")
text = text.replace("'🌶️ Chilli'", "'Chilli'").replace("'🌶️ మిరప'", "'మిరప'").replace("'🌶️ मिर्च'", "'मिर्च'")
text = text.replace("'🌾 Paddy'", "'Paddy'").replace("'🌾 వరి'", "'వరి'").replace("'🌾 धान'", "'धान'")
text = text.replace("'🍅 Tomato'", "'Tomato'").replace("'🍅 టమోటా'", "'టమోటా'").replace("'🍅 टमाटर'", "'टमाटर'")
text = text.replace("'🚜 Equipment'", "'Equipment'").replace("'🚜 యంత్రాలు'", "'యంత్రాలు'").replace("'🚜 उपकरण'", "'उपकरण'")
text = text.replace("'🧪 Bio-Medicines'", "'Bio-Medicines'").replace("'🧪 బయో మందులు'", "'బయో మందులు'").replace("'🧪 जैविक दवाएं'", "'जैविक दवाएं'")

# Clean equipment filter chips
text = text.replace("tractor: TL('🚜 Tractors', '🚜 ట్రాక్టర్లు', '🚜 ट्रैक्टर')", "tractor: TL('Tractors', 'ట్రాక్టర్లు', 'ट्रैक्टर')")
text = text.replace("drone: TL('🛸 Drones', '🛸 డ్రోన్లు', '🛸 ड्रोन्स')", "drone: TL('Drones', 'డ్రోన్లు', 'ड्रोन्स')")
text = text.replace("harvester: TL('🌾 Harvesters', '🌾 హార్వెస్టర్లు', '🌾 हार्वेस्टर')", "harvester: TL('Harvesters', 'హార్వెస్టర్లు', 'हार्वेस्टर')")
text = text.replace("sprayer: TL('💦 Sprayers', '💦 స్ప్రేయర్లు', '💦 स्प्रेयर')", "sprayer: TL('Sprayers', 'స్ప్రేయర్లు', 'स्प्रेयर')")

# Clean BioRx header
text = text.replace("<div>\n          <div style=\"font-size:18px;font-weight:900;color:#1B5E20;\">🌿 ${TL('Indigenous Organic Bio-Medicines'", "<div>\n          <div style=\"font-size:18px;font-weight:900;color:#1B5E20;display:flex;align-items:center;gap:6px;\"><svg width=\"20\" height=\"20\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"#16A34A\" stroke-width=\"2.2\"><path d=\"M10 2v7.31L4.36 19.46A2 2 0 0 0 6.07 22h11.86a2 2 0 0 0 1.71-2.54L14 9.31V2h-4z\"/><line x1=\"8.5\" y1=\"2\" x2=\"15.5\" y2=\"2\"/></svg><span>${TL('Indigenous Organic Bio-Medicines'")

# Clean Market auto-location btn
text = text.replace("const autoLocBtn = TL('📍 Auto-Detect Location', '📍 ఆటో-లొకేషన్', '📍 ऑटो-लोकेशन');", "const autoLocBtn = TL('Auto-Detect Location', 'ఆటో-లొకేషన్', 'ऑटो-लोकेशन');")

# Clean Total registered land label in profile modal
text = text.replace("""<label style="font-size:11.5px;font-weight:800;color:#0F172A;display:block;margin-bottom:4px;">🌾 Total Registered Land (Acres):</label>""",
                    """<label style="font-size:11.5px;font-weight:800;color:#0F172A;display:flex;align-items:center;gap:5px;margin-bottom:4px;"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2.2"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 3.5 1 9.2A7 7 0 0 1 11 20z"/><path d="M11 20v-8"/></svg><span>Total Registered Land (Acres):</span></label>""")

# Clean Save Profile button icon
text = text.replace("""💾 Save Profile Details""", """<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" style="vertical-align:middle;margin-right:6px;"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>Save Profile Details""")

with open('app/src/main/assets/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("✅ Applied all category and screen cleanups successfully!")
