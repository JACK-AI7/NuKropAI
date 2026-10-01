import sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('nukrop_emulator.html', 'r', encoding='utf-8') as f:
    text = f.read()

matches = [m.start() for m in re.finditer(r'function openOnboardingFlow', text)]
print(f"Occurrences of 'function openOnboardingFlow': {len(matches)} at positions {matches}")

for pos in matches:
    print("--- DEFINITION AT POS", pos, "---")
    print(text[pos:pos+400])
