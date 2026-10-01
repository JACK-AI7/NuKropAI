import sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html.bak', 'r', encoding='utf-8') as f:
    bak_text = f.read()

pos = bak_text.find('const APP_VIEWS =')
print("In bak file, APP_VIEWS pos:", pos)
if pos != -1:
    print(bak_text[pos:pos+300])

# Let's see the entire APP_VIEWS length in bak
m = re.search(r'const APP_VIEWS = \{[\s\S]*?\n\};', bak_text)
if m:
    print("Found full APP_VIEWS in bak! Length:", len(m.group(0)))
    with open('app_views_clean.js', 'w', encoding='utf-8') as out:
        out.write(m.group(0))
    print("Saved app_views_clean.js")
