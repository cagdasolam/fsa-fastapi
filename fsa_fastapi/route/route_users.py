from typing import List, Any

from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db.enity.user_entity import UserEntity
from db.repository import user_repo
from db.session import get_db
from model.user_model import UserRegisterRequest, UserDTO, UserUpdateDietRequest, UserChangePasswordRequest
from route.route_login import get_current_user_from_token

router = APIRouter()


@router.get("/", response_model=List[UserDTO])
async def get_all_users(db: Session = Depends(get_db),
                        current_user: UserEntity = Depends(get_current_user_from_token)):
    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Not authorized")
    return user_repo.get_users(db=db)


@router.get("/current", response_model=UserDTO)
async def get_current_user(db: Session = Depends(get_db), current_user: UserEntity = Depends(get_current_user_from_token)):
    return current_user


@router.post("/", response_model=UserDTO)
async def create_user(user: UserRegisterRequest, db: Session = Depends(get_db)):
    existing_user = user_repo.get_user_by_email(email=user.email, db=db)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already taken")
    user = user_repo.create_new_user(user_request=user, db=db)
    return user


@router.put("/change-password")
async def change_password(request: UserChangePasswordRequest, db: Session = Depends(get_db),
                          current_user: UserEntity = Depends(get_current_user_from_token)):
    return user_repo.change_password(change_request=request, db=db, user_id=current_user.id)


@router.put("/update-diet", response_model=UserDTO)
async def update_diet(request: UserUpdateDietRequest, db: Session = Depends(get_db),
                          current_user: UserEntity = Depends(get_current_user_from_token)):
    return user_repo.update_diet(db=db, update_request=request, user_id=current_user.id)
