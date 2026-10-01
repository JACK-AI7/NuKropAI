import sys, re
sys.stdout.reconfigure(encoding='utf-8')
content = open('app/src/main/assets/index.html', encoding='utf-8').read()
lines = content.splitlines()
print(f'Total lines: {len(lines)}')

def find(keyword, max_results=6, max_line=None):
    results = []
    for i, line in enumerate(lines):
        if max_line and i > max_line:
            break
        if keyword.lower() in line.lower():
            results.append((i+1, line[:130].strip()))
        if len(results) >= max_results:
            break
    return results

def find_re(pattern, max_results=6):
    results = []
    for i, line in enumerate(lines):
        if re.search(pattern, line, re.IGNORECASE):
            results.append((i+1, line[:130].strip()))
        if len(results) >= max_results:
            break
    return results

# Profile screen
print('\n=== farmerProfile object start ===')
for ln, txt in find('const farmerProfile', max_results=3):
    print(f'  L{ln}: {txt}')

print('\n=== openScreen profile ===')
for ln, txt in find_re(r"openScreen\s*\(\s*['\"]profile"):
    print(f'  L{ln}: {txt}')

print('\n=== profile edit modal ===')
for ln, txt in find('profile-edit-modal'):
    print(f'  L{ln}: {txt}')

print('\n=== farmerProfile defaults (name/phone/village) ===')
for ln, txt in find('farmerProfile', max_results=20, max_line=5090):
    print(f'  L{ln}: {txt}')

print('\n=== pesticide calculator ===')
for ln, txt in find('pesticide', max_results=8):
    print(f'  L{ln}: {txt}')

print('\n=== tank mix / tank dose ===')
for ln, txt in find_re(r'tank.*(mix|dose|calc)', max_results=8):
    print(f'  L{ln}: {txt}')

print('\n=== weather fetch function ===')
for ln, txt in find('fetchRealLocationAndWeather', max_results=8):
    print(f'  L{ln}: {txt}')

print('\n=== KCC loans section ===')
for ln, txt in find_re(r'kcc.*(loan|limit|sanctioned)', max_results=8):
    print(f'  L{ln}: {txt}')

print('\n=== subsidies screen ===')
for ln, txt in find_re(r"openScreen\s*\(\s*['\"]subsid", max_results=6):
    print(f'  L{ln}: {txt}')

print('\n=== GramHaul / truck ===')
for ln, txt in find_re(r'gramhaul|truckshare|truck.share', max_results=6):
    print(f'  L{ln}: {txt}')

print('\n=== indigenous / bio medicines ===')
for ln, txt in find_re(r'indigenous|biomed|bio.med|neem.formula', max_results=6):
    print(f'  L{ln}: {txt}')

print('\n=== community followers ===')
for ln, txt in find_re(r'follow(er|ing)', max_results=6):
    print(f'  L{ln}: {txt}')

print('\n=== scanner / disease scan ===')
for ln, txt in find_re(r'scanner|plantix|disease.*scan', max_results=6):
    print(f'  L{ln}: {txt}')

print('\n=== notification permission onboarding ===')
for ln, txt in find_re(r'perm_notif|notification.*perm|onboarding.*step', max_results=8):
    print(f'  L{ln}: {txt}')
