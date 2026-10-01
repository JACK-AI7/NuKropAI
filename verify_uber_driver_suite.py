import os, sys, time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

artifact_dir = r"C:\Users\bjasw\.gemini\antigravity\brain\36944d22-a0e5-4ba9-95b4-639674444ec9"
html_path = os.path.abspath("nukrop_emulator.html")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 430, "height": 932})

    page.on("pageerror", lambda err: print(f"PAGE ERROR: {err}"))
    page.on("console", lambda msg: print(f"CONSOLE [{msg.type}]: {msg.text}"))

    page.goto("file:///" + html_path.replace("\\", "/"))
    page.wait_for_load_state("networkidle")
    time.sleep(1.5)

    # === 1. DRIVER COCKPIT — ONLINE / IDLE STATE ===
    page.evaluate("""() => {
      finishLoginAndEnterDashboard('driver');
      localStorage.setItem('gh_driver_online', 'true');
      localStorage.removeItem('nukrop_active_trip');
      if (typeof openScreen === 'function') openScreen('driver_dashboard', null);
      const c = document.getElementById('screen-container');
      if (c) c.scrollTop = 0;
    }""")
    time.sleep(1.5)
    page.screenshot(path=os.path.join(artifact_dir, "v5_driver_online_idle.png"))
    print("Captured: v5_driver_online_idle.png")

    # === 2. DRIVER COCKPIT — ACTIVE LIVE TRIP ===
    page.evaluate("""() => {
      localStorage.setItem('nukrop_active_trip', JSON.stringify({
        id: 'GH-4192',
        crop: 'Cotton (పత్తి)',
        weight: '40 Quintals',
        mandi: 'Warangal Enamamula APMC Yard (Gate 3)',
        fare: '1850',
        status: 'en_route',
        bookedAt: new Date().toISOString()
      }));
      if (typeof openScreen === 'function') openScreen('driver_dashboard', null);
      const c = document.getElementById('screen-container');
      if (c) c.scrollTop = 0;
    }""")
    time.sleep(1.5)
    page.screenshot(path=os.path.join(artifact_dir, "v5_driver_active_trip.png"))
    print("Captured: v5_driver_active_trip.png")

    # === 3. DRIVER PAYMENT COLLECTION SCREEN ===
    page.evaluate("""() => {
      if (typeof driverShowPaymentScreen === 'function') {
        driverShowPaymentScreen('GH-4192', '1850');
      }
    }""")
    time.sleep(0.8)
    page.screenshot(path=os.path.join(artifact_dir, "v5_driver_payment_screen.png"))
    print("Captured: v5_driver_payment_screen.png")

    # Close payment modal
    page.evaluate("""() => {
      const m = document.getElementById('gh-driver-payment-modal');
      if (m) m.remove();
    }""")
    time.sleep(0.3)

    # === 4. DRIVER COCKPIT — OFFLINE STATE ===
    page.evaluate("""() => {
      localStorage.setItem('gh_driver_online', 'false');
      localStorage.removeItem('nukrop_active_trip');
      if (typeof openScreen === 'function') openScreen('driver_dashboard', null);
      const c = document.getElementById('screen-container');
      if (c) c.scrollTop = 0;
    }""")
    time.sleep(1.5)
    page.screenshot(path=os.path.join(artifact_dir, "v5_driver_offline.png"))
    print("Captured: v5_driver_offline.png")

    # === 5. FARMER — GRAMHAUL PHASE 1 (BOOKING) ===
    page.evaluate("""() => {
      localStorage.setItem('gh_driver_online', 'true');
      finishLoginAndEnterDashboard('farmer');
      localStorage.removeItem('nukrop_active_trip');
      if (typeof openScreen === 'function') openScreen('gramhaul', null);
      const c = document.getElementById('screen-container');
      if (c) c.scrollTop = 0;
    }""")
    time.sleep(1.5)
    page.screenshot(path=os.path.join(artifact_dir, "v5_farmer_gramhaul_phase1.png"))
    print("Captured: v5_farmer_gramhaul_phase1.png")

    # === 6. FARMER — GRAMHAUL PHASE 2 (ACTIVE BOOKING) ===
    page.evaluate("""() => {
      if (typeof executeGramhaulBookingTransition === 'function') executeGramhaulBookingTransition();
      const c = document.getElementById('screen-container');
      if (c) c.scrollTop = 200;
    }""")
    time.sleep(1.0)
    page.screenshot(path=os.path.join(artifact_dir, "v5_farmer_gramhaul_phase2.png"))
    print("Captured: v5_farmer_gramhaul_phase2.png")

    # === 7. FARMER — HOME DASHBOARD ===
    page.evaluate("""() => {
      if (typeof openScreen === 'function') openScreen('home', document.getElementById('tab-home'));
      const c = document.getElementById('screen-container');
      if (c) c.scrollTop = 0;
    }""")
    time.sleep(1.5)
    page.screenshot(path=os.path.join(artifact_dir, "v5_farmer_home.png"))
    print("Captured: v5_farmer_home.png")

    browser.close()
    print("\nAll 7 Uber-grade driver app screenshots captured successfully!")
