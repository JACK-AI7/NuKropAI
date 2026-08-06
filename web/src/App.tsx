import React from 'react';
import { Sprout, Smartphone, Apple, AlertTriangle, ShieldCheck, ChevronRight, ScanLine, TrendingUp, Landmark, CloudRain, Layers, Globe, MapPin, MessageCircle } from 'lucide-react';

export default function App() {
  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      
      {/* Background Elements */}
      <div className="dynamic-bg"></div>
      <div className="dynamic-overlay"></div>
      
      {/* Top Header */}
      <header style={{ 
        padding: '24px 40px', 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        position: 'absolute', 
        top: 0, 
        left: 0, 
        right: 0,
        zIndex: 50 
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{ padding: '8px', background: 'rgba(200, 232, 55, 0.1)', borderRadius: '12px' }}>
            <Sprout style={{ color: 'var(--nukrop-accent)', width: '28px', height: '28px' }} />
          </div>
          <span style={{ fontSize: '22px', fontFamily: 'Outfit', fontWeight: 'bold', letterSpacing: '0.02em', color: 'white' }}>NuKropAI</span>
        </div>
      </header>

      <main style={{ flex: '1', display: 'flex', flexDirection: 'column', alignItems: 'center', position: 'relative', zIndex: 10 }}>
        
        {/* Background Gradients */}
        <div style={{ position: 'absolute', top: '-10%', left: '-10%', width: '50vw', height: '50vw', background: 'radial-gradient(circle, rgba(200,232,55,0.05) 0%, transparent 70%)', zIndex: 0, pointerEvents: 'none' }}></div>
        <div style={{ position: 'absolute', bottom: '-10%', right: '-10%', width: '50vw', height: '50vw', background: 'radial-gradient(circle, rgba(46,90,28,0.1) 0%, transparent 70%)', zIndex: 0, pointerEvents: 'none' }}></div>

        {/* Hero Section */}
        <section style={{ width: '100%', maxWidth: '1200px', padding: '140px 24px 60px 24px', display: 'flex', flexDirection: 'column', alignItems: 'center', zIndex: 1 }} className="fade-in">
          <div style={{ padding: '6px 16px', background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.05)', borderRadius: '100px', marginBottom: '32px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ width: '8px', height: '8px', background: 'var(--nukrop-accent)', borderRadius: '50%', boxShadow: '0 0 10px var(--nukrop-accent)' }}></span>
            <span style={{ fontSize: '13px', color: 'var(--nukrop-text-muted)', fontWeight: '600', letterSpacing: '0.05em', textTransform: 'uppercase' }}>The Future of Indian Agriculture</span>
          </div>

          <h1 style={{ fontSize: 'clamp(48px, 6vw, 72px)', textAlign: 'center', lineHeight: 1.1, marginBottom: '24px', fontWeight: '800', color: 'white' }}>
            Agrarian Intelligence, <br/>
            <span style={{ 
              background: 'linear-gradient(135deg, var(--nukrop-accent) 0%, #D4F040 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}>
              Now in your pocket.
            </span>
          </h1>

          <p style={{ fontSize: 'clamp(18px, 2vw, 22px)', color: 'var(--nukrop-text-dim)', textAlign: 'center', maxWidth: '700px', lineHeight: 1.6, marginBottom: '60px' }}>
            A complete operating system engineered to eliminate crop loss and ensure fair market pricing through edge AI and live government data.
          </p>

        </section>

        {/* Problem / Solution Split */}
        <section style={{ width: '100%', maxWidth: '1200px', padding: '0 24px 80px 24px', zIndex: 1, display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '32px' }}>
          
          {/* Problem Card */}
          <div className="glass-card animate-float" style={{ padding: '40px' }}>
            <div style={{ width: '48px', height: '48px', background: 'rgba(239, 68, 68, 0.1)', borderRadius: '14px', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '24px' }}>
              <AlertTriangle style={{ color: 'var(--nukrop-error)', width: '24px', height: '24px' }} />
            </div>
            <h2 style={{ fontSize: '24px', color: 'white', marginBottom: '16px' }}>The Core Problem</h2>
            <p style={{ fontSize: '16px', color: 'var(--nukrop-text-dim)', lineHeight: 1.7 }}>
              Indian farmers lose up to <strong>40% of their yields</strong> to undiagnosed crop diseases. Meanwhile, predatory middlemen hide real market prices, and billions in government subsidies go unclaimed due to a lack of technical access. The agricultural sector is being left behind in the digital age.
            </p>
          </div>

          {/* Solution Card */}
          <div className="glass-card animate-float-delayed" style={{ padding: '40px' }}>
            <div style={{ width: '48px', height: '48px', background: 'linear-gradient(135deg, var(--nukrop-accent) 0%, var(--nukrop-accent-dark) 100%)', borderRadius: '14px', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '24px', boxShadow: '0 8px 24px rgba(200, 232, 55, 0.2)' }}>
              <ShieldCheck style={{ color: 'var(--nukrop-dark)', width: '24px', height: '24px' }} />
            </div>
            <h2 style={{ fontSize: '24px', color: 'white', marginBottom: '16px' }}>The NuKropAI Solution</h2>
            <p style={{ fontSize: '16px', color: 'var(--nukrop-text-dim)', lineHeight: 1.7 }}>
              NuKropAI puts a supercomputer in every farmer's hands. Snap a photo to instantly diagnose diseases with <strong>99.9% Llama 3.2 Vision AI accuracy</strong>. View live, unmanipulated Mandi prices directly from the Government of India, and auto-match your farm with missing subsidies instantly.
            </p>
          </div>

        </section>

        {/* Feature Showcase Section */}
        <section style={{ width: '100%', maxWidth: '1200px', padding: '0 24px 80px 24px', zIndex: 1, display: 'flex', flexDirection: 'column', gap: '32px' }}>
          
          <div style={{ textAlign: 'center', marginBottom: '24px' }}>
            <h2 style={{ fontSize: '32px', color: 'white', fontWeight: 'bold' }}>Unmatched Capabilities</h2>
            <p style={{ color: 'var(--nukrop-text-dim)', fontSize: '18px' }}>The tools you need to maximize your harvest.</p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '32px' }}>
            
            {/* Feature 1: AI Scanner */}
            <div className="glass-card" style={{ overflow: 'hidden', padding: 0, display: 'flex', flexDirection: 'column' }}>
              <div style={{ height: '220px', backgroundImage: 'url("/feature_scan.jpg")', backgroundSize: 'cover', backgroundPosition: 'center', borderBottom: '1px solid rgba(255,255,255,0.1)' }}></div>
              <div style={{ padding: '28px' }}>
                <h3 style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '18px', color: 'white', marginBottom: '10px' }}>
                  <ScanLine style={{ color: 'var(--nukrop-accent)', width: '22px', height: '22px', flexShrink: 0 }} />
                  AI Crop Scanning
                </h3>
                <p style={{ color: 'var(--nukrop-text-dim)', fontSize: '14px', lineHeight: 1.6 }}>
                  Point your camera at any crop leaf. Llama 3.2 Vision AI instantly diagnoses diseases, pests, and nutrient deficiencies with exact treatment dosages.
                </p>
              </div>
            </div>

            {/* Feature 2: Mandi Prices */}
            <div className="glass-card" style={{ overflow: 'hidden', padding: 0, display: 'flex', flexDirection: 'column' }}>
              <div style={{ height: '220px', backgroundImage: 'url("/feature_mandi.jpg")', backgroundSize: 'cover', backgroundPosition: 'center', borderBottom: '1px solid rgba(255,255,255,0.1)' }}></div>
              <div style={{ padding: '28px' }}>
                <h3 style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '18px', color: 'white', marginBottom: '10px' }}>
                  <TrendingUp style={{ color: '#D4F040', width: '22px', height: '22px', flexShrink: 0 }} />
                  Live Mandi Rates
                  <span style={{ display: 'inline-flex', alignItems: 'center', gap: '4px', fontSize: '11px', color: 'var(--nukrop-accent)', background: 'rgba(200,232,55,0.1)', padding: '2px 8px', borderRadius: '100px' }}><MapPin style={{ width: '10px', height: '10px' }} />Location Based</span>
                </h3>
                <p style={{ color: 'var(--nukrop-text-dim)', fontSize: '14px', lineHeight: 1.6 }}>
                  Fetches real-time commodity prices from your nearest Mandi using GPS and the Government of India's live API. No middlemen, no hidden rates.
                </p>
              </div>
            </div>

            {/* Feature 3: Subsidy Matcher */}
            <div className="glass-card" style={{ overflow: 'hidden', padding: 0, display: 'flex', flexDirection: 'column' }}>
              <div style={{ height: '220px', backgroundImage: 'url("/feature_subsidy.jpg")', backgroundSize: 'cover', backgroundPosition: 'center', borderBottom: '1px solid rgba(255,255,255,0.1)' }}></div>
              <div style={{ padding: '28px' }}>
                <h3 style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '18px', color: 'white', marginBottom: '10px' }}>
                  <Landmark style={{ color: '#64B5F6', width: '22px', height: '22px', flexShrink: 0 }} />
                  Loan & Subsidy Finder
                </h3>
                <p style={{ color: 'var(--nukrop-text-dim)', fontSize: '14px', lineHeight: 1.6 }}>
                  AI scans thousands of Central & State government schemes and auto-matches subsidies and loans you're eligible for based on your farm profile.
                </p>
              </div>
            </div>

            {/* Feature 4: Weather Alerts */}
            <div className="glass-card" style={{ overflow: 'hidden', padding: 0, display: 'flex', flexDirection: 'column' }}>
              <div style={{ height: '220px', backgroundImage: 'url("/feature_weather.jpg")', backgroundSize: 'cover', backgroundPosition: 'center', borderBottom: '1px solid rgba(255,255,255,0.1)' }}></div>
              <div style={{ padding: '28px' }}>
                <h3 style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '18px', color: 'white', marginBottom: '10px' }}>
                  <CloudRain style={{ color: '#F59E0B', width: '22px', height: '22px', flexShrink: 0 }} />
                  Weather Alerts
                  <span style={{ display: 'inline-flex', alignItems: 'center', gap: '4px', fontSize: '11px', color: '#F59E0B', background: 'rgba(245,158,11,0.1)', padding: '2px 8px', borderRadius: '100px' }}><MapPin style={{ width: '10px', height: '10px' }} />Location Based</span>
                </h3>
                <p style={{ color: 'var(--nukrop-text-dim)', fontSize: '14px', lineHeight: 1.6 }}>
                  Hyperlocal weather forecasts and real-time storm, frost, and heatwave alerts sent directly to your phone based on your exact GPS location.
                </p>
              </div>
            </div>

            {/* Feature 5: Soil Scanner */}
            <div className="glass-card" style={{ overflow: 'hidden', padding: 0, display: 'flex', flexDirection: 'column' }}>
              <div style={{ height: '220px', backgroundImage: 'url("/feature_soil.jpg")', backgroundSize: 'cover', backgroundPosition: 'center', borderBottom: '1px solid rgba(255,255,255,0.1)' }}></div>
              <div style={{ padding: '28px' }}>
                <h3 style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '18px', color: 'white', marginBottom: '10px' }}>
                  <Layers style={{ color: '#A78BFA', width: '22px', height: '22px', flexShrink: 0 }} />
                  AI Soil Scanner
                </h3>
                <p style={{ color: 'var(--nukrop-text-dim)', fontSize: '14px', lineHeight: 1.6 }}>
                  Photograph your soil sample and receive a detailed AI-powered analysis of pH, nitrogen, phosphorus, and potassium levels with fertilizer recommendations.
                </p>
              </div>
            </div>

            {/* Feature 6: AI Advisor */}
            <div className="glass-card" style={{ overflow: 'hidden', padding: 0, display: 'flex', flexDirection: 'column' }}>
              <div style={{ height: '220px', backgroundImage: 'url("/feature_advisor.jpg")', backgroundSize: 'cover', backgroundPosition: 'center', borderBottom: '1px solid rgba(255,255,255,0.1)' }}></div>
              <div style={{ padding: '28px' }}>
                <h3 style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '18px', color: 'white', marginBottom: '10px' }}>
                  <MessageCircle style={{ color: '#34D399', width: '22px', height: '22px', flexShrink: 0 }} />
                  AI Farm Advisor
                </h3>
                <p style={{ color: 'var(--nukrop-text-dim)', fontSize: '14px', lineHeight: 1.6 }}>
                  Ask any farming question in your language. Our Llama-powered AI advisor provides expert guidance on crop rotation, pest control, irrigation, and best practices 24/7.
                </p>
              </div>
            </div>
            
          </div>
        </section>

        {/* Multi-Language Support Section */}
        <section style={{ width: '100%', maxWidth: '1200px', padding: '0 24px 80px 24px', zIndex: 1 }}>
          <div className="glass-card" style={{ padding: '48px 40px', textAlign: 'center' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '12px', marginBottom: '20px' }}>
              <Globe style={{ color: 'var(--nukrop-accent)', width: '32px', height: '32px' }} />
              <h2 style={{ fontSize: '28px', color: 'white', fontWeight: 'bold' }}>Available in Your Language</h2>
            </div>
            <p style={{ color: 'var(--nukrop-text-dim)', fontSize: '16px', lineHeight: 1.6, maxWidth: '700px', margin: '0 auto 32px auto' }}>
              Every feature — AI scanning, Mandi prices, subsidies, weather alerts, and soil analysis — is fully available in all major Indian languages. Use the app the way you think.
            </p>
            <div style={{ display: 'flex', gap: '16px', justifyContent: 'center', flexWrap: 'wrap' }}>
              {['English', 'हिन्दी', 'తెలుగు', 'தமிழ்', 'मराठी'].map((lang) => (
                <span key={lang} style={{ padding: '10px 24px', background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '12px', color: 'white', fontSize: '16px', fontWeight: '600' }}>{lang}</span>
              ))}
            </div>
          </div>
        </section>

        {/* Download Hub */}
        <section style={{ width: '100%', maxWidth: '1200px', padding: '0 24px 80px 24px', zIndex: 1 }}>
          <div style={{ 
            background: 'linear-gradient(180deg, rgba(200, 232, 55, 0.08) 0%, rgba(200, 232, 55, 0.02) 100%)', 
            border: '1px solid rgba(200, 232, 55, 0.15)',
            borderRadius: '24px', 
            padding: '60px 40px',
            textAlign: 'center',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center'
          }}>
            <h2 style={{ fontSize: '36px', color: 'white', marginBottom: '16px', fontWeight: '700' }}>Start your digital farm today.</h2>
            <p style={{ fontSize: '18px', color: 'var(--nukrop-text-dim)', marginBottom: '40px', maxWidth: '600px', lineHeight: 1.6 }}>
              Download the official mobile app to access the AI Disease Scanner, GPS Field Navigator, and real-time alerts.
            </p>
            
            <div style={{ display: 'flex', gap: '24px', justifyContent: 'center', flexWrap: 'wrap' }}>
              <a href="/NuKropAI.apk" download className="nukrop-btn" style={{ padding: '18px 32px', fontSize: '16px', borderRadius: '16px', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '12px' }}>
                <Smartphone style={{ width: '20px', height: '20px' }} />
                <span>Download Android APK</span>
                <ChevronRight style={{ width: '16px', height: '16px', marginLeft: '4px' }} />
              </a>
              
              <button className="nukrop-btn nukrop-btn-secondary" style={{ padding: '18px 32px', fontSize: '16px', borderRadius: '16px', display: 'flex', alignItems: 'center', gap: '12px' }} onClick={() => alert("The iOS App is currently pending TestFlight approval.")}>
                <Apple style={{ width: '20px', height: '20px' }} />
                <span>Download for iOS</span>
              </button>
            </div>
            
            <p style={{ marginTop: '24px', fontSize: '13px', color: 'var(--nukrop-text-muted)' }}>* Android 8.0+ required for on-device AI inference.</p>
          </div>
        </section>

      </main>

      <footer style={{ padding: '40px 24px', textAlign: 'center', borderTop: '1px solid rgba(255,255,255,0.05)', background: 'rgba(0,0,0,0.2)', position: 'relative', zIndex: 10 }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px', marginBottom: '16px' }}>
          <Sprout style={{ color: 'var(--nukrop-text-muted)', width: '20px', height: '20px' }} />
          <span style={{ fontSize: '16px', fontFamily: 'Outfit', fontWeight: 'bold', color: 'var(--nukrop-text-dim)' }}>NuKropAI</span>
        </div>
        <p style={{ color: 'var(--nukrop-text-muted)', fontSize: '13px', marginBottom: '4px' }}>© 2026 NuKropAI by B. JASWANTH REDDY. All rights reserved.</p>
        <p style={{ color: 'var(--nukrop-text-muted)', fontSize: '13px' }}>Built with ❤️ for Indian Farmers.</p>
      </footer>

    </div>
  );
}
