from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.orm.exc import NoResultFound

from db.enity.product_entity import ProductEntity
from db.repository.ingredient_repo import get_ingredient_by_name
from model.product_model import ProductRequest


def get_by_product_id(product_id: int, db: Session):
    try:
        product = db.query(ProductEntity).filter(ProductEntity.id == product_id).first()
        return product
    except NoResultFound:
        return None


def get_by_product_name(product_name: str, db: Session):
    try:
        product = db.query(ProductEntity).filter(ProductEntity.name == product_name).first()
        return product
    except NoResultFound:
        return None


def get_by_product_folder_name(folder_name: str, db: Session):
    try:
        product = db.query(ProductEntity).filter(ProductEntity.folder_name == folder_name).first()
        return product
    except NoResultFound:
        return None


def get_products(db: Session, page: int, items_per_page: int, search: str):
    products_query = db.query(ProductEntity)

    if search:
        products_query = products_query.filter(or_(ProductEntity.name.like(f"%{search}%")))

    products_query = products_query.offset((page - 1) * items_per_page).limit(items_per_page)

    return products_query.all()


def get_products_by_brand(brand_name: str, db: Session):
    try:
        products = db.query(ProductEntity).filter(ProductEntity.brand == brand_name).all()
    except NoResultFound:
        products = None
    return products


def create_product(new_product: ProductRequest, db: Session):
    try:
        ingredients = []
        for ingredient in new_product.ingredients:
            ingredient_entity = get_ingredient_by_name(name=ingredient, db=db)
            ingredients.append(ingredient_entity)

        product = ProductEntity(name=new_product.name, ingredients=ingredients, brand=new_product.brand,
                                folder_name=new_product.folder_name, nutrition=new_product.nutrition.dict(),
                                photo_url=new_product.photo_url)

        db.add(product)
        db.commit()
        db.refresh(product)
        return product
    except SQLAlchemyError as e:
        print(str(e))
        db.rollback()
        return None


def delete_product(product_id: int, db: Session):
    try:
        product = db.query(ProductEntity).filter(ProductEntity.id == product_id).first()
        db.delete(product)
        db.commit()
        return True
    except NoResultFound:
        return False
    except SQLAlchemyError as e:
        print(str(e))
        db.rollback()
        return None


def update_product(product_id: int, updated_product: ProductRequest, db: Session):
    try:
        product = db.query(ProductEntity).filter(ProductEntity.id == product_id).first()

        product.name = updated_product.name

        new_ingredients = []
        for ingredient in updated_product.ingredients:
            ingredient_entity = get_ingredient_by_name(name=ingredient.name, db=db)
            new_ingredients.append(ingredient_entity)

        product.ingredients = new_ingredients
        db.commit()
        return product
    except NoResultFound:
        return None
    except SQLAlchemyError as e:
        print(str(e))
        db.rollback()
        return None
