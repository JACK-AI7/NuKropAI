import glob, re

for fpath in glob.glob('app/src/main/assets/*.bak*'):
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    m = re.search(r'function openScreen\s*\([^)]*\)\s*\{[\s\S]*?(?=\nfunction |\n</script>|$)', c)
    if m:
        print(f"Found openScreen in {fpath}:")
        print(m.group(0)[:800])
        print("="*40)
        break
