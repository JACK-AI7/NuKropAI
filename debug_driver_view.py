import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'driver_dashboard\s*:\s*\(\)\s*=>\s*\{', text)
if m:
    start = m.start()
    snippet = text[start:start+20000]
    
    # Look for the main HTML return point in the view
    search_term = 'return `'
    bt_pos = snippet.find(search_term)
    print('return backtick at offset:', bt_pos)
    
    # Also check for template literal start
    backtick_count = snippet.count('`')
    print('Total backticks in first 20000 chars:', backtick_count)
    
    # Find positions of all backticks
    for i, c in enumerate(snippet[:5000]):
        if c == '`':
            print('Backtick at', i, ':', repr(snippet[max(0,i-30):i+50]))
