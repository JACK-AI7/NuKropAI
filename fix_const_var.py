import sys, re

sys.stdout.reconfigure(encoding='utf-8')

def fix_var(path):
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    c = c.replace('const ONBOARDING_SLIDES_DATA = [', 'var ONBOARDING_SLIDES_DATA = [')
    c = c.replace('const PERMISSIONS_SLIDES_DATA = [', 'var PERMISSIONS_SLIDES_DATA = [')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"Fixed const in {path}")

fix_var('app/src/main/assets/index.html')
fix_var('nukrop_emulator.html')
