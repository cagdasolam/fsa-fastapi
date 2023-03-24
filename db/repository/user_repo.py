from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound

from model.user_model import UserRegisterRequest
from db.enity.user_entity import UserEntity
from db.enity.diet_entity import DietEntity
from db.repository.diet_repo import get_diet_by_name
from core.hashing import Hasher


def get_users(db: Session):
    return db.query(UserEntity).all()


def get_user_by_email(email: str, db: Session):
    try:
        user = db.query(UserEntity).filter(UserEntity.email == email).first()
    except NoResultFound:
        user = None
    return user


def create_new_user(user_request: UserRegisterRequest, db: Session):
    try:
        diets = []
        for diet in user_request.diet:
            diet_entity = get_diet_by_name(name=diet.name, db=db)
            diets.append(diet_entity)

        user = UserEntity(name=user_request.name,
                          surname=user_request.surname,
                          email=user_request.email,
                          password=Hasher.get_password_hash(user_request.password),
                          is_active=True,
                          is_superuser=False,
                          diets=diets
                          )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except SQLAlchemyError as e:
        print(str(e))
        db.rollback()
