import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'id=[\"\']tab-market[\"\'][\s\S]*?(?=<div class=[\"\']tab-pane|\n\s*</section>|$)', text)
if m:
    print("Found tab-market:")
    print(m.group(0)[:3000])
