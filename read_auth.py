import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()
idx = text.find('async function supabaseSignIn')
print(text[idx-500:idx+2000])
