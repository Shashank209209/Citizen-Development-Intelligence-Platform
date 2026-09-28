import { createContext, useContext, useState, useCallback } from 'react'

const AuthContext = createContext(null)
const ToastContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const t = localStorage.getItem('cdip_token')
    const r = localStorage.getItem('cdip_role')
    const n = localStorage.getItem('cdip_name')
    return t ? { token: t, role: r, name: n } : null
  })

  const login = (token, role, name) => {
    localStorage.setItem('cdip_token', token)
    localStorage.setItem('cdip_role', role)
    localStorage.setItem('cdip_name', name)
    setUser({ token, role, name })
  }

  const logout = () => {
    localStorage.removeItem('cdip_token')
    localStorage.removeItem('cdip_role')
    localStorage.removeItem('cdip_name')
    setUser(null)
  }

  return <AuthContext.Provider value={{ user, login, logout }}>{children}</AuthContext.Provider>
}

export const useAuth = () => useContext(AuthContext)

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([])

  const addToast = useCallback((message, type = 'info') => {
    const id = Date.now()
    setToasts(prev => [...prev, { id, message, type }])
    setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 4000)
  }, [])

  return (
    <ToastContext.Provider value={addToast}>
      {children}
      <div className="toast-container">
        {toasts.map(t => (
          <div key={t.id} className={`toast ${t.type}`}>
            <span>{t.type === 'success' ? '✅' : t.type === 'error' ? '❌' : 'ℹ️'}</span>
            <span style={{ fontSize: 13, color: 'var(--text-primary)' }}>{t.message}</span>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  )
}

export const useToast = () => useContext(ToastContext)
