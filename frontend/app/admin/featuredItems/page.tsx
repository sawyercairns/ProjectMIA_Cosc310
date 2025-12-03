'use client'

import { useState, useEffect } from 'react'

export default function AdminFeaturedItems() {
  const [allProducts, setAllProducts] = useState<any[]>([])
  const [featuredProductIds, setFeaturedProductIds] = useState<string[]>([])
  const [searchTerm, setSearchTerm] = useState('')
  const [loading, setLoading] = useState(true)
  const [userEmail, setUserEmail] = useState('')
  const [accessDenied, setAccessDenied] = useState(false)
  const [currentPage, setCurrentPage] = useState(1)
  const productsPerPage = 20

  useEffect(() => {
    const email = localStorage.getItem('userEmail')
    if (!email) {
      setAccessDenied(true)
      setLoading(false)
      return
    }
    setUserEmail(email)
    checkAdminAndFetchData(email)
  }, [])

  const checkAdminAndFetchData = async (email: string) => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      
      // Check if user is admin
      const usersResponse = await fetch(`${apiUrl}/login/users`)
      const users = await usersResponse.json()
      const currentUser = users.find((u: any) => u.email === email)
      
      if (!currentUser || !currentUser.is_admin) {
        setAccessDenied(true)
        setLoading(false)
        return
      }
      
      fetchData()
    } catch (error) {
      console.error("Error checking admin status:", error)
      setAccessDenied(true)
      setLoading(false)
    }
  }

  const fetchData = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      
      // Fetch all products
      const productsResponse = await fetch(`${apiUrl}/products`)
      const products = await productsResponse.json()
      setAllProducts(products)

      // Fetch featured product IDs
      const featuredResponse = await fetch(`${apiUrl}/featured`)
      const featuredData = await featuredResponse.json()
      setFeaturedProductIds(featuredData.featured_product_ids || [])
    } catch (error) {
      console.error("Error fetching data:", error)
      alert('Error loading data')
    } finally {
      setLoading(false)
    }
  }

  const addToFeatured = async (productId: string) => {
    if (!confirm('Add this product to featured items?')) return

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/featured`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          product_id: productId,
          admin_email: userEmail
        })
      })

      if (response.ok) {
        alert('Product added to featured items!')
        fetchData() // Refresh data
      } else {
        const errorData = await response.json()
        alert(errorData.detail || 'Failed to add to featured items')
      }
    } catch (error) {
      console.error("Error adding to featured:", error)
      alert('Error adding to featured items')
    }
  }

  const removeFromFeatured = async (productId: string) => {
    if (!confirm('Remove this product from featured items?')) return

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/featured/${productId}?admin_email=${userEmail}`, {
        method: 'DELETE'
      })

      if (response.ok) {
        alert('Product removed from featured items!')
        fetchData() // Refresh data
      } else {
        const errorData = await response.json()
        alert(errorData.detail || 'Failed to remove from featured items')
      }
    } catch (error) {
      console.error("Error removing from featured:", error)
      alert('Error removing from featured items')
    }
  }

  const filteredProducts = allProducts.filter(product =>
    product._product_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    product._product_id.toString().includes(searchTerm)
  )

  const totalPages = Math.ceil(filteredProducts.length / productsPerPage)
  const paginatedProducts = filteredProducts.slice((currentPage - 1) * productsPerPage, currentPage * productsPerPage)

  const isFeatured = (productId: string) => featuredProductIds.includes(productId)

  if (accessDenied) {
    return (
        <div>
        <header>
          <div>
            <h1>Featured Items Management</h1>
            <a href="/">🏠 Home</a>
          </div>
        </header>
        <div>
          <p>Please log in as an admin to make changes to this page.</p>
        </div>
      </div>
    )
  }

  return (
    <div style={{ padding: '20px' }}>
      <h1>⭐ Featured Items Management</h1>
      
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
        <a href="/">🏠 Home</a>
        <a href="/admin">👑 Admin Dashboard</a>
      </div>

      <h2>All Products</h2>
      
      <label htmlFor="search">Search by name or ID:</label>
      <input
        id="search"
        type="text"
        value={searchTerm}
        onChange={(e) => {
          setSearchTerm(e.target.value)
          setCurrentPage(1)
        }}
        placeholder="Enter name or ID..."
      />
      
      <br /><br />

      {loading ? (
        <p>Loading products...</p>
      ) : (
        <div>
          <p>Showing {paginatedProducts.length} out of {filteredProducts.length} products (Page {currentPage} of {totalPages || 1})</p>
          <p style={{ marginBottom: '10px' }}>
            Currently {featuredProductIds.length} featured item{featuredProductIds.length !== 1 ? 's' : ''}
          </p>

          <div style={{ marginBottom: '10px' }}>
            {currentPage > 1 ? (
              <a href="#" onClick={(e) => { e.preventDefault(); setCurrentPage(currentPage - 1) }}>← Previous</a>
            ) : (
              <span style={{ color: '#999' }}>← Previous</span>
            )}
            {' | '}
            {currentPage < totalPages ? (
              <a href="#" onClick={(e) => { e.preventDefault(); setCurrentPage(currentPage + 1) }}>Next →</a>
            ) : (
              <span style={{ color: '#999' }}>Next →</span>
            )}
          </div>

          <div style={{ display: 'flex', justifyContent: 'center' }}>
            <table style={{ borderCollapse: 'collapse', width: '80%' }}>
              <thead>
                <tr>
                  <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Product ID</th>
                  <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Name</th>
                  <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Price</th>
                  <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Status</th>
                  <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {paginatedProducts.map((product) => (
                  <tr key={product._product_id}>
                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>{product._product_id}</td>
                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>{product._product_name}</td>
                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>${product._price}</td>
                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                      {isFeatured(product._product_id.toString()) ? 'Featured' : 'Not Featured'}
                    </td>
                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                      {isFeatured(product._product_id.toString()) ? (
                        <button onClick={() => removeFromFeatured(product._product_id.toString())}>
                          Remove
                        </button>
                      ) : (
                        <button onClick={() => addToFeatured(product._product_id.toString())}>
                          Add to Featured
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {filteredProducts.length === 0 && (
            <p>No products found matching your search.</p>
          )}
          
          <div style={{ marginTop: '10px' }}>
            {currentPage > 1 ? (
              <a href="#" onClick={(e) => { e.preventDefault(); setCurrentPage(currentPage - 1) }}>← Previous</a>
            ) : (
              <span style={{ color: '#999' }}>← Previous</span>
            )}
            {' | '}
            {currentPage < totalPages ? (
              <a href="#" onClick={(e) => { e.preventDefault(); setCurrentPage(currentPage + 1) }}>Next →</a>
            ) : (
              <span style={{ color: '#999' }}>Next →</span>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
