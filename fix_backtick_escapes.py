import sys, re
sys.stdout.reconfigure(encoding='utf-8')

for filepath in ['app/src/main/assets/index.html', 'nukrop_emulator.html']:
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Fix escaped backtick -> real backtick in JS template literals
    # The Python string had \` which got written as \\` in the file
    before = text.count('return \\`')
    text = text.replace('return \\`', 'return `')
    after = text.count('return \\`')
    print(f'{filepath}: fixed {before - after} return backtick(s)')

    # Fix the closing \`; -> `;
    bc = text.count('\\`;')
    text = text.replace('\\`;', '`;')
    print(f'{filepath}: fixed {bc} closing backtick(s)')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f'Saved {filepath}')
