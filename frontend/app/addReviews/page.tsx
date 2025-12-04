'use client'

import { useState, useEffect } from 'react'
import { useSearchParams } from 'next/navigation'
import LoginButton from '../components/LoginButton'

export default function AddReviews() {
  const searchParams = useSearchParams()
  const productId = searchParams.get('productId')
  
  const [product, setProduct] = useState<any>(null)
  const [reviews, setReviews] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [userEmail, setUserEmail] = useState('')
  const [currentUserId, setCurrentUserId] = useState('')
  const [hasPurchased, setHasPurchased] = useState(false)
  const [hasReviewed, setHasReviewed] = useState(false)

  useEffect(() => {
    const email = localStorage.getItem('userEmail')
    if (email) {
      setUserEmail(email)
      checkUserAndFetchData(email)
    } else {
      fetchProductAndReviews()
    }
  }, [productId])

  const checkUserAndFetchData = async (email: string) => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      
      const usersResponse = await fetch(`${apiUrl}/login/users`)
      const users = await usersResponse.json()
      const currentUser = users.find((u: any) => u.email === email)
      
      if (currentUser) {
        setCurrentUserId(currentUser.user_id)
        

        const ordersResponse = await fetch(`${apiUrl}/orders?user_id=${currentUser.user_id}`)
        const ordersData = await ordersResponse.json()
        
    
        const purchased = ordersData.orders && ordersData.orders.some((order: any) => 
          order.order_items && order.order_items.some((item: any) => 
            item.product_id.toString() === productId
          )
        )
        setHasPurchased(purchased)
        
    
        const reviewsResponse = await fetch(`${apiUrl}/reviews/${currentUser.user_id}`)
        const userReviews = await reviewsResponse.json()
        const alreadyReviewed = userReviews.some((review: any) => 
          review.product_id.toString() === productId
        )
        setHasReviewed(alreadyReviewed)
      }
      
      fetchProductAndReviews()
    } catch (error) {
      console.error("Error checking user data:", error)
      fetchProductAndReviews()
    }
  }

  const fetchProductAndReviews = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      
      // Get product details
      const productsResponse = await fetch(`${apiUrl}/products`)
      const allProducts = await productsResponse.json()
      const productData = allProducts.find((p: any) => p._product_id.toString() === productId)
      setProduct(productData)

      // Get all reviews and filter by product
      const reviewsResponse = await fetch(`${apiUrl}/reviews/all`)
      const allReviews = await reviewsResponse.json()
      const productReviews = allReviews.filter((r: any) => r.product_id.toString() === productId)
      setReviews(productReviews)
    } catch (error) {
      console.error("Error fetching data:", error)
    } finally {
      setLoading(false)
    }
  }

  const submitReview = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    
    if (!userEmail) {
      alert('Please log in to leave a review')
      return
    }

    if (!hasPurchased) {
      alert('You must purchase this product before leaving a review')
      return
    }

    if (hasReviewed) {
      alert('You have already reviewed this product')
      return
    }

    const formData = new FormData(e.currentTarget)
    const rating = formData.get('rating') as string
    const title = formData.get('title') as string
    const body = formData.get('body') as string

    if (!rating || !title || !body) {
      alert('Please fill in all fields')
      return
    }

    let submissionSucceeded = false

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/reviews?user_id=${currentUserId}&product_id=${productId}&rating=${rating}&title=${encodeURIComponent(title)}&body=${encodeURIComponent(body)}`, {
        method: 'POST'
      })

      if (response.ok) {
        submissionSucceeded = true
        alert('Review submitted successfully!')
        setHasReviewed(true)
    
        e.currentTarget.reset()
       
        try {
          await fetchProductAndReviews()
        } catch (refreshError) {
          console.error("Error refreshing reviews:", refreshError)
        }
      } else {
        
        try {
          const errorData = await response.json()
          alert(errorData.detail || 'Failed to submit review')
        } catch {
          const errorText = await response.text()
          alert(errorText || 'Failed to submit review')
        }
      }
    } catch (error) {
      console.error("Error submitting review:", error)
      if (!submissionSucceeded) {
        alert('Error submitting review')
      }
    }
  }

  if (loading) {
    return <div style={{ padding: '20px' }}>Loading...</div>
  }

  if (!product) {
    return (
      <div style={{ padding: '20px' }}>
        <h1>Product Not Found</h1>
        <a href="/">← Back to Home</a>
      </div>
    )
  }

  return (
    <div style={{ padding: '20px' }}>
      <h1>Reviews for {product._product_name}</h1>
      
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <a href="/">🏠 Home</a>
        <LoginButton />
      </div>

      <div style={{ marginBottom: '30px', padding: '15px', border: '1px solid #ddd', borderRadius: '5px' }}>
        <h2>{product._product_name}</h2>
        <p>{product._product_desc}</p>
        <p><strong>Price:</strong> ${product._price.toFixed(2)}</p>
        <p><strong>Rating:</strong> {product._rating.toFixed(1)} ({product._rating_count} reviews)</p>
      </div>

      <h2>Leave a Review</h2>
      {!userEmail ? (
        <p style={{ color: '#666', marginBottom: '20px' }}>Please log in to leave a review.</p>
      ) : !hasPurchased ? (
        <p style={{ color: '#666', marginBottom: '20px' }}>You must purchase this product before leaving a review.</p>
      ) : hasReviewed ? (
        <p style={{ color: '#666', marginBottom: '20px' }}>You have already reviewed this product.</p>
      ) : (
        <form onSubmit={submitReview} style={{ marginBottom: '30px' }}>
          <div style={{ marginBottom: '10px' }}>
            <label htmlFor="rating">Rating (0-5):</label><br />
            <input 
              id="rating" 
              name="rating" 
              type="number" 
              min="0" 
              max="5" 
              step="0.5" 
              required 
              style={{ padding: '5px', width: '100px', backgroundColor: '#f9f9f9', color: 'black'  }}
            />
          </div>
          
          <div style={{ marginBottom: '10px' }}>
            <label htmlFor="title">Title:</label><br />
            <input 
              id="title" 
              name="title" 
              type="text" 
              required 
              style={{ padding: '5px', width: '100%', maxWidth: '500px', backgroundColor: '#f9f9f9', color: 'black'  }}
            />
          </div>
          
          <div style={{ marginBottom: '10px' }}>
            <label htmlFor="body">Review:</label><br />
            <textarea 
              id="body" 
              name="body" 
              required 
              rows={5}
              style={{ padding: '5px', width: '100%', maxWidth: '500px', backgroundColor: '#f9f9f9', color: 'black'  }}
            />
          </div>
          
          <button type="submit" style={{ padding: '10px 20px', backgroundColor: '#f9f9f9', color: 'black' }}>Submit Review</button>
        </form>
      )}

      <h2>All Reviews ({reviews.length})</h2>
      {reviews.length === 0 ? (
        <p>No reviews yet. Be the first to review this product!</p>
      ) : (
        <ul>
          {reviews.map((review: any) => (
            <li key={review.review_id} style={{ marginBottom: '20px', padding: '15px', border: '1px solid #ddd', borderRadius: '5px' }}>
              <strong>{review.title}</strong> - Rating: {review.rating}/5<br />
              <small>User ID: {review.user_id} | Date: {review.created_at}</small><br />
              <p style={{ marginTop: '10px' }}>{review.body}</p>
              <small>👍 {review.likes} likes</small>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
