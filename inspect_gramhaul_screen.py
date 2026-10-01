import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'id=[\"\']screen-gramhaul[\"\'][\s\S]*?(?=<div class=[\"\']screen-pane|\n\s*</section>|$)', text)
if m:
    print("Found screen-gramhaul:")
    print(m.group(0)[:3000])
else:
    print("Searching for any other gramhaul container:")
    m2 = re.search(r'id=[\"\'][a-zA-Z0-9_-]*gramhaul[a-zA-Z0-9_-]*[\"\']', text)
    if m2:
        print("Found:", m2.group(0))
