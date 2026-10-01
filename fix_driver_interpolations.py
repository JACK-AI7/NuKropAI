import sys, re
sys.stdout.reconfigure(encoding='utf-8')

for filepath in ['app/src/main/assets/index.html', 'nukrop_emulator.html']:
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Fix escaped template literal interpolations within driver_dashboard view
    # Pattern: \\${varName} -> ${varName}  (only in JS template literals)
    # We need to fix double-backslash before $ inside the driver_dashboard view
    
    # Find the driver_dashboard view block
    start_m = re.search(r'driver_dashboard\s*:\s*\(\)\s*=>', text)
    if not start_m:
        print(f'Could not find driver_dashboard in {filepath}')
        continue
    
    view_start = start_m.start()
    # Find where this view ends (next view definition or end of APP_VIEWS)
    view_end_m = re.search(r'\n  profile\s*:\s*\(\)\s*=>', text[view_start:])
    if view_end_m:
        view_end = view_start + view_end_m.start()
    else:
        view_end = view_start + 50000
    
    view_block = text[view_start:view_end]
    
    # Fix escaped dollar signs in template literals
    # \\${ -> ${
    original_count = view_block.count('\\\\${')
    view_block_fixed = view_block.replace('\\\\${', '${')
    fixed_count = view_block_fixed.count('\\\\${')
    
    print(f'{filepath}: Fixed {original_count - fixed_count} escaped interpolations in driver_dashboard')
    
    # Reconstruct full file
    text = text[:view_start] + view_block_fixed + text[view_end:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f'  Saved {filepath}')

print('\nDone!')
