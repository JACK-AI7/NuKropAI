import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
for m in re.finditer(r'Himayath Nagar Farm', text):
    start = max(0, m.start() - 100)
    end = min(len(text), m.end() + 100)
    print("Match at", m.start(), ":")
    print(text[start:end])
