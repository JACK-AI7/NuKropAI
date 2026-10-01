import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'driver_dashboard\s*:\s*\(\)\s*=>\s*\{', text)
if m:
    start = m.start()
    snippet = text[start:start+20000]

    # search for interpolated variables
    pattern = r'\$\{[a-zA-Z_]+\}'
    matches = list(re.finditer(pattern, snippet))
    print(f'Total interpolations found: {len(matches)}')
    for mm in matches[:20]:
        print(f'  At {mm.start()}: {mm.group()}')
    
    # Check if the template literal is properly formed
    # Find first backtick after 'return '
    ret_pos = snippet.find('return `')
    if ret_pos != -1:
        print(f'return backtick at: {ret_pos}')
        # Count unescaped backticks from that point
        sub = snippet[ret_pos:]
        bt_count = sub.count('`')
        print(f'Backticks after return: {bt_count}')
