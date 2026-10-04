import asyncio
import os
import sys

from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

ARTIFACT_DIR = r"C:\Users\bjasw\.gemini\antigravity\brain\36944d22-a0e5-4ba9-95b4-639674444ec9"

async def capture_scrolled():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 412, 'height': 915},
            device_scale_factor=2
        )
        page = await context.new_page()
        await page.goto("http://localhost:8080/app/src/main/assets/index.html", wait_until="networkidle")
        await page.wait_for_timeout(1000)

        await page.evaluate("""() => {
            localStorage.setItem('nukrop_onboarding_completed', 'true');
            localStorage.setItem('nukrop_language', 'en');
            localStorage.setItem('nukrop_user_role', 'farmer');
            const ov = document.getElementById('startup-experience-overlay');
            if (ov) ov.remove();
        }""")
        await page.wait_for_timeout(400)

        await page.evaluate("openScreen('gramhaul')")
        await page.wait_for_timeout(800)

        # Scroll the booking button into view
        print("Scrolling booking button into view...")
        await page.evaluate("""() => {
            const btn = document.getElementById('gh-confirm-booking-btn');
            if (btn) {
                btn.scrollIntoView({ behavior: 'instant', block: 'center' });
            }
        }""")
        await page.wait_for_timeout(600)

        s_path = os.path.join(ARTIFACT_DIR, "v3_09_gramhaul_scrolled_trucks.png")
        await page.screenshot(path=s_path)
        print(f"Captured: {s_path}")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(capture_scrolled())
