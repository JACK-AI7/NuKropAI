import sys

sys.stdout.reconfigure(encoding='utf-8')

def fix_auth_vars(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    auth_vars_decl = """
window.authFormMode = window.authFormMode || 'signin';
window.authUserRole = window.authUserRole || 'farmer';
var authFormMode = window.authFormMode;
var authUserRole = window.authUserRole;
function setAuthUserRole(role) {
  window.authUserRole = role;
  authUserRole = role;
  if (typeof renderLoginScreen === 'function') renderLoginScreen(document.getElementById('screen-container'));
}
function setAuthFormMode(mode) {
  window.authFormMode = mode;
  authFormMode = mode;
  if (typeof renderLoginScreen === 'function') renderLoginScreen(document.getElementById('screen-container'));
}
"""

    # Add right before renderLoginScreen
    if "var authFormMode = window.authFormMode;" not in content:
        content = content.replace("function renderLoginScreen", f"{auth_vars_decl}\nfunction renderLoginScreen", 1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed auth vars in {path}")

fix_auth_vars('app/src/main/assets/index.html')
fix_auth_vars('nukrop_emulator.html')
