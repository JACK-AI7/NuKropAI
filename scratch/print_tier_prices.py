import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'selectGramhaulTruckTier\(([1-5])\)', text):
    start = m.start()
    sub = text[start:start+1500]
    # find text-align:right
    tar = sub.find('text-align:right')
    if tar != -1:
        print(f"Tier {m.group(1)} price block:")
        print(sub[tar:tar+250])
