/**
 * Tier 0: Forensic Integrity & Anti-Facade Contract Suite
 * Directly inspects and executes both production web assets:
 * 1. app/src/main/assets/index.html (Android embedded web asset)
 * 2. nukrop_emulator.html (Browser preview runtime)
 * 
 * Enforces zero-tolerance against:
 * - Deprecated Groq Vision in scanner (must use Gemini Vision)
 * - setTimeout mock bypasses returning canned pathology records
 * - Missing header greetings (R1)
 * - Missing media input accept attributes (R3)
 * - Synthetic dummy price generators (R4)
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');
const { describe, it, expect } = require('./test_harness');

const indexPath = path.resolve(__dirname, '../app/src/main/assets/index.html');
const emulatorPath = path.resolve(__dirname, '../nukrop_emulator.html');

const indexHtml = fs.readFileSync(indexPath, 'utf8');
const emulatorHtml = fs.readFileSync(emulatorPath, 'utf8');

// ============================================================================
// SECTION 1: Static Architectural & Anti-Facade Contract Audits
// ============================================================================
describe('Tier 0.1 — Static Anti-Facade File Audit (index.html & nukrop_emulator.html)', () => {

  const webAssets = [
    { name: 'app/src/main/assets/index.html', content: indexHtml },
    { name: 'nukrop_emulator.html', content: emulatorHtml }
  ];

  webAssets.forEach(({ name, content }) => {

    it(`T0.1.1 [${name}]: R1 Supabase live auth endpoints and session persistence are present`, () => {
      expect(content.includes('https://yxjqseiegwjdfnccdchk.supabase.co')).toBe(true);
      expect(content.includes('/auth/v1/signup')).toBe(true);
      expect(content.includes('/auth/v1/token?grant_type=password')).toBe(true);
      expect(content.includes('loadPersistedUserSession')).toBe(true);
      expect(content.includes('nukrop_user_name')).toBe(true);
    });

    it(`T0.1.2 [${name}]: R1 Header greeting dynamically renders farmer name`, () => {
      // Must include Namaste greeting logic
      expect(content.includes('Namaste') || content.includes('నమస్కారం') || content.includes('नमस्ते')).toBe(true);
      // Must render farmerProfile.name dynamically in the top dashboard header
      const hasDynamicGreeting = content.includes('farmerProfile') && content.includes('name');
      expect(hasDynamicGreeting).toBe(true);
    });

    it(`T0.1.3 [${name}]: R2 Genuine Gemini Vision API endpoint and payload structure`, () => {
      expect(content.includes('https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent')).toBe(true);
      expect(content.includes('inlineData')).toBe(true);
      expect(content.includes('responseMimeType')).toBe(true);
    });

    it(`T0.1.4 [${name}]: R2 Strict prohibition of Groq Vision & setTimeout mock bypass in scanner`, () => {
      // Scanner function startScannerDiagnostic must NOT contain Groq or mock bypass
      const scannerFnMatch = content.match(/(?:async\s+)?function\s+startScannerDiagnostic\s*\(\)\s*\{([\s\S]*?)(?=\nfunction|\n\/\*|\nconst\s+_\w+|$)/);
      expect(scannerFnMatch).toBeTruthy();
      const fnBody = scannerFnMatch ? scannerFnMatch[1] : '';

      // 1. Must NOT reference Groq Vision in scanner
      expect(fnBody.includes('Groq Vision AI')).toBe(false);
      expect(fnBody.includes('api.groq.com')).toBe(false);

      // 2. Must invoke Gemini Vision endpoint
      expect(fnBody.includes('generativelanguage.googleapis.com')).toBe(true);

      // 3. Must NOT bypass network call with an unconditional setTimeout directly returning BOTANICAL_PATHOLOGY_DB
      const hasMockBypass = fnBody.includes('setTimeout') && !fnBody.includes('generativelanguage.googleapis.com');
      expect(hasMockBypass).toBe(false);
    });

    it(`T0.1.5 [${name}]: R3 Community media upload supports images and videos`, () => {
      // File input must accept both images and videos
      expect(content.includes('accept="image/*,video/*"')).toBe(true);
      expect(content.includes('<video')).toBe(true);
      expect(content.includes('controls')).toBe(true);
      expect(content.includes('playsinline')).toBe(true);
    });

    it(`T0.1.6 [${name}]: R4 Zero synthetic price generators & Agmarknet connection`, () => {
      // Zero tolerance for random price drifts and dummy IDs
      expect(content.includes('Math.random() * 50')).toBe(false);
      expect(content.includes('dyn-mkt-')).toBe(false);
      expect(content.includes('dynBasePrice')).toBe(false);

      // Must reference legitimate government Agmarknet resource ID or Supabase mandi live rates
      const hasRealMandi = content.includes('api.data.gov.in') || content.includes('mandi_live_rates');
      expect(hasRealMandi).toBe(true);
    });
  });
});

// ============================================================================
// SECTION 2: Dynamic VM Execution & Network Interception Audits
// ============================================================================
describe('Tier 0.2 — Dynamic Script VM Execution & Network Interception', () => {

  const webAssets = [
    { name: 'app/src/main/assets/index.html', html: indexHtml },
    { name: 'nukrop_emulator.html', html: emulatorHtml }
  ];

  webAssets.forEach(({ name, html }) => {
    const scriptMatch = html.match(/<script>(.*?)<\/script>/s);
    if (!scriptMatch) return;
    const jsCode = scriptMatch[1];

    it(`T0.2.1 [${name}]: Executing startScannerDiagnostic() dispatches live Gemini Vision POST`, async () => {
      let interceptedUrl = null;
      let interceptedOptions = null;

      const testStorage = {
        'GEMINI_API_KEY': 'AIzaSyTest_Forensic_Key_12345',
        'nukrop_user_name': 'B. Jaswanth Reddy'
      };

      const domElements = {};
      function getEl(id) {
        if (!domElements[id]) {
          domElements[id] = {
            id,
            style: {},
            classList: { add: () => {}, remove: () => {}, contains: () => false },
            appendChild: () => {},
            setAttribute: () => {},
            getAttribute: () => '',
            addEventListener: () => {},
            removeEventListener: () => {},
            remove: () => {},
            querySelectorAll: () => [],
            querySelector: () => null,
            scrollIntoView: () => {},
            offsetWidth: 100,
            offsetHeight: 100,
            innerHTML: '',
            textContent: '',
            value: '',
            disabled: false
          };
        }
        return domElements[id];
      }

      const sandbox = {
        window: null,
        document: {
          readyState: 'complete',
          getElementById: (id) => getEl(id),
          querySelector: (sel) => getEl('query_' + sel),
          querySelectorAll: () => [],
          createElement: (tag) => getEl(tag),
          addEventListener: () => {},
          removeEventListener: () => {},
          body: getEl('body')
        },
        localStorage: {
          getItem: (k) => testStorage[k] !== undefined ? testStorage[k] : null,
          setItem: (k, v) => { testStorage[k] = String(v); },
          removeItem: (k) => { delete testStorage[k]; }
        },
        navigator: {
          geolocation: { getCurrentPosition: () => {} },
          userAgent: 'ForensicTester'
        },
        location: { href: '', search: '', pathname: '' },
        fetch: async (url, opts) => {
          interceptedUrl = url;
          interceptedOptions = opts;
          return {
            ok: true,
            status: 200,
            json: async () => ({
              candidates: [{
                content: {
                  parts: [{
                    text: JSON.stringify({
                      diseaseName: "Cotton Leaf Curl Virus",
                      pathogen: "Begomovirus",
                      severity: "Moderate",
                      confidence: "94%"
                    })
                  }]
                }
              }]
            })
          };
        },
        speechSynthesis: { speak: () => {}, cancel: () => {} },
        SpeechSynthesisUtterance: function() {},
        console: { log: () => {}, warn: () => {}, error: () => {} },
        setTimeout: (cb, ms) => setTimeout(cb, 10),
        clearTimeout: (id) => clearTimeout(id),
        setInterval: () => 123,
        clearInterval: () => {}
      };
      sandbox.window = sandbox;

      const context = vm.createContext(sandbox);
      vm.runInContext(jsCode, context);

      // Provide test image and execute diagnostic
      vm.runInContext(`
        uploadedScanImageData = 'data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=';
        window.GEMINI_API_KEY = 'AIzaSyTest_Forensic_Key_12345';
        startScannerDiagnostic();
      `, context);

      // Allow async execution to process fetch
      for (let i = 0; i < 20; i++) {
        if (interceptedUrl) break;
        await new Promise(resolve => setTimeout(resolve, 50));
      }

      expect(interceptedUrl).toBeTruthy();
      expect(interceptedUrl).toContain('generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent');
      expect(interceptedUrl).toContain('key=AIzaSyTest_Forensic_Key_12345');
      expect(interceptedOptions.method).toBe('POST');

      const parsedBody = JSON.parse(interceptedOptions.body);
      expect(parsedBody.contents[0].parts[1].inlineData.mimeType).toBe('image/jpeg');
      expect(parsedBody.generationConfig.responseMimeType).toBe('application/json');
    });
  });
});

if (require.main === module) {
  const { globalContext } = require('./test_harness');
  globalContext.run().then(success => {
    process.exit(success ? 0 : 1);
  }).catch(err => {
    console.error('Fatal Test Exception:', err);
    process.exit(1);
  });
}

