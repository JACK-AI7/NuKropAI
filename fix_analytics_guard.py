import sys

sys.stdout.reconfigure(encoding='utf-8')

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define safe NuKropAnalytics if not defined
    analytics_guard = "window.NuKropAnalytics = window.NuKropAnalytics || { track: function(e, d) { console.log('[Analytics]', e, d); } };\n"
    
    if "window.NuKropAnalytics =" not in content:
        content = content.replace("<script>", f"<script>\n{analytics_guard}", 1)

    content = content.replace("NuKropAnalytics.track(", "if (typeof NuKropAnalytics !== 'undefined' && NuKropAnalytics.track) NuKropAnalytics.track(")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed {path}")

fix_file('app/src/main/assets/index.html')
fix_file('nukrop_emulator.html')
