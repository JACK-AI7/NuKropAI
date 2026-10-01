files = ['app/src/main/assets/index.html', 'nukrop_emulator.html']
for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    text = text.replace('<div style="width:64px;height:64px;border-radius:20px;background:var(--r-yellow);', 
                        '<div style="width:64px;height:64px;border-radius:50%;background:var(--r-yellow);')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
print('Driver profile avatar fixed')
