import sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('nukrop_emulator.html', 'r', encoding='utf-8') as f:
    text = f.read()

matches = [m.start() for m in re.finditer(r'openScreen', text)]
print(f"Total occurrences of 'openScreen': {len(matches)}")
for pos in matches[:10]:
    print(text[max(0, pos-40):min(len(text), pos+60)])
    print("-"*30)
