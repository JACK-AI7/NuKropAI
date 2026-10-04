import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos1 = text.find('gramhaul:')
pos2 = text.find('gramhaul_tracking:')
# Find end of gramhaul_tracking: () => { ... }
# Next key in APP_VIEWS:
pos3 = text.find('\n  driver_dashboard:', pos2)
if pos3 == -1:
    pos3 = text.find('\n  khata:', pos2)
if pos3 == -1:
    pos3 = text.find('\n  calc_', pos2)
if pos3 == -1:
    # search next property pattern: \n  [a-zA-Z0-9_]+:
    m = re.search(r'\n  [a-zA-Z0-9_]+:\s*(?:\(\)|function)', text[pos2+50:])
    if m:
        pos3 = pos2 + 50 + m.start()

print(f"APP_VIEWS.gramhaul: {pos1} to {pos2}")
print(f"APP_VIEWS.gramhaul_tracking: {pos2} to {pos3}")

view_gh = text[pos1:pos2]
view_track = text[pos2:pos3]

def find_all_emojis_in(label, content):
    print(f"\n================ {label} ================")
    # Find unicode characters that are emojis
    # Including \u2600-\u27bf, \U0001f000-\U0001f9ff, etc.
    emojis = re.findall(r'[\U00010000-\U0010ffff\u2600-\u27bf\u2300-\u23ff\u2b50]', content)
    unique_emojis = sorted(list(set(emojis)))
    print(f"Total emojis found: {len(emojis)} ({len(unique_emojis)} unique):")
    for em in unique_emojis:
        count = content.count(em)
        snippets = []
        for m in re.finditer(re.escape(em), content):
            start = max(0, m.start() - 35)
            end = min(len(content), m.end() + 35)
            snippets.append(content[start:end].replace('\n', ' '))
            if len(snippets) >= 4:
                break
        print(f"  {em} (x{count}):")
        for s in snippets:
            print(f"     ... {s.strip()} ...")

find_all_emojis_in("APP_VIEWS.gramhaul (Screen 1)", view_gh)
find_all_emojis_in("APP_VIEWS.gramhaul_tracking (Screen 2)", view_track)

