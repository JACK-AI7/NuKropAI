import os, sys, re

sys.stdout.reconfigure(encoding='utf-8')

def update_file(file_path):
    print(f"Updating {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update/Add CSS for the new full-bleed onboarding, permissions, potea auth, and gramhaul dark theme
    onboarding_css = """
/* ══════════════════════════════════════════════════════
   NUKROPAI FULL-BLEED ONBOARDING & PERMISSIONS SUITE
══════════════════════════════════════════════════════ */
.ob-carousel-slide {
  position: absolute;
  inset: 0;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.35s cubic-bezier(0.4, 0, 0.2, 1), transform 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  transform: scale(1.02);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background-size: cover;
  background-position: center top;
  background-repeat: no-repeat;
}
.ob-carousel-slide.active {
  opacity: 1;
  visibility: visible;
  transform: scale(1);
}
.ob-gradient-vignette {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0.05) 30%, rgba(0,0,0,0.2) 60%, rgba(0,0,0,0.85) 100%);
  pointer-events: none;
}
.ob-sheet-card {
  position: relative;
  z-index: 10;
  background: #FFFFFF;
  border-radius: 32px 32px 0 0;
  padding: 26px 22px 28px;
  box-shadow: 0 -12px 40px rgba(0,0,0,0.18);
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-top: auto;
  animation: obSheetSlideUp 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes obSheetSlideUp {
  from { transform: translateY(30px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
.ob-indicator-pill {
  height: 7px;
  border-radius: 6px;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}
.ob-indicator-pill.active {
  width: 26px;
  background: #16A34A;
}
.ob-indicator-pill.inactive {
  width: 7px;
  background: #E2E8F0;
}
.ob-fab-btn {
  width: 54px;
  height: 54px;
  border-radius: 50%;
  background: linear-gradient(135deg, #16A34A, #15803D);
  color: #FFFFFF;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  box-shadow: 0 6px 20px rgba(22, 163, 74, 0.42);
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  -webkit-tap-highlight-color: transparent;
}
.ob-fab-btn:active {
  transform: scale(0.92);
}
.ob-fab-btn.expanded {
  width: auto;
  padding: 0 22px;
  border-radius: 27px;
  font-size: 14px;
  font-weight: 800;
  gap: 8px;
}

/* Visual Permission Card */
.perm-suite-card {
  background: #FFFFFF;
  border: 1.5px solid #EEF2F7;
  border-radius: 20px;
  padding: 14px;
  display: flex;
  align-items: center;
  gap: 14px;
  box-shadow: 0 4px 16px -2px rgba(15, 23, 42, 0.05);
  transition: all 0.2s ease;
}
.perm-suite-card.granted {
  border-color: #86EFAC;
  background: #F0FDF4;
}
.perm-suite-img {
  width: 58px;
  height: 58px;
  border-radius: 16px;
  object-fit: cover;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  flex-shrink: 0;
}

/* GramHaul Dark/Neon Map Theme */
.gramhaul-dark-canvas {
  background: #0A0E17;
  color: #FFFFFF;
  border-radius: 24px;
  overflow: hidden;
  position: relative;
}
.neon-gps-route {
  stroke: #22C55E;
  stroke-width: 4;
  stroke-linecap: round;
  filter: drop-shadow(0 0 8px #22C55E);
}
"""

    if '/* ══════════════════════════════════════════════════════\n   NUKROPAI FULL-BLEED ONBOARDING' not in content:
        content = content.replace('</head>', f'<style>{onboarding_css}</style>\n</head>')

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Added CSS to {file_path}")

update_file('app/src/main/assets/index.html')
update_file('nukrop_emulator.html')
