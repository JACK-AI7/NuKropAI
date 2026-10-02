const fs = require('fs');

const updatedAppContent = `import { useState, useEffect } from 'react';
import { 
  Sprout, 
  Smartphone, 
  AlertTriangle, 
  ShieldCheck, 
  ChevronRight, 
  ChevronDown,
  ScanLine, 
  TrendingUp, 
  Landmark, 
  CloudRain, 
  Layers, 
  Globe, 
  Download, 
  Menu, 
  X, 
  Radio,
  CheckCircle,
  Copy,
  ExternalLink,
  Truck,
  Shield,
  FileText
} from 'lucide-react';

export default function App() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [openFaq, setOpenFaq] = useState<number | null>(0);
  const [scrollProgress, setScrollProgress] = useState(0);
  const [activeCategory, setActiveCategory] = useState<'all' | 'onboarding' | 'farmer' | 'logistics' | 'driver'>('all');
  const [selectedScreenshot, setSelectedScreenshot] = useState<string | null>(null);
  const [copiedHash, setCopiedHash] = useState(false);
  const [showPrivacyModal, setShowPrivacyModal] = useState(false);
  const [showTermsModal, setShowTermsModal] = useState(false);

  // Scroll Progress Tracker
  useEffect(() => {
    const handleScroll = () => {
      const totalScroll = document.documentElement.scrollTop || document.body.scrollTop;
      const windowHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      if (windowHeight > 0) {
        setScrollProgress((totalScroll / windowHeight) * 100);
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const apkSha256 = 'D825747717C02FB801B3D90D4CF21E697EBFFBE01C2908A31AA6B90E596B4805';

  const copyHashToClipboard = () => {
    navigator.clipboard.writeText(apkSha256);
    setCopiedHash(true);
    setTimeout(() => setCopiedHash(false), 2000);
  };

  const screenshots = [
    { id: '01', title: 'Splash Screen & Brand', file: '/screenshots/01_splash_screen.png', cat: 'onboarding', desc: 'Full-screen emerald brand lockup with pulsing golden seed ring and autonomous OS tagline.' },
    { id: '02', title: '11 Indian Languages', file: '/screenshots/02_language_selection.png', cat: 'onboarding', desc: 'Single-language selection across Telugu, Hindi, Tamil, Kannada, Malayalam, Marathi, Bengali, Odia.' },
    { id: '03', title: 'AI Crop Doctor Onboarding', file: '/screenshots/03_onboarding_slide1_telugu.png', cat: 'onboarding', desc: 'Full-bleed photograph slide with pure regional script and 6-stage animated dot indicator.' },
    { id: '04', title: 'Mandi Market Intelligence', file: '/screenshots/04_onboarding_slide3_mandi_telugu.png', cat: 'onboarding', desc: 'Real-time Agmarknet market intelligence onboarding with APMC trend forecasts.' },
    { id: '05', title: 'GramHaul Pooled Logistics', file: '/screenshots/05_onboarding_slide5_gramhaul_telugu.png', cat: 'logistics', desc: '40% cost reduction pooled farm haulage explanation with pure regional typography.' },
    { id: '06', title: 'Native Camera Permissions', file: '/screenshots/06_permissions_camera.png', cat: 'onboarding', desc: 'Hardware camera permission requester with direct OS intent trigger and skip bypass.' },
    { id: '07', title: '143 OpenFarm Crops', file: '/screenshots/07_crop_selection.png', cat: 'farmer', desc: 'Complete 143-crop catalog selection with native Telugu titles and active multi-select counters.' },
    { id: '08', title: 'Farmer Home Dashboard', file: '/screenshots/08_farmer_home_dashboard.png', cat: 'farmer', desc: 'Live weather bento card, spray condition indicator, APMC price marquee, and active pest warnings.' },
    { id: '09', title: 'Farmer Profile & Logout', file: '/screenshots/09_farmer_profile_clean.png', cat: 'farmer', desc: 'AgriStack ID badge, landholding acres, soil score, and prominent red session logout button.' },
    { id: '10', title: 'AgriStack Digital Passport', file: '/screenshots/10_agristack_passport_modal.png', cat: 'farmer', desc: 'National farmer digital ID card with QR verification, Dharani survey records, and RoR-1B links.' },
    { id: '11', title: 'GramHaul 40% Map Booking', file: '/screenshots/11_gramhaul_redesigned_map_trucks.png', cat: 'logistics', desc: 'Leaflet OpenStreetMap with real moving GPS trucks, sack stepper, and commercial tiers.' },
    { id: '12', title: 'Real-Time Dispatch Radar', file: '/screenshots/12_gramhaul_dispatch_broadcast_modal.png', cat: 'logistics', desc: 'Live driver dispatch broadcast radar with pulsing waves and 60-second matching timer.' },
    { id: '13', title: 'Driver Cockpit Live Map', file: '/screenshots/13_driver_cockpit_map.png', cat: 'driver', desc: 'Obsidian cockpit theme with Duty ON/OFF, incoming haul request card, and Accept/Decline actions.' },
    { id: '14', title: 'Driver Profile & Logs', file: '/screenshots/14_driver_profile_clean.png', cat: 'driver', desc: 'Driver credentials, Tata Ace Gold 1.5T plate, completed trips counter, and FASTag portal.' },
    { id: '15', title: 'Commercial Insurance & FASTag', file: '/screenshots/15_driver_insurance_fastag_modal.png', cat: 'driver', desc: 'Commercial vehicle insurance policy breakdown and real-time NETC FASTag toll balance check.' },
  ];

  const filteredScreenshots = activeCategory === 'all' 
    ? screenshots 
    : screenshots.filter(s => s.cat === activeCategory);

  const faqs = [
    {
      q: 'How do I install the NuKropAI APK on my Android smartphone?',
      a: 'Tap the "Download NuKropAI APK" button to download the official release APK file (49.4 MB). When downloaded, tap the file in your notification panel or Downloads folder, and select "Install" (enable "Install from Unknown Sources" if prompted). NuKropAI is 100% verified, ad-free, and contains zero tracking bloat.'
    },
    {
      q: 'Does the AI Disease Scanner work offline in remote fields without 4G/5G?',
      a: 'Yes! NuKropAI contains an embedded offline ICAR botanical diagnostic engine that diagnoses common Indian crop pathologies locally on your phone without requiring an active internet connection. When you reconnect to data, it auto-syncs with the Supabase cloud.'
    },
    {
      q: 'How does GramHaul pooled logistics save farmers 40% on transport?',
      a: 'GramHaul pools nearby farmers traveling to the same APMC Mandi onto verified commercial transport vehicles (Tata Ace Gold 1.5T, Mahindra Bolero Maxi 2.5T, Eicher Canter 5T). Instead of paying for a full empty return truck, you only pay per quintal for the space your crop sacks occupy.'
    },
    {
      q: 'How are live Mandi rates sourced and verified?',
      a: 'Rates are fetched in real-time directly from the Government of India Ministry of Agriculture (Agmarknet) APMC daily trading journals. Quoted modal prices, minimums, and maximums are 100% official and unmanipulated by local cartels.'
    },
    {
      q: 'What languages are supported across the mobile app?',
      a: 'NuKropAI features 100% single-language purity across 11 Indian languages: Telugu, Hindi, Tamil, Kannada, Malayalam, Marathi, Bengali, Gujarati, Punjabi, Odia, and English.'
    }
  ];

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', position: 'relative' }}>
      
      {/* ── TOP SCROLL PROGRESS ANIMATION BAR ── */}
      <div className="scroll-progress-container">
        <div 
          className="scroll-progress-bar" 
          style={{ width: \`\${scrollProgress}%\` }}
        ></div>
      </div>

      {/* Background Layers */}
      <div className="dynamic-bg"></div>
      <div className="dynamic-overlay"></div>
      
      {/* ── FLOATING LUXURY PILL NAVBAR ── */}
      <header className="site-header">
        <div className="nav-pill-wrapper">
          
          {/* Logo */}
          <a href="#" style={{ display: 'flex', alignItems: 'center', gap: '9px', textDecoration: 'none' }}>
            <div style={{ 
              padding: '6px', 
              background: 'linear-gradient(135deg, rgba(200, 232, 55, 0.2) 0%, rgba(34, 197, 94, 0.2) 100%)', 
              borderRadius: '50%', 
              border: '1px solid rgba(200, 232, 55, 0.35)', 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center' 
            }}>
              <Sprout style={{ color: 'var(--nukrop-accent)', width: '18px', height: '18px' }} />
            </div>
            <span style={{ fontSize: '18px', fontFamily: 'Outfit', fontWeight: '800', letterSpacing: '0.02em', color: '#FFFFFF' }}>
              NuKrop<span style={{ color: 'var(--nukrop-accent)' }}>AI</span>
            </span>
          </a>

          {/* Desktop Navigation Links */}
          <nav className="nav-links">
            <a href="#features" className="nav-link">Features</a>
            <a href="#showcase" className="nav-link">App Showcase</a>
            <a href="#gramhaul" className="nav-link">GramHaul</a>
            <a href="#languages" className="nav-link">Languages</a>
            <a href="#download" className="nav-link" style={{ color: 'var(--nukrop-accent)', fontWeight: '700' }}>Download</a>
            <a href="#faq" className="nav-link">FAQ</a>
            
            <a 
              href="/NuKropAI.apk" 
              download="NuKropAI.apk"
              className="nukrop-btn" 
              style={{ 
                padding: '8px 18px', 
                fontSize: '12.5px', 
                borderRadius: '100px',
                boxShadow: '0 4px 14px rgba(200, 232, 55, 0.3)'
              }}
            >
              <Download style={{ width: '14px', height: '14px' }} />
              <span>Get APK (v2.4)</span>
            </a>
          </nav>

          {/* Mobile Menu Toggle Button */}
          <button 
            className="nav-mobile-toggle"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Toggle Navigation Menu"
          >
            {mobileMenuOpen ? <X style={{ width: '20px', height: '20px' }} /> : <Menu style={{ width: '20px', height: '20px' }} />}
          </button>
        </div>
      </header>

      {/* Mobile Nav Drawer */}
      <div className={\`nav-mobile-drawer \${mobileMenuOpen ? 'open' : ''}\`}>
        <a href="#features" className="nav-link" onClick={() => setMobileMenuOpen(false)} style={{ fontSize: '15px', padding: '6px 0' }}>Features</a>
        <a href="#showcase" className="nav-link" onClick={() => setMobileMenuOpen(false)} style={{ fontSize: '15px', padding: '6px 0' }}>App Showcase</a>
        <a href="#gramhaul" className="nav-link" onClick={() => setMobileMenuOpen(false)} style={{ fontSize: '15px', padding: '6px 0' }}>GramHaul Logistics</a>
        <a href="#languages" className="nav-link" onClick={() => setMobileMenuOpen(false)} style={{ fontSize: '15px', padding: '6px 0' }}>Languages</a>
        <a href="#download" className="nav-link" onClick={() => setMobileMenuOpen(false)} style={{ fontSize: '15px', padding: '6px 0', color: 'var(--nukrop-accent)', fontWeight: '700' }}>Download APK</a>
        <a href="#faq" className="nav-link" onClick={() => setMobileMenuOpen(false)} style={{ fontSize: '15px', padding: '6px 0' }}>FAQ</a>
        <a 
          href="/NuKropAI.apk" 
          download="NuKropAI.apk"
          className="nukrop-btn" 
          onClick={() => setMobileMenuOpen(false)}
          style={{ width: '100%', padding: '12px 20px', fontSize: '14px', marginTop: '6px', borderRadius: '12px' }}
        >
          <Download style={{ width: '16px', height: '16px' }} />
          <span>Download NuKropAI APK (49.4 MB)</span>
        </a>
      </div>

      {/* ── MAIN CONTENT ── */}
      <main style={{ flex: '1', width: '100%', paddingTop: '90px' }}>
        
        {/* ═════════════════════ HERO SECTION ═════════════════════ */}
        <section className="site-container section-spacing" style={{ textAlign: 'center', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          
          {/* Live Status Pill */}
          <div style={{ 
            padding: '6px 16px', 
            background: 'rgba(200, 232, 55, 0.08)', 
            border: '1px solid rgba(200, 232, 55, 0.25)', 
            borderRadius: '100px', 
            marginBottom: '24px', 
            display: 'inline-flex', 
            alignItems: 'center', 
            gap: '8px' 
          }}>
            <span className="live-pulse"></span>
            <span style={{ fontSize: '12px', color: 'var(--nukrop-accent)', fontWeight: '700', letterSpacing: '0.04em', textTransform: 'uppercase' }}>
              NuKropAI v2.4 Production Engine · Active Release
            </span>
          </div>

          {/* Hero Headline */}
          <h1 style={{ 
            fontSize: 'clamp(32px, 5.5vw, 64px)', 
            lineHeight: 1.15, 
            marginBottom: '20px', 
            fontWeight: '800', 
            color: '#FFFFFF',
            maxWidth: '900px'
          }}>
            Sovereign Agrarian OS, <br/>
            <span style={{ 
              background: 'linear-gradient(135deg, var(--nukrop-accent) 0%, #D4F040 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              filter: 'drop-shadow(0 0 24px rgba(200, 232, 55, 0.3))'
            }}>
              Now in your hands.
            </span>
          </h1>

          {/* Subtitle */}
          <p style={{ 
            fontSize: 'clamp(15px, 2vw, 19px)', 
            color: 'var(--nukrop-text-dim)', 
            maxWidth: '720px', 
            lineHeight: 1.6, 
            marginBottom: '36px' 
          }}>
            A complete operating system engineered to eliminate crop loss, optimize fertilizer dosages, dispatch pooled farm logistics, and secure unmanipulated APMC market pricing.
          </p>

          {/* Download CTAs */}
          <div className="hero-buttons" style={{ display: 'flex', gap: '14px', justifyContent: 'center', marginBottom: '28px', flexWrap: 'wrap' }}>
            <a
              href="/NuKropAI.apk"
              download="NuKropAI.apk"
              className="nukrop-btn"
              style={{
                padding: '16px 36px',
                fontSize: '16px',
                borderRadius: '16px',
                boxShadow: '0 8px 32px rgba(200, 232, 55, 0.35)',
              }}
            >
              <Download style={{ width: '20px', height: '20px' }} />
              <span>Download NuKropAI App</span>
              <span style={{
                background: 'rgba(0,0,0,0.18)',
                borderRadius: '6px',
                padding: '3px 8px',
                fontSize: '12px',
                fontWeight: '700',
                marginLeft: '6px'
              }}>v2.4 (Latest) · 49.4 MB</span>
            </a>

            <a
              href="#showcase"
              className="nukrop-btn nukrop-btn-secondary"
              style={{
                padding: '16px 28px',
                fontSize: '15px',
                borderRadius: '16px',
              }}
            >
              <span>View 15-Screen Gallery</span>
              <ChevronRight style={{ width: '16px', height: '16px' }} />
            </a>
          </div>

          {/* Android Compatibility Disclaimer */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--nukrop-text-muted)', fontSize: '13px', marginBottom: '48px', flexWrap: 'wrap', justifyContent: 'center' }}>
            <Smartphone style={{ width: '15px', height: '15px', color: 'var(--nukrop-accent)' }} />
            <span>Android 8.0+ · SHA-256 Verified · Sideload Ready · Zero Ads · 100% Free for Farmers</span>
          </div>

          {/* Stats Bar */}
          <div className="glass-card stats-row" style={{ 
            width: '100%', 
            maxWidth: '920px', 
            padding: '24px 28px', 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'space-around',
            gap: '16px'
          }}>
            <div className="stat-item" style={{ textAlign: 'center' }}>
              <strong style={{ fontSize: 'clamp(20px, 3vw, 28px)', color: '#FFFFFF', display: 'block' }}>143</strong>
              <span style={{ fontSize: '12px', color: 'var(--nukrop-text-muted)', textTransform: 'uppercase', fontWeight: '600' }}>OpenFarm Crops</span>
            </div>
            <div className="stat-divider" style={{ width: '1px', height: '36px', background: 'rgba(255,255,255,0.1)' }}></div>
            
            <div className="stat-item" style={{ textAlign: 'center' }}>
              <strong style={{ fontSize: 'clamp(20px, 3vw, 28px)', color: 'var(--nukrop-accent)', display: 'block' }}>1,400+</strong>
              <span style={{ fontSize: '12px', color: 'var(--nukrop-text-muted)', textTransform: 'uppercase', fontWeight: '600' }}>APMC Mandis Synced</span>
            </div>
            <div className="stat-divider" style={{ width: '1px', height: '36px', background: 'rgba(255,255,255,0.1)' }}></div>
            
            <div className="stat-item" style={{ textAlign: 'center' }}>
              <strong style={{ fontSize: 'clamp(20px, 3vw, 28px)', color: '#FFFFFF', display: 'block' }}>11</strong>
              <span style={{ fontSize: '12px', color: 'var(--nukrop-text-muted)', textTransform: 'uppercase', fontWeight: '600' }}>Indian Languages</span>
            </div>
            <div className="stat-divider" style={{ width: '1px', height: '36px', background: 'rgba(255,255,255,0.1)' }}></div>

            <div className="stat-item" style={{ textAlign: 'center' }}>
              <strong style={{ fontSize: 'clamp(20px, 3vw, 28px)', color: '#10B981', display: 'block' }}>100%</strong>
              <span style={{ fontSize: '12px', color: 'var(--nukrop-text-muted)', textTransform: 'uppercase', fontWeight: '600' }}>Single-Lang Purity</span>
            </div>
          </div>

        </section>


        {/* ═════════════════ 15-SCREEN EMULATOR GALLERY ═════════════════ */}
        <section id="showcase" className="site-container section-spacing">
          <div style={{ textAlign: 'center', marginBottom: '32px' }}>
            <div style={{ display: 'inline-flex', padding: '5px 14px', background: 'rgba(200, 232, 55, 0.08)', borderRadius: '100px', border: '1px solid rgba(200, 232, 55, 0.2)', marginBottom: '12px' }}>
              <span style={{ fontSize: '12px', fontWeight: '700', color: 'var(--nukrop-accent)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                Pixel 7 Android 14 Emulator Verified
              </span>
            </div>
            <h2 style={{ fontSize: 'clamp(26px, 4vw, 36px)', color: '#FFFFFF', fontWeight: '800', marginBottom: '10px' }}>
              15-Screen High-Definition App Gallery
            </h2>
            <p style={{ color: 'var(--nukrop-text-dim)', fontSize: '16px', maxWidth: '680px', margin: '0 auto 24px auto' }}>
              Direct captures from the Android Mobile Emulator (412 × 915 viewport at 2.0x DPR) demonstrating 100% single-language purity and real-time logistics.
            </p>

            {/* Category Filter Pills */}
            <div style={{ display: 'flex', gap: '8px', justifyContent: 'center', flexWrap: 'wrap' }}>
              {[
                { key: 'all', label: 'All 15 Screens' },
                { key: 'onboarding', label: 'Onboarding & Perms' },
                { key: 'farmer', label: 'Farmer Hub' },
                { key: 'logistics', label: 'GramHaul Logistics' },
                { key: 'driver', label: 'Driver Cockpit' }
              ].map(c => (
                <button
                  key={c.key}
                  onClick={() => setActiveCategory(c.key as any)}
                  style={{
                    padding: '8px 18px',
                    borderRadius: '100px',
                    fontSize: '13px',
                    fontWeight: '700',
                    cursor: 'pointer',
                    border: activeCategory === c.key ? '1px solid var(--nukrop-accent)' : '1px solid rgba(255,255,255,0.1)',
                    background: activeCategory === c.key ? 'rgba(200, 232, 55, 0.15)' : 'rgba(255,255,255,0.03)',
                    color: activeCategory === c.key ? 'var(--nukrop-accent)' : '#94A3B8',
                    transition: 'all 0.2s ease'
                  }}
                >
                  {c.label}
                </button>
              ))}
            </div>
          </div>

          {/* Screenshot Grid */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))',
            gap: '20px',
          }}>
            {filteredScreenshots.map((s) => (
              <div 
                key={s.id}
                className="glass-card"
                style={{
                  borderRadius: '18px',
                  overflow: 'hidden',
                  cursor: 'pointer',
                  padding: 0,
                  transition: 'transform 0.2s ease, box-shadow 0.2s ease',
                  border: '1px solid rgba(255,255,255,0.08)'
                }}
                onClick={() => setSelectedScreenshot(s.file)}
              >
                <div style={{ height: '360px', background: '#0F172A', overflow: 'hidden', position: 'relative' }}>
                  <img 
                    src={s.file} 
                    alt={s.title} 
                    loading="lazy"
                    style={{ width: '100%', height: '100%', objectFit: 'cover', objectPosition: 'top' }} 
                  />
                  <div style={{
                    position: 'absolute',
                    top: '12px',
                    right: '12px',
                    background: 'rgba(0,0,0,0.6)',
                    backdropFilter: 'blur(8px)',
                    color: 'var(--nukrop-accent)',
                    padding: '4px 10px',
                    borderRadius: '8px',
                    fontSize: '11px',
                    fontWeight: '800'
                  }}>
                    Screen {s.id}
                  </div>
                </div>
                <div style={{ padding: '16px' }}>
                  <h3 style={{ fontSize: '15.5px', color: '#FFFFFF', fontWeight: '800', marginBottom: '6px' }}>{s.title}</h3>
                  <p style={{ color: 'var(--nukrop-text-dim)', fontSize: '12.5px', lineHeight: 1.5, margin: 0 }}>{s.desc}</p>
                </div>
              </div>
            ))}
          </div>

          {/* Lightbox Modal */}
          {selectedScreenshot && (
            <div 
              style={{
                position: 'fixed',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                background: 'rgba(0,0,0,0.85)',
                backdropFilter: 'blur(12px)',
                zIndex: 9999,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                padding: '20px'
              }}
              onClick={() => setSelectedScreenshot(null)}
            >
              <div style={{ maxWidth: '440px', maxHeight: '90vh', position: 'relative' }} onClick={e => e.stopPropagation()}>
                <img 
                  src={selectedScreenshot} 
                  alt="Enlarged Screen" 
                  style={{ width: '100%', maxHeight: '85vh', objectFit: 'contain', borderRadius: '24px', boxShadow: '0 20px 60px rgba(0,0,0,0.8)', border: '2px solid rgba(255,255,255,0.15)' }} 
                />
                <button 
                  onClick={() => setSelectedScreenshot(null)}
                  style={{
                    position: 'absolute',
                    top: '-16px',
                    right: '-16px',
                    width: '36px',
                    height: '36px',
                    borderRadius: '50%',
                    background: '#FFFFFF',
                    border: 'none',
                    color: '#000000',
                    fontSize: '18px',
                    fontWeight: 'bold',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                  }}
                >
                  ✕
                </button>
              </div>
            </div>
          )}
        </section>


        {/* ═════════════════ 6 CORE FARMING PILLARS ═════════════════ */}
        <section id="features" className="site-container section-spacing">
          <div style={{ textAlign: 'center', marginBottom: '36px' }}>
            <h2 style={{ fontSize: 'clamp(26px, 4vw, 36px)', color: '#FFFFFF', fontWeight: '800', marginBottom: '10px' }}>
              6 Core Agrarian Pillars
            </h2>
            <p style={{ color: 'var(--nukrop-text-dim)', fontSize: '16px', maxWidth: '650px', margin: '0 auto' }}>
              Built specifically to handle the toughest field conditions with 100% single-language vernacular UI.
            </p>
          </div>

          <div className="grid-3col">
            
            {/* Feature 1: AI Scanner */}
            <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column' }}>
              <div style={{ width: '44px', height: '44px', borderRadius: '12px', background: 'rgba(200, 232, 55, 0.12)', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '16px' }}>
                <ScanLine style={{ color: 'var(--nukrop-accent)', width: '22px', height: '22px' }} />
              </div>
              <h3 style={{ fontSize: '18px', color: '#FFFFFF', marginBottom: '8px', fontWeight: '800' }}>AI Crop Doctor</h3>
              <p style={{ color: 'var(--nukrop-text-dim)', fontSize: '13.5px', lineHeight: 1.6, margin: 0 }}>
                Point your camera at any diseased leaf. High-resolution vision diagnosis detects 600+ pathologies and calculates exact ICAR chemical and organic BioRx mixing dosages.
              </p>
            </div>

            {/* Feature 2: Mandi Rates */}
            <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column' }}>
              <div style={{ width: '44px', height: '44px', borderRadius: '12px', background: 'rgba(34, 197, 94, 0.12)', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '16px' }}>
                <TrendingUp style={{ color: '#22C55E', width: '22px', height: '22px' }} />
              </div>
              <h3 style={{ fontSize: '18px', color: '#FFFFFF', marginBottom: '8px', fontWeight: '800' }}>Live Mandi Intelligence</h3>
              <p style={{ color: 'var(--nukrop-text-dim)', fontSize: '13.5px', lineHeight: 1.6, margin: 0 }}>
                Real-time Agmarknet prices across 1,400+ APMC yards. Compare modal prices, track 7-day volatility trends, and set threshold alerts before dispatch.
              </p>
            </div>

            {/* Feature 3: GramHaul */}
            <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column' }}>
              <div style={{ width: '44px', height: '44px', borderRadius: '12px', background: 'rgba(245, 158, 11, 0.12)', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '16px' }}>
                <Truck style={{ color: '#F59E0B', width: '22px', height: '22px' }} />
              </div>
              <h3 style={{ fontSize: '18px', color: '#FFFFFF', marginBottom: '8px', fontWeight: '800' }}>GramHaul Pooled Logistics</h3>
              <p style={{ color: 'var(--nukrop-text-dim)', fontSize: '13.5px', lineHeight: 1.6, margin: 0 }}>
                40% viewport Leaflet OSM map with moving GPS commercial trucks. Pooled farm-to-mandi dispatch for Tata Ace, Bolero Maxi, and Eicher Canter.
              </p>
            </div>

            {/* Feature 4: AgriStack */}
            <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column' }}>
              <div style={{ width: '44px', height: '44px', borderRadius: '12px', background: 'rgba(168, 85, 247, 0.12)', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '16px' }}>
                <Landmark style={{ color: '#A855F7', width: '22px', height: '22px' }} />
              </div>
              <h3 style={{ fontSize: '18px', color: '#FFFFFF', marginBottom: '8px', fontWeight: '800' }}>AgriStack & Land Records</h3>
              <p style={{ color: 'var(--nukrop-text-dim)', fontSize: '13.5px', lineHeight: 1.6, margin: 0 }}>
                National digital farmer passport, digital RoR-1B, Pattadar Passbook, Dharani survey number search, and pre-approved KCC loan limits.
              </p>
            </div>

            {/* Feature 5: Hyperlocal Weather */}
            <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column' }}>
              <div style={{ width: '44px', height: '44px', borderRadius: '12px', background: 'rgba(59, 130, 246, 0.12)', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '16px' }}>
                <CloudRain style={{ color: '#3B82F6', width: '22px', height: '22px' }} />
              </div>
              <h3 style={{ fontSize: '18px', color: '#FFFFFF', marginBottom: '8px', fontWeight: '800' }}>Hyperlocal Weather & Radar</h3>
              <p style={{ color: 'var(--nukrop-text-dim)', fontSize: '13.5px', lineHeight: 1.6, margin: 0 }}>
                Precipitation probabilities, humidity tracking, and spray advisory indicators warning if high wind speeds make spraying ineffective.
              </p>
            </div>

            {/* Feature 6: BioShield */}
            <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column' }}>
              <div style={{ width: '44px', height: '44px', borderRadius: '12px', background: 'rgba(239, 68, 68, 0.12)', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '16px' }}>
                <ShieldCheck style={{ color: '#EF4444', width: '22px', height: '22px' }} />
              </div>
              <h3 style={{ fontSize: '18px', color: '#FFFFFF', marginBottom: '8px', fontWeight: '800' }}>BioShield Pest Radar</h3>
              <p style={{ color: 'var(--nukrop-text-dim)', fontSize: '13.5px', lineHeight: 1.6, margin: 0 }}>
                Autonomous early-warning radar aggregating regional pheromone trap captures across Telangana and Andhra Pradesh with meteorological vector modeling.
              </p>
            </div>

          </div>
        </section>


        {/* ═════════════════ OFFICIAL DOWNLOAD SECTION ═════════════════ */}
        <section id="download" className="site-container section-spacing">
          <div className="glass-card" style={{ 
            padding: 'clamp(28px, 5vw, 56px)', 
            borderRadius: '24px', 
            border: '1.5px solid var(--nukrop-accent)',
            background: 'linear-gradient(180deg, rgba(200, 232, 55, 0.05) 0%, rgba(5, 8, 3, 0.95) 100%)',
            boxShadow: '0 20px 60px rgba(0,0,0,0.6)'
          }}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '36px', alignItems: 'center' }}>
              
              {/* Left Column: Release Details */}
              <div>
                <div style={{ display: 'inline-flex', padding: '6px 14px', background: 'rgba(200, 232, 55, 0.15)', borderRadius: '100px', border: '1px solid var(--nukrop-accent)', marginBottom: '16px' }}>
                  <span style={{ fontSize: '12px', fontWeight: '800', color: 'var(--nukrop-accent)', textTransform: 'uppercase' }}>Official Release Build</span>
                </div>
                <h2 style={{ fontSize: 'clamp(28px, 4vw, 42px)', color: '#FFFFFF', fontWeight: '900', lineHeight: 1.15, marginBottom: '16px' }}>
                  NuKropAI Android Release APK
                </h2>
                <p style={{ color: 'var(--nukrop-text-dim)', fontSize: '15px', lineHeight: 1.6, marginBottom: '24px' }}>
                  Download the official production package directly to your Android device. Verified virus-free, telemetry-secured, and fully functional offline.
                </p>

                {/* Specs Table */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginBottom: '28px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 14px', background: 'rgba(255,255,255,0.03)', borderRadius: '10px', fontSize: '13px' }}>
                    <span style={{ color: 'var(--nukrop-text-muted)' }}>Current Release:</span>
                    <strong style={{ color: '#FFFFFF' }}>v2.4 Production Engine</strong>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 14px', background: 'rgba(255,255,255,0.03)', borderRadius: '10px', fontSize: '13px' }}>
                    <span style={{ color: 'var(--nukrop-text-muted)' }}>APK File Size:</span>
                    <strong style={{ color: '#FFFFFF' }}>49.4 MB (51,797,812 bytes)</strong>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 14px', background: 'rgba(255,255,255,0.03)', borderRadius: '10px', fontSize: '13px' }}>
                    <span style={{ color: 'var(--nukrop-text-muted)' }}>Minimum Android Version:</span>
                    <strong style={{ color: '#FFFFFF' }}>Android 8.0+ (Oreo through 14+)</strong>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 14px', background: 'rgba(255,255,255,0.03)', borderRadius: '10px', fontSize: '13px' }}>
                    <span style={{ color: 'var(--nukrop-text-muted)' }}>Release Date:</span>
                    <strong style={{ color: '#FFFFFF' }}>October 2026</strong>
                  </div>
                </div>

                {/* SHA-256 Checksum Verification Box */}
                <div style={{ padding: '14px', background: 'rgba(0,0,0,0.4)', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.08)', marginBottom: '28px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                    <span style={{ fontSize: '11px', color: 'var(--nukrop-text-muted)', textTransform: 'uppercase', fontWeight: '700' }}>SHA-256 Checksum</span>
                    <button 
                      onClick={copyHashToClipboard}
                      style={{ background: 'none', border: 'none', color: copiedHash ? '#22C55E' : 'var(--nukrop-accent)', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px', fontSize: '11px', fontWeight: '700' }}
                    >
                      {copiedHash ? <CheckCircle style={{ width: '12px', height: '12px' }} /> : <Copy style={{ width: '12px', height: '12px' }} />}
                      <span>{copiedHash ? 'Copied!' : 'Copy Hash'}</span>
                    </button>
                  </div>
                  <code style={{ fontSize: '11px', color: '#CBD5E1', wordBreak: 'break-all', fontFamily: 'monospace' }}>
                    {apkSha256}
                  </code>
                </div>

                {/* Primary Download Button */}
                <a
                  href="/NuKropAI.apk"
                  download="NuKropAI.apk"
                  className="nukrop-btn"
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '12px',
                    width: '100%',
                    padding: '18px 28px',
                    fontSize: '16px',
                    borderRadius: '16px',
                    boxShadow: '0 8px 30px rgba(200, 232, 55, 0.4)',
                    textDecoration: 'none'
                  }}
                >
                  <Download style={{ width: '22px', height: '22px' }} />
                  <span>Download NuKropAI APK (49.4 MB)</span>
                </a>
              </div>

              {/* Right Column: Step-by-Step Installation Guide */}
              <div style={{ background: 'rgba(255,255,255,0.02)', padding: '28px', borderRadius: '20px', border: '1px solid rgba(255,255,255,0.06)' }}>
                <h3 style={{ fontSize: '18px', color: '#FFFFFF', fontWeight: '800', marginBottom: '18px' }}>
                  Quick Sideload Installation Guide
                </h3>
                
                <div style={{ display: 'flex', flexDirection: 'column', gap: '18px' }}>
                  <div style={{ display: 'flex', gap: '14px' }}>
                    <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: 'var(--nukrop-accent)', color: '#000000', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: '900', fontSize: '14px', flexShrink: 0 }}>
                      1
                    </div>
                    <div>
                      <strong style={{ color: '#FFFFFF', fontSize: '14.5px', display: 'block' }}>Download the APK</strong>
                      <span style={{ color: 'var(--nukrop-text-dim)', fontSize: '12.5px', lineHeight: 1.5 }}>
                        Tap the download button above. Your browser will download the 49.4 MB official release file.
                      </span>
                    </div>
                  </div>

                  <div style={{ display: 'flex', gap: '14px' }}>
                    <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: 'var(--nukrop-accent)', color: '#000000', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: '900', fontSize: '14px', flexShrink: 0 }}>
                      2
                    </div>
                    <div>
                      <strong style={{ color: '#FFFFFF', fontSize: '14.5px', display: 'block' }}>Allow Unknown Sources</strong>
                      <span style={{ color: 'var(--nukrop-text-dim)', fontSize: '12.5px', lineHeight: 1.5 }}>
                        When opening the downloaded file, if Android prompts with "Install unknown apps", tap Settings and toggle "Allow from this source".
                      </span>
                    </div>
                  </div>

                  <div style={{ display: 'flex', gap: '14px' }}>
                    <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: 'var(--nukrop-accent)', color: '#000000', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: '900', fontSize: '14px', flexShrink: 0 }}>
                      3
                    </div>
                    <div>
                      <strong style={{ color: '#FFFFFF', fontSize: '14.5px', display: 'block' }}>Select Language & Begin</strong>
                      <span style={{ color: 'var(--nukrop-text-dim)', fontSize: '12.5px', lineHeight: 1.5 }}>
                        Launch NuKropAI, choose your preferred language (Telugu, Hindi, etc.), select your crops, and enjoy 100% sovereign farming intelligence.
                      </span>
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </section>


        {/* ═════════════════ FAQ ACCORDION ═════════════════ */}
        <section id="faq" className="site-container section-spacing">
          <div style={{ textAlign: 'center', marginBottom: '36px' }}>
            <h2 style={{ fontSize: 'clamp(26px, 4vw, 36px)', color: '#FFFFFF', fontWeight: '800', marginBottom: '10px' }}>
              Frequently Asked Questions
            </h2>
            <p style={{ color: 'var(--nukrop-text-dim)', fontSize: '16px', maxWidth: '650px', margin: '0 auto' }}>
              Everything you need to know about installing, deploying, and using NuKropAI.
            </p>
          </div>

          <div style={{ maxWidth: '820px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {faqs.map((faq, index) => {
              const isOpen = openFaq === index;
              return (
                <div 
                  key={index} 
                  className="glass-card" 
                  style={{ 
                    borderRadius: '14px', 
                    cursor: 'pointer',
                    borderColor: isOpen ? 'var(--nukrop-border-accent)' : 'var(--nukrop-border)'
                  }}
                  onClick={() => setOpenFaq(isOpen ? null : index)}
                >
                  <div style={{ padding: '18px 22px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '16px' }}>
                    <span style={{ fontSize: '15.5px', fontWeight: '700', color: isOpen ? 'var(--nukrop-accent)' : '#FFFFFF' }}>
                      {faq.q}
                    </span>
                    <ChevronDown style={{ 
                      width: '18px', 
                      height: '18px', 
                      color: isOpen ? 'var(--nukrop-accent)' : 'var(--nukrop-text-muted)',
                      transform: isOpen ? 'rotate(180deg)' : 'rotate(0deg)',
                      transition: 'transform 0.2s ease',
                      flexShrink: 0
                    }} />
                  </div>
                  {isOpen && (
                    <div style={{ padding: '0 22px 20px 22px', color: 'var(--nukrop-text-dim)', fontSize: '14px', lineHeight: 1.6, borderTop: '1px solid rgba(255,255,255,0.05)', paddingTop: '14px' }}>
                      {faq.a}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </section>

      </main>

      {/* ── BALANCED & STRUCTURED FOOTER ── */}
      <footer style={{ 
        padding: '56px 0 32px 0', 
        borderTop: '1px solid rgba(255,255,255,0.08)', 
        background: 'rgba(5, 8, 3, 0.95)', 
        position: 'relative', 
        zIndex: 10 
      }}>
        <div className="site-container footer-container">
          
          {/* Top Row Grid */}
          <div className="footer-top-row">
            
            {/* Column 1: Brand & Mission */}
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '14px' }}>
                <div style={{ padding: '6px', background: 'rgba(200, 232, 55, 0.12)', borderRadius: '8px', border: '1px solid rgba(200, 232, 55, 0.25)' }}>
                  <Sprout style={{ color: 'var(--nukrop-accent)', width: '20px', height: '20px' }} />
                </div>
                <span style={{ fontSize: '20px', fontFamily: 'Outfit', fontWeight: '800', color: '#FFFFFF' }}>
                  NuKrop<span style={{ color: 'var(--nukrop-accent)' }}>AI</span>
                </span>
              </div>
              <p style={{ fontSize: '13.5px', color: 'var(--nukrop-text-dim)', lineHeight: 1.6, maxWidth: '380px', margin: '0 0 16px 0' }}>
                Sovereign full-stack Agrarian Operating System designed to empower Indian farmers with edge AI pathology diagnostics, unmanipulated APMC market rates, and pooled rural logistics.
              </p>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--nukrop-text-muted)', fontSize: '12px' }}>
                <Radio style={{ width: '13px', height: '13px', color: '#22C55E' }} />
                <span>ICAR & Agmarknet Government Protocol Compliant</span>
              </div>
            </div>

            {/* Column 2: Quick Links */}
            <div>
              <h4 style={{ fontSize: '14px', color: '#FFFFFF', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '16px' }}>
                Platform
              </h4>
              <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '10px' }}>
                <li><a href="#features" style={{ color: 'var(--nukrop-text-dim)', textDecoration: 'none', fontSize: '13.5px' }}>6 Core Pillars</a></li>
                <li><a href="#showcase" style={{ color: 'var(--nukrop-text-dim)', textDecoration: 'none', fontSize: '13.5px' }}>15-Screen Gallery</a></li>
                <li><a href="#download" style={{ color: 'var(--nukrop-accent)', textDecoration: 'none', fontSize: '13.5px', fontWeight: '700' }}>Download APK (v2.4)</a></li>
                <li><a href="#faq" style={{ color: 'var(--nukrop-text-dim)', textDecoration: 'none', fontSize: '13.5px' }}>FAQ & Manual</a></li>
                <li><button onClick={() => setShowPrivacyModal(true)} style={{ background: 'none', border: 'none', padding: 0, color: 'var(--nukrop-text-dim)', cursor: 'pointer', fontSize: '13.5px', textAlign: 'left' }}>Privacy Policy (DPDPA 2023)</button></li>
                <li><button onClick={() => setShowTermsModal(true)} style={{ background: 'none', border: 'none', padding: 0, color: 'var(--nukrop-text-dim)', cursor: 'pointer', fontSize: '13.5px', textAlign: 'left' }}>Terms of Service</button></li>
              </ul>
            </div>

            {/* Column 3: Live System Infrastructure Status */}
            <div>
              <h4 style={{ fontSize: '14px', color: '#FFFFFF', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '16px' }}>
                Infrastructure Status
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '8px 12px', background: 'rgba(255,255,255,0.03)', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.06)' }}>
                  <span className="live-pulse" style={{ width: '6px', height: '6px' }}></span>
                  <span style={{ fontSize: '12px', color: 'var(--nukrop-text)' }}>Supabase V5 Cloud Grid: <strong>Operational</strong></span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '8px 12px', background: 'rgba(255,255,255,0.03)', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.06)' }}>
                  <span className="live-pulse" style={{ width: '6px', height: '6px' }}></span>
                  <span style={{ fontSize: '12px', color: 'var(--nukrop-text)' }}>Supabase Edge Functions: <strong>Active</strong></span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '8px 12px', background: 'rgba(255,255,255,0.03)', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.06)' }}>
                  <span className="live-pulse" style={{ width: '6px', height: '6px' }}></span>
                  <span style={{ fontSize: '12px', color: 'var(--nukrop-text)' }}>Agmarknet APMC Sync: <strong>100%</strong></span>
                </div>
              </div>
            </div>

          </div>

          {/* Bottom Row Divider & Centered Copyright */}
          <div className="footer-bottom-row">
            <p style={{ color: 'var(--nukrop-text-muted)', fontSize: '13px', margin: 0 }}>
              © 2026 NuKropAI by B. JASWANTH REDDY. All rights reserved.
            </p>
            <p style={{ color: 'var(--nukrop-text-dim)', fontSize: '13px', margin: 0 }}>
              Built with ❤️ for Indian Farmers.
            </p>
          </div>

        </div>
      </footer>

      {/* ── PRIVACY POLICY MODAL ── */}
      {showPrivacyModal && (
        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.85)', backdropFilter: 'blur(10px)', zIndex: 10000, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '20px' }}>
          <div className="glass-card" style={{ maxWidth: '600px', width: '100%', maxHeight: '80vh', overflowY: 'auto', padding: '32px', borderRadius: '20px', position: 'relative' }}>
            <h3 style={{ fontSize: '20px', color: '#FFFFFF', marginBottom: '16px' }}>Privacy Policy (DPDP Act 2023 Compliant)</h3>
            <p style={{ color: 'var(--nukrop-text-dim)', fontSize: '13.5px', lineHeight: 1.6 }}>
              NuKropAI is engineered under strict compliance with the Digital Personal Data Protection Act (DPDPA 2023). We believe farmer data sovereignty is non-negotiable.
            </p>
            <h4 style={{ color: '#FFFFFF', fontSize: '15px', marginTop: '16px' }}>1. Local-First Processing</h4>
            <p style={{ color: 'var(--nukrop-text-dim)', fontSize: '13.5px', lineHeight: 1.6 }}>Crop disease scans and diagnostic queries are evaluated using edge models. Your farm photos are never sold to commercial agrochemical corporations.</p>
            <h4 style={{ color: '#FFFFFF', fontSize: '15px', marginTop: '16px' }}>2. AgriStack & Land Records</h4>
            <p style={{ color: 'var(--nukrop-text-dim)', fontSize: '13.5px', lineHeight: 1.6 }}>National AgriStack ID credentials and RoR-1B records reside in your encrypted local vault. Only you can authorize instant loan sharing with certified banking institutions.</p>
            <button onClick={() => setShowPrivacyModal(false)} className="nukrop-btn" style={{ marginTop: '24px', width: '100%', padding: '12px' }}>Close</button>
          </div>
        </div>
      )}

      {/* ── TERMS OF SERVICE MODAL ── */}
      {showTermsModal && (
        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.85)', backdropFilter: 'blur(10px)', zIndex: 10000, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '20px' }}>
          <div className="glass-card" style={{ maxWidth: '600px', width: '100%', maxHeight: '80vh', overflowY: 'auto', padding: '32px', borderRadius: '20px', position: 'relative' }}>
            <h3 style={{ fontSize: '20px', color: '#FFFFFF', marginBottom: '16px' }}>Terms of Service & Agronomy Disclaimer</h3>
            <p style={{ color: 'var(--nukrop-text-dim)', fontSize: '13.5px', lineHeight: 1.6 }}>
              NuKropAI provides automated agronomic guidance based on ICAR, PJTSAU, and Agmarknet protocols.
            </p>
            <h4 style={{ color: '#FFFFFF', fontSize: '15px', marginTop: '16px' }}>1. Field Advisory</h4>
            <p style={{ color: 'var(--nukrop-text-dim)', fontSize: '13.5px', lineHeight: 1.6 }}>Recommendations are intended to aid farming operations. Local weather anomalies, soil pH, and seed quality may vary. Always follow chemical label safety guidelines.</p>
            <h4 style={{ color: '#FFFFFF', fontSize: '15px', marginTop: '16px' }}>2. GramHaul Logistics</h4>
            <p style={{ color: 'var(--nukrop-text-dim)', fontSize: '13.5px', lineHeight: 1.6 }}>GramHaul facilitates direct connection between farmers and independent commercial drivers. Fares are mutually agreed upon prior to dispatch.</p>
            <button onClick={() => setShowTermsModal(false)} className="nukrop-btn" style={{ marginTop: '24px', width: '100%', padding: '12px' }}>Close</button>
          </div>
        </div>
      )}

    </div>
  );
}
`;

fs.writeFileSync('web/src/App.tsx', updatedAppContent, 'utf8');
console.log('[PASS] Enhanced web/src/App.tsx with 15-screen gallery, verified download hub, and legal modals!');
