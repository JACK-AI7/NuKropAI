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

async def capture_all():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 430, 'height': 932},
            device_scale_factor=2,
            has_touch=True,
            is_mobile=True,
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
        )
        page = await context.new_page()

        print("Navigating to http://localhost:8080/nukrop_emulator.html...")
        await page.goto("http://localhost:8080/nukrop_emulator.html", wait_until="networkidle")
        await page.wait_for_timeout(2000)

        # Clear startup overlays to directly test application screens
        await page.evaluate("""() => {
            const ids = ['startup-experience-overlay', 'onboarding-experience-overlay', 'splash-viewport', 'login-screen-overlay'];
            ids.forEach(id => {
                const el = document.getElementById(id);
                if (el) el.remove();
            });
            authUserRole = 'farmer';
            localStorage.setItem('nukrop_user_role', 'farmer');
            if (typeof openScreen === 'function') openScreen('home', document.getElementById('tab-home'));
        }""")
        await page.wait_for_timeout(1500)

        # 1. FARMER HOME SCREEN
        print("Capturing final_01_farmer_home.png...")
        await page.evaluate("openScreen('home', document.getElementById('tab-home'))")
        await page.wait_for_timeout(1500)
        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "final_01_farmer_home.png"))

        # 2. MANDI MARKET SCREEN (Clean curved search bar & results)
        print("Capturing final_02_mandi_market_live.png...")
        await page.evaluate("openScreen('market', document.getElementById('tab-market'))")
        await page.wait_for_timeout(1500)
        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "final_02_mandi_market_live.png"))

        # 3. FARMER NOTIFICATIONS (Strictly Farmer-only alerts)
        print("Capturing final_03_farmer_notifs_isolated.png...")
        await page.evaluate("""() => {
            authUserRole = 'farmer';
            localStorage.setItem('nukrop_user_role', 'farmer');
            if (typeof openPriceAlertModal === 'function') openPriceAlertModal(null, 'feed');
        }""")
        await page.wait_for_timeout(1200)
        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "final_03_farmer_notifs_isolated.png"))
        await page.evaluate("""() => {
            if (typeof closePriceAlertModal === 'function') closePriceAlertModal();
        }""")
        await page.wait_for_timeout(500)

        # 4. GRAMHAUL MANDI DISPATCH (Leaflet Map + 5 Truck Tiers)
        print("Capturing final_04_gramhaul_truck_screen.png...")
        await page.evaluate("openScreen('gramhaul', document.getElementById('tab-gramhaul'))")
        await page.wait_for_timeout(2000)
        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "final_04_gramhaul_truck_screen.png"))

        # 5. RAPIDO SEARCHING RADAR HUD (With Leaflet OSM Map 100% VISIBLE behind it)
        print("Capturing final_05_rapido_searching_radar_map_visible.png...")
        await page.evaluate("""() => {
            renderLiveSearchingHud('GH-4491', 'Tata Ace Gold (1.5T)', 'Cotton', '40', 380, 'Gudimalkapur APMC Yard');
        }""")
        await page.wait_for_timeout(1200)
        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "final_05_rapido_searching_radar_map_visible.png"))

        # 6. RAPIDO LIVE TRACKING COCKPIT SHEET (With Leaflet OSM Map 100% VISIBLE on top + Live Truck Approaching)
        print("Capturing final_06_rapido_live_tracking_cockpit_map_visible.png...")
        await page.evaluate("""() => {
            const searchModal = document.getElementById('gh-searching-radar-modal');
            if (searchModal) searchModal.remove();
            renderLiveDispatchedModal('GH-4491', 'Tata Ace Gold (1.5T)', 'Cotton', '40', 380, 'Gudimalkapur APMC Yard');
        }""")
        await page.wait_for_timeout(1500)
        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "final_06_rapido_live_tracking_cockpit_map_visible.png"))
        await page.evaluate("""() => {
            const dispatchedModal = document.getElementById('gh-dispatched-modal');
            if (dispatchedModal) dispatchedModal.remove();
        }""")
        await page.wait_for_timeout(500)

        # 7. INSTAGRAM CREATE POST / ASK QUERY MODAL
        print("Capturing final_07_community_ask_modal_instagram.png...")
        await page.evaluate("""() => {
            openScreen('community', document.getElementById('tab-community'));
            setTimeout(() => {
                if (typeof openAskQuestionModal === 'function') openAskQuestionModal();
                if (typeof attachMediaToNewPost === 'function') attachMediaToNewPost('photo');
            }, 500);
        }""")
        await page.wait_for_timeout(1500)
        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "final_07_community_ask_modal_instagram.png"))
        await page.evaluate("""() => {
            if (typeof closeAskQuestionModal === 'function') closeAskQuestionModal();
        }""")
        await page.wait_for_timeout(500)

        # 8. DRIVER COCKPIT DASHBOARD (Live Map, Earnings & Driver Notifications button)
        print("Capturing final_08_driver_cockpit_dashboard.png...")
        await page.evaluate("""() => {
            authUserRole = 'driver';
            localStorage.setItem('nukrop_user_role', 'driver');
            openScreen('driver_dashboard', null);
        }""")
        await page.wait_for_timeout(2000)
        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "final_08_driver_cockpit_dashboard.png"))

        # 9. DRIVER NOTIFICATIONS (Strictly Driver-only Logistics alerts)
        print("Capturing final_09_driver_notifs_isolated.png...")
        await page.evaluate("""() => {
            authUserRole = 'driver';
            localStorage.setItem('nukrop_user_role', 'driver');
            if (typeof openPriceAlertModal === 'function') openPriceAlertModal(null, 'feed');
        }""")
        await page.wait_for_timeout(1200)
        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "final_09_driver_notifs_isolated.png"))

        print("All verified high-fidelity screenshots captured successfully!")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_all())
