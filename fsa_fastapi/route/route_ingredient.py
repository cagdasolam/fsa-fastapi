from typing import Any, List

from fastapi import APIRouter, Depends, Path
from fastapi import HTTPException
from sqlalchemy.orm import Session

from db.enity.user_entity import UserEntity
from db.repository import ingredient_repo
from db.session import get_db
from model.ingredient_model import IngredientDTO, IngredientRequest
from route.route_login import get_current_user_from_token

router = APIRouter()


@router.get("/", response_model=List[IngredientDTO])
async def get_all_ingredients(db: Session = Depends(get_db),
                              current_user: UserEntity = Depends(get_current_user_from_token)) -> [IngredientDTO]:
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return ingredient_repo.get_ingredients(db=db)


@router.get("/get/{id}", response_model=IngredientDTO)
async def get_ingredient_by_id(ingredient_id: int = Path(..., ge=1),
                               db: Session = Depends(get_db),
                               current_user: UserEntity = Depends(get_current_user_from_token)) -> IngredientDTO:
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return ingredient_repo.get_ingredient_by_id(ingredient_id=ingredient_id, db=db)


@router.post("/", response_model=IngredientDTO)
async def create_ingredient(new_ingredient: IngredientRequest,
                            db: Session = Depends(get_db),
                            current_user: UserEntity = Depends(get_current_user_from_token)) -> IngredientDTO:
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
    ingredient = ingredient_repo.create_ingredient(new_ingredient=new_ingredient, db=db)
    if ingredient is None:
        raise HTTPException(status_code=200, detail="Ingredient already exist")
    return ingredient


@router.put("/{ingredient_id}", response_model=IngredientDTO)
async def update_product(ingredient_id: int,
                         updated_ingredient: IngredientRequest,
                         db: Session = Depends(get_db),
                         current_user: UserEntity = Depends(get_current_user_from_token)) -> Any:
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
    product = ingredient_repo.update_ingredient(ingredient_id=ingredient_id, updated_ingredient=updated_ingredient,
                                                db=db)
    if product is None:
        raise HTTPException(status_code=200, detail="there is no ingredient id with {}".format(ingredient_id))
    return product


@router.delete("/{ingredient_id}")
async def delete_product(ingredient_id: int,
                         db: Session = Depends(get_db),
                         current_user: UserEntity = Depends(get_current_user_from_token)) -> Any:
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
    product = ingredient_repo.delete_ingredient(ingredient_id=ingredient_id, db=db)
    if product is None:
        raise HTTPException(status_code=200, detail="there is no ingredient id with {}".format(ingredient_id))
