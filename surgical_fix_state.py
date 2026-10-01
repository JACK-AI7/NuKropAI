import re
import os
import shutil

filepath = r"c:\Users\bjasw\Downloads\agriculture-ai-os\app\src\main\assets\index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Wrap the app shell
if 'id="app-shell"' not in content:
    # Find the audio elements comment which is right after the main app shell closes
    audio_idx = content.find('<!-- Audio Elements -->')
    if audio_idx != -1:
        sub = content[:audio_idx]
        last_div_idx = sub.rfind('</div>')
        if last_div_idx != -1:
            # Inject closing div for app-shell
            content = content[:last_div_idx] + '</div>\n    ' + content[last_div_idx:]
            # Inject opening div for app-shell
            content = content.replace('<div class="system-status-bar">', '<div id="app-shell" style="display:none; flex-direction:column; width:100%; height:100%; overflow:hidden; position:relative;">\n      <div class="system-status-bar">', 1)

# 2. Modify openScreen to show app-shell
if "document.getElementById('app-shell').style.display = 'flex';" not in content:
    content = content.replace(
        "function openScreen(screenKey, tabElement) {",
        "function openScreen(screenKey, tabElement) {\n    var appShell = document.getElementById('app-shell');\n    if(appShell) appShell.style.display = 'flex';\n"
    )

# 3. Modify initStartupExperience to ensure app-shell is hidden when startup restarts
if "appShell.style.display = 'none';" not in content:
    content = content.replace(
        "function initStartupExperience(forceReplay = false) {",
        "function initStartupExperience(forceReplay = false) {\n    var appShell = document.getElementById('app-shell');\n    if(appShell) appShell.style.display = 'none';\n"
    )

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

# We should also copy this index.html content to nukrop_emulator.html since it contains everything including the phone chassis wrapper in this architecture.
# Let's check if index.html already has the phone-chassis.
if '<div class="phone-chassis">' in content:
    shutil.copyfile(filepath, r"c:\Users\bjasw\Downloads\agriculture-ai-os\nukrop_emulator.html")

print("Startup state bug fixed surgically.")
