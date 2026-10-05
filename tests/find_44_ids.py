import subprocess
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

res = subprocess.run(['git', 'show', 'HEAD~1:app/src/main/assets/index.html'], capture_output=True, text=True, encoding='utf-8')
old_html = res.stdout

lines = old_html.splitlines()

searched_ids = set()
patterns = [
    r"getElementById\(['\"]([a-zA-Z0-9_-]+)['\"]\)",
    r"safeSetText\(['\"]([a-zA-Z0-9_-]+)['\"]",
    r"safeSetHtml\(['\"]([a-zA-Z0-9_-]+)['\"]",
    r"querySelector\(['\"]#([a-zA-Z0-9_-]+)['\"]\)"
]

for line in lines:
    for pat in patterns:
        for m in re.finditer(pat, line):
            searched_ids.add(m.group(1))

defined_ids = set()
for line in lines:
    for m in re.finditer(r"id=['\"]([a-zA-Z0-9_-]+)['\"]", line):
        defined_ids.add(m.group(1))

missing = sorted(searched_ids - defined_ids)
print(f"Total missing in HEAD~1 ({len(missing)}):")
for m in missing:
    print(f"  '{m}',")
