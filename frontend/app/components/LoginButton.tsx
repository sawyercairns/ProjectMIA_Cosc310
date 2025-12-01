'use client'

import { useState, useEffect } from 'react'
import LoginModal from './LoginModal'
import './LoginModal.css'

export default function LoginButton() {
  const [showLogin, setShowLogin] = useState(false)
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [userEmail, setUserEmail] = useState('')
  const [showDropdown, setShowDropdown] = useState(false)

  useEffect(() => {
    setIsLoggedIn(localStorage.getItem('isLoggedIn') === 'true')
    setUserEmail(localStorage.getItem('userEmail') || '')
  }, [])

  const handleLogout = (e: React.MouseEvent) => {
    e.preventDefault()
    localStorage.removeItem('userEmail')
    localStorage.removeItem('isLoggedIn')
    setIsLoggedIn(false)
    setShowDropdown(false)
    window.location.reload()
  }

  if (isLoggedIn) {
    return (
      <div style={{ position: 'relative', display: 'inline-block' }}>
        <a 
          href="#" 
          onClick={(e) => { 
            e.preventDefault()
            setShowDropdown(!showDropdown)
          }}
        >
          Profile
        </a>
        {showDropdown && (
          <div style={{
            position: 'absolute',
            top: '100%',
            right: 0,
            backgroundColor: 'white',
            border: '1px solid #ccc',
            borderRadius: '4px',
            marginTop: '4px',
            minWidth: '150px',
            boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
            zIndex: 1000
          }}>
            <a 
              href="/profile"
              style={{
                display: 'block',
                padding: '8px 16px',
                color: '#000',
                textDecoration: 'none',
                borderBottom: '1px solid #eee'
              }}
              onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#f5f5f5'}
              onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'white'}
            >
              Settings
            </a>
            <a 
              href="#"
              onClick={handleLogout}
              style={{
                display: 'block',
                padding: '8px 16px',
                color: '#000',
                textDecoration: 'none'
              }}
              onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#f5f5f5'}
              onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'white'}
            >
              Logout
            </a>
          </div>
        )}
      </div>
    )
  }
  
  return (
    <>
      <a 
        href="#" 
        onClick={(e) => {
          e.preventDefault()
          setShowLogin(true)
        }}
      >
        Login
      </a>
      <LoginModal isOpen={showLogin} onClose={() => setShowLogin(false)} />
    </>
  )
}
