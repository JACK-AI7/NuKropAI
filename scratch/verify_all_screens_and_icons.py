import asyncio
from playwright.async_api import async_playwright

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 412, 'height': 915})
        await page.goto('http://localhost:8080/app/src/main/assets/index.html')
        
        # Wait for splash to finish or remove it
        await page.wait_for_timeout(3500)
        await page.evaluate('''() => {
            const overlay = document.getElementById('startup-experience-overlay');
            if (overlay) overlay.remove();
        }''')
        await page.wait_for_timeout(500)

        # 1. Capture Home Screen
        await page.screenshot(path='scratch/home_screen_verified.png')
        print('Captured scratch/home_screen_verified.png')

        # 2. Open Community Screen
        await page.evaluate("openScreen('community', document.getElementById('tab-community'))")
        await page.wait_for_timeout(1000)
        await page.screenshot(path='scratch/community_screen_verified.png')
        print('Captured scratch/community_screen_verified.png')

        # 3. Open Story 0 from Community
        await page.evaluate("openInstagramStoryModal(0)")
        await page.wait_for_timeout(1000)
        await page.screenshot(path='scratch/story_screen_fullscreen_verified.png')
        print('Captured scratch/story_screen_fullscreen_verified.png')

        # Close Story
        await page.evaluate("closeInstagramStoryModal()")
        await page.wait_for_timeout(500)

        # 4. Open Mandi Screen
        await page.evaluate("openScreen('market', document.getElementById('tab-market'))")
        await page.wait_for_timeout(1000)
        await page.screenshot(path='scratch/mandi_screen_verified.png')
        print('Captured scratch/mandi_screen_verified.png')

        # 5. Open AgriStack Screen
        await page.evaluate("openScreen('agristack', null)")
        await page.wait_for_timeout(1200)
        await page.screenshot(path='scratch/agristack_screen_verified.png')
        print('Captured scratch/agristack_screen_verified.png')

        await browser.close()
        print('All screen captures completed!')

if __name__ == '__main__':
    asyncio.run(verify())
