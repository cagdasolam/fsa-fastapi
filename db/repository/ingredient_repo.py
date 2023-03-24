from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from db.enity.ingredient_entity import IngredientEntity
from model.ingredient_model import IngredientRequest


def get_ingredient_by_id(ingredient_id: int, db: Session):
    try:
        ingredient = db.query(IngredientEntity).filter(IngredientEntity.id == ingredient_id).first()
    except NoResultFound:
        ingredient = None
    return ingredient


def get_ingredient_by_name(name: str, db: Session):
    try:
        ingredient = db.query(IngredientEntity).filter(IngredientEntity.name == name).first()
    except NoResultFound:
        ingredient = None
    return ingredient


def get_ingredients(db: Session):
    return db.query(IngredientEntity).all()


def create_ingredient(new_ingredient: IngredientRequest, db: Session):
    try:
        ingredient = IngredientEntity(name=new_ingredient.name)
        db.add(ingredient)
        db.commit()
        db.refresh(ingredient)
        return ingredient
    except SQLAlchemyError as e:
        print(str(e))
        db.rollback()
        return None


def delete_ingredient(ingredient_id: int, db: Session):
    try:
        ingredient = db.query(IngredientEntity).filter(IngredientEntity.id == ingredient_id).first()
        db.delete(ingredient)
        db.commit()
        return True
    except NoResultFound:
        return False
    except SQLAlchemyError as e:
        print(str(e))
        db.rollback()
        return None


def update_ingredient(ingredient_id: int, updated_ingredient: IngredientRequest, db: Session):
    try:
        product = db.query(IngredientEntity).filter(IngredientEntity.id == ingredient_id).first()
        product.name = updated_ingredient.name
        db.commit()
        return product
    except NoResultFound:
        return None
    except SQLAlchemyError as e:
        print(str(e))
        db.rollback()
        return None
