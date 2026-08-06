import { ScanSearch, UploadCloud, Cpu } from 'lucide-react';

export default function ScannerWeb() {
  return (
    <section style={{ padding: '60px 20px', maxWidth: '1000px', margin: '0 auto', borderTop: '1px solid rgba(255,255,255,0.05)' }}>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '40px', alignItems: 'center' }}>
        
        <div>
          <h2 style={{ fontSize: '36px', marginBottom: '16px', lineHeight: 1.2 }}>
            <ScanSearch style={{ color: 'var(--nukrop-accent)', width: '36px', height: '36px', marginBottom: '12px' }} />
            <br/>
            AI Disease Scanner <br/>
            <span style={{ color: 'var(--nukrop-text-muted)', fontSize: '24px' }}>Now on the Web</span>
          </h2>
          <p style={{ color: 'var(--nukrop-text-dim)', fontSize: '16px', lineHeight: 1.6, marginBottom: '24px' }}>
            Upload a picture of any diseased crop from your computer. Our Llama 3.2 11B Vision model will instantly diagnose the issue and provide chemical treatment plans with exact dosages.
          </p>
          
          <ul style={{ listStyle: 'none', padding: 0, margin: '0 0 32px 0', display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <li style={{ display: 'flex', alignItems: 'center', gap: '12px', fontSize: '14px' }}>
              <div style={{ padding: '6px', background: 'rgba(200, 232, 55, 0.1)', borderRadius: '50%' }}>
                <Cpu style={{ width: '16px', height: '16px', color: 'var(--nukrop-accent)' }} />
              </div>
              Powered by Groq Ultra-fast Inference
            </li>
            <li style={{ display: 'flex', alignItems: 'center', gap: '12px', fontSize: '14px' }}>
              <div style={{ padding: '6px', background: 'rgba(200, 232, 55, 0.1)', borderRadius: '50%' }}>
                <Cpu style={{ width: '16px', height: '16px', color: 'var(--nukrop-accent)' }} />
              </div>
              600+ Plant Pathologies Detected
            </li>
          </ul>

          <button className="nukrop-btn" onClick={() => alert("Web upload is coming in v2.1! Please use the Android app for live scanning.")}>
            <UploadCloud style={{ width: '18px', height: '18px' }} />
            Try Web Scanner (Beta)
          </button>
        </div>

        <div className="glass-card" style={{ 
          padding: '40px', 
          display: 'flex', 
          flexDirection: 'column', 
          alignItems: 'center', 
          justifyContent: 'center',
          border: '2px dashed rgba(200, 232, 55, 0.2)',
          background: 'rgba(11, 15, 7, 0.4)',
          minHeight: '300px'
        }}>
          <UploadCloud style={{ width: '64px', height: '64px', color: 'var(--nukrop-text-muted)', marginBottom: '16px' }} />
          <strong style={{ fontSize: '18px', marginBottom: '8px' }}>Drag & Drop Crop Image</strong>
          <span style={{ fontSize: '13px', color: 'var(--nukrop-text-dim)' }}>Supports JPG, PNG (Max 5MB)</span>
        </div>

      </div>
    </section>
  );
}
