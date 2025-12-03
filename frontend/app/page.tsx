'use client'

import { useState, useEffect } from 'react'
import Form from 'next/form'
import LoginButton from './components/LoginButton'

export default function Home() {
  const [products, setProducts] = useState<any[]>([])
  const [popularItems, setPopularItems] = useState<any[]>([])
  const [search, setSearch] = useState('')
  const [page, setPage] = useState(1)
  const [totalMatches, setTotalMatches] = useState(0)
  const [totalPages, setTotalPages] = useState(1)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchProducts(search, page)
    fetchPopular()
  }, [search, page])

  const fetchProducts = async (searchTerm: string, pageNum: number) => {
    try {
      const keyword = searchTerm || ''
      const response = await fetch(`http://localhost:8000/products?keyword=${keyword}`)
      const allProducts = await response.json()
      
      const itemsPerPage = 50
      const startIndex = (pageNum - 1) * itemsPerPage
      const endIndex = startIndex + itemsPerPage
      
      const paginatedProducts = allProducts.slice(startIndex, endIndex)
      const total = allProducts.length
      const pages = Math.ceil(total / itemsPerPage)
      
      setProducts(paginatedProducts)
      setTotalMatches(total)
      setTotalPages(pages || 1)
    } catch (error) {
      console.error("Error fetching products:", error)
    } finally {
      setLoading(false)
    }
  }

  const fetchPopular = async () => {
    try {
      const response = await fetch('http://localhost:8000/products/popularProducts')
      const data = await response.json()
      setPopularItems(data)
    } catch (error) {
      console.error("Error fetching popular items:", error)
    }
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
      // Get user ID
      const usersResponse = await fetch(`http://localhost:8000/login/users`)
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

      // Add to cart
      const response = await fetch(`http://localhost:8000/cart/cart/items`, {
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
      // Get user ID
      const usersResponse = await fetch(`http://localhost:8000/login/users`)
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

      // Add to wishlist
      const response = await fetch(`http://localhost:8000/wishlist/items`, {
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
        alert('Failed to add item to wishlist')
      }
    } catch (error) {
      console.error("Error adding to wishlist:", error)
      alert('Error adding to wishlist')
    }
  }

  const handleSearch = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    const query = formData.get('query') as string
    setSearch(query)
    setPage(1)
  }

  if (loading) {
    return <div>Loading...</div>
  }

  const hasPrevious = page > 1
  const hasNext = page < totalPages

  return (
    <div>
      <h1>ProjectMIA Online Shop</h1>
    
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px 16px' }}>
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

      <h1>Popular Items: </h1>
      {popularItems.map((pop_item: any) => (
          <li key={pop_item._product_name}>
          <strong>{pop_item._product_name}</strong><br />
            <hr />
          </li>
        ))}

      <br /><br />

      <p>Showing {products.length} out of {totalMatches} products (Page {page} of {totalPages})</p>

      <div style={{ marginBottom: '10px' }}>
        {hasPrevious ? (
          <a href="#" onClick={(e) => { e.preventDefault(); setPage(page - 1) }}>← Previous</a>
        ) : (
          <span style={{ color: '#999' }}>← Previous</span>
        )}
        {' | '}
        {hasNext ? (
          <a href="#" onClick={(e) => { e.preventDefault(); setPage(page + 1) }}>Next →</a>
        ) : (
          <span style={{ color: '#999' }}>Next →</span>
        )}
      </div>

      <ul>
        {products.map((item: any) => (
          <li key={item._product_id}>
            <strong>{item._product_name}</strong><br />
            {item._product_desc}<br />
            Price: ${item._price.toFixed(2)}<br />
            Rating: {item._rating.toFixed(1)} ({item._rating_count} reviews)<br />
            Units sold: {item._units_sold}<br />
            <button onClick={() => addToCart(item)}>Add to Cart</button><br />
            <button onClick={() => addToWishlist(item)}>Add to Wishlist</button>
            <hr />
          </li>
        ))}
      </ul>

      <div style={{ marginTop: '10px' }}>
        {hasPrevious ? (
          <a href="#" onClick={(e) => { e.preventDefault(); setPage(page - 1) }}>← Previous</a>
        ) : (
          <span style={{ color: '#999' }}>← Previous</span>
        )}
        {' | '}
        {hasNext ? (
          <a href="#" onClick={(e) => { e.preventDefault(); setPage(page + 1) }}>Next →</a>
        ) : (
          <span style={{ color: '#999' }}>Next →</span>
        )}
      </div>
    </div> 
  )
}