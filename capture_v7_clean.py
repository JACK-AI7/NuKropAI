import asyncio
from playwright.async_api import async_playwright
import os

ARTIFACTS = r'C:\Users\bjasw\.gemini\antigravity\brain\36944d22-a0e5-4ba9-95b4-639674444ec9'
FILE = os.path.abspath('nukrop_emulator.html')

async def cap(page, name):
    await asyncio.sleep(1.0)
    path = os.path.join(ARTIFACTS, f'{name}.png')
    await page.screenshot(path=path, clip={'x':0,'y':0,'width':430,'height':900})
    print(f'Captured: {name}.png')

async def fresh_driver(page, tab='map', online=True, trip=None):
    """Navigate to driver dashboard cleanly"""
    script = f"""
        // Remove any open modals
        const m = document.getElementById('gh-pay-modal');
        if (m) m.remove();
        localStorage.setItem('gh_driver_online', '{str(online).lower()}');
        localStorage.setItem('gh_driver_tab', '{tab}');
        {'localStorage.removeItem("nukrop_active_trip");' if trip is None else f'localStorage.setItem("nukrop_active_trip", JSON.stringify({trip}));'}
        if (typeof openScreen === 'function') openScreen('driver_dashboard', null);
    """
    await page.evaluate(script)
    await asyncio.sleep(0.8)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
        ctx = await browser.new_context(viewport={'width':430,'height':900}, device_scale_factor=2)
        page = await ctx.new_page()
        await page.goto(f'file:///{FILE}')
        await asyncio.sleep(1.5)
        await page.evaluate("window.finishLoginAndEnterDashboard('driver')")
        await asyncio.sleep(0.5)

        # ── 1. MAP: Online + Haul Request bottom sheet ──
        await fresh_driver(page, tab='map', online=True, trip=None)
        await cap(page, 'v7_map_online_haul_request')

        # ── 2. MAP: Offline ──
        await fresh_driver(page, tab='map', online=False, trip=None)
        await cap(page, 'v7_map_offline')

        # ── 3. MAP: Active trip bottom sheet ──
        trip = '{"id":"GH-4192","crop":"Cotton (పత్తి)","weight":"40 Quintals","mandi":"Warangal Enamamula APMC (Gate 3)","fare":"1850","status":"en_route","bookedAt":"2025-04-05T06:50:00Z"}'
        await fresh_driver(page, tab='map', online=True, trip=trip)
        await cap(page, 'v7_map_active_trip')

        # ── 4. PAYMENT sheet ──
        await page.evaluate("""
            const m2 = document.getElementById('gh-pay-modal');
            if (m2) m2.remove();
            if (typeof driverShowPaymentScreen === 'function') driverShowPaymentScreen('GH-4192', '1850');
        """)
        await asyncio.sleep(0.6)
        await cap(page, 'v7_payment_sheet')
        # Close modal
        await page.evaluate("const m=document.getElementById('gh-pay-modal');if(m)m.remove();")

        # ── 5. EARNINGS tab ──
        await fresh_driver(page, tab='earnings', online=True, trip=None)
        await cap(page, 'v7_earnings_tab')

        # ── 6. PROFILE tab ──
        await fresh_driver(page, tab='profile', online=True, trip=None)
        await cap(page, 'v7_profile_tab')

        await browser.close()
        print('\n✅ All 6 clean Rapido Captain screenshots done!')

asyncio.run(main())
