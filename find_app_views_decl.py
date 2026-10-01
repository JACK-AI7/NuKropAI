import sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('nukrop_emulator.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('const APP_VIEWS =')
if pos == -1:
    pos = text.find('var APP_VIEWS =')
if pos == -1:
    pos = text.find('let APP_VIEWS =')

print("APP_VIEWS decl pos:", pos)
if pos != -1:
    print(text[pos:pos+300])
