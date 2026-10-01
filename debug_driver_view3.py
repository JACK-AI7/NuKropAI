import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'driver_dashboard\s*:\s*\(\)\s*=>\s*\{', text)
if m:
    start = m.start()
    snippet = text[start:start+45000]
    
    # Check if return template contains the interpolations
    ret_pos = snippet.find('return `')
    print('return template starts at offset:', ret_pos)
    
    # Search for variables in the template part (after ret_pos)
    template_part = snippet[ret_pos:]
    
    vars_to_check = ['todayEarnings', 'weekEarnings', 'todayTrips', 'activeTripHtml', 'onlineStatus', 'driverName']
    for v in vars_to_check:
        pos = template_part.find(v)
        if pos != -1:
            print(f'{v} FOUND in template at: {pos}')
            print('  Context:', repr(template_part[max(0,pos-15):pos+40]))
        else:
            print(f'{v} NOT in template section!')
