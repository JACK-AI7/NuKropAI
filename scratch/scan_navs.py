import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Check side nav and bottom nav
pos_side = text.find('id="side-nav-group"')
pos_side_end = text.find('</div>', pos_side + 2000)

pos_dock = text.find('class="bottom-dock-wrap"')
pos_dock_end = text.find('</div>', pos_dock + 3000)

def print_nav_emojis(name, s):
    emojis = re.findall(r'[\U00010000-\U0010ffff\u2600-\u27bf\u2300-\u23ff\u2b50]', s)
    print(f"\n{name} emojis: {set(emojis)}")
    for em in set(emojis):
        for m in re.finditer(re.escape(em), s):
            snip = s[max(0, m.start()-30):min(len(s), m.end()+30)].replace('\n', ' ')
            print(f"  {em}: {snip.strip()}")

if pos_side != -1: print_nav_emojis("Side Nav", text[pos_side:pos_side_end])
if pos_dock != -1: print_nav_emojis("Bottom Dock", text[pos_dock:pos_dock_end])
