import React, { useState, useEffect } from 'react';
import { 
  Sprout, 
  Lock, 
  Unlock, 
  ShieldAlert, 
  Droplet, 
  TrendingUp, 
  LogOut, 
  Compass,
  CheckCircle,
  Database,
  UserCheck,
  AlertCircle
} from 'lucide-react';
import { api, API_ROOT } from './api/client';

interface User {
  id: string;
  email: string;
  role: 'farmer' | 'buyer' | 'admin';
}

interface Valve {
  id: string;
  valve_name: string;
  state: 'OPEN' | 'CLOSED';
  flow_rate: number;
  triggered_by: string;
}

interface Contract {
  id: string;
  contract_address: string;
  buyer_name: string;
  commodity: string;
  amount: number;
  funds_status: 'LOCKED' | 'RELEASED' | 'REFUNDED';
  qr_verification_code: string;
  created_at: string;
  verified_at: string | null;
}

interface PestAlert {
  id: string;
  pest_name: string;
  latitude: number;
  longitude: number;
  reported_at: string;
  wind_direction: string;
  wind_speed: number;
}

interface SoilTelemetry {
  nitrogen: number;
  phosphorus: number;
  potassium: number;
  ph: number;
  organic_carbon: number;
  moisture: number;
}

interface Simulation {
  id: string;
  crop_name: string;
  field_size: number;
  yield_loss_risk: number;
  recommendation: string;
  created_at: string;
}

export default function App() {
  const [token, setToken] = useState<string | null>(localStorage.getItem('nk_token'));
  const [user, setUser] = useState<User | null>(
    localStorage.getItem('nk_user') ? JSON.parse(localStorage.getItem('nk_user')!) : null
  );

  // Auth Form
  const [isRegisterMode, setIsRegisterMode] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState<'farmer' | 'buyer' | 'admin'>('buyer');
  const [authError, setAuthError] = useState('');
  const [authLoading, setAuthLoading] = useState(false);

  // Data
  const [soil, setSoil] = useState<SoilTelemetry | null>(null);
  const [valves, setValves] = useState<Valve[]>([]);
  const [contracts, setContracts] = useState<Contract[]>([]);
  const [pests, setPests] = useState<PestAlert[]>([]);
  const [simulations, setSimulations] = useState<Simulation[]>([]);

  // UX states
  const [dataLoading, setDataLoading] = useState(false);
  const [dbStatus, setDbStatus] = useState<'connected' | 'error'>('connected');

  // Input states
  const [contractBuyer, setContractBuyer] = useState('');
  const [contractCommodity, setContractCommodity] = useState('Tomato');
  const [contractAmount, setContractAmount] = useState('');
  
  const [pestName, setPestName] = useState('Fall Armyworm');
  const [pestLat, setPestLat] = useState('28.7041');
  const [pestLon, setPestLon] = useState('77.1025');

  const [sandboxCrop, setSandboxCrop] = useState('Tomato');
  const [sandboxSize, setSandboxSize] = useState('3.0');

  useEffect(() => {
    if (token) {
      setDataLoading(true);
      fetchDashboardData().finally(() => setDataLoading(false));
      const interval = setInterval(fetchDashboardData, 5000);
      return () => clearInterval(interval);
    }
    return;
  }, [token]);

  const fetchDashboardData = async () => {
    try {
      // 1. Health check
      const healthRes = await fetch(`${API_ROOT}/health`);
      const healthData = await healthRes.json();
      setDbStatus(healthData.db === 'connected' ? 'connected' : 'error');

      // 2. Fetch via secure abstraction API client
      const soilData = await api.get('/soil/telemetry/latest');
      setSoil(soilData);

      const valvesList = await api.get('/irrigation/valves');
      setValves(valvesList);

      const contractsList = await api.get('/contracts');
      setContracts(contractsList);

      const pestsList = await api.get('/pests/alerts');
      setPests(pestsList);

      const simList = await api.get('/simulations');
      setSimulations(simList);

    } catch (err) {
      console.error("Dashboard Fetch Error: ", err);
      // Don't override status if it's a network disconnect
      if (err instanceof TypeError) {
        setDbStatus('error');
      }
    }
  };

  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    setAuthError('');
    setAuthLoading(true);

    const endpoint = isRegisterMode ? '/api/v1/auth/register' : '/api/v1/auth/login';
    const body = isRegisterMode ? { email, password, role } : { email, password };

    try {
      const res = await fetch(`${API_ROOT}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });

      const data = await res.json();
      if (!res.ok) {
        setAuthError(data.error || 'Authentication failed');
        setAuthLoading(false);
        return;
      }

      localStorage.setItem('nk_token', data.accessToken);
      localStorage.setItem('nk_refresh_token', data.refreshToken);
      localStorage.setItem('nk_user', JSON.stringify(data.user));
      setToken(data.accessToken);
      setUser(data.user);
    } catch (err) {
      setAuthError('Unable to connect to Core API Server');
    } finally {
      setAuthLoading(false);
    }
  };

  const handleLogout = async () => {
    const rToken = localStorage.getItem('nk_refresh_token');
    if (rToken) {
      await fetch(`${API_ROOT}/api/v1/auth/logout`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refreshToken: rToken })
      }).catch(() => {});
    }
    localStorage.removeItem('nk_token');
    localStorage.removeItem('nk_refresh_token');
    localStorage.removeItem('nk_user');
    setToken(null);
    setUser(null);
  };

  const handleCreateContract = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!contractBuyer || !contractAmount) return;

    try {
      await api.post('/contracts/create', {
        buyer_name: contractBuyer,
        commodity: contractCommodity,
        amount: parseFloat(contractAmount)
      });
      setContractBuyer('');
      setContractAmount('');
      fetchDashboardData();
    } catch (err: any) {
      alert(err.message || 'Operation failed');
    }
  };

  const handleReleaseEscrow = async (contractId: string, qrCode: string) => {
    try {
      await api.post('/contracts/verify-qr', {
        contract_id: contractId,
        qr_code: qrCode
      });
      fetchDashboardData();
    } catch (err: any) {
      alert(err.message || 'Verification rejected');
    }
  };

  const handleReportPest = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!pestName || !pestLat || !pestLon) return;

    try {
      await api.post('/pests/report', {
        pest_name: pestName,
        latitude: parseFloat(pestLat),
        longitude: parseFloat(pestLon),
        wind_direction: 'West',
        wind_speed: 15.0
      });
      fetchDashboardData();
    } catch (err: any) {
      alert(err.message || 'Outbreak logging failed');
    }
  };

  const handleRunSimulation = async () => {
    try {
      await api.post('/simulations/run', {
        crop_name: sandboxCrop,
        field_size: parseFloat(sandboxSize)
      });
      fetchDashboardData();
    } catch (err: any) {
      alert(err.message || 'Simulation failed');
    }
  };

  const handleToggleValve = async (name: string, currentState: 'OPEN' | 'CLOSED') => {
    const nextState = currentState === 'OPEN' ? 'CLOSED' : 'OPEN';
    const nextFlow = nextState === 'OPEN' ? 2.5 : 0.0;

    try {
      await api.post('/irrigation/valves/toggle', {
        valve_name: name,
        state: nextState,
        flow_rate: nextFlow,
        triggered_by: 'manual'
      });
      fetchDashboardData();
    } catch (err: any) {
      alert(err.message || 'Valve control rejected');
    }
  };

  const renderSkeletonList = () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
      {[1, 2, 3].map((i) => (
        <div key={i} style={{ background: 'rgba(255,255,255,0.02)', height: '60px', borderRadius: '10px', animation: 'pulse 1.5s infinite', border: '1px solid rgba(255,255,255,0.03)' }}></div>
      ))}
    </div>
  );

  if (!token) {
    return (
      <div style={{ display: 'flex', minHeight: '100vh', alignItems: 'center', justifyContent: 'center', padding: '20px' }}>
        <div className="glass-card" style={{ width: '100%', maxWidth: '400px', padding: '32px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '24px', justifyContent: 'center' }}>
            <Sprout style={{ color: 'var(--nukrop-accent)', width: '36px', height: '36px' }} />
            <span style={{ fontSize: '24px', fontFamily: 'Outfit', fontWeight: 'bold' }}>NuKropAI</span>
          </div>

          <h2 style={{ fontSize: '18px', textAlign: 'center', marginBottom: '20px' }}>
            {isRegisterMode ? 'Create Corporate Account' : 'Enterprise Control Sign In'}
          </h2>

          <form onSubmit={handleAuth} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
              <label style={{ fontSize: '12px', color: 'var(--nukrop-text-dim)' }}>Corporate Email</label>
              <input 
                type="email" 
                className="nukrop-input" 
                placeholder="buyer@bigbasket.com" 
                value={email}
                onChange={e => setEmail(e.target.value)}
                required
              />
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
              <label style={{ fontSize: '12px', color: 'var(--nukrop-text-dim)' }}>Secure Password</label>
              <input 
                type="password" 
                className="nukrop-input" 
                placeholder="••••••••" 
                value={password}
                onChange={e => setPassword(e.target.value)}
                required
              />
            </div>

            {isRegisterMode && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                <label style={{ fontSize: '12px', color: 'var(--nukrop-text-dim)' }}>Select Operating Role</label>
                <select 
                  className="nukrop-input"
                  value={role}
                  onChange={e => setRole(e.target.value as any)}
                >
                  <option value="buyer">Direct Crop Buyer / Corporates</option>
                  <option value="farmer">Operating Farm Lead</option>
                  <option value="admin">System Administrator</option>
                </select>
              </div>
            )}

            {authError && (
              <div style={{ padding: '10px', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid var(--nukrop-error)', borderRadius: '6px', color: 'var(--nukrop-error)', fontSize: '12px', textAlign: 'center' }}>
                {authError}
              </div>
            )}

            <button type="submit" className="nukrop-btn" disabled={authLoading} style={{ width: '100%', marginTop: '8px' }}>
              {authLoading ? 'Authenticating...' : isRegisterMode ? 'Register Account' : 'Authenticate Session'}
            </button>
          </form>

          <p style={{ textAlign: 'center', fontSize: '12px', marginTop: '20px', color: 'var(--nukrop-text-muted)' }}>
            {isRegisterMode ? 'Already registered?' : 'Request new corporate access?'}{' '}
            <span 
              onClick={() => setIsRegisterMode(!isRegisterMode)} 
              style={{ color: 'var(--nukrop-accent)', cursor: 'pointer', fontWeight: 'bold' }}
            >
              {isRegisterMode ? 'Sign In' : 'Register Here'}
            </span>
          </p>
        </div>
      </div>
    );
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      
      {/* Top Header */}
      <header className="glass-card" style={{ borderRadius: '0', borderLeft: 'none', borderRight: 'none', borderTop: 'none', padding: '16px 24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Sprout style={{ color: 'var(--nukrop-accent)', width: '28px', height: '28px' }} />
          <span style={{ fontSize: '20px', fontFamily: 'Outfit', fontWeight: 'bold' }}>NuKropAI Control Center</span>
          <div className="badge badge-green" style={{ display: 'flex', alignItems: 'center', gap: '4px', marginLeft: '12px' }}>
            <div className="live-pulse"></div> Live Sync
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', color: 'var(--nukrop-text-dim)' }}>
            <Database style={{ width: '14px', height: '14px' }} />
            Database: {dbStatus === 'connected' ? (
              <span style={{ color: 'var(--nukrop-green-badge)', fontWeight: 'bold' }}>CONNECTED</span>
            ) : (
              <span style={{ color: 'var(--nukrop-error)', fontWeight: 'bold' }}>DISCONNECTED</span>
            )}
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', color: 'var(--nukrop-text-dim)' }}>
            <UserCheck style={{ width: '14px', height: '14px', color: 'var(--nukrop-accent)' }} />
            Logged: <strong style={{ color: 'white' }}>{user?.email}</strong> 
            <span className="badge badge-yellow" style={{ fontSize: '9px', padding: '2px 6px' }}>{user?.role}</span>
          </div>

          <button onClick={handleLogout} className="nukrop-btn nukrop-btn-secondary" style={{ padding: '8px 12px' }}>
            <LogOut style={{ width: '14px', height: '14px' }} /> Logout
          </button>
        </div>
      </header>

      {/* Main UI panels */}
      <main style={{ flex: '1', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '24px', padding: '24px' }}>
        
        {/* Panel 1: Subsoil Gauges & Irrigation Valves */}
        <section style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          
          {/* Subsoil Telemetry */}
          <div className="glass-card" style={{ padding: '20px' }}>
            <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '16px', marginBottom: '6px' }}>
              <TrendingUp style={{ color: 'var(--nukrop-accent)', width: '20px', height: '20px' }} />
              Subsoil Telemetry Probe (Real-time)
            </h3>
            <p style={{ fontSize: '12px', color: 'var(--nukrop-text-muted)', marginBottom: '16px' }}>
              Real-time measurement indices logged from active IoT field sensors.
            </p>

            {dataLoading || !soil ? (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '12px' }}>
                {[1, 2, 3, 4, 5, 6].map((i) => (
                  <div key={i} style={{ background: 'rgba(255,255,255,0.02)', height: '55px', borderRadius: '10px', animation: 'pulse 1.5s infinite' }}></div>
                ))}
              </div>
            ) : (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '12px' }}>
                {[
                  { label: 'Nitrogen', value: `${soil.nitrogen} ppm`, color: '#60A5FA' },
                  { label: 'Phosphorus', value: `${soil.phosphorus} ppm`, color: '#F472B6' },
                  { label: 'Potassium', value: `${soil.potassium} ppm`, color: '#34D399' },
                  { label: 'pH Value', value: `${soil.ph}`, color: '#A78BFA' },
                  { label: 'Organic Carbon', value: `${soil.organic_carbon}%`, color: '#F59E0B' },
                  { label: 'Moisture', value: `${soil.moisture}%`, color: '#2563EB' }
                ].map((item, idx) => (
                  <div key={idx} style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.05)', borderRadius: '10px', padding: '12px', textAlign: 'center' }}>
                    <span style={{ fontSize: '10px', color: 'var(--nukrop-text-muted)', display: 'block', textTransform: 'uppercase' }}>{item.label}</span>
                    <span style={{ fontSize: '18px', fontWeight: 'bold', color: item.color, display: 'block', marginTop: '4px' }}>{item.value}</span>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Smart Micro-Irrigation Controls */}
          <div className="glass-card" style={{ padding: '20px' }}>
            <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '16px', marginBottom: '6px' }}>
              <Droplet style={{ color: 'var(--nukrop-accent)', width: '20px', height: '20px' }} />
              Smart Micro-Irrigation Control Panel
            </h3>
            <p style={{ fontSize: '12px', color: 'var(--nukrop-text-muted)', marginBottom: '16px' }}>
              Directly toggle solenoid micro-valves inside specific farming zones.
            </p>

            {dataLoading ? renderSkeletonList() : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {['Valve 01 (Northeast)', 'Valve 02 (Northwest)', 'Valve 03 (South Field)'].map((vName, idx) => {
                  const liveValve = valves.find(v => v.valve_name === vName);
                  const stateStr = liveValve ? liveValve.state : 'CLOSED';
                  const flowRate = liveValve ? liveValve.flow_rate : 0.0;
                  
                  return (
                    <div key={idx} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: 'rgba(255,255,255,0.02)', padding: '12px', borderRadius: '10px', border: '1px solid rgba(255,255,255,0.04)' }}>
                      <div>
                        <span style={{ display: 'block', fontSize: '13px', fontWeight: '600' }}>{vName}</span>
                        <span style={{ fontSize: '11px', color: 'var(--nukrop-text-muted)' }}>
                          Status: <strong style={{ color: stateStr === 'OPEN' ? 'var(--nukrop-accent)' : 'white' }}>{stateStr}</strong> ({flowRate} L/min)
                        </span>
                      </div>
                      
                      {user?.role === 'buyer' ? (
                        <span style={{ fontSize: '11px', color: 'var(--nukrop-text-muted)', fontStyle: 'italic' }}>Requires Operator Role</span>
                      ) : (
                        <button 
                          onClick={() => handleToggleValve(vName, stateStr)}
                          className={`nukrop-btn ${stateStr === 'OPEN' ? 'nukrop-btn-secondary' : ''}`}
                          style={{ padding: '6px 12px', fontSize: '12px' }}
                        >
                          {stateStr === 'OPEN' ? 'Close Valve' : 'Open Valve'}
                        </button>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>

        </section>

        {/* Panel 2: Direct Buyer Escrow Contracts */}
        <section style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          
          <div className="glass-card" style={{ padding: '20px' }}>
            <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '16px', marginBottom: '6px' }}>
              <Lock style={{ color: 'var(--nukrop-accent)', width: '20px', height: '20px' }} />
              Direct Buyer Escrow Contracts
            </h3>
            <p style={{ fontSize: '12px', color: 'var(--nukrop-text-muted)', marginBottom: '16px' }}>
              Real ledger blockchain-simulated lock/release contracts to bypass middle-men.
            </p>

            {/* Create Contract (Requires Buyer role) */}
            {user?.role === 'farmer' ? (
              <div style={{ display: 'flex', gap: '8px', padding: '12px', background: 'rgba(255,255,255,0.02)', border: '1px dashed rgba(255,255,255,0.1)', borderRadius: '10px', alignItems: 'center', marginBottom: '20px', fontSize: '12px', color: 'var(--nukrop-text-dim)' }}>
                <AlertCircle style={{ width: '16px', height: '16px', color: 'var(--nukrop-warning)' }} />
                Farmers can verify delivery but only Buyers can initialize purchase escrows.
              </div>
            ) : (
              <form onSubmit={handleCreateContract} style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '20px', background: 'rgba(255,255,255,0.02)', padding: '14px', borderRadius: '10px', border: '1px solid rgba(255,255,255,0.04)' }}>
                <span style={{ fontSize: '12px', fontWeight: 'bold', color: 'var(--nukrop-accent)', display: 'block' }}>Initialize Purchase Escrow</span>
                
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                  <input 
                    type="text" 
                    className="nukrop-input" 
                    placeholder="Buyer Corporation Name" 
                    value={contractBuyer}
                    onChange={e => setContractBuyer(e.target.value)}
                    required
                  />
                  <select 
                    className="nukrop-input"
                    value={contractCommodity}
                    onChange={e => setContractCommodity(e.target.value)}
                  >
                    <option value="Tomato">Tomato</option>
                    <option value="Wheat">Wheat</option>
                    <option value="Rice">Rice</option>
                    <option value="Cotton">Cotton</option>
                  </select>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '10px' }}>
                  <input 
                    type="number" 
                    className="nukrop-input" 
                    placeholder="Contract Escrow Value (₹)" 
                    value={contractAmount}
                    onChange={e => setContractAmount(e.target.value)}
                    required
                  />
                  <button type="submit" className="nukrop-btn" style={{ fontSize: '12px' }}>
                    Lock Funds
                  </button>
                </div>
              </form>
            )}

            {/* Escrow Contract list */}
            {dataLoading ? renderSkeletonList() : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', maxHeight: '350px', overflowY: 'auto' }}>
                {contracts.length === 0 ? (
                  <div style={{ textAlign: 'center', fontSize: '12px', color: 'var(--nukrop-text-muted)', padding: '40px 20px', border: '1px dashed rgba(255,255,255,0.05)', borderRadius: '10px' }}>
                    No contracts recorded on the ledger. Create an escrow lock to begin.
                  </div>
                ) : (
                  contracts.map((c) => (
                    <div key={c.id} style={{ background: 'rgba(255,255,255,0.02)', padding: '12px', borderRadius: '10px', border: '1px solid rgba(255,255,255,0.04)' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '8px' }}>
                        <div>
                          <strong style={{ fontSize: '13px', display: 'block' }}>{c.commodity} Purchase</strong>
                          <span style={{ fontSize: '11px', color: 'var(--nukrop-text-muted)' }}>Buyer: {c.buyer_name}</span>
                        </div>
                        <span className={`badge ${c.funds_status === 'RELEASED' ? 'badge-green' : 'badge-yellow'}`}>
                          {c.funds_status}
                        </span>
                      </div>

                      <div style={{ fontSize: '11px', color: 'var(--nukrop-text-dim)', marginBottom: '8px' }}>
                        <code style={{ background: 'black', padding: '2px 6px', borderRadius: '4px', display: 'block', overflowX: 'auto' }}>{c.contract_address}</code>
                      </div>

                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <span style={{ fontSize: '14px', fontWeight: 'bold', color: 'var(--nukrop-accent)' }}>₹{parseFloat(c.amount as any).toLocaleString()}</span>
                        
                        {c.funds_status === 'LOCKED' ? (
                          user?.role === 'buyer' ? (
                            <span style={{ fontSize: '11px', color: 'var(--nukrop-text-muted)', fontStyle: 'italic' }}>Awaiting Operator Release</span>
                          ) : (
                            <button 
                              onClick={() => handleReleaseEscrow(c.id, c.qr_verification_code)}
                              className="nukrop-btn"
                              style={{ padding: '6px 12px', fontSize: '11px' }}
                            >
                              <Unlock style={{ width: '12px', height: '12px' }} /> Release Escrow ({c.qr_verification_code})
                            </button>
                          )
                        ) : (
                          <span style={{ fontSize: '11px', color: 'var(--nukrop-green-badge)', fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: '4px' }}>
                            <CheckCircle style={{ width: '14px', height: '14px' }} /> Funds Settled Instantly
                          </span>
                        )}
                      </div>
                    </div>
                  ))
                )}
              </div>
            )}
          </div>

        </section>

        {/* Panel 3: Pest Warnings & Sandbox */}
        <section style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          
          {/* Pest Outbreak Radar */}
          <div className="glass-card radar-bg" style={{ padding: '20px' }}>
            <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '16px', marginBottom: '6px' }}>
              <ShieldAlert style={{ color: 'var(--nukrop-error)', width: '20px', height: '20px' }} />
              Pest Influx Warning Radar (Early Outbreaks)
            </h3>
            <p style={{ fontSize: '12px', color: 'var(--nukrop-text-muted)', marginBottom: '16px' }}>
              Crowd-sourced outbreaks reported by neighboring farms.
            </p>

            <form onSubmit={handleReportPest} style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginBottom: '16px', background: 'rgba(255,255,255,0.02)', padding: '12px', borderRadius: '10px', border: '1px solid rgba(255,255,255,0.04)' }}>
              <span style={{ fontSize: '11px', fontWeight: 'bold', color: 'var(--nukrop-error)', display: 'block' }}>Broadcast Outbreak Report</span>
              
              <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1fr', gap: '8px' }}>
                <input 
                  type="text" 
                  className="nukrop-input" 
                  value={pestName} 
                  onChange={e => setPestName(e.target.value)} 
                  required
                />
                <input 
                  type="text" 
                  className="nukrop-input" 
                  value={pestLat} 
                  onChange={e => setPestLat(e.target.value)} 
                  required
                />
                <input 
                  type="text" 
                  className="nukrop-input" 
                  value={pestLon} 
                  onChange={e => setPestLon(e.target.value)} 
                  required
                />
              </div>

              <button type="submit" className="nukrop-btn nukrop-btn-danger" style={{ fontSize: '11px', padding: '6px 12px' }}>
                Broadcast Early Warning
              </button>
            </form>

            {dataLoading ? renderSkeletonList() : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', maxHeight: '200px', overflowY: 'auto' }}>
                {pests.length === 0 ? (
                  <div style={{ textAlign: 'center', fontSize: '11px', color: 'var(--nukrop-text-muted)', padding: '20px' }}>
                    No alerts in this grid.
                  </div>
                ) : (
                  pests.map((p) => (
                    <div key={p.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: 'rgba(239, 68, 68, 0.05)', padding: '10px', borderRadius: '8px', border: '1px solid rgba(239, 68, 68, 0.15)' }}>
                      <div>
                        <span style={{ display: 'block', fontSize: '12px', fontWeight: 'bold', color: 'var(--nukrop-error)' }}>{p.pest_name}</span>
                        <span style={{ fontSize: '10px', color: 'var(--nukrop-text-dim)' }}>
                          Loc: {p.latitude.toFixed(4)}, {p.longitude.toFixed(4)} • Wind: East {p.wind_speed}km/h
                        </span>
                      </div>
                      <span style={{ fontSize: '10px', color: 'var(--nukrop-text-muted)' }}>
                        {new Date(p.reported_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </span>
                    </div>
                  ))
                )}
              </div>
            )}
          </div>

          {/* Simulation Sandbox */}
          <div className="glass-card" style={{ padding: '20px' }}>
            <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '16px', marginBottom: '6px' }}>
              <Compass style={{ color: 'var(--nukrop-accent)', width: '20px', height: '20px' }} />
              What-If Crop Simulation Sandbox
            </h3>
            <p style={{ fontSize: '12px', color: 'var(--nukrop-text-muted)', marginBottom: '16px' }}>
              Simulate soil, season, and yield forecasting parameters before planting.
            </p>

            <div style={{ display: 'flex', gap: '10px', marginBottom: '12px' }}>
              <select 
                className="nukrop-input"
                value={sandboxCrop}
                onChange={e => setSandboxCrop(e.target.value)}
                style={{ flex: 1 }}
              >
                <option value="Tomato">Tomato</option>
                <option value="Wheat">Wheat</option>
                <option value="Rice">Rice</option>
                <option value="Cotton">Cotton</option>
              </select>

              <input 
                type="number" 
                className="nukrop-input"
                style={{ width: '100px' }}
                value={sandboxSize}
                onChange={e => setSandboxSize(e.target.value)}
              />

              <button onClick={handleRunSimulation} className="nukrop-btn" style={{ fontSize: '12px' }}>
                Run Model
              </button>
            </div>

            {dataLoading ? renderSkeletonList() : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', maxHeight: '180px', overflowY: 'auto' }}>
                {simulations.length === 0 ? (
                  <div style={{ textAlign: 'center', fontSize: '11px', color: 'var(--nukrop-text-muted)', padding: '20px' }}>
                    No simulations executed yet. Select parameters to compute yield risk profiles.
                  </div>
                ) : (
                  simulations.map((sim) => (
                    <div key={sim.id} style={{ background: 'rgba(255,255,255,0.02)', padding: '10px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.04)', fontSize: '11px' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                        <strong>{sim.crop_name} ({sim.field_size} Acres)</strong>
                        <span style={{ color: 'var(--nukrop-warning)', fontWeight: 'bold' }}>{sim.yield_loss_risk}% Yield Risk</span>
                      </div>
                      <div style={{ color: 'var(--nukrop-text-dim)', whiteSpace: 'pre-line', lineHeight: '15px' }}>
                        {sim.recommendation}
                      </div>
                    </div>
                  ))
                )}
              </div>
            )}
          </div>

        </section>

      </main>
    </div>
  );
}
