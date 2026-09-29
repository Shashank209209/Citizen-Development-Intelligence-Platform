import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { AuthProvider, ToastProvider } from './context.jsx'

document.documentElement.dataset.theme = localStorage.getItem('cdip_theme') === 'dark' ? 'dark' : 'light'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <AuthProvider>
      <ToastProvider>
        <App />
      </ToastProvider>
    </AuthProvider>
  </StrictMode>,
)
