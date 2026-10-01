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
        await asyncio.sleep(4.0)
        
        # Switch to farmer
        await page.evaluate("window.switchUserRole('farmer');")
        await asyncio.sleep(1.0)
        
        # Capture GramHaul (Driver Style but Green)
        await page.evaluate("if (typeof openScreen === 'function') openScreen('gramhaul');")
        await asyncio.sleep(1.0)
        await page.screenshot(path=os.path.join(ARTIFACTS, 'v10_farmer_gramhaul.png'))
        print('Captured v10_farmer_gramhaul.png')

        # Capture Community (Plantix Style)
        await page.evaluate("if (typeof openScreen === 'function') openScreen('community');")
        await asyncio.sleep(1.0)
        await page.screenshot(path=os.path.join(ARTIFACTS, 'v10_community_feed.png'))
        print('Captured v10_community_feed.png')

        await b.close()
asyncio.run(main())
