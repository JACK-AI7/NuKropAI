import asyncio
import os
from playwright.async_api import async_playwright

SCREENSHOT_DIR = r"C:\Users\bjasw\.gemini\antigravity\brain\36944d22-a0e5-4ba9-95b4-639674444ec9"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

async def run_verification():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 430, "height": 932},
            device_scale_factor=2,
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15"
        )
        page = await context.new_page()

        print("Navigating to app...")
        await page.goto("http://localhost:8080/nukrop_emulator.html")
        await page.wait_for_timeout(1000)

        # 0. Clear onboarding/splash
        await page.evaluate("""() => {
            if (typeof finishLoginAndEnterDashboard === 'function') finishLoginAndEnterDashboard('farmer');
            const overlays = ['startup-experience-overlay', 'onboarding-experience-overlay', 'permission-experience-overlay', 'splash-viewport', 'login-screen-overlay'];
            overlays.forEach(id => {
                const el = document.getElementById(id);
                if (el) el.remove();
            });
            if (typeof openScreen === 'function') openScreen('home');
        }""")
        await page.wait_for_timeout(500)

        # 1. Capture Farmer Home
        await page.screenshot(path=os.path.join(SCREENSHOT_DIR, "v2_01_farmer_home.png"))
        print("Captured 01_farmer_home")

        # 2. Open Gramhaul Selector screen
        await page.evaluate("() => openScreen('gramhaul')")
        await page.wait_for_timeout(1000)
        await page.screenshot(path=os.path.join(SCREENSHOT_DIR, "v2_02_gramhaul_selector_tier1.png"))
        print("Captured 02_gramhaul_selector_tier1")

        # 3. Select Tier 2 (Mahindra Bolero Maxi) to verify dynamic map update
        await page.evaluate("() => selectGramhaulTruckTier(2)")
        await page.wait_for_timeout(600)
        await page.screenshot(path=os.path.join(SCREENSHOT_DIR, "v2_03_gramhaul_selector_tier2_bolero.png"))
        print("Captured 03_gramhaul_selector_tier2_bolero")

        # 4. Select Tier 3 (Ashok Leyland Dost+)
        await page.evaluate("() => selectGramhaulTruckTier(3)")
        await page.wait_for_timeout(600)
        await page.screenshot(path=os.path.join(SCREENSHOT_DIR, "v2_04_gramhaul_selector_tier3_dost.png"))
        print("Captured 04_gramhaul_selector_tier3_dost")

        # 5. Switch back to Tier 1 and click "Request Mandi Truck Now" -> Gramhaul Tracking Screen (Phase 1 Searching Radar)
        await page.evaluate("() => { selectGramhaulTruckTier(1); executeRealGramhaulDispatch(); }")
        await page.wait_for_timeout(600)
        await page.screenshot(path=os.path.join(SCREENSHOT_DIR, "v2_05_tracking_searching_radar.png"))
        print("Captured 05_tracking_searching_radar")

        # 6. Wait for auto-transition to Phase 2 Live Dispatched Rapido Cockpit Sheet (1.8s timeout)
        await page.wait_for_timeout(2000)
        await page.screenshot(path=os.path.join(SCREENSHOT_DIR, "v2_06_tracking_live_dispatched_cockpit.png"))
        print("Captured 06_tracking_live_dispatched_cockpit")

        # 7. Test In-App Secure Call modal
        await page.evaluate("() => triggerDriverCall('Suresh Yadav', '+91 94401 55667')")
        await page.wait_for_timeout(500)
        await page.screenshot(path=os.path.join(SCREENSHOT_DIR, "v2_07_driver_live_call_modal.png"))
        print("Captured 07_driver_live_call_modal")

        # Close Call Modal
        await page.evaluate("() => { const el = document.getElementById('driver-live-call-modal'); if (el) el.remove(); }")
        await page.wait_for_timeout(300)

        # 8. Test In-App Driver Live Chat Modal
        await page.evaluate("() => openDriverLiveChatModal('Suresh Yadav', 'TS 03 UB 4491')")
        await page.wait_for_timeout(500)
        await page.screenshot(path=os.path.join(SCREENSHOT_DIR, "v2_08_driver_live_chat_modal.png"))
        print("Captured 08_driver_live_chat_modal")

        # Close Chat Modal
        await page.evaluate("() => { const el = document.getElementById('driver-live-chat-modal'); if (el) el.remove(); }")
        await page.wait_for_timeout(300)

        # 9. Test Driver Cockpit Dashboard (Driver Mode Isolation)
        await page.evaluate("() => { switchUserRole('driver'); openScreen('driver_dashboard'); }")
        await page.wait_for_timeout(1000)
        await page.screenshot(path=os.path.join(SCREENSHOT_DIR, "v2_09_driver_dashboard_cockpit.png"))
        print("Captured 09_driver_dashboard_cockpit")

        # 10. Test Driver Isolated Notifications Modal
        await page.evaluate("() => openPriceAlertModal(null, 'feed')")
        await page.wait_for_timeout(500)
        await page.screenshot(path=os.path.join(SCREENSHOT_DIR, "v2_10_driver_notifications_isolated.png"))
        print("Captured 10_driver_notifications_isolated")

        # Close Notifications Modal
        await page.evaluate("() => { const el = document.getElementById('price-alert-modal'); if (el) el.remove(); }")
        await page.wait_for_timeout(300)

        # 11. Switch back to Farmer mode and open Farmer Notifications Modal
        await page.evaluate("() => { switchUserRole('farmer'); openScreen('home'); openPriceAlertModal(null, 'feed'); }")
        await page.wait_for_timeout(500)
        await page.screenshot(path=os.path.join(SCREENSHOT_DIR, "v2_11_farmer_notifications_isolated.png"))
        print("Captured 11_farmer_notifications_isolated")

        await browser.close()
        print("ALL VERIFICATION SCREENSHOTS CAPTURED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(run_verification())
