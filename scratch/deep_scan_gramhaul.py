import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's find Screen 1 and Screen 2 HTML
# Screen 1 contains id="gramhaul-real-osm-map"
m1_pos = text.find('id="gramhaul-real-osm-map"')
screen1_start = text.rfind('<div class="screen', 0, m1_pos)
screen1_end = text.find('<div class="screen', m1_pos)

print(f"Screen 1 HTML range: {screen1_start} to {screen1_end}")
s1_html = text[screen1_start:screen1_end]

# Screen 2 contains id="gramhaul-tracking-osm-map"
m2_pos = text.find('id="gramhaul-tracking-osm-map"')
screen2_start = text.rfind('<div class="screen', 0, m2_pos)
screen2_end = text.find('<div class="screen', m2_pos)

print(f"Screen 2 HTML range: {screen2_start} to {screen2_end}")
s2_html = text[screen2_start:screen2_end]

# GramHaul functions range
f_start = text.find('function swapGramhaulLocations')
f_end = text.find('function cancelActiveHaulTrip(')
if f_end == -1:
    f_end = text.find('function cancelActiveHaulTrip') + 1500
else:
    # find end of cancelActiveHaulTrip
    f_end = text.find('\nfunction ', f_end + 30)

print(f"GramHaul JS range: {f_start} to {f_end}")
js_code = text[f_start:f_end]

def analyze_section(name, content):
    print(f"\n================ {name} ================")
    emojis = re.findall(r'[\U00010000-\U0010ffff\u2600-\u27bf]', content)
    unique_emojis = sorted(list(set(emojis)))
    print(f"Found {len(emojis)} emoji occurrences ({len(unique_emojis)} unique):")
    for em in unique_emojis:
        count = content.count(em)
        snippets = []
        for m in re.finditer(re.escape(em), content):
            start = max(0, m.start() - 35)
            end = min(len(content), m.end() + 35)
            snippets.append(content[start:end].replace('\n', ' '))
            if len(snippets) >= 3:
                break
        print(f"  {em} (x{count}):")
        for s in snippets:
            print(f"     ... {s.strip()} ...")

analyze_section("SCREEN 1 HTML", s1_html)
analyze_section("SCREEN 2 HTML", s2_html)
analyze_section("GRAMHAUL JS FUNCTIONS", js_code)
