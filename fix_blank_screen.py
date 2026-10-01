import re

with open('nukrop_emulator.html', 'r', encoding='utf-8') as f:
    content = f.read()

replacement = """        const existingOverlay = document.getElementById('startup-experience-overlay');
        if (existingOverlay) existingOverlay.remove();
        if (typeof openScreen === 'function') {
          openScreen('home', document.getElementById('tab-home'));
        }
        return;"""

content = re.sub(
    r"const existingOverlay = document.getElementById\('startup-experience-overlay'\);\s*if \(existingOverlay\) existingOverlay\.remove\(\);\s*return;",
    replacement,
    content
)

with open('nukrop_emulator.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed initStartupExperience to load home')
