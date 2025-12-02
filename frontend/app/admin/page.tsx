'use client'

import { useState, useEffect } from 'react'

export default function AdminPage() {
    const [user, setUser] = useState<any>(null)
    const [loading, setLoading] = useState(true)
    const [imageUrl, setImageUrl] = useState('')

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

    if (loading) {
        return <div>Loading...</div>
    }

    if (!user) {
        return (
            <div>
                <header>
                    <div>
                        <h1>👤 User Profile</h1>
                        <a href="/">🏠 Home</a>
                    </div>
                </header>
                <div>
                <p>Please log in as an admin to view this page</p>
                </div>
            </div>
        )
      }
    return (
      <div>
        <h1>👑 Admin Page</h1>
        <a href="/">🏠 Home</a>
        {/* Admin functionalities go here */}
      </div>
    )          

}
