import os

files = ['app/src/main/assets/index.html', 'nukrop_emulator.html']
for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Fix 1: Connecting line alignment
    old_line_html = '<div style="display:flex;flex-direction:column;align-items:center;padding-top:2px;flex-shrink:0;">'
    new_line_html = '<div style="display:flex;flex-direction:column;align-items:center;padding-top:2px;flex-shrink:0;width:16px;">'
    text = text.replace(old_line_html, new_line_html)

    # Fix 2: Move the Haul Request sheet up so the toggle doesn't overlap it
    old_sheet = 'class="r-sheet" style="position:absolute;bottom:0;left:0;right:0;background:#FFFFFF;border-radius:22px 22px 0 0;padding:0 0 20px;box-shadow:0 -8px 32px rgba(0,0,0,0.15);z-index:20;">'
    new_sheet = 'class="r-sheet" style="position:absolute;bottom:65px;left:0;right:0;background:#FFFFFF;border-radius:22px 22px 0 0;padding:0 0 20px;box-shadow:0 -8px 32px rgba(0,0,0,0.15);z-index:20;">'
    text = text.replace(old_sheet, new_sheet)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

print('Visual fixes applied')
