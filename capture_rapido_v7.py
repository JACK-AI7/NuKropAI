import asyncio
from playwright.async_api import async_playwright
import os, shutil

ARTIFACTS = r'C:\Users\bjasw\.gemini\antigravity\brain\36944d22-a0e5-4ba9-95b4-639674444ec9'
FILE = os.path.abspath('nukrop_emulator.html')

async def cap(page, name, fn=None):
    if fn: await fn()
    await asyncio.sleep(1.2)
    path = os.path.join(ARTIFACTS, f'{name}.png')
    await page.screenshot(path=path, clip={'x':0,'y':0,'width':430,'height':900})
    print(f'Captured: {name}.png')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
        ctx = await browser.new_context(viewport={'width':430,'height':900},
                                        device_scale_factor=2)
        page = await ctx.new_page()
        await page.goto(f'file:///{FILE}')
        await asyncio.sleep(1.5)

        # Enter driver view
        await page.evaluate("window.finishLoginAndEnterDashboard('driver')")
        await asyncio.sleep(0.5)

        # 1. Driver MAP — online, haul request
        localStorage_driver_online = "localStorage.setItem('gh_driver_online','true');localStorage.removeItem('nukrop_active_trip');localStorage.setItem('gh_driver_tab','map')"
        await page.evaluate(localStorage_driver_online)
        await page.evaluate("if(typeof openScreen==='function') openScreen('driver_dashboard', null)")
        await cap(page, 'v7_driver_map_online_request')

        # 2. Driver MAP — offline
        await page.evaluate("localStorage.setItem('gh_driver_online','false');if(typeof openScreen==='function') openScreen('driver_dashboard', null)")
        await cap(page, 'v7_driver_map_offline')

        # 3. Driver MAP — active trip
        trip = '{"id":"GH-4192","crop":"Cotton (పత్తి)","weight":"40 Quintals","mandi":"Warangal Enamamula APMC (Gate 3)","fare":"1850","status":"en_route","bookedAt":"2025-04-05T06:50:00Z","driver":{"name":"Suresh Yadav","plate":"TS 03 UB 4491"}}'
        await page.evaluate(f"localStorage.setItem('nukrop_active_trip', JSON.stringify({trip}));localStorage.setItem('gh_driver_online','true');if(typeof openScreen==='function') openScreen('driver_dashboard', null)")
        await cap(page, 'v7_driver_map_active_trip')

        # 4. Payment sheet
        await page.evaluate("if(typeof driverShowPaymentScreen==='function') driverShowPaymentScreen('GH-4192','1850')")
        await cap(page, 'v7_driver_payment_sheet')

        # 5. Earnings tab
        await page.evaluate("localStorage.removeItem('nukrop_active_trip');localStorage.setItem('gh_driver_tab','earnings');if(typeof openScreen==='function') openScreen('driver_dashboard', null)")
        await cap(page, 'v7_driver_earnings_tab')

        # 6. Profile tab
        await page.evaluate("localStorage.setItem('gh_driver_tab','profile');if(typeof openScreen==='function') openScreen('driver_dashboard', null)")
        await cap(page, 'v7_driver_profile_tab')

        await browser.close()
        print('\nAll 6 Rapido Captain screenshots captured!')

asyncio.run(main())
