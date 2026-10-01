import sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('nukrop_emulator.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('startup-experience-overlay')
if pos != -1:
    print("Found startup-experience-overlay at pos", pos)
    print(text[max(0, pos-200):min(len(text), pos+1500)])
