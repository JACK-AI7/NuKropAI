import os

out = []
with open("test_uipolish.js", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if i < 7500 or i > 9710:
        continue
    if "`" in line:
        out.append(f"Line {i}: {line.strip()}")

with open("ticks.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
