from typing import Any, List

from PIL import Image
from fastapi import APIRouter, Depends, Path, UploadFile, File
from fastapi import HTTPException
from sqlalchemy.orm import Session

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
                           current_user: UserEntity = Depends(get_current_user_from_token)) -> Any:
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return product_repo.get_products(db=db)


@router.get("/{product_id}", response_model=ProductDTO)
async def get_product_by_id(product_id: int = Path(..., ge=1),
                            db: Session = Depends(get_db),
                            current_user: UserEntity = Depends(get_current_user_from_token)) -> Any:
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    product = product_repo.get_by_product_id(product_id=product_id, db=db)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=ProductDTO)
async def create_product(new_product: ProductRequest,
                         db: Session = Depends(get_db),
                         current_user: UserEntity = Depends(get_current_user_from_token)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    product = product_repo.create_product(new_product=new_product, db=db)
    if product is None:
        raise HTTPException(status_code=404, detail="Product already exist")
    return product


@router.put("/{product_id}", response_model=ProductDTO)
async def update_product(product_id: int,
                         updated_product: ProductRequest,
                         db: Session = Depends(get_db),
                         current_user: UserEntity = Depends(get_current_user_from_token)) -> Any:
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    product = product_repo.update_product(product_id=product_id, updated_product=updated_product, db=db)
    if product is None:
        raise HTTPException(status_code=404, detail="there is no product id with {}".format(product_id))
    return product


@router.delete("/{product_id}")
async def delete_product(product_id: int,
                         db: Session = Depends(get_db),
                         current_user: UserEntity = Depends(get_current_user_from_token)) -> Any:
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    product = product_repo.delete_product(product_id=product_id, db=db)
    if product is None:
        raise HTTPException(status_code=404, detail="there is no product id with {}".format(product_id))


@router.post("/photo")
async def predict_product_from_photo(file: UploadFile = File(...),
                                     db: Session = Depends(get_db),
                                     current_user: UserEntity = Depends(get_current_user_from_token)
                                     ) -> Any:
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    img = Image.open(file.file)
    res = prediction.prediction_image(img)
    if res is None:
        raise HTTPException(status_code=404, detail="no product found")
    found_product = product_repo.get_by_product_name(product_name=res, db=db)
    return can_consume_product(found_product=found_product, current_user=current_user)


def can_consume_product(found_product: ProductEntity, current_user: UserEntity) -> bool:
    ingredients_set = set(found_product.ingredients)
    diets_set = {frozenset(diet.cant_consume) for diet in current_user.diets}
    for cant_consume_set in diets_set:
        if cant_consume_set & ingredients_set:
            return False
    return True
