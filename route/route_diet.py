from typing import Any, List

from fastapi import APIRouter, Depends, Path
from fastapi import HTTPException
from sqlalchemy.orm import Session

from db.enity.user_entity import UserEntity
from db.repository import diet_repo
from db.session import get_db
from model.diet_model import DietDTO, DietRequest
from route.route_login import get_current_user_from_token

router = APIRouter()


@router.get("/", response_model=List[DietDTO])
async def get_all_diets(db: Session = Depends(get_db),
                        current_user: UserEntity = Depends(get_current_user_from_token)) -> Any:
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return diet_repo.get_diets(db=db)


@router.get("/{diet_id}", response_model=DietDTO)
async def get_diet_by_id(diet_id: int = Path(..., ge=1),
                            db: Session = Depends(get_db),
                            current_user: UserEntity = Depends(get_current_user_from_token)) -> Any:
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    diet = diet_repo.get_diet_by_id(diet_id=diet_id, db=db)
    if diet is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return diet


@router.post("/", response_model=DietDTO)
async def create_diet(new_diet: DietRequest,
                         db: Session = Depends(get_db),
                         current_user: UserEntity = Depends(get_current_user_from_token)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    diet = diet_repo.create_diet(new_diet=new_diet, db=db)
    if diet is None:
        raise HTTPException(status_code=404, detail="Product already exist")
    return diet


@router.put("/{diet_id}", response_model=DietDTO)
async def update_diet(diet_id: int,
                         updated_diet: DietRequest,
                         db: Session = Depends(get_db),
                         current_user: UserEntity = Depends(get_current_user_from_token)) -> Any:
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    diet = diet_repo.update_diet(diet_id=diet_id, updated_diet=updated_diet, db=db)
    if diet is None:
        raise HTTPException(status_code=404, detail="there is no product id with {}".format(diet_id))
    return diet


@router.delete("/{product_id}")
async def delete_diet(diet_id: int,
                         db: Session = Depends(get_db),
                         current_user: UserEntity = Depends(get_current_user_from_token)) -> Any:
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    diet = diet_repo.delete_diet(diet_id=diet_id, db=db)
    if diet is None:
        raise HTTPException(status_code=404, detail="there is no product id with {}".format(diet_id))
