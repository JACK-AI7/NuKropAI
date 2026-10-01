with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the boot function to NOT call initStartupExperience on the HTML side
# (MainActivity.kt now calls it via evaluateJavascript after page loads with forceReplay=true)
# The HTML-side boot should only set up language and fetch weather
old_boot = """// Initial Boot & Fetch Real Weather
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

new_boot = """// Initial Boot & Fetch Real Weather
function nukropBoot() {
  setLanguage('en');
  fetchRealLocationAndWeather();
  // initStartupExperience is triggered by MainActivity.kt after page load
  // with forceReplay=true so splash always shows.
  // Fallback: if not triggered by native in 1s, start it ourselves.
  setTimeout(function() {
    if (typeof initStartupExperience === 'function') {
      initStartupExperience(true);
    }
  }, 800);
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

html2 = html2.replace(old_boot, new_boot)

with open('nukrop_emulator.html', 'w', encoding='utf-8') as f:
    f.write(html2)

print("Boot sequence updated — splash will always play on launch")
