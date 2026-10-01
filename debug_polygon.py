import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# find the broken polygon SVG in the bottom nav dock
star_svg_matches = list(re.finditer(r'<polygon[^>]{0,200}points=', text))
print(f'Total polygon elements: {len(star_svg_matches)}')
for pm in star_svg_matches[:10]:
    seg = text[pm.start():pm.start()+200]
    print(repr(seg))
    print('---')
