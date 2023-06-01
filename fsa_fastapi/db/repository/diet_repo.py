from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from db.enity.diet_entity import DietEntity
from db.repository.ingredient_repo import get_ingredient_by_name
from model.diet_model import DietRequest


def get_diet_by_id(diet_id: int, db: Session):
    try:
        diet = db.query(DietEntity).filter(DietEntity.id == diet_id).first()
    except NoResultFound:
        diet = None
    return diet


def get_diet_by_name(name: str, db: Session):
    try:
        diet = db.query(DietEntity).filter(DietEntity.name == name).first()
    except NoResultFound:
        diet = None
    return diet


def get_diets(db: Session):
    return db.query(DietEntity).all()


def create_diet(new_diet: DietRequest, db: Session):
    try:
        cant_consume = []
        for ingredient in new_diet.cant_consume:
            ingredient_entity = get_ingredient_by_name(name=ingredient.name, db=db)
            cant_consume.append(ingredient_entity)

        diet = DietEntity(name=new_diet.name, cant_consume=cant_consume)
        db.add(diet)
        db.commit()
        db.refresh(diet)
        return diet
    except SQLAlchemyError as e:
        print(str(e))
        db.rollback()
        return None


def delete_diet(diet_id: int, db: Session):
    try:
        diet = db.query(DietEntity).filter(DietEntity.id == diet_id).first()
        db.delete(diet)
        db.commit()
        return True
    except NoResultFound:
        return False
    except SQLAlchemyError as e:
        print(str(e))
        db.rollback()
        return None


def update_diet(diet_id: int, updated_diet: DietRequest, db: Session):
    try:
        diet = db.query(DietEntity).filter(DietEntity.id == diet_id).first()
        diet.name = updated_diet.name
        new_cant_consume = []
        for ingredient in updated_diet.cant_consume:
            ingredient_entity = get_ingredient_by_name(name=ingredient.name, db=db)
            new_cant_consume.append(ingredient_entity)

        diet.ingredients = new_cant_consume
        db.commit()
        return diet
    except NoResultFound:
        return None
    except SQLAlchemyError as e:
        print(str(e))
        db.rollback()
        return None
