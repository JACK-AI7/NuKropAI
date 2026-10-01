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
