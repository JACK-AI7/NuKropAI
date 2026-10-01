import re

with open('nukrop_emulator.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Make sure .phone-chassis doesn't have border-radius
content = re.sub(
    r'border-radius:\s*48px;',
    'border-radius: 0px;',
    content
)

# And remove it from the inline style of startup-experience-overlay
content = content.replace('border-radius:48px;', 'border-radius:0px;')
content = content.replace('border-radius: 48px;', 'border-radius: 0px;')

# Ensure any margin or padding is gone
content = content.replace('<div style="display:flex;gap:20px;align-items:flex-start;flex-wrap:wrap;">', '')
# If we replaced it with width 100vw already, let's just make sure
content = content.replace('<div style="width: 100vw; height: 100vh; overflow: hidden; margin: 0; padding: 0;">', '')

# Remove the closing div for the wrapper if we removed the open div
# It might be near <!-- SIDEBAR REMOVED -->
content = content.replace('<!-- SIDEBAR REMOVED -->\\n</div>\\n</div>', '<!-- SIDEBAR REMOVED -->\\n</div>')
content = content.replace('<!-- SIDEBAR REMOVED -->\\n</div>', '<!-- SIDEBAR REMOVED -->')

with open('nukrop_emulator.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed layout wrapper')
