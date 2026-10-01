import os

with open("test_uipolish.js", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if i < 7500 or i > 9710:
        continue
    if "`" in line:
        print(f"Line {i}: {line.strip()}")
