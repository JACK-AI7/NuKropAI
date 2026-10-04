import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('✓ Ready')
print(f"✓ Ready at {pos}:")
print(text[pos-150:pos+150])
