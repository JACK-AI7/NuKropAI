import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

def find_func(name):
    m = re.search(r'function ' + name + r'[\s\S]*?(?=\nfunction |\n</script>|$)', text)
    if m:
        print(f'=== {name} ===')
        print(m.group(0))
        print('----------------------------------------\n')

find_func('renderSplashScreen')
find_func('checkAndTriggerOnboarding')
find_func('openOnboardingFlow')
find_func('renderLoginScreen')
find_func('openInAppGoogleAuthModal')
find_func('selectGoogleAccount')
find_func('promptForCustomGoogleAccount')
