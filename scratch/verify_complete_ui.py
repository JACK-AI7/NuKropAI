import asyncio
import os
import sys

from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

ARTIFACT_DIR = r"C:\Users\bjasw\.gemini\antigravity\brain\36944d22-a0e5-4ba9-95b4-639674444ec9"

async def run_visual_verification():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Mobile viewport matching modern smartphone (Pixel 7 / iPhone 14 Pro style: 412x915)
        context = await browser.new_context(
            viewport={'width': 412, 'height': 915},
            device_scale_factor=2
        )
        page = await context.new_page()

        print("Navigating to local server...")
        await page.goto("http://localhost:8080/app/src/main/assets/index.html", wait_until="networkidle")
        await page.wait_for_timeout(1000)

        # Bypass onboarding overlay
        print("Dismissing onboarding overlay if present...")
        await page.evaluate("""() => {
            localStorage.setItem('nukrop_onboarding_completed', 'true');
            localStorage.setItem('nukrop_language', 'en');
            localStorage.setItem('nukrop_user_role', 'farmer');
            const ov = document.getElementById('startup-experience-overlay');
            if (ov) ov.remove();
        }""")
        await page.wait_for_timeout(500)

        # 1. Open GramHaul Screen 1
        print("Opening GramHaul Screen 1...")
        await page.evaluate("openScreen('gramhaul')")
        await page.wait_for_timeout(1000)

        # Capture Screen 1
        s1_path = os.path.join(ARTIFACT_DIR, "v3_01_gramhaul_screen1_verified.png")
        await page.screenshot(path=s1_path)
        print(f"Captured: {s1_path}")

        # 2. Open Crop Selector Modal
        print("Opening Crop Selector Modal...")
        await page.evaluate("openGramhaulCropSelectorModal()")
        await page.wait_for_timeout(600)

        s_crop_path = os.path.join(ARTIFACT_DIR, "v3_02_crop_selector_modal_verified.png")
        await page.screenshot(path=s_crop_path)
        print(f"Captured: {s_crop_path}")

        # Select Chilli
        print("Selecting Chilli crop...")
        await page.evaluate("selectGramhaulCrop('chilli', 'Teja Red Chilli (ఎండు మిర్చి / सूखी मिर्च)')")
        await page.wait_for_timeout(600)

        s_chilli_path = os.path.join(ARTIFACT_DIR, "v3_03_crop_selected_chilli.png")
        await page.screenshot(path=s_chilli_path)
        print(f"Captured: {s_chilli_path}")

        # 3. Trigger Booking -> Screen 2 Searching State
        print("Triggering Mandi Truck Booking...")
        await page.evaluate("executeRealGramhaulDispatch()")
        await page.wait_for_timeout(700)

        s_search_path = os.path.join(ARTIFACT_DIR, "v3_04_screen2_searching_verified.png")
        await page.screenshot(path=s_search_path)
        print(f"Captured: {s_search_path}")

        # 4. Wait for Dispatched State (timeout triggers at 1.8s)
        print("Waiting for driver dispatch...")
        await page.wait_for_timeout(2200)

        s_dispatch_path = os.path.join(ARTIFACT_DIR, "v3_05_screen2_dispatched_verified.png")
        await page.screenshot(path=s_dispatch_path)
        print(f"Captured: {s_dispatch_path}")

        # 5. Open Trip Details Drawer
        print("Opening Trip Details drawer...")
        await page.evaluate("toggleTripDetailsDrawer()")
        await page.wait_for_timeout(500)

        s_drawer_path = os.path.join(ARTIFACT_DIR, "v3_06_screen2_drawer_opened_verified.png")
        await page.screenshot(path=s_drawer_path)
        print(f"Captured: {s_drawer_path}")

        # 6. Test Driver Call Modal
        print("Testing Driver Call Modal...")
        await page.evaluate("triggerDriverCall('Suresh Goud', '+91 98480 22338')")
        await page.wait_for_timeout(600)

        s_call_path = os.path.join(ARTIFACT_DIR, "v3_07_driver_call_modal_verified.png")
        await page.screenshot(path=s_call_path)
        print(f"Captured: {s_call_path}")

        # End call
        await page.evaluate("endDriverLiveCall('driver-live-call-modal')")
        await page.wait_for_timeout(400)

        # 7. Test Driver Chat Modal
        print("Testing Driver Chat Modal...")
        await page.evaluate("openDriverLiveChatModal('Suresh Goud', 'TS 03 UB 4491')")
        await page.wait_for_timeout(600)

        s_chat_path = os.path.join(ARTIFACT_DIR, "v3_08_driver_chat_modal_verified.png")
        await page.screenshot(path=s_chat_path)
        print(f"Captured: {s_chat_path}")

        await browser.close()
        print("\nAll verification screenshots captured successfully!")

if __name__ == '__main__':
    asyncio.run(run_visual_verification())
