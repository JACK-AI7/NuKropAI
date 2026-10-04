import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('gh-tier-1')
print(text[pos-9000:pos-7500])
