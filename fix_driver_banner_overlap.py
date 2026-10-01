import sys, re
sys.stdout.reconfigure(encoding='utf-8')

# Fix the notification banner overlap issue in the driver dashboard
# The banner (#nukrop-alert-banner) stays fixed at top and overlaps driver header
# Solution: add paddingTop to the driver dashboard root div to account for it

for filepath in ['app/src/main/assets/index.html', 'nukrop_emulator.html']:
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Find the driver dashboard root div and fix its top padding
    # Current: padding:12px 16px 14px; in the header section
    # We need to add padding-top to account for the notification banner (height ~80px)
    
    # Fix 1: The driver dashboard outer wrapper should have padding-top:0
    # and the status bar div should add safe area + banner height awareness
    
    # Actually the easier fix is to ensure the driver cockpit view renders below the notification banner
    # The banner is outside #screen-container, so the issue is the absolute positioning
    # Let's check how the screen container works
    
    # The screen container already handles this - the notification banner is at top
    # and screen-container should have position:relative with proper top offset
    # Looking at the screenshot, the GramHaul Cockpit header IS visible correctly in offline state
    # but in online-idle state the notification banner covers it
    # 
    # This is because when we call finishLoginAndEnterDashboard('driver'), 
    # the notification banner doesn't get dismissed
    #
    # Fix: dismiss the banner when entering driver mode OR ensure the banner is offset properly
    
    # The quickest fix: in the driver dashboard view, add a paddingTop to account for banner
    # when banner is visible, add 80px padding-top to the outermost div
    
    old = 'background:#F4F6F9;min-height:100%;padding-bottom:100px;font-family:-apple-system,BlinkMacSystemFont,\'Plus Jakarta Sans\',\'Inter\',sans-serif;'
    new = 'background:#F4F6F9;min-height:100%;padding-bottom:100px;font-family:-apple-system,BlinkMacSystemFont,\'Plus Jakarta Sans\',\'Inter\',sans-serif;padding-top:0;'
    
    # Instead, fix in the JS: auto-dismiss notification when entering driver view
    # Find the driver_dashboard view function and add banner dismissal at start
    old_init = "let activeTrip = null;\n    try {\n      const tripRaw = localStorage.getItem('nukrop_active_trip');"
    new_init = """// Auto-dismiss notification banner in driver cockpit
    const alertBanner = document.getElementById('nukrop-alert-banner');
    if (alertBanner) alertBanner.style.display = 'none';

    let activeTrip = null;
    try {
      const tripRaw = localStorage.getItem('nukrop_active_trip');"""
    
    if old_init in text:
        text = text.replace(old_init, new_init, 1)
        print(f'{filepath}: Added banner auto-dismiss in driver_dashboard')
    else:
        print(f'{filepath}: Could not find init pattern to add banner dismiss')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f'  Saved {filepath}')

print('\nDone!')
