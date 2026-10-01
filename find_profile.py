import sys, re
sys.stdout.reconfigure(encoding='utf-8')
content = open('app/src/main/assets/index.html', encoding='utf-8').read()
lines = content.splitlines()

# Find openScreen function / case
openscreen_fn = [(i+1, lines[i][:160]) for i in range(len(lines)) if 'function openScreen' in lines[i]]
print('=== openScreen function ===')
for ln, txt in openscreen_fn[:5]:
    print(f'  L{ln}: {txt.strip()}')

# Find profile rendering  
profile_render = [(i+1, lines[i][:160]) for i in range(len(lines)) if ("case 'profile'" in lines[i] or "'profile':" in lines[i]) and i > 5000]
print('\n=== profile case in openScreen ===')
for ln, txt in profile_render[:10]:
    print(f'  L{ln}: {txt.strip()}')

# Find farmerProfile.name rendered in HTML
fp_html = [(i+1, lines[i][:160]) for i in range(len(lines)) if 'farmerProfile.' in lines[i] and i > 5220]
print('\n=== farmerProfile used in rendering ===')
for ln, txt in fp_html[:20]:
    print(f'  L{ln}: {txt.strip()}')
    
# Pesticide calculator
pest_fn = [(i+1, lines[i][:160]) for i in range(len(lines)) if 'function calcPesticideDose' in lines[i] or 'calcPesticideDose' in lines[i]]
print('\n=== calcPesticideDose ===')
for ln, txt in pest_fn[:10]:
    print(f'  L{ln}: {txt.strip()}')

# Bio medicines data
bio_data = [(i+1, lines[i][:160]) for i in range(len(lines)) if 'BIO_MEDICINE' in lines[i] or 'BIORX_RECIPES' in lines[i] or 'biorxRecipes' in lines[i] or "recipe" in lines[i].lower() and i > 2340]
print('\n=== Bio medicine data ===')
for ln, txt in bio_data[:10]:
    print(f'  L{ln}: {txt.strip()}')

# Community followers
follow_fn = [(i+1, lines[i][:160]) for i in range(len(lines)) if 'follow' in lines[i].lower() and ('button' in lines[i].lower() or 'function' in lines[i].lower() or 'count' in lines[i].lower())]
print('\n=== community follow ===')
for ln, txt in follow_fn[:10]:
    print(f'  L{ln}: {txt.strip()}')
