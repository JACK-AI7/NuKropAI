import sys

sys.stdout.reconfigure(encoding='utf-8')

FILES = [
    'app/src/main/assets/index.html',
    'nukrop_emulator.html'
]

SVG_PIN = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/><circle cx="12" cy="9" r="2.5" fill="#FFFFFF"/></svg>'

for fp in FILES:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    # Target 1
    t1 = '📍 Himayath Nagar Farm</div>\n      <div style="width:14px;height:14px;background:#16A34A;'
    r1 = f'{SVG_PIN}<span>Himayath Nagar Farm</span></div>\\n      <div style="width:14px;height:14px;background:#16A34A;'.replace('\\n', '\n')
    
    # Target 2
    t2 = '📍 Himayath Nagar Farm</div>\n      <div style="width:16px;height:16px;background:#16A34A;'
    r2 = f'{SVG_PIN}<span>Himayath Nagar Farm</span></div>\\n      <div style="width:16px;height:16px;background:#16A34A;'.replace('\\n', '\n')

    # Also style display:inline-flex;align-items:center;gap:4px;
    content = content.replace('white-space:nowrap;box-shadow:0 2px 8px rgba(0,0,0,0.3);border:1px solid #FFFFFF;">📍 Himayath Nagar Farm', 'white-space:nowrap;box-shadow:0 2px 8px rgba(0,0,0,0.3);border:1px solid #FFFFFF;display:inline-flex;align-items:center;gap:4px;">' + SVG_PIN + '<span>Himayath Nagar Farm</span>')
    content = content.replace('white-space:nowrap;box-shadow:0 3px 10px rgba(0,0,0,0.35);border:1.5px solid #FFFFFF;">📍 Himayath Nagar Farm', 'white-space:nowrap;box-shadow:0 3px 10px rgba(0,0,0,0.35);border:1.5px solid #FFFFFF;display:inline-flex;align-items:center;gap:4px;">' + SVG_PIN + '<span>Himayath Nagar Farm</span>')

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Updated {fp}")

print("Both map markers upgraded to vector SVG pins.")
