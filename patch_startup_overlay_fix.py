import sys, re

sys.stdout.reconfigure(encoding='utf-8')

def patch_file(path):
    print(f"Patching startup overlay in {path}...")
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. In openOnboardingFlow, ensure startup-experience-overlay and global-push-toast are cleared
    c = c.replace(
        "const existing = document.getElementById('onboarding-experience-overlay');\n  if (existing) existing.remove();",
        """const existing = document.getElementById('onboarding-experience-overlay');
  if (existing) existing.remove();
  const startupOverlay = document.getElementById('startup-experience-overlay');
  if (startupOverlay) startupOverlay.remove();
  const pushToast = document.getElementById('global-push-toast');
  if (pushToast) pushToast.remove();"""
    )

    # 2. In openPermissionsSuiteModal, ensure startup overlay and onboarding overlay are removed
    c = c.replace(
        "const existing = document.getElementById('onboarding-experience-overlay');\n  if (existing) existing.remove();",
        """const existing = document.getElementById('onboarding-experience-overlay');
  if (existing) existing.remove();
  const startupOverlay = document.getElementById('startup-experience-overlay');
  if (startupOverlay) startupOverlay.remove();"""
    )

    # 3. Ensure onboarding-experience-overlay has z-index: 999999
    c = c.replace(
        'id="onboarding-experience-overlay" style="position:absolute;inset:0;background:#0F172A;border-radius:40px;overflow:hidden;z-index:9999;',
        'id="onboarding-experience-overlay" style="position:absolute;inset:0;background:#0F172A;border-radius:40px;overflow:hidden;z-index:999999;'
    )
    c = c.replace(
        'id="permissions-suite-modal" style="position:absolute;inset:0;background:#FFFFFF;border-radius:40px;overflow:hidden;z-index:9999;',
        'id="permissions-suite-modal" style="position:absolute;inset:0;background:#FFFFFF;border-radius:40px;overflow:hidden;z-index:999999;'
    )

    # 4. Hide startup-experience-overlay on start if user already completed onboarding
    c = c.replace(
        '<div id="startup-experience-overlay" style="position:absolute;inset:0;background:#FFFFFF;border-radius:48px;overflow:hidden;z-index:99999;display:flex;flex-direction:column;">',
        '<div id="startup-experience-overlay" style="display:none;position:absolute;inset:0;background:#FFFFFF;border-radius:48px;overflow:hidden;z-index:99999;flex-direction:column;">'
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"Patched {path}")

patch_file('app/src/main/assets/index.html')
patch_file('nukrop_emulator.html')
