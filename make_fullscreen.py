import re

with open('nukrop_emulator.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Modify the .phone-chassis CSS to be full-screen for the webview
new_chassis_css = """
.phone-chassis {
  width: 100vw;
  height: 100vh;
  background: #F8FAF8;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}
"""

content = re.sub(
    r'\.phone-chassis \{[^}]+\}',
    new_chassis_css.strip(),
    content
)

# 2. Remove the body padding and background that make it look like an emulator
new_body_css = """
body {
  background: #FFFFFF;
  font-family: 'Plus Jakarta Sans', 'Noto Sans Telugu', 'Noto Sans Devanagari', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  padding: 0px;
  margin: 0px;
  color: #0F172A;
  -webkit-font-smoothing: antialiased;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}
"""
content = re.sub(
    r'body \{[^}]+\}',
    new_body_css.strip(),
    content
)

# 3. Remove the side panel navigation that acts as the "emulator controls"
# The panel is wrapped in `<div class="side-panel-container">` which starts around line 1038
# Let's just find that block and remove it. We'll use string replacement.
content = re.sub(
    r'<!-- ═════════════════ SIDEBAR CONTROLLER ═════════════════ -->.*?<div class="side-panel-container">.*?</div>\s*</div>\s*</div>',
    '<!-- SIDEBAR REMOVED -->\n</div>\n</div>',
    content,
    flags=re.DOTALL
)

# Let's be safer and just hide `.side-panel-container` via CSS if the regex is tricky.
new_side_panel_css = """
.side-panel-container {
  display: none !important;
}
"""
if '.side-panel-container {' in content:
    content = re.sub(
        r'\.side-panel-container \{[^}]+\}',
        new_side_panel_css.strip(),
        content
    )
else:
    # insert it if not found just in case
    content = content.replace('</style>', new_side_panel_css + '\n</style>')

# Hide the outer wrapper flex container by replacing the wrapper div with just its contents or setting display: block
# It's at `<div style="display:flex;gap:20px;align-items:flex-start;flex-wrap:wrap;">`
content = content.replace('<div style="display:flex;gap:20px;align-items:flex-start;flex-wrap:wrap;">', '<div style="width: 100vw; height: 100vh; overflow: hidden; margin: 0; padding: 0;">')


with open('nukrop_emulator.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated HTML for Full Screen WebView')
