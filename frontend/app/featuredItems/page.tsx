'use client'

import { useState, useEffect } from 'react'
import LoginButton from '../components/LoginButton'

export default function FeaturedItems() {
  const [featuredProducts, setFeaturedProducts] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [allFeaturedProducts, setAllFeaturedProducts] = useState<any[]>([])

  useEffect(() => {
    fetchFeaturedProducts()
  }, [])

  const fetchFeaturedProducts = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      
      // Get featured product IDs
      const featuredResponse = await fetch(`${apiUrl}/featured`)
      const featuredData = await featuredResponse.json()
      const productIds = featuredData.featured_product_ids

      if (productIds.length === 0) {
        setFeaturedProducts([])
        setLoading(false)
        return
      }

      // Get all products
      const productsResponse = await fetch(`${apiUrl}/products`)
      const allProducts = await productsResponse.json()

      // Filter to get only featured products
      const featured = allProducts.filter((p: any) => 
        productIds.includes(p._product_id.toString())
      )

      setAllFeaturedProducts(featured)
      setFeaturedProducts(featured)
    } catch (error) {
      console.error("Error fetching featured products:", error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (search === '') {
      setFeaturedProducts(allFeaturedProducts)
    } else {
      const filtered = allFeaturedProducts.filter((p: any) =>
        p._product_name.toLowerCase().includes(search.toLowerCase())
      )
      setFeaturedProducts(filtered)
    }
  }, [search, allFeaturedProducts])

  const handleSearch = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    const query = formData.get('query') as string
    setSearch(query)
  }

  const addToCart = async (product: any) => {
    const userEmail = localStorage.getItem('userEmail')
    if (!userEmail) {
      alert('Please log in to add items to cart')
      return
    }

    const quantity = prompt('Enter quantity:', '1')
    if (!quantity || parseInt(quantity) <= 0) return

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const usersResponse = await fetch(`${apiUrl}/login/users`)
      const users = await usersResponse.json()
      const currentUser = users.find((u: any) => u.email === userEmail)

      if (!currentUser) {
        alert('User not found')
        return
      }

      if (currentUser.is_admin) {
        alert('Admins cannot add items to cart')
        return
      }

      const response = await fetch(`${apiUrl}/cart/cart/items`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: currentUser.user_id,
          product_id: parseInt(product._product_id),
          product_name: product._product_name,
          product_desc: product._product_desc,
          price: product._price,
          quantity: parseInt(quantity)
        })
      })

      if (response.ok) {
        alert('Item added to cart!')
      } else {
        const errorData = await response.json()
        alert(errorData.detail || 'Failed to add item to cart')
      }
    } catch (error) {
      console.error("Error adding to cart:", error)
      alert('Error adding to cart')
    }
  }

  const addToWishlist = async (product: any) => {
    const userEmail = localStorage.getItem('userEmail')
    if (!userEmail) {
      alert('Please log in to add items to wishlist')
      return
    }

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const usersResponse = await fetch(`${apiUrl}/login/users`)
      const users = await usersResponse.json()
      const currentUser = users.find((u: any) => u.email === userEmail)

      if (!currentUser) {
        alert('User not found')
        return
      }

      if (currentUser.is_admin) {
        alert('Admins cannot add items to wishlist')
        return
      }

      const response = await fetch(`${apiUrl}/wishlist/items`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: currentUser.user_id,
          product_id: parseInt(product._product_id)
        })
      })

      if (response.ok) {
        alert('Item added to wishlist!')
      } else {
        const errorData = await response.json()
        alert(errorData.detail || 'Failed to add item to wishlist')
      }
    } catch (error) {
      console.error("Error adding to wishlist:", error)
      alert('Error adding to wishlist')
    }
  }

  if (loading) {
    return <div>Loading...</div>
  }

  return (
    <div style={{ padding: '20px' }}>
      <h1>ProjectMIA Online Shop</h1>
    
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <a href="/">🏠 Home</a>
        <LoginButton />
      </div>

      <form onSubmit={handleSearch}>
        <label htmlFor="search">Search products:</label>
        <input 
          id="search" 
          name="query" 
          defaultValue={search}
          placeholder="Enter product name..."
        />
        <button type="submit">Search</button>
      </form>

      <br /><br />

      <h1>Featured Items:</h1>

      {featuredProducts.length === 0 ? (
        <p>No featured items available at this time.</p>
      ) : (
        <ul>
          {featuredProducts.map((item: any) => (
            <li key={item._product_id}>
              <strong>{item._product_name}</strong><br />
              {item._product_desc}<br />
              Price: ${item._price.toFixed(2)}<br />
              Rating: {item._rating.toFixed(1)} ({item._rating_count} reviews)<br />
              Units sold: {item._units_sold}<br />
              <button onClick={() => addToCart(item)}>Add to Cart</button><br />
              <button onClick={() => addToWishlist(item)}>Add to Wishlist</button><br />
              <a href={`/addReviews?productId=${item._product_id}`}>
                <button>Review</button>
              </a>
              <hr />
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
