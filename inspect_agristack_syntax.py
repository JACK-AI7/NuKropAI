import sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('nukrop_emulator.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('agristack:')
if pos != -1:
    print("Around agristack:")
    print(text[max(0, pos-300):min(len(text), pos+300)])
