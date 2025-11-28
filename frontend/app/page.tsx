'use client'
import Form from 'next/form'
import { useSearchParams } from 'next/navigation';

export default async function Home() {
  const searchParams = useSearchParams();
  const search = searchParams.get('search');
  const page = searchParams.get('page');
  const htmlContent = await fetchBrowsingPage(search, page);
  return (
    
      <div dangerouslySetInnerHTML={{ __html: htmlContent }} />
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