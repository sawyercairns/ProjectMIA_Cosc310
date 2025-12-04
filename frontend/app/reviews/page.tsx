'use client'

import { useState, useEffect, ChangeEvent, FormEvent } from 'react'

export default function ReviewsPage() {
  const [user, setUser] = useState<any>(null)
  const [reviews, setReviews] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [editingReviewId, setEditingReviewId] = useState<string | null>(null)
  const [editForm, setEditForm] = useState({ rating: '', title: '', body: '' })
  const [processingReviewId, setProcessingReviewId] = useState<string | null>(null)
  const [savingEdit, setSavingEdit] = useState(false)

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
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/login/users`)
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
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/reviews/${userId}`)
      if (!response.ok) {
        setLoading(false)
        return
      }
      const userReviews = await response.json()
      
      // Fetch product details for each review
      const reviewsWithProducts = await Promise.all(
        userReviews.map(async (review: any) => {
          try {
            const productResponse = await fetch(`${apiUrl}/products/${review.product_id}`)
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

  const startEditingReview = (review: any) => {
    setEditingReviewId(String(review.review_id))
    setEditForm({
      rating: review.rating?.toString() ?? '',
      title: review.title ?? '',
      body: review.body ?? ''
    })
  }

  const handleEditInputChange = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setEditForm((prev) => ({ ...prev, [name]: value }))
  }

  const handleSaveReview = async (event: FormEvent<HTMLFormElement>, review: any) => {
    event.preventDefault()
    if (!user) return

    const ratingValue = parseFloat(editForm.rating)
    if (Number.isNaN(ratingValue) || ratingValue < 1 || ratingValue > 5) {
      alert('Rating must be between 1 and 5')
      return
    }

    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    setSavingEdit(true)
    try {
      const response = await fetch(`${apiUrl}/reviews/${review.review_id}?user_id=${user.user_id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          rating: ratingValue,
          title: editForm.title,
          body: editForm.body
        })
      })

      if (response.ok) {
        alert('Review updated successfully!')
        setEditingReviewId(null)
        await fetchUserReviews(user.user_id)
      } else {
        const errorText = await response.text()
        alert(errorText || 'Failed to update review')
      }
    } catch (error) {
      console.error('Error updating review:', error)
      alert('Error updating review')
    } finally {
      setSavingEdit(false)
    }
  }

  const handleDeleteReview = async (reviewId: string) => {
    if (!user) return
    if (!window.confirm('Are you sure you want to delete this review?')) return

    const password = prompt('Enter your password to delete this review')
    if (!password) return

    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    setProcessingReviewId(String(reviewId))
    try {
      const response = await fetch(`${apiUrl}/reviews/${reviewId}?email=${encodeURIComponent(user.email)}&password=${encodeURIComponent(password)}`, {
        method: 'DELETE'
      })
      if (response.ok) {
        alert('Review deleted successfully')
        setReviews((prev) => prev.filter((review) => String(review.review_id) !== String(reviewId)))
      } else {
        const errorText = await response.text()
        alert(errorText || 'Failed to delete review')
      }
    } catch (error) {
      console.error('Error deleting review:', error)
      alert('Error deleting review')
    } finally {
      setProcessingReviewId(null)
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
              <div style={{ marginTop: '15px', display: 'flex', gap: '10px' }}>
                <button onClick={() => startEditingReview(review)}>
                  {editingReviewId === String(review.review_id) ? 'Close Editor' : 'Update Review'}
                </button>
                <button
                  onClick={() => handleDeleteReview(String(review.review_id))}
                  disabled={processingReviewId === String(review.review_id)}
                  style={{color: '#000000' }}
                >
                  {processingReviewId === String(review.review_id) ? 'Deleting...' : 'Delete Review'}
                </button>
              </div>

              {editingReviewId === String(review.review_id) && (
                <form onSubmit={(event) => handleSaveReview(event, review)} style={{ marginTop: '15px', padding: '15px', border: '1px solid #eee', borderRadius: '6px', backgroundColor: '#f9f9f9' }}>
                  <div style={{ marginBottom: '10px' }}>
                    <label>
                      Rating (1-5):
                      <input
                        type="number"
                        name="rating"
                        min="1"
                        max="5"
                        step="0.1"
                        value={editForm.rating}
                        onChange={handleEditInputChange}
                        required
                      />
                    </label>
                  </div>
                  <div style={{ marginBottom: '10px' }}>
                    <label>
                      Title:
                      <input
                        type="text"
                        name="title"
                        value={editForm.title}
                        onChange={handleEditInputChange}
                        required
                      />
                    </label>
                  </div>
                  <div style={{ marginBottom: '10px' }}>
                    <label>
                      Review:
                      <textarea
                        name="body"
                        rows={3}
                        value={editForm.body}
                        onChange={handleEditInputChange}
                        required
                      />
                    </label>
                  </div>
                  <div style={{ display: 'flex', gap: '10px' }}>
                    <button type="button" onClick={() => setEditingReviewId(null)}>
                      Cancel
                    </button>
                    <button type="submit" disabled={savingEdit} style={{ backgroundColor: '#4CAF50', color: '#fff' }}>
                      {savingEdit ? 'Saving...' : 'Save Changes'}
                    </button>
                  </div>
                </form>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  )
}
