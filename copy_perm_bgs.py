import os, shutil

src_dir = r"C:\Users\bjasw\.gemini\antigravity\brain\36944d22-a0e5-4ba9-95b4-639674444ec9"
dst_assets = r"app\src\main\assets\images"
dst_root = r"images"

os.makedirs(dst_assets, exist_ok=True)
os.makedirs(dst_root, exist_ok=True)

mapping = {
    'perm_bg_camera_leaf_scan_1790880572961.jpg': 'perm_bg_camera.jpg',
    'perm_bg_gps_mandi_radar_1790880597447.jpg': 'perm_bg_location.jpg',
    'onboard_ai_voice_weather.jpg': 'perm_bg_notification.jpg'
}

for src_name, dst_name in mapping.items():
    s = os.path.join(src_dir, src_name) if os.path.exists(os.path.join(src_dir, src_name)) else os.path.join(dst_assets, src_name)
    if os.path.exists(s):
        shutil.copy2(s, os.path.join(dst_assets, dst_name))
        shutil.copy2(s, os.path.join(dst_root, dst_name))
        print(f"Copied: {dst_name} ({os.path.getsize(s)} bytes)")
    else:
        print(f"Missing: {src_name}")
