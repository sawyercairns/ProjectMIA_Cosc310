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
      const response = await fetch(`http://localhost:8000/reviews/${userId}`)
      if (!response.ok) {
        setLoading(false)
        return
      }
      const userReviews = await response.json()
      
      // Fetch product details for each review
      const reviewsWithProducts = await Promise.all(
        userReviews.map(async (review: any) => {
          try {
            const productResponse = await fetch(`http://localhost:8000/products/${review.product_id}`)
            if (productResponse.ok) {
              const product = await productResponse.json()
              return {
                ...review,
                product_name: product.product_name
              }
            }
          } catch (error) {
            console.error(`Error fetching product ${review.product_id}:`, error)
          }
          return {
            ...review,
            product_name: 'Unknown Product'
          }
        })
      )
      
      setReviews(reviewsWithProducts)
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
    <div style={{ padding: '20px' }}>
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
                <strong>Name:</strong> {review.product_name}
              </div>
              <div style={{ marginBottom: '10px' }}>
                <strong>Rating:</strong> {'⭐'.repeat(Math.floor(review.rating))} ({review.rating}/5)
              </div>
              <div style={{ marginBottom: '10px' }}>
                <strong>Title:</strong> {review.title}
              </div>
              <div style={{ marginBottom: '10px' }}>
                <strong>Review:</strong>
                <p style={{ marginTop: '5px' }}>{review.body}</p>
              </div>
              <div style={{ marginBottom: '10px' }}>
                <strong>Likes:</strong> 👍 {review.likes}
              </div>
              <div style={{ fontSize: '12px', color: '#666' }}>
                <strong>Date:</strong> {new Date(review.created_at).toLocaleDateString()}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
