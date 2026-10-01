import sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('nukrop_emulator.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'<(?:div|nav)[^>]*id=[\"\'][a-zA-Z0-9_-]*dock[a-zA-Z0-9_-]*[\"\']', text)
if m:
    print("Found bottom dock element by ID:", m.group(0))
else:
    m2 = re.search(r'<(?:div|nav)[^>]*class=[\"\'][a-zA-Z0-9_ -]*dock[a-zA-Z0-9_ -]*[\"\']', text)
    if m2:
        print("Found bottom dock element by class:", m2.group(0))
