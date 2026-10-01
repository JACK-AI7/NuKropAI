import sys, re

sys.stdout.reconfigure(encoding='utf-8')

open_screen_code = """
function openScreen(screenKey, tabElement) {
  if (typeof fetchCommunityPostsFromSupabase === 'function' && screenKey === 'community') fetchCommunityPostsFromSupabase();
  if (typeof fetchKhataFromSupabase === 'function' && screenKey === 'khata') fetchKhataFromSupabase();
  if (typeof fetchMandiRatesFromSupabase === 'function' && screenKey === 'market') fetchMandiRatesFromSupabase();
  if (typeof fetchEquipmentFromSupabase === 'function' && screenKey === 'equipment') fetchEquipmentFromSupabase();
  
  if (typeof currentScreenKey !== 'undefined') currentScreenKey = screenKey || 'home';
  if (typeof currentTabElement !== 'undefined') currentTabElement = tabElement || null;

  document.querySelectorAll('.dock-tab-btn').forEach(b => b.classList.remove('active'));
  if (tabElement) {
    tabElement.classList.add('active');
  } else {
    const tabMap = {home:'tab-home', community:'tab-community', market:'tab-market', profile:'tab-profile'};
    if (tabMap[screenKey]) {
      const el = document.getElementById(tabMap[screenKey]);
      if (el) el.classList.add('active');
    }
  }

  const container = document.getElementById('screen-body');
  if (container) {
    container.classList.remove('screen-fade');
    void container.offsetWidth;
    container.classList.add('screen-fade');
    const viewFn = (typeof APP_VIEWS !== 'undefined' && APP_VIEWS[screenKey]) ? APP_VIEWS[screenKey] : (typeof APP_VIEWS !== 'undefined' ? APP_VIEWS.home : null);
    if (viewFn) {
      container.innerHTML = viewFn();
    }
    if (typeof applyCustomCropDropdowns === 'function') setTimeout(applyCustomCropDropdowns, 0);
  }

  const screenContainer = document.getElementById('screen-container');
  if (screenContainer) screenContainer.scrollTop = 0;

  if (screenKey === 'home' && typeof updateWeatherCardDom === 'function') updateWeatherCardDom();
  if (typeof updateStatusBarTheme === 'function') updateStatusBarTheme(screenKey);
  if (screenKey === 'calc_fert' && typeof calcFertilizerDose === 'function') calcFertilizerDose();
  if (screenKey === 'calc_pest' && typeof calcPesticideDose === 'function') calcPesticideDose();
  if (screenKey === 'scanner' && typeof startLiveCameraStream === 'function') { setTimeout(startLiveCameraStream, 150); } else if (typeof stopLiveCameraStream === 'function') { stopLiveCameraStream(); }
  if (screenKey === 'calc_budget' && typeof calcBudgetRoi === 'function') calcBudgetRoi();
  if (typeof updateBottomDockForRole === 'function') updateBottomDockForRole();

  const dock = document.querySelector('.bottom-dock-wrap');
  if (dock) dock.style.display = 'flex';
}
window.openScreen = openScreen;
"""

def restore_open_screen(filepath):
    print(f"Restoring openScreen in {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if "function openScreen(" not in content:
        content = content.replace("</script>\n</body>", f"\n{open_screen_code}\n</script>\n</body>")
    else:
        # Check if window.openScreen is assigned
        if "window.openScreen =" not in content:
            content = content.replace("function openScreen(", f"{open_screen_code}\nfunction _old_openScreen(")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully ensured openScreen in {filepath}")

restore_open_screen('app/src/main/assets/index.html')
restore_open_screen('nukrop_emulator.html')
