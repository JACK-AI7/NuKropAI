import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos1 = text.find('function openGramhaulCropSelectorModal(')
pos2 = text.find('function selectGramhaulCrop(')
pos3 = text.find('\nfunction ', pos2 + 30)

print(text[pos1:pos3])
