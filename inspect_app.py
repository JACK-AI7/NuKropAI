import re

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

print('Length of index.html:', len(text))
matches = re.findall(r'function [a-zA-Z0-9_]+', text)
relevant = [m for m in matches if any(k in m.lower() for k in ['onboard', 'perm', 'login', 'auth', 'splash', 'gramhaul', 'driver', 'google', 'signin', 'signup'])]
print('Relevant functions:', set(relevant))

# Search for sections in html
for match in re.finditer(r'<(?:div|section)[^>]*id=[\"\']([a-zA-Z0-9_-]+)[\"\']', text):
    id_name = match.group(1)
    if any(k in id_name.lower() for k in ['onboard', 'perm', 'login', 'auth', 'splash', 'gramhaul', 'driver', 'screen']):
        print('Element ID:', id_name)
