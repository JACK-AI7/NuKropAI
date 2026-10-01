import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'function (?:renderGramhaul|initGramhaulOpenStreetMap|getGramhaulTrucksHtml)[\s\S]*?(?=\nfunction [a-zA-Z0-9_]+\s*\(|\n</script>|$)', text)
if m:
    print("Found GramHaul function:")
    print(m.group(0)[:2500])
