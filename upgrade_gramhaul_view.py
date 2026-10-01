import sys, re

sys.stdout.reconfigure(encoding='utf-8')

new_gramhaul_view = '''gramhaul: () => {
    const t = I18N[currentLang] || I18N.en;
    const isTe = currentLang === 'te';
    const isHi = currentLang === 'hi';

    return `
    <!-- GramHaul Luxury Obsidian Dark Logistics Experience (Image 4 Style) -->
    <div style="background:#0A0E17;min-height:100%;color:#FFFFFF;display:flex;flex-direction:column;box-sizing:border-box;">
      
      <!-- Top Navigation & Pickup/Drop HUD -->
      <div style="padding:16px 16px 12px;background:linear-gradient(180deg, rgba(10,14,23,0.98) 0%, rgba(10,14,23,0.8) 100%);backdrop-filter:blur(10px);position:sticky;top:0;z-index:20;">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
          <div style="display:flex;align-items:center;gap:10px;">
            <button onclick="openScreen('home',null);syncSideNav('btn-home')" style="width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.15);color:#FFFFFF;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:16px;">
              ←
            </button>
            <div>
              <div style="font-size:15px;font-weight:900;color:#FFFFFF;letter-spacing:-0.3px;">GramHaul Logistics</div>
              <div style="font-size:10px;color:#22C55E;font-weight:700;">● Live GPS Telemetry Active</div>
            </div>
          </div>
          <div style="width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg, #22C55E, #16A34A);display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:900;box-shadow:0 0 12px rgba(34,197,94,0.4);">
            👨‍🌾
          </div>
        </div>

        <!-- Pickup / Drop Route Card -->
        <div style="background:#151C28;border:1px solid rgba(255,255,255,0.08);border-radius:18px;padding:12px;display:flex;flex-direction:column;gap:10px;box-shadow:0 8px 24px rgba(0,0,0,0.4);">
          <!-- Pickup Row -->
          <div style="display:flex;align-items:center;gap:10px;">
            <div style="width:20px;height:20px;border-radius:50%;background:rgba(255,255,255,0.15);display:flex;align-items:center;justify-content:center;font-size:11px;">📍</div>
            <div style="flex:1;min-width:0;">
              <div style="font-size:9.5px;color:#94A3B8;font-weight:700;text-transform:uppercase;">Pickup Location</div>
              <div style="font-size:12px;font-weight:800;color:#FFFFFF;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">Plot 4B, Jaswanth Farm, Warangal Rural</div>
            </div>
          </div>

          <!-- Divider with exchange icon -->
          <div style="display:flex;align-items:center;gap:10px;padding-left:9px;">
            <div style="width:2px;height:12px;background:#22C55E;border-radius:1px;"></div>
            <div style="flex:1;height:1px;background:rgba(255,255,255,0.06);"></div>
            <span style="font-size:11px;color:#64748B;cursor:pointer;">⇅</span>
          </div>

          <!-- Drop Row -->
          <div style="display:flex;align-items:center;gap:10px;">
            <div style="width:20px;height:20px;border-radius:50%;background:rgba(34,197,94,0.2);display:flex;align-items:center;justify-content:center;font-size:11px;color:#22C55E;">🎯</div>
            <div style="flex:1;min-width:0;">
              <div style="font-size:9.5px;color:#94A3B8;font-weight:700;text-transform:uppercase;">Destination Mandi</div>
              <div style="font-size:12px;font-weight:800;color:#22C55E;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">Enumamula APMC Grain Market (4.8 km)</div>
            </div>
          </div>
        </div>

        <!-- Quick Destination Chips -->
        <div style="display:flex;gap:8px;margin-top:10px;overflow-x:auto;padding-bottom:2px;">
          <div style="background:#1A2333;border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:6px 12px;font-size:10.5px;font-weight:700;display:flex;align-items:center;gap:6px;flex-shrink:0;cursor:pointer;">
            <span>🏡</span> <span>Home Farm (12 min)</span>
          </div>
          <div style="background:#1A2333;border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:6px 12px;font-size:10.5px;font-weight:700;display:flex;align-items:center;gap:6px;flex-shrink:0;cursor:pointer;">
            <span>🏢</span> <span>APMC Yard (28 min)</span>
          </div>
          <div style="background:#1A2333;border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:6px 12px;font-size:10.5px;font-weight:700;display:flex;align-items:center;gap:6px;flex-shrink:0;cursor:pointer;">
            <span>❄️</span> <span>Cold Storage (45 min)</span>
          </div>
        </div>
      </div>

      <!-- Live Interactive Neon GPS Map Vector Canvas -->
      <div style="position:relative;height:240px;background:#06090F;margin:0 16px;border-radius:22px;overflow:hidden;border:1px solid rgba(34,197,94,0.2);box-shadow:inset 0 0 40px rgba(0,0,0,0.8), 0 8px 30px rgba(0,0,0,0.6);">
        
        <!-- Ambient Grid Background -->
        <div style="position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);background-size:24px 24px;"></div>
        
        <!-- Glowing SVG Laser GPS Route -->
        <svg style="position:absolute;inset:0;width:100%;height:100%;">
          <defs>
            <filter id="neonGlow" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="4" result="blur"/>
              <feMerge>
                <feMergeNode in="blur"/>
                <feMergeNode in="SourceGraphic"/>
              </feMerge>
            </filter>
          </defs>
          <!-- Neon Laser Path -->
          <path d="M 40 50 L 110 50 L 110 130 L 220 130 L 220 190" fill="none" stroke="#22C55E" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round" filter="url(#neonGlow)"/>
          <path d="M 40 50 L 110 50 L 110 130 L 220 130 L 220 190" fill="none" stroke="#FFFFFF" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="6, 6"/>
          
          <!-- Farm Origin Radar Pin -->
          <circle cx="40" cy="50" r="10" fill="#22C55E" opacity="0.25"/>
          <circle cx="40" cy="50" r="5" fill="#22C55E"/>
          
          <!-- Destination Mandi Pin -->
          <circle cx="220" cy="190" r="10" fill="#22C55E" opacity="0.25"/>
          <circle cx="220" cy="190" r="5" fill="#22C55E"/>
          
          <!-- Moving Truck Indicator -->
          <g transform="translate(145, 120)">
            <rect x="-12" y="-8" width="24" height="16" rx="4" fill="#FFFFFF" stroke="#22C55E" stroke-width="2"/>
            <text x="-6" y="4" font-size="10" fill="#0A0E17">🚚</text>
          </g>
        </svg>

        <!-- Live Status Pill in Map -->
        <div style="position:absolute;top:12px;left:12px;background:rgba(10,14,23,0.85);backdrop-filter:blur(8px);border:1px solid rgba(34,197,94,0.3);border-radius:14px;padding:4px 10px;display:flex;align-items:center;gap:6px;">
          <span style="width:6px;height:6px;background:#22C55E;border-radius:50%;box-shadow:0 0 8px #22C55E;"></span>
          <span style="font-size:10px;font-weight:800;color:#22C55E;">Truck in Transit · 2 min away</span>
        </div>

        <!-- Recenter Map FAB -->
        <button onclick="refreshGramhaulLocation()" style="position:absolute;bottom:12px;right:12px;width:34px;height:34px;border-radius:50%;background:#151C28;border:1px solid rgba(255,255,255,0.15);color:#FFFFFF;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(0,0,0,0.5);">
          🎯
        </button>
      </div>

      <!-- Tiered Vehicle Selection & Driver Cockpit Tracker Sheet -->
      <div style="padding:16px 16px 80px;display:flex;flex-direction:column;gap:12px;">
        
        <div style="font-size:13px;font-weight:900;color:#FFFFFF;letter-spacing:-0.2px;margin-bottom:-4px;">
          Choose Vehicle Option
        </div>

        <!-- Option 1: Standard (Selected) -->
        <div onclick="selectGramhaulVehicleTier('standard')" id="tier-standard" style="background:#151C28;border:2px solid #22C55E;border-radius:18px;padding:12px 14px;display:flex;align-items:center;gap:12px;cursor:pointer;box-shadow:0 4px 16px rgba(34,197,94,0.15);transition:all 0.2s ease;">
          <div style="width:46px;height:46px;border-radius:14px;background:#1F293D;display:flex;align-items:center;justify-content:center;font-size:24px;flex-shrink:0;">
            🛻
          </div>
          <div style="flex:1;min-width:0;">
            <div style="display:flex;align-items:center;justify-content:space-between;">
              <span style="font-size:13.5px;font-weight:900;color:#FFFFFF;">Standard (Tata Ace)</span>
              <span style="font-size:14px;font-weight:900;color:#22C55E;">₹850</span>
            </div>
            <div style="font-size:10.5px;color:#94A3B8;margin-top:2px;">
              1.5 Ton Capacity · 4 min away · Fast Farm Pickup
            </div>
          </div>
        </div>

        <!-- Option 2: Comfort (Bolero Pickup) -->
        <div onclick="selectGramhaulVehicleTier('comfort')" id="tier-comfort" style="background:#111722;border:1px solid rgba(255,255,255,0.08);border-radius:18px;padding:12px 14px;display:flex;align-items:center;gap:12px;cursor:pointer;transition:all 0.2s ease;">
          <div style="width:46px;height:46px;border-radius:14px;background:#1F293D;display:flex;align-items:center;justify-content:center;font-size:24px;flex-shrink:0;">
            🚚
          </div>
          <div style="flex:1;min-width:0;">
            <div style="display:flex;align-items:center;justify-content:space-between;">
              <span style="font-size:13.5px;font-weight:900;color:#FFFFFF;">Comfort (Bolero Pickup)</span>
              <span style="font-size:14px;font-weight:900;color:#FFFFFF;">₹1,420</span>
            </div>
            <div style="font-size:10.5px;color:#94A3B8;margin-top:2px;">
              2.5 Ton Capacity · 6 min away · Heavy Duty Bed
            </div>
          </div>
        </div>

        <!-- Option 3: Heavy (Eicher Pro) -->
        <div onclick="selectGramhaulVehicleTier('heavy')" id="tier-heavy" style="background:#111722;border:1px solid rgba(255,255,255,0.08);border-radius:18px;padding:12px 14px;display:flex;align-items:center;gap:12px;cursor:pointer;transition:all 0.2s ease;">
          <div style="width:46px;height:46px;border-radius:14px;background:#1F293D;display:flex;align-items:center;justify-content:center;font-size:24px;flex-shrink:0;">
            🚛
          </div>
          <div style="flex:1;min-width:0;">
            <div style="display:flex;align-items:center;justify-content:space-between;">
              <span style="font-size:13.5px;font-weight:900;color:#FFFFFF;">Heavy (Eicher 5-Ton)</span>
              <span style="font-size:14px;font-weight:900;color:#FFFFFF;">₹2,600</span>
            </div>
            <div style="font-size:10.5px;color:#94A3B8;margin-top:2px;">
              5.0 Ton Capacity · 8 min away · Bulk Grain Bulkhead
            </div>
          </div>
        </div>

        <!-- Active In-Transit Driver Card (Image 4 Style) -->
        <div style="background:#151C28;border:1px solid rgba(34,197,94,0.3);border-radius:20px;padding:14px;margin-top:4px;box-shadow:0 8px 24px rgba(0,0,0,0.5);">
          <!-- Top ETA Header -->
          <div style="background:#22C55E;color:#0A0E17;border-radius:12px;padding:8px 12px;display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
            <span style="font-size:12px;font-weight:900;">Your driver is on the way</span>
            <span style="font-size:11px;font-weight:900;background:rgba(0,0,0,0.15);padding:2px 8px;border-radius:6px;">2 min</span>
          </div>

          <!-- Driver Profile Row -->
          <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
            <div style="width:46px;height:46px;border-radius:50%;background:linear-gradient(135deg, #10B981, #059669);display:flex;align-items:center;justify-content:center;font-size:22px;border:2px solid #22C55E;">
              🧔🏽
            </div>
            <div style="flex:1;min-width:0;">
              <div style="display:flex;align-items:center;justify-content:space-between;">
                <span style="font-size:13.5px;font-weight:900;color:#FFFFFF;">Ramesh Kumar</span>
                <span style="font-size:11px;font-weight:800;color:#FBBF24;">⭐️ 4.9</span>
              </div>
              <div style="display:flex;align-items:center;justify-content:space-between;margin-top:2px;">
                <span style="font-size:11px;color:#94A3B8;">Tata Ace Super</span>
                <span style="font-size:10px;font-weight:800;background:#1E293B;color:#CBD5E1;padding:2px 6px;border-radius:6px;">TS03AB2940</span>
              </div>
            </div>
          </div>

          <!-- Action Buttons: Call, Message, Share, Cancel -->
          <div style="display:grid;grid-template-columns:repeat(4, 1fr);gap:8px;">
            <button onclick="alert('Calling Driver Ramesh Kumar: +91 98480 22334')" style="background:#1E293B;border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:8px 0;color:#FFFFFF;cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:4px;">
              <span style="font-size:14px;">📞</span>
              <span style="font-size:9.5px;font-weight:700;">Call</span>
            </button>
            <button onclick="alert('Opening GramHaul Driver Chat...')" style="background:#1E293B;border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:8px 0;color:#FFFFFF;cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:4px;">
              <span style="font-size:14px;">💬</span>
              <span style="font-size:9.5px;font-weight:700;">Message</span>
            </button>
            <button onclick="alert('Live Trip Tracking Link copied to clipboard!')" style="background:#1E293B;border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:8px 0;color:#FFFFFF;cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:4px;">
              <span style="font-size:14px;">📤</span>
              <span style="font-size:9.5px;font-weight:700;">Share</span>
            </button>
            <button onclick="alert('Trip booking cancelled successfully.')" style="background:#1E293B;border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:8px 0;color:#EF4444;cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:4px;">
              <span style="font-size:14px;">✕</span>
              <span style="font-size:9.5px;font-weight:700;">Cancel</span>
            </button>
          </div>

          <!-- Trip Timeline -->
          <div style="display:flex;justify-content:space-between;align-items:center;margin-top:14px;padding-top:12px;border-top:1px solid rgba(255,255,255,0.08);">
            <div>
              <div style="font-size:9.5px;color:#94A3B8;">Pickup in</div>
              <div style="font-size:12.5px;font-weight:900;color:#FFFFFF;">2 min</div>
            </div>
            <!-- Progress Line -->
            <div style="flex:1;margin:0 12px;height:4px;background:#1E293B;border-radius:2px;position:relative;">
              <div style="width:75%;height:100%;background:#22C55E;border-radius:2px;"></div>
              <div style="position:absolute;top:-4px;left:75%;width:12px;height:12px;border-radius:50%;background:#22C55E;box-shadow:0 0 8px #22C55E;"></div>
            </div>
            <div style="text-align:right;">
              <div style="font-size:9.5px;color:#94A3B8;">Arrive Mandi by</div>
              <div style="font-size:12.5px;font-weight:900;color:#FFFFFF;">9:52 AM</div>
            </div>
          </div>
        </div>

        <!-- Primary Confirm CTA Button -->
        <button onclick="alert('GramHaul Standard Booking Confirmed! Driver Ramesh Kumar is en route.')" style="width:100%;height:52px;border-radius:26px;background:linear-gradient(135deg, #22C55E, #16A34A);color:#0A0E17;border:none;font-size:15px;font-weight:900;cursor:pointer;box-shadow:0 8px 24px rgba(34,197,94,0.35);display:flex;align-items:center;justify-content:center;gap:8px;margin-top:6px;">
          <span>Confirm Standard</span>
          <span>·</span>
          <span>₹850</span>
        </button>

      </div>

    </div>
  `;
}'''

def update_file(path):
    print(f"Updating GramHaul view in {path}...")
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # Replace gramhaul: () => { ... }
    # Let's find gramhaul: in APP_VIEWS
    pattern = r'gramhaul:\s*\(\)\s*=>\s*\{[\s\S]*?(?=\n\s*[a-zA-Z0-9_]+:\s*(?:\(\)|function)|\n\s*\};)'
    match = re.search(pattern, c)
    if match:
        c = c[:match.start()] + new_gramhaul_view + c[match.end():]
        print("Replaced APP_VIEWS.gramhaul successfully!")
    else:
        print("Could not find exact regex match for gramhaul view; searching by substring")
        idx_start = c.find('gramhaul: () => {')
        if idx_start != -1:
            idx_end = c.find('agristack: () => {', idx_start)
            if idx_end != -1:
                c = c[:idx_start] + new_gramhaul_view + ',\n    ' + c[idx_end:]
                print("Replaced by substring markers!")

    # Add helper JS function for selecting vehicle tier
    tier_js = '''
function selectGramhaulVehicleTier(tier) {
  ['standard', 'comfort', 'heavy'].forEach(t => {
    const el = document.getElementById('tier-' + t);
    if (el) {
      if (t === tier) {
        el.style.border = '2px solid #22C55E';
        el.style.boxShadow = '0 4px 16px rgba(34,197,94,0.2)';
      } else {
        el.style.border = '1px solid rgba(255,255,255,0.08)';
        el.style.boxShadow = 'none';
      }
    }
  });
}
'''
    if 'function selectGramhaulVehicleTier' not in c:
        c = c.replace('</body>', f'<script>\n{tier_js}\n</script>\n</body>')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"Done updating {path}")

update_file('app/src/main/assets/index.html')
update_file('nukrop_emulator.html')
