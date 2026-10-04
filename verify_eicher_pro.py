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

async def test_eicher_pro():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 412, 'height': 892},
            device_scale_factor=2,
            has_touch=True,
            is_mobile=True,
            user_agent="Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
        )
        page = await context.new_page()

        print("[1] Opening GramHaul Screen 1...")
        await page.goto("http://localhost:8080/app/src/main/assets/index.html", wait_until="networkidle")
        await page.wait_for_timeout(1000)

        # Clear startup overlays and open GramHaul
        await page.evaluate("""() => {
            const ids = ['startup-experience-overlay', 'onboarding-experience-overlay', 'splash-viewport', 'login-screen-overlay'];
            ids.forEach(id => {
                const el = document.getElementById(id);
                if (el) el.remove();
            });
            openScreen('gramhaul');
        }""")
        await page.wait_for_timeout(800)

        # Select Tier 5 (Eicher Pro) and scroll down
        await page.evaluate("""() => {
            selectGramhaulTruckTier(5);
            const container = document.querySelector('#screen-body div[style*="overflow-y:auto"], #screen-body div[style*="overflow-y: auto"]');
            if (container) {
                container.scrollTop = 320;
            }
        }""")
        await page.wait_for_timeout(500)

        snap_s1_t5 = os.path.join(ARTIFACT_DIR, "screen1_tier5_eicher_pro.png")
        await page.screenshot(path=snap_s1_t5)
        print("  -> Screen 1 Tier 5 saved:", snap_s1_t5)

        # Dispatch Tier 5
        print("[2] Dispatching Tier 5 Eicher Pro...")
        await page.evaluate("""() => {
            executeRealGramhaulDispatch();
        }""")
        await page.wait_for_timeout(2200)

        snap_s2_t5 = os.path.join(ARTIFACT_DIR, "screen2_tier5_eicher_pro_dispatched.png")
        await page.screenshot(path=snap_s2_t5)
        print("  -> Screen 2 Tier 5 Dispatched saved:", snap_s2_t5)

        await browser.close()
        print("\nEICHER PRO VERIFICATION COMPLETE!")

asyncio.run(test_eicher_pro())
