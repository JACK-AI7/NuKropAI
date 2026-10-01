import sys, os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

html_path = os.path.abspath("nukrop_emulator.html")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 430, "height": 932})

    page.goto(f"file:///{html_path.replace(os.sep, '/')}")
    page.wait_for_load_state("networkidle")

    # Check visible elements and overlays
    overlays = page.evaluate("""() => {
      const allDivs = Array.from(document.querySelectorAll('div, section, modal'));
      return allDivs
        .filter(d => {
          const style = window.getComputedStyle(d);
          return (style.position === 'fixed' || style.position === 'absolute') &&
                 style.display !== 'none' &&
                 style.visibility !== 'hidden' &&
                 style.opacity !== '0' &&
                 parseInt(style.zIndex || '0') > 10;
        })
        .map(d => ({ id: d.id, className: d.className, zIndex: window.getComputedStyle(d).zIndex, text: d.innerText?.slice(0, 50) }));
    }""")

    print("Visible high z-index overlays on load:")
    for o in overlays:
        print(o)

    browser.close()
