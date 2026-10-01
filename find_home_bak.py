import sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html.bak', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Search for home view definition
pos = text.find('home:')
print("Found 'home:' at pos", pos)
if pos != -1:
    print(text[max(0, pos-100):min(len(text), pos+600)])
