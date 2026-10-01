import os

files = ['app/src/main/assets/index.html', 'nukrop_emulator.html']
for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Find driver init function or just the spot where driver logs in.
    # We can inject the listener when driver dashboard is rendered.
    # Search for "driver_dashboard: () => {"
    idx = text.find('driver_dashboard: () => {')
    if idx != -1:
        # We can add a script block to start listening, or just put it in a setTimeout
        listen_script = """setTimeout(() => {
        if (typeof nk_subscribeToHaulRequests !== 'undefined') {
            nk_subscribeToHaulRequests('GH-4192', (payload) => {
                console.log("DRIVER RECEIVED REALTIME HAUL REQUEST:", payload);
                localStorage.setItem('gh_haul_request', JSON.stringify(payload));
                // Force driver screen to re-render to show request sheet
                if (window.currentAppScreen === 'driver_dashboard') {
                    openScreen('driver_dashboard');
                    if (typeof showLuxuryToast === 'function') {
                        showLuxuryToast('🔔 New Haul Request from Farmer!', 'success');
                    }
                }
            });
            // Also start broadcasting GPS
            nk_startDriverLocationBroadcast('GH-4192', 17.9689, 79.5941);
        }
    }, 1000);"""
        
        # Insert after "const activeTab    = localStorage.getItem('gh_driver_tab') || 'map';"
        insert_idx = text.find("const activeTab    = localStorage.getItem('gh_driver_tab') || 'map';", idx)
        if insert_idx != -1:
            insert_idx += len("const activeTab    = localStorage.getItem('gh_driver_tab') || 'map';")
            text = text[:insert_idx] + "\n    " + listen_script + text[insert_idx:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

print("Driver listeners injected.")
