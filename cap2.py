import asyncio
from playwright.async_api import async_playwright
import os
ARTIFACTS = r'C:\Users\bjasw\.gemini\antigravity\brain\36944d22-a0e5-4ba9-95b4-639674444ec9'
FILE = os.path.abspath('nukrop_emulator.html')
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True, args=['--no-sandbox'])
        c = await b.new_context(viewport={'width':430,'height':900}, device_scale_factor=2)
        page = await c.new_page()
        await page.goto(f'file:///{FILE}')
        await asyncio.sleep(1.5)
        # Skip splash
        await page.evaluate("""
            const splash = document.getElementById('gh-splash');
            if(splash) splash.remove();
            window.switchUserRole('farmer'); 
            if (typeof openScreen === 'function') openScreen('home', null);
        """)
        await asyncio.sleep(1.0)
        await page.screenshot(path=os.path.join(ARTIFACTS, 'v9_farmer_home_plantix.png'))
        print('Captured v9_farmer_home_plantix.png')
        await b.close()
asyncio.run(main())
