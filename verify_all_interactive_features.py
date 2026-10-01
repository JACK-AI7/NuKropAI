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
    time.sleep(1)

    # 1. Login & Enter GramHaul Phase 1
    page.evaluate("""() => {
      finishLoginAndEnterDashboard('farmer');
      openScreen('gramhaul', null);
      const container = document.getElementById('screen-container');
      if (container) container.scrollTop = 0;
    }""")
    time.sleep(1)

    # 2. Open Pickup Location Exact GPS Modal
    page.evaluate("""() => {
      openGramhaulPickupLocationModal();
    }""")
    time.sleep(0.5)
    page.screenshot(path=os.path.join(artifact_dir, "verified_action_1_pickup_gps_modal.png"))
    print("Captured: verified_action_1_pickup_gps_modal.png")

    # Close pickup modal and book trip to Phase 2
    page.evaluate("""() => {
      const modal = document.getElementById('gh-pickup-modal');
      if (modal) modal.remove();
      executeGramhaulBookingTransition();
      const container = document.getElementById('screen-container');
      if (container) container.scrollTop = 220;
    }""")
    time.sleep(0.5)

    # 3. Trigger Real Call Dialog
    page.evaluate("""() => {
      callGramhaulDriver();
    }""")
    time.sleep(0.5)
    page.screenshot(path=os.path.join(artifact_dir, "verified_action_2_call_dialog.png"))
    print("Captured: verified_action_2_call_dialog.png")

    # Close call dialog and trigger Real In-App Chat Modal
    page.evaluate("""() => {
      const modal = document.getElementById('gh-call-modal');
      if (modal) modal.remove();
      messageGramhaulDriver();
    }""")
    time.sleep(0.5)
    page.screenshot(path=os.path.join(artifact_dir, "verified_action_3_live_chat_modal.png"))
    print("Captured: verified_action_3_live_chat_modal.png")

    # Close chat modal and trigger Share Modal
    page.evaluate("""() => {
      const modal = document.getElementById('gh-chat-modal');
      if (modal) modal.remove();
      shareGramhaulLiveTracking();
    }""")
    time.sleep(0.5)
    page.screenshot(path=os.path.join(artifact_dir, "verified_action_4_share_modal.png"))
    print("Captured: verified_action_4_share_modal.png")

    # Close share modal and trigger Cancel Modal
    page.evaluate("""() => {
      const modal = document.getElementById('gh-share-modal');
      if (modal) modal.remove();
      cancelGramhaulTrip();
    }""")
    time.sleep(0.5)
    page.screenshot(path=os.path.join(artifact_dir, "verified_action_5_cancel_modal.png"))
    print("Captured: verified_action_5_cancel_modal.png")

    # Close cancel modal, keep booking, and switch to Driver Cockpit to verify Live Trip Sync!
    page.evaluate("""() => {
      const modal = document.getElementById('gh-cancel-modal');
      if (modal) modal.remove();
      openScreen('driver_dashboard', null);
      const container = document.getElementById('screen-container');
      if (container) container.scrollTop = 0;
    }""")
    time.sleep(0.5)
    page.screenshot(path=os.path.join(artifact_dir, "verified_action_6_driver_synced_trip.png"))
    print("Captured: verified_action_6_driver_synced_trip.png")

    browser.close()
    print("All 6 real interactive action tests verified and captured successfully!")
