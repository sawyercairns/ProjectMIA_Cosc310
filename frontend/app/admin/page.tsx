'use client'

import { useState, useEffect } from 'react'

export default function AdminPage() {
    const [user, setUser] = useState<any>(null)
    const [loading, setLoading] = useState(true)
    const [activeTab, setActiveTab] = useState('users')
    const [users, setUsers] = useState<any[]>([])
    const [reviews, setReviews] = useState<any[]>([])
    const [searchName, setSearchName] = useState('')
    const [currentPage, setCurrentPage] = useState(1)
    const usersPerPage = 20

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
            const response = await fetch(`http://localhost:8000/review`)
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

        try {
            const response = await fetch(`http://localhost:8000/review/${reviewId}`, {
                method: 'DELETE'
            })
            if (response.ok) {
                setReviews(reviews.filter(r => r.review_id !== reviewId))
                alert('Review deleted successfully')
            }
        } catch (error) {
            console.error("Error deleting review:", error)
            alert('Error deleting review')
        }
    }

    const deleteUser = async (userId: string) => {
        if (!confirm('Are you sure you want to delete this user?')) return

        try {
            const response = await fetch(`http://localhost:8000/login/user/${userId}`, {
                method: 'DELETE'
            })
            if (response.ok) {
                setUsers(users.filter(u => u.user_id !== userId))
                alert('User deleted successfully')
            } else {
                alert('Failed to delete user')
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
            return fullName.includes(searchName.toLowerCase())
        })

    const totalPages = Math.ceil(filteredUsers.length / usersPerPage)
    const paginatedUsers = filteredUsers.slice((currentPage - 1) * usersPerPage, currentPage * usersPerPage)

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
                    
                    <label htmlFor="search">Search by name:</label>
                    <input
                        id="search"
                        type="text"
                        value={searchName}
                        onChange={(e) => {
                            setSearchName(e.target.value)
                            setCurrentPage(1)
                        }}
                        placeholder="Enter name..."
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
                    
                    {reviews.length === 0 ? (
                        <p>No reviews found.</p>
                    ) : (
                        <ul>
                            {reviews.map((review: any) => (
                                <li key={review.review_id}>
                                    <strong>Review ID: {review.review_id}</strong><br />
                                    User ID: {review.user_id}<br />
                                    Product ID: {review.product_id}<br />
                                    Rating: {'⭐'.repeat(review.rating)} ({review.rating}/5)<br />
                                    Review: {review.review_text}<br />
                                    Date: {new Date(review.review_date).toLocaleDateString()}<br />
                                    <button onClick={() => deleteReview(review.review_id)}>Delete Review</button>
                                    <hr />
                                </li>
                            ))}
                        </ul>
                    )}
                </div>
            )}
        </div>
    )
}
