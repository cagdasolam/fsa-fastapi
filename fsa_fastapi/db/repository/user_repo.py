from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from core.hashing import Hasher
from db.enity.user_entity import UserEntity
from db.repository.diet_repo import get_diet_by_name
from model.user_model import UserRegisterRequest, UserChangePasswordRequest, UserUpdateDietRequest
from sqlalchemy.testing.plugin.plugin_base import logging


def get_users(db: Session):
    return db.query(UserEntity).all()


def get_user_by_id(db: Session, user_id: int):
    try:
        user = db.query(UserEntity).filter(UserEntity.id == user_id).first()
    except NoResultFound:
        user = None
    return user


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
            diet_entity = get_diet_by_name(name=diet, db=db)
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


def change_password(change_request: UserChangePasswordRequest, db: Session, user_id: int):
    try:
        user = db.query(UserEntity).filter(UserEntity.id == user_id).first()
        if not user or not Hasher.verify_password(change_request.old_password, user.password):
            return False
        if change_request.old_password == change_request.new_password:
            return False

        user.password = Hasher.get_password_hash(change_request.new_password)

        db.commit()
        return True
    except SQLAlchemyError as e:
        logging.error(f"Error changing password: {str(e)}")
        db.rollback()
        return False


def update_diet(db: Session, update_request: UserUpdateDietRequest, user_id: int):
    try:
        user = db.query(UserEntity).filter(UserEntity.id == user_id).first()
        diets = []
        for diet in update_request.new_diet:
            diet_entity = get_diet_by_name(name=diet, db=db)
            diets.append(diet_entity)

        user.diets = diets
        db.commit()
        return user

    except NoResultFound:
        return None
