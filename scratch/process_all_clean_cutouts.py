import os
import glob
import cv2
import numpy as np
from PIL import Image

def clean_cutout(img_path, margin=10):
    img = cv2.imread(img_path)
    h, w = img.shape[:2]
    
    # 1. GrabCut initialization
    mask = np.zeros((h, w), np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    rect = (margin, margin, w - 2 * margin, h - 2 * margin)
    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 4, cv2.GC_INIT_WITH_RECT)
    
    fg_mask = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype('uint8')
    
    # 2. Post-clean: any near-white (r, g, b > 230) that touches the image border or is above the truck
    b, g, r = cv2.split(img)
    is_white = (r >= 230) & (g >= 230) & (b >= 230)
    
    # Floodfill from top border on is_white
    flood = np.zeros((h + 2, w + 2), np.uint8)
    white_u8 = is_white.astype(np.uint8) * 255
    for x in range(0, w, 10):
        if white_u8[0, x] == 255 and flood[1, x + 1] == 0:
            cv2.floodFill(white_u8, flood, (x, 0), 0, flags=8 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY)
        if white_u8[h - 1, x] == 255 and flood[h, x + 1] == 0:
            cv2.floodFill(white_u8, flood, (x, h - 1), 0, flags=8 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY)
    for y in range(0, h, 10):
        if white_u8[y, 0] == 255 and flood[y + 1, 1] == 0:
            cv2.floodFill(white_u8, flood, (0, y), 0, flags=8 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY)
        if white_u8[y, w - 1] == 255 and flood[y + 1, w] == 0:
            cv2.floodFill(white_u8, flood, (w - 1, y), 0, flags=8 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY)
            
    border_white = (flood[1:h+1, 1:w+1] == 255)
    fg_mask[border_white] = 0
    
    # Remove floor shadow: in bottom 18% of image, if color is light grayish floor
    diff = np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)
    is_gray_floor = (r > 185) & (g > 185) & (b > 185) & (diff < 15)
    bottom_zone = np.zeros((h, w), dtype=bool)
    bottom_zone[int(h * 0.82):, :] = True
    fg_mask[is_gray_floor & bottom_zone] = 0
    
    # Keep largest connected component
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(fg_mask)
    if num_labels > 1:
        largest_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
        fg_mask = np.where(labels == largest_label, 255, 0).astype('uint8')
        
    alpha = cv2.GaussianBlur(fg_mask, (3, 3), 0)
    rgba = cv2.merge([r, g, b, alpha])
    
    pil_img = Image.fromarray(rgba)
    bbox = pil_img.getbbox()
    if bbox:
        pil_img = pil_img.crop(bbox)
        
    # Resize to standard card aspect: max width 360, max height 220
    target_w = 340
    target_h = int(pil_img.height * (target_w / pil_img.width))
    pil_img = pil_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    return pil_img

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

for key, pattern in truck_defs:
    files = glob.glob(os.path.join(artifact_dir, pattern))
    if not files:
        print(f"File not found: {pattern}")
        continue
    files.sort(key=os.path.getmtime)
    f = files[-1]
    print(f"Processing {key} from {f}...")
    cutout = clean_cutout(f)
    for d in dest_dirs:
        out_p = os.path.join(d, f"{key}.png")
        cutout.save(out_p, "PNG", optimize=True)
        print(f"  Saved {out_p} ({cutout.size}, {os.path.getsize(out_p)} bytes)")

print("\nAll 5 trucks processed into transparent PNGs.")
