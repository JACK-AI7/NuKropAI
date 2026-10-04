import re

def update_file(filepath):
    print(f"Reading {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update getCropIconImg
    old_crop_img_fn = '''function getCropIconImg(path, slug) {
  let cleanSlug = (slug || 'cotton').toLowerCase().trim();
  
  if (typeof MASTER_120_CROPS !== 'undefined') {
    const found = MASTER_120_CROPS.find(x => x.key === cleanSlug || x.slug === cleanSlug);
    if (found && found.slug) cleanSlug = found.slug;
  }

  const ICON_MAP = {
    'cotton': 'cotton.svg',
    'chilli': 'chilli.svg',
    'chili': 'chilli.svg',
    'birds-eye-chili': 'birds-eye-chili.svg',
    'red-tomato': 'tomato.svg',
    'tomato': 'tomato.svg',
    'wheat': 'wheat.svg',
    'paddy': 'rice.svg',
    'rice': 'rice.svg',
    'paddy-rice': 'rice.svg',
    'paddy / rice': 'rice.svg',
    'maize': 'corn.svg',
    'corn': 'corn.svg',
    'millet': 'sorghum-millet.svg',
    'sorghum': 'sorghum-millet.svg',
    'turmeric': 'turmeric.svg',
    'onion': 'red-onion.svg',
    'red-onion': 'red-onion.svg',
    'white-onion': 'white-onion.svg',
    'potato': 'russet-potato.svg',
    'russet-potato': 'russet-potato.svg',
    'groundnut': 'runner-bean.svg',
    'peanut': 'runner-bean.svg',
    'sugarcane': 'sugarcane.svg',
    'sugar-cane': 'sugarcane.svg',
    'soybean': 'soybean.svg',
    'soy-bean': 'soybean.svg',
    'bhindi': 'bhindi.svg',
    'okra': 'bhindi.svg',
    'brinjal': 'eggplant.svg',
    'eggplant': 'eggplant.svg',
    'cabbage': 'green-cabbage.svg',
    'green-cabbage': 'green-cabbage.svg',
    'cauliflower': 'yellow-cauliflower.svg',
    'spinach': 'spinach.svg',
    'garlic': 'garlic.svg',
    'ginger': 'ginger.svg',
    'carrot': 'white-carrot.svg',
    'cucumber': 'cucumber.svg',
    'watermelon': 'watermelon.svg',
    'sunflower': 'sunflower.svg',
    'apple': 'generic-apple.svg',
    'generic-apple': 'generic-apple.svg',
    'banana': 'banana-pepper.svg',
    'mango': 'apricot.svg'
  };

  const svgName = ICON_MAP[cleanSlug] || (cleanSlug.endsWith('.svg') ? cleanSlug : `${cleanSlug}.svg`);
  return `<img src="crop-icons/${svgName}" alt="${cleanSlug}" style="width:100%;height:100%;object-fit:contain;display:block;" onerror="this.onerror=null;this.src='crop-icons/cotton.svg';" />`;
}'''

    new_crop_img_fn = '''function getCropIconImg(path, slug) {
  let cleanSlug = (slug || 'cotton').toLowerCase().trim();
  
  if (typeof MASTER_120_CROPS !== 'undefined') {
    const found = MASTER_120_CROPS.find(x => x.key === cleanSlug || x.slug === cleanSlug);
    if (found && found.slug) cleanSlug = found.slug;
  }

  const ICON_MAP = {
    'cotton': 'cotton.svg',
    'chilli': 'chilli.svg',
    'chili': 'chilli.svg',
    'birds-eye-chili': 'birds-eye-chili.svg',
    'red-tomato': 'tomato.svg',
    'tomato': 'tomato.svg',
    'wheat': 'wheat.svg',
    'paddy': 'rice.svg',
    'rice': 'rice.svg',
    'paddy-rice': 'rice.svg',
    'paddy / rice': 'rice.svg',
    'maize': 'corn.svg',
    'corn': 'corn.svg',
    'millet': 'sorghum-millet.svg',
    'sorghum': 'sorghum-millet.svg',
    'turmeric': 'turmeric.svg',
    'onion': 'red-onion.svg',
    'red-onion': 'red-onion.svg',
    'white-onion': 'white-onion.svg',
    'potato': 'russet-potato.svg',
    'russet-potato': 'russet-potato.svg',
    'groundnut': 'groundnut.svg',
    'peanut': 'groundnut.svg',
    'sugarcane': 'sugarcane.svg',
    'sugar-cane': 'sugarcane.svg',
    'soybean': 'soybean.svg',
    'soy-bean': 'soybean.svg',
    'bhindi': 'bhindi.svg',
    'okra': 'bhindi.svg',
    'brinjal': 'eggplant.svg',
    'eggplant': 'eggplant.svg',
    'cabbage': 'green-cabbage.svg',
    'green-cabbage': 'green-cabbage.svg',
    'cauliflower': 'yellow-cauliflower.svg',
    'spinach': 'spinach.svg',
    'garlic': 'garlic.svg',
    'ginger': 'ginger.svg',
    'carrot': 'carrot.svg',
    'cucumber': 'cucumber.svg',
    'watermelon': 'watermelon.svg',
    'sunflower': 'sunflower.svg',
    'apple': 'generic-apple.svg',
    'generic-apple': 'generic-apple.svg',
    'banana': 'banana.svg',
    'mango': 'mango.svg',
    'mustard': 'mustard.svg',
    'chickpea': 'chickpea.svg',
    'redgram': 'redgram.svg',
    'greengram': 'greengram.svg',
    'blackgram': 'blackgram.svg',
    'papaya': 'papaya.svg',
    'guava': 'guava.svg',
    'pomegranate': 'pomegranate.svg',
    'lemon': 'lemon.svg',
    'sweetlime': 'sweetlime.svg',
    'coconut': 'coconut.svg',
    'capsicum': 'capsicum.svg',
    'sesame': 'sesame.svg',
    'castor': 'castor.svg',
    'jowar': 'jowar.svg',
    'bajra': 'bajra.svg',
    'ragi': 'ragi.svg',
    'cumin': 'cumin.svg',
    'coriander': 'coriander.svg',
    'cardamom': 'cardamom.svg',
    'blackpepper': 'blackpepper.svg',
    'coffee': 'coffee.svg',
    'tea': 'tea.svg',
    'cashew': 'cashew.svg',
    'tobacco': 'tobacco.svg',
    'rubber': 'rubber.svg'
  };

  const svgName = ICON_MAP[cleanSlug] || (cleanSlug.endsWith('.svg') ? cleanSlug : `${cleanSlug}.svg`);
  return `<img src="crop-icons/${svgName}" alt="${cleanSlug}" style="width:100%;height:100%;object-fit:contain;display:block;" onerror="this.onerror=null;this.src='crop-icons/cotton.svg';" />`;
}'''

    if old_crop_img_fn in content:
        content = content.replace(old_crop_img_fn, new_crop_img_fn)
        print("Updated getCropIconImg successfully!")
    else:
        print("Warning: old getCropIconImg not matched directly, checking normalized...")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

update_file('app/src/main/assets/index.html')
update_file('nukrop_emulator.html')
