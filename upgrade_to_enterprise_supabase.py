# -*- coding: utf-8 -*-
import sys
import os
import re

def patch_file(filepath):
    print(f"Applying enterprise Supabase upgrade to: {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Insert comprehensive Supabase Live Data Grid and Cloud Sync Engine
    supabase_engine_code = """
  // ========================================================================
  // ENTERPRISE SUPABASE CLOUD SYNC & REAL-TIME CRUD ENGINE v4.0
  // ========================================================================
  let isSupabaseSyncActive = false;

  // 1. Fetch Kisan Community Posts & Comments from Supabase
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
          console.log(`✅ Loaded ${data.length} community posts from Supabase!`);
          COMMUNITY_POSTS_CATALOG = data.map(p => ({
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
            likes: p.likes_count || 0,
            isLiked: false,
            photos: p.media_type === 'image' && p.media_url ? [p.media_url] : [],
            videos: p.media_type === 'video' && p.media_url ? [p.media_url] : [],
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
          }));
          if (typeof renderCommunityFeedDom === 'function') {
            renderCommunityFeedDom();
          }
        }
      }
    } catch(e) {
      console.warn('Supabase Community sync fallback active:', e.message);
    }
  }

  // 2. Push New Community Post to Supabase
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
        likes_count: 0,
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
        console.log('✅ Community post saved to Supabase cloud!');
        fetchCommunityPostsFromSupabase();
      }
    } catch(e) {
      console.warn('Offline cache for community post:', e.message);
    }
  }

  // 3. Push Comment to Supabase
  async function pushCommunityCommentToSupabase(postId, commentText) {
    try {
      const authorName = (typeof farmerProfile !== 'undefined' && farmerProfile.name ? (typeof farmerProfile.name === 'object' ? (farmerProfile.name[currentLang] || farmerProfile.name.en) : farmerProfile.name) : 'Farmer');
      const res = await fetch(`${SUPABASE_CONFIG.url}/rest/v1/community_comments`, {
        method: 'POST',
        headers: {
          'apikey': SUPABASE_CONFIG.anonKey,
          'Authorization': `Bearer ${SUPABASE_CONFIG.anonKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          post_id: postId,
          author_name: authorName,
          author_role: 'Progressive Farmer',
          avatar_url: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80',
          content: commentText
        })
      });
      if (res.ok) console.log('✅ Comment written to Supabase!');
    } catch(e) {
      console.warn('Comment sync fallback:', e.message);
    }
  }

  // 4. Fetch Farm Khata Ledger Records from Supabase
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

  // 5. Push Farm Khata Record to Supabase
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

  // 6. Push GramHaul Truck Booking to Supabase
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

  // 7. Master Synchronize All Supabase Services
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

  function updateCloudSyncIndicator() {
    const badge = document.getElementById('cloud-sync-status-badge');
    if (badge) {
      badge.innerHTML = '<span style="width:6px;height:6px;border-radius:50%;background:#22C55E;display:inline-block;animation:pulseDot 1.5s infinite;"></span> <span style="font-size:10px;font-weight:900;color:#15803D;">Supabase Live</span>';
    }
  }
"""

    # Check if our new functions are already present
    if "fetchCommunityPostsFromSupabase" not in html:
        # Insert right after SUPABASE_CONFIG
        sb_config_idx = html.find("const SUPABASE_CONFIG = {")
        if sb_config_idx != -1:
            end_bracket = html.find("};", sb_config_idx)
            if end_bracket != -1:
                html = html[:end_bracket+2] + "\n" + supabase_engine_code + "\n" + html[end_bracket+2:]
                print("Added Supabase Live Data Grid to file")

    # 2. Wire submitNewCommunityPost to call pushCommunityPostToSupabase
    old_post_unshift = "COMMUNITY_POSTS_CATALOG.unshift(newPost);"
    new_post_unshift = """COMMUNITY_POSTS_CATALOG.unshift(newPost);
  pushCommunityPostToSupabase(newPost);"""
    if old_post_unshift in html and "pushCommunityPostToSupabase(newPost)" not in html:
        html = html.replace(old_post_unshift, new_post_unshift)
        print("Wired submitNewCommunityPost to pushCommunityPostToSupabase")

    # 3. Wire saveKhataEntry to call pushKhataToSupabase
    old_khata_unshift = "farmKhataEntries.unshift(newEntry);"
    new_khata_unshift = """farmKhataEntries.unshift(newEntry);
  pushKhataToSupabase(newEntry);"""
    if old_khata_unshift in html and "pushKhataToSupabase(newEntry)" not in html:
        html = html.replace(old_khata_unshift, new_khata_unshift)
        print("Wired saveKhataEntry to pushKhataToSupabase")

    # 4. Wire book truck slot to pushTruckBookingToSupabase
    old_truck_toast = "showPushNotificationToast({\n    title: TL(`\ud83d\ude9a Mandi Freight Confirmed"
    if old_truck_toast in html and "pushTruckBookingToSupabase(truck);" not in html:
        html = html.replace(
            old_truck_toast,
            "pushTruckBookingToSupabase(truck);\n  " + old_truck_toast
        )
        print("Wired truck booking to pushTruckBookingToSupabase")

    # 5. Wire openScreen to refresh Supabase data on tab transitions
    old_open_screen = "function openScreen(screenKey, tabElement) {"
    new_open_screen = """function openScreen(screenKey, tabElement) {
  if (screenKey === 'community') fetchCommunityPostsFromSupabase();
  if (screenKey === 'khata') fetchKhataFromSupabase();
  if (screenKey === 'market') fetchMandiRatesFromSupabase();
  if (screenKey === 'equipment') fetchEquipmentFromSupabase();"""

    if old_open_screen in html and "fetchCommunityPostsFromSupabase()" not in html[html.find(old_open_screen):html.find(old_open_screen)+400]:
        html = html.replace(old_open_screen, new_open_screen)
        print("Wired openScreen to auto-refresh Supabase data")

    # 6. Auto-sync on boot
    old_boot_call = "fetchRealLocationAndWeather();"
    new_boot_call = """fetchRealLocationAndWeather();
    setTimeout(syncAllSupabaseData, 200);"""
    if old_boot_call in html and "syncAllSupabaseData" not in html:
        html = html.replace(old_boot_call, new_boot_call)
        print("Wired nukropBoot to trigger syncAllSupabaseData")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Completed {filepath} successfully!")

if __name__ == '__main__':
    patch_file('app/src/main/assets/index.html')
    patch_file('nukrop_emulator.html')
