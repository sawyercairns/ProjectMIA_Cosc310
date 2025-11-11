from fastapi import FastAPI
from backend.app.routers.productRouter import router as products_router
from backend.app.routers.cartRouter import router as cart_router

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(products_router)
app.include_router(cart_router)
