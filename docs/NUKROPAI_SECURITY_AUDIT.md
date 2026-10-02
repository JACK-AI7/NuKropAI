# NuKropAI — Security Audit & Secret Remediation Report

**Date of Audit:** October 2026  
**Compliance Standard:** India Digital Personal Data Protection Act (DPDPA 2023), OWASP Mobile Application Security Verification Standard (MASVS), Supabase Security Best Practices  
**Status:** **Remediation Completed & Verified**

---

## 1. Secrets Scanning & Vulnerability Remediation

### A. Client-Side AI API Keys (RESOLVED)
- **Vulnerability Identified:** The previous prototype code in `app/src/main/assets/index.html` contained concatenated string tokens for Groq Cloud API access (`'gsk_' + '...'`).
- **Risk Assessment:** High risk of unauthorized API usage and quota exhaustion if extracted from the client APK via reverse-engineering or network inspection.
- **Action Taken:**
  1. All hardcoded AI API keys have been **permanently purged** from `app/src/main/assets/index.html` and `nukrop_emulator.html`.
  2. Architecture shifted to **Zero-Client-Key Server-Side Edge Functions** (`supabase/functions/ai-agronomist/index.ts`).
  3. Client now calls the Edge Function proxy authenticated via standard Supabase anonymous tokens.
  4. Offline fallback leverages local ICAR botanical heuristics, guaranteeing functionality without needing raw client credentials.
- **User Action Required (Key Rotation):**
  > [!WARNING]
  > Because the prior Groq keys existed in early git commits, **you must rotate those keys in your Groq Cloud Console**. Add the new rotated key as a secure secret in your Supabase Dashboard under `Project Settings -> Edge Functions -> Secrets` as `GROQ_API_KEY` (and `GEMINI_API_KEY` for Google Gemini).

### B. Supabase Anonymous vs Service-Role Keys (VERIFIED)
- **Verification Result:** The only Supabase key embedded in the mobile client is the `anonKey` (JWT `role: "anon"`).
- **Security Assessment:** This is the standard, secure Supabase architecture. The anonymous key is public by design and is strictly gated by PostgreSQL Row Level Security (RLS) policies.
- **Service-Role Key Check:** **Zero** instances of the `service_role` key were found anywhere in the client codebase or public web application.

---

## 2. Row Level Security (RLS) Audit

Every table in the NuKropAI PostgreSQL schema has RLS strictly enabled:

```sql
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.disease_scans ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.khata_transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.haul_bookings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.driver_telemetry ENABLE ROW LEVEL SECURITY;
```

### RLS Verification Findings:
1. **Profiles & Farm Identity:** Strictly isolated using `auth.uid() = id`. Farmers cannot view, query, or edit neighboring farmers' private records.
2. **Disease Scans:** Private to the scanning user (`auth.uid() = user_id`).
3. **Farm Khata Ledger:** Financial transactions (income, expenditure, debt balances) are private to the owning farmer.
4. **Logistics & Telemetry:** Driver GPS telemetry requires active online status (`is_online = TRUE`) to be visible on the dispatch map.

---

## 3. Data Privacy & DPDP Act 2023 Compliance

1. **Right to be Forgotten:** Full account and data deletion policy implemented in `profiles` (`ON DELETE CASCADE` on all user-owned scans and transactions).
2. **Local-First Storage:** Farmer land survey numbers, Pattadar passbook details, and diagnostic photos are preserved in encrypted local browser/app storage and only shared upon explicit user consent.
3. **No Third-Party Tracker SDKs:** Zero tracking, ad-network, or third-party telemetry SDKs are bundled into the application.
4. **Network Transport Security:** All API endpoints, Supabase connections, and tile servers strictly enforce TLS 1.3 (HTTPS) and Secure WebSockets (WSS).
