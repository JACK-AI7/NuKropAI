import sys
sys.stdout.reconfigure(encoding='utf-8')

FILES = [
    'app/src/main/assets/index.html',
    'nukrop_emulator.html'
]

SVG_CHECK = '<div style="font-size:9.5px;color:#16A34A;font-weight:800;margin-top:1px;display:flex;align-items:center;justify-content:flex-end;gap:3px;"><svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg><span>Ready</span></div>'

target = '<div style="font-size:9.5px;color:#16A34A;font-weight:800;margin-top:1px;">✓ Ready</div>'

for fp in FILES:
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()
    if target in c:
        c = c.replace(target, SVG_CHECK)
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Replaced Ready badge in {fp}")
    else:
        print(f"Target not found in {fp}")
