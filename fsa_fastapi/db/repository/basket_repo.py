from db.enity.basket_entity import BasketEntity
from db.enity.product_entity import ProductEntity
from db.enity.user_entity import UserEntity
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from model.basket_model import BasketRequest

from db.enity.diet_entity import DietEntity
from db.repository.ingredient_repo import get_ingredient_by_name
from model.diet_model import DietRequest


def get_basket_by_id(basket_id: int, db: Session):
    try:
        basket = db.query(BasketEntity).filter(BasketEntity.id == basket_id).first()
    except NoResultFound:
        basket = None
    return basket


def get_baskets(db: Session):
    return db.query(BasketEntity).all()


def get_basket(db:Session, basket_id: int):
    try:
        basket = db.query(BasketEntity).filter(BasketEntity.id == basket_id).first()
    except NoResultFound:
        basket = None
    return basket


def get_users_basket(user_id: int, db: Session):
    try:
        user = db.query(UserEntity).get(user_id)

        return user.baskets
    except SQLAlchemyError as e:
        print(str(e))
        db.rollback()
        return None


def create_basket(basket_request: BasketRequest, user: UserEntity, db: Session):
    try:
        products = db.query(ProductEntity).filter(ProductEntity.id.in_(basket_request.products)).all()

        if len(products) != len(basket_request.products):
            raise ValueError("Some product IDs were invalid")

        basket = BasketEntity(name=basket_request.name, products=products)

        db.add(basket)
        db.commit()
        db.refresh(basket)

        user.baskets.append(basket)
        db.commit()
        return basket
    except SQLAlchemyError as e:
        print(str(e))
        db.rollback()
        return None


def delete_basket(basket_id: int, db: Session):
    try:
        basket = db.query(BasketEntity).filter(BasketEntity.id == basket_id).first()
        if not basket:
            return False
        db.delete(basket)
        db.commit()
    except NoResultFound:
        return False
    except SQLAlchemyError as e:
        print(str(e))
        db.rollback()
        return None


def update_basket(basket_id: int, updated_basket: BasketRequest, db: Session):
    try:
        found_basket = db.query(BasketEntity).filter(BasketEntity.id == basket_id).first()
        products = db.query(ProductEntity).filter(ProductEntity.id.in_(updated_basket.products)).all()

        if len(products) != len(updated_basket.products):
            raise ValueError("Some product IDs were invalid")

        found_basket.name = updated_basket.name
        found_basket.products = products

        db.commit()
        return found_basket
    except NoResultFound:
        return None
    except SQLAlchemyError as e:
        print(str(e))
        db.rollback()
        return None


