import os
import re
import sys
import shutil

sys.stdout.reconfigure(encoding='utf-8')

import upgrade_functions as ufg

FILES = [
    'app/src/main/assets/index.html',
    'nukrop_emulator.html'
]

def apply_to_file(filepath):
    print(f"\nProcessing {filepath}...")
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found!")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    orig_len = len(content)
    print(f"Original length: {orig_len}")

    # 1. Replace renderTrackingSearchingState
    search_fn_start = content.find('function renderTrackingSearchingState(activeTrip) {')
    dispatched_fn_start = content.find('function renderTrackingDispatchedState(activeTrip) {')
    recenter_fn_start = content.find('function recenterTrackingMap() {')

    if search_fn_start == -1 or dispatched_fn_start == -1 or recenter_fn_start == -1:
        print("Error: Could not locate tracking functions boundaries!")
        return False

    new_searching = ufg.generate_searching_function() + "\n\n"
    new_dispatched = ufg.generate_dispatched_function() + "\n\n"

    # Replace searching & dispatched
    content = content[:search_fn_start] + new_searching + new_dispatched + content[recenter_fn_start:]
    print("Replaced renderTrackingSearchingState and renderTrackingDispatchedState.")

    # 2. Replace triggerDriverCall
    call_start = content.find('function triggerDriverCall(driverName, phone) {')
    if call_start != -1:
        # Find end of triggerDriverCall: next function is function endDriverLiveCall
        end_call_start = content.find('function endDriverLiveCall(', call_start)
        if end_call_start != -1:
            new_call = ufg.generate_call_function() + "\n\n"
            content = content[:call_start] + new_call + content[end_call_start:]
            print("Replaced triggerDriverCall.")
        else:
            print("Warning: Could not find function endDriverLiveCall boundary.")
    else:
        print("Warning: Could not find triggerDriverCall.")

    # 3. Replace openDriverLiveChatModal
    chat_start = content.find('function openDriverLiveChatModal(driverName, plate) {')
    if chat_start != -1:
        # next function is sendLiveHaulChatMessage
        send_start = content.find('function sendLiveHaulChatMessage() {', chat_start)
        if send_start != -1:
            new_chat = ufg.generate_chat_function() + "\n\n"
            content = content[:chat_start] + new_chat + content[send_start:]
            print("Replaced openDriverLiveChatModal.")
        else:
            print("Warning: Could not find sendLiveHaulChatMessage boundary.")
    else:
        print("Warning: Could not find openDriverLiveChatModal.")

    # 4. Replace Edit button in Screen 1
    # Target: ${TL('Edit ✏️', 'మార్చు ✏️', 'బదలెం ✏️')} or variations
    # Let's inspect what is inside openGramhaulPickupLocationModal button
    edit_btn_pattern = r'<button\s+onclick="openGramhaulPickupLocationModal\(\)"\s+style="background:#F0FDF4;[^>]*>\$\{TL\([^)]+\)\}</button>'
    new_edit_btn = '''<button onclick="openGramhaulPickupLocationModal()" style="background:#F0FDF4;color:#15803D;border:1px solid #BBF7D0;border-radius:10px;padding:5px 12px;font-size:11px;font-weight:900;cursor:pointer;flex-shrink:0;display:inline-flex;align-items:center;gap:5px;transition:all 0.15s ease;">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#15803D" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4C3.46957 4 2.96086 4.21071 2.58579 4.58579C2.21071 4.96086 2 5.46957 2 6V20C2 20.5304 2.21071 21.0391 2.58579 21.4142C2.96086 21.7893 3.46957 22 4 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V13M18.5 2.5C18.8978 2.10217 19.4374 1.87868 20 1.87868C20.5626 1.87868 21.1022 2.10217 21.5 2.5C21.8978 2.89783 22.1213 3.43739 22.1213 4C22.1213 4.56261 21.8978 5.10217 21.5 5.5L12 15L8 16L9 12L18.5 2.5Z"/></svg>
              <span>${TL('Edit', 'మార్చు', 'बदलें')}</span>
            </button>'''
    content, count_edit = re.subn(edit_btn_pattern, new_edit_btn, content)
    print(f"Replaced Edit button (matches: {count_edit})")

    # 5. Replace crop card Ready badge and chevron in Screen 1
    # Check for: <div style="font-size:11px;color:#16A34A;font-weight:800;margin-top:1px;">✓ Ready</div>
    ready_target = '<div style="font-size:11px;color:#16A34A;font-weight:800;margin-top:1px;">✓ Ready</div>'
    ready_replace = '''<div style="font-size:11px;color:#16A34A;font-weight:800;margin-top:1px;display:flex;align-items:center;gap:3px;">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" fill="#DCFCE7"/><path d="M8 12L11 15L16 9" stroke="#16A34A" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
                <span>Ready</span>
              </div>'''
    if ready_target in content:
        content = content.replace(ready_target, ready_replace)
        print("Replaced Ready badge in crop card.")

    # Replace chevron in crop card
    chevron_target = '<span style="font-size:10px;color:#16A34A;font-weight:800;flex-shrink:0;">▾</span>'
    chevron_replace = '''<span style="display:flex;align-items:center;color:#16A34A;flex-shrink:0;">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
              </span>'''
    if chevron_target in content:
        content = content.replace(chevron_target, chevron_replace)
        print("Replaced chevron in crop card.")

    # 6. Replace Booking button arrow in Screen 1
    book_target = '''<button id="gh-confirm-booking-btn" onclick="executeRealGramhaulDispatch()" style="width:100%;height:52px;background:linear-gradient(135deg,#16A34A,#15803D);color:#FFFFFF;border:none;border-radius:16px;font-size:16px;font-weight:900;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;box-shadow:0 8px 24px rgba(22,163,74,0.35);">
          <span>${TL('Request Mandi Truck Now', 'మండి ట్రక్కును బుక్ చేయండి', 'मंडी ट्रक बुक करें')}</span>
          <span>→</span>
        </button>'''
    book_replace = '''<button id="gh-confirm-booking-btn" onclick="executeRealGramhaulDispatch()" style="width:100%;height:52px;background:linear-gradient(135deg,#16A34A,#15803D);color:#FFFFFF;border:none;border-radius:16px;font-size:16px;font-weight:900;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:10px;box-shadow:0 8px 24px rgba(22,163,74,0.35);transition:all 0.2s cubic-bezier(0.16,1,0.3,1);">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none"><rect x="1" y="6" width="14" height="11" rx="2" fill="#FFFFFF"/><path d="M15 9H19L22 13V17H15V9Z" fill="#DCFCE7"/><circle cx="5.5" cy="17" r="2.2" fill="#15803D"/><circle cx="18.5" cy="17" r="2.2" fill="#15803D"/></svg>
          <span>${TL('Request Mandi Truck Now', 'మండి ట్రక్కును బుక్ చేయండి', 'మండి ట్రక్కును బుక్ చేయండి', 'मंडी ट्रक बुक करें')}</span>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
        </button>'''
    # Note: TL has signature TL(en, te, hi)
    book_replace_clean = '''<button id="gh-confirm-booking-btn" onclick="executeRealGramhaulDispatch()" style="width:100%;height:52px;background:linear-gradient(135deg,#16A34A,#15803D);color:#FFFFFF;border:none;border-radius:16px;font-size:16px;font-weight:900;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:10px;box-shadow:0 8px 24px rgba(22,163,74,0.35);transition:all 0.2s cubic-bezier(0.16,1,0.3,1);">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none"><rect x="1" y="6" width="14" height="11" rx="2" fill="#FFFFFF"/><path d="M15 9H19L22 13V17H15V9Z" fill="#DCFCE7"/><circle cx="5.5" cy="17" r="2.2" fill="#15803D"/><circle cx="18.5" cy="17" r="2.2" fill="#15803D"/></svg>
          <span>${TL('Request Mandi Truck Now', 'మండి ట్రక్కును బుక్ చేయండి', 'मंडी ट्रक बुक करें')}</span>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
        </button>'''
    if book_target in content:
        content = content.replace(book_target, book_replace_clean)
        print("Replaced Booking button.")

    # 7. Replace crop list checkmark in openGramhaulCropSelectorModal
    crop_check_target = '<div style="color:#16A34A;font-size:14px;font-weight:900;">✓</div>'
    crop_check_replace = '''<div style="display:flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:50%;background:#DCFCE7;">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
        </div>'''
    if crop_check_target in content:
        content = content.replace(crop_check_target, crop_check_replace)
        print("Replaced crop list checkmark.")

    # 8. Replace invoice modal emoji
    # <div style="width:44px;height:44px;border-radius:14px;background:#DCFCE7;display:flex;align-items:center;justify-content:center;font-size:22px;">🧾</div>
    inv_emoji = '<div style="width:44px;height:44px;border-radius:14px;background:#DCFCE7;display:flex;align-items:center;justify-content:center;font-size:22px;">🧾</div>'
    inv_svg = '''<div style="width:44px;height:44px;border-radius:14px;background:#DCFCE7;display:flex;align-items:center;justify-content:center;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><line x1="10" y1="9" x2="8" y2="9"/></svg>
          </div>'''
    if inv_emoji in content:
        content = content.replace(inv_emoji, inv_svg)
        print("Replaced invoice modal emoji.")

    # 9. Replace driver history modal truck emoji
    # <div style="width:44px;height:44px;border-radius:14px;background:#FEF9C3;display:flex;align-items:center;justify-content:center;font-size:22px;">🚚</div>
    hist_emoji = '<div style="width:44px;height:44px;border-radius:14px;background:#FEF9C3;display:flex;align-items:center;justify-content:center;font-size:22px;">🚚</div>'
    hist_svg = '''<div style="width:44px;height:44px;border-radius:14px;background:#DCFCE7;display:flex;align-items:center;justify-content:center;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none"><rect x="1" y="6" width="14" height="11" rx="2" fill="#16A34A"/><path d="M15 9H19L22 13V17H15V9Z" fill="#15803D"/><circle cx="5.5" cy="17" r="2.2" fill="#0F172A"/><circle cx="18.5" cy="17" r="2.2" fill="#0F172A"/></svg>
          </div>'''
    if hist_emoji in content:
        content = content.replace(hist_emoji, hist_svg)
        print("Replaced history modal emoji.")

    # 10. Replace history modal crop list items with rich colored SVGs
    hist_crop_old = """['🌾 Cotton 40 Qtl','Kadipikonda → Warangal Enamamula APMC','₹1,450 · Completed'],
          ['🌶️ Teja Chilli 25 Qtl','Hasanparthy → Warangal Enamamula APMC','₹980 · Completed'],
          ['🌾 Paddy 35 Qtl','Geesukonda → Enumamula Mandi Hub','₹1,250 · Completed'],
          ['🌽 Maize 50 Qtl','Narsampet → Jangaon APMC Yard','₹1,890 · Completed']"""

    hist_crop_new = """[`<div style="display:flex;align-items:center;gap:6px;"><div style="width:20px;height:20px;flex-shrink:0;">${getCropIconImg(null, 'cotton')}</div><span>Cotton 40 Qtl</span></div>`,'Kadipikonda → Warangal Enamamula APMC','₹1,450 · Completed'],
          [`<div style="display:flex;align-items:center;gap:6px;"><div style="width:20px;height:20px;flex-shrink:0;">${getCropIconImg(null, 'chilli')}</div><span>Teja Chilli 25 Qtl</span></div>`,'Hasanparthy → Warangal Enamamula APMC','₹980 · Completed'],
          [`<div style="display:flex;align-items:center;gap:6px;"><div style="width:20px;height:20px;flex-shrink:0;">${getCropIconImg(null, 'rice')}</div><span>Paddy 35 Qtl</span></div>`,'Geesukonda → Enumamula Mandi Hub','₹1,250 · Completed'],
          [`<div style="display:flex;align-items:center;gap:6px;"><div style="width:20px;height:20px;flex-shrink:0;">${getCropIconImg(null, 'corn')}</div><span>Maize 50 Qtl</span></div>`,'Narsampet → Jangaon APMC Yard','₹1,890 · Completed']"""

    # We can do this replacement by finding the array block
    if "['🌾 Cotton 40 Qtl'" in content:
        content = content.replace(
            "['🌾 Cotton 40 Qtl'",
            "[`<div style=\"display:flex;align-items:center;gap:6px;\"><div style=\"width:20px;height:20px;flex-shrink:0;\">${getCropIconImg(null, 'cotton')}</div><span>Cotton 40 Qtl</span></div>`"
        )
        content = content.replace(
            "['🌶️ Teja Chilli 25 Qtl'",
            "[`<div style=\"display:flex;align-items:center;gap:6px;\"><div style=\"width:20px;height:20px;flex-shrink:0;\">${getCropIconImg(null, 'chilli')}</div><span>Teja Chilli 25 Qtl</span></div>`"
        )
        content = content.replace(
            "['🌾 Paddy 35 Qtl'",
            "[`<div style=\"display:flex;align-items:center;gap:6px;\"><div style=\"width:20px;height:20px;flex-shrink:0;\">${getCropIconImg(null, 'rice')}</div><span>Paddy 35 Qtl</span></div>`"
        )
        content = content.replace(
            "['🌽 Maize 50 Qtl'",
            "[`<div style=\"display:flex;align-items:center;gap:6px;\"><div style=\"width:20px;height:20px;flex-shrink:0;\">${getCropIconImg(null, 'corn')}</div><span>Maize 50 Qtl</span></div>`"
        )
        print("Replaced history modal crop items with colored SVG icons.")

    # 11. Replace history modal export button emoji
    hist_exp_old = '📥 Export Full GST Ledger (CSV)'
    hist_exp_new = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block;vertical-align:middle;margin-right:4px;"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>Export Full GST Ledger (CSV)'
    if hist_exp_old in content:
        content = content.replace(hist_exp_old, hist_exp_new)
        print("Replaced history modal export button icon.")

    # 12. Replace side nav btn-gramhaul
    btn_gh_old = '🚚 Mandi Truck Sharing'
    btn_gh_new = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" style="vertical-align:middle;margin-right:6px;"><rect x="1" y="6" width="14" height="11" rx="2" fill="currentColor"/><path d="M15 9H19L22 13V17H15V9Z" fill="currentColor"/><circle cx="5.5" cy="17" r="2.2" fill="#FFFFFF"/><circle cx="18.5" cy="17" r="2.2" fill="#FFFFFF"/></svg>Mandi Truck Sharing'
    if btn_gh_old in content:
        content = content.replace(btn_gh_old, btn_gh_new)
        print("Replaced side nav btn-gramhaul icon.")

    # Save upgraded file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Successfully updated {filepath}. New length: {len(content)} (diff: {len(content) - orig_len})")
    return True

for f in FILES:
    apply_to_file(f)

print("\nAll files updated.")
