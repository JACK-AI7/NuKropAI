import asyncio
from playwright.async_api import async_playwright
import os

ARTIFACTS = r'C:\Users\bjasw\.gemini\antigravity\brain\36944d22-a0e5-4ba9-95b4-639674444ec9'
FILE = os.path.abspath('nukrop_emulator.html')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
        ctx = await browser.new_context(viewport={'width':430,'height':900}, device_scale_factor=2)
        page = await ctx.new_page()
        await page.goto(f'file:///{FILE}')
        await asyncio.sleep(1.5)
        
        # 1. Driver Map Online
        await page.evaluate("""
            const m = document.getElementById('gh-pay-modal');
            if (m) m.remove();
            localStorage.setItem('gh_driver_online', 'true');
            localStorage.setItem('gh_driver_tab', 'map');
            localStorage.removeItem('nukrop_active_trip');
            window.finishLoginAndEnterDashboard('driver');
            if (typeof openScreen === 'function') openScreen('driver_dashboard', null);
        """)
        await asyncio.sleep(0.8)
        await page.screenshot(path=os.path.join(ARTIFACTS, 'v8_driver_map_online.png'))
        print('Captured v8_driver_map_online.png')

        # 2. Driver Active Trip (to see that pill is hidden)
        trip = '{"id":"GH-4192","crop":"Cotton (పత్తి)","weight":"40 Quintals","mandi":"Warangal Enamamula APMC (Gate 3)","fare":"1850","status":"en_route","bookedAt":"2025-04-05T06:50:00Z"}'
        await page.evaluate(f"""
            localStorage.setItem('nukrop_active_trip', JSON.stringify({trip}));
            if (typeof openScreen === 'function') openScreen('driver_dashboard', null);
        """)
        await asyncio.sleep(0.8)
        await page.screenshot(path=os.path.join(ARTIFACTS, 'v8_driver_map_active_trip.png'))
        print('Captured v8_driver_map_active_trip.png')

        # 3. Farmer Home
        await page.evaluate("""
            window.switchUserRole('farmer');
            if (typeof openScreen === 'function') openScreen('home', null);
        """)
        await asyncio.sleep(0.8)
        await page.screenshot(path=os.path.join(ARTIFACTS, 'v8_farmer_home.png'))
        print('Captured v8_farmer_home.png')
        
        # 4. Farmer GramHaul
        await page.evaluate("""
            if (typeof openScreen === 'function') openScreen('gramhaul', null);
        """)
        await asyncio.sleep(0.8)
        await page.screenshot(path=os.path.join(ARTIFACTS, 'v8_farmer_gramhaul.png'))
        print('Captured v8_farmer_gramhaul.png')
        
        # 5. Driver Profile (to see the circular avatar)
        await page.evaluate("""
            window.switchUserRole('driver');
            localStorage.setItem('gh_driver_tab', 'profile');
            if (typeof openScreen === 'function') openScreen('driver_dashboard', null);
        """)
        await asyncio.sleep(0.8)
        await page.screenshot(path=os.path.join(ARTIFACTS, 'v8_driver_profile.png'))
        print('Captured v8_driver_profile.png')

        await browser.close()

asyncio.run(main())
