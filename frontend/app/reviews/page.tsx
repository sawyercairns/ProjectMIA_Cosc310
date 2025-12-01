'use client'

import { useState, useEffect } from 'react'

export default function ReviewsPage() {
  const [user, setUser] = useState<any>(null)
  const [reviews, setReviews] = useState<any[]>([])
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
        fetchUserReviews(currentUser.user_id)
      }
    } catch (error) {
      console.error("Error fetching user:", error)
      setLoading(false)
    }
  }

  const fetchUserReviews = async (userId: string) => {
    try {
      const response = await fetch(`http://localhost:8000/review`)
      if (!response.ok) {
        setLoading(false)
        return
      }
      const allReviews = await response.json()
      const userReviews = allReviews.filter((r: any) => r.user_id === userId)
      setReviews(userReviews)
    } catch (error) {
      console.error("Error fetching reviews:", error)
    } finally {
      setLoading(false)
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
            <h1>My Reviews</h1>
            <a href="/">Home</a>
          </div>
        </header>
        <div>
          <p>Please log in to view your reviews</p>
        </div>
      </div>
    )
  }

  return (
    <div>
      {/* Header */}
      <header>
        <div>
          <div>
            <h1>📝 My Reviews</h1>
            <a href="/">🏠 Home</a>
          </div>
        </div>
      </header>

      {/* Reviews Content */}
      <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto', color: "black" }}>
        {/* Navigation Links */}
        <div style={{ marginBottom: '20px' , backgroundColor: 'white' }}>
          <a href="/profile">👤 Profile</a>
          <span style={{ margin: '0 10px' }}>|</span>
          <a href="/wishlist">⭐My Wishlist</a>
        </div>

        {/* User Info */}
        <div style={{ backgroundColor: 'white', padding: '20px', marginBottom: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
          <h2>{user.first_name} {user.last_name}'s Reviews</h2>
          <p>Total Reviews: {reviews.length}</p>
        </div>

        {/* Reviews List */}
        {reviews.length === 0 ? (
          <div style={{ backgroundColor: 'white', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
            <p>You haven't written any reviews yet.</p>
          </div>
        ) : (
          reviews.map((review) => (
            <div key={review.review_id} style={{ backgroundColor: 'white', padding: '20px', marginBottom: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
              <div style={{ marginBottom: '10px' }}>
                <strong>Product ID:</strong> {review.product_id}
              </div>
              <div style={{ marginBottom: '10px' }}>
                <strong>Rating:</strong> {'⭐'.repeat(review.rating)} ({review.rating}/5)
              </div>
              <div style={{ marginBottom: '10px' }}>
                <strong>Review:</strong>
                <p style={{ marginTop: '5px' }}>{review.review_text}</p>
              </div>
              <div style={{ fontSize: '12px', color: '#666' }}>
                <strong>Date:</strong> {new Date(review.review_date).toLocaleDateString()}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
