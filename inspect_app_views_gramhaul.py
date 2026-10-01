import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'gramhaul:\s*function\s*\(\)\s*\{[\s\S]*?(?=\n\s*[a-zA-Z0-9_]+:\s*function|\n\};|$)', text)
if m:
    print("Found APP_VIEWS.gramhaul:")
    print(m.group(0)[:3000])
