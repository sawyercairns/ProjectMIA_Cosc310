import Form from 'next/form'
import LoginButton from './components/LoginButton'

// Use internal Docker network URL for server-side, or localhost for client
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
const INTERNAL_API_URL = process.env.INTERNAL_API_URL || API_URL

export default async function Home({
  searchParams,
}: {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}) {
  const params = await searchParams
  const search = (params.query as string) || ''
  const page = parseInt((params.page as string) || '1')
  
  const result = await fetchProductsWithPagination(search, page)
  const { products, displayedCount, totalMatches, currentPage, totalPages, hasPrevious, hasNext } = result
  const popular_items = await fetchPopular()

  return (
    <div>
      <h1>ProjectMIA Online Shop</h1>
    
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px 16px' }}>
        <a href="/">🏠 Home</a>
        <LoginButton />
      </div>

      <Form action="/">
        <label htmlFor="search">Search products:</label>
        <input 
          id="search" 
          name="query" 
          defaultValue={search}
          placeholder="Enter product name..."
        />
        <button type="submit">Search</button>
      </Form>

      <br></br><br></br>

      <h1>Popular Items: </h1>
      {popular_items.map((pop_item: any) => (
          <li key={pop_item._product_name}>
          <strong>{ pop_item._product_name }</strong><br></br>
            <hr></hr>
          </li>
        ))}

      <br></br><br></br>

      <p>Showing {displayedCount} out of {totalMatches} products (Page {currentPage} of {totalPages})</p>

      <div style={{ marginBottom: '10px' }}>
        {hasPrevious ? (
          <a href={`/?query=${search}&page=${currentPage - 1}`}>← Previous</a>
        ) : (
          <span style={{ color: '#999' }}>← Previous</span>
        )}
        {' | '}
        {hasNext ? (
          <a href={`/?query=${search}&page=${currentPage + 1}`}>Next →</a>
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
            Units sold: {item._units_sold}
            <hr />
          </li>
        ))}
      </ul>

      <div style={{ marginTop: '10px' }}>
        {hasPrevious ? (
          <a href={`/?query=${search}&page=${currentPage - 1}`}>← Previous</a>
        ) : (
          <span style={{ color: '#999' }}>← Previous</span>
        )}
        {' | '}
        {hasNext ? (
          <a href={`/?query=${search}&page=${currentPage + 1}`}>Next →</a>
        ) : (
          <span style={{ color: '#999' }}>Next →</span>
        )}
      </div>
    </div> 
  );
}

async function fetchProductsWithPagination(search: string, page: number) {
  try {
    const keyword = search || ''
    const response = await fetch(`${INTERNAL_API_URL}/products?keyword=${keyword}`)
    const allProducts = await response.json()
    
    const itemsPerPage = 50
    const startIndex = (page - 1) * itemsPerPage
    const endIndex = startIndex + itemsPerPage
    
    const products = allProducts.slice(startIndex, endIndex)
    const totalMatches = allProducts.length
    const totalPages = Math.ceil(totalMatches / itemsPerPage)
    
    return {
      products,
      displayedCount: products.length,
      totalMatches,
      currentPage: page,
      totalPages: totalPages || 1,
      hasPrevious: page > 1,
      hasNext: page < totalPages
    }
  } catch (error) {
    console.error("Error fetching products:", error)
    return {
      products: [],
      displayedCount: 0,
      totalMatches: 0,
      currentPage: 1,
      totalPages: 1,
      hasPrevious: false,
      hasNext: false
    }
  }
}

async function fetchPopular(){
  try {
    const response = await fetch(`${INTERNAL_API_URL}/products/popularProducts`);
    const data = await response.json();
    return data
  } catch (error) {
    console.error("Error fetching item:", error);
    return []
  }
}