import React, { useState, useEffect } from 'react';
import { TrendingUp, Activity, Search } from 'lucide-react';

export default function MandiWeb() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<any[]>([]);
  const [error, setError] = useState('');
  
  const [state, setState] = useState('Maharashtra');
  const [commodity, setCommodity] = useState('Tomato');

  const fetchData = async () => {
    setLoading(true);
    setError('');
    
    try {
      const stateEnc = encodeURIComponent(state);
      const commEnc = encodeURIComponent(commodity);
      // Public Gov API key used in the app
      const apiKey = '579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b';
      const url = `https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key=${apiKey}&format=json&limit=10&filters[state]=${stateEnc}&filters[commodity]=${commEnc}`;
      
      const res = await fetch(url);
      if (!res.ok) throw new Error(`API returned ${res.status}`);
      const json = await res.json();
      
      if (json.records) {
        setData(json.records);
      } else {
        setData([]);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to fetch');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <section style={{ padding: '60px 20px', maxWidth: '1000px', margin: '0 auto' }}>
      <div style={{ textAlign: 'center', marginBottom: '40px' }}>
        <h2 style={{ fontSize: '36px', marginBottom: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '12px' }}>
          <Activity style={{ color: 'var(--nukrop-accent)', width: '32px', height: '32px' }} />
          Live Mandi Prices
        </h2>
        <p style={{ color: 'var(--nukrop-text-dim)' }}>Real-time government market data directly on the web.</p>
      </div>

      <div className="glass-card" style={{ padding: '24px' }}>
        <div style={{ display: 'flex', gap: '12px', marginBottom: '24px', flexWrap: 'wrap' }}>
          <input 
            type="text" 
            className="nukrop-input" 
            value={state}
            onChange={(e) => setState(e.target.value)}
            style={{ flex: 1, minWidth: '200px' }}
          />
          <input 
            type="text" 
            className="nukrop-input" 
            value={commodity}
            onChange={(e) => setCommodity(e.target.value)}
            style={{ flex: 1, minWidth: '200px' }}
          />
          <button className="nukrop-btn" onClick={fetchData}>
            <Search style={{ width: '16px', height: '16px' }} />
            Search
          </button>
        </div>

        {loading ? (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {[1, 2, 3, 4].map(i => (
              <div key={i} className="skeleton" style={{ height: '60px', borderRadius: '10px' }}></div>
            ))}
          </div>
        ) : error ? (
          <div style={{ padding: '20px', textAlign: 'center', color: 'var(--nukrop-error)', background: 'rgba(239, 68, 68, 0.1)', borderRadius: '10px' }}>
            {error}
          </div>
        ) : data.length === 0 ? (
          <div style={{ padding: '40px', textAlign: 'center', color: 'var(--nukrop-text-muted)' }}>
            No records found for {commodity} in {state}.
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {data.map((item, idx) => (
              <div key={idx} style={{ 
                display: 'flex', 
                justifyContent: 'space-between', 
                alignItems: 'center',
                padding: '16px', 
                background: 'rgba(255,255,255,0.02)', 
                borderRadius: '10px',
                border: '1px solid rgba(255,255,255,0.05)'
              }}>
                <div>
                  <strong style={{ fontSize: '16px', display: 'block', color: 'var(--nukrop-accent)' }}>{item.market}</strong>
                  <span style={{ fontSize: '12px', color: 'var(--nukrop-text-dim)' }}>{item.district}, {item.state}</span>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', justifyContent: 'flex-end' }}>
                    <TrendingUp style={{ color: 'var(--nukrop-warning)', width: '14px', height: '14px' }} />
                    <strong style={{ fontSize: '20px' }}>₹{item.modal_price}</strong>
                  </div>
                  <span style={{ fontSize: '11px', color: 'var(--nukrop-text-muted)' }}>Arrival: {item.arrival_date}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}
