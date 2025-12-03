'use client'

import { useState, useEffect } from 'react'

export default function CartPage() {
    const [cart, setCart] = useState<any>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const userEmail = localStorage.getItem('userEmail')
        if (userEmail) {
            fetchCart(userEmail)
        } else {
            setLoading(false)
        }
    }, [])

    const fetchCart = async (email: string) => {
        try {
            // First get user to find user_id
            const usersResponse = await fetch(`http://localhost:8000/login/users`)
            if (!usersResponse.ok) {
                setLoading(false)
                return
            }
            const users = await usersResponse.json()
            const currentUser = users.find((u: any) => u.email === email)
            
            if (!currentUser) {
                setLoading(false)
                return
            }

            // Check if user is admin
            if (currentUser.is_admin) {
                setLoading(false)
                return
            }

            // Then get cart
            const cartResponse = await fetch(`http://localhost:8000/cart?user_id=${currentUser.user_id}`)
            if (cartResponse.ok) {
                const cartData = await cartResponse.json()
                setCart(cartData)
            }
        } catch (error) {
            console.error("Error fetching cart:", error)
        } finally {
            setLoading(false)
        }
    }

    const removeFromCart = async (productId: string) => {
        if (!confirm('Remove this item from cart?')) return

        const userEmail = localStorage.getItem('userEmail')
        if (!userEmail) return

        try {
            const usersResponse = await fetch(`http://localhost:8000/login/users`)
            const users = await usersResponse.json()
            const currentUser = users.find((u: any) => u.email === userEmail)

            const response = await fetch(`http://localhost:8000/cart/items?user_id=${currentUser.user_id}&product_id=${productId}`, {
                method: 'DELETE'
            })
            
            if (response.ok) {
                const updatedCart = await response.json()
                setCart(updatedCart)
                alert('Item removed from cart')
            }
        } catch (error) {
            console.error("Error removing item:", error)
            alert('Error removing item')
        }
    }

    if (loading) {
        return <div>Loading...</div>
    }

    if (!cart) {
        return (
            <div>
                <h1>Shopping Cart</h1>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px 16px' }}>
                    <a href="/">🏠 Home</a>
                </div>
                <p>Admins do not have shopping carts.</p>
            </div>
        )
    }

    const items = cart.cart_items || []
    const total = cart.cart_value || 0

    return (
        <div style={{ padding: '20px' }}>
            <h1>Shopping Cart</h1>
            
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                <a href="/">🏠 Home</a>
            </div>

            <h2>Cart Items</h2>

            {items.length === 0 ? (
                <p>Your cart is empty</p>
            ) : (
                <>
                    <p>Total Items: {items.length}</p>

                    <div style={{ display: 'flex', justifyContent: 'center' }}>
                        <table style={{ borderCollapse: 'collapse', width: '80%' }}>
                            <thead>
                                <tr>
                                    <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Product ID</th>
                                    <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Name</th>
                                    <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Description</th>
                                    <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Price</th>
                                    <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Quantity</th>
                                    <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Subtotal</th>
                                    <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {items.map((item: any) => (
                                    <tr key={item.product_id}>
                                        <td style={{ border: '1px solid #ddd', padding: '8px' }}>{item.product_id}</td>
                                        <td style={{ border: '1px solid #ddd', padding: '8px' }}>{item.product_name}</td>
                                        <td style={{ border: '1px solid #ddd', padding: '8px' }}>{item.product_desc}</td>
                                        <td style={{ border: '1px solid #ddd', padding: '8px' }}>${parseFloat(item.price).toFixed(2)}</td>
                                        <td style={{ border: '1px solid #ddd', padding: '8px' }}>{item.quantity}</td>
                                        <td style={{ border: '1px solid #ddd', padding: '8px' }}>${(parseFloat(item.price) * item.quantity).toFixed(2)}</td>
                                        <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                                            <button onClick={() => removeFromCart(item.product_id)}>Remove</button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>

                    <br />
                    <h3>Total: ${parseFloat(total).toFixed(2)}</h3>
                </>
            )}
        </div>
    )
}
