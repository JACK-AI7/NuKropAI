import sys, re

sys.stdout.reconfigure(encoding='utf-8')

def fix_render_login(filepath):
    print(f"Fixing renderLoginScreen in {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    old_fn_start = "function renderLoginScreen(container) {"
    new_fn_start = """function renderLoginScreen(container) {
  window.authFormMode = window.authFormMode || 'signin';
  window.authUserRole = window.authUserRole || 'farmer';
  const currentAuthMode = window.authFormMode;
  const currentAuthRole = window.authUserRole;
  if (typeof NuKropAnalytics !== 'undefined' && NuKropAnalytics.track) NuKropAnalytics.track('onboarding_login_screen_viewed', { mode: currentAuthMode, role: currentAuthRole });
  const isSignUp = currentAuthMode === 'signup';
  const authUserRole = currentAuthRole;
  const authFormMode = currentAuthMode;"""

    # Replace the start of renderLoginScreen
    content = content.replace(
        """function renderLoginScreen(container) {
  if (typeof NuKropAnalytics !== 'undefined' && NuKropAnalytics.track) NuKropAnalytics.track('onboarding_login_screen_viewed', { mode: authFormMode, role: authUserRole });

  const isSignUp = authFormMode === 'signup';""",
        new_fn_start
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully patched {filepath}")

fix_render_login('app/src/main/assets/index.html')
fix_render_login('nukrop_emulator.html')
