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
        await page.evaluate("if (typeof openScreen === 'function') openScreen('home');")
        await asyncio.sleep(1.0)
        
        # Remove any lingering splash screens by forcefully removing the element
        await page.evaluate("""
            const splashes = document.querySelectorAll('#gh-splash, .nukrop-splash');
            splashes.forEach(s => s.remove());
        """)
        
        await page.screenshot(path=os.path.join(ARTIFACTS, 'v9_farmer_home_plantix2.png'))
        print('Captured v9_farmer_home_plantix2.png')
        await b.close()
asyncio.run(main())
