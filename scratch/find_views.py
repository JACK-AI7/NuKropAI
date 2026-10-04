import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m1_pos = text.find('id="gramhaul-real-osm-map"')
m2_pos = text.find('id="gramhaul-tracking-osm-map"')

# Find the enclosing screens
screen1_tag = text.rfind('<div', 0, text.rfind('id="view-gramhaul"', 0, m1_pos) if 'id="view-gramhaul"' in text else 0)
# Let's find id="view-" or similar
views = [m.start() for m in re.finditer(r'<div[^>]+id=["\']view-[^"\']+["\']', text)]
print(f"Total views found: {len(views)}")
for v in views:
    v_tag = text[v:v+100]
    if 'gramhaul' in v_tag.lower():
        print("Gramhaul view tag:", v_tag, "at", v)

# Let's search for gramhaul screen div
for m in re.finditer(r'<div[^>]+(screen-gramhaul|view-gramhaul|gramhaul)[^>]*>', text, re.IGNORECASE):
    print("Match:", m.group(0)[:120], "at", m.start())
