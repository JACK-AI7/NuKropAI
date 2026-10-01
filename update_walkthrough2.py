import re

with open(r"C:\Users\bjasw\.gemini\antigravity\brain\36944d22-a0e5-4ba9-95b4-639674444ec9\walkthrough.md", "r", encoding="utf-8") as f:
    content = f.read()

# Add a section detailing the State Fix and the UI Simplification
new_section = """
## 🚨 CRITICAL CORRECTIONS (Premium & Coherent UI Update)

| Component / System | Issue Identified | Surgical Fix Applied | Status |
|---|---|---|---|
| **App Startup State Bug** | The app shell (Home, Nav) was rendering simultaneously underneath the Splash/Onboarding overlays. | Wrapped the entire app shell in `#app-shell` (`display:none` by default). Now, **only one primary state** controls the viewport. | ✅ **FIXED** |
| **Typography Hierarchy** | `font-weight: 900` was used over 340 times, creating a "shouty" interface. | Downgraded ultra-bold text to Semibold (`600`) and Medium (`500`). Established a calm, precise typographical hierarchy. | ✅ **FIXED** |
| **Visual Noise / Overdesign** | Bubbly pills (`border-radius: 40px+`), excessive shadows (`40px` blur), and unnecessary gradients. | Stripped non-semantic gradients. Flattened shadows to subtle 1px-4px elevation. Squared off extreme pill radii to clean `8px`-`16px` curves. | ✅ **FIXED** |

---
"""

content = content.replace("## 🎨 Summary of Surgical Polish Applied", new_section + "## 🎨 Summary of Surgical Polish Applied")

# Add the new clean screenshots to the carousel
new_slides = """<!-- slide -->
![13. Clean UI Update - Startup Overlay Isolation](/C:/Users/bjasw/.gemini/antigravity/brain/36944d22-a0e5-4ba9-95b4-639674444ec9/qa_startup_1_splash.png)
<!-- slide -->
![14. Clean UI Update - Typography & Flat Shadows (Home)](/C:/Users/bjasw/.gemini/antigravity/brain/36944d22-a0e5-4ba9-95b4-639674444ec9/qa_post_color_home.png)
<!-- slide -->
![15. Clean UI Update - Typography & Flat Shadows (Market)](/C:/Users/bjasw/.gemini/antigravity/brain/36944d22-a0e5-4ba9-95b4-639674444ec9/qa_post_color_market.png)
````"""
content = content.replace("````\n\n---", new_slides + "\n\n---")

with open(r"C:\Users\bjasw\.gemini\antigravity\brain\36944d22-a0e5-4ba9-95b4-639674444ec9\walkthrough.md", "w", encoding="utf-8") as f:
    f.write(content)
