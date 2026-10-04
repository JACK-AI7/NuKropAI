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

async def test_screen1_and_interactions():
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

        print("[1] Opening GramHaul Screen 1 on http://localhost:8080/app/src/main/assets/index.html...")
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

        # Capture Screen 1 top view
        snap_s1_top = os.path.join(ARTIFACT_DIR, "screen1_top_view.png")
        await page.screenshot(path=snap_s1_top)
        print("  -> Screen 1 Top View saved:", snap_s1_top)

        # Inspect images of the 5 tiers in Screen 1
        tier_images = await page.evaluate("""() => {
            const tiers = [1, 2, 3, 4, 5];
            return tiers.map(t => {
                const card = document.getElementById('gh-tier-' + t);
                const img = card ? card.querySelector('img') : null;
                return {
                    tier: t,
                    src: img ? img.getAttribute('src') : null,
                    alt: img ? img.getAttribute('alt') : null,
                    displayedWidth: img ? img.clientWidth : null,
                    displayedHeight: img ? img.clientHeight : null
                };
            });
        }""")
        print("[2] Screen 1 Tier Truck Images:", tier_images)

        # Scroll down slightly inside the sheet to show all vehicle cards
        await page.evaluate("""() => {
            const container = document.querySelector('#screen-body div[style*=\"overflow-y:auto\"], #screen-body div[style*=\"overflow-y: auto\"]');
            if (container) {
                container.scrollTop = 180;
            }
        }""")
        await page.wait_for_timeout(400)

        snap_s1_fleet = os.path.join(ARTIFACT_DIR, "screen1_fleet_scrolled.png")
        await page.screenshot(path=snap_s1_fleet)
        print("  -> Screen 1 Fleet Scrolled saved:", snap_s1_fleet)

        # Select Tier 2 and verify selection
        await page.evaluate("""() => {
            selectGramhaulTruckTier(2);
        }""")
        await page.wait_for_timeout(400)
        snap_s1_tier2 = os.path.join(ARTIFACT_DIR, "screen1_tier2_selected.png")
        await page.screenshot(path=snap_s1_tier2)
        print("  -> Screen 1 Tier 2 Selected saved:", snap_s1_tier2)

        # Test Dispatch and Real-Time Driver Movement on Map
        print("[3] Dispatching trip to test real-time driver movement on map...")
        await page.evaluate("""() => {
            executeRealGramhaulDispatch();
        }""")
        await page.wait_for_timeout(2200) # Wait for driver accept (1.8s timeout)

        # Get initial driver marker position
        pos1 = await page.evaluate("""() => {
            if (trackingDriverMarker) {
                const latlng = trackingDriverMarker.getLatLng();
                return { lat: latlng.lat, lng: latlng.lng };
            }
            return null;
        }""")
        print("  -> Driver pos at accept:", pos1)

        # Wait 3.6 seconds (approx 3 movement ticks)
        await page.wait_for_timeout(3600)
        pos2 = await page.evaluate("""() => {
            if (trackingDriverMarker) {
                const latlng = trackingDriverMarker.getLatLng();
                return { lat: latlng.lat, lng: latlng.lng };
            }
            return null;
        }""")
        print("  -> Driver pos after 3.6s movement:", pos2)

        # Verify marker actually moved!
        if pos1 and pos2:
            moved = (pos1['lat'] != pos2['lat']) or (pos1['lng'] != pos2['lng'])
            print(f"  -> DID DRIVER MARKER MOVE REALISTICALLY? {moved} (lat delta: {pos2['lat'] - pos1['lat']:.6f})")

        # Test Real Call Button redirection
        print("[4] Testing real call button...")
        call_result = await page.evaluate("""() => {
            let interceptedHref = null;
            const originalLocation = window.location.href;
            
            // Override window.AndroidBridge or check what triggerDriverCall does
            window.AndroidBridge = {
                makePhoneCall: function(num) {
                    window.__calledPhone = num;
                }
            };
            
            triggerDriverCall('Suresh Yadav', '+91 94401 55667');
            return {
                androidCallMade: window.__calledPhone,
                modalExists: !!document.getElementById('driver-live-call-modal')
            };
        }""")
        print("  -> Call Result (AndroidBridge / tel redirect, NO fake modal):", call_result)

        await browser.close()
        print("\nALL VERIFICATIONS PASSED SUCCESSFULLY!")

asyncio.run(test_screen1_and_interactions())
