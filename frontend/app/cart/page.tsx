'use client'

import { useState, useEffect } from 'react'

export default function CartPage() {
    const [cart, setCart] = useState<any>(null)
    const [loading, setLoading] = useState(true)
    const [placingOrder, setPlacingOrder] = useState(false)
    const [userId, setUserId] = useState<number | null>(null)
    const [address, setAddress] = useState({
        line1: "",
        line2: "",
        city: "",
        province: "",
        country: ""
    })

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
            const usersResponse = await fetch(`http://localhost:8000/login/users`)
            if (!usersResponse.ok) {
                setLoading(false)
                return
            }
            
            const users = await usersResponse.json()
            const currentUser = users.find((u: any) => u.email == email)
            
            if (!currentUser) {
                setLoading(false)
                return
            }

            setUserId(currentUser.user_id)

            // Check if user is admin
            if (currentUser.is_admin) {
                setLoading(false)
                return
            }

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
            const currentUser = users.find((u: any) => u.email == userEmail)

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

    const handlePlaceOrder = async (isGift: boolean = false) => {
        if (!userId || !cart || cart.cart_items.length == 0) return

        // validate address (only for regular orders)
        if (!isGift && (!address.line1 || !address.city || !address.province || !address.country)) {
            alert('Please fill in all required address fields (Address Line 1, City, Province, Country)')
            return
        }

        setPlacingOrder(true)
        try {
            const paymentResponse = await fetch(`http://localhost:8000/payment?user_id=${userId}`)
            
            if (!paymentResponse.ok) {
                alert('Please update your payment method.')
                setPlacingOrder(false)
                return
            }

            const paymentData = await paymentResponse.json()
            
            if (!paymentData.card_number || paymentData.card_number == '') {
                alert('Please update your payment method.')
                setPlacingOrder(false)
                return
            }

            const orderItems = cart.cart_items.map((item: any) => ({
                product_id: item.product_id,
                product_name: item.product_name,
                product_desc: item.product_desc,
                quantity: item.quantity,
                price: parseFloat(item.price)
            }))

            const orderRequest = {
                user_id: userId,
                order_items: orderItems,
                address: isGift ? null : address
            }

            const endpoint = isGift ? 'http://localhost:8000/orders/gift' : 'http://localhost:8000/orders'
            const orderResponse = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(orderRequest)
            })

            if (orderResponse.ok) {
                // clear cart
                for (const item of cart.cart_items) {
                    await fetch(`http://localhost:8000/cart/items?user_id=${userId}&product_id=${item.product_id}`, {
                        method: 'DELETE'
                    })
                }
                
                alert(isGift ? 'Gift sent to a random user!' : 'Order Placed')
                const userEmail = localStorage.getItem('userEmail')
                if (userEmail) {
                    fetchCart(userEmail)
                }
            } else {
                const errorData = await orderResponse.text()
                alert(`Failed to place ${isGift ? 'gift' : 'order'}: ${errorData}`)
            }
        } catch (error) {
            console.error(`Error placing ${isGift ? 'gift' : 'order'}:`, error)
            alert(`Error placing ${isGift ? 'gift' : 'order'}. Please try again.`)
        } finally {
            setPlacingOrder(false)
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
                {items.length > 0 && (
                    <div style={{ display: 'flex', gap: '10px' }}>
                        <button
                            onClick={() => handlePlaceOrder(false)}
                            disabled={placingOrder}
                            className="place-order-btn"
                        >
                            {placingOrder ? 'Processing...' : 'Place Order'}
                        </button>
                        <button
                            onClick={() => handlePlaceOrder(true)}
                            disabled={placingOrder}
                            className="gift-order-btn"
                        >
                            Gift to Random User
                        </button>
                    </div>
                )}
            </div>

            {items.length > 0 && (
                <div className="address-section">
                    <h3>Shipping Address</h3>
                    <div className="address-form">
                        <div className="form-field">
                            <label>Address Line 1 *</label>
                            <input
                                type="text"
                                value={address.line1}
                                onChange={(e) => setAddress({...address, line1: e.target.value})}
                                placeholder="Street address"
                            />
                        </div>
                        <div className="form-field">
                            <label>Address Line 2</label>
                            <input
                                type="text"
                                value={address.line2}
                                onChange={(e) => setAddress({...address, line2: e.target.value})}
                                placeholder="Apartment, suite, etc. (optional)"
                            />
                        </div>
                        <div className="form-field">
                            <label>City *</label>
                            <input
                                type="text"
                                value={address.city}
                                onChange={(e) => setAddress({...address, city: e.target.value})}
                                placeholder="City"
                            />
                        </div>
                        <div className="form-field">
                            <label>Province *</label>
                            <input
                                type="text"
                                value={address.province}
                                onChange={(e) => setAddress({...address, province: e.target.value})}
                                placeholder="Province"
                            />
                        </div>
                        <div className="form-field">
                            <label>Country *</label>
                            <input
                                type="text"
                                value={address.country}
                                onChange={(e) => setAddress({...address, country: e.target.value})}
                                placeholder="Country"
                            />
                        </div>
                    </div>
                </div>
            )}

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
