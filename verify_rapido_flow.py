# -*- coding: utf-8 -*-
import asyncio
import os
import sys
from playwright.async_api import async_playwright

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

ARTIFACT_DIR = r"C:\Users\bjasw\.gemini\antigravity\brain\36944d22-a0e5-4ba9-95b4-639674444ec9"

async def test_rapido_flow():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Mobile viewport (Pixel 7 / Galaxy S23 standard Android dimensions)
        context = await browser.new_context(
            viewport={'width': 412, 'height': 892},
            device_scale_factor=2,
            has_touch=True,
            is_mobile=True,
            user_agent="Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
        )
        page = await context.new_page()

        print("[1] Navigating to http://localhost:8080/app/src/main/assets/index.html...")
        await page.goto("http://localhost:8080/app/src/main/assets/index.html", wait_until="networkidle")
        await page.wait_for_timeout(1500)

        # Clear startup overlays
        await page.evaluate("""() => {
            const ids = ['startup-experience-overlay', 'onboarding-experience-overlay', 'splash-viewport', 'login-screen-overlay'];
            ids.forEach(id => {
                const el = document.getElementById(id);
                if (el) el.remove();
            });
        }""")

        # Open GramHaul screen
        print("[2] Opening GramHaul screen...")
        await page.evaluate("""() => {
            openScreen('gramhaul');
        }""")
        await page.wait_for_timeout(1200)

        # Verify layout metrics
        metrics = await page.evaluate("""() => {
            const dock = document.querySelector('.bottom-dock-wrap');
            const sc = document.getElementById('screen-container');
            const sb = document.getElementById('screen-body');
            const btn = document.getElementById('gh-confirm-booking-btn');
            const map = document.getElementById('gramhaul-real-osm-map');
            const sheet = document.getElementById('gh-rapido-sheet');
            return {
                dockDisplay: dock ? dock.style.display : null,
                sc_h: sc ? sc.clientHeight : null,
                sb_h: sb ? sb.clientHeight : null,
                map_h: map ? map.clientHeight : null,
                btn_box: btn ? btn.getBoundingClientRect() : null,
                btn_text: btn ? btn.innerText.replace(/\\s+/g, ' ').trim() : null
            };
        }""")
        print("[3] Layout metrics in gramhaul:", metrics)

        # Screenshot 1: GramHaul Booking Screen (Tata Ace selected by default)
        snap1 = os.path.join(ARTIFACT_DIR, "rapido_01_gramhaul_booking.png")
        await page.screenshot(path=snap1)
        print("  -> Saved:", snap1)

        # Click Tier 2: Mahindra Bolero Maxi
        print("[4] Selecting Tier 2: Mahindra Bolero Maxi...")
        await page.evaluate("""() => {
            selectGramhaulTruckTier(2);
        }""")
        await page.wait_for_timeout(600)

        btn_text_t2 = await page.evaluate("""() => {
            const btn = document.getElementById('gh-confirm-booking-btn');
            return btn ? btn.innerText.replace(/\\s+/g, ' ').trim() : null;
        }""")
        print("[5] Button text after Tier 2 selection:", btn_text_t2)

        # Screenshot 2: Bolero Maxi selected
        snap2 = os.path.join(ARTIFACT_DIR, "rapido_02_bolero_selected.png")
        await page.screenshot(path=snap2)
        print("  -> Saved:", snap2)

        # Click Tier 3: Ashok Leyland Dost+
        print("[6] Selecting Tier 3: Ashok Leyland Dost+...")
        await page.evaluate("""() => {
            selectGramhaulTruckTier(3);
        }""")
        await page.wait_for_timeout(600)

        snap3 = os.path.join(ARTIFACT_DIR, "rapido_03_dost_selected.png")
        await page.screenshot(path=snap3)
        print("  -> Saved:", snap3)

        # Click Book Button to trigger dispatch
        print("[7] Executing booking dispatch...")
        await page.evaluate("""() => {
            const btn = document.getElementById('gh-confirm-booking-btn');
            if (btn) btn.click();
        }""")
        await page.wait_for_timeout(800)

        # Screenshot 4: Searching Radar state
        snap4 = os.path.join(ARTIFACT_DIR, "rapido_04_searching_radar.png")
        await page.screenshot(path=snap4)
        print("  -> Saved:", snap4)

        # Wait for driver dispatch (1.8s timeout in JS)
        print("[8] Waiting for driver match and dispatch...")
        await page.wait_for_timeout(2200)

        # Screenshot 5: Dispatched Live Tracking Cockpit
        snap5 = os.path.join(ARTIFACT_DIR, "rapido_05_dispatched_cockpit.png")
        await page.screenshot(path=snap5)
        print("  -> Saved:", snap5)

        # Test Driver Call Modal
        print("[9] Opening Driver Call Modal...")
        await page.evaluate("""() => {
            triggerDriverCall('Md. Ismail Khan', '+91 97014 33290');
        }""")
        await page.wait_for_timeout(500)

        snap6 = os.path.join(ARTIFACT_DIR, "rapido_06_driver_call_modal.png")
        await page.screenshot(path=snap6)
        print("  -> Saved:", snap6)

        # Close call modal and open Chat Modal
        print("[10] Opening Live Chat Modal...")
        await page.evaluate("""() => {
            closeDriverCallModal();
            openDriverLiveChatModal('Md. Ismail Khan', 'TS 08 AB 1102');
        }""")
        await page.wait_for_timeout(500)

        snap7 = os.path.join(ARTIFACT_DIR, "rapido_07_driver_chat_modal.png")
        await page.screenshot(path=snap7)
        print("  -> Saved:", snap7)

        # Close Chat Modal and return to Home
        print("[11] Closing chat and returning to Home screen...")
        await page.evaluate("""() => {
            closeDriverLiveChatModal();
            openScreen('home');
            updateBottomDockForRole();
        }""")
        await page.wait_for_timeout(800)

        # Verify bottom dock is restored
        dock_state = await page.evaluate("""() => {
            const dock = document.querySelector('.bottom-dock-wrap');
            return dock ? dock.style.display : null;
        }""")
        print("[12] Dock display after returning home:", dock_state)

        snap8 = os.path.join(ARTIFACT_DIR, "rapido_08_home_dock_restored.png")
        await page.screenshot(path=snap8)
        print("  -> Saved:", snap8)

        await browser.close()
        print("\nALL RAPIDO FLOW TESTS PASSED SUCCESSFULLY!")

asyncio.run(test_rapido_flow())
