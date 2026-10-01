import re

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove the broken gstatic tailwind CDN script (doesn't exist publicly)
html = html.replace(
    '<script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>',
    ''
)

# 2. Fix the boot logic - remove duplicate initStartupExperience calls
# The readyState check outside DOMContentLoaded fires immediately before DOM is ready
# causing triple boot attempts. Keep only DOMContentLoaded.
old_boot = """// Initial Boot & Fetch Real Weather
document.addEventListener('DOMContentLoaded', () => {
  setLanguage('te');
  fetchRealLocationAndWeather();
  initStartupExperience();
});
if (document.readyState === 'complete' || document.readyState === 'interactive') {
  initStartupExperience();
}
if (document.readyState === 'complete' || document.readyState === 'interactive') {
  setLanguage('en');
  fetchRealLocationAndWeather();
  initStartupExperience();
}"""

new_boot = """// Initial Boot & Fetch Real Weather
function nukropBoot() {
  setLanguage('en');
  fetchRealLocationAndWeather();
  initStartupExperience();
}
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', nukropBoot);
} else {
  nukropBoot();
}"""

html = html.replace(old_boot, new_boot)

with open('app/src/main/assets/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Also update nukrop_emulator.html
with open('nukrop_emulator.html', 'r', encoding='utf-8') as f:
    html2 = f.read()

html2 = html2.replace(
    '<script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>',
    ''
)
html2 = html2.replace(old_boot, new_boot)

with open('nukrop_emulator.html', 'w', encoding='utf-8') as f:
    f.write(html2)

print("Fixed: removed bad CDN script and cleaned boot sequence")
