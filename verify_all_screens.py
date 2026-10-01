import asyncio
from playwright.async_api import async_playwright
import os

async def verify_screens():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 390, "height": 844})
        
        file_url = "file:///" + os.path.abspath("nukrop_emulator.html").replace("\\", "/")
        print(f"Loading {file_url}")
        await page.goto(file_url)
        await page.wait_for_timeout(1000)
        
        # 1. Splash Screen
        await page.screenshot(path="verified_splash.png")
        print("Captured verified_splash.png")
        
        # 2. Language Selection Screen
        await page.evaluate("""
            const el = document.getElementById('startup-experience-overlay');
            if (el && typeof renderLanguageSelectionScreen === 'function') {
                renderLanguageSelectionScreen(el);
            }
        """)
        await page.wait_for_timeout(500)
        await page.screenshot(path="verified_language.png")
        print("Captured verified_language.png")
        
        # 3. Onboarding Slide Screen
        await page.evaluate("""
            const el = document.getElementById('startup-experience-overlay');
            if (el && typeof renderOnboardingCarousel === 'function') {
                renderOnboardingCarousel(el);
            }
        """)
        await page.wait_for_timeout(500)
        await page.screenshot(path="verified_onboarding.png")
        print("Captured verified_onboarding.png")
        
        # 4. Farmer Login Screen
        await page.evaluate("""
            const el = document.getElementById('startup-experience-overlay');
            if (el && typeof renderLoginScreen === 'function') {
                authUserRole = 'farmer';
                renderLoginScreen(el);
            }
        """)
        await page.wait_for_timeout(500)
        await page.screenshot(path="verified_farmer_login.png")
        print("Captured verified_farmer_login.png")
        
        # 5. Truck Driver Login Screen
        await page.evaluate("""
            const el = document.getElementById('startup-experience-overlay');
            if (el && typeof renderLoginScreen === 'function') {
                authUserRole = 'driver';
                renderLoginScreen(el);
            }
        """)
        await page.wait_for_timeout(500)
        await page.screenshot(path="verified_driver_login.png")
        print("Captured verified_driver_login.png")
        
        # 6. Google Auth Modal
        await page.evaluate("if (typeof openGoogleAuthModal === 'function') openGoogleAuthModal()")
        await page.wait_for_timeout(500)
        await page.screenshot(path="verified_google_modal.png")
        print("Captured verified_google_modal.png")
        
        # 7. Farmer Home Dashboard
        await page.evaluate("""
            if (typeof closeGoogleAuthModal === 'function') closeGoogleAuthModal();
            if (typeof dismissStartupToHome === 'function') dismissStartupToHome();
            else if (typeof openScreen === 'function') openScreen('home');
        """)
        await page.wait_for_timeout(1000)
        await page.screenshot(path="verified_farmer_home.png")
        print("Captured verified_farmer_home.png")
        
        # 8. Driver Cockpit Dashboard
        await page.evaluate("if (typeof openScreen === 'function') openScreen('driver_cockpit');")
        await page.wait_for_timeout(1000)
        await page.screenshot(path="verified_driver_cockpit.png")
        print("Captured verified_driver_cockpit.png")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify_screens())
