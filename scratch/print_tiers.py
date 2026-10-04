import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

for i in range(1, 6):
    pos = text.find(f'id="gh-tier-{i}"')
    if pos != -1:
        print(f"--- TIER {i} ---")
        print(text[pos:pos+1600].split('</div>\n          </div>')[0])
