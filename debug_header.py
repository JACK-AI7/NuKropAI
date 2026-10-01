import sys, re
sys.stdout.reconfigure(encoding='utf-8')

# The broken polygon is the truck SVG: <polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/>
# This is missing the stroke and fill attrs so browser complains
# Let's find exactly which instance and fix it

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix broken truck icon SVG - the polygon needs stroke/fill attrs consistent
# The error says: Expected number, "…11 23 16 16 16 8" - the issue is the points attr looks fine
# but the SVG may be missing stroke/fill context making it fail

# Actually the console error was just a browser warning, not fatal
# Let's focus on fixing the online state header overlap issue
# which is caused by the notification banner + driver header stacking

# Find where the driver header is defined and ensure it has proper z-index + padding-top
m = re.search(rb'GramHaul Cockpit', open('app/src/main/assets/index.html', 'rb').read())
if m:
    print('Found at:', m.start())

# Check the header padding-top in driver_dashboard
m2 = re.search(r'GramHaul Cockpit', text)
if m2:
    segment = text[m2.start()-200:m2.start()+400]
    print('Driver header context:')
    print(segment)
