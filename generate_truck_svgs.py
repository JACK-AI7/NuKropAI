import sys

sys.stdout.reconfigure(encoding='utf-8')

# Real High-End SVG Vector Renders for Indian Commercial Farm Trucks

TATA_ACE_SVG = '''<svg width="64" height="42" viewBox="0 0 120 70" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- Tata Ace Mini Truck Side Profile -->
  <!-- Cargo Bed Box -->
  <rect x="38" y="18" width="76" height="32" rx="3" fill="#E2E8F0" stroke="#94A3B8" stroke-width="1.5"/>
  <path d="M40 22H112M40 32H112M40 42H112" stroke="#CBD5E1" stroke-width="1"/>
  <!-- Tarpaulin Cover / Bags -->
  <path d="M40 18 Q 75 10 112 18" fill="#16A34A" fill-opacity="0.2" stroke="#16A34A" stroke-width="1.5"/>
  <!-- Cabin Main Body -->
  <path d="M12 48 L12 28 C12 24 16 20 22 18 L34 18 C37 18 38 20 38 24 L38 48 Z" fill="#FFFFFF" stroke="#64748B" stroke-width="1.5"/>
  <!-- Front Windshield -->
  <path d="M16 28 L24 20 L34 20 L34 30 L16 30 Z" fill="#38BDF8" fill-opacity="0.5" stroke="#0284C7" stroke-width="1"/>
  <!-- Headlight & Bumper -->
  <rect x="8" y="40" width="5" height="7" rx="1.5" fill="#FBBF24" stroke="#D97706" stroke-width="0.8"/>
  <rect x="8" y="47" width="30" height="5" rx="2" fill="#334155"/>
  <!-- Chassis Base -->
  <rect x="15" y="49" width="98" height="4" fill="#1E293B"/>
  <!-- Front Wheel -->
  <circle cx="28" cy="52" r="11" fill="#0F172A"/>
  <circle cx="28" cy="52" r="6" fill="#94A3B8"/>
  <circle cx="28" cy="52" r="2.5" fill="#0F172A"/>
  <!-- Rear Wheel -->
  <circle cx="94" cy="52" r="11" fill="#0F172A"/>
  <circle cx="94" cy="52" r="6" fill="#94A3B8"/>
  <circle cx="94" cy="52" r="2.5" fill="#0F172A"/>
</svg>'''

BOLERO_MAXI_SVG = '''<svg width="64" height="42" viewBox="0 0 130 70" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- Mahindra Bolero Maxi Truck Pickup Profile -->
  <!-- Long Cargo Bed -->
  <rect x="46" y="24" width="78" height="26" rx="2" fill="#F1F5F9" stroke="#94A3B8" stroke-width="1.5"/>
  <rect x="50" y="28" width="70" height="18" fill="#E2E8F0"/>
  <!-- Bolero Rugged Cab -->
  <path d="M8 48 L8 32 C8 30 10 28 14 26 L26 18 C28 16 32 16 36 16 L44 16 C46 16 46 18 46 22 L46 48 Z" fill="#FFFFFF" stroke="#475569" stroke-width="1.5"/>
  <!-- Slanted Windshield & Side Window -->
  <path d="M16 28 L27 19 L36 19 L36 30 L14 30 Z" fill="#38BDF8" fill-opacity="0.5" stroke="#0284C7" stroke-width="1"/>
  <rect x="38" y="19" width="6" height="11" fill="#38BDF8" fill-opacity="0.4" stroke="#0284C7" stroke-width="0.8"/>
  <!-- Front Grille & Bullbar -->
  <rect x="6" y="34" width="4" height="10" fill="#CBD5E1" stroke="#475569" stroke-width="1"/>
  <rect x="5" y="44" width="40" height="6" rx="2" fill="#1E293B"/>
  <!-- Chassis Base -->
  <rect x="10" y="49" width="112" height="4" fill="#0F172A"/>
  <!-- Front Wheel -->
  <circle cx="28" cy="52" r="11.5" fill="#0F172A"/>
  <circle cx="28" cy="52" r="6.5" fill="#64748B"/>
  <circle cx="28" cy="52" r="2.5" fill="#0F172A"/>
  <!-- Rear Wheel -->
  <circle cx="102" cy="52" r="11.5" fill="#0F172A"/>
  <circle cx="102" cy="52" r="6.5" fill="#64748B"/>
  <circle cx="102" cy="52" r="2.5" fill="#0F172A"/>
</svg>'''

EICHER_PRO_SVG = '''<svg width="64" height="42" viewBox="0 0 140 70" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- Eicher Pro Heavy Duty Commercial Lorry -->
  <!-- Heavy Cargo Container -->
  <rect x="44" y="10" width="90" height="40" rx="3" fill="#F8FAFC" stroke="#64748B" stroke-width="1.5"/>
  <path d="M46 16 H132 M46 26 H132 M46 36 H132 M46 46 H132" stroke="#E2E8F0" stroke-width="1.5"/>
  <path d="M72 10 V50 M104 10 V50" stroke="#CBD5E1" stroke-width="1.5"/>
  <!-- Big Tall Cabin -->
  <path d="M8 48 L8 22 C8 16 12 12 18 12 L42 12 C44 12 44 14 44 18 L44 48 Z" fill="#15803D" stroke="#14532D" stroke-width="1.5"/>
  <!-- Big Windshield & Side Window -->
  <path d="M12 26 L16 16 L34 16 L34 28 L12 28 Z" fill="#E0F2FE" fill-opacity="0.8" stroke="#0284C7" stroke-width="1"/>
  <rect x="36" y="16" width="6" height="12" fill="#E0F2FE" fill-opacity="0.6" stroke="#0284C7" stroke-width="0.8"/>
  <!-- Heavy Bumper -->
  <rect x="6" y="42" width="38" height="8" rx="2" fill="#1E293B"/>
  <rect x="6" y="38" width="5" height="5" fill="#FBBF24"/>
  <!-- Heavy Multi-Axle Chassis -->
  <rect x="12" y="49" width="122" height="5" fill="#0F172A"/>
  <!-- Front Wheel -->
  <circle cx="26" cy="52" r="12" fill="#0F172A"/>
  <circle cx="26" cy="52" r="7" fill="#CBD5E1"/>
  <circle cx="26" cy="52" r="3" fill="#0F172A"/>
  <!-- Dual Rear Axle Wheels -->
  <circle cx="94" cy="52" r="12" fill="#0F172A"/>
  <circle cx="94" cy="52" r="7" fill="#CBD5E1"/>
  <circle cx="94" cy="52" r="3" fill="#0F172A"/>
  <circle cx="120" cy="52" r="12" fill="#0F172A"/>
  <circle cx="120" cy="52" r="7" fill="#CBD5E1"/>
  <circle cx="120" cy="52" r="3" fill="#0F172A"/>
</svg>'''

print("All truck SVGs created cleanly!")
