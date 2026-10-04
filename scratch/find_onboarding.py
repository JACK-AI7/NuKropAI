import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# find "Welcome!" or language selection
pos = text.find('Welcome!')
print("Welcome! found at:", pos)
if pos != -1:
    print(text[pos:pos+1000])
