# Dispatch: survey_explorer_2 (R2 - Dynamic Pest Alerts & R3 - Community Features)
Target Directory: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_explorer_survey_2
Original Request: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\ORIGINAL_REQUEST.md
Dispatch Instructions: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_orchestrator_5\DISPATCH.md

## Mission
Investigate R2 (Pest & Disease Alerts) and R3 (Interactive Community) in the codebase:
1. Locate where Pest & Disease Alerts are implemented (e.g. in nukrop_emulator.html, JS, API services). Search for hardcoded fallbacks like "Warangal" or static district/state strings.
2. Determine how the user's detected state/location is obtained (e.g., GPS, IP geolocation, user profile state, localStorage, or state selector) and how alerts are fetched/filtered dynamically without hardcoded fallback values.
3. Investigate the Kisan Community section (in nukrop_emulator.html and Supabase):
   - Current community posts rendering, like buttons, follower/following counts, profile view, edit/delete actions.
   - Supabase tables for posts, likes/post_likes, follows/followers, user profile.
   - Check if tables exist or if SQL migrations are needed.
   - Verify how editing and deleting own posts is handled (ownership check via auth user ID).
   - Verify how follow/unfollow and liking/unliking are hooked to Supabase and update UI counts.
4. Produce a comprehensive report in `c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_explorer_survey_2\handoff.md`.

## 2026-09-09T06:13:15Z
You are survey_explorer_2.
Your working directory is: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_explorer_survey_2
Read your dispatch at: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_explorer_survey_2\DISPATCH.md
Read the original request at: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\ORIGINAL_REQUEST.md

Your mission:
Investigate R2 (Dynamic Pest and Disease Alerts) and R3 (Interactive Community Features).
1. Locate where Pest & Disease Alerts are implemented in the codebase. Search for hardcoded fallbacks like "Warangal" or static district/state strings. Determine how user location/state is detected and how alerts can be fetched/filtered dynamically.
2. Investigate the Community tab in nukrop_emulator.html and Supabase:
   - Followers/following system (Supabase table, counts, UI state, follow/unfollow actions).
   - Real post likes (Supabase table, toggle like, like counts).
   - Edit and delete own posts (ownership check, Supabase update/delete, UI update).
3. Check existing Supabase schema and tables for posts, likes, followers.
4. Write your comprehensive analysis and recommendations to c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_explorer_survey_2\handoff.md.
When finished, send a message to parent notifying completion with the path to handoff.md.
