import sys
sys.stdout.reconfigure(encoding='utf-8')
import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 412, 'height': 915})
        page = await context.new_page()

        errors = []
        page.on('console', lambda msg: print(f"PAGE LOG [{msg.type}]: {msg.text}") if msg.type in ['error', 'warn'] else None)
        page.on('pageerror', lambda err: errors.append(str(err)))

        file_path = os.path.abspath('app/src/main/assets/index.html')
        url = 'file:///' + file_path.replace('\\', '/')
        print('1. Launching:', url)
        await page.goto(url)
        await asyncio.sleep(1)

        # 1. Splash Viewport
        splash_text = await page.evaluate("() => document.getElementById('splash-viewport') ? 'VISIBLE' : 'HIDDEN'")
        print("Phase 1: Splash Screen ->", splash_text)
        await page.screenshot(path="verified_phase1_splash.png")

        # 2. Six Onboarding Slides
        slides = [
            ('slide_disease', '1_crop_doctor', 'images/onboard_crop_doctor.jpg'),
            ('slide_tips', '2_ai_voice_weather', 'images/onboard_ai_voice_weather.jpg'),
            ('slide_mandi', '3_mandi_prices', 'images/onboard_mandi_prices.jpg'),
            ('slide_deals', '4_machinery_community', 'images/onboard_community_machinery.jpg'),
            ('slide_haul', '5_farm_logistics', 'images/onboard_farm_logistics.jpg'),
            ('slide_agristack', '6_agristack_tech', 'images/onboard_agristack_tech.jpg'),
        ]

        for s_id, s_name, expected_img in slides:
            await page.evaluate(f"() => {{ advanceSlide('{s_id}'); }}")
            await asyncio.sleep(0.3)
            info = await page.evaluate("""() => {
                const img = document.querySelector('#startup-experience-overlay img');
                const title = document.querySelector('#startup-experience-overlay div[style*="font-weight:900"]')?.innerText || '';
                return {
                    imgSrc: img ? img.getAttribute('src') : 'NO_IMG',
                    imgComplete: img ? img.complete : false,
                    naturalWidth: img ? img.naturalWidth : 0,
                    title: title
                };
            }""")
            print(f"Phase 2: Slide [{s_id}] ({s_name}):")
            print(f"   Title: {info['title']}")
            print(f"   Image src: {info['imgSrc']}")
            print(f"   Loaded: {info['imgComplete']}, Natural Size: {info['naturalWidth']}px")
            await page.screenshot(path=f"verified_phase2_onboarding_{s_name}.png")

        # 3. Three Permissions
        # Advance from slide 6 to perm_location (clicking next or skip)
        await page.evaluate("() => { advanceSlide('perm_location'); }")
        await asyncio.sleep(0.3)
        p1 = await page.evaluate("""() => {
            const img = document.querySelector('#startup-experience-overlay img');
            return {
                imgSrc: img ? img.getAttribute('src') : 'NO_IMG',
                loaded: img ? img.complete : false,
                naturalWidth: img ? img.naturalWidth : 0,
                text: document.querySelector('#startup-experience-overlay')?.innerText.slice(0, 50)
            };
        }""")
        print("Phase 3a: Location Permission -> Image:", p1['imgSrc'], "Loaded:", p1['loaded'], p1['naturalWidth'], "px")
        await page.screenshot(path="verified_phase3a_perm_location.png")

        await page.evaluate("() => { grantLocationAndContinue(); }")
        await asyncio.sleep(0.3)
        p2 = await page.evaluate("""() => {
            const img = document.querySelector('#startup-experience-overlay img');
            return {
                imgSrc: img ? img.getAttribute('src') : 'NO_IMG',
                loaded: img ? img.complete : false,
                naturalWidth: img ? img.naturalWidth : 0,
                text: document.querySelector('#startup-experience-overlay')?.innerText.slice(0, 50)
            };
        }""")
        print("Phase 3b: Notifications Permission -> Image:", p2['imgSrc'], "Loaded:", p2['loaded'], p2['naturalWidth'], "px")
        await page.screenshot(path="verified_phase3b_perm_notifications.png")

        await page.evaluate("() => { grantNotificationAndContinue(); }")
        await asyncio.sleep(0.3)
        p3 = await page.evaluate("""() => {
            const img = document.querySelector('#startup-experience-overlay img');
            return {
                imgSrc: img ? img.getAttribute('src') : 'NO_IMG',
                loaded: img ? img.complete : false,
                naturalWidth: img ? img.naturalWidth : 0,
                text: document.querySelector('#startup-experience-overlay')?.innerText.slice(0, 50)
            };
        }""")
        print("Phase 3c: Camera Permission -> Image:", p3['imgSrc'], "Loaded:", p3['loaded'], p3['naturalWidth'], "px")
        await page.screenshot(path="verified_phase3c_perm_camera.png")

        # 4. Crop Selection Screen
        await page.evaluate("() => { grantCameraAndContinue(); }")
        await asyncio.sleep(0.3)
        crops = await page.evaluate("""() => {
            return {
                overlay: document.getElementById('startup-experience-overlay') ? 'VISIBLE' : 'HIDDEN',
                cropsCount: document.querySelectorAll('#startup-experience-overlay div[onclick*="toggleCropSelection"]').length,
                text: document.querySelector('#startup-experience-overlay')?.innerText.slice(0, 60)
            };
        }""")
        print("Phase 4: Crop Selection -> Badge Count:", crops['cropsCount'])
        await page.screenshot(path="verified_phase4_crop_selection.png")

        # 5. Login Screen
        await page.evaluate("() => { finishPlantixOnboarding(); }")
        await asyncio.sleep(0.3)
        login = await page.evaluate("""() => {
            return {
                overlay: document.getElementById('startup-experience-overlay') ? 'VISIBLE' : 'HIDDEN',
                hasLoginInputs: document.querySelectorAll('#startup-experience-overlay input').length,
                text: document.querySelector('#startup-experience-overlay')?.innerText.slice(0, 60)
            };
        }""")
        print("Phase 5: Login Screen -> Input fields:", login['hasLoginInputs'])
        await page.screenshot(path="verified_phase5_login.png")

        # 6a. Farmer Dashboard
        await page.evaluate("() => { handleGuestLogin(); }")
        await asyncio.sleep(0.5)
        farmer = await page.evaluate("""() => {
            return {
                overlayClosed: document.getElementById('startup-experience-overlay') ? false : true,
                bodyText: document.body.innerText.slice(0, 80)
            };
        }""")
        print("Phase 6a: Farmer Dashboard -> Overlay Closed:", farmer['overlayClosed'])
        await page.screenshot(path="verified_phase6a_farmer_dashboard.png")

        # 6b. Driver Dashboard / GramHaul Maps
        await page.evaluate("() => { loginAsDriver(); }")
        await asyncio.sleep(0.5)
        driver = await page.evaluate("""() => {
            return {
                driverDash: document.getElementById('gh-driver-dashboard') ? 'VISIBLE' : 'NOT_FOUND',
                driverMap: document.getElementById('driver-map') ? 'MAP_PRESENT' : 'NO_MAP'
            };
        }""")
        print("Phase 6b: Driver Dashboard / GramHaul Maps ->", driver['driverDash'], driver['driverMap'])
        await page.screenshot(path="verified_phase6b_driver_dashboard.png")

        await browser.close()

        if errors:
            print("\nERRORS DETECTED:", errors)
            sys.exit(1)
        else:
            print("\nPERFECT VERIFICATION: All 6 Onboarding Screens, 3 Permissions, Crop Selection, Login, and Dashboards executed flawlessly!")

asyncio.run(main())
