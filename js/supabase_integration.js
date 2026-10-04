/**
 * NuKropAI - Supabase Architecture & Realtime Sync Layer (V5 - Production Ready)
 * Fully aligned to the actual Supabase schema.
 * Fixed: receiver_name NOT NULL, profiles FK, haul_bookings persistence,
 *        presence tracking, chat history, community history.
 */

const SUPABASE_URL = localStorage.getItem('nukrop_supabase_url') || 'https://yxjqseiegwjdfnccdchk.supabase.co';
const SUPABASE_ANON_KEY = localStorage.getItem('nukrop_supabase_key') || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl4anFzZWllZ3dqZGZuY2NkY2hrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODU5NDU2NTMsImV4cCI6MjEwMTUyMTY1M30.J4swglpV5qu3hRZFll3aqhG1Y2G9mUllvXMjKq6Ikmo';

var sbClient = null;
if (typeof window.supabase !== 'undefined') {
  sbClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY, {
    auth: { persistSession: true, autoRefreshToken: true }
  });
  window.sbClient = sbClient;
  console.log('🟢 NuKropAI: Supabase V5 Production Architecture Connected.');
  sbClient.auth.onAuthStateChange((event, session) => {
    if (event === 'SIGNED_IN')  console.log('✅ Session Restored / Signed In');
    if (event === 'SIGNED_OUT') console.log('❌ Signed Out');
    if (event === 'TOKEN_REFRESHED') console.log('🔄 Token Auto-Refreshed');
  });
} else {
  console.warn('🟡 Supabase JS lib not loaded. Realtime disabled — running offline mode.');
}

// ─────────────────────────────────────────────────────────────────
// 1. AUTH — SIGNUP & LOGIN
// FIX: On signup, creates both `profiles` AND `user_profiles` rows
//      to satisfy the foreign-key constraint.
// ─────────────────────────────────────────────────────────────────
async function nk_signUp(email, password, fullName) {
  if (!sbClient) return { data: null, error: 'Offline' };
  try {
    // Step 1: Create Supabase Auth user
    const { data: authData, error: authError } = await sbClient.auth.signUp({ email, password });
    if (authError) throw authError;

    const userUuid = authData?.user?.id || null;
    const farmerId = 'NK-' + Math.floor(10000 + Math.random() * 89999);

    // Step 2: Insert into `profiles` first with proper UUID relationship
    await sbClient.from('profiles').insert([{
      id: userUuid,
      user_id: userUuid,
      email,
      full_name: fullName,
      farmer_id: farmerId,
      role: 'farmer'
    }]);

    // Step 3: Insert into `user_profiles`
    await sbClient.from('user_profiles').insert([{
      user_id: userUuid,
      email,
      full_name: fullName,
      farmer_id: farmerId
    }]);

    if (userUuid) localStorage.setItem('nukrop_user_uuid', userUuid);
    localStorage.setItem('nukrop_farmer_id', farmerId);
    localStorage.setItem('nukrop_user_email', email);
    localStorage.setItem('nukrop_user_name', fullName);
    return { data: authData, error: null };
  } catch (err) {
    console.error('SignUp Error:', err.message);
    return { data: null, error: err };
  }
}

async function nk_loginUser(email, password) {
  if (!sbClient) return { data: null, error: 'Offline' };
  try {
    const { data, error } = await sbClient.auth.signInWithPassword({ email, password });
    if (error) throw error;

    if (data?.user?.id) {
      localStorage.setItem('nukrop_user_uuid', data.user.id);
    }

    // Fetch and cache the full farmer profile on login
    const profile = await nk_fetchUserProfile(email);
    if (profile) {
      localStorage.setItem('nukrop_active_user', JSON.stringify(profile));
      localStorage.setItem('nukrop_farmer_id', profile.farmer_id || '');
      localStorage.setItem('nukrop_user_name', profile.full_name || '');
      if (profile.id) localStorage.setItem('nukrop_user_uuid', profile.id);
    }
    return { data, error: null };
  } catch (err) {
    console.error('Login Error:', err.message);
    return { data: null, error: err };
  }
}

async function nk_logout() {
  if (!sbClient) return;
  await sbClient.auth.signOut();
  localStorage.removeItem('nukrop_active_user');
  localStorage.removeItem('nukrop_farmer_id');
}

async function nk_fetchUserProfile(email) {
  if (!sbClient) return null;
  const { data, error } = await sbClient.from('user_profiles').select('*').eq('email', email).single();
  if (error) console.warn('Profile fetch:', error.message);
  return data;
}

// ─────────────────────────────────────────────────────────────────
// 2. COMMUNITY POSTS (Plantix Style)
// ─────────────────────────────────────────────────────────────────
async function nk_fetchCommunityHistory(cropId = 'all', limit = 50) {
  if (!sbClient) return [];
  let query = sbClient.from('community_posts').select('*, community_comments(count), community_likes(count)')
    .order('created_at', { ascending: false }).limit(limit);
  if (cropId !== 'all') query = query.eq('crop_id', cropId);
  const { data, error } = await query;
  if (error) console.warn('Community fetch:', error.message);
  return data || [];
}

function nk_subscribeToCommunityPosts(onNewPostCallback) {
  if (!sbClient) return;
  sbClient.channel('realtime:community_posts')
    .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'community_posts' },
      payload => {
        console.log('🌱 New Community Post:', payload.new.title);
        onNewPostCallback(payload.new);
      })
    .subscribe();
}

async function nk_createCommunityPost(authorName, title, content, cropId, mediaUrl = null) {
  if (!sbClient) return { data: null, error: 'Offline' };
  const farmerId = localStorage.getItem('nukrop_farmer_id') || 'NK-87621';
  const { data, error } = await sbClient.from('community_posts').insert([{
    author_name: authorName,
    farmer_id:   farmerId,
    title,
    content,
    crop_id:    cropId,
    crop_tag:   cropId,
    media_url:  mediaUrl
  }]);
  if (error) console.error('Create post error:', error.message);
  return { data, error };
}

async function nk_togglePostLike(postId, userId) {
  if (!sbClient) return;
  // Check if already liked
  const { data: existing } = await sbClient.from('community_likes').select('id').eq('post_id', postId).eq('user_id', userId).single();
  if (existing) {
    await sbClient.from('community_likes').delete().eq('id', existing.id);
    await sbClient.from('community_posts').update({ likes_count: sbClient.rpc('decrement', { x: 1 }) }).eq('id', postId);
  } else {
    await sbClient.from('community_likes').insert([{ post_id: postId, user_id: userId }]);
    await sbClient.from('community_posts').update({ likes_count: sbClient.rpc('increment', { x: 1 }) }).eq('id', postId);
  }
}

async function nk_addComment(postId, authorName, content) {
  if (!sbClient) return;
  const farmerId = localStorage.getItem('nukrop_farmer_id') || 'NK-87621';
  await sbClient.from('community_comments').insert([{
    post_id:     postId,
    author_name: authorName,
    farmer_id:   farmerId,
    content
  }]);
}

// ─────────────────────────────────────────────────────────────────
// 3. GRAMHAUL — REAL-TIME HAUL REQUESTS + PERSISTENCE
// FIX: Now writes accepted bookings to `haul_bookings` table.
// ─────────────────────────────────────────────────────────────────
function nk_subscribeToHaulRequests(driverId, onRequestCallback) {
  if (!sbClient) return;
  sbClient.channel(`haul:${driverId}`)
    .on('broadcast', { event: 'new_haul' }, payload => {
      console.log('🚚 Incoming Haul Request:', payload.payload);
      onRequestCallback(payload.payload);
    }).subscribe();
}

async function nk_sendHaulRequest(driverId, haulData) {
  if (!sbClient) {
    localStorage.setItem('gh_haul_request', JSON.stringify(haulData));
    return;
  }
  const channel = sbClient.channel(`haul:${driverId}`);
  await channel.send({ type: 'broadcast', event: 'new_haul', payload: haulData });
  console.log('📤 Haul request broadcast to driver:', driverId);
}

// FIX: Persist accepted haul to `haul_bookings` table using authenticated farmer UUID
async function nk_acceptHaul(haulData) {
  if (!sbClient) return;
  const userUuid = localStorage.getItem('nukrop_user_uuid') || null;
  const farmerId = localStorage.getItem('nukrop_farmer_id') || 'NK-87621';
  const { data, error } = await sbClient.from('haul_bookings').insert([{
    farmer_user_id:    userUuid,
    farmer_id:         farmerId,
    pickup_village:    haulData.pickup   || 'Farm Location',
    destination_mandi: haulData.mandi    || 'APMC Yard',
    crop_name:         haulData.crop     || 'Cotton',
    load_quintals:     haulData.weight   || 40,
    agreed_fare:       haulData.fare     || 1850,
    truck_type:        haulData.truckType || 'Commercial Freight 2.5T',
    status:            'CONFIRMED'
  }]);
  if (error) console.error('Haul booking save error:', error.message);
  return data;
}

async function nk_fetchHaulHistory() {
  if (!sbClient) return [];
  const userUuid = localStorage.getItem('nukrop_user_uuid');
  const farmerId = localStorage.getItem('nukrop_farmer_id') || 'NK-87621';
  let query = sbClient.from('haul_bookings').select('*');
  if (userUuid) {
    query = query.or(`farmer_user_id.eq.${userUuid},farmer_id.eq.${farmerId}`);
  } else {
    query = query.eq('farmer_id', farmerId);
  }
  const { data, error } = await query.order('created_at', { ascending: false });
  return data || [];
}

// ─────────────────────────────────────────────────────────────────
// 4. DRIVER GPS SYNC + PRESENCE (Online/Offline tracking)
// ─────────────────────────────────────────────────────────────────
let _gpsInterval = null;

async function nk_updateDriverTelemetry(driverId, lat, lng, speed = 0, heading = 0) {
  if (!sbClient || !driverId) return;
  const userUuid = localStorage.getItem('nukrop_user_uuid') || null;
  const driverName = localStorage.getItem('nukrop_user_name') || 'Registered Driver';
  const payload = {
    driver_id: driverId,
    driver_name: driverName,
    vehicle_plate: localStorage.getItem('nukrop_driver_plate') || 'TS 03 COMMERCIAL',
    vehicle_type: localStorage.getItem('nukrop_driver_vehicle') || 'Commercial Freight 2.5T',
    current_lat: lat,
    current_lng: lng,
    speed_kmh: speed,
    heading: heading,
    is_online: true,
    last_ping: new Date().toISOString()
  };
  if (userUuid) payload.user_id = userUuid;

  try {
    const { data, error } = await sbClient
      .from('driver_telemetry')
      .update(payload)
      .eq('driver_id', driverId)
      .select('driver_id');
    
    // Only attempt insert if an authenticated session exists (avoids 401 RLS restriction on anon)
    if (!error && (!data || data.length === 0)) {
      const { data: sessionData } = await sbClient.auth.getSession();
      if (sessionData && sessionData.session) {
        await sbClient.from('driver_telemetry').insert([payload]);
      }
    }
  } catch (_) {}
}

function nk_startDriverLocationBroadcast(driverId, lat, lng) {
  if (!sbClient) return;
  if (_gpsInterval) clearInterval(_gpsInterval); // Prevent duplicate intervals

  // Update cloud telemetry record immediately
  nk_updateDriverTelemetry(driverId, lat, lng);

  // Clean up any existing channel with same topic to avoid duplicate callback crash
  const topic = `gps:${driverId}`;
  if (sbClient.getChannels) {
    const existing = sbClient.getChannels().find(c => c.topic === `realtime:${topic}` || c.topic === topic);
    if (existing) {
      try { sbClient.removeChannel(existing); } catch (_) {}
    }
  }

  const channel = sbClient.channel(topic, {
    config: { presence: { key: driverId } }
  });

  channel
    .on('presence', { event: 'sync' }, () => console.log('Driver Presence Synced'))
    .subscribe(async (status) => {
      if (status === 'SUBSCRIBED') {
        await channel.track({ driver: driverId, status: 'ONLINE', at: new Date().toISOString() });
        _gpsInterval = setInterval(async () => {
          // Send broadcast packet and keep cloud heartbeat fresh
          await channel.send({
            type: 'broadcast', event: 'gps',
            payload: { lat, lng, ts: Date.now() }
          });
          nk_updateDriverTelemetry(driverId, lat, lng);
        }, 5000);
      }
    });
}

async function nk_stopDriverBroadcast(driverId) {
  if (_gpsInterval) { clearInterval(_gpsInterval); _gpsInterval = null; }
  if (sbClient && driverId) {
    await sbClient.from('driver_telemetry').update({ is_online: false }).eq('driver_id', driverId);
  }
  console.log('📍 GPS Broadcast stopped.');
}

function nk_trackDriverLocation(driverId, onGPS, onStatus) {
  if (!sbClient || !driverId) return;
  const topic = `gps:${driverId}`;
  if (sbClient.getChannels) {
    const existing = sbClient.getChannels().find(c => c.topic === `realtime:${topic}` || c.topic === topic);
    if (existing) {
      try { sbClient.removeChannel(existing); } catch (_) {}
    }
  }
  const channel = sbClient.channel(topic);
  channel
    .on('broadcast', { event: 'gps' }, ({ payload }) => onGPS(payload))
    .on('presence', { event: 'join' },  () => onStatus && onStatus('ONLINE'))
    .on('presence', { event: 'leave' }, () => onStatus && onStatus('OFFLINE'))
    .subscribe();
  return channel;
}

// Controlled telemetry fetch: calls secure RPC get_active_driver_telemetry()
async function nk_fetchOnlineDrivers(limit = 15) {
  if (!sbClient) return [];
  try {
    const { data, error } = await sbClient.rpc('get_active_driver_telemetry');
    if (!error && Array.isArray(data) && data.length > 0) return data;
  } catch (_) {}

  const fiveMinsAgo = new Date(Date.now() - 5 * 60 * 1000).toISOString();
  const { data, error } = await sbClient.from('driver_telemetry')
    .select('driver_id, vehicle_type, vehicle_plate, current_lat, current_lng, heading, speed_kmh, is_online, last_ping')
    .eq('is_online', true)
    .gt('last_ping', fiveMinsAgo)
    .limit(limit);
  if (error) {
    console.warn('Driver telemetry fetch:', error.message);
    return [];
  }
  return data || [];
}

// ─────────────────────────────────────────────────────────────────
// 5. P2P CHAT / PEER MESSAGES
// FIX: receiver_name NOT NULL — now always provided in insert.
// ─────────────────────────────────────────────────────────────────
async function nk_fetchChatHistory(senderEmail, receiverEmail) {
  if (!sbClient) return [];
  const { data, error } = await sbClient.from('peer_messages').select('*')
    .or(`and(sender_email.eq.${senderEmail},receiver_email.eq.${receiverEmail}),and(sender_email.eq.${receiverEmail},receiver_email.eq.${senderEmail})`)
    .order('created_at', { ascending: true });
  if (error) console.warn('Chat history:', error.message);
  return data || [];
}

function nk_subscribeToMessages(myEmail, onMessage) {
  if (!sbClient) return;
  sbClient.channel(`chat:${myEmail}`)
    .on('postgres_changes', {
      event: 'INSERT', schema: 'public', table: 'peer_messages',
      filter: `receiver_email=eq.${myEmail}`
    }, payload => onMessage(payload.new))
    .subscribe();
}

// FIX: receiver_name was missing — added as required parameter
async function nk_sendMessage(senderEmail, receiverEmail, receiverName, text) {
  if (!sbClient) return;
  const { error } = await sbClient.from('peer_messages').insert([{
    sender_email:   senderEmail,
    receiver_email: receiverEmail,
    receiver_name:  receiverName || 'Farmer', // FIX: was missing — caused NOT NULL crash
    message_text:   text
  }]);
  if (error) console.error('Send message error:', error.message);
}

// ─────────────────────────────────────────────────────────────────
// 6. DISEASE SCANS — Sync to `disease_scans` table
// ─────────────────────────────────────────────────────────────────
async function nk_saveDiseaScan(scanRecord) {
  if (!sbClient) return;
  const farmerId = localStorage.getItem('nukrop_farmer_id') || 'NK-87621';
  const { error } = await sbClient.from('disease_scans').insert([{
    farmer_id:         farmerId,
    crop_name:         scanRecord.cropName        || 'Unknown',
    disease_name:      scanRecord.diseaseName     || 'Healthy',
    disease_detected:  scanRecord.diseaseName     || 'Healthy',
    confidence:        scanRecord.confidence      || '90%',
    confidence_score:  parseFloat(scanRecord.confidence) || 90,
    severity:          scanRecord.severity        || 'LOW',
    treatment_chemical: scanRecord.chemical       || '',
    treatment_organic:  scanRecord.organic        || '',
    location:          'Warangal Rural, Telangana',
    latitude:          17.9689,
    longitude:         79.5941
  }]);
  if (error) console.error('Scan save error:', error.message);
  else console.log('✅ Disease scan saved to Supabase.');
}

// ─────────────────────────────────────────────────────────────────
// 7. MANDI RATES (GOVERNMENT OGD / AGMARKNET INTEGRATION)
// ─────────────────────────────────────────────────────────────────
async function nk_fetchMandiRates(state = 'Telangana', limit = 40) {
  if (!sbClient) return [];
  const { data, error } = await sbClient.from('mandi_live_rates')
    .select('id, state, district, market_name, commodity, variety, min_price, max_price, modal_price, trend, trade_date, freshness_status, source_name, market_center_lat, market_center_lng, updated_at')
    .eq('state', state)
    .order('trade_date', { ascending: false })
    .limit(limit);
  if (error) console.warn('Mandi rates fetch:', error.message);
  return data || [];
}

async function nk_fetchNearbyMandis(lat, lng, radiusKm = 100, commodity = null) {
  if (!sbClient) return [];
  const validLat = parseFloat(lat);
  const validLng = parseFloat(lng);
  if (isNaN(validLat) || isNaN(validLng) || validLat < -90 || validLat > 90 || validLng < -180 || validLng > 180) {
    console.warn('Invalid GPS coordinates for nearby mandi resolution:', lat, lng);
    return nk_fetchMandiRates();
  }

  try {
    let query = sbClient.from('mandi_live_rates').select('*');
    if (commodity) query = query.ilike('commodity', `%${commodity}%`);
    const { data, error } = await query.order('trade_date', { ascending: false }).limit(60);
    if (!error && Array.isArray(data) && data.length > 0) {
      const withDistance = data.map(m => {
        const mLat = parseFloat(m.market_center_lat || m.lat || 16.3067);
        const mLng = parseFloat(m.market_center_lng || m.lng || 80.4365);
        const dLat = (mLat - validLat) * Math.PI / 180;
        const dLng = (mLng - validLng) * Math.PI / 180;
        const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                  Math.cos(validLat * Math.PI / 180) * Math.cos(mLat * Math.PI / 180) *
                  Math.sin(dLng/2) * Math.sin(dLng/2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        const distance_km = Math.round(6371 * c * 10) / 10;
        return { ...m, distance_km };
      });
      withDistance.sort((a, b) => a.distance_km - b.distance_km);
      return withDistance;
    }
  } catch (err) {
    console.warn('Direct mandi distance fetch fallback:', err.message);
  }
  return nk_fetchMandiRates();
}

function nk_subscribeToMandiRates(onUpdate) {
  if (!sbClient) return;
  sbClient.channel('realtime:mandi_live_rates')
    .on('postgres_changes', { event: '*', schema: 'public', table: 'mandi_live_rates' },
      payload => onUpdate(payload.new))
    .subscribe();
}


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
