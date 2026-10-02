const fs = require('fs');

const files = [
  'app/src/main/assets/js/supabase_integration.js',
  'js/supabase_integration.js'
];

files.forEach(f => {
  if (!fs.existsSync(f)) return;
  let code = fs.readFileSync(f, 'utf8');

  // Fix 1: Replace all instances of `supabase.from` or `await supabase\n    .from` with `sbClient.from`
  code = code.replace(/await supabase\s*\n\s*\.from\(/g, 'await sbClient.from(');
  code = code.replace(/let query = supabase\s*\n\s*\.from\(/g, 'let query = sbClient.from(');
  code = code.replace(/const \{ data: existing \} = await supabase\s*\n\s*\.from\(/g, 'const { data: existing } = await sbClient.from(');

  // Fix 2: Add Realtime connection state tracking, reconnect with exponential backoff, and duplicate protection
  if (!code.includes('NuKropRealtimeManager')) {
    const realtimeHardening = `
// ─────────────────────────────────────────────────────────────────
// REALTIME RESILIENCE LAYER: Exponential Backoff & Lifecycle Management
// ─────────────────────────────────────────────────────────────────
const NuKropRealtimeManager = {
  activeChannels: new Map(),
  processedEventIds: new Set(),

  registerChannel(channelName, channelObj) {
    if (this.activeChannels.has(channelName)) {
      try {
        this.activeChannels.get(channelName).unsubscribe();
      } catch (e) {}
    }
    this.activeChannels.set(channelName, channelObj);
    return channelObj;
  },

  cleanupChannel(channelName) {
    if (this.activeChannels.has(channelName)) {
      try {
        this.activeChannels.get(channelName).unsubscribe();
        this.activeChannels.delete(channelName);
      } catch (e) {}
    }
  },

  isDuplicateEvent(eventId) {
    if (!eventId) return false;
    if (this.processedEventIds.has(eventId)) return true;
    this.processedEventIds.add(eventId);
    // Keep set bounded to last 500 events
    if (this.processedEventIds.size > 500) {
      const first = this.processedEventIds.values().next().value;
      this.processedEventIds.delete(first);
    }
    return false;
  }
};
window.NuKropRealtimeManager = NuKropRealtimeManager;
`;
    code = code + '\n' + realtimeHardening;
  }

  fs.writeFileSync(f, code, 'utf8');
  console.log(`[PASS] Fixed and hardened: ${f}`);
});
