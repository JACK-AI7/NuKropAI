import sys, re

sys.stdout.reconfigure(encoding='utf-8')

def apply_pixel_perfection(filepath):
    print(f"Applying pixel perfection to {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Pixel-perfect CSS for carousel, permissions, login, and dock
    perfect_css = """
/* ══════════════════════════════════════════════════════
   PIXEL-PERFECT ONBOARDING & PERMISSION DESIGN SYSTEM
══════════════════════════════════════════════════════ */
#ob-slides-viewport {
  position: relative !important;
  width: 100% !important;
  height: 100% !important;
  overflow: hidden !important;
  display: block !important;
}
.ob-carousel-slide {
  position: absolute !important;
  inset: 0 !important;
  width: 100% !important;
  height: 100% !important;
  opacity: 0 !important;
  visibility: hidden !important;
  pointer-events: none !important;
  transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1), transform 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
  transform: scale(1.02) !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: space-between !important;
  background-size: cover !important;
  background-position: center top !important;
  background-repeat: no-repeat !important;
  z-index: 1 !important;
}
.ob-carousel-slide.active {
  opacity: 1 !important;
  visibility: visible !important;
  pointer-events: auto !important;
  transform: scale(1) !important;
  z-index: 10 !important;
}
.ob-gradient-vignette {
  position: absolute !important;
  inset: 0 !important;
  background: linear-gradient(180deg, rgba(0,0,0,0.5) 0%, rgba(0,0,0,0.02) 30%, rgba(0,0,0,0.2) 65%, rgba(0,0,0,0.85) 100%) !important;
  pointer-events: none !important;
}
.ob-sheet-card {
  position: absolute !important;
  bottom: 0 !important;
  left: 0 !important;
  right: 0 !important;
  z-index: 25 !important;
  background: #FFFFFF !important;
  border-radius: 32px 32px 0 0 !important;
  padding: 24px 20px 24px !important;
  box-shadow: 0 -12px 40px rgba(0,0,0,0.22) !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 12px !important;
  min-height: 210px !important;
  justify-content: space-between !important;
}
.ob-indicator-pill {
  height: 6px !important;
  border-radius: 6px !important;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
}
.ob-indicator-pill.active {
  width: 24px !important;
  background: #16A34A !important;
}
.ob-indicator-pill.inactive {
  width: 6px !important;
  background: #CBD5E1 !important;
}
.ob-fab-btn {
  width: 52px !important;
  height: 52px !important;
  border-radius: 50% !important;
  background: linear-gradient(135deg, #16A34A, #15803D) !important;
  color: #FFFFFF !important;
  border: none !important;
  cursor: pointer !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  font-size: 20px !important;
  font-weight: 900 !important;
  box-shadow: 0 6px 20px rgba(22, 163, 74, 0.45) !important;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
}
.ob-fab-btn:active {
  transform: scale(0.92) !important;
}
.ob-fab-btn.expanded {
  width: auto !important;
  padding: 0 20px !important;
  border-radius: 26px !important;
  font-size: 13.5px !important;
  font-weight: 900 !important;
  gap: 6px !important;
}

/* Permission Suite */
.perm-suite-card {
  background: #FFFFFF !important;
  border: 1.5px solid #EEF2F7 !important;
  border-radius: 18px !important;
  padding: 12px 14px !important;
  display: flex !important;
  align-items: center !important;
  gap: 12px !important;
  box-shadow: 0 4px 14px -2px rgba(15, 23, 42, 0.04) !important;
  transition: all 0.2s ease !important;
}
.perm-suite-card.granted {
  border-color: #86EFAC !important;
  background: #F0FDF4 !important;
}
.perm-suite-img {
  width: 52px !important;
  height: 52px !important;
  min-width: 52px !important;
  min-height: 52px !important;
  max-width: 52px !important;
  max-height: 52px !important;
  border-radius: 14px !important;
  object-fit: cover !important;
  box-shadow: 0 3px 10px rgba(0,0,0,0.1) !important;
  flex-shrink: 0 !important;
  display: block !important;
}
"""

    if '/* ══════════════════════════════════════════════════════\n   PIXEL-PERFECT ONBOARDING' not in content:
        content = content.replace('</head>', f'<style>{perfect_css}</style>\n</head>')
    else:
        # replace existing
        content = re.sub(r'/\* ═+\n\s*PIXEL-PERFECT ONBOARDING[\s\S]*?\*/[\s\S]*?(?=</style>)', perfect_css, content)

    # 2. Update renderLoginScreen to hide dock
    content = content.replace(
        "function renderLoginScreen(container) {",
        """function renderLoginScreen(container) {
  const dock = document.querySelector('.bottom-dock-wrapper');
  if (dock) dock.style.display = 'none';"""
    )

    # 3. Update openScreen to show dock
    content = content.replace(
        "function openScreen(screenKey, tabElement) {",
        """function openScreen(screenKey, tabElement) {
  const dock = document.querySelector('.bottom-dock-wrapper');
  if (dock) dock.style.display = 'flex';"""
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Done perfecting {filepath}")

apply_pixel_perfection('app/src/main/assets/index.html')
apply_pixel_perfection('nukrop_emulator.html')
