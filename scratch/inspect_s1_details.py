import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos1 = text.find('gramhaul: () => {')
pos2 = text.find('gramhaul_tracking: () => {')
s1 = text[pos1:pos2]

print("Length of Screen 1 code:", len(s1))

# Let's inspect headings, buttons, and badges in Screen 1
print("\n--- Buttons in Screen 1 ---")
for m in re.finditer(r'<button[^>]*>.*?</button>', s1, re.DOTALL):
    print("Button:", m.group(0)[:100].replace('\n', ' '))

print("\n--- SVGs in Screen 1 ---")
svgs = re.findall(r'<svg[^>]*>.*?</svg>', s1, re.DOTALL)
print(f"Total SVGs in Screen 1: {len(svgs)}")
