
import sys
sys.stdout.reconfigure(encoding='utf-8')
lines = open('app/src/main/assets/index.html', encoding='utf-8').read().splitlines()
for i, line in enumerate(lines):
    if 'gramhaul:' in line:
        print(f'Found at L{i+1}')
        for j in range(max(0, i-2), min(len(lines), i+30)):
            print(f'L{j+1}: {lines[j].strip()}')
        break

