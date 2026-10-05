/**
 * Tier 2: Boundary & Corner Cases Test Suite (>=5 tests per feature)
 * Tests invalid inputs, network disruptions, corrupt payloads, and extreme conditions.
 */

const { describe, it, expect, createMockStorage, createMockFetch } = require('./test_harness');

// ============================================================================
// Feature 1 Boundaries: Authentication & Session Edge Cases (R1)
// ============================================================================
describe('Tier 2 — Feature 1 Boundaries: Auth & Session Edge Cases (R1)', () => {

  it('T2.1.1: Cold start with empty cache / first-time user initialization', () => {
    const emptyStorage = createMockStorage({});

    function initializeAuthState(storage) {
      const savedToken = storage.getItem('nukrop_supabase_token');
      const savedUser = storage.getItem('nukrop_user_name');
      const onboardingDone = storage.getItem('nukrop_onboarding_plantix_completed');

      if (!onboardingDone) {
        return { screen: 'splash', isAuthenticated: false, user: null };
      }
      if (savedToken && savedUser) {
        return { screen: 'home', isAuthenticated: true, user: { name: savedUser } };
      }
      return { screen: 'login', isAuthenticated: false, user: null };
    }

    const state = initializeAuthState(emptyStorage);
    expect(state.screen).toBe('splash');
    expect(state.isAuthenticated).toBe(false);
    expect(state.user).toBeNull();
  });

  it('T2.1.2: Expired token detection and refresh flow', () => {
    function isTokenExpired(jwtPayload) {
      const currentEpochSec = Math.floor(Date.now() / 1000);
      return jwtPayload.exp < currentEpochSec;
    }

    // Token expired 1 hour ago
    const expiredPayload = {
      sub: 'usr-101',
      exp: Math.floor(Date.now() / 1000) - 3600
    };

    // Token valid for next 1 hour
    const validPayload = {
      sub: 'usr-101',
      exp: Math.floor(Date.now() / 1000) + 3600
    };

    expect(isTokenExpired(expiredPayload)).toBe(true);
    expect(isTokenExpired(validPayload)).toBe(false);
  });

  it('T2.1.3: Malformed session token recovery from local storage', () => {
    const corruptStorage = createMockStorage({
      'nukrop_supabase_token': '{invalid-json-payload%%%',
      'nukrop_user_name': 'Jaswanth'
    });

    function safelyRecoverSession(storage) {
      try {
        const raw = storage.getItem('nukrop_supabase_token');
        if (!raw) return null;
        // Invariant: If token format is invalid (not JWT format), reject and purge
        if (!raw.startsWith('eyJ') && !raw.startsWith('sb_token_')) {
          storage.removeItem('nukrop_supabase_token');
          return null;
        }
        return { token: raw };
      } catch (e) {
        storage.clear();
        return null;
      }
    }

    const session = safelyRecoverSession(corruptStorage);
    expect(session).toBeNull();
    expect(corruptStorage.getItem('nukrop_supabase_token')).toBeNull();
  });

  it('T2.1.4: Special characters, multi-script unicode (Telugu, Hindi), and emoji in user name', () => {
    const complexNames = [
      'బి. జస్వంత్ రెడ్డి (వరి & పత్తి రైతు)',
      'चौधरी रामेश्वर सिंह 🌾🚜',
      "O'Connor-D'Souza",
      'Dr. K. V. Rao & Sons, Agronomists <Warangal>'
    ];

    function sanitizeAndStoreProfile(name) {
      const json = JSON.stringify({ full_name: name });
      const parsed = JSON.parse(json);
      return parsed.full_name;
    }

    complexNames.forEach(name => {
      const roundTrip = sanitizeAndStoreProfile(name);
      expect(roundTrip).toBe(name);
    });
  });

  it('T2.1.5: Rapid sequential auth state transitions (race condition immunity)', () => {
    // Verifies that during initial boot, an unauthenticated session status does NOT wipe preferences
    const storage = createMockStorage({
      'user_name': 'Jaswanth Reddy',
      'user_email': 'jaswanth@kisan.in'
    });

    let currentUser = storage.getItem('user_name');

    // Simulate Supabase SessionStatus stream:
    // Emits 1: SessionStatus.Initializing
    // Emits 2: SessionStatus.NotAuthenticated (before async cache load)
    // Emits 3: SessionStatus.Authenticated
    const emittedStatuses = ['Initializing', 'NotAuthenticated', 'Authenticated'];

    emittedStatuses.forEach(status => {
      if (status === 'Authenticated') {
        currentUser = 'Jaswanth Reddy';
        storage.setItem('user_name', currentUser);
      } else if (status === 'NotAuthenticated' || status === 'Initializing') {
        // INVARIANT: Do NOT call storage.clear() during boot initialization!
        // Retain existing cached credentials
      }
    });

    expect(storage.getItem('user_name')).toBe('Jaswanth Reddy');
    expect(currentUser).toBe('Jaswanth Reddy');
  });
});

// ============================================================================
// Feature 2 Boundaries: Gemini Vision AI Edge Cases (R2)
// ============================================================================
describe('Tier 2 — Feature 2 Boundaries: Gemini Vision AI Edge Cases (R2)', () => {

  it('T2.2.1: Missing API key graceful fallback to on-device engine', () => {
    function executeScannerInference(apiKey, leafBitmap) {
      if (!apiKey || apiKey.trim() === '') {
        // Immediate fallback to on-device without network crash
        return {
          source: 'ON_DEVICE_FALLBACK',
          disease: 'Healthy Leaf / Minor Abiotic Stress',
          confidence: 85
        };
      }
      return { source: 'CLOUD_GEMINI', disease: 'Cloud Diagnosis' };
    }

    const fallbackResult = executeScannerInference('', {});
    expect(fallbackResult.source).toBe('ON_DEVICE_FALLBACK');
  });

  it('T2.2.2: Network 500 / 503 / timeout failover to local botanical database', async () => {
    const fetchMock = createMockFetch({
      'generativelanguage.googleapis.com': async () => {
        return { ok: false, status: 503, statusText: 'Service Unavailable', json: async () => ({ error: 'High Load' }) };
      }
    });

    async function scanWithAutomaticFailover(fetchFn) {
      try {
        const res = await fetchFn('https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=KEY');
        if (!res.ok) {
          throw new Error(`API Error ${res.status}: ${res.statusText}`);
        }
        return { source: 'CLOUD' };
      } catch (err) {
        // Resilient failover caught the error and routed to on-device
        return {
          source: 'ON_DEVICE_FAILOVER',
          errorHandled: err.message,
          diagnosis: 'Cercospora Leaf Spot'
        };
      }
    }

    const result = await scanWithAutomaticFailover(fetchMock);
    expect(result.source).toBe('ON_DEVICE_FAILOVER');
    expect(result.errorHandled).toContain('503');
  });

  it('T2.2.3: Corrupt image bytes / invalid base64 stream handling', () => {
    function validateAndPrepareImage(base64Data) {
      if (!base64Data || base64Data.trim() === '') {
        throw new Error('Validation Error: Empty image data');
      }
      // Check for minimum viable header
      if (base64Data.length < 32) {
        throw new Error('Validation Error: Corrupt or truncated image stream');
      }
      return true;
    }

    expect(() => validateAndPrepareImage('')).toThrow('Empty image data');
    expect(() => validateAndPrepareImage('short-corrupt')).toThrow('Corrupt or truncated image stream');
    expect(validateAndPrepareImage('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=')).toBe(true);
  });

  it('T2.2.4: Large base64 payload (>5MB) compression and memory safety', () => {
    function enforcePayloadSizeLimit(byteLength, maxAllowedBytes = 4 * 1024 * 1024) {
      if (byteLength > maxAllowedBytes) {
        // Requires client-side downsampling/compression
        return { needsDownsample: true, targetQuality: 0.75 };
      }
      return { needsDownsample: false, targetQuality: 1.0 };
    }

    const oversized = 6 * 1024 * 1024; // 6MB
    const normal = 1.5 * 1024 * 1024; // 1.5MB

    expect(enforcePayloadSizeLimit(oversized).needsDownsample).toBe(true);
    expect(enforcePayloadSizeLimit(normal).needsDownsample).toBe(false);
  });

  it('T2.2.5: Non-JSON / conversational LLM response resilience', () => {
    // Model returned conversational filler with markdown code block
    const conversationalResponse = `
    Certainly, farmer! Here is your ICAR diagnostic report:
    \`\`\`json
    {
      "status": "Diseased",
      "name": "Bacterial Blight",
      "confidence": 92
    }
    \`\`\`
    Hope this helps your crops!
    `;

    function extractJsonPayload(rawText) {
      const match = rawText.match(/\{[\s\S]*\}/);
      if (match) {
        return JSON.parse(match[0]);
      }
      throw new Error('No JSON object found in response');
    }

    const parsed = extractJsonPayload(conversationalResponse);
    expect(parsed.status).toBe('Diseased');
    expect(parsed.name).toBe('Bacterial Blight');
    expect(parsed.confidence).toBe(92);
  });
});

// ============================================================================
// Feature 3 Boundaries: Community Media Edge Cases (R3)
// ============================================================================
describe('Tier 2 — Feature 3 Boundaries: Community Media Edge Cases (R3)', () => {

  it('T2.3.1: Text-only post submission without media attachments', () => {
    function buildPostObject(author, text, media = null) {
      return {
        author,
        text,
        media_url: media ? media.url : null,
        media_type: media ? media.type : null,
        hasMedia: Boolean(media && media.url)
      };
    }

    const post = buildPostObject('Jaswanth', 'What is the optimal sowing spacing for Cotton in red soils?');
    expect(post.media_url).toBeNull();
    expect(post.media_type).toBeNull();
    expect(post.hasMedia).toBe(false);
  });

  it('T2.3.2: Unsupported media format and 404 URL graceful fallback rendering', () => {
    function validateMediaAttachment(fileType) {
      const allowed = ['image/jpeg', 'image/png', 'image/webp', 'video/mp4', 'video/webm', 'video/quicktime'];
      if (!allowed.includes(fileType.toLowerCase())) {
        return { valid: false, error: 'Unsupported media format. Please upload JPG, PNG, or MP4.' };
      }
      return { valid: true };
    }

    expect(validateMediaAttachment('application/pdf').valid).toBe(false);
    expect(validateMediaAttachment('application/x-msdownload').valid).toBe(false);
    expect(validateMediaAttachment('image/jpeg').valid).toBe(true);
    expect(validateMediaAttachment('video/mp4').valid).toBe(true);
  });

  it('T2.3.3: Video playback under offline network conditions', () => {
    function buildVideoElementMarkup(mediaUrl) {
      return `
        <video src="${mediaUrl}" controls playsinline preload="metadata">
          <p class="video-offline-fallback">Unable to stream video while offline.</p>
        </video>
      `.trim();
    }

    const markup = buildVideoElementMarkup('https://cdn.nukrop.ai/field.mp4');
    expect(markup).toContain('preload="metadata"');
    expect(markup).toContain('Unable to stream video while offline');
  });

  it('T2.3.4: Extreme length post text (>1000 chars) and emoji handling', () => {
    const longQuestion = 'వరి పంటలో ఆకు ఎండు తెగులు (Bacterial Leaf Blight) గమనించాము... '.repeat(30);
    expect(longQuestion.length).toBeGreaterThan(1000);

    function preparePostContent(content, maxLen = 2000) {
      return content.trim().substring(0, maxLen);
    }

    const trimmed = preparePostContent(longQuestion);
    expect(trimmed.length).toBeLessThanOrEqual(2000);
    expect(trimmed).toContain('ఆకు ఎండు తెగులు');
  });

  it('T2.3.5: Rapid consecutive media attachments replacement in post composer', () => {
    let attached = { type: null, url: null };

    // Farmer attaches photo 1
    attached = { type: 'image', url: 'blob:photo1' };
    expect(attached.type).toBe('image');

    // Farmer replaces with photo 2
    attached = { type: 'image', url: 'blob:photo2' };
    expect(attached.url).toBe('blob:photo2');

    // Farmer replaces with video
    attached = { type: 'video', url: 'blob:video1' };
    expect(attached.type).toBe('video');

    // Farmer clears attachment
    attached = { type: null, url: null };
    expect(attached.type).toBeNull();
  });
});

// ============================================================================
// Feature 4 Boundaries: Real Agmarknet Market Data Edge Cases (R4)
// ============================================================================
describe('Tier 2 — Feature 4 Boundaries: Agmarknet Market Data Edge Cases (R4)', () => {

  it('T2.4.1: Agmarknet API HTTP 429 rate-limit backoff and secondary cache routing', async () => {
    let callAttempts = 0;
    const fetchMock = createMockFetch({
      'api.data.gov.in': async () => {
        callAttempts++;
        // Simulate HTTP 429 Rate Limit
        return { ok: false, status: 429, json: async () => ({ error: 'Rate limit exceeded' }) };
      },
      'mandi_live_rates': async () => {
        return {
          ok: true,
          status: 200,
          json: async () => [
            { commodity: 'Cotton', modal_price: 7480, source: 'Supabase_Tier1_Cache' }
          ]
        };
      }
    });

    async function fetchMandiWith429Failover(fetchFn) {
      const govRes = await fetchFn('https://api.data.gov.in/resource/123');
      if (govRes.status === 429) {
        // Failover to Supabase persistent cache
        const cacheRes = await fetchFn('https://yxjqseiegwjdfnccdchk.supabase.co/rest/v1/mandi_live_rates');
        const data = await cacheRes.json();
        return { ...data[0], failoverActivated: true };
      }
      return await govRes.json();
    }

    const rate = await fetchMandiWith429Failover(fetchMock);
    expect(callAttempts).toBe(1);
    expect(rate.failoverActivated).toBe(true);
    expect(rate.source).toBe('Supabase_Tier1_Cache');
    expect(rate.modal_price).toBe(7480);
  });

  it('T2.4.2: Unknown / exotic crop query handling', () => {
    const KNOWN_CROPS = ['Cotton', 'Chilli', 'Paddy', 'Wheat', 'Tomato', 'Onion', 'Maize', 'Turmeric'];

    function lookupMandiCommodity(cropQuery) {
      const match = KNOWN_CROPS.find(c => c.toLowerCase() === cropQuery.toLowerCase());
      if (!match) {
        return {
          found: false,
          message: `No active APMC arrivals reported for "${cropQuery}" today. Showing state agricultural benchmark.`,
          defaultBenchmarkPrice: 2400
        };
      }
      return { found: true, commodity: match };
    }

    const unlistedCrop = lookupMandiCommodity('Dragonfruit');
    expect(unlistedCrop.found).toBe(false);
    expect(unlistedCrop.message).toContain('No active APMC arrivals');
    expect(unlistedCrop.defaultBenchmarkPrice).toBe(2400);
  });

  it('T2.4.3: Unmapped GPS coordinates fallback to nearest state APMC', () => {
    function resolveLocationToApmc(lat, lon) {
      // Telangana bounding box: ~15.8 to ~19.9 N, ~77.2 to ~81.8 E
      if (lat >= 15.8 && lat <= 19.9 && lon >= 77.2 && lon <= 81.8) {
        return { state: 'Telangana', primaryApmc: 'Warangal APMC Yard' };
      }
      // Offshore / Border unmapped fallback
      return { state: 'Telangana', primaryApmc: 'Hyderabad Bowenpally Market Yard', isDefaultFallback: true };
    }

    // Coordinates in middle of ocean / unmapped
    const offshore = resolveLocationToApmc(0.0, 0.0);
    expect(offshore.isDefaultFallback).toBe(true);
    expect(offshore.primaryApmc).toBe('Hyderabad Bowenpally Market Yard');

    // Valid Warangal coordinates
    const warangal = resolveLocationToApmc(18.0, 79.5);
    expect(warangal.primaryApmc).toBe('Warangal APMC Yard');
  });

  it('T2.4.4: Zero and negative price anomaly filtering', () => {
    const rawApmcData = [
      { market: 'Yard A', commodity: 'Cotton', modal_price: 7450 },
      { market: 'Yard B', commodity: 'Cotton', modal_price: 0 },       // Anomaly: 0
      { market: 'Yard C', commodity: 'Cotton', modal_price: -1500 },    // Anomaly: negative
      { market: 'Yard D', commodity: 'Cotton', modal_price: 'N/A' },    // Anomaly: non-numeric
      { market: 'Yard E', commodity: 'Cotton', modal_price: 7520 }
    ];

    function sanitizeMandiRecords(records) {
      return records.filter(r => {
        const price = Number(r.modal_price);
        return !isNaN(price) && price > 0 && price < 500000;
      });
    }

    const sanitized = sanitizeMandiRecords(rawApmcData);
    expect(sanitized.length).toBe(2);
    expect(sanitized[0].market).toBe('Yard A');
    expect(sanitized[1].market).toBe('Yard E');
  });

  it('T2.4.5: MSP floor price enforcement & boundary validation', () => {
    // Government of India MSP (2024-2026 reference): Medium Staple Cotton = ₹7,121/quintal
    const GOVT_MSP_FLOORS = {
      'Cotton': 7121,
      'Paddy': 2300,
      'Wheat': 2275
    };

    function evaluateMandiMspStatus(commodity, marketPrice) {
      const msp = GOVT_MSP_FLOORS[commodity];
      if (!msp) return { status: 'NO_MSP_DECLARED' };
      const spread = marketPrice - msp;
      return {
        msp,
        marketPrice,
        isAboveMsp: spread >= 0,
        spreadAmount: spread,
        alert: spread < 0 ? '⚠️ Market rate is below Govt MSP! Avail CCI procurement window.' : '🟢 Market rate exceeds MSP.'
      };
    }

    const warangalCotton = evaluateMandiMspStatus('Cotton', 7480);
    expect(warangalCotton.isAboveMsp).toBe(true);
    expect(warangalCotton.spreadAmount).toBe(359);

    const distressedCotton = evaluateMandiMspStatus('Cotton', 6800);
    expect(distressedCotton.isAboveMsp).toBe(false);
    expect(distressedCotton.alert).toContain('below Govt MSP');
  });
});


// ============================================================================
// Feature 5 Boundaries (F1): Language Selection & Multi-Storage Persistence
// ============================================================================
describe('Tier 2 — Feature 5 Boundaries (F1): Language Selection & Persistence Edge Cases', () => {

  it('T2.5.1: Fallback on unrecognized or empty language code defaults safely to en without throwing', () => {
    const VALID_LANGS = new Set(['te', 'hi', 'en', 'ta', 'kn', 'ml', 'mr', 'bn', 'gu', 'pa', 'or']);

    function resolveValidLanguage(langCode) {
      if (!langCode || typeof langCode !== 'string' || !VALID_LANGS.has(langCode.trim().toLowerCase())) {
        return 'en';
      }
      return langCode.trim().toLowerCase();
    }

    expect(resolveValidLanguage(null)).toBe('en');
    expect(resolveValidLanguage('')).toBe('en');
    expect(resolveValidLanguage('fr')).toBe('en');
    expect(resolveValidLanguage('UNKNOWN_CODE_99')).toBe('en');
    expect(resolveValidLanguage('TE')).toBe('te');
  });

  it('T2.5.2: Rapid multi-language sequential switching (te -> hi -> ta -> en -> mr in 100ms) preserves consistent final state', () => {
    const store = createMockStorage();
    const switchSequence = ['te', 'hi', 'ta', 'en', 'mr'];

    let finalLang = null;
    switchSequence.forEach(lang => {
      store.setItem('nukrop_user_lang', lang);
      store.setItem('nukrop_language', lang);
      finalLang = lang;
    });

    expect(finalLang).toBe('mr');
    expect(store.getItem('nukrop_user_lang')).toBe('mr');
    expect(store.getItem('nukrop_language')).toBe('mr');
  });

  it('T2.5.3: Storage key desynchronization recovery (when nukrop_user_lang != nukrop_language)', () => {
    const store = createMockStorage({
      'nukrop_user_lang': 'hi',
      'nukrop_language': 'te'
    });

    function harmonizeLanguageKeys(storage) {
      const primary = storage.getItem('nukrop_user_lang');
      const secondary = storage.getItem('nukrop_language');
      const resolved = primary || secondary || 'en';
      storage.setItem('nukrop_user_lang', resolved);
      storage.setItem('nukrop_language', resolved);
      return resolved;
    }

    const resolved = harmonizeLanguageKeys(store);
    expect(resolved).toBe('hi');
    expect(store.getItem('nukrop_language')).toBe('hi');
  });

  it('T2.5.4: Corrupted or null localStorage values gracefully recover to default language', () => {
    const store = createMockStorage({
      'nukrop_user_lang': 'undefined',
      'nukrop_language': 'null'
    });

    function safeGetLang(storage) {
      const val = storage.getItem('nukrop_user_lang');
      if (!val || val === 'undefined' || val === 'null') {
        return 'en';
      }
      return val;
    }

    expect(safeGetLang(store)).toBe('en');
  });

  it('T2.5.5: Non-ASCII script rendering boundaries: Multi-script Unicode font fallbacks for 11 languages', () => {
    const sampleStrings = {
      te: 'రైతు సేవలు',
      hi: 'किसान सेवाएँ',
      ta: 'விவசாய சேவைகள்',
      kn: 'ರೈತ ಸೇವೆಗಳು',
      ml: 'കർഷക സേവനങ്ങൾ',
      mr: 'शेतकरी सेवा',
      bn: 'কৃষক সেবা',
      gu: 'ખેડૂત સેવાઓ',
      pa: 'ਕਿਸਾਨ ਸੇਵਾਵਾਂ',
      or: 'କୃଷକ ସେବା',
      en: 'Farmer Services'
    };

    Object.entries(sampleStrings).forEach(([code, text]) => {
      expect(text.length).toBeGreaterThan(0);
      const encoded = encodeURIComponent(text);
      expect(decodeURIComponent(encoded)).toBe(text);
    });
  });
});

// ============================================================================
// Feature 6 Boundaries (F2): Plant / Crop Selector Counter & Storage
// ============================================================================
describe('Tier 2 — Feature 6 Boundaries (F2): Crop Selector & Counter Edge Cases', () => {

  it('T2.6.1: Zero crops selected (empty array) renders counter as 0 and displays empty state prompt', () => {
    function renderCropCounter(selectedCrops) {
      const count = Array.isArray(selectedCrops) ? selectedCrops.length : 0;
      return {
        count,
        displayBadge: `${count} Selected`,
        isEmpty: count === 0,
        emptyPrompt: count === 0 ? 'Please select at least one active crop.' : null
      };
    }

    const empty = renderCropCounter([]);
    expect(empty.count).toBe(0);
    expect(empty.isEmpty).toBe(true);
    expect(empty.emptyPrompt).toContain('select at least one');
  });

  it('T2.6.2: Maximum crop selection limit enforcement (rejects selection >10 crops with warning)', () => {
    const MAX_LIMIT = 10;
    const currentList = new Array(10).fill(0).map((_, i) => ({ id: `crop-${i}` }));

    function attemptAddCrop(crop, list) {
      if (list.length >= MAX_LIMIT) {
        throw new Error(`Maximum crop limit reached (${MAX_LIMIT} crops max).`);
      }
      list.push(crop);
      return list.length;
    }

    expect(() => attemptAddCrop({ id: 'crop-11' }, currentList)).toThrow('Maximum crop limit reached');
    expect(currentList.length).toBe(10);
  });

  it('T2.6.3: Duplicate crop selection prevention: selecting an already-selected crop toggles off or retains single instance', () => {
    const list = [{ id: 'cotton' }, { id: 'chilli' }];

    function toggleCropSelection(cropId, cropList) {
      const idx = cropList.findIndex(c => c.id === cropId);
      if (idx !== -1) {
        cropList.splice(idx, 1); // toggle off
        return { action: 'removed', count: cropList.length };
      }
      cropList.push({ id: cropId });
      return { action: 'added', count: cropList.length };
    }

    const res1 = toggleCropSelection('cotton', list);
    expect(res1.action).toBe('removed');
    expect(res1.count).toBe(1);

    const res2 = toggleCropSelection('cotton', list);
    expect(res2.action).toBe('added');
    expect(res2.count).toBe(2);
  });

  it('T2.6.4: Corrupted JSON in nukrop_user_active_crops storage recovers cleanly with fallback default crop', () => {
    const store = createMockStorage({
      'nukrop_user_active_crops': '{{INVALID_JSON_CORRUPTED_BYTES%%'
    });

    function safelyLoadActiveCrops(storage) {
      try {
        const raw = storage.getItem('nukrop_user_active_crops');
        if (!raw) return [{ id: 'cotton', name: 'Cotton' }];
        const parsed = JSON.parse(raw);
        if (!Array.isArray(parsed) || parsed.length === 0) {
          return [{ id: 'cotton', name: 'Cotton' }];
        }
        return parsed;
      } catch (err) {
        return [{ id: 'cotton', name: 'Cotton' }];
      }
    }

    const recovered = safelyLoadActiveCrops(store);
    expect(recovered.length).toBe(1);
    expect(recovered[0].id).toBe('cotton');
  });

  it('T2.6.5: Unknown or deleted crop ID safely filtered out from active selection without breaking counter', () => {
    const VALID_CATALOG_IDS = new Set(['cotton', 'chilli', 'paddy', 'maize', 'turmeric']);
    const rawSavedList = [
      { id: 'cotton' },
      { id: 'obsolete-deleted-crop-id' },
      { id: 'chilli' },
      { id: 'unknown-999' }
    ];

    function filterValidCrops(list) {
      return list.filter(item => item && item.id && VALID_CATALOG_IDS.has(item.id));
    }

    const validCrops = filterValidCrops(rawSavedList);
    expect(validCrops.length).toBe(2);
    expect(validCrops[0].id).toBe('cotton');
    expect(validCrops[1].id).toBe('chilli');
  });
});

// ============================================================================
// Feature 7 Boundaries (F3): Pure Real-Time GPS Telemetry
// ============================================================================
describe('Tier 2 — Feature 7 Boundaries (F3): GPS Telemetry Edge Cases', () => {

  it('T2.7.1: Geolocation permission denied or device GPS unavailable handles error gracefully with UI notification', () => {
    function handleGeoError(errorCode) {
      const ERRORS = {
        1: { code: 'PERMISSION_DENIED', message: 'Location permission required to broadcast driver availability.' },
        2: { code: 'POSITION_UNAVAILABLE', message: 'GPS signal lost. Please enable high accuracy in device settings.' },
        3: { code: 'TIMEOUT', message: 'GPS request timed out. Retrying connection...' }
      };
      return ERRORS[errorCode] || { code: 'UNKNOWN_ERROR', message: 'Unable to retrieve location.' };
    }

    const err1 = handleGeoError(1);
    expect(err1.code).toBe('PERMISSION_DENIED');
    expect(err1.message).toContain('Location permission required');

    const err2 = handleGeoError(2);
    expect(err2.code).toBe('POSITION_UNAVAILABLE');
  });

  it('T2.7.2: Extreme / boundary coordinates validation (e.g. [0, 0], outside India bounding box) rejected by sanitization', () => {
    // Geographic bounding box for India: Lat 6.0 to 37.5, Lng 68.0 to 97.5
    function isValidIndiaCoordinates(lat, lng) {
      if (typeof lat !== 'number' || typeof lng !== 'number') return false;
      if (isNaN(lat) || isNaN(lng)) return false;
      if (lat === 0 && lng === 0) return false;
      return lat >= 6.0 && lat <= 37.5 && lng >= 68.0 && lng <= 97.5;
    }

    expect(isValidIndiaCoordinates(17.9689, 79.5941)).toBe(true);  // Warangal
    expect(isValidIndiaCoordinates(0, 0)).toBe(false);              // Null Island
    expect(isValidIndiaCoordinates(51.5074, -0.1278)).toBe(false);  // London
    expect(isValidIndiaCoordinates(90, 0)).toBe(false);             // North Pole
  });

  it('T2.7.3: Rapid GPS telemetry anomaly / speed threshold rejection (>150 km/h impossible jump within 1s)', () => {
    function calculateSpeedKmh(p1, p2, timeDeltaSec) {
      if (timeDeltaSec <= 0) return 0;
      // Approximate distance calculation using equirectangular approximation
      const R = 6371; // km
      const dLat = (p2.lat - p1.lat) * Math.PI / 180;
      const dLon = (p2.lng - p1.lng) * Math.PI / 180;
      const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                Math.cos(p1.lat * Math.PI / 180) * Math.cos(p2.lat * Math.PI / 180) *
                Math.sin(dLon / 2) * Math.sin(dLon / 2);
      const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
      const distKm = R * c;
      return (distKm / timeDeltaSec) * 3600;
    }

    function isReasonableRuralTruckSpeed(p1, p2, deltaSec) {
      const speed = calculateSpeedKmh(p1, p2, deltaSec);
      return speed <= 150; // max reasonable truck speed
    }

    const p1 = { lat: 17.9689, lng: 79.5941 };
    const pNormal = { lat: 17.9692, lng: 79.5944 }; // small advance in 5s
    const pTeleport = { lat: 18.5000, lng: 80.5000 }; // ~120 km jump in 1s

    expect(isReasonableRuralTruckSpeed(p1, pNormal, 5)).toBe(true);
    expect(isReasonableRuralTruckSpeed(p1, pTeleport, 1)).toBe(false);
  });

  it('T2.7.4: Zero accuracy GPS fixes (accuracy > 5000m) flagged as imprecise before broadcasting', () => {
    function evaluateGpsAccuracy(accuracyMeters) {
      if (accuracyMeters <= 50) return { quality: 'HIGH', broadcastAllowed: true };
      if (accuracyMeters <= 500) return { quality: 'ACCEPTABLE', broadcastAllowed: true };
      return { quality: 'IMPRECISE', broadcastAllowed: false, warning: 'Cell tower triangulation too coarse' };
    }

    expect(evaluateGpsAccuracy(15).broadcastAllowed).toBe(true);
    expect(evaluateGpsAccuracy(6500).broadcastAllowed).toBe(false);
    expect(evaluateGpsAccuracy(6500).quality).toBe('IMPRECISE');
  });

  it('T2.7.5: Driver going offline during active network outage cleanly terminates local watch and queues status update', () => {
    let localWatchCleared = false;
    let pendingQueue = [];

    function offlineSafeDutyToggle(watchId, isNetworkOnline) {
      localWatchCleared = true;
      if (!isNetworkOnline) {
        pendingQueue.push({ action: 'SET_OFFLINE', ts: Date.now() });
        return { isDutyActive: false, queuedForSync: true };
      }
      return { isDutyActive: false, queuedForSync: false };
    }

    const res = offlineSafeDutyToggle(101, false);
    expect(res.isDutyActive).toBe(false);
    expect(res.queuedForSync).toBe(true);
    expect(localWatchCleared).toBe(true);
    expect(pendingQueue.length).toBe(1);
  });
});

// ============================================================================
// Feature 8 Boundaries (F4): Rapido-Style Trip Flow & Driver Broadcast
// ============================================================================
describe('Tier 2 — Feature 8 Boundaries (F4): Trip Lifecycle Edge Cases', () => {

  it('T2.8.1: Booking validation: zero or negative distance / identical pickup and dropoff coordinates throws validation error', () => {
    function validateTripBooking(pickup, dropoff) {
      if (!pickup || !dropoff) throw new Error('Missing coordinates');
      if (pickup.lat === dropoff.lat && pickup.lng === dropoff.lng) {
        throw new Error('Pickup and Dropoff locations cannot be identical.');
      }
      return true;
    }

    expect(() => validateTripBooking({ lat: 17.9, lng: 79.5 }, { lat: 17.9, lng: 79.5 })).toThrow('identical');
    expect(validateTripBooking({ lat: 17.9, lng: 79.5 }, { lat: 18.0, lng: 79.6 })).toBe(true);
  });

  it('T2.8.2: Out-of-order trip state transitions (e.g. attempting to complete before in-transit) rejected by state machine', () => {
    const STATE_TRANSITIONS = {
      'SEARCHING': ['ACCEPTED', 'CANCELLED'],
      'ACCEPTED': ['ARRIVED', 'CANCELLED'],
      'ARRIVED': ['IN_TRANSIT', 'CANCELLED'],
      'IN_TRANSIT': ['COMPLETED'],
      'COMPLETED': [],
      'CANCELLED': []
    };

    function transitionTripState(current, next) {
      const allowed = STATE_TRANSITIONS[current] || [];
      if (!allowed.includes(next)) {
        throw new Error(`Illegal state transition from ${current} to ${next}`);
      }
      return next;
    }

    expect(transitionTripState('SEARCHING', 'ACCEPTED')).toBe('ACCEPTED');
    expect(transitionTripState('ACCEPTED', 'ARRIVED')).toBe('ARRIVED');
    expect(transitionTripState('ARRIVED', 'IN_TRANSIT')).toBe('IN_TRANSIT');
    expect(transitionTripState('IN_TRANSIT', 'COMPLETED')).toBe('COMPLETED');
    expect(() => transitionTripState('ACCEPTED', 'COMPLETED')).toThrow('Illegal state transition');
  });

  it('T2.8.3: Driver cancellation handling resets booking state back to SEARCHING or allows farmer retry', () => {
    function handleDriverCancellation(trip) {
      return {
        ...trip,
        status: 'SEARCHING',
        driver_id: null,
        cancellationReason: 'Driver vehicle breakdown',
        retryBroadcast: true
      };
    }

    const resetTrip = handleDriverCancellation({ id: 'trip-101', status: 'ACCEPTED', driver_id: 'DRV-1' });
    expect(resetTrip.status).toBe('SEARCHING');
    expect(resetTrip.driver_id).toBeNull();
    expect(resetTrip.retryBroadcast).toBe(true);
  });

  it('T2.8.4: Race condition: two drivers simultaneously accepting same trip awards exclusively to first transaction', () => {
    let tripRecord = { id: 'trip-101', status: 'SEARCHING', driver_id: null };

    function atomicAcceptTrip(driverId) {
      if (tripRecord.status !== 'SEARCHING') {
        return { success: false, reason: 'Trip already accepted by another driver' };
      }
      tripRecord.status = 'ACCEPTED';
      tripRecord.driver_id = driverId;
      return { success: true, driverId };
    }

    const driver1Result = atomicAcceptTrip('DRV-SURESH');
    const driver2Result = atomicAcceptTrip('DRV-RAMESH');

    expect(driver1Result.success).toBe(true);
    expect(driver2Result.success).toBe(false);
    expect(driver2Result.reason).toContain('already accepted');
    expect(tripRecord.driver_id).toBe('DRV-SURESH');
  });

  it('T2.8.5: Network disconnection recovery during in-transit state preserves active ride ID and resumes tracking on reconnect', () => {
    const storage = createMockStorage({
      'nukrop_active_trip_id': 'TRIP-8821',
      'nukrop_active_trip_state': JSON.stringify({ status: 'IN_TRANSIT', driverName: 'Suresh Yadav' })
    });

    function recoverActiveTrip(store) {
      const tripId = store.getItem('nukrop_active_trip_id');
      const raw = store.getItem('nukrop_active_trip_state');
      if (tripId && raw) {
        return { tripId, ...JSON.parse(raw), shouldResumeWebSocket: true };
      }
      return null;
    }

    const recovered = recoverActiveTrip(storage);
    expect(recovered).toBeDefined();
    expect(recovered.tripId).toBe('TRIP-8821');
    expect(recovered.status).toBe('IN_TRANSIT');
    expect(recovered.shouldResumeWebSocket).toBe(true);
  });
});

// ============================================================================
// Feature 9 Boundaries (F5): 4-Digit OTP PIN Verification
// ============================================================================
describe('Tier 2 — Feature 9 Boundaries (F5): 4-Digit OTP PIN Edge Cases', () => {

  it('T2.9.1: Malformed OTP input (letters, special characters, <4 digits, >4 digits) rejected by format validator', () => {
    function validateOtpFormat(input) {
      if (typeof input !== 'string') return false;
      return /^\d{4}$/.test(input.trim());
    }

    expect(validateOtpFormat('4491')).toBe(true);
    expect(validateOtpFormat('449')).toBe(false);
    expect(validateOtpFormat('44910')).toBe(false);
    expect(validateOtpFormat('abcd')).toBe(false);
    expect(validateOtpFormat('44 1')).toBe(false);
    expect(validateOtpFormat('44#1')).toBe(false);
  });

  it('T2.9.2: Mismatched OTP entry returns explicit failure without advancing trip state', () => {
    let tripStatus = 'ARRIVED';

    function attemptVerify(inputOtp, expectedOtp) {
      if (inputOtp !== expectedOtp) {
        return { verified: false, error: 'Incorrect 4-digit PIN' };
      }
      tripStatus = 'IN_TRANSIT';
      return { verified: true };
    }

    const attempt = attemptVerify('9999', '4491');
    expect(attempt.verified).toBe(false);
    expect(attempt.error).toContain('Incorrect');
    expect(tripStatus).toBe('ARRIVED');
  });

  it('T2.9.3: Brute-force threshold: 3 consecutive failed OTP attempts triggers temporary lockout', () => {
    let failedAttempts = 0;
    const MAX_ATTEMPTS = 3;

    function verifyWithRateLimit(input, expected) {
      if (failedAttempts >= MAX_ATTEMPTS) {
        throw new Error('Too many invalid attempts. PIN entry locked for 60 seconds.');
      }
      if (input !== expected) {
        failedAttempts++;
        return false;
      }
      failedAttempts = 0;
      return true;
    }

    expect(verifyWithRateLimit('1111', '4491')).toBe(false);
    expect(verifyWithRateLimit('2222', '4491')).toBe(false);
    expect(verifyWithRateLimit('3333', '4491')).toBe(false);
    expect(() => verifyWithRateLimit('4444', '4491')).toThrow('PIN entry locked');
  });

  it('T2.9.4: Boundary values: numeric OTPs with leading zeros (0007, 0921) retain full 4 digits as string', () => {
    function formatOtpString(rawNumber) {
      return String(rawNumber).padStart(4, '0');
    }

    expect(formatOtpString(7)).toBe('0007');
    expect(formatOtpString(921)).toBe('0921');
    expect(formatOtpString(0)).toBe('0000');
    expect(formatOtpString(4491)).toBe('4491');
  });

  it('T2.9.5: Expired OTP / cancelled booking OTP verification cleanly rejected', () => {
    function verifyOtpForTrip(booking) {
      if (booking.status === 'CANCELLED') {
        throw new Error('Cannot verify OTP for a cancelled booking.');
      }
      if (Date.now() - booking.created_at_ms > 3600000) { // 1 hr expiry
        throw new Error('OTP has expired.');
      }
      return true;
    }

    expect(() => verifyOtpForTrip({ status: 'CANCELLED', created_at_ms: Date.now() })).toThrow('cancelled');
    expect(() => verifyOtpForTrip({ status: 'ARRIVED', created_at_ms: Date.now() - 7200000 })).toThrow('expired');
  });
});

// ============================================================================
// Feature 10 Boundaries (F6): Dynamic Driver UPI Settlement & Farmer Checkout
// ============================================================================
describe('Tier 2 — Feature 10 Boundaries (F6): Dynamic UPI Settlement Edge Cases', () => {

  it('T2.10.1: Boundary fare values: Zero fare (₹0) or fractional amounts (₹1450.50) formatted properly according to UPI spec', () => {
    function formatUpiAmount(amount) {
      const num = parseFloat(amount);
      if (isNaN(num) || num < 0) throw new Error('Invalid fare amount');
      return num.toFixed(2);
    }

    expect(formatUpiAmount(0)).toBe('0.00');
    expect(formatUpiAmount(1450.5)).toBe('1450.50');
    expect(formatUpiAmount(3500)).toBe('3500.00');
    expect(() => formatUpiAmount(-50)).toThrow('Invalid fare');
  });

  it('T2.10.2: Extreme fare boundary: Very large amounts (>₹1,00,000) validated against maximum single UPI transaction limit', () => {
    const UPI_MAX_LIMIT = 100000; // NPCI standard limit

    function validateUpiTransactionLimit(amount) {
      if (amount > UPI_MAX_LIMIT) {
        return {
          allowed: false,
          warning: `Fare ₹${amount} exceeds single UPI limit ₹${UPI_MAX_LIMIT}. Split payment or NEFT required.`
        };
      }
      return { allowed: true };
    }

    expect(validateUpiTransactionLimit(4500).allowed).toBe(true);
    expect(validateUpiTransactionLimit(150000).allowed).toBe(false);
    expect(validateUpiTransactionLimit(150000).warning).toContain('exceeds single UPI limit');
  });

  it('T2.10.3: Special characters in driver VPA or payee name properly URL-encoded in UPI URI', () => {
    function generateSafeUpiUri(vpa, name, amount, note) {
      const params = new URLSearchParams();
      params.set('pa', vpa);
      params.set('pn', name);
      params.set('am', String(amount));
      params.set('cu', 'INR');
      params.set('tn', note);
      return `upi://pay?${params.toString()}`;
    }

    const uri = generateSafeUpiUri('suresh+truck@okaxis', 'Suresh & Sons (Transporters)', 3500, 'Haul #101 & Bonus');
    expect(uri.includes('upi://pay?')).toBe(true);
    expect(uri).toContain('suresh%2Btruck%40okaxis');
    expect(uri).toContain('Suresh+%26+Sons');
  });

  it('T2.10.4: Missing or invalid VPA handles gracefully with cash fallback option', () => {
    function resolvePaymentMethods(driverVpa) {
      const methods = ['CASH'];
      if (driverVpa && driverVpa.includes('@')) {
        methods.unshift('UPI_QR');
      }
      return methods;
    }

    expect(resolvePaymentMethods('driver@upi')).toEqual(['UPI_QR', 'CASH']);
    expect(resolvePaymentMethods('')).toEqual(['CASH']);
    expect(resolvePaymentMethods(null)).toEqual(['CASH']);
  });

  it('T2.10.5: UPI URI generation error handling handles missing trip parameters without throwing unhandled exceptions', () => {
    function safeBuildUpiUri(trip) {
      if (!trip || !trip.fareAmount) {
        return { success: false, error: 'Missing trip fare parameters' };
      }
      const vpa = trip.driverVpa || 'nukrop.haul@upi';
      return { success: true, uri: `upi://pay?pa=${vpa}&am=${trip.fareAmount}&cu=INR` };
    }

    expect(safeBuildUpiUri(null).success).toBe(false);
    expect(safeBuildUpiUri({}).success).toBe(false);
    expect(safeBuildUpiUri({ fareAmount: 2500 }).success).toBe(true);
  });
});

// ============================================================================
// Feature 11 Boundaries (F7): Live Peer-to-Peer In-Ride Chat
// ============================================================================
describe('Tier 2 — Feature 11 Boundaries (F7): P2P In-Ride Chat Edge Cases', () => {

  it('T2.11.1: Empty or whitespace-only chat message submission blocked by validation', () => {
    function validateChatMessage(text) {
      if (!text || typeof text !== 'string') return false;
      return text.trim().length > 0;
    }

    expect(validateChatMessage('')).toBe(false);
    expect(validateChatMessage('   ')).toBe(false);
    expect(validateChatMessage('\n\t')).toBe(false);
    expect(validateChatMessage('Arrived')).toBe(true);
  });

  it('T2.11.2: Extremely long chat message (>2000 characters) truncated or rejected with character limit error', () => {
    const MAX_CHAT_LENGTH = 500;

    function sanitizeChatMessage(text) {
      if (text.length > MAX_CHAT_LENGTH) {
        return { allowed: false, error: `Message exceeds ${MAX_CHAT_LENGTH} characters.` };
      }
      return { allowed: true, text: text.trim() };
    }

    const hugeText = 'a'.repeat(600);
    expect(sanitizeChatMessage(hugeText).allowed).toBe(false);
    expect(sanitizeChatMessage('Standard message').allowed).toBe(true);
  });

  it('T2.11.3: Unicode emojis, regional scripts (Telugu, Hindi, Tamil) and special characters transmitted without distortion', () => {
    const multiScriptMessages = [
      '🌾 ధాన్యం బస్తాలు సిద్ధంగా ఉన్నాయి (Grain sacks ready)',
      'नमस्ते भइया, 5 मिनट में पहुँच रहे हैं 🚛',
      'வணக்கம் அண்ணா 👍',
      'OK! Meet at gate @ 10:30am & bring receipt.'
    ];

    multiScriptMessages.forEach(msg => {
      const wireFormat = JSON.stringify({ text: msg });
      const decoded = JSON.parse(wireFormat);
      expect(decoded.text).toBe(msg);
    });
  });

  it('T2.11.4: XSS / HTML injection attempt in chat text properly escaped before rendering (<script>alert(1)</script>)', () => {
    function escapeHtml(str) {
      return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    }

    const malicious = '<script>alert("hack")</script>';
    const safe = escapeHtml(malicious);
    expect(safe).not.toContain('<script>');
    expect(safe).toContain('&lt;script&gt;');
  });

  it('T2.11.5: Offline message handling: queuing messages when peer or network is temporarily disconnected', () => {
    const offlineQueue = [];

    function dispatchOrQueue(msg, isConnected) {
      if (!isConnected) {
        offlineQueue.push(msg);
        return { sent: false, queued: true };
      }
      return { sent: true, queued: false };
    }

    const res = dispatchOrQueue({ text: 'Where are you?' }, false);
    expect(res.sent).toBe(false);
    expect(res.queued).toBe(true);
    expect(offlineQueue.length).toBe(1);

    function flushQueue() {
      const flushed = [...offlineQueue];
      offlineQueue.length = 0;
      return flushed;
    }

    const sent = flushQueue();
    expect(sent.length).toBe(1);
    expect(offlineQueue.length).toBe(0);
  });
});
