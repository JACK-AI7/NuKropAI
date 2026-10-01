import sys

sys.stdout.reconfigure(encoding='utf-8')

def fix_comma(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace("  `;\n}\n  \n  \n  agristack: () => {", "  `;\n},\n  \n  agristack: () => {")
    content = content.replace("  `;\n}\n  agristack: () => {", "  `;\n},\n  agristack: () => {")
    content = content.replace("  `;\n}\nagristack: () => {", "  `;\n},\nagristack: () => {")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed comma in {path}")

fix_comma('app/src/main/assets/index.html')
fix_comma('nukrop_emulator.html')
