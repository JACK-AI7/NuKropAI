import os, re, sys

sys.stdout.reconfigure(encoding='utf-8')

# Read current patch script and add the helper functions into MASTER_OVERLAY_JS
with open('patch_potea_and_gramhaul_uber_white.py', 'r', encoding='utf-8') as f:
    code = f.read()

helpers = """
function selectGramhaulRideTier(tier) {
  const t1 = document.getElementById('gh-tier-1');
  const t2 = document.getElementById('gh-tier-2');
  const t3 = document.getElementById('gh-tier-3');
  const btn = document.querySelector('[onclick*="confirmGramhaulBooking"]');
  if (t1) {
    t1.style.background = tier === 1 ? '#F0FDF4' : '#FFFFFF';
    t1.style.borderColor = tier === 1 ? '#16A34A' : '#E2E8F0';
    t1.style.boxShadow = tier === 1 ? '0 4px 14px rgba(22,163,74,0.12)' : '0 2px 8px rgba(15,23,42,0.04)';
  }
  if (t2) {
    t2.style.background = tier === 2 ? '#F0FDF4' : '#FFFFFF';
    t2.style.borderColor = tier === 2 ? '#16A34A' : '#E2E8F0';
    t2.style.boxShadow = tier === 2 ? '0 4px 14px rgba(22,163,74,0.12)' : '0 2px 8px rgba(15,23,42,0.04)';
  }
  if (t3) {
    t3.style.background = tier === 3 ? '#F0FDF4' : '#FFFFFF';
    t3.style.borderColor = tier === 3 ? '#16A34A' : '#E2E8F0';
    t3.style.boxShadow = tier === 3 ? '0 4px 14px rgba(22,163,74,0.12)' : '0 2px 8px rgba(15,23,42,0.04)';
  }
  if (btn) {
    if (tier === 1) btn.innerHTML = '<span>Confirm Tata Ace · ₹450</span> <span>→</span>';
    if (tier === 2) btn.innerHTML = '<span>Confirm Mahindra Bolero · ₹650</span> <span>→</span>';
    if (tier === 3) btn.innerHTML = '<span>Confirm Eicher Pro 5T · ₹1,100</span> <span>→</span>';
  }
}

function confirmGramhaulBooking() {
  const sheet = document.getElementById('gh-active-trip-sheet');
  if (sheet) {
    sheet.scrollIntoView({ behavior: 'smooth' });
    sheet.style.boxShadow = '0 0 0 3px rgba(22, 163, 74, 0.4)';
    setTimeout(() => { sheet.style.boxShadow = '0 8px 30px rgba(15,23,42,0.08)'; }, 1500);
  }
}
"""

if 'function selectGramhaulRideTier' not in code:
    code = code.replace('</script>', helpers + '\n</script>')
    with open('patch_potea_and_gramhaul_uber_white.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Updated patch script with interactive GramHaul ride selection helpers!")

