'use client'

import { useState, useEffect } from 'react'

export default function AdminPage() {
    const [user, setUser] = useState<any>(null)
    const [loading, setLoading] = useState(true)
    const [activeTab, setActiveTab] = useState('users')
    const [users, setUsers] = useState<any[]>([])
    const [reviews, setReviews] = useState<any[]>([])
    const [searchName, setSearchName] = useState('')
    const [searchReview, setSearchReview] = useState('')
    const [currentPage, setCurrentPage] = useState(1)
    const [reviewPage, setReviewPage] = useState(1)
    const usersPerPage = 20
    const reviewsPerPage = 20

    useEffect(() => {
        const userEmail = localStorage.getItem('userEmail')
        if (userEmail) {
            fetchUserByEmail(userEmail)
        } else {
            setLoading(false)
        }
    }, [])

    useEffect(() => {
        if (user && user.is_admin) {
            fetchAllUsers()
            fetchAllReviews()
        }
    }, [user])

    const fetchUserByEmail = async (email: string) => {
        try {
            const response = await fetch(`http://localhost:8000/login/users`)
            if (!response.ok) {
                setLoading(false)
                return
            }
            const users = await response.json()
            const currentUser = users.find((u: any) => u.email === email)
            
            if (currentUser && currentUser.is_admin) {
                setUser(currentUser)
            } else {
                setUser(null)
            }
        } catch (error) {
            console.error("Error fetching user:", error)
        } finally {
            setLoading(false)
        }
    }

    const fetchAllUsers = async () => {
        try {
            const response = await fetch(`http://localhost:8000/login/users`)
            if (response.ok) {
                const data = await response.json()
                setUsers(data)
            }
        } catch (error) {
            console.error("Error fetching users:", error)
        }
    }

    const fetchAllReviews = async () => {
        try {
            const response = await fetch(`http://localhost:8000/reviews/all`)
            if (response.ok) {
                const data = await response.json()
                setReviews(data)
            }
        } catch (error) {
            console.error("Error fetching reviews:", error)
        }
    }

    const deleteReview = async (reviewId: string) => {
        if (!confirm('Are you sure you want to delete this review?')) return

        const userEmail = localStorage.getItem('userEmail')
        const userPassword = prompt('Please enter your password to confirm:')
        
        if (!userPassword) return

        try {
            const response = await fetch(`http://localhost:8000/reviews/${reviewId}?email=${encodeURIComponent(userEmail || '')}&password=${encodeURIComponent(userPassword)}`, {
                method: 'DELETE'
            })
            if (response.ok) {
                setReviews(reviews.filter(r => r.review_id !== reviewId))
                alert('Review deleted successfully')
            } else {
                alert('Failed to delete review - unauthorized')
            }
        } catch (error) {
            console.error("Error deleting review:", error)
            alert('Error deleting review')
        }
    }

    const deleteUser = async (userId: string) => {
        if (!confirm('Are you sure you want to delete this user?')) return

        const userEmail = localStorage.getItem('userEmail')
        const userPassword = prompt('Please enter your password to confirm:')
        
        if (!userPassword) return

        try {
            const response = await fetch(`http://localhost:8000/login/${userId}?email=${encodeURIComponent(userEmail || '')}&password=${encodeURIComponent(userPassword)}`, {
                method: 'DELETE'
            })
            if (response.ok) {
                setUsers(users.filter(u => u.user_id !== userId))
                alert('User deleted successfully')
            } else {
                alert('Failed to delete user - unauthorized')
            }
        } catch (error) {
            console.error("Error deleting user:", error)
            alert('Error deleting user')
        }
    }

    if (loading) {
        return <div>Loading...</div>
    }

    if (!user) {
        return (
            <div>
                <h1>Admin Access Required</h1>
                <a href="/">🏠 Home</a>
                <p>Please log in as an admin to view this page</p>
            </div>
        )
    }

    const filteredUsers = users
        .filter((u: any) => !u.is_admin)
        .filter((u: any) => {
            const fullName = `${u.first_name} ${u.last_name}`.toLowerCase()
            const userId = u.user_id.toString().toLowerCase()
            const searchTerm = searchName.toLowerCase()
            return fullName.includes(searchTerm) || userId.includes(searchTerm)
        })

    const totalPages = Math.ceil(filteredUsers.length / usersPerPage)
    const paginatedUsers = filteredUsers.slice((currentPage - 1) * usersPerPage, currentPage * usersPerPage)

    const filteredReviews = reviews.filter((r: any) => {
        const userId = r.user_id.toString().toLowerCase()
        const productId = r.product_id.toString().toLowerCase()
        const searchTerm = searchReview.toLowerCase()
        return userId.includes(searchTerm) || productId.includes(searchTerm)
    })

    const totalReviewPages = Math.ceil(filteredReviews.length / reviewsPerPage)
    const paginatedReviews = filteredReviews.slice((reviewPage - 1) * reviewsPerPage, reviewPage * reviewsPerPage)

    return (
        <div>
            <h1>👑 Admin Dashboard</h1>
            
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px 16px' }}>
                <a href="/">🏠 Home</a>
                <span>Welcome, {user.first_name}!</span>
            </div>

            <div style={{ marginBottom: '20px' }}>
                <button onClick={() => setActiveTab('users')} style={{ marginRight: '10px' }}>
                    👥 Users ({users.filter((u: any) => !u.is_admin).length})
                </button>
                <button onClick={() => setActiveTab('reviews')}>
                    📝 Reviews ({reviews.length})
                </button>
            </div>

            {activeTab === 'users' && (
                <div>
                    <h2>All Users</h2>
                    
                    <label htmlFor="search">Search by name or ID:</label>
                    <input
                        id="search"
                        type="text"
                        value={searchName}
                        onChange={(e) => {
                            setSearchName(e.target.value)
                            setCurrentPage(1)
                        }}
                        placeholder="Enter name or ID..."
                    />
                    
                    <br /><br />
                    
                    <p>Showing {paginatedUsers.length} out of {filteredUsers.length} users (Page {currentPage} of {totalPages || 1})</p>

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
                                    <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>User ID</th>
                                    <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Name</th>
                                    <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Email</th>
                                    <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Age</th>
                                    <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {paginatedUsers.map((u: any) => (
                                    <tr key={u.user_id}>
                                        <td style={{ border: '1px solid #ddd', padding: '8px' }}>{u.user_id}</td>
                                        <td style={{ border: '1px solid #ddd', padding: '8px' }}>{u.first_name} {u.last_name}</td>
                                        <td style={{ border: '1px solid #ddd', padding: '8px' }}>{u.email}</td>
                                        <td style={{ border: '1px solid #ddd', padding: '8px' }}>{u.age}</td>
                                        <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                                            <button onClick={() => deleteUser(u.user_id)}>Delete</button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>

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

            {activeTab === 'reviews' && (
                <div>
                    <h2>All Reviews</h2>
                    
                    <label htmlFor="searchReview">Search by user ID or product ID:</label>
                    <input
                        id="searchReview"
                        type="text"
                        value={searchReview}
                        onChange={(e) => {
                            setSearchReview(e.target.value)
                            setReviewPage(1)
                        }}
                        placeholder="Enter user ID or product ID..."
                    />
                    
                    <br /><br />
                    
                    <p>Showing {paginatedReviews.length} out of {filteredReviews.length} reviews (Page {reviewPage} of {totalReviewPages || 1})</p>

                    <div style={{ marginBottom: '10px' }}>
                        {reviewPage > 1 ? (
                            <a href="#" onClick={(e) => { e.preventDefault(); setReviewPage(reviewPage - 1) }}>← Previous</a>
                        ) : (
                            <span style={{ color: '#999' }}>← Previous</span>
                        )}
                        {' | '}
                        {reviewPage < totalReviewPages ? (
                            <a href="#" onClick={(e) => { e.preventDefault(); setReviewPage(reviewPage + 1) }}>Next →</a>
                        ) : (
                            <span style={{ color: '#999' }}>Next →</span>
                        )}
                    </div>
                    
                    {reviews.length === 0 ? (
                        <p>No reviews found.</p>
                    ) : (
                        <div style={{ display: 'flex', justifyContent: 'center' }}>
                            <table style={{ borderCollapse: 'collapse', width: '80%' }}>
                                <thead>
                                    <tr>
                                        <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>User ID</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Product ID</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Rating</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Review</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Date</th>
                                        <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {paginatedReviews.map((review: any) => (
                                        <tr key={review.review_id}>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{review.user_id}</td>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{review.product_id}</td>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{'⭐'.repeat(Math.floor(review.rating))} ({review.rating}/5)</td>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{review.body || review.review_text}</td>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{review.created_at || new Date(review.review_date).toLocaleDateString()}</td>
                                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                                                <button onClick={() => deleteReview(review.review_id)}>Delete</button>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}

                    <div style={{ marginTop: '10px' }}>
                        {reviewPage > 1 ? (
                            <a href="#" onClick={(e) => { e.preventDefault(); setReviewPage(reviewPage - 1) }}>← Previous</a>
                        ) : (
                            <span style={{ color: '#999' }}>← Previous</span>
                        )}
                        {' | '}
                        {reviewPage < totalReviewPages ? (
                            <a href="#" onClick={(e) => { e.preventDefault(); setReviewPage(reviewPage + 1) }}>Next →</a>
                        ) : (
                            <span style={{ color: '#999' }}>Next →</span>
                        )}
                    </div>
                </div>
            )}
        </div>
    )
}
