import asyncio, os
from playwright.async_api import async_playwright

ARTIFACTS_DIR = r"C:\Users\bjasw\.gemini\antigravity\brain\36944d22-a0e5-4ba9-95b4-639674444ec9"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 412, 'height': 892}, device_scale_factor=2)
        page = await context.new_page()

        print("1. Loading emulator...")
        await page.goto("http://localhost:8080/nukrop_emulator.html", wait_until="networkidle")

        # Clear startup overlays
        await page.evaluate("""() => {
            const ids = ['startup-experience-overlay', 'onboarding-experience-overlay', 'splash-viewport', 'login-screen-overlay'];
            ids.forEach(id => { const el = document.getElementById(id); if (el) el.remove(); });
            openScreen('gramhaul');
        }""")
        await page.wait_for_timeout(1000)

        # 1. Screen 1 Map Pin with Tata Ace Gold (Tier 1)
        print("2. Capturing Screen 1 Map with Tata Ace...")
        await page.screenshot(path=os.path.join(ARTIFACTS_DIR, "screen1_map_pin_tata_ace.png"))

        # Switch to Tier 2 (Mahindra Bolero Maxi)
        print("3. Switching to Tier 2 (Bolero Maxi)...")
        await page.evaluate("() => selectGramhaulTruckTier(2)")
        await page.wait_for_timeout(600)
        await page.screenshot(path=os.path.join(ARTIFACTS_DIR, "screen1_map_pin_bolero_maxi.png"))

        # Switch to Tier 5 (Eicher Pro)
        print("4. Switching to Tier 5 (Eicher Pro)...")
        await page.evaluate("() => selectGramhaulTruckTier(5)")
        await page.wait_for_timeout(600)
        await page.screenshot(path=os.path.join(ARTIFACTS_DIR, "screen1_map_pin_eicher_pro.png"))

        # Switch back to Tier 1 and Dispatch
        print("5. Dispatching Tier 1 Tata Ace to test Screen 2 radar and cockpit...")
        await page.evaluate("""() => {
            selectGramhaulTruckTier(1);
            executeRealGramhaulDispatch();
        }""")
        await page.wait_for_timeout(800)
        # Radar searching state screenshot
        await page.screenshot(path=os.path.join(ARTIFACTS_DIR, "screen2_radar_real_truck.png"))

        # Wait for driver acceptance / dispatched state
        await page.wait_for_timeout(1800)
        await page.screenshot(path=os.path.join(ARTIFACTS_DIR, "screen2_dispatched_real_truck.png"))

        # 6. Test Driver Side: Driver Dashboard
        print("6. Opening Driver Dashboard...")
        await page.evaluate("""() => {
            if (window.gramhaulLiveMoveInterval) clearInterval(window.gramhaulLiveMoveInterval);
            localStorage.setItem('nukrop_user_role', 'driver');
            localStorage.setItem('nukrop_driver_name', 'Suresh Yadav');
            localStorage.setItem('nukrop_driver_plate', 'TS 03 UB 4491');
            localStorage.setItem('nukrop_driver_vehicle', 'Tata Ace Gold (1.5 Ton)');
            localStorage.setItem('nukrop_driver_vehicle_img', 'images/trucks/tata_ace.png');
            localStorage.removeItem('nukrop_active_trip');
            localStorage.setItem('gh_driver_tab', 'map');
            openScreen('driver_dashboard');
        }""")
        await page.wait_for_timeout(1000)
        await page.screenshot(path=os.path.join(ARTIFACTS_DIR, "driver_dashboard_map_tab.png"))

        # 7. Open Driver Vehicle Selector Modal
        print("7. Opening Driver Vehicle Selector Modal...")
        await page.evaluate("() => openDriverVehicleSelectorModal()")
        await page.wait_for_timeout(600)
        await page.screenshot(path=os.path.join(ARTIFACTS_DIR, "driver_vehicle_selector_modal.png"))

        # 8. Select Tier 5 (Eicher Pro) on driver side
        print("8. Selecting Eicher Pro in driver vehicle selector...")
        await page.evaluate("() => selectDriverCommercialVehicle(4)") # index 4 is Eicher Pro
        await page.wait_for_timeout(1000)
        await page.screenshot(path=os.path.join(ARTIFACTS_DIR, "driver_dashboard_eicher_switched.png"))

        # 9. Check Driver Profile Tab
        print("9. Checking Driver Profile Tab...")
        await page.evaluate("() => ghDriverNavTo('profile')")
        await page.wait_for_timeout(600)
        await page.screenshot(path=os.path.join(ARTIFACTS_DIR, "driver_profile_tab_vehicle_card.png"))

        print("All test screenshots successfully captured!")
        await browser.close()

asyncio.run(main())
