const fs = require('fs');

const files = ['app/src/main/assets/index.html', 'nukrop_emulator.html'];

files.forEach(f => {
  if (!fs.existsSync(f)) return;
  let code = fs.readFileSync(f, 'utf8');

  const p = code.indexOf('const GROQ_CONFIG = {');
  const pEnd = code.indexOf('/* ═════════════════ REAL SUPABASE CLOUD AUTH & DATA INTEGRATION ═════════════════ */', p);

  if (p !== -1 && pEnd !== -1) {
    const secureAiCode = `const SECURE_AI_ENDPOINT = \`\${SUPABASE_CONFIG.url}/functions/v1/ai-agronomist\`;

async function callTokenRouterAi(userQuery, activeLangCode) {
  return await callSecureAiEngine(userQuery, activeLangCode);
}

function callGroqAiEngine(userQuery, activeLangCode) {
  return callSecureAiEngine(userQuery, activeLangCode);
}

async function callSecureAiEngine(userQuery, activeLangCode) {
  const langCode = activeLangCode || currentLang || 'te';

  // 1. Primary: Server-Side Supabase Edge Function (Zero Client Secret Exposure)
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 8000);

    const res = await fetch(SECURE_AI_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'apikey': SUPABASE_CONFIG.anonKey,
        'Authorization': \`Bearer \${SUPABASE_CONFIG.anonKey}\`
      },
      body: JSON.stringify({
        query: userQuery,
        languageCode: langCode,
        cropContext: (typeof myActiveCrops !== 'undefined' && myActiveCrops[activeCropIdx]) ? myActiveCrops[activeCropIdx].id : 'cotton'
      }),
      signal: controller.signal
    });
    clearTimeout(timeoutId);

    if (res.ok) {
      const data = await res.json();
      if (data && data.response) {
        return data.response;
      }
    }
  } catch (err) {
    console.warn('Supabase AI Edge Function offline fallback:', err.message);
  }

  // 2. Offline Rural Fallback: Built-in ICAR Botanical Knowledge Engine
  return getOfflineAgronomyAdvice(userQuery, langCode);
}

function getOfflineAgronomyAdvice(query, lang) {
  const q = (query || '').toLowerCase();
  const isTe = lang === 'te';
  const isHi = lang === 'hi';

  if (q.includes('పత్తి') || q.includes('cotton') || q.includes('కాయ') || q.includes('పురుగు') || q.includes('bollworm')) {
    if (isTe) {
      return "🌿 **పత్తి పంట సంరక్షణ సలహా (ICAR):**\\n\\n• **గులాబీ రంగు కాయ తొలిచే పురుగు నివారణ:** ఎకరానికి 5 లింగాకర్షక బుట్టలు అమర్చండి.\\n• **సేంద్రీయ చికిత్స:** వేప నూనె 10,000 ppm (30 మి.లీ / 15 లీటర్ల నీరు) లేదా బ్రహ్మాస్త్రం పిచికారీ చేయండి.\\n• **రసాయన చికిత్స:** ప్రొఫెనోఫాస్ 50% EC @ 350 మి.లీ/ఎకరం లేదా ఎమామెక్టిన్ బెంజోయేట్ 5% SG @ 88 గ్రా/ఎకరం స్ప్రే చేయండి.";
    } else if (isHi) {
      return "🌿 **कपास फसल सुरक्षा सलाह (ICAR):**\\n\\n• **गुलाबी सुंडी नियंत्रण:** 5 फेरोमोन ट्रैप प्रति एकड़ लगाएं।\\n• **जैविक उपाय:** 10,000 ppm नीम तेल (30ml/15L) या ब्रह्मास्त्र का छिड़काव करें।\\n• **रासायनिक उपाय:** प्रोफेनोफॉस 50% EC @ 350ml/एकड़ या इमामेक्टिन बेंजोएट 5% SG @ 88g/एकड़ छिड़कें।";
    } else {
      return "🌿 **Cotton Crop Protection (ICAR Advisory):**\\n\\n• **Pink Bollworm Control:** Install 5 pheromone traps per acre.\\n• **Organic Treatment:** Spray Neem Oil 10,000 ppm (30ml / 15L water) or Brahmastra.\\n• **Chemical Treatment:** Profenofos 50% EC @ 350ml/acre or Emamectin Benzoate 5% SG @ 88g/acre.";
    }
  }

  if (q.includes('మిరప') || q.includes('chilli') || q.includes('ముడత') || q.includes('thrips')) {
    if (isTe) {
      return "🌶️ **మిరప తామర పురుగులు & ఆకుముడత నివారణ (ICAR):**\\n\\n• **రక్షణ చర్యలు:** ఎకరానికి 20 నీలం + 20 పసుపు జిగురు అట్టలు పెట్టండి.\\n• **సేంద్రీయ చికిత్స:** దశపర్ణి కషాయం 500 మి.లీ లేదా అగ్నియాస్త్రం 300 మి.లీ / పంపు స్ప్రే చేయండి.\\n• **సిఫార్సు మందులు:** ఫిప్రోనిల్ 5% SC @ 400 మి.లీ/ఎకరం లేదా ఎసిటామిప్రిడ్ 20% SP @ 50 గ్రా/ఎకరం.";
    } else {
      return "🌶️ **Chilli Thrips & Leaf Curl Advisory:**\\n\\n• Install 20 blue + 20 yellow sticky traps per acre.\\n• Organic: Spray Dashaparni Kashayam (500ml/tank).\\n• Recommended: Fipronil 5% SC @ 400ml/acre or Acetamiprid 20% SP @ 50g/acre.";
    }
  }

  // Default practical agronomy advice
  if (isTe) {
    return "🌾 **NuKropAI రైతు సలహా:**\\n\\n• మీ పొలంలో తెగులు లేదా పోషక లోపాన్ని గుర్తించడానికి కెమెరా ద్వారా ఆకు ఫోటో తీసి స్కాన్ చేయండి.\\n• ప్రస్తుత వాతావరణం ఆధారంగా సాయంత్రం వేళల్లో గాలి వేగం తక్కువగా ఉన్నప్పుడు మాత్రమే మందుల పిచికారీ చేపట్టండి.\\n• మరిన్ని వివరాల కోసం 24/7 ఉచిత కిసాన్ హెల్ప్‌లైన్: 1800-180-1551 ను సంప్రదించండి.";
  } else if (isHi) {
    return "🌾 **NuKropAI किसान सलाह:**\\n\\n• फसल रोग की सटीक पहचान के लिए कैमरे से पत्ती की फोटो स्कैन करें।\\n• मौसम के अनुसार शाम के समय कम हवा में ही दवा का छिड़काव करें।\\n• अधिक जानकारी के लिए किसान हेल्पलाइन: 1800-180-1551 पर कॉल करें।";
  } else {
    return "🌾 **NuKropAI Agronomy Advisory:**\\n\\n• Scan clear leaf photographs using the AI Scanner for automated diagnosis.\\n• Perform spraying only during evening hours when wind speed is under 10 km/h.\\n• For real-time expert assistance, contact the Kisan Call Centre at 1800-180-1551.";
  }
}
`;

    code = code.substring(0, p) + secureAiCode + '\n\n' + code.substring(pEnd);
    fs.writeFileSync(f, code, 'utf8');
    console.log(`[PASS] Secured AI layer in: ${f}`);
  }
});
