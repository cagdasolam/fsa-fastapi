from typing import List, Any

from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db.enity.user_entity import UserEntity
from db.repository import user_repo
from db.session import get_db
from model.user_model import UserRegisterRequest, UserDTO
from route.route_login import get_current_user_from_token

router = APIRouter()


@router.get("/", response_model=List[UserDTO])
def get_all_users(db: Session = Depends(get_db),
                  current_user: UserEntity = Depends(get_current_user_from_token)) -> Any:
    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Not authorized")
    return user_repo.get_users(db=db)


@router.post("/", response_model=UserDTO)
def create_user(user: UserRegisterRequest, db: Session = Depends(get_db)):
    existing_user = user_repo.get_user_by_email(email=user.email, db=db)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already taken")
    user = user_repo.create_new_user(user_request=user, db=db)
    return user
