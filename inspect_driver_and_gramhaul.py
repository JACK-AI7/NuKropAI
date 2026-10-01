import sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'driver_dashboard:\s*\(\)\s*=>\s*\{([\s\S]*?)\n\s*\},', text)
if m:
    content = m.group(1)
    print("Driver Dashboard view length:", len(content))
    # print the active trip section
    active_trip_m = re.search(r'<!-- 1\. Live Assigned Active Trip[^>]*-->([\s\S]*?)<!-- [23]\.', content)
    if active_trip_m:
        print("=== ACTIVE TRIP SECTION ===")
        print(active_trip_m.group(1)[:1200])
    else:
        print("No exact active trip comment, printing first 2000 chars:")
        print(content[:2000])
