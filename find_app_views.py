import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'const APP_VIEWS\s*=\s*\{[\s\S]*?(?=\n\};|\nconst |\nlet |\nfunction )', text)
if m:
    print("Found APP_VIEWS keys:")
    keys = re.findall(r'([a-zA-Z0-9_]+)\s*:\s*(?:function|\()', m.group(0))
    print(keys)
