import Form from 'next/form'


export default async function Home({
  searchParams,
}: {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}) {
   const items = await fetchProducts((await searchParams).query);
  return (
    <div>
      <h1>ProjectMIA Online Shop</h1>
    
      <a href="/">🏠 Home</a>
      <Form action="/">
        <input name="query"  placeholder="Enter product name..."/>
        <button type="submit">Submit</button>
      </Form>
      <ul>
        {items.map(item => (
          <li key={item._product_id}>
          <strong>{ item._product_name }</strong><br></br>
          {item._product_desc}<br></br>
          Price: ${ item._price }<br></br>
          Rating: { item._rating } ({ item._rating_count } reviews)<br></br>
          Units sold: { item._units_sold }
            <hr></hr>
          </li>
        ))}
      </ul>
        
    </div> 
  );
}


async function fetchBrowsingPage(search:any, page:any) {
  try {
    if (search == null) search = ''
    if (page == null) page = '1'
    const response = await fetch('http://localhost:8000/?search=' + search +'&page=' + page);
    const data = await response.text();
    return data
  } catch (error) {
    console.error("Error fetching item:", error);
  }
}

async function fetchProducts(keyword:any){
  try {
    if(keyword == null) keyword = ""
    const response = await fetch('http://localhost:8000/products?keyword=' + keyword);
    const data = await response.json();
    return data
  } catch (error) {
    console.error("Error fetching item:", error);
  }
}