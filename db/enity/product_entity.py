from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from db.base_class import Base

product_ingredient_association = Table('product_ingredient_association', Base.metadata,
                                       Column('product_id', Integer, ForeignKey('products.id')),
                                       Column('ingredient_id', Integer, ForeignKey('ingredients.id'))
                                       )


class ProductEntity(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    ingredients = relationship("IngredientEntity", secondary=product_ingredient_association)
