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

async def test_screen2():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Mobile viewport matching user's device (Pixel 7 / Galaxy S23 standard Android dimensions)
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
        await page.wait_for_timeout(1000)

        # Clear startup overlays and trigger GramHaul booking dispatch
        await page.evaluate("""() => {
            const ids = ['startup-experience-overlay', 'onboarding-experience-overlay', 'splash-viewport', 'login-screen-overlay'];
            ids.forEach(id => {
                const el = document.getElementById(id);
                if (el) el.remove();
            });
            openScreen('gramhaul');
        }""")
        await page.wait_for_timeout(600)

        print("[2] Executing booking dispatch to enter Screen 2 (Tracking)...")
        await page.evaluate("""() => {
            executeRealGramhaulDispatch();
        }""")
        await page.wait_for_timeout(600)

        # Inspect top bar and searching card metrics
        search_metrics = await page.evaluate("""() => {
            const backBtn = document.querySelector('#screen-body button');
            const statusPill = document.getElementById('gh-tracking-top-status-pill');
            const recenterBtn = document.querySelector('#screen-body button:last-of-type');
            const searchCard = document.querySelector('#gh-tracking-bottom-container > div');
            return {
                backBg: backBtn ? getComputedStyle(backBtn).backgroundColor : null,
                backRadius: backBtn ? getComputedStyle(backBtn).borderRadius : null,
                pillBg: statusPill ? getComputedStyle(statusPill).backgroundColor : null,
                cardWidth: searchCard ? searchCard.clientWidth : null,
                cardRadius: searchCard ? getComputedStyle(searchCard).borderRadius : null,
                containerWidth: document.getElementById('gh-tracking-bottom-container')?.clientWidth
            };
        }""")
        print("[3] Searching state metrics:", search_metrics)

        # Screenshot 1: Screen 2 Searching Radar State
        snap_search = os.path.join(ARTIFACT_DIR, "screen2_tracking_searching_verified.png")
        await page.screenshot(path=snap_search)
        print("  -> Saved:", snap_search)

        # Wait for driver match and transition to Dispatched state (1.8s timeout in JS)
        print("[4] Waiting for driver match and dispatched cockpit...")
        await page.wait_for_timeout(2200)

        # Inspect dispatched cockpit metrics
        dispatch_metrics = await page.evaluate("""() => {
            const greenBanner = document.querySelector('#gh-tracking-bottom-container div[style*="background:#22C55E"], #gh-tracking-bottom-container div[style*="background: rgb(34, 197, 94)"]');
            const cockpitCard = document.querySelector('#gh-tracking-bottom-container div[style*="background:#FFFFFF"], #gh-tracking-bottom-container div[style*="background: rgb(255, 255, 255)"]');
            const plateBadge = document.querySelector('#gh-tracking-bottom-container div[style*="background:#FBBF24"], #gh-tracking-bottom-container div[style*="background: rgb(251, 191, 36)"]');
            const otpBox = document.querySelector('#gh-tracking-bottom-container div[style*="background:#FEF3C7"], #gh-tracking-bottom-container div[style*="background: rgb(254, 243, 199)"]');
            return {
                bannerWidth: greenBanner ? greenBanner.clientWidth : null,
                cockpitWidth: cockpitCard ? cockpitCard.clientWidth : null,
                cockpitBg: cockpitCard ? getComputedStyle(cockpitCard).backgroundColor : null,
                plateText: plateBadge ? plateBadge.innerText.trim() : null,
                otpText: otpBox ? otpBox.innerText.replace(/\\s+/g, ' ').trim() : null
            };
        }""")
        print("[5] Dispatched state metrics:", dispatch_metrics)

        # Screenshot 2: Screen 2 Dispatched Live Cockpit State
        snap_dispatch = os.path.join(ARTIFACT_DIR, "screen2_tracking_dispatched_verified.png")
        await page.screenshot(path=snap_dispatch)
        print("  -> Saved:", snap_dispatch)

        await browser.close()
        print("\nSCREEN 2 VERIFICATION COMPLETE!")

asyncio.run(test_screen2())
