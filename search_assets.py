import re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Look for header logo in index.html
matches = list(re.finditer(r'NuKrop|న్యూక్రాప్|app-logo|brand-logo', text))
print(f"Found {len(matches)} matches")
for m in matches[:10]:
    idx = m.start()
    print(text[max(0, idx-50):min(len(text), idx+150)])
    print('='*50)

# Look for gramhaul view in APP_VIEWS
gh_match = re.search(r'gramhaul\s*:\s*\(\)\s*=>\s*\{', text)
if gh_match:
    gh_idx = gh_match.start()
    print("GRAMHAUL VIEW START:", gh_idx)
    print(text[gh_idx:gh_idx+1500])
