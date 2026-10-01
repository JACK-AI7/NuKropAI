import os, sys, time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

artifact_dir = r"C:\Users\bjasw\.gemini\antigravity\brain\36944d22-a0e5-4ba9-95b4-639674444ec9"
html_path = os.path.abspath("nukrop_emulator.html")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 430, "height": 932})

    page.goto(f"file:///{html_path.replace(os.sep, '/')}")
    page.wait_for_load_state("networkidle")
    time.sleep(1)

    page.evaluate("""() => {
      finishLoginAndEnterDashboard('farmer');
      openScreen('gramhaul', null);
      const container = document.getElementById('screen-container');
      if (container) container.scrollTop = 0;
    }""")
    time.sleep(0.5)
    page.screenshot(path=os.path.join(artifact_dir, "verified_gramhaul_uber_white_top.png"))
    print("Captured GramHaul Top View")

    page.evaluate("""() => {
      const container = document.getElementById('screen-container');
      if (container) container.scrollTop = 420;
    }""")
    time.sleep(0.5)
    page.screenshot(path=os.path.join(artifact_dir, "verified_gramhaul_uber_white_bottom.png"))
    print("Captured GramHaul Bottom View")

    browser.close()
    print("GramHaul gallery captured!")
