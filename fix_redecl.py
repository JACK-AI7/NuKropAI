import sys

sys.stdout.reconfigure(encoding='utf-8')

def fix_redecl(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove the duplicate declarations
    duplicate_snippet = """window.authFormMode = window.authFormMode || 'signin';
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
}"""

    clean_snippet = """window.authFormMode = window.authFormMode || 'signin';
window.authUserRole = window.authUserRole || 'farmer';
function setAuthUserRole(role) {
  window.authUserRole = role;
  if (typeof authUserRole !== 'undefined') authUserRole = role;
  if (typeof renderLoginScreen === 'function') renderLoginScreen(document.getElementById('screen-container'));
}
function setAuthFormMode(mode) {
  window.authFormMode = mode;
  if (typeof authFormMode !== 'undefined') authFormMode = mode;
  if (typeof renderLoginScreen === 'function') renderLoginScreen(document.getElementById('screen-container'));
}"""

    content = content.replace(duplicate_snippet, clean_snippet)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed redeclarations in {path}")

fix_redecl('app/src/main/assets/index.html')
fix_redecl('nukrop_emulator.html')
