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

    # 1. Slide 0 (Crop Doctor)
    page.evaluate("openOnboardingFlow(true); advanceOnboardingSlide(0);")
    time.sleep(0.4)
    page.screenshot(path=os.path.join(artifact_dir, "verified_onboard_1_crop_doctor.png"))
    print("Captured Slide 1: Crop Doctor")

    # Slide 1 (Mandi Rates)
    page.evaluate("advanceOnboardingSlide(1);")
    time.sleep(0.4)
    page.screenshot(path=os.path.join(artifact_dir, "verified_onboard_2_mandi_rates.png"))
    print("Captured Slide 2: Mandi Rates")

    # Slide 2 (GramHaul Logistics)
    page.evaluate("advanceOnboardingSlide(2);")
    time.sleep(0.4)
    page.screenshot(path=os.path.join(artifact_dir, "verified_onboard_3_farm_logistics.png"))
    print("Captured Slide 3: Farm Logistics")

    # Slide 3 (AgriStack)
    page.evaluate("advanceOnboardingSlide(3);")
    time.sleep(0.4)
    page.screenshot(path=os.path.join(artifact_dir, "verified_onboard_4_agristack.png"))
    print("Captured Slide 4: AgriStack Tech")

    # Slide 4 (AI Voice Agronomist & Weather)
    page.evaluate("advanceOnboardingSlide(4);")
    time.sleep(0.4)
    page.screenshot(path=os.path.join(artifact_dir, "verified_onboard_5_voice_weather.png"))
    print("Captured Slide 5: Voice Agronomist & Weather")

    # Slide 5 (Kisan Community & Machinery)
    page.evaluate("advanceOnboardingSlide(5);")
    time.sleep(0.4)
    page.screenshot(path=os.path.join(artifact_dir, "verified_onboard_6_community_machinery.png"))
    print("Captured Slide 6: Community Machinery Sharing")

    # 2. Permissions Suite Dialog
    page.evaluate("openPermissionsSuiteModal();")
    time.sleep(0.4)
    page.screenshot(path=os.path.join(artifact_dir, "verified_permissions_suite.png"))
    print("Captured Permissions Suite Dialog")

    # 3. Potea Login Screen
    page.evaluate("document.getElementById('permissions-suite-modal')?.remove(); renderLoginScreen(document.getElementById('screen-container'));")
    time.sleep(0.4)
    page.screenshot(path=os.path.join(artifact_dir, "verified_potea_login_phone.png"))
    print("Captured Potea Login")

    # 4. Google Auth Modal
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
      document.getElementById('onboarding-experience-overlay')?.remove();
      document.getElementById('startup-experience-overlay')?.remove();
      document.getElementById('permissions-suite-modal')?.remove();
      if (typeof switchUserRole === 'function') switchUserRole('farmer');
      openScreen('home', null);
    """)
    time.sleep(0.5)
    page.screenshot(path=os.path.join(artifact_dir, "verified_farmer_home_dashboard.png"))
    print("Captured Farmer Home Dashboard")

    # 7. GramHaul Dark/Neon Logistics
    page.evaluate("openScreen('gramhaul', null);")
    time.sleep(0.5)
    page.screenshot(path=os.path.join(artifact_dir, "verified_gramhaul_dark_neon.png"))
    print("Captured GramHaul Dark/Neon Logistics")

    # 8. Driver Cockpit Portal
    page.evaluate("if (typeof loginAsDriver === 'function') loginAsDriver(); else if (typeof switchUserRole === 'function') switchUserRole('driver');")
    time.sleep(0.5)
    page.screenshot(path=os.path.join(artifact_dir, "verified_driver_cockpit_portal.png"))
    print("Captured Driver Cockpit Portal")

    browser.close()
    print("Verification and capture completed successfully!")
