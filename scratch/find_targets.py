with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

targets = [
    'function getCropIconImg',
    'gramhaul: () => {',
    'gramhaul_tracking: () => {',
    'function updateGramhaulSelectorMapVehicles',
    'function renderTrackingSearchingState',
    'function renderTrackingDispatchedState',
    'function openGramhaulCropSelectorModal'
]

for t in targets:
    found = [(i+1, line.strip()) for i, line in enumerate(lines) if t in line]
    print(f'Target: "{t}" -> {len(found)} occurrences:')
    for line_num, l in found:
        print(f'   Line {line_num}: {ascii(l[:60])}')
