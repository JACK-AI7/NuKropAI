import os, sys, time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

artifact_dir = r"C:\Users\bjasw\.gemini\antigravity\brain\36944d22-a0e5-4ba9-95b4-639674444ec9"
html_path = os.path.abspath("nukrop_emulator.html")

print(f"Loading emulator from file:///{html_path.replace(os.sep, '/')}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 430, "height": 932})

    page.goto(f"file:///{html_path.replace(os.sep, '/')}")
    page.wait_for_load_state("networkidle")
    time.sleep(0.8)

    # 1. Onboarding Slides 0 to 5
    page.evaluate("openOnboardingFlow(true); advanceOnboardingSlide(0);")
    time.sleep(0.4)
    page.screenshot(path=os.path.join(artifact_dir, "verified_onboard_1_crop_doctor.png"))
    print("Captured Onboard 1: Crop Doctor")

    page.evaluate("advanceOnboardingSlide(1);")
    time.sleep(0.4)
    page.screenshot(path=os.path.join(artifact_dir, "verified_onboard_2_mandi_rates.png"))
    print("Captured Onboard 2: Mandi Rates")

    page.evaluate("advanceOnboardingSlide(2);")
    time.sleep(0.4)
    page.screenshot(path=os.path.join(artifact_dir, "verified_onboard_3_farm_logistics.png"))
    print("Captured Onboard 3: Farm Logistics")

    page.evaluate("advanceOnboardingSlide(3);")
    time.sleep(0.4)
    page.screenshot(path=os.path.join(artifact_dir, "verified_onboard_4_agristack.png"))
    print("Captured Onboard 4: AgriStack")

    page.evaluate("advanceOnboardingSlide(4);")
    time.sleep(0.4)
    page.screenshot(path=os.path.join(artifact_dir, "verified_onboard_5_voice_weather.png"))
    print("Captured Onboard 5: Voice Weather")

    page.evaluate("advanceOnboardingSlide(5);")
    time.sleep(0.4)
    page.screenshot(path=os.path.join(artifact_dir, "verified_onboard_6_community_machinery.png"))
    print("Captured Onboard 6: Community Machinery")

    # 2. Full-Bleed Permissions Flow (Steps 1, 2, 3)
    page.evaluate("openPermissionsFullBleedFlow();")
    time.sleep(0.4)
    page.screenshot(path=os.path.join(artifact_dir, "verified_perm_1_camera.png"))
    print("Captured Permission 1: Camera")

    page.evaluate("handlePermissionSlideAction(0);")
    time.sleep(0.4)
    page.screenshot(path=os.path.join(artifact_dir, "verified_perm_2_location.png"))
    print("Captured Permission 2: Location")

    page.evaluate("handlePermissionSlideAction(1);")
    time.sleep(0.4)
    page.screenshot(path=os.path.join(artifact_dir, "verified_perm_3_notification.png"))
    print("Captured Permission 3: Notification")

    # 3. Clean Potea Login Screen (With Zero Bottom Dock)
    page.evaluate("handlePermissionSlideAction(2);")
    time.sleep(0.4)
    page.screenshot(path=os.path.join(artifact_dir, "verified_potea_login_clean.png"))
    print("Captured Clean Potea Login")

    # 4. Google Auth Chooser Modal
    page.evaluate("openInAppGoogleAuthModal();")
    time.sleep(0.4)
    page.screenshot(path=os.path.join(artifact_dir, "verified_google_auth_modal.png"))
    print("Captured Google Auth Modal")

    # 5. Success Modal
    page.evaluate("document.getElementById('google-auth-modal')?.remove(); openPostLoginSuccessModal('B. Jaswanth Reddy', 'farmer');")
    time.sleep(0.4)
    page.screenshot(path=os.path.join(artifact_dir, "verified_auth_success_modal.png"))
    print("Captured Auth Success Modal")

    # 6. Farmer Home Dashboard
    page.evaluate("""
      document.getElementById('post-login-success-modal')?.remove();
      document.getElementById('login-screen-overlay')?.remove();
      document.getElementById('onboarding-experience-overlay')?.remove();
      document.getElementById('permission-experience-overlay')?.remove();
      document.getElementById('startup-experience-overlay')?.remove();
      const dock = document.querySelector('.bottom-dock-wrap');
      if (dock) dock.style.display = 'flex';
      if (typeof switchUserRole === 'function') switchUserRole('farmer');
      if (typeof openScreen === 'function') openScreen('home', null);
    """)
    time.sleep(0.5)
    page.screenshot(path=os.path.join(artifact_dir, "verified_farmer_home_dashboard.png"))
    print("Captured Farmer Home Dashboard")

    # 7. GramHaul Dark/Neon Logistics
    page.evaluate("if (typeof openScreen === 'function') openScreen('gramhaul', null);")
    time.sleep(0.5)
    page.screenshot(path=os.path.join(artifact_dir, "verified_gramhaul_dark_neon.png"))
    print("Captured GramHaul Dark/Neon Logistics")

    # 8. Driver Cockpit Portal
    page.evaluate("if (typeof loginAsDriver === 'function') loginAsDriver(); else if (typeof switchUserRole === 'function') switchUserRole('driver');")
    time.sleep(0.5)
    page.screenshot(path=os.path.join(artifact_dir, "verified_driver_cockpit_portal.png"))
    print("Captured Driver Cockpit Portal")

    browser.close()
    print("All verification screenshots successfully captured!")
