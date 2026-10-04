import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx1 = text.find('id="gramhaul-real-osm-map"')
idx2 = text.find('id="gramhaul-tracking-osm-map"')

print(f"Map 1 at {idx1}, Map 2 at {idx2}")

# Let's find screens before idx1 and idx2
p1 = text.rfind('<div id="screen-', 0, idx1)
p2 = text.rfind('<div id="screen-', 0, idx2)
print("Screen before map1:", repr(text[p1:p1+80]))
print("Screen before map2:", repr(text[p2:p2+80]))

# Let's find next screen after map1 and map2
n1 = text.find('<div id="screen-', idx1)
n2 = text.find('<div id="screen-', idx2)
print("Screen after map1:", repr(text[n1:n1+80]))
print("Screen after map2:", repr(text[n2:n2+80]))

# Let's check emojis in Screen 1 (p1 to n1)
s1_text = text[p1:n1]
emojis1 = set(re.findall(r'[\U00010000-\U0010ffff]', s1_text))
print("Emojis in Screen 1:", emojis1)
for em in emojis1:
    for m in re.finditer(re.escape(em), s1_text):
        snip = s1_text[max(0, m.start()-30):min(len(s1_text), m.end()+30)]
        print(f"  {em}: {snip.strip()}")

# Let's check emojis in Screen 2 (p2 to n2)
s2_text = text[p2:n2]
emojis2 = set(re.findall(r'[\U00010000-\U0010ffff]', s2_text))
print("\nEmojis in Screen 2 HTML:", emojis2)
for em in emojis2:
    for m in re.finditer(re.escape(em), s2_text):
        snip = s2_text[max(0, m.start()-30):min(len(s2_text), m.end()+30)]
        print(f"  {em}: {snip.strip()}")

# Let's check emojis in GramHaul JS functions
fn1 = text.find('function openGramHaul')
fn2 = text.find('function recenterTrackingMap')
fn_end = text.find('\nfunction ', fn2 + 50)
js_text = text[fn1:fn_end]

emojis_js = set(re.findall(r'[\U00010000-\U0010ffff]', js_text))
print("\nEmojis in GramHaul JS functions:", emojis_js)
for em in emojis_js:
    for m in re.finditer(re.escape(em), js_text):
        snip = js_text[max(0, m.start()-30):min(len(js_text), m.end()+30)]
        print(f"  {em}: {snip.strip()}")
