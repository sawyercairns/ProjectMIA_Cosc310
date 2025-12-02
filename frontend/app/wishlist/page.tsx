'use client'

import { useState, useEffect } from 'react'

export default function WishlistPage() {
  const [user, setUser] = useState<any>(null)
  const [wishlistItems, setWishlistItems] = useState<any[]>([])
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
        fetchWishlist(currentUser.user_id)
      }
    } catch (error) {
      console.error("Error fetching user:", error)
      setLoading(false)
    }
  }

  const fetchWishlist = async (userId: string) => {
    try {
      const response = await fetch(`http://localhost:8000/wishlist?user_id=${userId}`)
      if (!response.ok) {
        console.error("Failed to fetch wishlist, status:", response.status)
        setLoading(false)
        return
      }
      const wishlist = await response.json()
      console.log("Wishlist response:", wishlist)
      console.log("Wishlist items:", wishlist.entries)
      
      // Fetch product details for each wishlist item
      const itemsWithDetails = await Promise.all(
        (wishlist.entries || []).map(async (entry: any) => {
          try {
            console.log(`Fetching product ${entry.product_id}...`)
            const productResponse = await fetch(`http://localhost:8000/products/${entry.product_id}`)
            console.log(`Product ${entry.product_id} response status:`, productResponse.status)
            if (productResponse.ok) {
              const product = await productResponse.json()
              console.log(`Product ${entry.product_id} data:`, product)
              return {
                product_id: entry.product_id,
                date_added: entry.date_added,
                product_name: product.product_name,
                price: product.actual_price
              }
            }
          } catch (error) {
            console.error(`Error fetching product ${entry.product_id}:`, error)
          }
          return {
            product_id: entry.product_id,
            date_added: entry.date_added,
            product_name: 'N/A',
            price: 'N/A'
          }
        })
      )
      
      console.log("Final items with details:", itemsWithDetails)
      setWishlistItems(itemsWithDetails)
    } catch (error) {
      console.error("Error fetching wishlist:", error)
    } finally {
      setLoading(false)
    }
  }

  const removeFromWishlist = async (productId: string) => {
    try {
      const response = await fetch(`http://localhost:8000/wishlist/users/${user.user_id}/items/${productId}`, {
        method: 'DELETE'
      })

      if (response.ok) {
        setWishlistItems(wishlistItems.filter(item => item.product_id !== productId))
      }
    } catch (error) {
      console.error("Error removing item:", error)
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
            <h1>My Wishlist</h1>
            <a href="/">Home</a>
          </div>
        </header>
        <div>
          <p>Please log in to view your wishlist</p>
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
            <h1>⭐ My Wishlist</h1>
            <a href="/">🏠 Home</a>
          </div>
        </div>
      </header>

      {/* Wishlist Content */}
      <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto', color: "black" }}>
        {/* Navigation Links */}
        <div style={{ marginBottom: '20px' , backgroundColor: 'white' }}>
          <a href="/profile">👤 Profile</a>
          <span style={{ margin: '0 10px' }}>|</span>
          <a href="/reviews">📝My Reviews</a>
        </div>

        {/* User Info */}
        <div style={{ backgroundColor: 'white', padding: '20px', marginBottom: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
          <h2>{user.first_name} {user.last_name}'s Wishlist</h2>
          <p>Total Items: {wishlistItems.length}</p>
          <p>Note: 10 items max in wishlist.</p>
        </div>

        {/* Wishlist Items */}
        {wishlistItems.length === 0 ? (
          <div style={{ backgroundColor: 'white', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
            <p>Your wishlist is empty.</p>
          </div>
        ) : (
          wishlistItems.map((item) => (
            <div key={item.product_id} style={{ backgroundColor: 'white', padding: '20px', marginBottom: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                <div style={{ flex: 1 }}>
                  <div style={{ marginBottom: '10px' }}>
                    <strong>Product ID:</strong> {item.product_id}
                  </div>
                  <div style={{ marginBottom: '10px' }}>
                    <strong>Product Name:</strong> {item.product_name || 'N/A'}
                  </div>
                  <div style={{ marginBottom: '10px' }}>
                    <strong>Price:</strong> ${item.price || 'N/A'}
                  </div>
                  <div style={{ fontSize: '12px', color: '#666' }}>
                    <strong>Added:</strong> {item.date_added ? new Date(item.date_added).toLocaleDateString() : 'N/A'}
                  </div>
                </div>
                <button 
                  onClick={() => removeFromWishlist(item.product_id)}
                  style={{ 
                    padding: '8px 16px', 
                    backgroundColor: '#dc3545', 
                    color: 'white', 
                    border: 'none', 
                    borderRadius: '4px', 
                    cursor: 'pointer' 
                  }}
                >
                  Remove
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
