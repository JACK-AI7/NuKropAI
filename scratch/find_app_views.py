import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos1 = text.find('gramhaul:')
pos2 = text.find('gramhaul_tracking:')

print("pos1 (gramhaul:):", pos1, "pos2 (gramhaul_tracking:):", pos2)

if pos1 != -1:
    print("--- APP_VIEWS.gramhaul start ---")
    print(text[pos1:pos1+500])

if pos2 != -1:
    print("--- APP_VIEWS.gramhaul_tracking start ---")
    print(text[pos2:pos2+500])
