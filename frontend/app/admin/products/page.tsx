"use client"

import { useEffect, useState } from "react"

type Product = {
	_product_id: number
	_product_name: string
	_product_desc: string
	_price: number
	_discount_price?: number | null
}

export default function AdminProductsPage() {
	const [products, setProducts] = useState<Product[]>([])
	const [loading, setLoading] = useState(true)
	const [userEmail, setUserEmail] = useState("")
	const [accessDenied, setAccessDenied] = useState(false)
	const [searchTerm, setSearchTerm] = useState("")
	const [currentPage, setCurrentPage] = useState(1)
	const [formData, setFormData] = useState({ name: "", description: "", price: "", discountPrice: "" })
	const [submitting, setSubmitting] = useState(false)
	const [removingId, setRemovingId] = useState<number | null>(null)
	const productsPerPage = 20

	useEffect(() => {
		const email = localStorage.getItem("userEmail")
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
			const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
			const usersResponse = await fetch(`${apiUrl}/login/users`)
			const users = await usersResponse.json()
			const currentUser = users.find((u: any) => u.email === email)

			if (!currentUser || !currentUser.is_admin) {
				setAccessDenied(true)
				setLoading(false)
				return
			}

			fetchProducts()
		} catch (error) {
			console.error("Error verifying admin status:", error)
			setAccessDenied(true)
			setLoading(false)
		}
	}

	const fetchProducts = async () => {
		try {
			setLoading(true)
			const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
			const response = await fetch(`${apiUrl}/products`)
			const data = await response.json()
			setProducts(data)
		} catch (error) {
			console.error("Error fetching products:", error)
			alert("Failed to load products")
		} finally {
			setLoading(false)
		}
	}

	const handleFormChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
		const { name, value } = e.target
		setFormData((prev) => ({ ...prev, [name]: value }))
	}

	const handleAddProduct = async (e: React.FormEvent<HTMLFormElement>) => {
		e.preventDefault()
		if (!formData.name.trim() || !formData.description.trim() || !formData.price.trim()) {
			alert("Please complete all fields")
			return
		}

		const priceValue = parseFloat(formData.price)
		if (Number.isNaN(priceValue) || priceValue <= 0) {
			alert("Price must be a positive number")
			return
		}

		const discountValue = formData.discountPrice.trim() ? parseFloat(formData.discountPrice) : 0
		if (Number.isNaN(discountValue) || discountValue < 0) {
			alert("Discount price must be zero or a positive number")
			return
		}
		if (discountValue > priceValue) {
			alert("Discount price cannot exceed the regular price")
			return
		}

		const password = prompt("Enter your admin password to create this product")
		if (!password) return

		setSubmitting(true)
		try {
			const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
			const params = new URLSearchParams({
				email: userEmail,
				password,
				product_name: formData.name.trim(),
				description: formData.description.trim(),
				price: priceValue.toString(),
				discount_price: discountValue.toString()
			})

			const response = await fetch(`${apiUrl}/products?${params.toString()}`, {
				method: "POST"
			})

			if (response.ok) {
				alert("Product created successfully!")
				setFormData({ name: "", description: "", price: "", discountPrice: "" })
				fetchProducts()
			} else {
				const errorText = await response.text()
				alert(errorText || "Failed to create product")
			}
		} catch (error) {
			console.error("Error creating product:", error)
			alert("Error creating product")
		} finally {
			setSubmitting(false)
		}
	}

	const handleRemoveProduct = async (productId: number) => {
		if (!confirm(`Remove product #${productId}?`)) return
		const password = prompt("Enter your admin password to remove this product")
		if (!password) return

		setRemovingId(productId)
		try {
			const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
			const params = new URLSearchParams({
				email: userEmail,
				password,
				id: productId.toString()
			})

			const response = await fetch(`${apiUrl}/products?${params.toString()}`, {
				method: "DELETE"
			})

			if (response.ok) {
				alert("Product removed successfully")
				fetchProducts()
			} else {
				const errorText = await response.text()
				alert(errorText || "Failed to remove product")
			}
		} catch (error) {
			console.error("Error removing product:", error)
			alert("Error removing product")
		} finally {
			setRemovingId(null)
		}
	}

	const filteredProducts = products.filter((product) => {
		const term = searchTerm.toLowerCase()
		return (
			product._product_name.toLowerCase().includes(term) ||
			product._product_id.toString().includes(term)
		)
	})

	const totalPages = Math.ceil(filteredProducts.length / productsPerPage) || 1
	const paginatedProducts = filteredProducts.slice(
		(currentPage - 1) * productsPerPage,
		currentPage * productsPerPage
	)

	if (accessDenied) {
		return (
			<div style={{ padding: "20px" }}>
				<h1>Products Management</h1>
				<a href="/">🏠 Home</a>
				<p style={{ marginTop: "20px" }}>Please log in as an admin to manage products.</p>
			</div>
		)
	}

	return (
		<div style={{ padding: "20px" }}>
			<h1>🛒 Products Management</h1>

			<div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
				<a href="/">🏠 Home</a>
				<a href="/admin">👑 Admin Dashboard</a>
			</div>

			<section style={{ marginTop: "20px", backgroundColor: "#fff", padding: "20px", borderRadius: "8px", border: "1px solid #000000", color: 'black' }}>
				<h2>Add New Product</h2>
				<form onSubmit={handleAddProduct} style={{ display: "flex", flexDirection: "column", gap: "10px", maxWidth: "500px" }}>
					<label>
						Product Name:
						<input
							type="text"
							name="name"
							value={formData.name}
							onChange={handleFormChange}
							required
							style={{ border: "1px solid #000", borderRadius: "4px", padding: "6px" }}
						/>
					</label>
					<label>
						Description:
						<textarea
							name="description"
							rows={3}
							value={formData.description}
							onChange={handleFormChange}
							required
							style={{ border: "1px solid #000", borderRadius: "4px", padding: "6px" }}
						/>
					</label>
					<label>
						Price:
						<input
							type="number"
							name="price"
							min="0"
							step="0.01"
							value={formData.price}
							onChange={handleFormChange}
							required
							style={{ border: "1px solid #000", borderRadius: "4px", padding: "6px" }}
						/>
					</label>
					<label>
						Discount Price (optional):
						<input
							type="number"
							name="discountPrice"
							min="0"
							step="0.01"
							value={formData.discountPrice}
							onChange={handleFormChange}
							style={{ border: "1px solid #000", borderRadius: "4px", padding: "6px" }}
						/>
					</label>
					<button type="submit" disabled={submitting} style={{ alignSelf: "flex-start" }}>
						{submitting ? "Adding..." : "Add Product"}
					</button>
				</form>
			</section>

			<section style={{ marginTop: "30px" }}>
				<h2>Existing Products</h2>

				<label htmlFor="product-search">Search by name or ID:</label>
				<input
					id="product-search"
					type="text"
					value={searchTerm}
					onChange={(e) => {
						setSearchTerm(e.target.value)
						setCurrentPage(1)
					}}
					placeholder="Enter name or ID..."
				/>

				{loading ? (
					<p style={{ marginTop: "20px" }}>Loading products...</p>
				) : (
					<div style={{ marginTop: "20px" }}>
						<p>
							Showing {paginatedProducts.length} of {filteredProducts.length} products (Page {currentPage} of {totalPages})
						</p>

						<div style={{ margin: "10px 0" }}>
							{currentPage > 1 ? (
								<a href="#" onClick={(e) => { e.preventDefault(); setCurrentPage(currentPage - 1) }}>← Previous</a>
							) : (
								<span style={{ color: "#999" }}>← Previous</span>
							)}
							{" | "}
							{currentPage < totalPages ? (
								<a href="#" onClick={(e) => { e.preventDefault(); setCurrentPage(currentPage + 1) }}>Next →</a>
							) : (
								<span style={{ color: "#999" }}>Next →</span>
							)}
						</div>

						<div style={{ display: "flex", justifyContent: "center" }}>
							<table style={{ borderCollapse: "collapse", width: "90%" }}>
								<thead>
									<tr>
										<th style={{ border: "1px solid #ddd", padding: "8px", textAlign: "left" }}>ID</th>
										<th style={{ border: "1px solid #ddd", padding: "8px", textAlign: "left" }}>Name</th>
										<th style={{ border: "1px solid #ddd", padding: "8px", textAlign: "left" }}>Description</th>
										<th style={{ border: "1px solid #ddd", padding: "8px", textAlign: "left" }}>Price</th>
										<th style={{ border: "1px solid #ddd", padding: "8px", textAlign: "left" }}>Discount Price</th>
										<th style={{ border: "1px solid #ddd", padding: "8px", textAlign: "left" }}>Actions</th>
									</tr>
								</thead>
								<tbody>
									{paginatedProducts.map((product) => (
										<tr key={product._product_id}>
											<td style={{ border: "1px solid #ddd", padding: "8px" }}>{product._product_id}</td>
											<td style={{ border: "1px solid #ddd", padding: "8px" }}>{product._product_name}</td>
											<td style={{ border: "1px solid #ddd", padding: "8px" }}>{product._product_desc}</td>
											<td style={{ border: "1px solid #ddd", padding: "8px" }}>${product._price.toFixed(2)}</td>
											<td style={{ border: "1px solid #ddd", padding: "8px" }}>
												{product._discount_price ? `$${product._discount_price.toFixed(2)}` : "—"}
											</td>
											<td style={{ border: "1px solid #ddd", padding: "8px" }}>
												<button
													onClick={() => handleRemoveProduct(product._product_id)}
													disabled={removingId === product._product_id}
													style={{ backgroundColor: "#f44336", color: "#fff", border: "none", padding: "6px 12px" }}
												>
													{removingId === product._product_id ? "Removing..." : "Remove"}
												</button>
											</td>
										</tr>
									))}
								</tbody>
							</table>
						</div>

						{filteredProducts.length === 0 && <p>No products found.</p>}

						<div style={{ marginTop: "10px" }}>
							{currentPage > 1 ? (
								<a href="#" onClick={(e) => { e.preventDefault(); setCurrentPage(currentPage - 1) }}>← Previous</a>
							) : (
								<span style={{ color: "#999" }}>← Previous</span>
							)}
							{" | "}
							{currentPage < totalPages ? (
								<a href="#" onClick={(e) => { e.preventDefault(); setCurrentPage(currentPage + 1) }}>Next →</a>
							) : (
								<span style={{ color: "#999" }}>Next →</span>
							)}
						</div>
					</div>
				)}
			</section>
		</div>
	)
}
