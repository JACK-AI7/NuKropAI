import sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('nukrop_emulator.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's see around line 15639
lines = text.split('\n')
print(f"Total lines: {len(lines)}")
start_line = max(0, 15639 - 25)
end_line = min(len(lines), 15639 + 25)

for i in range(start_line, end_line):
    print(f"{i+1}: {lines[i]}")
