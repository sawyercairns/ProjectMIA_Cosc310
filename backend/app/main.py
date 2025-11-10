from fastapi import FastAPI
from backend.app.routers.productRouter import router as products_router
from backend.app.routers.userSignInRouter import router as validation_router

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(products_router)
app.include_router(validation_router)
