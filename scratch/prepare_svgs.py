import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# High-end SVG constants
SVG_DRIVER_AVATAR = '''<svg width="44" height="44" viewBox="0 0 44 44" fill="none" style="display:block;">
  <circle cx="22" cy="22" r="22" fill="#DCFCE7"/>
  <mask id="driverMask" maskUnits="userSpaceOnUse" x="0" y="0" width="44" height="44">
    <circle cx="22" cy="22" r="22" fill="#FFFFFF"/>
  </mask>
  <g mask="url(#driverMask)">
    <path d="M7 44C7 35.7 13.7 29 22 29C30.3 29 37 35.7 37 44H7Z" fill="#1E293B"/>
    <path d="M19 29L22 34L25 29H19Z" fill="#22C55E"/>
    <path d="M22 25C25.9 25 29 21.6 29 17.5C29 13.4 25.9 10 22 10C18.1 10 15 13.4 15 17.5C15 21.6 18.1 25 22 25Z" fill="#F8D7BE"/>
    <path d="M14 14C14 10.5 17.5 8 22 8C26.5 8 30 10.5 30 14H14Z" fill="#0F172A"/>
    <path d="M12 14C12 14 14.5 15.5 22 15.5C29.5 15.5 32 14 32 14L34 16H10L12 14Z" fill="#15803D"/>
    <circle cx="22" cy="11" r="1.8" fill="#FBBF24"/>
  </g>
  <circle cx="34" cy="34" r="8" fill="#16A34A" stroke="#FFFFFF" stroke-width="2"/>
  <path d="M31 34L33 36L37 32" stroke="#FFFFFF" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
</svg>'''

SVG_DRIVER_AVATAR_LARGE = '''<svg width="76" height="76" viewBox="0 0 44 44" fill="none" style="display:block;">
  <circle cx="22" cy="22" r="22" fill="#DCFCE7"/>
  <mask id="driverMaskLg" maskUnits="userSpaceOnUse" x="0" y="0" width="44" height="44">
    <circle cx="22" cy="22" r="22" fill="#FFFFFF"/>
  </mask>
  <g mask="url(#driverMaskLg)">
    <path d="M7 44C7 35.7 13.7 29 22 29C30.3 29 37 35.7 37 44H7Z" fill="#1E293B"/>
    <path d="M19 29L22 34L25 29H19Z" fill="#22C55E"/>
    <path d="M22 25C25.9 25 29 21.6 29 17.5C29 13.4 25.9 10 22 10C18.1 10 15 13.4 15 17.5C15 21.6 18.1 25 22 25Z" fill="#F8D7BE"/>
    <path d="M14 14C14 10.5 17.5 8 22 8C26.5 8 30 10.5 30 14H14Z" fill="#0F172A"/>
    <path d="M12 14C12 14 14.5 15.5 22 15.5C29.5 15.5 32 14 32 14L34 16H10L12 14Z" fill="#15803D"/>
    <circle cx="22" cy="11" r="1.8" fill="#FBBF24"/>
  </g>
  <circle cx="34" cy="34" r="8" fill="#16A34A" stroke="#FFFFFF" stroke-width="2"/>
  <path d="M31 34L33 36L37 32" stroke="#FFFFFF" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
</svg>'''

SVG_RADAR_TRUCK = '''<svg width="28" height="28" viewBox="0 0 28 28" fill="none" style="display:block;">
  <rect x="2" y="8" width="16" height="12" rx="2.5" fill="#FFFFFF"/>
  <path d="M18 11H22.5L25.5 15.5V20H18V11Z" fill="#DCFCE7"/>
  <path d="M19 12.5H22L24.5 15.5H19V12.5Z" fill="#16A34A"/>
  <circle cx="7" cy="20" r="3" fill="#15803D" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="21" cy="20" r="3" fill="#15803D" stroke="#FFFFFF" stroke-width="1.5"/>
</svg>'''

SVG_CALL = '''<svg width="22" height="22" viewBox="0 0 24 24" fill="none" style="display:block;"><path d="M22 16.92V19.92C22.0011 20.1985 21.9441 20.4742 21.8325 20.7294C21.7209 20.9845 21.5573 21.2136 21.3521 21.4019C21.1468 21.5901 20.9046 21.7335 20.6407 21.8228C20.3769 21.912 20.0974 21.9452 19.82 21.92C16.7428 21.5856 13.787 20.5342 11.19 18.85C8.77382 17.3147 6.72533 15.2662 5.18999 12.85C3.49997 10.2412 2.44824 7.27099 2.11999 4.17997C2.095 3.90354 2.12787 3.62486 2.21651 3.36173C2.30516 3.0986 2.44766 2.85686 2.63503 2.65171C2.82241 2.44655 3.05051 2.28257 3.30456 2.17013C3.55861 2.05769 3.83307 2.00003 4.10999 2H7.10999C7.5953 1.99522 8.06579 2.16708 8.43376 2.48353C8.80173 2.80007 9.04207 3.23945 9.10999 3.71997C9.23662 4.68007 9.47144 5.62273 9.80999 6.52997C9.9446 6.88789 9.97366 7.27689 9.8939 7.65089C9.81415 8.02488 9.62886 8.36814 9.35999 8.63997L8.08999 9.90997C9.51355 12.4135 11.5864 14.4864 14.09 15.91L15.36 14.64C15.6318 14.3711 15.9751 14.1858 16.3491 14.1061C16.7231 14.0263 17.1121 14.0554 17.47 14.19C18.3773 14.5285 19.3199 14.7634 20.28 14.89C20.7658 14.9585 21.2094 15.2032 21.5265 15.5776C21.8437 15.9519 22.0121 16.4305 22 16.92Z" fill="#16A34A"/></svg>'''

SVG_MSG = '''<svg width="22" height="22" viewBox="0 0 24 24" fill="none" style="display:block;"><path d="M21 11.5C21.0034 12.8199 20.6951 14.1219 20.1 15.3C19.3944 16.7118 18.3098 17.8992 16.9674 18.7293C15.6251 19.5594 14.0782 19.9994 12.5 20C11.1801 20.0034 9.87812 19.6951 8.7 19.1L3 21L4.9 15.3C4.30493 14.1219 3.99656 12.8199 4 11.5C4.00061 9.92179 4.44061 8.37488 5.27072 7.03258C6.10083 5.69028 7.28825 4.6056 8.7 3.90003C9.87812 3.30496 11.1801 2.99659 12.5 3.00003H13C15.0843 3.11502 17.053 3.99479 18.5291 5.47089C20.0052 6.94699 20.885 8.91568 21 11V11.5Z" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="#EFF6FF"/><circle cx="8.5" cy="11.5" r="1.2" fill="#2563EB"/><circle cx="12.5" cy="11.5" r="1.2" fill="#2563EB"/><circle cx="16.5" cy="11.5" r="1.2" fill="#2563EB"/></svg>'''

SVG_SHARE = '''<svg width="22" height="22" viewBox="0 0 24 24" fill="none" style="display:block;"><circle cx="18" cy="5" r="3" fill="#8B5CF6" stroke="#8B5CF6" stroke-width="1.5"/><circle cx="6" cy="12" r="3" fill="#8B5CF6" stroke="#8B5CF6" stroke-width="1.5"/><circle cx="18" cy="19" r="3" fill="#8B5CF6" stroke="#8B5CF6" stroke-width="1.5"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49" stroke="#8B5CF6" stroke-width="2" stroke-linecap="round"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49" stroke="#8B5CF6" stroke-width="2" stroke-linecap="round"/></svg>'''

SVG_CANCEL = '''<svg width="22" height="22" viewBox="0 0 24 24" fill="none" style="display:block;"><circle cx="12" cy="12" r="10" fill="#FEE2E2"/><path d="M15 9L9 15M9 9L15 15" stroke="#EF4444" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'''

SVG_PIN_FARM = '''<svg width="18" height="18" viewBox="0 0 24 24" fill="none" style="flex-shrink:0;"><circle cx="12" cy="10" r="3" fill="#22C55E"/><path d="M12 2C7.58 2 4 5.58 4 10C4 15.25 12 22 12 22C12 22 20 15.25 20 10C20 5.58 16.42 2 12 2Z" stroke="#22C55E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'''

SVG_APMC_MANDI = '''<svg width="18" height="18" viewBox="0 0 24 24" fill="none" style="flex-shrink:0;"><path d="M3 21H21M4 18V9L12 3L20 9V18M9 21V12H15V21" stroke="#3B82F6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="#EFF6FF"/></svg>'''

SVG_PRODUCE_LOAD = '''<svg width="18" height="18" viewBox="0 0 24 24" fill="none" style="flex-shrink:0;"><path d="M12 22V2M12 7C9.5 5 7 7 7 10C7 13 12 15 12 15M12 7C14.5 5 17 7 17 10C17 13 12 15 12 15M12 12C9.5 10 7 12 7 15C7 18 12 20 12 20M12 12C14.5 10 17 12 17 15C17 18 12 20 12 20" stroke="#F59E0B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'''

SVG_FARE_CURRENCY = '''<svg width="18" height="18" viewBox="0 0 24 24" fill="none" style="flex-shrink:0;"><rect x="2" y="5" width="20" height="14" rx="3" fill="#DCFCE7" stroke="#16A34A" stroke-width="1.8"/><circle cx="16" cy="12" r="2.5" fill="#16A34A"/><path d="M6 9H11M6 12H9.5M6 15L9 12" stroke="#15803D" stroke-width="1.8" stroke-linecap="round"/></svg>'''

SVG_CHEVRON_DOWN = '''<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#94A3B8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="transition:transform 0.2s ease;"><polyline points="6 9 12 15 18 9"/></svg>'''

SVG_CROSS_SM = '''<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>'''

SVG_MIC = '''<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg>'''

SVG_SPEAKER = '''<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"/></svg>'''

SVG_SEND = '''<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>'''

SVG_INVOICE_RECEIPT = '''<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><line x1="10" y1="9" x2="8" y2="9"/></svg>'''

SVG_DOWNLOAD = '''<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>'''

SVG_CHECK_SHIELD = '''<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/></svg>'''

SVG_LOCK_SHIELD = '''<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#92400E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>'''

print("SVGs prepared successfully.")
