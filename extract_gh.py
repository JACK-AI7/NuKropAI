
import sys
sys.stdout.reconfigure(encoding='utf-8')
lines = open('app/src/main/assets/index.html', encoding='utf-8').read().splitlines()
in_gh = False
for line in lines:
    if 'gramhaul: () => {' in line:
        in_gh = True
    if in_gh:
        print(line)
        if '},' in line and 'market:' in lines[lines.index(line)+2]: # roughly finding the end
            pass
        if '/* --' in line:
            break

