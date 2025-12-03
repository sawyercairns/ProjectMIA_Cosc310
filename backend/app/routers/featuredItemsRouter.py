from fastapi import APIRouter, HTTPException
from app.schemas.featuredItemsClass import AddFeaturedItemRequest
from app.services.featuredItemsInteractor import get_featured_items, add_featured_item, remove_featured_item
from app.services.Interactor import load_json

router = APIRouter(prefix="/featured", tags=["featured"])


@router.get("")
def get_featured_product_ids():
    """Getting all the featured items ids"""
    try:
        featured = get_featured_items()
        return featured.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("")
def add_product_to_featured(request: AddFeaturedItemRequest):
    """Add a product to featured items - admin only"""
    users = load_json("users.json")
    user = next((u for u in users if u.get("email") == request.admin_email), None)
    
    if not user or not user.get("is_admin", False):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        featured = add_featured_item(request.product_id)
        return {"message": "Product added to featured items", "featured_items": featured.to_dict()}
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{product_id}")
def remove_product_from_featured(product_id: str, admin_email: str):
    """Remove a product from featured items - admin only"""
    users = load_json("users.json")
    user = next((u for u in users if u.get("email") == admin_email), None)
    
    if not user or not user.get("is_admin", False):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        featured = remove_featured_item(product_id)
        return {"message": "Product removed from featured items", "featured_items": featured.to_dict()}
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
