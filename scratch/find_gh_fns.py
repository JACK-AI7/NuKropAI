import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's search all functions with 'gramhaul' or 'haul' or 'Tracking'
fns = re.findall(r'function\s+([a-zA-Z0-9_]*(?:[Gg]ramhaul|[Hh]aul|[Tt]racking)[a-zA-Z0-9_]*)\s*\(', text)
print("GramHaul/Haul/Tracking functions:", fns)
