'use client'

import { useState, useEffect } from 'react'
import dynamic from 'next/dynamic'

// Dynamically import ReCAPTCHA to avoid SSR issues
const ReCAPTCHA = dynamic(() => import('react-google-recaptcha'), {
  ssr: false,
})

interface LoginModalProps {
  isOpen: boolean
  onClose: () => void
}

export default function LoginModal({ isOpen, onClose }: LoginModalProps) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [message, setMessage] = useState('')
  const [captchaToken, setCaptchaToken] = useState<string | null>(null)
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!isOpen) return null

  const handleCaptchaChange = (token: string | null) => {
    setCaptchaToken(token)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setMessage('')

    // Validate reCAPTCHA
    if (!captchaToken) {
      setMessage('Please complete the CAPTCHA verification')
      return
    }

    try {
      const response = await fetch(`http://localhost:8000/login?email=${email}&password=${password}`)
      const data = await response.text()
      
      // Backend returns JSON string with quotes, so we need to check for both formats
      if (data === 'VALID USER' || data === '"VALID USER"') {
        setMessage('Login successful!')
        // Store user info in localStorage
        localStorage.setItem('userEmail', email)
        localStorage.setItem('isLoggedIn', 'true')
        // Redirect or close modal
        setTimeout(() => {
          onClose()
          window.location.reload() // Refresh to update UI
        }, 1000)
      } else {
        setMessage('Invalid email or password')
      }
    } catch (error) {
      setMessage('Error connecting to server')
    }
  }

  return (
    <div className="login-modal" aria-hidden="false">
      <div className="login-modal__panel" role="dialog" aria-modal="true" aria-labelledby="login-modal-title">
        <button 
          className="login-modal__close" 
          type="button" 
          aria-label="Close login form" 
          onClick={onClose}
        >
          &times;
        </button>
        
        <div className="login-modal__content">
          <h2 className="login-title" id="login-modal-title">ProjectMIA Login</h2>

          <form className="login-form" onSubmit={handleSubmit}>
            <label className="login-label" htmlFor="modal-email">Email</label>
            <input 
              id="modal-email" 
              className="login-input" 
              name="email" 
              type="email" 
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />

            <label className="login-label" htmlFor="modal-password">Password</label>
            <input 
              id="modal-password" 
              className="login-input" 
              name="password" 
              type="password" 
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />

            <div style={{ marginTop: '16px', display: 'flex', justifyContent: 'center' }}>
              {mounted && (
                <ReCAPTCHA
                  sitekey={process.env.NEXT_PUBLIC_RECAPTCHA_SITE_KEY || ''}
                  onChange={handleCaptchaChange}
                />
              )}
            </div>

            {message && (
              <div style={{ color: message.includes('successful') ? 'green' : 'red', fontSize: '13px', marginTop: '4px' }}>
                {message}
              </div>
            )}

            <div className="login-actions">
              <button className="login-btn is-primary" type="submit">Login</button>
              <button className="login-btn" type="button" onClick={onClose}>Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}
