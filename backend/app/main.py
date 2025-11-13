from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from backend.app.routers.productRouter import router as products_router
from backend.app.routers.cartRouter import router as cart_router
from backend.app.routers.userSignInRouter import router as validation_router
from backend.app.routers.wishListRouter import router as wishList_router
from backend.app.services.productInteractor import get_products_filtered

app = FastAPI()

templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))

@app.get("/", response_class=HTMLResponse)
def root(request: Request, search: str = "", page: int = 1):
    all_matching_products = get_products_filtered(keywords=search, max_price=100000)
    total_matches = len(all_matching_products)
    
    items_per_page = 50
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    products = all_matching_products[start_index:end_index]
    displayed_count = len(products)
    

    total_pages = (total_matches + items_per_page - 1) // items_per_page  
    has_previous = page > 1
    has_next = page < total_pages
    
    return templates.TemplateResponse(
        "products.html", 
        {
            "request": request, 
            "products": products, 
            "displayed_count": displayed_count, 
            "total_matches": total_matches, 
            "search_query": search,
            "current_page": page,
            "total_pages": total_pages,
            "has_previous": has_previous,
            "has_next": has_next
        }
    )

@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(products_router)
app.include_router(cart_router)
app.include_router(validation_router)
app.include_router(wishList_router)
