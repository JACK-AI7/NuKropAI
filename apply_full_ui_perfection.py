# -*- coding: utf-8 -*-
import re

def update_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f'Updating {filename} (original len: {len(content)})...')

    # 1. Add .plantix-crop-badge, .crop-add-btn, .suite-bento-tile, and .icon-plate styles to CSS
    css_to_add = """
/* === 100% CIRCULAR CROP SELECTOR BADGES === */
.plantix-crop-badge {
  width: 58px !important;
  height: 58px !important;
  border-radius: 50% !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  background: #FFFFFF !important;
  overflow: hidden !important;
  box-sizing: border-box !important;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
}
.plantix-crop-badge:active {
  transform: scale(0.92) !important;
}
.plantix-crop-badge.active {
  border: 2.5px solid #16A34A !important;
  box-shadow: 0 4px 14px rgba(22,163,74,0.35), 0 0 0 3px rgba(22,163,74,0.2) !important;
  background: #F0FDF4 !important;
}
.plantix-crop-badge img {
  width: 100% !important;
  height: 100% !important;
  max-width: 36px !important;
  max-height: 36px !important;
  object-fit: contain !important;
  display: block !important;
}
.crop-add-btn {
  width: 58px !important;
  height: 58px !important;
  border-radius: 50% !important;
  border: 2px dashed #93C5FD !important;
  background: #EFF6FF !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  margin: 0 auto 6px !important;
  box-sizing: border-box !important;
  box-shadow: 0 2px 6px rgba(37,99,235,0.06) !important;
}
.crop-add-btn:active {
  transform: scale(0.92) !important;
  background: #DBEAFE !important;
}

/* === LUXURY 2-COLUMN BENTO TILES & SQUIRCLE ICON PLATES === */
.suite-bento-tile {
  background: #FFFFFF !important;
  border: 1.5px solid #EEF2F7 !important;
  border-radius: 20px !important;
  padding: 14px 12px !important;
  box-shadow: 0 1px 3px rgba(15,23,42,0.03), 0 4px 16px -4px rgba(15,23,42,0.06) !important;
  cursor: pointer !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 10px !important;
  transition: transform 140ms cubic-bezier(0.16, 1, 0.3, 1), box-shadow 140ms ease !important;
  position: relative !important;
  overflow: hidden !important;
  box-sizing: border-box !important;
}
.suite-bento-tile:active {
  transform: scale(0.97) !important;
  box-shadow: 0 1px 2px rgba(15,23,42,0.03), 0 2px 8px -2px rgba(15,23,42,0.04) !important;
}
.suite-bento-tile .icon-plate {
  width: 44px !important;
  height: 44px !important;
  min-width: 44px !important;
  min-height: 44px !important;
  max-width: 44px !important;
  max-height: 44px !important;
  border-radius: 14px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05) !important;
  flex-shrink: 0 !important;
  box-sizing: border-box !important;
}
"""

    last_style_end = content.rfind('</style>')
    if last_style_end != -1:
        content = content[:last_style_end] + css_to_add + content[last_style_end:]
        print('Added Bento Tile & Icon Plate CSS')

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Successfully updated {filename} (new len: {len(content)})')

update_file('app/src/main/assets/index.html')
update_file('nukrop_emulator.html')
