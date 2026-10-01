import re

with open('nukrop_emulator.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the viewport meta tag to prevent scaling issues on mobile
content = re.sub(
    r'<meta name="viewport" content="width=device-width,initial-scale=1"/>',
    '<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0"/>',
    content
)

with open('nukrop_emulator.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Added viewport meta tag')
