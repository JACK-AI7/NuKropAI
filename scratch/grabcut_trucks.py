import os
import glob
import cv2
import numpy as np
from PIL import Image

artifact_dir = r"C:\Users\bjasw\.gemini\antigravity\brain\36944d22-a0e5-4ba9-95b4-639674444ec9"

def grabcut_extract(img_path, margin=15):
    img = cv2.imread(img_path)
    h, w = img.shape[:2]
    
    # Initialize mask
    mask = np.zeros((h, w), np.uint8)
    
    # Background and foreground models
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    
    # Define rectangle: leave a margin around edges where we know it's pure background
    rect = (margin, margin, w - 2 * margin, h - 2 * margin)
    
    # Run GrabCut
    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    
    # Definite and probable foreground
    fg_mask = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype('uint8')
    
    # Remove floor shadow: in bottom 20%, if color is very bright gray (r, g, b all > 215)
    b, g, r = cv2.split(img)
    is_light_floor = (r > 200) & (g > 200) & (b > 200) & (np.abs(r.astype(int) - b.astype(int)) < 15)
    bottom_strip = np.zeros((h, w), dtype=bool)
    bottom_strip[int(h * 0.85):, :] = True
    fg_mask[is_light_floor & bottom_strip] = 0
    
    # Keep only the largest connected component in fg_mask (the truck itself)
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(fg_mask)
    if num_labels > 1:
        # Find largest component excluding background (label 0)
        largest_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
        fg_mask = np.where(labels == largest_label, 255, 0).astype('uint8')
        
    # Smooth edges
    alpha = cv2.GaussianBlur(fg_mask, (3, 3), 0)
    
    rgba = cv2.merge([r, g, b, alpha])
    pil_img = Image.fromarray(rgba)
    bbox = pil_img.getbbox()
    if bbox:
        pil_img = pil_img.crop(bbox)
        
    return pil_img

test_files = glob.glob(os.path.join(artifact_dir, "tata_ace_truck_*.jpg"))
if test_files:
    latest = sorted(test_files, key=os.path.getmtime)[-1]
    print(f"Running GrabCut on {latest}...")
    res = grabcut_extract(latest)
    res.save("images/trucks/tata_ace_test.png", "PNG")
    print(f"Saved images/trucks/tata_ace_test.png ({res.size})")
