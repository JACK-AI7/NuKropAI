import re

with open(r"C:\Users\bjasw\.gemini\antigravity\brain\36944d22-a0e5-4ba9-95b4-639674444ec9\walkthrough.md", "r", encoding="utf-8") as f:
    content = f.read()

# Add the new screenshots into the carousel
new_slides = """<!-- slide -->
![10. Design System Applied - Home Screen](/C:/Users/bjasw/.gemini/antigravity/brain/36944d22-a0e5-4ba9-95b4-639674444ec9/qa_post_color_home.png)
<!-- slide -->
![11. Design System Applied - Market Screen](/C:/Users/bjasw/.gemini/antigravity/brain/36944d22-a0e5-4ba9-95b4-639674444ec9/qa_post_color_market.png)
<!-- slide -->
![12. Design System Applied - Scanner Screen](/C:/Users/bjasw/.gemini/antigravity/brain/36944d22-a0e5-4ba9-95b4-639674444ec9/qa_post_color_scanner.png)
````"""
content = content.replace("````\n\n---", new_slides + "\n\n---")

# Add a row to the table
new_row = """| **Design System & Typography** | 1,470+ hardcoded hex colors (`#1B5E20`, etc.), arbitrary padding, and flat shadows scattered across HTML strings. | Injected Central CSS Custom Properties (`:root` Master Color System) and surgically replaced colors via automated Python script. Standardized hierarchy and spacing. | ✅ **FIXED** |
"""

# Inject before the route aliases row to keep it in the table
content = content.replace("| **Route Aliases**", new_row + "| **Route Aliases**")

with open(r"C:\Users\bjasw\.gemini\antigravity\brain\36944d22-a0e5-4ba9-95b4-639674444ec9\walkthrough.md", "w", encoding="utf-8") as f:
    f.write(content)
