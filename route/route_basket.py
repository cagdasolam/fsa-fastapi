from random import sample
from typing import Any, List

import prediction
from PIL import Image
from db.enity.product_entity import ProductEntity
from db.enity.user_entity import UserEntity
from db.repository import basket_repo
from db.session import get_db
from fastapi import APIRouter, Depends, Path, UploadFile, File
from fastapi import HTTPException
from model.product_model import ProductDTO, ProductRequest
from model.basket_model import BasketRequest, BasketDTO
from route.route_login import get_current_user_from_token
from route.route_users import router
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/", response_model=List[BasketDTO])
async def get_all_baskets(db: Session = Depends(get_db),
                          current_user: UserEntity = Depends(get_current_user_from_token)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return basket_repo.get_baskets(db=db)


@router.get("/basket/{basket_id}", response_model=BasketDTO)
async def get_basket_by_id(basker_id: int, db: Session = Depends(get_db),
                           current_user: UserEntity = Depends(get_current_user_from_token)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return basket_repo.get_basket(basket_id=basker_id, db=db)


@router.get("/user", response_model=List[BasketDTO])
async def get_users_basket(db: Session = Depends(get_db),
                           current_user: UserEntity = Depends(get_current_user_from_token)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return basket_repo.get_users_basket(db=db, user_id=current_user.id)


@router.post("/", response_model=BasketDTO)
async def create_basket(basket: BasketRequest, db: Session = Depends(get_db),
                        current_user: UserEntity = Depends(get_current_user_from_token)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return basket_repo.create_basket(basket_request=basket, user=current_user, db=db)


@router.put("/{basket_id}", response_model=BasketDTO)
async def update_basket(basket_id: int, basket: BasketRequest, db: Session = Depends(get_db),
                        current_user: UserEntity = Depends(get_current_user_from_token)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return basket_repo.update_basket(basket_id=basket_id, updated_basket=basket, db=db)


@router.delete("/{basket_id}")
async def delete_basket(basket_id: int, db: Session = Depends(get_db),
                        current_user: UserEntity = Depends(get_current_user_from_token)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return basket_repo.delete_basket(basket_id=basket_id, db=db)
