import sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('nukrop_emulator.html', 'r', encoding='utf-8') as f:
    text = f.read()

def print_func(name):
    m = re.search(r'function ' + name + r'[\s\S]*?(?=\nfunction |\n</script>|$)', text)
    if m:
        print(f"=== {name} ===")
        print(m.group(0)[:1500])
        print("="*40)

print_func('handleGuestLogin')
print_func('completeGoogleAuth')
print_func('executeSignOutToLogin')
