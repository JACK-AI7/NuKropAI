import re

with open("app/src/main/assets/index.html", "r", encoding="utf-8") as f:
    content = f.read()

match = re.search(r"<script>([\s\S]*?)</script>", content)
if match:
    with open("test4.js", "w", encoding="utf-8") as f:
        f.write(match.group(1))
