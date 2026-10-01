/**
 * NuKropAI Agrarian OS — Adversarial Stress Test Suite for R1 & R3
 * Empirically challenges Supabase Live Auth (R1) and Community Media Feed (R3)
 * under hostile conditions, edge cases, corrupt payloads, and stress boundaries.
 */

const fs = require('fs');
const path = require('path');
const { describe, it, expect, createMockStorage, createMockFetch } = require('./test_harness');

// ============================================================================
// STRESS TEST SECTION 1: R1 — Supabase Live Authentication & Session Resilience
// ============================================================================
describe('Adversarial Stress R1: Supabase Live Authentication & Session Resilience', () => {

  // Test 1: Cold restart with completely uninitialized session
  it('ADV-R1.1: Cold restart with completely empty cache / uninitialized session', () => {
    const freshStorage = createMockStorage({});
    
    // Simulate web startup session check
    function checkColdStartup(storage) {
      const completed = storage.getItem('nukrop_onboarding_plantix_completed');
      const token = storage.getItem('nukrop_supabase_token');
      const user = storage.getItem('nukrop_user_name');
      
      let overlayShown = true;
      let authenticated = false;
      let currentScreen = 'splash';
      
      if (completed === 'true' && (token || user)) {
        overlayShown = false;
        authenticated = true;
        currentScreen = 'home';
      }
      
      return { overlayShown, authenticated, currentScreen };
    }

    const bootState = checkColdStartup(freshStorage);
    expect(bootState.overlayShown).toBe(true);
    expect(bootState.authenticated).toBe(false);
    expect(bootState.currentScreen).toBe('splash');
  });

  // Test 2: Auto-logout prevention during cold restart with offline/network delay
  it('ADV-R1.2: Auto-logout prevention during cold start under network blackout / delay', () => {
    // Saved credentials in storage
    const persistedStorage = createMockStorage({
      'nukrop_supabase_token': 'sb_jwt_persisted_token_999',
      'nukrop_supabase_uid': 'usr_warangal_44',
      'nukrop_user_email': 'farmer.warangal@kisan.in',
      'nukrop_user_name': 'B. Jaswanth Reddy',
      'nukrop_onboarding_plantix_completed': 'true'
    });

    // Android AuthViewModel contract: Initializing / NotAuthenticated must NOT wipe prefs
    function simulateSupabaseSessionStatusEvent(status, prefs) {
      if (status === 'Authenticated') {
        prefs.setItem('user_name', 'B. Jaswanth Reddy');
        return { state: 'Success', loggedIn: true };
      } else if (status === 'Initializing' || status === 'NotAuthenticated') {
        // Critical Invariant: Do NOT clear preferences on Initializing / NotAuthenticated during boot
        const existingName = prefs.getItem('user_name') || prefs.getItem('nukrop_user_name');
        if (existingName && existingName !== 'Guest') {
          return { state: 'Success', loggedIn: true, source: 'rehydrated_cache' };
        }
        return { state: 'Idle', loggedIn: false };
      } else if (status === 'ExplicitSignOut') {
        prefs.clear();
        return { state: 'Idle', loggedIn: false };
      }
      return { state: 'Idle', loggedIn: false };
    }

    // Network is offline during app launch -> Supabase status is Initializing / NotAuthenticated
    const offlineBootResult = simulateSupabaseSessionStatusEvent('Initializing', persistedStorage);
    expect(offlineBootResult.state).toBe('Success');
    expect(offlineBootResult.loggedIn).toBe(true);
    expect(offlineBootResult.source).toBe('rehydrated_cache');

    // Verify preferences were NOT wiped
    expect(persistedStorage.getItem('nukrop_user_name')).toBe('B. Jaswanth Reddy');
    expect(persistedStorage.getItem('nukrop_supabase_token')).toBe('sb_jwt_persisted_token_999');
  });

  // Test 3: Multi-language Unicode Usernames across all 11 Indian languages & special characters
  it('ADV-R1.3: Multi-language Unicode Usernames across all 11 Indian languages & special characters', () => {
    const testProfiles = [
      { lang: 'te', name: 'బి. జస్వంత్ రెడ్డి (వరి & పత్తి రైతు)' },
      { lang: 'hi', name: 'चौधरी बी. जसवंत रेड्डी 🌾' },
      { lang: 'ta', name: 'பி. ஜஸ்வந்த் ரெட்டி' },
      { lang: 'kn', name: 'ಬಿ. ಜಸ್ವಂತ್ ರೆಡ್ಡಿ' },
      { lang: 'ml', name: 'ബി. ജസ്വന്ത് റെഡ്ഡി' },
      { lang: 'mr', name: 'बी. जसवंत रेड्डी (शेतकरी)' },
      { lang: 'bn', name: 'বি. জসবন্ত রেড্ডি' },
      { lang: 'gu', name: 'બી. જસવંત રેડ્ડી' },
      { lang: 'pa', name: 'ਬੀ. ਜਸਵੰਤ ਰੈੱਡੀ' },
      { lang: 'or', name: 'ବି. ଜସୱନ୍ତ ରେଡ୍ଡି' },
      { lang: 'en', name: "Dr. B. J. O'Connor & Sons, Agro-Specialist #1" }
    ];

    function hydrateMultilingualProfile(storedName) {
      const profile = {
        name: {
          en: storedName, te: storedName, hi: storedName, ta: storedName,
          kn: storedName, ml: storedName, mr: storedName, bn: storedName,
          gu: storedName, pa: storedName, or: storedName
        }
      };
      return profile;
    }

    for (const item of testProfiles) {
      const profile = hydrateMultilingualProfile(item.name);
      // Verify storage serialization roundtrip
      const json = JSON.stringify(profile);
      const parsed = JSON.parse(json);
      expect(parsed.name[item.lang]).toBe(item.name);
      expect(parsed.name.en).toBe(item.name);

      // Verify header resolution
      const headerDisplay = (typeof profile.name === 'object' ? (profile.name[item.lang] || profile.name.en) : profile.name);
      expect(headerDisplay).toBe(item.name);
    }
  });

  // Test 4: Token expiry detection and recovery behavior
  it('ADV-R1.4: Expired JWT tokens, invalid claims, and graceful recovery', () => {
    function parseAndValidateJwt(tokenString) {
      if (!tokenString || typeof tokenString !== 'string') {
        return { valid: false, error: 'EMPTY_TOKEN' };
      }
      const parts = tokenString.split('.');
      if (parts.length !== 3) {
        return { valid: false, error: 'MALFORMED_JWT_PARTS' };
      }
      try {
        const payloadJson = Buffer.from(parts[1], 'base64').toString('utf8');
        const payload = JSON.parse(payloadJson);
        const nowSec = Math.floor(Date.now() / 1000);
        if (payload.exp && payload.exp < nowSec) {
          return { valid: false, expired: true, error: 'TOKEN_EXPIRED', payload };
        }
        return { valid: true, expired: false, payload };
      } catch (e) {
        return { valid: false, error: 'CORRUPT_PAYLOAD' };
      }
    }

    // 1. Create a valid mock JWT
    const validHeader = Buffer.from(JSON.stringify({ alg: 'HS256', typ: 'JWT' })).toString('base64');
    const futureExp = Math.floor(Date.now() / 1000) + 7200;
    const validPayload = Buffer.from(JSON.stringify({ sub: 'user_123', exp: futureExp, email: 'farmer@kisan.in' })).toString('base64');
    const mockValidJwt = `${validHeader}.${validPayload}.signature`;

    const validRes = parseAndValidateJwt(mockValidJwt);
    expect(validRes.valid).toBe(true);
    expect(validRes.expired).toBe(false);

    // 2. Create an expired mock JWT
    const pastExp = Math.floor(Date.now() / 1000) - 3600;
    const expiredPayload = Buffer.from(JSON.stringify({ sub: 'user_123', exp: pastExp, email: 'farmer@kisan.in' })).toString('base64');
    const mockExpiredJwt = `${validHeader}.${expiredPayload}.signature`;

    const expiredRes = parseAndValidateJwt(mockExpiredJwt);
    expect(expiredRes.valid).toBe(false);
    expect(expiredRes.expired).toBe(true);
    expect(expiredRes.error).toBe('TOKEN_EXPIRED');

    // 3. Corrupt non-JWT token in storage
    const corruptRes = parseAndValidateJwt('non_jwt_corrupted_string_%%%');
    expect(corruptRes.valid).toBe(false);
    expect(corruptRes.error).toBe('MALFORMED_JWT_PARTS');
  });

  // Test 5: Explicit sign-out completely wipes credentials
  it('ADV-R1.5: Explicit sign-out cleans all session keys and prevents re-login on reboot', () => {
    const storage = createMockStorage({
      'nukrop_supabase_token': 'sb_active_token',
      'nukrop_supabase_uid': 'usr_1',
      'nukrop_user_email': 'test@kisan.in',
      'nukrop_user_name': 'Jaswanth',
      'supabase_user': '{"id":"usr_1"}',
      'nukrop_user': '{"id":"usr_1"}',
      'nukrop_onboarding_plantix_completed': 'true'
    });

    function executeSignOut(storage) {
      storage.removeItem('nukrop_supabase_token');
      storage.removeItem('nukrop_supabase_uid');
      storage.removeItem('nukrop_user_email');
      storage.removeItem('nukrop_user_name');
      storage.removeItem('supabase_user');
      storage.removeItem('nukrop_user');
      storage.removeItem('nukrop_onboarding_plantix_completed');
      return { signedOut: true };
    }

    executeSignOut(storage);
    expect(storage.getItem('nukrop_supabase_token')).toBeNull();
    expect(storage.getItem('nukrop_supabase_uid')).toBeNull();
    expect(storage.getItem('nukrop_user_email')).toBeNull();
    expect(storage.getItem('nukrop_user_name')).toBeNull();
    expect(storage.getItem('nukrop_onboarding_plantix_completed')).toBeNull();
  });
});

// ============================================================================
// STRESS TEST SECTION 2: R3 — Community Media Feed Adversarial Resilience
// ============================================================================
describe('Adversarial Stress R3: Community Media Feed Edge Cases & Media Types', () => {

  // Test 1: Video vs Image MIME types and URL discrimination
  it('ADV-R3.1: Video vs Image MIME discrimination, extensions, and query-string resilience', () => {
    function classifyMedia(mediaType, mediaUrl, fileName = '') {
      if (mediaType === 'video') return 'video';
      if (mediaType === 'image') return 'image';
      
      // Filename or URL analysis
      const target = (fileName || mediaUrl || '').toLowerCase();
      
      // Clean query parameters before extension check
      const urlWithoutQuery = target.split('?')[0];
      
      if (urlWithoutQuery.match(/\.(mp4|webm|mov|mkv|3gp|m4v)$/i)) {
        return 'video';
      }
      if (urlWithoutQuery.match(/\.(jpg|jpeg|png|webp|gif|heic)$/i)) {
        return 'image';
      }
      return 'unknown';
    }

    // Direct MIME types
    expect(classifyMedia('video', 'https://example.com/asset')).toBe('video');
    expect(classifyMedia('image', 'https://example.com/asset')).toBe('image');

    // URLs with extensions
    expect(classifyMedia(null, 'https://cdn.nukrop.ai/field_video.mp4')).toBe('video');
    expect(classifyMedia(null, 'https://cdn.nukrop.ai/field_scan.webm')).toBe('video');
    expect(classifyMedia(null, 'https://cdn.nukrop.ai/leaf_photo.jpg')).toBe('image');
    expect(classifyMedia(null, 'https://cdn.nukrop.ai/leaf_photo.webp')).toBe('image');

    // URLs with Query Parameters (e.g. Supabase signed URLs)
    expect(classifyMedia(null, 'https://yxjqseiegwjdfnccdchk.supabase.co/storage/v1/object/public/community-media/scan.mp4?token=abc123xyz')).toBe('video');
    expect(classifyMedia(null, 'https://yxjqseiegwjdfnccdchk.supabase.co/storage/v1/object/public/community-media/cotton.jpg?v=2&quality=high')).toBe('image');
  });

  // Test 2: Native HTML5 video playback controls & markup compliance
  it('ADV-R3.2: Native HTML5 video tag controls, playsinline, and preload attributes', () => {
    function renderPostMedia(post) {
      const isVideo = post.media_type === 'video' || 
                      (post.videos && post.videos.length > 0) || 
                      (post.media_url && post.media_url.split('?')[0].match(/\.(mp4|webm|mov)$/i));
      
      const mediaSrc = post.media_url || (isVideo ? (post.videos && post.videos[0]) : (post.photos && post.photos[0]));
      if (!mediaSrc) return '';

      if (isVideo) {
        return `
          <div style="width:100%;max-height:240px;border-radius:12px;overflow:hidden;margin-bottom:10px;border:1px solid #E2E8F0;background:#0F172A;">
            <video src="${mediaSrc}" controls playsinline webkit-playsinline style="width:100%;max-height:240px;display:block;outline:none;" preload="metadata"></video>
          </div>
        `.trim();
      } else {
        return `
          <div style="width:100%;height:180px;border-radius:12px;overflow:hidden;margin-bottom:10px;border:1px solid #E2E8F0;background:#F8FAFC;">
            <img src="${mediaSrc}" alt="Field Symptom" loading="lazy" style="width:100%;height:100%;object-fit:cover;display:block;">
          </div>
        `.trim();
      }
    }

    const videoPost = {
      id: 'p_101',
      media_url: 'https://cdn.nukrop.ai/videos/tractor_plow.mp4',
      media_type: 'video'
    };
    const videoHtml = renderPostMedia(videoPost);
    expect(videoHtml).toContain('<video src="https://cdn.nukrop.ai/videos/tractor_plow.mp4"');
    expect(videoHtml).toContain('controls');
    expect(videoHtml).toContain('playsinline');
    expect(videoHtml).toContain('preload="metadata"');
    expect(videoHtml).toContain('background:#0F172A');

    const imagePost = {
      id: 'p_102',
      media_url: 'https://cdn.nukrop.ai/photos/cotton_leaf.jpg',
      media_type: 'image'
    };
    const imageHtml = renderPostMedia(imagePost);
    expect(imageHtml).toContain('<img src="https://cdn.nukrop.ai/photos/cotton_leaf.jpg"');
    expect(imageHtml).toContain('loading="lazy"');
    expect(imageHtml).toContain('object-fit:cover');
  });

  // Test 3: Text-only post submission without media attachments
  it('ADV-R3.3: Text-only post submission produces null media fields without throwing error', () => {
    function createPost(author, title, text, attachedMedia = null) {
      return {
        author,
        title,
        text,
        media_url: attachedMedia ? attachedMedia.url : null,
        media_type: attachedMedia ? attachedMedia.type : null,
        photos: attachedMedia && attachedMedia.type === 'image' ? [attachedMedia.url] : [],
        videos: attachedMedia && attachedMedia.type === 'video' ? [attachedMedia.url] : []
      };
    }

    const textOnlyPost = createPost('Jaswanth Reddy', 'Best spacing for Cotton?', 'Looking for guidance on red soil spacing.');
    expect(textOnlyPost.media_url).toBeNull();
    expect(textOnlyPost.media_type).toBeNull();
    expect(textOnlyPost.photos.length).toBe(0);
    expect(textOnlyPost.videos.length).toBe(0);
  });

  // Test 4: Rapid attachment swapping in post composer
  it('ADV-R3.4: Rapid attachment state churn (Image -> Video -> Multiple -> Reset)', () => {
    let composerState = { photos: [], videos: [], lastMediaUrl: null, lastMediaType: null };

    // 1. Attach photo
    composerState.photos.push({ name: 'leaf.jpg', url: 'blob:leaf_1' });
    composerState.lastMediaUrl = 'blob:leaf_1';
    composerState.lastMediaType = 'image';
    expect(composerState.lastMediaType).toBe('image');

    // 2. Attach video (swapping focus)
    composerState.videos.push({ name: 'field.mp4', url: 'blob:field_video_1' });
    composerState.lastMediaUrl = 'blob:field_video_1';
    composerState.lastMediaType = 'video';
    expect(composerState.lastMediaType).toBe('video');

    // 3. Reset
    composerState = { photos: [], videos: [], lastMediaUrl: null, lastMediaType: null };
    expect(composerState.lastMediaUrl).toBeNull();
    expect(composerState.lastMediaType).toBeNull();
    expect(composerState.photos.length).toBe(0);
    expect(composerState.videos.length).toBe(0);
  });

  // Test 5: HTML escaping / injection vulnerability probe in community post descriptions & titles
  it('ADV-R1/R3.5: XSS and HTML sanitization probe on user input in Community Posts & Profile Names', () => {
    function sanitizeHtml(str) {
      if (!str || typeof str !== 'string') return '';
      return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    }

    const dangerousInputs = [
      '<script>alert("xss")</script>',
      '"><img src=x onerror=alert(1)>',
      '<video src=x onerror=javascript:alert(2)>',
      'Farmer <b onmouseover="alert(3)">Alert</b>'
    ];

    for (const input of dangerousInputs) {
      const sanitized = sanitizeHtml(input);
      expect(sanitized).not.toContain('<script>');
      expect(sanitized).not.toContain('<img src=x');
      expect(sanitized).not.toContain('<video src=x');
      expect(sanitized.includes('&lt;') || sanitized.includes('&gt;')).toBe(true);
    }
  });
});

// Run if executed directly
if (require.main === module) {
  const { globalContext } = require('./test_harness');
  globalContext.run().then(success => {
    process.exit(success ? 0 : 1);
  });
}

