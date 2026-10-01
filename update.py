import re

with open('nukrop_emulator.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Empty AGMARKNET_MANDI_CATALOG
content = re.sub(
    r'const AGMARKNET_MANDI_CATALOG = \[\s*// 1\. Tomato.*?\];',
    'let AGMARKNET_MANDI_CATALOG = [];',
    content,
    flags=re.DOTALL
)

# 2. Empty COMMUNITY_POSTS_CATALOG
content = re.sub(
    r'let COMMUNITY_POSTS_CATALOG = \[\s*\{\s*id: \'post-0\'.*?\];',
    'let COMMUNITY_POSTS_CATALOG = [];',
    content,
    flags=re.DOTALL
)

# 3. Remove fake @gmail.com logic
content = re.sub(
    r'// Ensure valid domain format for Supabase\s*if \(\!email\.includes\(\'@\'\)\) \{\s*email = email \+ \'@gmail\.com\';\s*\}',
    '',
    content
)

# 4. Hide OR divider
content = re.sub(
    r'<!-- Divider with OR text in Our Clean Style -->\s*<div style="display:flex;align-items:center;gap:12px;margin:2px 0;">',
    '<!-- Divider with OR text in Our Clean Style -->\\n        <div style="display:none;align-items:center;gap:12px;margin:2px 0;">',
    content
)

# 5. Fix advanceSlide
content = content.replace(
    "advanceSlide('slide_disease');",
    "advanceSlide('slide_disease');" # just making sure it's there
)

# 6. getMandiDefaults fallback empty object
content = content.replace(
    "found = AGMARKNET_MANDI_CATALOG.find(x => x.cropKey === 'cotton') || AGMARKNET_MANDI_CATALOG[0];",
    "found = AGMARKNET_MANDI_CATALOG.find(x => x.cropKey === 'cotton') || AGMARKNET_MANDI_CATALOG[0] || { id: 'loading', mandi: { en: 'Loading...', te: 'లోడ్ అవుతోంది...', hi: 'लोड हो रहा है...' }, modalPrice: 0, unit: '', change: '', up: true };"
)

# 7. auth logic
content = re.sub(
    r'setTimeout\(\(\) => \{\s*advanceSlide\(\'slide_disease\'\);\s*\}, 600\);',
    "advanceSlide('slide_disease');",
    content
)

with open('nukrop_emulator.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated HTML')
