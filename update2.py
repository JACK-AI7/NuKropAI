import re

with open('nukrop_emulator.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add fetchCommunityPostsFromSupabase and saveCommunityPostToSupabase right after fetchMandiRatesFromSupabase block
supabase_community_funcs = """

// 2b. Fetch Community Posts from Supabase
async function fetchCommunityPostsFromSupabase() {
  try {
    const res = await fetch(`${SUPABASE_CONFIG.url}/rest/v1/community_posts?select=*&order=created_at.desc`, {
      method: 'GET',
      headers: {
        'apikey': SUPABASE_CONFIG.anonKey,
        'Authorization': `Bearer ${SUPABASE_CONFIG.anonKey}`,
        'Accept': 'application/json'
      }
    });
    if (!res.ok) throw new Error('Supabase HTTP ' + res.status);
    const data = await res.json();
    if (Array.isArray(data) && data.length > 0) {
      console.log(`✅ Fetched ${data.length} real Community posts from Supabase!`);
      
      COMMUNITY_POSTS_CATALOG = data.map(r => ({
        id: r.id,
        author: { en: r.author_name || 'Farmer', te: r.author_name || 'రైతు', hi: r.author_name || 'किसान' },
        avatar: '👨‍🌾',
        cropId: r.crop_id || 'cotton',
        cropName: { en: r.crop_id, te: r.crop_id, hi: r.crop_id },
        timeAgo: { en: 'Recently', te: 'ఇటీవల', hi: 'हाल ही में' },
        title: { en: r.title, te: r.title, hi: r.title },
        text: { en: r.body, te: r.body, hi: r.body },
        likes: r.likes || 0,
        isLiked: false,
        comments: []
      }));
      renderCommunityFeedDom();
    }
  } catch (err) {
    console.warn('Supabase Community fetch offline/table missing:', err.message);
  }
}

async function saveCommunityPostToSupabase(post) {
  try {
    const payload = {
      id: post.id,
      author_name: post.author.en,
      crop_id: post.cropId,
      title: post.title.en,
      body: post.text.en,
      likes: post.likes
    };
    const res = await fetch(`${SUPABASE_CONFIG.url}/rest/v1/community_posts`, {
      method: 'POST',
      headers: {
        'apikey': SUPABASE_CONFIG.anonKey,
        'Authorization': `Bearer ${SUPABASE_CONFIG.anonKey}`,
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal'
      },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error('Failed to post to Supabase');
    console.log('✅ Community post saved to Supabase');
  } catch (err) {
    console.error('Supabase save post error (table may not exist):', err);
  }
}
"""

content = content.replace("async function fetchEquipmentFromSupabase() {", supabase_community_funcs + "\\nasync function fetchEquipmentFromSupabase() {")

# Call fetchCommunityPostsFromSupabase alongside others
content = content.replace("fetchEquipmentFromSupabase();", "fetchEquipmentFromSupabase();\\n  fetchCommunityPostsFromSupabase();")

# Update the submission logic in closeAskQuestionModal (but it's actually in submitQuestion or openScreen? Wait, let's look for "COMMUNITY_POSTS_CATALOG.unshift(newPost);")
submit_replacement = """
  COMMUNITY_POSTS_CATALOG.unshift(newPost);
  saveCommunityPostToSupabase(newPost); // Push to production Supabase database
"""
content = content.replace("COMMUNITY_POSTS_CATALOG.unshift(newPost);", submit_replacement)

with open('nukrop_emulator.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated HTML for Community Supabase')
