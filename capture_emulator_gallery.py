import os
import time
from playwright.sync_api import sync_playwright

output_dir = os.path.abspath("emulator_screenshots")
os.makedirs(output_dir, exist_ok=True)

html_path = os.path.abspath("nukrop_emulator.html").replace("\\", "/")
url = f"file:///{html_path}"

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome", headless=True)
    context = browser.new_context(
        viewport={"width": 412, "height": 915},
        device_scale_factor=2.0,
        is_mobile=True,
        has_touch=True,
        user_agent="Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
    )
    page = context.new_page()

    page.goto(url)
    page.wait_for_load_state("networkidle")

    # 1. Splash Screen
    page.evaluate("""() => {
        if (typeof plantixFlowState !== 'undefined') {
            plantixFlowState.currentScreen = 'splash';
            renderPlantixFlow();
        }
        const toast = document.getElementById('global-push-toast');
        if (toast) toast.style.display = 'none';
    }""")
    time.sleep(0.5)
    page.screenshot(path=os.path.join(output_dir, "01_splash_screen.png"))
    print("[OK] 01_splash_screen.png")

    # 2. Language Selection Screen
    page.evaluate("""() => {
        if (typeof plantixFlowState !== 'undefined') {
            plantixFlowState.currentScreen = 'language';
            renderPlantixFlow();
        }
        const toast = document.getElementById('global-push-toast');
        if (toast) toast.style.display = 'none';
    }""")
    time.sleep(0.5)
    page.screenshot(path=os.path.join(output_dir, "02_language_selection.png"))
    print("[OK] 02_language_selection.png")

    # Select Telugu as user choice
    page.evaluate("""() => {
        if (typeof selectPlantixLang === 'function') {
            selectPlantixLang('te');
        }
    }""")
    time.sleep(0.3)

    # 3. Onboarding Slide 1 (AI Crop Doctor)
    page.evaluate("""() => {
        plantixFlowState.currentScreen = 'slide_disease';
        renderPlantixFlow();
        const toast = document.getElementById('global-push-toast');
        if (toast) toast.style.display = 'none';
    }""")
    time.sleep(0.5)
    page.screenshot(path=os.path.join(output_dir, "03_onboarding_slide1_telugu.png"))
    print("[OK] 03_onboarding_slide1_telugu.png")

    # 4. Onboarding Slide 3 (Mandi Prices in Telugu)
    page.evaluate("""() => {
        plantixFlowState.currentScreen = 'slide_mandi';
        renderPlantixFlow();
        const toast = document.getElementById('global-push-toast');
        if (toast) toast.style.display = 'none';
    }""")
    time.sleep(0.5)
    page.screenshot(path=os.path.join(output_dir, "04_onboarding_slide3_mandi_telugu.png"))
    print("[OK] 04_onboarding_slide3_mandi_telugu.png")

    # 5. Onboarding Slide 5 (GramHaul in Telugu)
    page.evaluate("""() => {
        plantixFlowState.currentScreen = 'slide_haul';
        renderPlantixFlow();
        const toast = document.getElementById('global-push-toast');
        if (toast) toast.style.display = 'none';
    }""")
    time.sleep(0.5)
    page.screenshot(path=os.path.join(output_dir, "05_onboarding_slide5_gramhaul_telugu.png"))
    print("[OK] 05_onboarding_slide5_gramhaul_telugu.png")

    # 6. Permissions Screen (Camera in 100% Telugu)
    page.evaluate("""() => {
        plantixFlowState.currentScreen = 'perm_camera';
        renderPlantixFlow();
        const toast = document.getElementById('global-push-toast');
        if (toast) toast.style.display = 'none';
    }""")
    time.sleep(0.5)
    page.screenshot(path=os.path.join(output_dir, "06_permissions_camera.png"))
    print("[OK] 06_permissions_camera.png")

    # 7. Crop Selection Screen (100% Pure Telugu Crop Names)
    page.evaluate("""() => {
        plantixFlowState.currentScreen = 'crops';
        renderPlantixFlow();
        const toast = document.getElementById('global-push-toast');
        if (toast) toast.style.display = 'none';
    }""")
    time.sleep(0.5)
    page.screenshot(path=os.path.join(output_dir, "07_crop_selection.png"))
    print("[OK] 07_crop_selection.png")

    # 8. Complete Onboarding & Open Farmer Home Dashboard
    page.evaluate("""() => {
        const overlay = document.getElementById('startup-experience-overlay');
        if (overlay) overlay.style.display = 'none';
        authUserRole = 'farmer';
        currentLang = 'te';
        localStorage.setItem('nukrop_lang', 'te');
        localStorage.setItem('nukrop_logged_in', 'true');
        localStorage.setItem('nukrop_onboarding_completed', 'true');
        localStorage.setItem('nukrop_user_role', 'farmer');
        if (typeof openScreen === 'function') openScreen('home', null);
    }""")
    time.sleep(1.0)
    page.screenshot(path=os.path.join(output_dir, "08_farmer_home_dashboard.png"))
    print("[OK] 08_farmer_home_dashboard.png")

    # 9. Open Farmer Profile (Pure Telugu with clean Red Log Out)
    page.evaluate("""() => {
        if (typeof openScreen === 'function') openScreen('profile', null);
    }""")
    time.sleep(0.5)
    page.screenshot(path=os.path.join(output_dir, "09_farmer_profile_clean.png"))
    print("[OK] 09_farmer_profile_clean.png")

    # 10. Open AgriStack Modal in Profile
    page.evaluate("""() => {
        if (typeof openAgriStackModal === 'function') openAgriStackModal();
    }""")
    time.sleep(0.5)
    page.screenshot(path=os.path.join(output_dir, "10_agristack_passport_modal.png"))
    print("[OK] 10_agristack_passport_modal.png")

    # Close modal
    page.evaluate("""() => {
        const m = document.getElementById('agristack-identity-modal');
        if (m) m.remove();
    }""")

    # 11. Open GramHaul Screen (Pure Telugu Booking Sheet & 40% Map)
    page.evaluate("""() => {
        if (typeof openScreen === 'function') openScreen('gramhaul', null);
    }""")
    time.sleep(1.5)
    page.screenshot(path=os.path.join(output_dir, "11_gramhaul_redesigned_map_trucks.png"))
    print("[OK] 11_gramhaul_redesigned_map_trucks.png")

    # 12. Trigger Real GramHaul Dispatch Modal (Pure Telugu)
    page.evaluate("""() => {
        if (typeof executeRealGramhaulDispatch === 'function') executeRealGramhaulDispatch();
    }""")
    time.sleep(1.8)
    page.screenshot(path=os.path.join(output_dir, "12_gramhaul_dispatch_broadcast_modal.png"))
    print("[OK] 12_gramhaul_dispatch_broadcast_modal.png")

    # Cleanly remove all modals before switching to driver screen
    page.evaluate("""() => {
        const m1 = document.getElementById('gh-dispatched-modal');
        if (m1) m1.remove();
        const m2 = document.getElementById('gh-dispatch-loading-modal');
        if (m2) m2.remove();
        const m3 = document.getElementById('agristack-identity-modal');
        if (m3) m3.remove();
        const m4 = document.getElementById('driver-insurance-modal');
        if (m4) m4.remove();
    }""")
    time.sleep(0.4)

    # 13. Open Driver Cockpit Dashboard (Pure Telugu)
    page.evaluate("""() => {
        authUserRole = 'driver';
        currentLang = 'te';
        localStorage.setItem('nukrop_lang', 'te');
        localStorage.setItem('nukrop_user_role', 'driver');
        localStorage.setItem('gh_driver_tab', 'map');
        if (typeof openScreen === 'function') openScreen('driver_dashboard', null);
    }""")
    time.sleep(1.5)
    page.screenshot(path=os.path.join(output_dir, "13_driver_cockpit_map.png"))
    print("[OK] 13_driver_cockpit_map.png")

    # 14. Open Driver Profile (Pure Telugu with Red Log Out)
    page.evaluate("""() => {
        localStorage.setItem('gh_driver_tab', 'profile');
        if (typeof openScreen === 'function') openScreen('driver_dashboard', null);
    }""")
    time.sleep(0.8)
    page.screenshot(path=os.path.join(output_dir, "14_driver_profile_clean.png"))
    print("[OK] 14_driver_profile_clean.png")

    # 15. Open Driver Insurance & FASTag Modal
    page.evaluate("""() => {
        if (typeof openDriverInsuranceFastagModal === 'function') openDriverInsuranceFastagModal();
    }""")
    time.sleep(0.8)
    page.screenshot(path=os.path.join(output_dir, "15_driver_insurance_fastag_modal.png"))
    print("[OK] 15_driver_insurance_fastag_modal.png")

    browser.close()
    print("All emulator screenshots successfully captured with single-language purity!")
