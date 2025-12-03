'use client'

import { useState, useEffect } from 'react'

export default function ProfilePage() {
  const [user, setUser] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [imageError, setImageError] = useState(false)
  
  // Password update form
  const [oldPassword, setOldPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [passwordMessage, setPasswordMessage] = useState('')
  
  // Image update form
  const [imageUrl, setImageUrl] = useState('')
  const [imageMessage, setImageMessage] = useState('')
  
  // Payment update form
  const [cardNumber, setCardNumber] = useState('')
  const [cvv, setCvv] = useState('')
  const [expirationDate, setExpirationDate] = useState('')
  const [paymentMessage, setPaymentMessage] = useState('')

  // Year in Review
  const [yearSummaryExpanded, setYearSummaryExpanded] = useState(false)
  const [yearSummary, setYearSummary] = useState<any>(null)
  const [yearSummaryLoading, setYearSummaryLoading] = useState(false)

  const DEFAULT_IMAGE = '/defaultUser.png'

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
      setImageUrl(currentUser?.image_url || '')
    } catch (error) {
      console.error("Error fetching user:", error)
    } finally {
      setLoading(false)
    }
  }

  const handlePasswordUpdate = async (e: React.FormEvent) => {
    e.preventDefault()
    setPasswordMessage('')

    if (newPassword !== confirmPassword) {
      setPasswordMessage('New passwords do not match')
      return
    }

    if (newPassword.length < 3) {
      setPasswordMessage('Password must be at least 3 characters')
      return
    }

    try {
      const response = await fetch('http://localhost:8000/login/password', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: user.user_id,
          old_password: oldPassword,
          new_password: newPassword
        })
      })

      const data = await response.json()
      
      if (response.ok) {
        setPasswordMessage('Password updated successfully!')
        setOldPassword('')
        setNewPassword('')
        setConfirmPassword('')
      } else {
        setPasswordMessage(data.detail || 'Failed to update password')
      }
    } catch (error) {
      setPasswordMessage('Error connecting to server')
    }
  }

  const handleImageUpdate = async (e: React.FormEvent) => {
    e.preventDefault()
    setImageMessage('')

    try {
      const response = await fetch('http://localhost:8000/login/image', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: user.user_id,
          image_url: imageUrl
        })
      })

      const data = await response.json()
      
      if (response.ok) {
        setImageMessage('Profile image updated successfully!')
        setUser({ ...user, image_url: imageUrl })
      } else {
        setImageMessage(data.detail || 'Failed to update image')
      }
    } catch (error) {
      setImageMessage('Error connecting to server')
    }
  }

  const handlePaymentUpdate = async (e: React.FormEvent) => {
    e.preventDefault()
    setPaymentMessage('')

    try {
      const response = await fetch('http://localhost:8000/payment', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: user.user_id,
          card_number: cardNumber,
          CVV: cvv,
          expiration_date: expirationDate
        })
      })

      const data = await response.json()
      
      if (response.ok) {
        setPaymentMessage('Payment information updated successfully!')
        setCardNumber('')
        setCvv('')
        setExpirationDate('')
      } else {
        setPaymentMessage(data.detail || 'Failed to update payment information')
      }
    } catch (error) {
      setPaymentMessage('Error connecting to server')
    }
  }

  const fetchYearSummary = async () => {
    if (!user) return
    setYearSummaryLoading(true)
    try {
      const currentYear = new Date().getFullYear()
      const response = await fetch(`http://localhost:8000/summary/${user.user_id}/year/${currentYear}`)
      if (response.ok) {
        const data = await response.json()
        setYearSummary(data)
      }
    } catch (error) {
      console.error("Error fetching year summary:", error)
    } finally {
      setYearSummaryLoading(false)
    }
  }

  const toggleYearSummary = () => {
    if (!yearSummaryExpanded && !yearSummary) {
      fetchYearSummary()
    }
    setYearSummaryExpanded(!yearSummaryExpanded)
  }

  if (loading) {
    return <div>Loading...</div>
  }

  if (!user) {
    return (
      <div>
        <header>
          <div>
            <h1>User Profile</h1>
            <a href="/">Home</a>
          </div>
        </header>
        <div>
          <p>Please log in to view your profile</p>
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
            <h1>👤 User Profile</h1>
            <a href="/">🏠 Home</a>
          </div>
        </div>
      </header>

      {/* Profile Content */}
      <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto', color: "black" }}>
        {/* Navigation Buttons */}
        <div style={{ marginBottom: '20px' , backgroundColor: 'white'}}>
          {user.is_admin ? (
            <a href="/admin">👑 Admin Page</a>
          ) : (
            <>
              <a href="/wishlist">⭐ My Wishlist</a>
              <span style={{ margin: '0 10px' }}>|</span>
              <a href="/reviews">📝 My Reviews</a>
            </>
          )}
        </div>

        {/* Profile Info */}
        <div style={{ backgroundColor: 'white', padding: '20px', marginBottom: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
          <h2>{user.first_name} {user.last_name}</h2>
          <p>Email: {user.email}</p>
          <p>User ID: {user.user_id}</p>
          <p>Age: {user.age}</p>
          {user.is_admin && <p>Role: 👑 Administrator</p>}
          
          <div style={{ marginTop: '10px' }}>
            <img 
              src={imageError ? DEFAULT_IMAGE : (user.image_url || DEFAULT_IMAGE)} 
              alt="Profile" 
              style={{ maxWidth: '200px', borderRadius: '8px' }}
              onError={() => setImageError(true)}
            />
          </div>
        </div>

        {/* Year in Review */}
        {!user.is_admin && (
        <div style={{ backgroundColor: 'white', padding: '20px', marginBottom: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
          <div 
            onClick={toggleYearSummary}
            style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', cursor: 'pointer' }}
          >
            <h3 style={{ margin: 0 }}>📊 {new Date().getFullYear()} Year in Review</h3>
            <span style={{ fontSize: '20px' }}>{yearSummaryExpanded ? '▶' : '▲'}</span>
          </div>
          
          {yearSummaryExpanded && (
            <div style={{ marginTop: '15px', paddingTop: '15px', borderTop: '1px solid #eee' }}>
              {yearSummaryLoading ? (
                <p>Loading your year summary...</p>
              ) : yearSummary ? (
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '15px' }}>
                  <div style={{ backgroundColor: '#f8f9fa', padding: '15px', borderRadius: '8px', textAlign: 'center' }}>
                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#28a745' }}>${yearSummary.total_spent}</div>
                    <div style={{ fontSize: '14px', color: '#666' }}>Total Spent</div>
                  </div>
                  <div style={{ backgroundColor: '#f8f9fa', padding: '15px', borderRadius: '8px', textAlign: 'center' }}>
                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#007bff' }}>{yearSummary.total_orders}</div>
                    <div style={{ fontSize: '14px', color: '#666' }}>Orders Placed</div>
                  </div>
                  <div style={{ backgroundColor: '#f8f9fa', padding: '15px', borderRadius: '8px', textAlign: 'center' }}>
                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#17a2b8' }}>{yearSummary.items_purchased}</div>
                    <div style={{ fontSize: '14px', color: '#666' }}>Items Purchased</div>
                  </div>
                  <div style={{ backgroundColor: '#f8f9fa', padding: '15px', borderRadius: '8px', textAlign: 'center' }}>
                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#ffc107' }}>{yearSummary.reviews_written}</div>
                    <div style={{ fontSize: '14px', color: '#666' }}>Reviews Written</div>
                  </div>
                  <div style={{ backgroundColor: '#f8f9fa', padding: '15px', borderRadius: '8px', textAlign: 'center' }}>
                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#e83e8c' }}>👍 {yearSummary.likes_received}</div>
                    <div style={{ fontSize: '14px', color: '#666' }}>Likes Received</div>
                  </div>
                  <div style={{ backgroundColor: '#f8f9fa', padding: '15px', borderRadius: '8px', textAlign: 'center' }}>
                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#6f42c1' }}>${yearSummary.biggest_order}</div>
                    <div style={{ fontSize: '14px', color: '#666' }}>Biggest Order</div>
                  </div>
                  <div style={{ backgroundColor: '#f8f9fa', padding: '15px', borderRadius: '8px', textAlign: 'center' }}>
                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#20c997' }}>${yearSummary.avg_order_amount}</div>
                    <div style={{ fontSize: '14px', color: '#666' }}>Avg Order Amount</div>
                  </div>
                  <div style={{ backgroundColor: '#f8f9fa', padding: '15px', borderRadius: '8px', textAlign: 'center' }}>
                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#dc3545' }}>{yearSummary.orders_returned}</div>
                    <div style={{ fontSize: '14px', color: '#666' }}>Orders Returned</div>
                  </div>
                </div>
              ) : (
                <p>No activity this year yet.</p>
              )}
            </div>
          )}
        </div>
        )}

        {/* Update Profile Image */}
        <div style={{ backgroundColor: 'white', padding: '20px', marginBottom: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
          <h3>Update Profile Image</h3>
          <form onSubmit={handleImageUpdate}>
            <div style={{ marginBottom: '10px' }}>
              <label style={{ display: 'block', marginBottom: '5px', color: '#000' }}>Image URL</label>
              <input 
                type="text"
                value={imageUrl}
                onChange={(e) => setImageUrl(e.target.value)}
                placeholder="https://example.com/image.jpg"
                style={{ width: '100%', padding: '8px', border: '1px solid #ccc', borderRadius: '4px', color: '#000' }}
                required
              />
            </div>
            
            {imageMessage && (
              <div style={{ color: imageMessage.includes('success') ? 'green' : 'red', marginBottom: '10px', fontSize: '14px' }}>
                {imageMessage}
              </div>
            )}
            
            <button type="submit" style={{ padding: '8px 16px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
              Update Image
            </button>
          </form>
        </div>

        {/* Update Payment Information */}
        {user.is_admin ? null : (
        <div style={{ backgroundColor: 'white', padding: '20px', marginBottom: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
          <h3>Update Payment Information</h3>
          <form onSubmit={handlePaymentUpdate}>
            <div style={{ marginBottom: '10px' }}>
              <label style={{ display: 'block', marginBottom: '5px', color: '#000' }}>Card Number</label>
              <input 
                type="text"
                value={cardNumber}
                onChange={(e) => setCardNumber(e.target.value)}
                placeholder="1234567890123456"
                maxLength={19}
                style={{ width: '100%', padding: '8px', border: '1px solid #ccc', borderRadius: '4px', color: '#000' }}
                required
              />
            </div>
            
            <div style={{ marginBottom: '10px' }}>
              <label style={{ display: 'block', marginBottom: '5px', color: '#000' }}>CVV</label>
              <input 
                type="text"
                value={cvv}
                onChange={(e) => setCvv(e.target.value)}
                placeholder="123"
                maxLength={4}
                style={{ width: '100%', padding: '8px', border: '1px solid #ccc', borderRadius: '4px', color: '#000' }}
                required
              />
            </div>
            
            <div style={{ marginBottom: '10px' }}>
              <label style={{ display: 'block', marginBottom: '5px', color: '#000' }}>Expiration Date</label>
              <input 
                type="text"
                value={expirationDate}
                onChange={(e) => setExpirationDate(e.target.value)}
                placeholder="MM/YY"
                style={{ width: '100%', padding: '8px', border: '1px solid #ccc', borderRadius: '4px', color: '#000' }}
                required
              />
            </div>
            
            {paymentMessage && (
              <div style={{ color: paymentMessage.includes('success') ? 'green' : 'red', marginBottom: '10px', fontSize: '14px' }}>
                {paymentMessage}
              </div>
            )}
            
            <button type="submit" style={{ padding: '8px 16px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
              Update Payment
            </button>
          </form>
        </div>
        )}

        {/* Update Password */}
        <div style={{ backgroundColor: 'white', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
          <h3>Update Password</h3>
          <form onSubmit={handlePasswordUpdate}>
            <div style={{ marginBottom: '10px' }}>
              <label style={{ display: 'block', marginBottom: '5px', color: '#000' }}>Old Password</label>
              <input 
                type="password"
                value={oldPassword}
                onChange={(e) => setOldPassword(e.target.value)}
                style={{ width: '100%', padding: '8px', border: '1px solid #ccc', borderRadius: '4px', color: '#000' }}
                required
              />
            </div>
            
            <div style={{ marginBottom: '10px' }}>
              <label style={{ display: 'block', marginBottom: '5px', color: '#000' }}>New Password</label>
              <input 
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                style={{ width: '100%', padding: '8px', border: '1px solid #ccc', borderRadius: '4px', color: '#000' }}
                required
              />
            </div>
            
            <div style={{ marginBottom: '10px' }}>
              <label style={{ display: 'block', marginBottom: '5px', color: '#000' }}>Confirm New Password</label>
              <input 
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                style={{ width: '100%', padding: '8px', border: '1px solid #ccc', borderRadius: '4px', color: '#000' }}
                required
              />
            </div>
            
            {passwordMessage && (
              <div style={{ color: passwordMessage.includes('success') ? 'green' : 'red', marginBottom: '10px', fontSize: '14px' }}>
                {passwordMessage}
              </div>
            )}
            
            <button type="submit" style={{ padding: '8px 16px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
              Update Password
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}
