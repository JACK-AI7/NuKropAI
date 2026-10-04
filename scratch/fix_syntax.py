import re
import subprocess

file_path = "app/src/main/assets/index.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Fix literal \' inside TL calls
content = content.replace("TL(\\'Kisan Community\\'", "TL('Kisan Community'")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Replacement done. Now validating JS syntax across all scripts...")
