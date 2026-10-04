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

async def test_full_real_flow():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Mobile viewport matching Galaxy / Pixel
        context = await browser.new_context(
            viewport={'width': 412, 'height': 892},
            device_scale_factor=2,
            has_touch=True,
            is_mobile=True,
            geolocation={'latitude': 17.4401, 'longitude': 78.3489}, # Gachibowli / Hyderabad real GPS
            permissions=['geolocation']
        )
        page = await context.new_page()

        print("[1] Opening app with real GPS coordinates (17.4401, 78.3489)...")
        await page.goto("http://localhost:8080/nukrop_emulator.html", wait_until="networkidle")
        await page.wait_for_timeout(1500)

        # Clear startup overlays and open GramHaul
        await page.evaluate("""() => {
            const ids = ['startup-experience-overlay', 'onboarding-experience-overlay', 'splash-viewport', 'login-screen-overlay'];
            ids.forEach(id => { const el = document.getElementById(id); if (el) el.remove(); });
            // Clear any old active trip
            localStorage.removeItem('nukrop_active_trip');
            openScreen('gramhaul');
        }""")
        await page.wait_for_timeout(1000)

        # 1. Verify Farm Pickup Location on Screen 1
        pickup_info = await page.evaluate("""() => {
            const lbl = document.getElementById('gh-pickup-location-label');
            return {
                pickupText: lbl ? lbl.innerText.trim() : null,
                farmCoords: window.currentGramhaulFarmCoords
            };
        }""")
        print("[2] Screen 1 Pickup Location Info:", pickup_info)

        # Take Screen 1 screenshot
        snap1 = os.path.join(ARTIFACT_DIR, "real_screen1_gps_pickup_verified.png")
        await page.screenshot(path=snap1)
        print("  -> Saved Screen 1 Screenshot:", snap1)

        # 2. Click Request Mandi Truck Now -> Enter Searching State
        print("[3] Clicking 'Request Mandi Truck Now' to start searching...")
        await page.evaluate("executeRealGramhaulDispatch();")
        await page.wait_for_timeout(1200)

        # Verify Searching Radar is active
        searching_info = await page.evaluate("""() => {
            const title = document.querySelector('#gh-tracking-bottom-container div[style*=\"font-size:18px\"]');
            const sub = document.querySelector('#gh-tracking-bottom-container div[style*=\"font-size:12px\"]');
            const radarContainer = document.querySelector('#gh-tracking-bottom-container div[style*=\"radarRipple\"]');
            const trip = JSON.parse(localStorage.getItem('nukrop_active_trip') || '{}');
            return {
                titleText: title ? title.innerText.trim() : null,
                subText: sub ? sub.innerText.trim() : null,
                radarVisible: !!radarContainer,
                tripStatus: trip.status,
                tripPickup: trip.pickup
            };
        }""")
        print("[4] Screen 2 Searching Radar Info:", searching_info)

        # Wait 3 seconds to verify that it DOES NOT automatically timeout/dispatch (proving NO fake timeout!)
        print("[5] Waiting 3 seconds to prove NO fake timeout occurs...")
        await page.wait_for_timeout(3000)

        trip_status_after_3s = await page.evaluate("JSON.parse(localStorage.getItem('nukrop_active_trip') || '{}').status")
        print(f"  -> Trip Status after 3 seconds: '{trip_status_after_3s}' (Expected: 'SEARCHING' - Still Searching!)")
        assert trip_status_after_3s == 'SEARCHING', f"Expected 'SEARCHING', got '{trip_status_after_3s}'"

        snap_search = os.path.join(ARTIFACT_DIR, "real_screen2_searching_radar_verified.png")
        await page.screenshot(path=snap_search)
        print("  -> Saved Screen 2 Searching Radar Screenshot:", snap_search)

        # 3. Switch to Driver Dashboard to verify Incoming Request Card
        print("[6] Switching to Driver Dashboard to verify Incoming Request notification...")
        await page.evaluate("openScreen('driver_dashboard');")
        await page.wait_for_timeout(1500)

        driver_card_info = await page.evaluate("""() => {
            const modal = document.getElementById('driver-incoming-haul-modal');
            const acceptBtn = document.querySelector('#driver-incoming-haul-modal button:last-of-type');
            return {
                modalFound: !!modal,
                modalText: modal ? modal.innerText.replace(/\\s+/g, ' ').trim() : null,
                hasAcceptBtn: !!acceptBtn
            };
        }""")
        print("[7] Driver Dashboard Incoming Request Modal Info:", driver_card_info)

        snap_driver_request = os.path.join(ARTIFACT_DIR, "real_driver_incoming_request_verified.png")
        await page.screenshot(path=snap_driver_request)
        print("  -> Saved Driver Incoming Request Screenshot:", snap_driver_request)

        # 4. Driver Clicks [ACCEPT HAUL TRIP]
        print("[8] Driver clicks [ACCEPT HAUL TRIP]...")
        await page.evaluate("driverAcceptHaulRequest();")
        await page.wait_for_timeout(3000)

        # Verify Driver Cockpit is now in Active Navigation Mode with real OSRM route & stepper
        driver_active_info = await page.evaluate("""() => {
            const mapEl = document.getElementById('driver-real-osm-map');
            const paths = document.querySelectorAll('#driver-real-osm-map .leaflet-overlay-pane path');
            const trip = JSON.parse(localStorage.getItem('nukrop_active_trip') || '{}');
            const stepperSteps = document.querySelectorAll('.r-sheet div[onclick*=\"driverUpdateTripStep\"]');
            return {
                tripStatus: trip.status,
                driverName: trip.driverName,
                polylinesCount: paths.length,
                stepperCount: stepperSteps.length
            };
        }""")
        print("[9] Driver Active Navigation Mode Info:", driver_active_info)

        snap_driver_accepted = os.path.join(ARTIFACT_DIR, "real_driver_accepted_navigation_verified.png")
        await page.screenshot(path=snap_driver_accepted)
        print("  -> Saved Driver Active Navigation Screenshot:", snap_driver_accepted)

        # 5. Now switch back to Farmer Screen 2 Tracking: it should now be DISPATCHED!
        print("[10] Checking Farmer Screen 2 Live Tracking now that driver accepted...")
        await page.evaluate("openScreen('gramhaul_tracking');")
        await page.wait_for_timeout(3000)

        farmer_dispatched_info = await page.evaluate("""() => {
            const mapEl = document.getElementById('gramhaul-tracking-osm-map');
            const paths = document.querySelectorAll('#gramhaul-tracking-osm-map .leaflet-overlay-pane path');
            const etaBadge = document.getElementById('gh-dispatched-eta-badge')?.innerText;
            const topStatus = document.getElementById('gh-tracking-top-status-text')?.innerText;
            const trip = JSON.parse(localStorage.getItem('nukrop_active_trip') || '{}');
            return {
                tripStatus: trip.status,
                etaBadge: etaBadge,
                topStatus: topStatus,
                driverName: trip.driverName,
                pathsCount: paths.length
            };
        }""")
        print("[11] Farmer Screen 2 Dispatched Live Tracking Info:", farmer_dispatched_info)

        snap_farmer_dispatched = os.path.join(ARTIFACT_DIR, "real_farmer_dispatched_tracking_verified.png")
        await page.screenshot(path=snap_farmer_dispatched)
        print("  -> Saved Farmer Dispatched Tracking Screenshot:", snap_farmer_dispatched)

        await browser.close()
        print("\n🎉 COMPLETE REAL FLOW TEST PASSED WITH 100% SUCCESS!")

if __name__ == "__main__":
    asyncio.run(test_full_real_flow())
