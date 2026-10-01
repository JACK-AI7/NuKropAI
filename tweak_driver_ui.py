import os

files = ['app/src/main/assets/index.html', 'nukrop_emulator.html']
for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Change color to Neon Lime
    text = text.replace('--r-yellow:#FFCA20;', '--r-yellow:#C6FF00;')

    # 2. Make driver avatar circle
    old_avatar = '<div style="width:72px;height:72px;background:var(--r-yellow);border-radius:18px;display:flex;align-items:center;justify-content:center;font-size:32px;font-weight:900;color:var(--r-dark);box-shadow:0 4px 20px rgba(0,0,0,0.2);\">S</div>'
    new_avatar = old_avatar.replace('border-radius:18px', 'border-radius:50%')
    text = text.replace(old_avatar, new_avatar)

    # 3. Move the floating toggle to the top of the bottom navbar and hide it when activeTrip exists
    old_toggle_start = text.find('<!-- ── ONLINE/OFFLINE big pill (Rapido style — bottom, above request sheet) ── -->')
    if old_toggle_start != -1:
        old_toggle_end = text.find('</div>', old_toggle_start + 100)
        old_toggle_end = text.find('</div>', old_toggle_end + 1)
        old_toggle_end = text.find('</div>', old_toggle_end + 1)
        old_toggle_end += 6 # include </div>

        # Remove it from the current location
        text = text[:old_toggle_start] + text[old_toggle_end:]

        # Insert it inside the bottomNav div
        bottom_nav_marker = '<div style="position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:430px;background:#FFFFFF;'
        idx = text.find(bottom_nav_marker)
        
        if idx != -1:
            idx = text.find('>', idx) + 1
            new_toggle = """
      ${(!activeTrip && activeTab === 'map') ? `
      <!-- CENTERED ON DUTY TOGGLE -->
      <div style="position:absolute; top:-28px; left:50%; transform:translateX(-50%);">
        <button class="r-btn ${isOnline ? 'r-online-pulse' : ''}" onclick="toggleGhDriverOnline()" style="display:flex;align-items:center;gap:10px;background:${isOnline ? 'var(--r-dark)' : '#FFFFFF'};border:2px solid ${isOnline ? 'var(--r-yellow)' : '#E5E7EB'};border-radius:100px;padding:8px 16px 8px 8px;box-shadow:0 6px 20px rgba(0,0,0,0.15);cursor:pointer; height:46px;">
          <div style="width:28px;height:28px;border-radius:50%;background:${isOnline ? 'var(--r-yellow)' : '#F3F4F6'};display:flex;align-items:center;justify-content:center;">
            ${isOnline
              ? `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--r-dark)" stroke-width="3" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>`
              : `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#6B7280" stroke-width="2.5" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>`
            }
          </div>
          <div style="text-align:left;">
            <div style="font-size:14px;font-weight:900;color:${isOnline ? 'var(--r-yellow)' : 'var(--r-dark)'};letter-spacing:-0.2px;line-height:1.2;">${isOnline ? 'On Duty' : 'Go Online'}</div>
          </div>
        </button>
      </div>
      ` : ''}
            """
            text = text[:idx] + new_toggle + text[idx:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

print('Driver UI enhancements applied!')
