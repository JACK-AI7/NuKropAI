import re
import os

app_path = "web/src/App.tsx"
hero_path = "web/src/components/Hero.tsx"

with open(app_path, "r", encoding="utf-8") as f:
    app_code = f.read()

# Remove iOS button block
app_code = re.sub(
    r"<button className=\"nukrop-btn nukrop-btn-secondary\"[^>]+>\s*<Apple[^>]+/>\s*<span>Download for iOS</span>\s*</button>", 
    "", 
    app_code
)

# Remove the entire section "Ready to transform your farm?"
app_code = re.sub(
    r"<section style=\{\{\s*padding:\s*'80px 24px'[^>]+>.*?Ready to transform your farm.*?</section>",
    "",
    app_code,
    flags=re.DOTALL
)

with open(app_path, "w", encoding="utf-8") as f:
    f.write(app_code)


with open(hero_path, "r", encoding="utf-8") as f:
    hero_code = f.read()

hero_code = re.sub(
    r"<button className=\"nukrop-btn nukrop-btn-secondary\"[^>]+>\s*<Apple[^>]+/>\s*Download for iOS\s*</button>",
    "",
    hero_code
)

with open(hero_path, "w", encoding="utf-8") as f:
    f.write(hero_code)

print("Website cleaned up successfully")
