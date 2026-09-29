import { useState } from 'react'
import { api } from '../api'
import { useAuth, useToast } from '../context'
import { ArrowRight, BarChart3, Languages, Landmark, MapPinned, ShieldCheck } from 'lucide-react'

export default function LoginPage() {
  const { login } = useAuth()
  const toast = useToast()
  const [email, setEmail] = useState('policy@demo.in')
  const [password, setPassword] = useState('policy456')
  const [loading, setLoading] = useState(false)

  const handleLogin = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      const res = await api.login(email, password)
      if (res.access_token) {
        login(res.access_token, res.role, res.name)
        toast('Login successful! Welcome, ' + res.name, 'success')
      } else {
        toast(res.detail || 'Login failed', 'error')
      }
    } catch {
      toast('Network error — is the backend running?', 'error')
    }
    setLoading(false)
  }

  const quickLogin = (e, pw) => { setEmail(e); setPassword(pw) }

  return (
    <div className="login-page">
      <section className="login-story">
        <div className="login-brand"><span className="login-brand-mark"><Landmark size={20} /></span> CDIP <span className="login-brand-tag">PUBLIC SERVICE INTELLIGENCE</span></div>
        <div className="login-story-content">
          <span className="login-eyebrow"><span className="pulse-dot" /> A civic signal, made actionable</span>
          <h1>Hear local needs.<br /><span>Plan with evidence.</span></h1>
          <p>Multilingual citizen input, transparent demand signals, and human-led development decisions in one place.</p>
          <div className="login-visual" aria-hidden="true">
            <div className="visual-orbit orbit-one" /><div className="visual-orbit orbit-two" />
            <div className="visual-center"><Landmark size={30} /></div>
            <div className="visual-node node-map"><MapPinned size={18} /></div>
            <div className="visual-node node-lang"><Languages size={18} /></div>
            <div className="visual-node node-data"><BarChart3 size={18} /></div>
            <span className="visual-caption">LISTEN <i /> UNDERSTAND <i /> RESPOND</span>
          </div>
          <div className="login-trust-row"><ShieldCheck size={17} /><span>Decision support, never automated sanction</span></div>
        </div>
        <div className="login-story-footer">India prototype <span>·</span> Synthetic demonstration data</div>
      </section>

      <div className="login-card fade-in">
        <div className="login-hero">
          <div className="login-emblem"><Landmark size={26} /></div>
          <p className="login-kicker">SECURE DEMO ACCESS</p>
          <h2 className="login-title">Welcome back</h2>
          <p className="login-subtitle">Sign in to explore the platform</p>
        </div>

        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label className="form-label" htmlFor="login-email">Email address</label>
            <input id="login-email" className="form-input" type="email" value={email} onChange={e => setEmail(e.target.value)} required />
          </div>
          <div className="form-group">
            <label className="form-label" htmlFor="login-password">Password</label>
            <input id="login-password" className="form-input" type="password" value={password} onChange={e => setPassword(e.target.value)} required />
          </div>
          <button className="btn btn-primary" style={{ width: '100%', justifyContent: 'center' }} disabled={loading}>
            {loading ? 'Signing in…' : <>Sign in <ArrowRight size={16} /></>}
          </button>
        </form>

        <div className="login-demo-hint">
            <strong style={{ color: 'var(--text-primary)', display: 'block', marginBottom: 8 }}>Choose a demo role</strong>
          <div className="demo-account-list">
            {[
              ['🏛️ Policymaker', 'policy@demo.in', 'policy456'],
              ['📊 Analyst', 'analyst@demo.in', 'analyst789'],
              ['👤 Citizen', 'citizen@demo.in', 'citizen123']
            ].map(([label, em, pw]) => (
              <button key={em} onClick={() => quickLogin(em, pw)}
                className={`demo-account ${email === em ? 'selected' : ''}`}>
                <span>{label}</span><span className="demo-account-hint">{email === em ? 'Selected' : 'Use this account'}</span>
              </button>
            ))}
          </div>
          <p style={{ marginTop: 10, fontSize: 11, color: 'var(--text-muted)', lineHeight: 1.5 }}>
            ⚠️ Prototype Demo System. All data synthetic. No real government integration.
          </p>
        </div>
      </div>
    </div>
  )
}
