from app.services.Interactor import load_json, write_to_json
from app.schemas.featuredItemsClass import FeaturedItems


def get_featured_items():
    data = load_json("featuredItems.json")
    return FeaturedItems(**data)


def add_featured_item(product_id: str):
    data = load_json("featuredItems.json")
    featured = FeaturedItems(**data)
    
    if product_id in featured.featured_product_ids:
        raise ValueError(f"Product {product_id} is already in featured items")
    
    featured.featured_product_ids.append(product_id)
    write_to_json("featuredItems.json", featured.to_dict())
    return featured


def remove_featured_item(product_id: str):
    data = load_json("featuredItems.json")
    featured = FeaturedItems(**data)
    
    if product_id not in featured.featured_product_ids:
        raise ValueError(f"Product {product_id} is not in featured items")
    
    featured.featured_product_ids.remove(product_id)
    write_to_json("featuredItems.json", featured.to_dict())
    return featured
