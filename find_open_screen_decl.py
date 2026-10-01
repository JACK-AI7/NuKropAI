import sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('nukrop_emulator.html', 'r', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'(?:function|const|let|var)\s+openScreen', text):
    print("Found openScreen at pos", m.start())
    print(text[m.start():m.start()+200])
    print("="*40)
