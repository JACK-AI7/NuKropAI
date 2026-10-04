import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos1 = text.find('gramhaul: () => {')
pos2 = text.find('gramhaul_tracking: () => {')
s1 = text[pos1:pos2]

for m in re.finditer(r'<button[^>]*>(.*?)</button>', s1, re.DOTALL):
    print("--- BUTTON ---")
    print(m.group(0))
