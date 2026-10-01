import sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('nukrop_emulator.html', 'r', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'id=[\"\']startup-experience-overlay[\"\']', text):
    print("Found HTML element at pos", m.start())
    print(text[m.start():m.start()+800])
    print("="*40)
