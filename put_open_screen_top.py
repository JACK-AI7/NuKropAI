import sys

sys.stdout.reconfigure(encoding='utf-8')

open_screen_top = """
window.openScreen = function(screenKey, tabElement) {
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
};
var openScreen = window.openScreen;
"""

def put_open_screen_at_top(filepath):
    print(f"Injecting openScreen at very top of first script in {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the very first <script> tag
    idx = content.find('<script>')
    if idx != -1:
        content = content[:idx+8] + '\n' + open_screen_top + '\n' + content[idx+8:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Done putting openScreen at top in {filepath}")

put_open_screen_at_top('app/src/main/assets/index.html')
put_open_screen_at_top('nukrop_emulator.html')
