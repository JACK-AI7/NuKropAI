import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

def print_section(start_kw, length=2000):
    idx = text.find(start_kw)
    if idx != -1:
        print(f"=== SECTION: {start_kw} (pos {idx}) ===")
        print(text[idx:idx+length])
        print("\n" + "="*50 + "\n")
    else:
        print(f"Keyword '{start_kw}' not found")

print_section('function renderSplashScreen', 1200)
print_section('function openOnboardingFlow', 1500)
print_section('function renderLoginScreen', 2000)
print_section('function renderCameraPermissionScreen', 1500)
