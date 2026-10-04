import os
import glob
from PIL import Image
import numpy as np

# Find the latest generated images in artifact directory
artifact_dir = r"C:\Users\bjasw\.gemini\antigravity\brain\36944d22-a0e5-4ba9-95b4-639674444ec9"

truck_defs = [
    ("tata_ace", "tata_ace_truck_*.jpg"),
    ("bolero_maxi", "bolero_maxi_truck_*.jpg"),
    ("ashok_leyland_dost", "ashok_leyland_dost_*.jpg"),
    ("tata_407", "tata_407_truck_*.jpg"),
    ("eicher_pro", "eicher_pro_truck_*.jpg")
]

dest_dirs = [
    r"app/src/main/assets/images/trucks",
    r"web/public/images/trucks",
    r"images/trucks"
]

for d in dest_dirs:
    os.makedirs(d, exist_ok=True)

def remove_white_background(img, threshold=240, feather=15):
    # Convert to RGBA
    img = img.convert("RGBA")
    data = np.array(img)
    
    # Calculate brightness / whiteness
    r, g, b, a = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]
    
    # Check if pixel is near-white or light gray studio floor
    # We want to remove the white studio background: r > threshold and g > threshold and b > threshold
    # Also handle soft floor shadow: difference between max and min channel is low (grayish)
    diff = np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)
    is_white_bg = (r >= 235) & (g >= 235) & (b >= 235) & (diff < 20)
    
    # Floor soft shadow: near the bottom, very light gray
    is_floor = (r >= 210) & (g >= 210) & (b >= 210) & (diff < 15)
    
    # Use flood fill / distance mask from top-left, top-right, bottom-left, bottom-right
    # Let's use simple alpha calculation:
    # Whiteness index: min(r, g, b)
    whiteness = np.minimum(np.minimum(r, g), b)
    alpha = np.where(is_white_bg, 0, 255).astype(np.uint8)
    
    # Feather edge:
    mask = (whiteness >= 225) & (diff < 20)
    fade = np.clip((245 - whiteness) / 20.0 * 255, 0, 255).astype(np.uint8)
    alpha[mask] = fade[mask]
    
    data[:, :, 3] = alpha
    result = Image.fromarray(data)
    
    # Autocrop to bounding box of non-transparent pixels
    bbox = result.getbbox()
    if bbox:
        result = result.crop(bbox)
        
    return result

for key, pattern in truck_defs:
    files = glob.glob(os.path.join(artifact_dir, pattern))
    if not files:
        print(f"No file found for {key} with pattern {pattern}")
        continue
    # Pick latest
    files.sort(key=os.path.getmtime)
    latest_file = files[-1]
    print(f"Processing {key} from {latest_file}...")
    
    raw_img = Image.open(latest_file)
    proc_img = remove_white_background(raw_img)
    
    # Resize to reasonable dimensions for web/mobile UI (max width 600px, high DPI crisp)
    w, h = proc_img.size
    target_w = 480
    target_h = int(h * (target_w / w))
    proc_img = proc_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    for d in dest_dirs:
        out_path = os.path.join(d, f"{key}.png")
        proc_img.save(out_path, "PNG", optimize=True)
        print(f"Saved {out_path} ({os.path.getsize(out_path)} bytes)")

print("\nAll truck transparent PNGs generated successfully.")
