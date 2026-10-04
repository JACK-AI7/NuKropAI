import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos1 = text.find('gramhaul: () => {')
pos2 = text.find('gramhaul_tracking: () => {')

# Find where gramhaul_tracking ends:
# Look for next view property, like "\n  driver_dashboard:" or "\n  khata:" or "\n  community:"
m = re.search(r'\n  [a-z0-9_]+:\s*(?:\(\)|\(?[a-zA-Z0-9_, ]*\)?\s*=>|function)', text[pos2+30:])
if m:
    pos3 = pos2 + 30 + m.start()
else:
    pos3 = pos2 + 5000

print(f"Screen 1 exact range: {pos1} to {pos2} (length: {pos2-pos1})")
print(f"Screen 2 exact range: {pos2} to {pos3} (length: {pos3-pos2})")

s1_content = text[pos1:pos2]
s2_content = text[pos2:pos3]

def list_emojis(name, content):
    print(f"\n--- EMOJIS IN {name} ---")
    emojis = re.findall(r'[\U00010000-\U0010ffff\u2600-\u27bf\u2300-\u23ff\u2b50]', content)
    unique = sorted(list(set(emojis)))
    print(f"Found {len(emojis)} emojis ({len(unique)} unique): {unique}")
    for u in unique:
        snippets = [content[max(0, m.start()-30):min(len(content), m.end()+30)].replace('\n', ' ') for m in re.finditer(re.escape(u), content)]
        print(f"  {u} (x{len(snippets)}): {snippets[0].strip()}")

list_emojis("SCREEN 1 (Selector)", s1_content)
list_emojis("SCREEN 2 (Tracking HTML)", s2_content)

