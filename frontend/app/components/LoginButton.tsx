'use client'

import { useState, useEffect } from 'react'
import LoginModal from './LoginModal'
import './LoginModal.css'

export default function LoginButton() {
  const [showLogin, setShowLogin] = useState(false)
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [userEmail, setUserEmail] = useState('')
  const [showDropdown, setShowDropdown] = useState(false)
  const [isAdmin, setIsAdmin] = useState(false)
  const [notificationCount, setNotificationCount] = useState(0)

  useEffect(() => {
    setIsLoggedIn(localStorage.getItem('isLoggedIn') === 'true')
    const email = localStorage.getItem('userEmail') || ''
    setUserEmail(email)
    
    // Fetch user data to check if admin
    if (email) {
      fetchUserAdmin(email)
    }
  }, [])

  const fetchUserAdmin = async (email: string) => {
    try {
      const response = await fetch(`http://localhost:8000/login/users`)
      if (response.ok) {
        const users = await response.json()
        const currentUser = users.find((u: any) => u.email === email)
        if (currentUser) {
          setIsAdmin(currentUser.is_admin || false)
          fetchNotificationCount(currentUser.user_id)
        }
      }
    } catch (error) {
      console.error("Error fetching user:", error)
    }
  }

  const fetchNotificationCount = async (userId: number) => {
    try {
      const response = await fetch(`http://localhost:8000/notifications/${userId}`)
      if (response.ok) {
        const notifications = await response.json()
        setNotificationCount(notifications.length)
      }
    } catch (error) {
      console.error("Error fetching notifications:", error)
    }
  }

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
            {!isAdmin && (
              <>
                <a 
                  href="/cart"
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
                  Cart
                </a>
                <a 
                  href="/orders"
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
                    Orders
                </a>
                <a 
                  href="/wishlist"
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
                    Wishlist
                </a>
                <a 
                  href="/notifications"
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
                    Notifications{notificationCount > 0 ? ` (${notificationCount})` : ''}
                </a>
              </>
            )}
            {isAdmin && (
              <a 
                href="/admin"
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
                Admin Page
              </a>
            )}
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
