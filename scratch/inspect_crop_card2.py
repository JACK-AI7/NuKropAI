import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos1 = text.find('id="gh-selected-crop-icon"')
print(text[pos1+150:pos1+550])
