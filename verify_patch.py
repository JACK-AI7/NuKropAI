import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'app\src\main\assets\index.html', 'rb') as f:
    raw = f.read()
bom = raw[:3] if raw[:3]==b'\xef\xbb\xbf' else b''
text = raw[len(bom):].decode('utf-8')

checks = [
    ('OLD: SELECT YOUR TRUCK',     'SELECT YOUR TRUCK'),
    ('OLD: gh-vehicle-card',       'gh-vehicle-card'),
    ('OLD: GramHaul Mandi Dispatch','GramHaul Mandi Dispatch'),
    ('OLD: 38% map height',        '38vh'),
    ('NEW: gh-rapido-sheet',       'gh-rapido-sheet'),
    ('NEW: gh-rv-icon',            'gh-rv-icon'),
    ('NEW: Choose a Truck',        'Choose a Truck'),
    ('NEW: Book Mandi Truck',      'Book Mandi Truck'),
]
for label, pattern in checks:
    idx = text.find(pattern)
    status = ('FOUND at ' + str(idx)) if idx >= 0 else 'NOT FOUND'
    print(label + ': ' + status)

import re
matches = list(re.finditer(r'gramhaul:\s*\(\)\s*=>', text))
print('gramhaul: () => count: ' + str(len(matches)))
for m in matches:
    print('  at char ' + str(m.start()) + ': ' + repr(text[m.start():m.start()+60]))
