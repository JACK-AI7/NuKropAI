import os
import glob
import cv2
import numpy as np
from PIL import Image

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

def make_transparent_cutout(img_path, threshold_val=238):
    # Read image with OpenCV
    img = cv2.imread(img_path)
    h, w = img.shape[:2]
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Binary mask of non-white
    # Studio background is high brightness (> 230) and low saturation
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    sat = hsv[:, :, 1]
    val = hsv[:, :, 2]
    
    # Background: high value and low saturation
    # We floodFill from all 4 corners and along the borders to only remove the external background
    # (avoiding white cabins inside)
    # Create a mask for floodFill: size (h+2, w+2)
    flood_mask = np.zeros((h + 2, w + 2), np.uint8)
    
    # We create a floodfill copy
    flood_img = gray.copy()
    
    # Seed points along top, bottom, left, right borders
    seed_points = []
    for x in range(0, w, 20):
        seed_points.append((x, 0))
        seed_points.append((x, h - 1))
    for y in range(0, h, 20):
        seed_points.append((0, y))
        seed_points.append((w - 1, y))
        
    for pt in seed_points:
        if gray[pt[1], pt[0]] > 180 and flood_mask[pt[1] + 1, pt[0] + 1] == 0:
            cv2.floodFill(flood_img, flood_mask, pt, 0, loDiff=15, upDiff=15, flags=8 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY)
            
    # The external background is in flood_mask[1:h+1, 1:w+1] == 255
    bg_mask = (flood_mask[1:h+1, 1:w+1] == 255)
    
    # Also clean up soft floor shadow near bottom if connected to background
    # Floor shadow: in the bottom 25% of image, if gray > 180 and sat < 25
    bottom_zone = int(h * 0.72)
    floor_candidate = (gray > 175) & (sat < 28)
    # Only expand into floor shadow
    kernel = np.ones((5, 5), np.uint8)
    dilated_bg = cv2.dilate(bg_mask.astype(np.uint8), kernel, iterations=2)
    bg_mask = bg_mask | ((dilated_bg == 1) & floor_candidate & (np.arange(h)[:, None] > bottom_zone))
    
    # Alpha channel: 0 where bg, 255 where foreground
    alpha = np.where(bg_mask, 0, 255).astype(np.uint8)
    
    # Smooth alpha edges with slight gaussian blur for feathering
    alpha_blurred = cv2.GaussianBlur(alpha, (3, 3), 0)
    
    # Create RGBA
    b, g, r = cv2.split(img)
    rgba = cv2.merge([r, g, b, alpha_blurred])
    
    pil_img = Image.fromarray(rgba)
    bbox = pil_img.getbbox()
    if bbox:
        pil_img = pil_img.crop(bbox)
        
    return pil_img

for key, pattern in truck_defs:
    files = glob.glob(os.path.join(artifact_dir, pattern))
    if not files:
        continue
    files.sort(key=os.path.getmtime)
    latest_file = files[-1]
    print(f"Creating clean transparent cutout for {key} from {latest_file}...")
    
    proc_img = make_transparent_cutout(latest_file)
    w, h = proc_img.size
    target_w = 420
    target_h = int(h * (target_w / w))
    proc_img = proc_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    for d in dest_dirs:
        out_path = os.path.join(d, f"{key}.png")
        proc_img.save(out_path, "PNG", optimize=True)
        print(f"  -> Saved {out_path} ({os.path.getsize(out_path)} bytes)")

print("\nDone creating transparent cutouts.")
