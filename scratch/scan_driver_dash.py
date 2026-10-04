import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('driver_dashboard:')
if pos != -1:
    pos_end = text.find('\n  khata:', pos)
    if pos_end == -1: pos_end = pos + 10000
    d_html = text[pos:pos_end]
    emojis = re.findall(r'[\U00010000-\U0010ffff\u2600-\u27bf\u2300-\u23ff\u2b50]', d_html)
    print("driver_dashboard emojis:", set(emojis))
    for em in set(emojis):
        for m in re.finditer(re.escape(em), d_html):
            snip = d_html[max(0, m.start()-30):min(len(d_html), m.end()+30)].replace('\n', ' ')
            print(f"  {em}: {snip.strip()}")
