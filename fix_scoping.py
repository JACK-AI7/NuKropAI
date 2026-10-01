import sys, re

sys.stdout.reconfigure(encoding='utf-8')

def fix_scope(path):
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # Clean up any duplicated startupOverlay definitions
    c = re.sub(
        r'const startupOverlay = document\.getElementById\(\'startup-experience-overlay\'\);\s*if \(startupOverlay\) startupOverlay\.remove\(\);',
        "{ const s = document.getElementById('startup-experience-overlay'); if (s) s.remove(); }",
        c
    )
    c = re.sub(
        r'const pushToast = document\.getElementById\(\'global-push-toast\'\);\s*if \(pushToast\) pushToast\.remove\(\);',
        "{ const pt = document.getElementById('global-push-toast'); if (pt) pt.remove(); }",
        c
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"Fixed scoping in {path}")

fix_scope('app/src/main/assets/index.html')
fix_scope('nukrop_emulator.html')
