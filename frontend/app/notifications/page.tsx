'use client'

import { useState, useEffect } from 'react'

interface Notification {
  notification_id: number
  message: string
  notification_type: string
  order_id?: number
  total_price?: number
  item_count?: number
  product_id?: number
  product_name?: string
  old_price?: number
  new_price?: number
  discount_percent?: number
}

export default function NotificationsPage() {
  const [user, setUser] = useState<any>(null)
  const [notifications, setNotifications] = useState<Notification[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const userEmail = localStorage.getItem('userEmail')
    if (userEmail) {
      fetchUserByEmail(userEmail)
    } else {
      setLoading(false)
    }
  }, [])

  const fetchUserByEmail = async (email: string) => {
    try {
      const response = await fetch(`http://localhost:8000/login/users`)
      if (!response.ok) {
        setLoading(false)
        return
      }
      const users = await response.json()
      const currentUser = users.find((u: any) => u.email === email)
      setUser(currentUser)
      
      if (currentUser) {
        fetchNotifications(currentUser.user_id)
      }
    } catch (error) {
      console.error("Error fetching user:", error)
      setLoading(false)
    }
  }

  const fetchNotifications = async (userId: number) => {
    try {
      const response = await fetch(`http://localhost:8000/notifications/${userId}`)
      if (!response.ok) {
        console.error("Failed to fetch notifications, status:", response.status)
        setLoading(false)
        return
      }
      const data = await response.json()
      setNotifications(data)
    } catch (error) {
      console.error("Error fetching notifications:", error)
    } finally {
      setLoading(false)
    }
  }

  const dismissNotification = async (notificationId: number) => {
    try {
      const response = await fetch(`http://localhost:8000/notifications/${user.user_id}/${notificationId}`, {
        method: 'DELETE'
      })

      if (response.ok) {
        setNotifications(notifications.filter(n => n.notification_id !== notificationId))
      }
    } catch (error) {
      console.error("Error dismissing notification:", error)
    }
  }

  const dismissAll = async () => {
    for (const notification of notifications) {
      try {
        await fetch(`http://localhost:8000/notifications/${user.user_id}/${notification.notification_id}`, {
          method: 'DELETE'
        })
      } catch (error) {
        console.error("Error dismissing notification:", error)
      }
    }
    setNotifications([])
  }

  const getNotificationIcon = (type: string) => {
    switch (type) {
      case 'order_complete':
        return '📦'
      case 'wishlist_discount':
        return '💰'
      case 'wishlist_added':
        return '⭐'
      default:
        return '🔔'
    }
  }

  const getNotificationStyle = (type: string) => {
    switch (type) {
      case 'order_complete':
        return { borderLeft: '4px solid #4CAF50' }
      case 'wishlist_discount':
        return { borderLeft: '4px solid #FF9800' }
      case 'wishlist_added':
        return { borderLeft: '4px solid #9C27B0' }
      default:
        return { borderLeft: '4px solid #2196F3' }
    }
  }

  if (loading) {
    return <div>Loading...</div>
  }

  if (!user) {
    return (
      <div>
        <header>
          <div>
            <h1>🔔 Notifications</h1>
            <a href="/">🏠 Home</a>
          </div>
        </header>
        <div>
          <p>Please log in to view your notifications</p>
        </div>
      </div>
    )
  }

  return (
    <div style={{ padding: '20px' }}>
      {/* Header */}
      <header>
        <div>
          <div>
            <h1>🔔 Notifications</h1>
            <a href="/">🏠 Home</a>
          </div>
        </div>
      </header>

      {/* Notifications Content */}
      <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto', color: "black" }}>
        {/* Navigation Links */}
        <div style={{ marginBottom: '20px', backgroundColor: 'white' }}>
          <a href="/profile">👤 Profile</a>
          <span style={{ margin: '0 10px' }}>|</span>
          <a href="/orders">📦 Orders</a>
          <span style={{ margin: '0 10px' }}>|</span>
          <a href="/wishlist">⭐ Wishlist</a>
        </div>

        {/* User Info */}
        <div style={{ backgroundColor: 'white', padding: '20px', marginBottom: '20px', border: '1px solid #ccc', borderRadius: '8px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h2>{user.first_name} {user.last_name}'s Notifications</h2>
            <p>Total: {notifications.length} notification{notifications.length !== 1 ? 's' : ''}</p>
          </div>
          {notifications.length > 0 && (
            <button
              onClick={dismissAll}
              style={{
                padding: '10px 20px',
                backgroundColor: '#f44336',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Dismiss All
            </button>
          )}
        </div>

        {/* Notifications List */}
        {notifications.length === 0 ? (
          <div style={{ backgroundColor: 'white', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
            <p>You have no notifications.</p>
          </div>
        ) : (
          notifications.map((notification) => (
            <div 
              key={notification.notification_id} 
              style={{ 
                backgroundColor: 'white', 
                padding: '20px', 
                marginBottom: '15px', 
                border: '1px solid #ccc', 
                borderRadius: '8px',
                ...getNotificationStyle(notification.notification_type)
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                <div style={{ flex: 1 }}>
                  <div style={{ marginBottom: '10px', fontSize: '18px' }}>
                    {getNotificationIcon(notification.notification_type)} {notification.message}
                  </div>
                  <div style={{ fontSize: '12px', color: '#666' }}>
                    <strong>Type:</strong> {notification.notification_type.replace('_', ' ')}
                  </div>
                  {notification.notification_type === 'order_complete' && notification.order_id && (
                    <div style={{ marginTop: '10px' }}>
                      <a 
                        href={`/orders#order-${notification.order_id}`}
                        style={{ color: '#1976D2', textDecoration: 'underline' }}
                      >
                        View Order #{notification.order_id}
                      </a>
                    </div>
                  )}
                  {notification.notification_type === 'wishlist_added' && (
                    <div style={{ marginTop: '10px' }}>
                      <a 
                        href={`/wishlist#wishlist-${notification.product_id}`}
                        style={{ color: '#9C27B0', textDecoration: 'underline' }}
                      >
                        View in Wishlist
                      </a>
                    </div>
                  )}
                  {notification.notification_type === 'wishlist_discount' && (
                    <div style={{ marginTop: '10px' }}>
                      <a 
                        href={`/wishlist#wishlist-${notification.product_id}`}
                        style={{ color: '#FF9800', textDecoration: 'underline' }}
                      >
                        View in Wishlist
                      </a>
                    </div>
                  )}
                </div>
                <button 
                  onClick={() => dismissNotification(notification.notification_id)}
                  style={{ 
                    padding: '8px 16px', 
                    backgroundColor: '#9e9e9e', 
                    color: 'white', 
                    border: 'none', 
                    borderRadius: '4px', 
                    cursor: 'pointer' 
                  }}
                >
                  Dismiss
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
