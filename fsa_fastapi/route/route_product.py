from typing import Any, List, Dict

from PIL import Image
from fastapi import APIRouter, Depends, Path, UploadFile, File
from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from random import sample

import prediction
from db.enity.product_entity import ProductEntity
from db.enity.user_entity import UserEntity
from db.repository import product_repo
from db.session import get_db
from model.product_model import ProductDTO, ProductRequest
from route.route_login import get_current_user_from_token

router = APIRouter()


@router.get("/", response_model=List[ProductDTO])
async def get_all_products(db: Session = Depends(get_db),
                           current_user: UserEntity = Depends(get_current_user_from_token)) -> List[ProductDTO]:
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return product_repo.get_products(db=db)


@router.get("/{product_id}", response_model=ProductDTO)
async def get_product_by_id(product_id: int = Path(..., ge=1),
                            db: Session = Depends(get_db),
                            current_user: UserEntity = Depends(get_current_user_from_token)) -> ProductDTO:
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    product = product_repo.get_by_product_id(product_id=product_id, db=db)
    if product is None:
        raise HTTPException(status_code=200, detail="Product not found")
    return product


@router.get("/{brand_name}", response_model=List[ProductDTO])
async def get_products_by_brand(brand_name: str,
                                db: Session = Depends(get_db),
                                current_user: UserEntity = Depends(get_current_user_from_token)) -> ProductDTO:
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    products = product_repo.get_products_by_brand(brand_name=brand_name, db=db)
    if products is None:
        raise HTTPException(status_code=200, detail="Brand no found")
    return products


@router.post("/", response_model=ProductDTO)
async def create_product(new_product: ProductRequest,
                         db: Session = Depends(get_db),
                         current_user: UserEntity = Depends(get_current_user_from_token)) -> ProductDTO:
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
    product = product_repo.create_product(new_product=new_product, db=db)
    if product is None:
        raise HTTPException(status_code=200, detail="Product already exist")
    return product


@router.put("/{product_id}", response_model=ProductDTO)
async def update_product(product_id: int,
                         updated_product: ProductRequest,
                         db: Session = Depends(get_db),
                         current_user: UserEntity = Depends(get_current_user_from_token)) -> ProductDTO:
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
    product = product_repo.update_product(product_id=product_id, updated_product=updated_product, db=db)
    if product is None:
        raise HTTPException(status_code=200, detail="there is no product id with {}".format(product_id))
    return product


@router.delete("/{product_id}")
async def delete_product(product_id: int,
                         db: Session = Depends(get_db),
                         current_user: UserEntity = Depends(get_current_user_from_token)) -> Any:
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
    product = product_repo.delete_product(product_id=product_id, db=db)
    if product is None:
        raise HTTPException(status_code=200, detail="there is no product id with {}".format(product_id))


@router.post("/photo")
async def predict_product_from_photo(file: UploadFile = File(...),
                                     db: Session = Depends(get_db),
                                     current_user: UserEntity = Depends(get_current_user_from_token)
                                     ) -> dict:
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    img = Image.open(file.file)
    res = prediction.prediction_image(img)
    if res is None:
        raise HTTPException(status_code=200, detail="no product found")
    found_product = product_repo.get_by_product_name(product_name=res, db=db)
    if found_product is None:
        raise HTTPException(status_code=200, detail="no product found database")
    return {'product': found_product,
            'can_consume': can_consume_product(found_product=found_product, current_user=current_user)}


def can_consume_product(found_product: ProductEntity, current_user: UserEntity) -> bool:
    ingredients_set = set(found_product.ingredients)
    diets_set = {frozenset(diet.cant_consume) for diet in current_user.diets}
    for cant_consume_set in diets_set:
        if cant_consume_set & ingredients_set:
            return False
    return True


@router.post("/recommended")
async def get_recommended_product(db: Session = Depends(get_db),
                                  current_user: UserEntity = Depends(get_current_user_from_token)) -> dict[
    str, list[Any]]:
    # Query to get user's diets
    user_diets = current_user.diets

    # Query to get all ingredients that user can't consume
    non_consumable_ingredients = set()
    for diet in user_diets:
        non_consumable_ingredients.update(diet.cant_consume)

    # Query to get all products
    all_products = product_repo.get_products(db=db)

    # Filter out products that have ingredients the user can't consume
    consumable_products = [product for product in all_products if
                           not set(product.ingredients).intersection(non_consumable_ingredients)]

    # Choose 5 random products from consumable_products list
    consumable_products_sample = sample(consumable_products, 5) if len(
        consumable_products) > 5 else consumable_products

    return {"products": [product for product in consumable_products_sample]}
