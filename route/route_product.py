from random import sample
from typing import Any, List

import prediction
from PIL import Image
from db.enity.product_entity import ProductEntity
from db.enity.user_entity import UserEntity
from db.repository import product_repo, user_repo
from db.session import get_db
from fastapi import APIRouter, Depends, Path, UploadFile, File, Query
from fastapi import HTTPException
from model.product_model import ProductDTO, ProductRequest
from route.route_login import get_current_user_from_token
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/recommended")
async def get_recommended_product(db: Session = Depends(get_db),
                                  current_user: UserEntity = Depends(get_current_user_from_token)) -> dict[
    str, list[Any]]:
    user_diets = current_user.diets

    non_consumable_ingredients = set()
    for diet in user_diets:
        non_consumable_ingredients.update(diet.cant_consume)

    all_products = product_repo.get_products(db=db, page=1, items_per_page=200, search=None)

    consumable_products = [product for product in all_products if
                           not set(product.ingredients).intersection(non_consumable_ingredients)]

    consumable_products_sample = sample(consumable_products, 5) if len(
        consumable_products) > 5 else consumable_products

    return {"products": [product for product in consumable_products_sample]}


@router.get("/like", response_model=List[ProductDTO])
async def get_likes(db: Session = Depends(get_db),
                    current_user: UserEntity = Depends(get_current_user_from_token)):
    user = user_repo.get_user_by_id(db=db, user_id=current_user.id)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    return user.likes


@router.get("/", response_model=List[ProductDTO])
async def get_all_products(db: Session = Depends(get_db),
                           page: int = Query(1, ge=1, description="Page number"),
                           items_per_page: int = Query(5, ge=1, description="Items per page"),
                           search: str = Query(None, description="Search query"),
                           current_user: UserEntity = Depends(get_current_user_from_token)) -> List[ProductDTO]:
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return product_repo.get_products(db=db, page=page, items_per_page=items_per_page, search=search)


@router.get("/id/{product_id}", response_model=ProductDTO)
async def get_product_by_id(product_id: int = Path(..., ge=1),
                            db: Session = Depends(get_db),
                            current_user: UserEntity = Depends(get_current_user_from_token)) -> ProductDTO:
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    product = product_repo.get_by_product_id(product_id=product_id, db=db)
    if product is None:
        raise HTTPException(status_code=200, detail="Product not found")
    return product


@router.get("/brand/{brand_name}", response_model=List[ProductDTO])
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
    found_product = product_repo.get_by_product_folder_name(product_name=res, db=db)
    if found_product is None:
        raise HTTPException(status_code=200, detail="no product found database")
    return {'product': found_product,
            'can_consume': can_consume_product(found_product=found_product, current_user=current_user)}


@router.post("/consume/{product_id}", response_model=ProductDTO)
async def consume_product(product_id: int, db: Session = Depends(get_db),
                          current_user: UserEntity = Depends(get_current_user_from_token)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    found_product = product_repo.get_by_product_id(product_id=product_id, db=db)
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


@router.post("/like/{product_id}", response_model=ProductDTO)
async def like(product_id: int, db: Session = Depends(get_db),
               current_user: UserEntity = Depends(get_current_user_from_token)):
    user = user_repo.get_user_by_id(db=db, user_id=current_user.id)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    product = product_repo.get_by_product_id(db=db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=400, detail="Product not found")

    user.likes.append(product)
    db.commit()

    return product


@router.post("/unlike/{product_id}", response_model=ProductDTO)
async def unlike(product_id: int, db: Session = Depends(get_db),
                 current_user: UserEntity = Depends(get_current_user_from_token)):
    user = user_repo.get_user_by_id(db=db, user_id=current_user.id)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    product = product_repo.get_by_product_id(db=db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=400, detail="Product not found")

    user.likes.remove(product)
    db.commit()

    return product
