import sys, re
sys.stdout.reconfigure(encoding='utf-8')

for filepath in ['app/src/main/assets/index.html', 'nukrop_emulator.html']:
    with open(filepath, 'rb') as f:
        raw = f.read()
    
    # Find driver_dashboard section
    dd_marker = b'driver_dashboard: () =>'
    dd_pos = raw.find(dd_marker)
    if dd_pos == -1:
        print(f'Not found in {filepath}')
        continue
    
    profile_marker = b'\n  profile: () =>'
    profile_pos = raw.find(profile_marker, dd_pos)
    if profile_pos == -1:
        profile_pos = dd_pos + 50000
    
    # Extract driver_dashboard block
    block = raw[dd_pos:profile_pos]
    
    # The issue: backslash (0x5C) before $ (0x24) -> fix to just $ 
    # In the template literal part, we have \${ which should be ${
    # Pattern: b'\\${' (3 bytes: 0x5C, 0x24, 0x7B)
    count_before = block.count(b'\\${')
    block_fixed = block.replace(b'\\${', b'${')
    count_after = block_fixed.count(b'\\${')
    
    print(f'{filepath}: Fixed {count_before - count_after} escaped interpolations')
    
    # Reconstruct
    raw_fixed = raw[:dd_pos] + block_fixed + raw[profile_pos:]
    
    with open(filepath, 'wb') as f:
        f.write(raw_fixed)
    print(f'  Saved {filepath}')

print('Done!')
