# Original User Request

## 2026-08-24T14:54:11Z

# Teamwork Project Prompt — Draft

> Status: Ready for launch — awaiting user approval
> Goal: Craft prompt → get user approval → delegate to teamwork_preview
> Requested team: Use a very large team of agents (App senior maker, alignment checker, bug fixer, and API token checker)

Thoroughly audit and fix the NuKropAI Android app. The team must fix any remaining UI alignment issues, resolve any lingering bugs, and verify that all API tokens and connections (Groq AI, Supabase, Agmarknet) are functioning correctly. Use a very large team of agents.

Working directory: c:\Users\bjasw\Downloads\agriculture-ai-os
Integrity mode: development

## Requirements

### R1. UI Alignment & Polish
Audit all Jetpack Compose screens (Home, Market, Profile, Scanner, Loan, etc.) for text overflow, missing padding, or overlapping elements (especially with the bottom navigation bar) and fix them.

### R2. Bug Squashing
Review the Kotlin codebase for any crashes, infinite loading states, or logical errors and apply fixes.

### R3. API Token & Connection Verification
Test and verify that the Groq AI keys, Supabase DB credentials, and Agmarknet API endpoints are correctly formatted, not rate-limited, and successfully fetching data.

## Acceptance Criteria

### Verification (Agent-as-Judge & Compilation)
- [ ] An independent reviewer agent must read the modified UI code and confirm that proper spacing (e.g., `Spacer` or `padding`) is applied at the bottom of all scrollable lists.
- [ ] An independent reviewer agent must verify that API keys are correctly formatted strings and the network request logic does not contain obvious syntax errors.
- [ ] A test compilation (`./gradlew assembleDebug` or similar script) must pass without syntax errors to prove the codebase remains structurally sound after the fixes.
