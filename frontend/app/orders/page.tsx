'use client'

import { useState, useEffect } from 'react'

export default function OrdersPage() {
    const [orders, setOrders] = useState<any[]>([])
    const [loading, setLoading] = useState(true)
    const [userId, setUserId] = useState<number | null>(null)

    useEffect(() => {
        const userEmail = localStorage.getItem('userEmail')
        if (userEmail) {
            fetchOrders(userEmail)
        } else {
            setLoading(false)
        }
    }, [])

    const fetchOrders = async (email: string) => {
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

            setUserId(currentUser.user_id)

            // Then get orders
            const ordersResponse = await fetch(`http://localhost:8000/orders?user_id=${currentUser.user_id}`)
            if (ordersResponse.ok) {
                const ordersData = await ordersResponse.json()
                setOrders(ordersData.orders || [])
            }
        } catch (error) {
            console.error("Error fetching orders:", error)
        } finally {
            setLoading(false)
        }
    }

    if (loading) {
        return <div style={{ color: '#000' }}>Loading...</div>
    }

    if (userId === null) {
        return (
            <div style={{ padding: '20px', color: '#000' }}>
                <h1 style={{ color: '#fff' }}>My Orders</h1>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px 16px' }}>
                    <a href="/" style={{ color: '#fff' }}>🏠 Home</a>
                </div>
                <p style={{ color: '#000' }}>Please log in to view your orders.</p>
            </div>
        )
    }

    return (
        <div style={{ padding: '20px', color: '#000' }}>
            <h1 style={{ color: '#fff' }}>My Orders</h1>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                <a href="/" style={{ color: '#fff' }}>🏠 Home</a>
            </div>

            <h2 style={{ color: '#fff' }}>Order History</h2>

            {orders.length === 0 ? (
                <p style={{ color: '#000' }}>You have no orders yet</p>
            ) : (
                <>
                    <p style={{ color: '#fff' }}>Total Orders: {orders.length}</p>

                    <div style={{ marginTop: '20px' }}>
                        {orders.map((order: any) => (
                            <div key={order.order_id} style={{ 
                                border: '1px solid #ddd', 
                                padding: '20px', 
                                marginBottom: '20px',
                                borderRadius: '8px',
                                backgroundColor: '#f9f9f9'
                            }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '15px' }}>
                                    <div>
                                        <h3 style={{ margin: '0 0 10px 0', color: '#000' }}>Order #{order.order_id}</h3>
                                        <p style={{ margin: '5px 0', color: '#000' }}>
                                            <strong>Date:</strong> {new Date(order.order_date).toLocaleDateString()}
                                        </p>
                                        {order.is_gift && (
                                            <p style={{ margin: '5px 0', color: '#4CAF50', fontWeight: 'bold' }}>
                                                🎁 Gift Order
                                                {order.gifter_id && order.gifter_id !== userId && (
                                                    <span> from User #{order.gifter_id}</span>
                                                )}
                                            </p>
                                        )}
                                        {order.returned && (
                                            <p style={{ margin: '5px 0', color: '#f44336', fontWeight: 'bold' }}>
                                                ↩️ Returned
                                            </p>
                                        )}
                                    </div>
                                    <div style={{ textAlign: 'right' }}>
                                        <h3 style={{ margin: '0', color: '#4CAF50' }}>
                                            ${parseFloat(order.total_price).toFixed(2)}
                                        </h3>
                                    </div>
                                </div>

                                {order.address && (
                                    <div style={{ marginBottom: '15px', padding: '10px', backgroundColor: '#fff', borderRadius: '4px', color: '#000' }}>
                                        <strong>Shipping Address:</strong>
                                        <p style={{ margin: '5px 0', color: '#000' }}>
                                            {order.address.line1}
                                            {order.address.line2 && <>, {order.address.line2}</>}
                                        </p>
                                        <p style={{ margin: '5px 0', color: '#000' }}>
                                            {order.address.city}, {order.address.province}, {order.address.country}
                                        </p>
                                    </div>
                                )}

                                <div style={{ marginTop: '15px', color: '#000' }}>
                                    <strong>Items:</strong>
                                    <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '10px', backgroundColor: '#fff', color: '#000' }}>
                                        <thead>
                                            <tr style={{ backgroundColor: '#f0f0f0' }}>
                                                <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left', color: '#000' }}>Product</th>
                                                <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left', color: '#000' }}>Description</th>
                                                <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'right', color: '#000' }}>Price</th>
                                                <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'right', color: '#000' }}>Qty</th>
                                                <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'right', color: '#000' }}>Subtotal</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {order.order_items.map((item: any, index: number) => (
                                                <tr key={index}>
                                                    <td style={{ border: '1px solid #ddd', padding: '8px', color: '#000' }}>{item.product_name}</td>
                                                    <td style={{ border: '1px solid #ddd', padding: '8px', color: '#000' }}>{item.product_desc}</td>
                                                    <td style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'right', color: '#000' }}>
                                                        ${parseFloat(item.price).toFixed(2)}
                                                    </td>
                                                    <td style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'right', color: '#000' }}>
                                                        {item.quantity}
                                                    </td>
                                                    <td style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'right', color: '#000' }}>
                                                        ${(parseFloat(item.price) * item.quantity).toFixed(2)}
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        ))}
                    </div>
                </>
            )}
        </div>
    )
}