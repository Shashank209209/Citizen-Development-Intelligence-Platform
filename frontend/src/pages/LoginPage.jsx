import { useState } from 'react'
import { api } from '../api'
import { useAuth, useToast } from '../context'

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
      <div className="login-card fade-in">
        <div className="login-hero">
          <div className="login-emblem">🇮🇳</div>
          <h1 className="login-title">CDIP — Digital Public Good</h1>
          <p className="login-subtitle">Citizen Development Intelligence Platform<br/>India Prototype · Multilingual · AI-Assisted</p>
        </div>

        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label className="form-label">Email</label>
            <input className="form-input" type="email" value={email} onChange={e => setEmail(e.target.value)} required />
          </div>
          <div className="form-group">
            <label className="form-label">Password</label>
            <input className="form-input" type="password" value={password} onChange={e => setPassword(e.target.value)} required />
          </div>
          <button className="btn btn-primary" style={{ width: '100%', justifyContent: 'center' }} disabled={loading}>
            {loading ? 'Signing In…' : '🔐 Sign In'}
          </button>
        </form>

        <div className="login-demo-hint">
          <strong style={{ color: 'var(--text-primary)', display: 'block', marginBottom: 8 }}>Demo Accounts</strong>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
            {[
              ['🏛️ Policymaker', 'policy@demo.in', 'policy456'],
              ['📊 Analyst', 'analyst@demo.in', 'analyst789'],
              ['👤 Citizen', 'citizen@demo.in', 'citizen123']
            ].map(([label, em, pw]) => (
              <button key={em} onClick={() => quickLogin(em, pw)}
                style={{ background: 'none', border: 'none', color: 'var(--accent)', cursor: 'pointer', textAlign: 'left', fontSize: 12, padding: '2px 0' }}>
                {label}: {em} / {pw}
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
