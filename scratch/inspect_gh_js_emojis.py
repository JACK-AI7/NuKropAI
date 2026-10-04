import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

f_start = text.find('function swapGramhaulLocations')
f_end = text.find('function cancelActiveHaulTrip(')
if f_end != -1:
    f_end = text.find('\nfunction ', f_end + 30)

print(f"GramHaul JS range: {f_start} to {f_end} (length: {f_end - f_start})")
js_code = text[f_start:f_end]

emojis = re.findall(r'[\U00010000-\U0010ffff\u2600-\u27bf\u2300-\u23ff\u2b50\u25a0-\u25ff]', js_code)
unique = sorted(list(set(emojis)))
print(f"\nFound {len(emojis)} symbols/emojis ({len(unique)} unique):")
for u in unique:
    print(f"\nSymbol: {u}")
    for m in re.finditer(re.escape(u), js_code):
        start = max(0, m.start() - 40)
        end = min(len(js_code), m.end() + 40)
        print("  ...", js_code[start:end].replace('\n', ' ').strip(), "...")

