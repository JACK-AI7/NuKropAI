import asyncio
import os
import shutil
from playwright.async_api import async_playwright

async def capture_all_screens():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 390, "height": 844})
        
        file_url = "file:///" + os.path.abspath("nukrop_emulator.html").replace("\\", "/")
        await page.goto(file_url)
        await page.wait_for_timeout(1000)

        # 1. Splash Screen
        await page.screenshot(path="app_01_splash.png")
        print("Captured app_01_splash.png")

        # 2. Language Selection Screen
        await page.evaluate("""
            const el = document.getElementById('startup-experience-overlay');
            if (el && typeof renderLanguageSelectionScreen === 'function') {
                renderLanguageSelectionScreen(el);
            }
        """)
        await page.wait_for_timeout(400)
        await page.screenshot(path="app_02_language.png")
        print("Captured app_02_language.png")

        # 3. Onboarding Carousel
        await page.evaluate("""
            const el = document.getElementById('startup-experience-overlay');
            if (el && typeof renderOnboardingCarousel === 'function') {
                renderOnboardingCarousel(el);
            }
        """)
        await page.wait_for_timeout(400)
        await page.screenshot(path="app_03_onboarding.png")
        print("Captured app_03_onboarding.png")

        # 4. Farmer Login Screen
        await page.evaluate("""
            const el = document.getElementById('startup-experience-overlay');
            if (el && typeof renderLoginScreen === 'function') {
                authUserRole = 'farmer';
                renderLoginScreen(el);
            }
        """)
        await page.wait_for_timeout(400)
        await page.screenshot(path="app_04_farmer_login.png")
        print("Captured app_04_farmer_login.png")

        # 5. Driver Login Screen
        await page.evaluate("""
            const el = document.getElementById('startup-experience-overlay');
            if (el && typeof renderLoginScreen === 'function') {
                authUserRole = 'driver';
                renderLoginScreen(el);
            }
        """)
        await page.wait_for_timeout(400)
        await page.screenshot(path="app_05_driver_login.png")
        print("Captured app_05_driver_login.png")

        # 6. Google Account Chooser Modal
        await page.evaluate("openInAppGoogleAuthModal()")
        await page.wait_for_timeout(400)
        await page.screenshot(path="app_06_google_account_chooser.png")
        print("Captured app_06_google_account_chooser.png")

        # Remove overlays & dismiss toasts for clean view of all screens
        await page.evaluate("""
            const modal = document.getElementById('google-auth-modal');
            if (modal) modal.remove();
            const overlay = document.getElementById('startup-experience-overlay');
            if (overlay) overlay.remove();
            if (typeof dismissPushToast === 'function') dismissPushToast();
            const toast = document.getElementById('global-push-toast');
            if (toast) toast.style.display = 'none';
        """)

        screens = [
            ("home", "app_07_farmer_home.png"),
            ("scanner", "app_09_crop_scanner.png"),
            ("market", "app_10_mandi_market.png"),
            ("gramhaul", "app_11_gramhaul_farmer.png"),
            ("agristack", "app_12_agristack_passport.png"),
            ("equipment", "app_13_equipment_rental.png"),
            ("loan", "app_14_kcc_loans.png"),
            ("khata", "app_15_farm_khata.png"),
            ("chat", "app_16_ai_advisor_chat.png"),
            ("bioshield", "app_17_bioshield_radar.png"),
            ("biorx", "app_18_biorx_organic.png"),
            ("calc_fert", "app_19_calculator_fertilizer.png"),
            ("calc_pest", "app_20_calculator_pesticide.png"),
            ("calc_budget", "app_21_calculator_budget.png"),
            ("community", "app_22_community_forum.png"),
            ("profile", "app_23_farmer_profile.png"),
        ]

        for screen_key, filename in screens:
            await page.evaluate(f"openScreen('{screen_key}', null);")
            await page.wait_for_timeout(600)
            await page.screenshot(path=filename)
            print(f"Captured {filename} ({screen_key})")

        # Crop Selection Modal
        await page.evaluate("openScreen('home', null); openCropModal();")
        await page.wait_for_timeout(400)
        await page.screenshot(path="app_08_crop_selection_modal.png")
        print("Captured app_08_crop_selection_modal.png")

        # Close Crop Modal and Open Driver Cockpit
        await page.evaluate("""
            if (typeof closeCropModal === 'function') closeCropModal();
            const m = document.getElementById('crop-modal');
            if (m) m.classList.remove('open');
            authUserRole = 'driver';
            localStorage.setItem('nukrop_user_role', 'driver');
            openScreen('driver_dashboard', null);
        """)
        await page.wait_for_timeout(800)
        await page.screenshot(path="app_24_driver_cockpit.png")
        print("Captured app_24_driver_cockpit.png")

        await browser.close()
        print("All 24 screenshots captured successfully!")

        # Copy all to artifact directory
        art_dir = r"C:\Users\bjasw\.gemini\antigravity\brain\36944d22-a0e5-4ba9-95b4-639674444ec9"
        import glob
        for f in glob.glob("app_*.png"):
            dest = os.path.join(art_dir, f)
            shutil.copy(f, dest)
            print(f"Copied {f} to {dest}")

if __name__ == "__main__":
    asyncio.run(capture_all_screens())
