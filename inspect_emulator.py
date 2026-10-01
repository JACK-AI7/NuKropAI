import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('nukrop_emulator.html', 'r', encoding='utf-8') as f:
    text = f.read()

print('nukrop_emulator.html length:', len(text))
matches = re.findall(r'function [a-zA-Z0-9_]+', text)
relevant = [m for m in matches if any(k in m.lower() for k in ['onboard', 'perm', 'login', 'auth', 'splash', 'gramhaul', 'driver', 'google', 'signin', 'signup'])]
print('Relevant in emulator:', set(relevant))
