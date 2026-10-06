import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', encoding='utf-8') as f:
    text = f.read()

# Let's collect all modal elements
modal_ids = sorted(list(set(re.findall(r'id=["\']([a-zA-Z0-9_\-]+modal[a-zA-Z0-9_\-]*)["\']', text, re.IGNORECASE))))
print(f"Total static/template modal IDs found in index.html: {len(modal_ids)}")
for mid in modal_ids:
    print(f"  - {mid}")

# Check key modals required for M2
m2_modals = ['driver-otp-verification-modal', 'driver-payment-collection-modal', 'gramhaul-crop-modal']
for m in m2_modals:
    assert m in text, f"Missing M2 modal: {m}"
print("\nAll Milestone 2 target modals verified present!")
