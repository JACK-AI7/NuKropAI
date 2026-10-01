# apply_supabase_realtime_patch.py
import re
import sys
import os

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

with open('app/src/main/assets/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("Original index.html length:", len(content))

# -------------------------------------------------------------
# 1. Add getCommunityLikedIds & saveCommunityLikedIds before COMMUNITY_POSTS_CATALOG
# -------------------------------------------------------------
target_1 = "let userAttachedMedia = { photos: [], videos: [], voiceNote: null };\n\nlet COMMUNITY_POSTS_CATALOG = ["
replacement_1 = """let userAttachedMedia = { photos: [], videos: [], voiceNote: null };

function getCommunityLikedIds() {
  try {
    const raw = localStorage.getItem('nukrop_community_liked_ids');
    if (raw) return JSON.parse(raw);
  } catch(e) {}
  return [];
}

function saveCommunityLikedIds(ids) {
  try {
    localStorage.setItem('nukrop_community_liked_ids', JSON.stringify(ids));
  } catch(e) {}
}

let COMMUNITY_POSTS_CATALOG = ["""

if target_1 in content:
    content = content.replace(target_1, replacement_1, 1)
    print("[OK] Patched 1: Added getCommunityLikedIds and saveCommunityLikedIds")
else:
    print("Warning: target_1 not found directly, checking variations...")
    idx = content.find("let COMMUNITY_POSTS_CATALOG = [")
    print("idx of COMMUNITY_POSTS_CATALOG:", idx)

# -------------------------------------------------------------
# 2. Add immediate catalog rehydration after COMMUNITY_POSTS_CATALOG array definition
# -------------------------------------------------------------
target_2 = """    isResolved: true,
    comments: []
  }
];

function attachMediaToNewPost(type) {"""

replacement_2 = """    isResolved: true,
    comments: []
  }
];

// Rehydrate community posts and persistent likes from localStorage immediately on startup
(function restoreLocalCommunityPosts() {
  try {
    const raw = localStorage.getItem('nukrop_community_posts');
    const likedIds = getCommunityLikedIds();
    if (raw) {
      const parsed = JSON.parse(raw);
      if (Array.isArray(parsed) && parsed.length > 0) {
        COMMUNITY_POSTS_CATALOG = parsed.map(p => ({
          ...p,
          isLiked: likedIds.includes(p.id),
          likes: likedIds.includes(p.id) ? Math.max(1, p.likes || 1) : (p.likes || 0)
        }));
      }
    }
  } catch(e) {}
})();

function attachMediaToNewPost(type) {"""

if target_2 in content:
    content = content.replace(target_2, replacement_2, 1)
    print("[OK] Patched 2: Added immediate restoreLocalCommunityPosts")
else:
    print("Warning: target_2 not found directly!")

# -------------------------------------------------------------
# 3. Patch toggleCommunityLike & submitCommunityComment
# -------------------------------------------------------------
target_3 = """function toggleCommunityLike(postId) {
  const p = COMMUNITY_POSTS_CATALOG.find(x => x.id === postId);
  if (!p) return;
  p.isLiked = !p.isLiked;
  p.likes += p.isLiked ? 1 : -1;
  try { localStorage.setItem('nukrop_community_posts', JSON.stringify(COMMUNITY_POSTS_CATALOG)); } catch(e) {}
  renderCommunityFeedDom();
}

function toggleCommunityComments(postId) {
  expandedCommunityPostId = expandedCommunityPostId === postId ? null : postId;
  renderCommunityFeedDom();
}

function submitCommunityComment(postId) {
  const inp = document.getElementById('comm-reply-inp-' + postId);
  if (!inp || !inp.value.trim()) return;

  const p = COMMUNITY_POSTS_CATALOG.find(x => x.id === postId);
  if (!p) return;

  const newComment = {
    author: {
      en: ((typeof farmerProfile !== 'undefined' && farmerProfile.name ? (typeof farmerProfile.name === 'object' ? (farmerProfile.name[currentLang] || farmerProfile.name.en) : farmerProfile.name) : 'Farmer') + ' (You)'),
      te: ((typeof farmerProfile !== 'undefined' && farmerProfile.name ? (typeof farmerProfile.name === 'object' ? (farmerProfile.name[currentLang] || farmerProfile.name.en) : farmerProfile.name) : 'రైతు') + ' (మీరు)'),
      hi: ((typeof farmerProfile !== 'undefined' && farmerProfile.name ? (typeof farmerProfile.name === 'object' ? (farmerProfile.name[currentLang] || farmerProfile.name.en) : farmerProfile.name) : 'किसान') + ' (आप)')
    },
    time: 'Just now',
    text: { en: inp.value.trim(), te: inp.value.trim(), hi: inp.value.trim() }
  };

  p.comments.push(newComment);
  inp.value = '';
  try { localStorage.setItem('nukrop_community_posts', JSON.stringify(COMMUNITY_POSTS_CATALOG)); } catch(e) {}
  renderCommunityFeedDom();
  showLuxuryToast(TL('Comment posted successfully!', 'వ్యాఖ్య విజయవంతంగా పోస్ట్ చేయబడింది!', 'टिप्पणी सफलतापूर्वक पोस्ट की गई!'), 'success');
}"""

replacement_3 = """function toggleCommunityLike(postId) {
  const p = COMMUNITY_POSTS_CATALOG.find(x => x.id === postId);
  if (!p) return;

  let likedIds = getCommunityLikedIds();
  const currentlyLiked = likedIds.includes(postId);
  const willBeLiked = !currentlyLiked;

  // 1. Persist liked IDs in dedicated localStorage key
  if (willBeLiked) {
    if (!likedIds.includes(postId)) likedIds.push(postId);
  } else {
    likedIds = likedIds.filter(id => id !== postId);
  }
  saveCommunityLikedIds(likedIds);

  // 2. Optimistic UI update
  p.isLiked = willBeLiked;
  const delta = willBeLiked ? 1 : -1;
  p.likes = Math.max(0, (p.likes || 0) + delta);

  // 3. Save full catalog to localStorage so likes survive reload
  try {
    localStorage.setItem('nukrop_community_posts', JSON.stringify(COMMUNITY_POSTS_CATALOG));
  } catch(e) {}

  renderCommunityFeedDom();

  // 4. Background Cloud Synchronization with Supabase (RPC + REST fallback + community_likes table)
  if (typeof syncCommunityLikeToSupabase === 'function') {
    syncCommunityLikeToSupabase(postId, willBeLiked, delta, p.likes);
  }
}

function toggleCommunityComments(postId) {
  expandedCommunityPostId = expandedCommunityPostId === postId ? null : postId;
  renderCommunityFeedDom();
}

function submitCommunityComment(postId) {
  const inp = document.getElementById('comm-reply-inp-' + postId);
  if (!inp || !inp.value.trim()) return;

  const p = COMMUNITY_POSTS_CATALOG.find(x => x.id === postId);
  if (!p) return;

  const commentText = inp.value.trim();
  const rawFarmerName = (typeof farmerProfile !== 'undefined' && farmerProfile.name ? (typeof farmerProfile.name === 'object' ? (farmerProfile.name[currentLang] || farmerProfile.name.en) : farmerProfile.name) : 'Farmer');

  const newComment = {
    author: {
      en: rawFarmerName + ' (You)',
      te: (typeof farmerProfile !== 'undefined' && farmerProfile.name && typeof farmerProfile.name === 'object' && farmerProfile.name.te ? farmerProfile.name.te : rawFarmerName) + ' (మీరు)',
      hi: (typeof farmerProfile !== 'undefined' && farmerProfile.name && typeof farmerProfile.name === 'object' && farmerProfile.name.hi ? farmerProfile.name.hi : rawFarmerName) + ' (आप)'
    },
    time: 'Just now',
    text: { en: commentText, te: commentText, hi: commentText }
  };

  if (!p.comments) p.comments = [];
  p.comments.push(newComment);
  inp.value = '';

  try { localStorage.setItem('nukrop_community_posts', JSON.stringify(COMMUNITY_POSTS_CATALOG)); } catch(e) {}
  renderCommunityFeedDom();
  showLuxuryToast(TL('Comment posted successfully!', 'వ్యాఖ్య విజయవంతంగా పోస్ట్ చేయబడింది!', 'टिप्पणी सफलतापूर्वक पोस्ट की गई!'), 'success');

  // Push comment to Supabase in real time
  if (typeof pushCommunityCommentToSupabase === 'function') {
    pushCommunityCommentToSupabase(postId, commentText);
  }
}"""

if target_3 in content:
    content = content.replace(target_3, replacement_3, 1)
    print("[OK] Patched 3: toggleCommunityLike & submitCommunityComment upgraded")
else:
    print("Warning: target_3 not found directly!")

# -------------------------------------------------------------
# 4. Patch submitNewCommunityPost to properly register likes & author name
# -------------------------------------------------------------
target_4 = """  userAttachedMedia = { photos: [], videos: [], voiceNote: null, lastMediaUrl: null, lastMediaType: null };
  renderAttachedMediaChips();

  COMMUNITY_POSTS_CATALOG.unshift(newPost);
  pushCommunityPostToSupabase(newPost);
  closeAskQuestionModal();"""

replacement_4 = """  userAttachedMedia = { photos: [], videos: [], voiceNote: null, lastMediaUrl: null, lastMediaType: null };
  renderAttachedMediaChips();

  // Automatically track author's own like
  let likedIds = getCommunityLikedIds();
  if (!likedIds.includes(newPost.id)) likedIds.push(newPost.id);
  saveCommunityLikedIds(likedIds);

  COMMUNITY_POSTS_CATALOG.unshift(newPost);
  try { localStorage.setItem('nukrop_community_posts', JSON.stringify(COMMUNITY_POSTS_CATALOG)); } catch(e) {}

  if (typeof pushCommunityPostToSupabase === 'function') {
    pushCommunityPostToSupabase(newPost);
  }
  closeAskQuestionModal();"""

if target_4 in content:
    content = content.replace(target_4, replacement_4, 1)
    print("[OK] Patched 4: submitNewCommunityPost like registration updated")
else:
    print("Warning: target_4 not found directly!")

# -------------------------------------------------------------
# 5. Patch openMachineryChatModal to tag modal with data-item-id and fetch cloud messages
# -------------------------------------------------------------
target_5 = """  const modalHtml = `
    <div id="machinery-chat-modal" style="position:fixed;inset:0;background:rgba(15,23,42,0.65);backdrop-filter:blur(6px);z-index:999999;display:flex;flex-direction:column;justify-content:flex-end;animation:fadeIn 0.2s ease;">"""

replacement_5 = """  if (typeof fetchMachineryMessagesFromSupabase === 'function') {
    fetchMachineryMessagesFromSupabase(item.id || itemId);
  }

  const modalHtml = `
    <div id="machinery-chat-modal" data-item-id="${item.id || itemId}" style="position:fixed;inset:0;background:rgba(15,23,42,0.65);backdrop-filter:blur(6px);z-index:999999;display:flex;flex-direction:column;justify-content:flex-end;animation:fadeIn 0.2s ease;">"""

if target_5 in content:
    content = content.replace(target_5, replacement_5, 1)
    print("[OK] Patched 5: openMachineryChatModal data-item-id tagged")
else:
    print("Warning: target_5 not found directly!")

# -------------------------------------------------------------
# 6. Patch sendMachineryOwnerMessage to push messages to Supabase machinery_messages
# -------------------------------------------------------------
target_6 = """  // Append user message to stream
  const uBubble = document.createElement('div');
  uBubble.style.cssText = 'align-self:flex-end;max-width:82%;background:#15803D;color:#FFFFFF;border:1.2px solid #15803D;border-radius:16px 16px 4px 16px;padding:10px 14px;box-shadow:0 2px 6px rgba(0,0,0,0.03);';
  uBubble.innerHTML = `<div style="font-size:12.5px;line-height:1.45;font-weight:600;">${msgText}</div><div style="font-size:9.5px;opacity:0.75;text-align:right;margin-top:4px;">${nowTime}</div>`;
  stream.appendChild(uBubble);
  stream.scrollTop = stream.scrollHeight;

  // Automated owner response after 1.2s"""

replacement_6 = """  // Append user message to stream
  const uBubble = document.createElement('div');
  uBubble.style.cssText = 'align-self:flex-end;max-width:82%;background:#15803D;color:#FFFFFF;border:1.2px solid #15803D;border-radius:16px 16px 4px 16px;padding:10px 14px;box-shadow:0 2px 6px rgba(0,0,0,0.03);';
  uBubble.innerHTML = `<div style="font-size:12.5px;line-height:1.45;font-weight:600;">${msgText}</div><div style="font-size:9.5px;opacity:0.75;text-align:right;margin-top:4px;">${nowTime}</div>`;
  stream.appendChild(uBubble);
  stream.scrollTop = stream.scrollHeight;

  // Push user message to Supabase
  const currentFarmerName = (typeof farmerProfile !== 'undefined' && farmerProfile.name ? (typeof farmerProfile.name === 'object' ? (farmerProfile.name[currentLang] || farmerProfile.name.en) : farmerProfile.name) : 'Farmer');
  if (typeof pushMachineryMessageToSupabase === 'function') {
    pushMachineryMessageToSupabase(item.id || itemId, 'user', currentFarmerName, msgText);
  }

  // Automated owner response after 1.2s"""

if target_6 in content:
    content = content.replace(target_6, replacement_6, 1)
    print("[OK] Patched 6: sendMachineryOwnerMessage user message push added")
else:
    print("Warning: target_6 not found directly!")

# Also patch owner response in sendMachineryOwnerMessage
target_6b = """    const rBubble = document.createElement('div');
    rBubble.style.cssText = 'align-self:flex-start;max-width:82%;background:#FFFFFF;color:#0F172A;border:1.2px solid #E2E8F0;border-radius:16px 16px 16px 4px;padding:10px 14px;box-shadow:0 2px 6px rgba(0,0,0,0.03);';
    rBubble.innerHTML = `<div style="font-size:12.5px;line-height:1.45;font-weight:600;">${ownerReplyText}</div><div style="font-size:9.5px;opacity:0.75;text-align:right;margin-top:4px;">${replyMsg.time}</div>`;
    stream.appendChild(rBubble);
    stream.scrollTop = stream.scrollHeight;
  }, 1200);"""

replacement_6b = """    const rBubble = document.createElement('div');
    rBubble.style.cssText = 'align-self:flex-start;max-width:82%;background:#FFFFFF;color:#0F172A;border:1.2px solid #E2E8F0;border-radius:16px 16px 16px 4px;padding:10px 14px;box-shadow:0 2px 6px rgba(0,0,0,0.03);';
    rBubble.innerHTML = `<div style="font-size:12.5px;line-height:1.45;font-weight:600;">${ownerReplyText}</div><div style="font-size:9.5px;opacity:0.75;text-align:right;margin-top:4px;">${replyMsg.time}</div>`;
    stream.appendChild(rBubble);
    stream.scrollTop = stream.scrollHeight;

    // Push owner response to Supabase
    if (typeof pushMachineryMessageToSupabase === 'function') {
      pushMachineryMessageToSupabase(item.id || itemId, 'owner', ownerName, ownerReplyText);
    }
  }, 1200);"""

if target_6b in content:
    content = content.replace(target_6b, replacement_6b, 1)
    print("[OK] Patched 6b: sendMachineryOwnerMessage owner response push added")
else:
    print("Warning: target_6b not found directly!")

# -------------------------------------------------------------
# 7. Patch confirmMachineryBooking to push to Supabase machinery_bookings
# -------------------------------------------------------------
target_7 = """  // Persist booking to localStorage
  try {
    const existingBookings = JSON.parse(localStorage.getItem('nukrop_machinery_bookings') || '[]');
    existingBookings.unshift({
      id: bookingRef,
      machineId: selectedBookingMachine.id,
      name: nameStr,
      total: total,
      date: new Date().toISOString().split('T')[0],
      status: 'DISPATCHED'
    });
    localStorage.setItem('nukrop_machinery_bookings', JSON.stringify(existingBookings));
  } catch(e) {}"""

replacement_7 = """  // Persist booking to localStorage
  try {
    const existingBookings = JSON.parse(localStorage.getItem('nukrop_machinery_bookings') || '[]');
    existingBookings.unshift({
      id: bookingRef,
      machineId: selectedBookingMachine.id,
      name: nameStr,
      total: total,
      date: new Date().toISOString().split('T')[0],
      status: 'DISPATCHED'
    });
    localStorage.setItem('nukrop_machinery_bookings', JSON.stringify(existingBookings));
  } catch(e) {}

  // Push booking to Supabase in real time
  if (typeof pushMachineryBookingToSupabase === 'function') {
    pushMachineryBookingToSupabase({
      bookingRef: bookingRef,
      machineId: selectedBookingMachine.id,
      machineName: nameStr,
      total: total,
      farmerName: (typeof farmerProfile !== 'undefined' && farmerProfile.name ? (typeof farmerProfile.name === 'object' ? (farmerProfile.name[currentLang] || farmerProfile.name.en) : farmerProfile.name) : 'Farmer'),
      farmerPhone: (typeof farmerProfile !== 'undefined' && farmerProfile.phone) || '+91 98492 11048',
      farmerVillage: (typeof farmerProfile !== 'undefined' && farmerProfile.village ? (typeof farmerProfile.village === 'object' ? (farmerProfile.village[currentLang] || farmerProfile.village.en) : farmerProfile.village) : 'Warangal Rural')
    });
  }"""

if target_7 in content:
    content = content.replace(target_7, replacement_7, 1)
    print("[OK] Patched 7: confirmMachineryBooking pushMachineryBookingToSupabase added")
else:
    print("Warning: target_7 not found directly!")

# -------------------------------------------------------------
# 8. Upgrade the entire ENTERPRISE SUPABASE CLOUD SYNC & REAL-TIME CRUD ENGINE v4.0 section
# -------------------------------------------------------------
old_sync_block_start = "  // ========================================================================\n  // ENTERPRISE SUPABASE CLOUD SYNC & REAL-TIME CRUD ENGINE v4.0\n  // ========================================================================"
old_sync_block_end = "  function updateCloudSyncIndicator() {\n    const badge = document.getElementById('cloud-sync-status-badge');\n    if (badge) {\n      badge.innerHTML = '<span style=\"width:6px;height:6px;border-radius:50%;background:#22C55E;display:inline-block;animation:pulseDot 1.5s infinite;\"></span> <span style=\"font-size:10px;font-weight:900;color:#15803D;\">Supabase Live</span>';\n    }\n  }"

start_pos = content.find(old_sync_block_start)
end_pos = content.find(old_sync_block_end)

if start_pos != -1 and end_pos != -1:
    end_pos += len(old_sync_block_end)
    old_block = content[start_pos:end_pos]
    
    new_sync_engine = """  // ========================================================================
  // ENTERPRISE SUPABASE CLOUD SYNC & REAL-TIME CRUD ENGINE v5.0
  // ========================================================================
  let isSupabaseSyncActive = false;
  let supabaseRealtimeWs = null;
  let supabaseRealtimeHeartbeatInterval = null;

  // 1. Fetch Kisan Community Posts & Comments from Supabase (Preserves User Likes & Local Posts)
  async function fetchCommunityPostsFromSupabase() {
    try {
      const res = await fetch(`${SUPABASE_CONFIG.url}/rest/v1/community_posts?select=*,community_comments(*)&order=created_at.desc`, {
        method: 'GET',
        headers: {
          'apikey': SUPABASE_CONFIG.anonKey,
          'Authorization': `Bearer ${SUPABASE_CONFIG.anonKey}`,
          'Accept': 'application/json'
        }
      });
      if (res.ok) {
        const data = await res.json();
        if (Array.isArray(data) && data.length > 0) {
          const likedIds = getCommunityLikedIds();
          
          const remotePosts = data.map(p => {
            const userLiked = likedIds.includes(p.id);
            const remoteLikes = p.likes_count !== undefined ? Number(p.likes_count) : 0;
            // If user previously liked this post, ensure it displays at least 1 like and isLiked: true
            const effectiveLikes = userLiked ? Math.max(1, remoteLikes) : remoteLikes;

            return {
              id: p.id,
              author: { en: p.author_name, te: p.author_name, hi: p.author_name },
              avatarUrl: p.avatar_url || 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80',
              avatar: '👨‍🌾',
              verified: p.is_verified !== false,
              verifiedBadge: 'Verified Progressive Farmer',
              village: { en: p.author_village || 'Warangal', te: p.author_village || 'వరంగల్', hi: p.author_village || 'वारंगल' },
              cropId: p.crop_id || 'cotton',
              cropName: { en: getLocalizedCropName(p.crop_id||'cotton'), te: getLocalizedCropName(p.crop_id||'cotton'), hi: getLocalizedCropName(p.crop_id||'cotton') },
              timeAgo: { en: 'Live on Cloud', te: 'క్లౌడ్ లైవ్', hi: 'क्लाउड लाइव' },
              title: { en: p.title, te: p.title, hi: p.title },
              text: { en: p.content, te: p.content, hi: p.content },
              likes: effectiveLikes,
              isLiked: userLiked,
              photos: p.media_type === 'image' && p.media_url ? [p.media_url] : (Array.isArray(p.photos) ? p.photos : []),
              videos: p.media_type === 'video' && p.media_url ? [p.media_url] : (Array.isArray(p.videos) ? p.videos : []),
              media_url: p.media_url,
              media_type: p.media_type,
              mediaLabel: { en: p.media_label || 'Field Media', te: p.media_label || 'మీడియా', hi: p.media_label || 'मीडिया' },
              isResolved: p.is_resolved || false,
              comments: (p.community_comments || []).map(c => ({
                author: { en: c.author_name, te: c.author_name, hi: c.author_name },
                avatarUrl: c.avatar_url || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80',
                role: c.author_role || 'Progressive Farmer',
                text: { en: c.content, te: c.content, hi: c.content }
              }))
            };
          });

          // Non-destructive merge: preserve local-only pending posts
          const remoteIds = new Set(remotePosts.map(x => x.id));
          const localOnlyPosts = (COMMUNITY_POSTS_CATALOG || []).filter(lp => !remoteIds.has(lp.id));

          COMMUNITY_POSTS_CATALOG = [...localOnlyPosts, ...remotePosts];
          try {
            localStorage.setItem('nukrop_community_posts', JSON.stringify(COMMUNITY_POSTS_CATALOG));
          } catch(e) {}

          console.log(`✅ Loaded & merged ${COMMUNITY_POSTS_CATALOG.length} community posts (Remote: ${remotePosts.length}, Local: ${localOnlyPosts.length})`);
          if (typeof renderCommunityFeedDom === 'function') {
            renderCommunityFeedDom();
          }
        }
      }
    } catch(e) {
      console.warn('Supabase Community sync fallback active:', e.message);
    }
  }

  // 2. Synchronize Community Likes in Supabase (Atomic RPC + REST Fallback + Audit Table)
  async function syncCommunityLikeToSupabase(postId, willBeLiked, delta, newLikesCount) {
    if (typeof SUPABASE_CONFIG === 'undefined' || !SUPABASE_CONFIG.url) return;
    const currentUserId = (typeof farmerProfile !== 'undefined' && farmerProfile.email) || localStorage.getItem('nukrop_user_email') || 'farmer_user_' + (localStorage.getItem('nukrop_device_uuid') || 'default');

    try {
      // Step A: Attempt atomic RPC execution
      let rpcSuccess = false;
      try {
        const rpcRes = await fetch(`${SUPABASE_CONFIG.url}/rest/v1/rpc/increment_post_likes`, {
          method: 'POST',
          headers: {
            'apikey': SUPABASE_CONFIG.anonKey,
            'Authorization': `Bearer ${SUPABASE_CONFIG.anonKey}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ p_post_id: postId, p_delta: delta })
        });
        if (rpcRes.ok) rpcSuccess = true;
      } catch (err) {}

      // Step B: Direct PATCH fallback if RPC not yet created
      if (!rpcSuccess) {
        await fetch(`${SUPABASE_CONFIG.url}/rest/v1/community_posts?id=eq.${encodeURIComponent(postId)}`, {
          method: 'PATCH',
          headers: {
            'apikey': SUPABASE_CONFIG.anonKey,
            'Authorization': `Bearer ${SUPABASE_CONFIG.anonKey}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ likes_count: newLikesCount })
        });
      }

      // Step C: Update community_likes audit table
      if (willBeLiked) {
        await fetch(`${SUPABASE_CONFIG.url}/rest/v1/community_likes`, {
          method: 'POST',
          headers: {
            'apikey': SUPABASE_CONFIG.anonKey,
            'Authorization': `Bearer ${SUPABASE_CONFIG.anonKey}`,
            'Content-Type': 'application/json',
            'Prefer': 'resolution=ignore-duplicates'
          },
          body: JSON.stringify({
            post_id: postId,
            user_id: currentUserId,
            created_at: new Date().toISOString()
          })
        });
      } else {
        await fetch(`${SUPABASE_CONFIG.url}/rest/v1/community_likes?post_id=eq.${encodeURIComponent(postId)}&user_id=eq.${encodeURIComponent(currentUserId)}`, {
          method: 'DELETE',
          headers: {
            'apikey': SUPABASE_CONFIG.anonKey,
            'Authorization': `Bearer ${SUPABASE_CONFIG.anonKey}`
          }
        });
      }
      console.log(`✅ Like synchronized to Supabase cloud! (Post: ${postId}, liked: ${willBeLiked}, count: ${newLikesCount})`);
    } catch(err) {
      console.warn('Supabase like sync background note:', err.message);
    }
  }

  // 3. Push New Community Post to Supabase
  async function pushCommunityPostToSupabase(post) {
    try {
      const authorName = (typeof farmerProfile !== 'undefined' && farmerProfile.name ? (typeof farmerProfile.name === 'object' ? (farmerProfile.name[currentLang] || farmerProfile.name.en) : farmerProfile.name) : 'Farmer');
      const authorVillage = (typeof farmerProfile !== 'undefined' && farmerProfile.village ? (typeof farmerProfile.village === 'object' ? (farmerProfile.village[currentLang] || farmerProfile.village.en) : farmerProfile.village) : 'Warangal Rural');
      const payload = {
        author_name: authorName,
        author_village: authorVillage,
        avatar_url: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80',
        crop_id: post.cropId || 'cotton',
        title: typeof post.title === 'object' ? (post.title[currentLang] || post.title.en) : post.title,
        content: typeof post.text === 'object' ? (post.text[currentLang] || post.text.en) : post.text,
        media_url: post.media_url || null,
        media_type: post.media_type || 'none',
        media_label: post.media_type === 'video' ? '1 Field Video (HD)' : (post.media_type === 'image' ? '1 Field Photo' : 'Discussion'),
        likes_count: 1,
        comments_count: 0,
        is_verified: true,
        is_resolved: false
      };

      const res = await fetch(`${SUPABASE_CONFIG.url}/rest/v1/community_posts`, {
        method: 'POST',
        headers: {
          'apikey': SUPABASE_CONFIG.anonKey,
          'Authorization': `Bearer ${SUPABASE_CONFIG.anonKey}`,
          'Content-Type': 'application/json',
          'Prefer': 'return=representation'
        },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        const createdRows = await res.json();
        if (Array.isArray(createdRows) && createdRows.length > 0) {
          const createdRow = createdRows[0];
          // Replace temp id with Supabase persistent UUID
          const localIdx = COMMUNITY_POSTS_CATALOG.findIndex(p => p.id === post.id);
          if (localIdx >= 0) {
            COMMUNITY_POSTS_CATALOG[localIdx].id = createdRow.id;
            let likedIds = getCommunityLikedIds();
            likedIds = likedIds.filter(id => id !== post.id);
            likedIds.push(createdRow.id);
            saveCommunityLikedIds(likedIds);
            localStorage.setItem('nukrop_community_posts', JSON.stringify(COMMUNITY_POSTS_CATALOG));
          }
        }
        console.log('✅ Community post saved to Supabase cloud!');
        fetchCommunityPostsFromSupabase();
      }
    } catch(e) {
      console.warn('Offline cache for community post:', e.message);
    }
  }

  // 4. Push Comment to Supabase
  async function pushCommunityCommentToSupabase(postId, commentText) {
    try {
      const authorName = (typeof farmerProfile !== 'undefined' && farmerProfile.name ? (typeof farmerProfile.name === 'object' ? (farmerProfile.name[currentLang] || farmerProfile.name.en) : farmerProfile.name) : 'Farmer');
      const res = await fetch(`${SUPABASE_CONFIG.url}/rest/v1/community_comments`, {
        method: 'POST',
        headers: {
          'apikey': SUPABASE_CONFIG.anonKey,
          'Authorization': `Bearer ${SUPABASE_CONFIG.anonKey}`,
          'Content-Type': 'application/json',
          'Prefer': 'return=representation'
        },
        body: JSON.stringify({
          post_id: postId,
          author_name: authorName,
          author_role: 'Progressive Farmer',
          avatar_url: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80',
          content: commentText
        })
      });
      if (res.ok) {
        console.log('✅ Comment written to Supabase cloud!');
        // Update comments_count on community_posts
        const post = COMMUNITY_POSTS_CATALOG.find(x => x.id === postId);
        const commentsCount = (post && post.comments) ? post.comments.length : 1;
        fetch(`${SUPABASE_CONFIG.url}/rest/v1/community_posts?id=eq.${encodeURIComponent(postId)}`, {
          method: 'PATCH',
          headers: {
            'apikey': SUPABASE_CONFIG.anonKey,
            'Authorization': `Bearer ${SUPABASE_CONFIG.anonKey}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ comments_count: commentsCount })
        }).catch(() => {});
      }
    } catch(e) {
      console.warn('Comment sync fallback:', e.message);
    }
  }

  // 5. Machinery Messages & Chat Engine (Farmer ↔ Equipment Owner)
  async function fetchMachineryMessagesFromSupabase(itemId) {
    if (typeof SUPABASE_CONFIG === 'undefined' || !SUPABASE_CONFIG.url) return;
    try {
      const res = await fetch(`${SUPABASE_CONFIG.url}/rest/v1/machinery_messages?item_id=eq.${encodeURIComponent(itemId)}&order=created_at.asc`, {
        headers: {
          'apikey': SUPABASE_CONFIG.anonKey,
          'Authorization': `Bearer ${SUPABASE_CONFIG.anonKey}`,
          'Accept': 'application/json'
        }
      });
      if (res.ok) {
        const data = await res.json();
        if (Array.isArray(data) && data.length > 0) {
          const storageKey = 'nukrop_mach_chat_' + itemId;
          let localHistory = [];
          try { localHistory = JSON.parse(localStorage.getItem(storageKey) || '[]'); } catch(e) {}

          const textSet = new Set(localHistory.map(h => h.text));
          data.forEach(m => {
            if (!textSet.has(m.message_text)) {
              localHistory.push({
                sender: m.sender_type || 'owner',
                time: new Date(m.created_at || Date.now()).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
                text: m.message_text
              });
              textSet.add(m.message_text);
            }
          });

          localStorage.setItem(storageKey, JSON.stringify(localHistory));

          const modal = document.getElementById('machinery-chat-modal');
          if (modal && modal.getAttribute('data-item-id') === String(itemId)) {
            const stream = document.getElementById('mach-chat-stream');
            if (stream) {
              stream.innerHTML = localHistory.map(m => `
                <div style="align-self:${m.sender==='user'?'flex-end':'flex-start'};max-width:82%;background:${m.sender==='user'?'#15803D':'#FFFFFF'};color:${m.sender==='user'?'#FFFFFF':'#0F172A'};border:1.2px solid ${m.sender==='user'?'#15803D':'#E2E8F0'};border-radius:${m.sender==='user'?'16px 16px 4px 16px':'16px 16px 16px 4px'};padding:10px 14px;box-shadow:0 2px 6px rgba(0,0,0,0.03);">
                  <div style="font-size:12.5px;line-height:1.45;font-weight:600;">${m.text}</div>
                  <div style="font-size:9.5px;opacity:0.75;text-align:right;margin-top:4px;">${m.time || 'Now'}</div>
                </div>
              `).join('');
              stream.scrollTop = stream.scrollHeight;
            }
          }
        }
      }
    } catch(e) {
      console.warn('Machinery chat sync fallback:', e.message);
    }
  }

  async function pushMachineryMessageToSupabase(itemId, senderType, senderName, messageText) {
    if (typeof SUPABASE_CONFIG === 'undefined' || !SUPABASE_CONFIG.url) return;
    try {
      await fetch(`${SUPABASE_CONFIG.url}/rest/v1/machinery_messages`, {
        method: 'POST',
        headers: {
          'apikey': SUPABASE_CONFIG.anonKey,
          'Authorization': `Bearer ${SUPABASE_CONFIG.anonKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          item_id: String(itemId),
          sender_type: senderType,
          sender_name: senderName,
          message_text: messageText
        })
      });
      console.log(`✅ Machinery message (${senderType}) pushed to Supabase cloud!`);
    } catch(e) {
      console.warn('Machinery message push fallback:', e.message);
    }
  }

  // 6. Push Machinery Booking to Supabase
  async function pushMachineryBookingToSupabase(booking) {
    if (typeof SUPABASE_CONFIG === 'undefined' || !SUPABASE_CONFIG.url) return;
    try {
      await fetch(`${SUPABASE_CONFIG.url}/rest/v1/machinery_bookings`, {
        method: 'POST',
        headers: {
          'apikey': SUPABASE_CONFIG.anonKey,
          'Authorization': `Bearer ${SUPABASE_CONFIG.anonKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          booking_ref: booking.bookingRef,
          machine_id: String(booking.machineId),
          machine_name: booking.machineName,
          farmer_name: booking.farmerName,
          farmer_phone: booking.farmerPhone,
          farmer_village: booking.farmerVillage,
          acreage: 2.0,
          total_amount: booking.total,
          status: 'DISPATCHED'
        })
      });
      console.log('✅ Machinery booking pushed to Supabase cloud!');
    } catch(e) {
      console.warn('Machinery booking push fallback:', e.message);
    }
  }

  // 7. Fetch Farm Khata Ledger Records from Supabase
  async function fetchKhataFromSupabase() {
    try {
      const res = await fetch(`${SUPABASE_CONFIG.url}/rest/v1/khata_records?select=*&order=record_date.desc`, {
        method: 'GET',
        headers: {
          'apikey': SUPABASE_CONFIG.anonKey,
          'Authorization': `Bearer ${SUPABASE_CONFIG.anonKey}`,
          'Accept': 'application/json'
        }
      });
      if (res.ok) {
        const data = await res.json();
        if (Array.isArray(data) && data.length > 0) {
          console.log(`✅ Loaded ${data.length} Khata records from Supabase!`);
          farmKhataEntries = data.map(r => ({
            id: r.id,
            type: r.type,
            desc: { en: r.title, te: r.title, hi: r.title },
            amount: parseFloat(r.amount),
            date: r.record_date || new Date().toISOString().split('T')[0]
          }));
        }
      }
    } catch(e) {
      console.warn('Supabase Khata offline fallback active:', e.message);
    }
  }

  // 8. Push Farm Khata Record to Supabase
  async function pushKhataToSupabase(entry) {
    try {
      const descText = typeof entry.desc === 'object' ? (entry.desc[currentLang] || entry.desc.en) : entry.desc;
      const res = await fetch(`${SUPABASE_CONFIG.url}/rest/v1/khata_records`, {
        method: 'POST',
        headers: {
          'apikey': SUPABASE_CONFIG.anonKey,
          'Authorization': `Bearer ${SUPABASE_CONFIG.anonKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          crop_id: 'cotton',
          type: entry.type || 'expense',
          category: entry.category || 'general',
          title: descText,
          amount: entry.amount,
          record_date: entry.date || new Date().toISOString().split('T')[0]
        })
      });
      if (res.ok) console.log('✅ Khata record saved to Supabase!');
    } catch(e) {
      console.warn('Khata sync fallback:', e.message);
    }
  }

  // 9. Push GramHaul Truck Booking to Supabase
  async function pushTruckBookingToSupabase(booking) {
    try {
      const res = await fetch(`${SUPABASE_CONFIG.url}/rest/v1/truck_bookings`, {
        method: 'POST',
        headers: {
          'apikey': SUPABASE_CONFIG.anonKey,
          'Authorization': `Bearer ${SUPABASE_CONFIG.anonKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          driver_name: booking.driverName || 'Verified Driver',
          driver_phone: booking.driverPhone || '+91 98480 22338',
          vehicle: booking.vehicle || 'Tata Ace (1.5 Ton)',
          from_loc: booking.from || 'Warangal Rural',
          to_mandi: booking.destination || 'Warangal APMC Yard',
          crop_name: booking.crop || 'Cotton',
          quantity_qtl: (booking.bags || 15) * 0.5,
          total_cost: booking.totalCost || 675,
          status: 'confirmed'
        })
      });
      if (res.ok) console.log('✅ Truck booking saved to Supabase!');
    } catch(e) {
      console.warn('Truck booking offline fallback:', e.message);
    }
  }

  // 10. Supabase Realtime WebSocket Connection & Listener
  function initSupabaseRealtime() {
    if (typeof SUPABASE_CONFIG === 'undefined' || !SUPABASE_CONFIG.url) return;
    const projectRef = SUPABASE_CONFIG.url.replace('https://', '').replace('.supabase.co', '');
    const wsUrl = `wss://${projectRef}.supabase.co/realtime/v1/websocket?apikey=${SUPABASE_CONFIG.anonKey}&vsn=1.0.0`;

    try {
      if (supabaseRealtimeWs) {
        try { supabaseRealtimeWs.close(); } catch(e) {}
      }

      supabaseRealtimeWs = new WebSocket(wsUrl);

      supabaseRealtimeWs.onopen = function() {
        console.log('⚡ Supabase Realtime WebSocket Connected!');
        updateCloudSyncIndicator(true);

        // Subscribe to community_posts changes
        supabaseRealtimeWs.send(JSON.stringify({
          topic: 'realtime:public:community_posts',
          event: 'phx_join',
          payload: {
            config: {
              broadcast: { self: true },
              postgres_changes: [{ event: '*', schema: 'public', table: 'community_posts' }]
            }
          },
          ref: 'posts-sub-1'
        }));

        // Subscribe to community_comments changes
        supabaseRealtimeWs.send(JSON.stringify({
          topic: 'realtime:public:community_comments',
          event: 'phx_join',
          payload: {
            config: {
              broadcast: { self: true },
              postgres_changes: [{ event: '*', schema: 'public', table: 'community_comments' }]
            }
          },
          ref: 'comments-sub-1'
        }));

        // Subscribe to machinery_messages changes
        supabaseRealtimeWs.send(JSON.stringify({
          topic: 'realtime:public:machinery_messages',
          event: 'phx_join',
          payload: {
            config: {
              broadcast: { self: true },
              postgres_changes: [{ event: '*', schema: 'public', table: 'machinery_messages' }]
            }
          },
          ref: 'mach-sub-1'
        }));

        // Maintain WebSocket heartbeat every 25 seconds
        if (supabaseRealtimeHeartbeatInterval) clearInterval(supabaseRealtimeHeartbeatInterval);
        supabaseRealtimeHeartbeatInterval = setInterval(() => {
          if (supabaseRealtimeWs && supabaseRealtimeWs.readyState === WebSocket.OPEN) {
            supabaseRealtimeWs.send(JSON.stringify({
              topic: 'phoenix',
              event: 'heartbeat',
              payload: {},
              ref: 'hb-' + Date.now()
            }));
          }
        }, 25000);
      };

      supabaseRealtimeWs.onmessage = function(event) {
        try {
          const msg = JSON.parse(event.data);
          if (msg.event === 'postgres_changes') {
            const payload = msg.payload || {};
            const table = payload.data ? payload.data.table : (payload.table || '');
            const record = payload.data ? (payload.data.record || payload.data.new) : (payload.record || payload.new);

            if (table === 'community_posts' || table === 'community_comments') {
              console.log('⚡ Realtime Community update received:', table);
              fetchCommunityPostsFromSupabase();
            } else if (table === 'machinery_messages' && record) {
              const modal = document.getElementById('machinery-chat-modal');
              if (modal && modal.getAttribute('data-item-id') === String(record.item_id) && record.sender_type !== 'user') {
                const stream = document.getElementById('mach-chat-stream');
                if (stream) {
                  const bubble = document.createElement('div');
                  bubble.style.cssText = 'align-self:flex-start;max-width:82%;background:#FFFFFF;color:#0F172A;border:1.2px solid #E2E8F0;border-radius:16px 16px 16px 4px;padding:10px 14px;box-shadow:0 2px 6px rgba(0,0,0,0.03);';
                  bubble.innerHTML = `<div style="font-size:12.5px;line-height:1.45;font-weight:600;">${record.message_text}</div><div style="font-size:9.5px;opacity:0.75;text-align:right;margin-top:4px;">${new Date(record.created_at || Date.now()).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</div>`;
                  stream.appendChild(bubble);
                  stream.scrollTop = stream.scrollHeight;
                }
              }
            }
          }
        } catch(err) {}
      };

      supabaseRealtimeWs.onclose = function() {
        console.log('🔌 Supabase Realtime disconnected. Reconnecting in 8s...');
        if (supabaseRealtimeHeartbeatInterval) clearInterval(supabaseRealtimeHeartbeatInterval);
        setTimeout(initSupabaseRealtime, 8000);
      };

      supabaseRealtimeWs.onerror = function() {};
    } catch (e) {
      console.warn('Supabase Realtime setup note:', e.message);
    }
  }

  // 11. Master Synchronize All Supabase Services
  async function syncAllSupabaseData() {
    await Promise.allSettled([
      fetchMandiRatesFromSupabase(),
      fetchEquipmentFromSupabase(),
      fetchCommunityPostsFromSupabase(),
      fetchKhataFromSupabase()
    ]);
    isSupabaseSyncActive = true;
    updateCloudSyncIndicator();
  }

  function updateCloudSyncIndicator(isLive) {
    const badge = document.getElementById('cloud-sync-status-badge');
    if (badge) {
      badge.innerHTML = '<span style="width:6px;height:6px;border-radius:50%;background:#22C55E;display:inline-block;animation:pulseDot 1.5s infinite;"></span> <span style="font-size:10px;font-weight:900;color:#15803D;">Supabase Live</span>';
    }
  }"""

    content = content[:start_pos] + new_sync_engine + content[end_pos:]
    print("[OK] Patched 8: Replaced enterprise Supabase sync engine v5.0")
else:
    print(f"Warning: sync engine block positions: start={start_pos}, end={end_pos}")

# -------------------------------------------------------------
# 9. In bootApp(), ensure syncAllSupabaseData() and initSupabaseRealtime() are called
# -------------------------------------------------------------
target_9 = """function bootApp() {
  if (appBooted) return;
  appBooted = true;

  // 1. Restore user session and active crops if returning user
  restoreUserSession();

  // 2. Pre-render the home screen in the background so it is instantly mounted underneath
  openScreen('home', document.getElementById('tab-home'));

  // 3. Fetch real location and live weather in background
  fetchRealLocationAndWeather();

  // 4. Initialize startup experience (splash 3.8s, then smoothly transition into home or onboarding)
  initStartupExperience();
}"""

replacement_9 = """function bootApp() {
  if (appBooted) return;
  appBooted = true;

  // 1. Restore user session and active crops if returning user
  restoreUserSession();

  // 2. Pre-render the home screen in the background so it is instantly mounted underneath
  openScreen('home', document.getElementById('tab-home'));

  // 3. Fetch real location and live weather in background
  fetchRealLocationAndWeather();

  // 4. Trigger Realtime Supabase Data Sync & WebSocket connection
  try {
    syncAllSupabaseData();
    initSupabaseRealtime();
    // Background polling watchdog every 12 seconds
    setInterval(() => {
      const commView = document.getElementById('view-community');
      if (commView && commView.classList.contains('active-screen')) {
        fetchCommunityPostsFromSupabase();
      }
    }, 12000);
  } catch(e) {}

  // 5. Initialize startup experience (splash 3.8s, then smoothly transition into home or onboarding)
  initStartupExperience();
}"""

if target_9 in content:
    content = content.replace(target_9, replacement_9, 1)
    print("[OK] Patched 9: bootApp now launches syncAllSupabaseData & initSupabaseRealtime")
else:
    print("Warning: target_9 not found directly!")

# Write to app/src/main/assets/index.html
with open('app/src/main/assets/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Copy 100% byte-for-byte identical to nukrop_emulator.html
with open('nukrop_emulator.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"[SUCCESS] Successfully wrote updated content! New length: {len(content)}")
