# Dispatch: Worker M3 (Milestone 3 - Interactive Community Features)
Working Directory: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_worker_m3
Original Request: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\ORIGINAL_REQUEST.md
Survey Report: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_explorer_survey_2_gen2\handoff.md
Project Index: c:\Users\bjasw\Downloads\agriculture-ai-os\PROJECT.md

## MANDATORY INTEGRITY WARNING
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Objective: Implement Milestone 3 (R3 - Interactive Community Features)
1. **Supabase Database Migration**:
   - Create `backend/migrations/004_community_interactive.sql`:
     - Add `user_id TEXT` column to `public.community_posts` with index.
     - Create `public.post_likes` (`id`, `post_id`, `user_id`, `created_at`, unique constraint `unique_post_likes`).
     - Create `public.user_follows` (`id`, `follower_id`, `following_id`, `created_at`, unique constraint `unique_user_follows`).
     - Create trigger `trg_post_likes_count` to automatically keep `community_posts.likes_count` synchronized on INSERT/DELETE.
     - Add RLS policies for public access.
     - Sync schema changes into `backend/supabase_setup.sql` and `backend/schema.sql`.
2. **User Identity & State Management**:
   - Implement `getCurrentUserId()` returning a persistent user ID (`nukrop_supabase_uid` / `supabase_user.id` / `nukrop_guest_uid`).
   - Store created posts with `user_id: getCurrentUserId()`.
3. **Follow / Unfollow System**:
   - In `renderCommunityFeedDom()`, render a `[+ Follow]` / `[✓ Following]` button on posts where the author is not current user.
   - Implement `toggleFollowUser(authorId, authorName)`:
     - Toggles follow state, updating local cache (`nukrop_user_follows`).
     - Dispatches `POST` or `DELETE` to `${SUPABASE_CONFIG.url}/rest/v1/user_follows`.
     - Dynamically updates the follow button text/styling and author follower count.
   - In `screens.profile()`: Add Follower, Following, and My Posts metric stats chips, reflecting active follow counts.
4. **Real Post Liking System**:
   - Update `toggleCommunityLike(postId)`:
     - Optimistically updates heart icon (with heart pop animation) and increments/decrements like counter.
     - Dispatches `POST` or `DELETE` to `${SUPABASE_CONFIG.url}/rest/v1/post_likes`.
     - Also updates `community_posts.likes_count` via PostgREST fallback.
     - Persists liked IDs to `localStorage` (`nukrop_community_liked_ids`).
5. **Edit Own Posts**:
   - Ownership check: `const isOwnPost = Boolean(p.user_id && p.user_id === currentUserId) || Boolean(p.author && (p.author.en || p.author) === getCurrentFarmerName());`.
   - If `isOwnPost` is true, render `✏️ Edit` button on the post card.
   - Clicking `Edit` opens an edit modal allowing editing title, description, and crop.
   - Implement `saveEditedCommunityPost(postId, newTitle, newText, newCrop)`:
     - Optimistically updates `COMMUNITY_POSTS_CATALOG` and re-renders feed.
     - Dispatches `PATCH ${SUPABASE_CONFIG.url}/rest/v1/community_posts?id=eq.${postId}&user_id=eq.${currentUserId}`.
6. **Delete Own Posts**:
   - If `isOwnPost` is true, render `🗑️ Delete` button on the post card.
   - Clicking `Delete` prompts for confirmation.
   - Implement `deleteCommunityPost(postId)`:
     - Optimistically removes post from `COMMUNITY_POSTS_CATALOG` and re-renders feed.
     - Dispatches `DELETE ${SUPABASE_CONFIG.url}/rest/v1/community_posts?id=eq.${postId}&user_id=eq.${currentUserId}`.
     - Shows luxury toast notification.
7. **Dual-File Platform Parity**:
   - Maintain 100% parity across `nukrop_emulator.html` and `app/src/main/assets/index.html`.
8. **Automated Verification**:
   - Create `tests/verify_milestone3_community.js` verifying:
     - Liking and unliking updates DB endpoint pattern and UI counter.
     - Following and unfollowing updates `user_follows` endpoint and profile stats.
     - Post ownership check properly displays Edit/Delete buttons only for own posts.
     - Edit post updates title and content in memory and via PATCH.
     - Delete post removes post from feed and via DELETE.
   - Run `node test_production_readiness.js` and ensure all tests pass (0 regressions).
9. **Handoff Report**:
   - Write report to `c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_worker_m3\handoff.md`.
   - Notify parent with test outputs.

## 2026-09-09T09:43:47Z
You are Worker M3 (teamwork_preview_worker).
Your working directory is: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_worker_m3
Read your dispatch at: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_worker_m3\DISPATCH.md
Read the original request at: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\ORIGINAL_REQUEST.md
Read the survey report at: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_explorer_survey_2_gen2\handoff.md
Read the project scope at: c:\Users\bjasw\Downloads\agriculture-ai-os\PROJECT.md

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Your Mission:
Implement Milestone 3: Interactive Community Features (Followers, Following, Real Likes, Edit & Delete Own Posts).
1. Create `backend/migrations/004_community_interactive.sql` adding `community_posts.user_id`, `post_likes`, `user_follows`, triggers, and RLS policies (synced to `backend/supabase_setup.sql` and `backend/schema.sql`).
2. Implement `getCurrentUserId()` and wire new posts with user_id.
3. Implement follow/unfollow system on post cards and update profile followers/following stats counters.
4. Implement real post likes updating `post_likes` and `community_posts.likes_count` with heart animation.
5. Implement edit own post and delete own post with ownership check (`post.user_id === currentUserId`).
6. Maintain 100% parity across `nukrop_emulator.html` and `app/src/main/assets/index.html`.
7. Create and run `tests/verify_milestone3_community.js` and verify `node test_production_readiness.js` passes with 0 regressions.
8. Write your handoff report to `c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_worker_m3\handoff.md` and notify parent.
