import os

crop_dir = r'c:\Users\bjasw\Downloads\agriculture-ai-os\app\src\main\assets\crop-icons'
os.makedirs(crop_dir, exist_ok=True)

ICONS = {
    # 1. Vibrant Cotton
    'cotton.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="cgLeaf" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#4ADE80"/>
      <stop offset="100%" stop-color="#15803D"/>
    </linearGradient>
    <linearGradient id="cgCalyx" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#EAB308"/>
      <stop offset="100%" stop-color="#854D0E"/>
    </linearGradient>
    <linearGradient id="cgStem" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#16A34A"/>
      <stop offset="100%" stop-color="#14532D"/>
    </linearGradient>
    <linearGradient id="cgBoll" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="65%" stop-color="#F8FAFC"/>
      <stop offset="100%" stop-color="#E2E8F0"/>
    </linearGradient>
    <filter id="cgShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="4" stdDeviation="3" flood-opacity="0.18"/>
    </filter>
  </defs>
  <path d="M64 92 C64 106 58 116 48 122" stroke="url(#cgStem)" stroke-width="6" stroke-linecap="round" fill="none"/>
  <path d="M40 96 C22 92 16 76 26 64 C36 76 48 84 56 88 Z" fill="url(#cgLeaf)"/>
  <path d="M88 96 C106 92 112 76 102 64 C92 76 80 84 72 88 Z" fill="url(#cgLeaf)"/>
  <g filter="url(#cgShadow)">
    <circle cx="64" cy="40" r="26" fill="url(#cgBoll)"/>
    <circle cx="40" cy="58" r="24" fill="url(#cgBoll)"/>
    <circle cx="88" cy="58" r="24" fill="url(#cgBoll)"/>
    <circle cx="64" cy="66" r="25" fill="url(#cgBoll)"/>
  </g>
  <path d="M64 88 L52 74 C50 68 56 66 60 72 L64 78 L68 72 C72 66 78 68 76 74 Z" fill="url(#cgCalyx)"/>
  <path d="M64 88 L38 82 C32 80 34 74 40 76 L54 82 Z" fill="url(#cgCalyx)"/>
  <path d="M64 88 L90 82 C96 80 94 74 88 76 L74 82 Z" fill="url(#cgCalyx)"/>
</svg>''',

    # 2. Banana (Golden yellow ripe bananas with green stem)
    'banana.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="bgYellow" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FEF08A"/>
      <stop offset="40%" stop-color="#FACC15"/>
      <stop offset="100%" stop-color="#CA8A04"/>
    </linearGradient>
    <linearGradient id="bgGreen" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#4ADE80"/>
      <stop offset="100%" stop-color="#15803D"/>
    </linearGradient>
  </defs>
  <!-- Main Banana -->
  <path d="M32 26 C48 30 76 46 92 78 C102 98 94 114 86 116 C78 118 70 102 60 88 C46 68 30 52 24 38 C20 30 24 24 32 26 Z" fill="url(#bgYellow)"/>
  <path d="M22 28 C28 32 38 46 50 64 C64 84 76 102 82 108" stroke="#EAB308" stroke-width="2" fill="none" opacity="0.6"/>
  <!-- Second banana overlap -->
  <path d="M42 34 C58 40 82 58 96 86 C102 98 98 110 92 112 C98 102 94 88 84 72 C70 52 54 40 44 34 Z" fill="#EAB308"/>
  <!-- Crown stem -->
  <path d="M22 24 C24 16 32 14 36 20 L30 30 Z" fill="url(#bgGreen)"/>
  <!-- Tip -->
  <circle cx="86" cy="115" r="3" fill="#713F12"/>
</svg>''',

    # 3. Mango (Juicy Alphonso Saffron & Golden with fresh leaf)
    'mango.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="mgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F87171"/>
      <stop offset="35%" stop-color="#FB923C"/>
      <stop offset="75%" stop-color="#FBBF24"/>
      <stop offset="100%" stop-color="#FDE047"/>
    </linearGradient>
    <linearGradient id="mgLeaf" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#22C55E"/>
      <stop offset="100%" stop-color="#15803D"/>
    </linearGradient>
  </defs>
  <!-- Leaf -->
  <path d="M64 36 C74 16 98 18 108 22 C106 36 94 48 76 44 Z" fill="url(#mgLeaf)"/>
  <path d="M64 36 Q88 28 108 22" stroke="#166534" stroke-width="2" fill="none"/>
  <!-- Stem -->
  <path d="M64 42 C64 30 68 24 72 20" stroke="#78350F" stroke-width="4" stroke-linecap="round" fill="none"/>
  <!-- Mango Body -->
  <path d="M64 40 C84 40 102 56 102 78 C102 102 84 118 64 118 C42 118 28 98 28 78 C28 54 44 40 64 40 Z" fill="url(#mgGrad)"/>
  <!-- Beak curve -->
  <path d="M64 118 C58 118 52 114 54 108 C56 102 64 104 64 118 Z" fill="#F59E0B"/>
  <!-- Highlight -->
  <ellipse cx="50" cy="62" rx="10" ry="16" transform="rotate(-25 50 62)" fill="#FFFFFF" opacity="0.35"/>
</svg>''',

    # 4. Mustard (Bright blooming yellow flowers and slender green siliques)
    'mustard.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="mustYellow" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FEF08A"/>
      <stop offset="100%" stop-color="#EAB308"/>
    </linearGradient>
    <linearGradient id="mustStem" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#4ADE80"/>
      <stop offset="100%" stop-color="#16A34A"/>
    </linearGradient>
  </defs>
  <path d="M64 122 L64 32" stroke="url(#mustStem)" stroke-width="5" stroke-linecap="round"/>
  <!-- Pods -->
  <path d="M64 90 Q40 76 34 60" stroke="url(#mustStem)" stroke-width="3.5" fill="none" stroke-linecap="round"/>
  <path d="M64 74 Q88 60 94 44" stroke="url(#mustStem)" stroke-width="3.5" fill="none" stroke-linecap="round"/>
  <!-- Mustard Flower Petals Top -->
  <g fill="url(#mustYellow)">
    <circle cx="64" cy="24" r="8"/>
    <circle cx="52" cy="34" r="8"/>
    <circle cx="76" cy="34" r="8"/>
    <circle cx="64" cy="44" r="8"/>
    <!-- Flower 2 left -->
    <circle cx="40" cy="46" r="6"/>
    <circle cx="32" cy="54" r="6"/>
    <circle cx="48" cy="54" r="6"/>
    <circle cx="40" cy="62" r="6"/>
    <!-- Flower 3 right -->
    <circle cx="88" cy="46" r="6"/>
    <circle cx="80" cy="54" r="6"/>
    <circle cx="96" cy="54" r="6"/>
    <circle cx="88" cy="62" r="6"/>
  </g>
  <circle cx="64" cy="34" r="3.5" fill="#CA8A04"/>
</svg>''',

    # 5. Chickpea / Bengal Gram (Rich golden roasted and fresh chickpeas)
    'chickpea.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="cpGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FDE68A"/>
      <stop offset="50%" stop-color="#D97706"/>
      <stop offset="100%" stop-color="#92400E"/>
    </linearGradient>
  </defs>
  <!-- Main Chickpea -->
  <path d="M64 24 C78 24 96 38 96 66 C96 92 80 108 64 108 C48 108 32 92 32 66 C32 46 44 28 58 24 C60 22 62 20 64 24 Z" fill="url(#cpGrad)"/>
  <!-- Chickpea distinctive beak / suture -->
  <path d="M64 24 C62 38 60 48 52 56" stroke="#78350F" stroke-width="3" fill="none" stroke-linecap="round"/>
  <circle cx="62" cy="23" r="4" fill="#F59E0B"/>
  <ellipse cx="50" cy="70" rx="6" ry="12" fill="#FFFFFF" opacity="0.25"/>
</svg>''',

    # 6. Red Gram / Tur / Arhar (Vibrant red-orange pigeon peas and pods)
    'redgram.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="rgPod" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F87171"/>
      <stop offset="100%" stop-color="#B91C1C"/>
    </linearGradient>
    <linearGradient id="rgSeed" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FDBA74"/>
      <stop offset="100%" stop-color="#C2410C"/>
    </linearGradient>
  </defs>
  <!-- Pod Shell -->
  <path d="M24 104 C40 92 78 68 108 32 C112 28 110 24 104 26 C74 48 44 80 20 98 C18 102 20 106 24 104 Z" fill="url(#rgPod)"/>
  <!-- Exposed seeds inside pod -->
  <circle cx="48" cy="76" r="13" fill="url(#rgSeed)"/>
  <circle cx="68" cy="58" r="13" fill="url(#rgSeed)"/>
  <circle cx="88" cy="40" r="13" fill="url(#rgSeed)"/>
  <circle cx="46" cy="74" r="3" fill="#FFFFFF" opacity="0.4"/>
  <circle cx="66" cy="56" r="3" fill="#FFFFFF" opacity="0.4"/>
  <circle cx="86" cy="38" r="3" fill="#FFFFFF" opacity="0.4"/>
</svg>''',

    # 7. Green Gram / Moong (Lush glossy green beans)
    'greengram.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="ggGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#86EFAC"/>
      <stop offset="40%" stop-color="#22C55E"/>
      <stop offset="100%" stop-color="#15803D"/>
    </linearGradient>
  </defs>
  <!-- Bean 1 -->
  <ellipse cx="50" cy="56" rx="28" ry="20" transform="rotate(-30 50 56)" fill="url(#ggGrad)"/>
  <path d="M42 48 Q50 54 58 60" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" fill="none" opacity="0.8"/>
  <!-- Bean 2 -->
  <ellipse cx="80" cy="76" rx="26" ry="18" transform="rotate(25 80 76)" fill="url(#ggGrad)"/>
  <path d="M72 74 Q80 78 88 82" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" fill="none" opacity="0.8"/>
</svg>''',

    # 8. Black Gram / Urad (Glossy black-seed pulse with white eye)
    'blackgram.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#475569"/>
      <stop offset="40%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#020617"/>
    </linearGradient>
  </defs>
  <ellipse cx="54" cy="54" rx="28" ry="20" transform="rotate(-35 54 54)" fill="url(#bgGrad)"/>
  <ellipse cx="54" cy="54" rx="5" ry="12" transform="rotate(-35 54 54)" fill="#F8FAFC"/>
  <ellipse cx="78" cy="78" rx="26" ry="18" transform="rotate(30 78 78)" fill="url(#bgGrad)"/>
  <ellipse cx="78" cy="78" rx="4" ry="10" transform="rotate(30 78 78)" fill="#F8FAFC"/>
</svg>''',

    # 9. Papaya (Tropical rich orange with dark seeds and green rind)
    'papaya.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="papFlesh" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FB923C"/>
      <stop offset="100%" stop-color="#EA580C"/>
    </linearGradient>
    <linearGradient id="papRind" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#84CC16"/>
      <stop offset="100%" stop-color="#15803D"/>
    </linearGradient>
  </defs>
  <!-- Outer Rind -->
  <path d="M64 16 C88 16 104 44 104 76 C104 104 86 120 64 120 C42 120 24 104 24 76 C24 44 40 16 64 16 Z" fill="url(#papRind)"/>
  <!-- Cut Orange Flesh -->
  <path d="M64 22 C84 22 96 46 96 76 C96 100 82 114 64 114 C46 114 32 100 32 76 C32 46 44 22 64 22 Z" fill="url(#papFlesh)"/>
  <!-- Hollow center cavity -->
  <ellipse cx="64" cy="74" rx="16" ry="26" fill="#FBBF24"/>
  <!-- Black seeds -->
  <circle cx="64" cy="62" r="3" fill="#1E293B"/>
  <circle cx="60" cy="70" r="3.2" fill="#0F172A"/>
  <circle cx="68" cy="72" r="3.1" fill="#1E293B"/>
  <circle cx="62" cy="78" r="3" fill="#0F172A"/>
  <circle cx="66" cy="84" r="3.2" fill="#1E293B"/>
  <circle cx="61" cy="88" r="2.8" fill="#0F172A"/>
</svg>''',

    # 10. Guava (Crisp green with fresh pink pulp)
    'guava.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="gvRind" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#86EFAC"/>
      <stop offset="100%" stop-color="#16A34A"/>
    </linearGradient>
    <linearGradient id="gvPink" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F472B6"/>
      <stop offset="100%" stop-color="#DB2777"/>
    </linearGradient>
  </defs>
  <circle cx="64" cy="68" r="48" fill="url(#gvRind)"/>
  <circle cx="64" cy="68" r="40" fill="url(#gvPink)"/>
  <!-- Guava seeds -->
  <circle cx="56" cy="60" r="3" fill="#FDE047"/>
  <circle cx="70" cy="62" r="3" fill="#FDE047"/>
  <circle cx="60" cy="74" r="3" fill="#FDE047"/>
  <circle cx="72" cy="76" r="3" fill="#FDE047"/>
  <circle cx="64" cy="84" r="3" fill="#FDE047"/>
  <!-- Leaf -->
  <path d="M64 20 C74 8 92 12 96 16 C92 26 80 30 68 24 Z" fill="#15803D"/>
</svg>''',

    # 11. Pomegranate (Ruby red with shining arils)
    'pomegranate.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="pomSkin" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F87171"/>
      <stop offset="40%" stop-color="#DC2626"/>
      <stop offset="100%" stop-color="#991B1B"/>
    </linearGradient>
  </defs>
  <!-- Crown calyx -->
  <path d="M52 24 L64 12 L76 24 L86 16 L80 30 L48 30 L42 16 Z" fill="#991B1B"/>
  <circle cx="64" cy="72" r="46" fill="url(#pomSkin)"/>
  <!-- Cut window showing red jewel seeds -->
  <path d="M50 56 C70 50 86 64 84 84 C76 96 54 94 46 80 Z" fill="#FEE2E2"/>
  <circle cx="56" cy="66" r="4.5" fill="#DC2626"/>
  <circle cx="68" cy="64" r="4.5" fill="#B91C1C"/>
  <circle cx="62" cy="76" r="5" fill="#E11D48"/>
  <circle cx="74" cy="76" r="4.5" fill="#991B1B"/>
  <circle cx="58" cy="84" r="4" fill="#DC2626"/>
  <!-- Highlight -->
  <ellipse cx="44" cy="50" rx="8" ry="14" transform="rotate(-30 44 50)" fill="#FFFFFF" opacity="0.3"/>
</svg>''',

    # 12. Lemon (Sunshine yellow citrus with green leaf)
    'lemon.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="lemGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FEF08A"/>
      <stop offset="50%" stop-color="#FACC15"/>
      <stop offset="100%" stop-color="#CA8A04"/>
    </linearGradient>
  </defs>
  <!-- Green leaf -->
  <path d="M72 26 C86 12 108 14 114 18 C110 32 94 40 80 34 Z" fill="#16A34A"/>
  <!-- Lemon body with pointed ends -->
  <path d="M30 40 C44 26 84 26 98 40 C114 56 114 84 98 100 C84 114 44 114 30 100 C14 84 14 56 30 40 Z" fill="url(#lemGrad)"/>
  <ellipse cx="48" cy="54" rx="8" ry="16" transform="rotate(-40 48 54)" fill="#FFFFFF" opacity="0.35"/>
</svg>''',

    # 13. Coconut (Hard brown textured shell with palm leaf)
    'coconut.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="cocoHusk" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#A16207"/>
      <stop offset="60%" stop-color="#78350F"/>
      <stop offset="100%" stop-color="#451A03"/>
    </linearGradient>
  </defs>
  <!-- Palm Leaf -->
  <path d="M40 32 C56 16 88 18 104 22 C96 36 78 44 56 40 Z" fill="#15803D"/>
  <!-- Coconut Body -->
  <ellipse cx="64" cy="74" rx="42" ry="46" fill="url(#cocoHusk)"/>
  <!-- Three dark eyes of coconut -->
  <circle cx="54" cy="56" r="5" fill="#291203"/>
  <circle cx="74" cy="56" r="5" fill="#291203"/>
  <circle cx="64" cy="68" r="5" fill="#291203"/>
  <!-- Fiber lines -->
  <path d="M34 74 Q64 96 94 74" stroke="#451A03" stroke-width="2" fill="none" opacity="0.5"/>
</svg>''',

    # 14. Capsicum (Glossy green bell pepper)
    'capsicum.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="capGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#4ADE80"/>
      <stop offset="50%" stop-color="#22C55E"/>
      <stop offset="100%" stop-color="#15803D"/>
    </linearGradient>
  </defs>
  <!-- Stem -->
  <path d="M64 36 C64 22 68 14 74 12" stroke="#15803D" stroke-width="6" stroke-linecap="round" fill="none"/>
  <!-- Pepper Lobes -->
  <path d="M36 44 C26 58 26 94 38 108 C50 118 64 116 64 116 C64 116 78 118 90 108 C102 94 102 58 92 44 C84 34 76 38 64 38 C52 38 44 34 36 44 Z" fill="url(#capGrad)"/>
  <path d="M50 42 C50 68 50 98 56 112" stroke="#14532D" stroke-width="2.5" fill="none" opacity="0.4"/>
  <path d="M78 42 C78 68 78 98 72 112" stroke="#14532D" stroke-width="2.5" fill="none" opacity="0.4"/>
  <!-- Highlight -->
  <ellipse cx="44" cy="60" rx="6" ry="16" fill="#FFFFFF" opacity="0.4"/>
</svg>''',

    # 15. Sesame (Golden sesame seeds)
    'sesame.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="sesGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FEF08A"/>
      <stop offset="50%" stop-color="#EAB308"/>
      <stop offset="100%" stop-color="#A16207"/>
    </linearGradient>
  </defs>
  <!-- Seed 1 -->
  <path d="M46 32 C58 32 64 54 60 70 C56 82 46 84 42 80 C36 74 34 54 40 40 Z" fill="url(#sesGrad)"/>
  <!-- Seed 2 -->
  <path d="M82 48 C94 48 100 68 96 82 C92 94 82 96 78 92 C72 86 70 68 76 54 Z" fill="url(#sesGrad)"/>
  <!-- Seed 3 small -->
  <path d="M56 82 C64 82 68 96 66 106 C64 112 58 114 54 110 C50 106 48 94 52 86 Z" fill="url(#sesGrad)"/>
</svg>''',

    # 16. Jowar / Sorghum (Dense golden grain spike)
    'jowar.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="jowGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FDE68A"/>
      <stop offset="60%" stop-color="#D97706"/>
      <stop offset="100%" stop-color="#854D0E"/>
    </linearGradient>
  </defs>
  <path d="M64 122 L64 36" stroke="#15803D" stroke-width="5" stroke-linecap="round"/>
  <!-- Dense grain cluster -->
  <ellipse cx="64" cy="52" rx="22" ry="34" fill="url(#jowGrad)"/>
  <!-- Grains details -->
  <g fill="#78350F" opacity="0.6">
    <circle cx="58" cy="38" r="3.5"/><circle cx="70" cy="38" r="3.5"/>
    <circle cx="52" cy="48" r="4"/><circle cx="64" cy="48" r="4"/><circle cx="76" cy="48" r="4"/>
    <circle cx="54" cy="60" r="4"/><circle cx="66" cy="60" r="4"/><circle cx="78" cy="60" r="3.5"/>
    <circle cx="58" cy="72" r="3.5"/><circle cx="70" cy="72" r="3.5"/>
  </g>
</svg>''',

    # 17. Bajra / Pearl Millet
    'bajra.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="bajGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#CBD5E1"/>
      <stop offset="50%" stop-color="#64748B"/>
      <stop offset="100%" stop-color="#334155"/>
    </linearGradient>
  </defs>
  <path d="M64 122 L64 24" stroke="#16A34A" stroke-width="5" stroke-linecap="round"/>
  <!-- Long slender pearl millet head -->
  <rect x="52" y="24" width="24" height="74" rx="12" fill="url(#bajGrad)"/>
  <!-- Bristles -->
  <g stroke="#94A3B8" stroke-width="1.5">
    <line x1="52" y1="36" x2="42" y2="30"/><line x1="76" y1="36" x2="86" y2="30"/>
    <line x1="52" y1="52" x2="40" y2="48"/><line x1="76" y1="52" x2="88" y2="48"/>
    <line x1="52" y1="68" x2="42" y2="64"/><line x1="76" y1="68" x2="86" y2="64"/>
    <line x1="52" y1="84" x2="44" y2="82"/><line x1="76" y1="84" x2="84" y2="82"/>
  </g>
</svg>''',

    # 18. Cardamom (Aromatic green cardamom pod)
    'cardamom.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#86EFAC"/>
      <stop offset="50%" stop-color="#22C55E"/>
      <stop offset="100%" stop-color="#15803D"/>
    </linearGradient>
  </defs>
  <!-- Cardamom ribbed capsule -->
  <path d="M64 20 C78 36 86 64 80 88 C76 102 68 112 64 112 C60 112 52 102 48 88 C42 64 50 36 64 20 Z" fill="url(#cardGrad)"/>
  <!-- Rib ridges -->
  <path d="M64 20 L64 112" stroke="#166534" stroke-width="2"/>
  <path d="M64 20 C72 40 76 74 64 112" stroke="#166534" stroke-width="1.8" fill="none"/>
  <path d="M64 20 C56 40 52 74 64 112" stroke="#166534" stroke-width="1.8" fill="none"/>
  <!-- Tip -->
  <path d="M64 14 L62 20 L66 20 Z" fill="#78350F"/>
</svg>''',

    # 19. Coriander (Lush aromatic green leaves & round golden seeds)
    'coriander.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="corLeaf" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#4ADE80"/>
      <stop offset="100%" stop-color="#15803D"/>
    </linearGradient>
  </defs>
  <path d="M64 118 C64 80 62 60 48 40" stroke="#16A34A" stroke-width="3.5" fill="none" stroke-linecap="round"/>
  <path d="M64 80 C74 64 84 56 94 44" stroke="#16A34A" stroke-width="3.5" fill="none" stroke-linecap="round"/>
  <!-- Serrated Leaflets -->
  <path d="M48 40 C34 32 30 16 44 14 C52 24 54 34 48 40 Z" fill="url(#corLeaf)"/>
  <path d="M94 44 C106 36 112 20 98 18 C90 28 88 38 94 44 Z" fill="url(#corLeaf)"/>
  <circle cx="64" cy="24" r="5" fill="#CA8A04"/>
  <circle cx="74" cy="28" r="4.5" fill="#EAB308"/>
</svg>''',

    # 20. Coffee (Ruby red coffee cherries and roasted bean)
    'coffee.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="cofRed" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F87171"/>
      <stop offset="50%" stop-color="#DC2626"/>
      <stop offset="100%" stop-color="#7F1D1D"/>
    </linearGradient>
    <linearGradient id="cofBean" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#78350F"/>
      <stop offset="100%" stop-color="#451A03"/>
    </linearGradient>
  </defs>
  <!-- Branch & Leaf -->
  <path d="M64 42 C78 26 104 28 112 32 C108 48 90 56 74 48 Z" fill="#15803D"/>
  <path d="M34 100 L94 40" stroke="#78350F" stroke-width="4" stroke-linecap="round"/>
  <!-- Red Cherries -->
  <circle cx="56" cy="62" r="18" fill="url(#cofRed)"/>
  <circle cx="76" cy="74" r="18" fill="url(#cofRed)"/>
  <circle cx="54" cy="58" r="4" fill="#FFFFFF" opacity="0.4"/>
  <circle cx="74" cy="70" r="4" fill="#FFFFFF" opacity="0.4"/>
</svg>''',

    # 21. Tea (Lush green two-leaves-and-a-bud)
    'tea.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="teaGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#86EFAC"/>
      <stop offset="60%" stop-color="#22C55E"/>
      <stop offset="100%" stop-color="#15803D"/>
    </linearGradient>
  </defs>
  <!-- Stem -->
  <path d="M64 116 L64 56" stroke="#166534" stroke-width="4.5" stroke-linecap="round"/>
  <!-- Center young bud -->
  <path d="M64 56 C60 40 62 26 64 18 C66 26 68 40 64 56 Z" fill="url(#teaGrad)"/>
  <!-- Left Leaf -->
  <path d="M64 74 C44 70 26 52 30 36 C46 38 60 56 64 74 Z" fill="url(#teaGrad)"/>
  <!-- Right Leaf -->
  <path d="M64 68 C84 64 102 46 98 30 C82 32 68 50 64 68 Z" fill="url(#teaGrad)"/>
</svg>''',

    # 22. Cashew (Golden cashew apple with grey kidney nut)
    'cashew.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="cashApple" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F87171"/>
      <stop offset="50%" stop-color="#F59E0B"/>
      <stop offset="100%" stop-color="#EAB308"/>
    </linearGradient>
    <linearGradient id="cashNut" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#94A3B8"/>
      <stop offset="100%" stop-color="#475569"/>
    </linearGradient>
  </defs>
  <!-- Cashew Apple (false fruit) -->
  <path d="M64 20 C82 20 94 36 94 56 C94 76 80 88 64 88 C48 88 34 76 34 56 C34 36 46 20 64 20 Z" fill="url(#cashApple)"/>
  <!-- Kidney nut attached below -->
  <path d="M52 88 C56 86 72 86 76 88 C82 96 82 108 72 116 C62 122 52 116 50 108 C48 100 48 94 52 88 Z" fill="url(#cashNut)"/>
</svg>'''
}

created = 0
for name, svg in ICONS.items():
    p = os.path.join(crop_dir, name)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(svg)
    created += 1

print(f"Successfully generated {created} premium colored SVG crop icons!")

MORE_ICONS = {
    # 23. Castor (Spiky seed capsule)
    'castor.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="casGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F87171"/>
      <stop offset="60%" stop-color="#DC2626"/>
      <stop offset="100%" stop-color="#991B1B"/>
    </linearGradient>
  </defs>
  <circle cx="64" cy="64" r="36" fill="url(#casGrad)"/>
  <!-- Spikes -->
  <g stroke="#991B1B" stroke-width="4" stroke-linecap="round">
    <line x1="64" y1="28" x2="64" y2="16"/><line x1="64" y1="100" x2="64" y2="112"/>
    <line x1="28" y1="64" x2="16" y2="64"/><line x1="100" y1="64" x2="112" y2="64"/>
    <line x1="38" y1="38" x2="28" y2="28"/><line x1="90" y1="90" x2="100" y2="100"/>
    <line x1="90" y1="38" x2="100" y2="28"/><line x1="38" y1="90" x2="28" y2="100"/>
  </g>
</svg>''',

    # 24. Ragi / Finger Millet
    'ragi.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="ragGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#A16207"/>
      <stop offset="60%" stop-color="#78350F"/>
      <stop offset="100%" stop-color="#451A03"/>
    </linearGradient>
  </defs>
  <path d="M64 122 L64 56" stroke="#15803D" stroke-width="5" stroke-linecap="round"/>
  <!-- Finger millet fingers -->
  <path d="M64 56 C54 36 34 26 26 30 C30 46 52 52 64 56 Z" fill="url(#ragGrad)"/>
  <path d="M64 56 C60 30 52 14 62 12 C70 24 68 46 64 56 Z" fill="url(#ragGrad)"/>
  <path d="M64 56 C74 36 94 26 102 30 C98 46 76 52 64 56 Z" fill="url(#ragGrad)"/>
  <path d="M64 56 C68 30 76 14 66 12 C58 24 60 46 64 56 Z" fill="url(#ragGrad)"/>
</svg>''',

    # 25. Cumin / Jeera
    'cumin.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="cumGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#CA8A04"/>
      <stop offset="60%" stop-color="#854D0E"/>
      <stop offset="100%" stop-color="#581C87"/>
    </linearGradient>
  </defs>
  <ellipse cx="50" cy="52" rx="12" ry="34" transform="rotate(-35 50 52)" fill="url(#cumGrad)"/>
  <line x1="34" y1="36" x2="66" y2="68" stroke="#FEF08A" stroke-width="1.8" opacity="0.6"/>
  <ellipse cx="80" cy="74" rx="12" ry="32" transform="rotate(35 80 74)" fill="url(#cumGrad)"/>
  <line x1="66" y1="90" x2="94" y2="58" stroke="#FEF08A" stroke-width="1.8" opacity="0.6"/>
</svg>''',

    # 26. Black Pepper
    'blackpepper.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="pepGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#64748B"/>
      <stop offset="50%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#020617"/>
    </linearGradient>
  </defs>
  <path d="M64 20 Q56 60 64 114" stroke="#166534" stroke-width="4" fill="none" stroke-linecap="round"/>
  <!-- Peppercorns cluster -->
  <circle cx="56" cy="40" r="10" fill="url(#pepGrad)"/><circle cx="54" cy="38" r="2.5" fill="#FFFFFF" opacity="0.4"/>
  <circle cx="72" cy="48" r="10" fill="url(#pepGrad)"/><circle cx="70" cy="46" r="2.5" fill="#FFFFFF" opacity="0.4"/>
  <circle cx="54" cy="62" r="10" fill="url(#pepGrad)"/><circle cx="52" cy="60" r="2.5" fill="#FFFFFF" opacity="0.4"/>
  <circle cx="72" cy="72" r="10" fill="url(#pepGrad)"/><circle cx="70" cy="70" r="2.5" fill="#FFFFFF" opacity="0.4"/>
  <circle cx="58" cy="86" r="9" fill="url(#pepGrad)"/><circle cx="56" cy="84" r="2.5" fill="#FFFFFF" opacity="0.4"/>
  <circle cx="68" cy="98" r="8" fill="url(#pepGrad)"/><circle cx="66" cy="96" r="2" fill="#FFFFFF" opacity="0.4"/>
</svg>''',

    # 27. Sweet Lime / Mosambi
    'sweetlime.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="mosGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#BEF264"/>
      <stop offset="50%" stop-color="#84CC16"/>
      <stop offset="100%" stop-color="#4D7C0F"/>
    </linearGradient>
  </defs>
  <path d="M64 24 C76 10 98 12 104 16 C98 28 84 34 72 28 Z" fill="#15803D"/>
  <circle cx="64" cy="72" r="46" fill="url(#mosGrad)"/>
  <ellipse cx="48" cy="54" rx="8" ry="16" transform="rotate(-30 48 54)" fill="#FFFFFF" opacity="0.3"/>
</svg>''',

    # 28. Tobacco Leaf
    'tobacco.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="tobGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FDE047"/>
      <stop offset="40%" stop-color="#CA8A04"/>
      <stop offset="100%" stop-color="#854D0E"/>
    </linearGradient>
  </defs>
  <path d="M64 16 C88 40 98 80 64 116 C30 80 40 40 64 16 Z" fill="url(#tobGrad)"/>
  <path d="M64 16 L64 120" stroke="#78350F" stroke-width="3" stroke-linecap="round"/>
  <path d="M64 42 Q80 50 86 60" stroke="#78350F" stroke-width="2" fill="none"/>
  <path d="M64 42 Q48 50 42 60" stroke="#78350F" stroke-width="2" fill="none"/>
  <path d="M64 68 Q82 76 88 88" stroke="#78350F" stroke-width="2" fill="none"/>
  <path d="M64 68 Q46 76 40 88" stroke="#78350F" stroke-width="2" fill="none"/>
</svg>''',

    # 29. Rubber
    'rubber.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="rubGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#E2E8F0"/>
      <stop offset="70%" stop-color="#94A3B8"/>
      <stop offset="100%" stop-color="#64748B"/>
    </linearGradient>
  </defs>
  <!-- Tree trunk tapping with white latex bowl -->
  <rect x="42" y="16" width="44" height="96" rx="4" fill="#78350F"/>
  <path d="M42 36 L86 64" stroke="#451A03" stroke-width="4"/>
  <!-- Collection spout & bowl -->
  <ellipse cx="64" cy="90" rx="22" ry="14" fill="url(#rubGrad)"/>
  <path d="M64 64 L64 82" stroke="#FFFFFF" stroke-width="3.5"/>
</svg>'''
}

for name, svg in MORE_ICONS.items():
    p = os.path.join(crop_dir, name)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(svg)

print("Added more crop icons!")
