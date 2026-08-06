import { Smartphone, Apple } from 'lucide-react';

export default function Hero() {
  return (
    <section style={{ 
      minHeight: '85vh', 
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'center', 
      padding: '40px 20px',
      position: 'relative',
      overflow: 'hidden'
    }}>
      <div className="radar-bg" style={{ 
        position: 'absolute', 
        top: 0, left: 0, right: 0, bottom: 0, 
        opacity: 0.15, 
        zIndex: 0 
      }}></div>

      <div style={{ position: 'relative', zIndex: 1, maxWidth: '900px', textAlign: 'center' }} className="fade-in">
        <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '24px' }}>
          <div className="glass-card" style={{ padding: '8px 16px', display: 'flex', alignItems: 'center', gap: '8px', borderRadius: '100px' }}>
            <div className="live-pulse"></div>
            <span style={{ fontSize: '12px', fontWeight: 'bold', letterSpacing: '0.05em', color: 'var(--nukrop-accent)' }}>
              NuKropAI 2.0 IS LIVE
            </span>
          </div>
        </div>

        <h1 style={{ fontSize: 'clamp(40px, 6vw, 72px)', lineHeight: 1.1, marginBottom: '24px', textShadow: '0 4px 24px rgba(0,0,0,0.5)' }}>
          Farming Reimagined with <br/>
          <span style={{ 
            background: 'linear-gradient(135deg, var(--nukrop-accent) 0%, #D4F040 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            filter: 'drop-shadow(0 0 30px rgba(200, 232, 55, 0.4))'
          }}>
            Artificial Intelligence
          </span>
        </h1>

        <p style={{ fontSize: 'clamp(16px, 2vw, 20px)', color: 'var(--nukrop-text-dim)', maxWidth: '650px', margin: '0 auto 48px', lineHeight: 1.6 }}>
          Experience the ultimate full-stack agrarian operating system. Real-time Mandi rates, AI disease scanning, and government subsidy matching directly on your smartphone.
        </p>

        <div style={{ display: 'flex', gap: '16px', justifyContent: 'center', flexWrap: 'wrap' }}>
          <a href="/NuKropAI.apk" download className="nukrop-btn" style={{ padding: '16px 28px', fontSize: '16px', borderRadius: '14px', textDecoration: 'none' }}>
            <Smartphone style={{ width: '20px', height: '20px' }} />
            Download for Android
          </a>
          <button className="nukrop-btn nukrop-btn-secondary" style={{ padding: '16px 28px', fontSize: '16px', borderRadius: '14px' }} onClick={() => alert("iOS App is currently in TestFlight review. Stay tuned!")}>
            <Apple style={{ width: '20px', height: '20px' }} />
            Download for iOS
          </button>
        </div>

        <div style={{ marginTop: '48px', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '32px', opacity: 0.7 }}>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <strong style={{ fontSize: '24px', color: 'white' }}>1.2M+</strong>
            <span style={{ fontSize: '12px', color: 'var(--nukrop-text-muted)', textTransform: 'uppercase' }}>Crops Scanned</span>
          </div>
          <div style={{ width: '1px', height: '40px', background: 'rgba(255,255,255,0.1)' }}></div>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <strong style={{ fontSize: '24px', color: 'white' }}>Live</strong>
            <span style={{ fontSize: '12px', color: 'var(--nukrop-text-muted)', textTransform: 'uppercase' }}>Mandi Synced</span>
          </div>
          <div style={{ width: '1px', height: '40px', background: 'rgba(255,255,255,0.1)' }}></div>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <strong style={{ fontSize: '24px', color: 'white' }}>99.9%</strong>
            <span style={{ fontSize: '12px', color: 'var(--nukrop-text-muted)', textTransform: 'uppercase' }}>AI Accuracy</span>
          </div>
        </div>
      </div>
    </section>
  );
}
