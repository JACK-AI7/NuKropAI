import os, sys

sys.stdout.reconfigure(encoding='utf-8')

for path in ['app/src/main/assets/index.html', 'nukrop_emulator.html']:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    marker1 = "openScreen('home', null);\n    }\n  }\n}"
    marker2 = "/* ══════════════════════════════════════════════════════════════\n   GRAMHAUL: REAL GPS"

    idx1 = content.find(marker1)
    idx2 = content.find(marker2)

    if idx1 != -1 and idx2 != -1 and idx1 < idx2:
        content = content[:idx1 + len(marker1)] + '\n\n' + content[idx2:]
        print(f"Cleaned {path}!")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
