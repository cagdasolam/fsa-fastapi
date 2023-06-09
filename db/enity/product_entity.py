from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from db.base_class import Base

product_ingredient_association = Table('product_ingredient_association', Base.metadata,
                                       Column('product_id', Integer, ForeignKey('products.id')),
                                       Column('ingredient_id', Integer, ForeignKey('ingredients.id'))
                                       )


class ProductEntity(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    brand = Column(String(50))
    name = Column(String(50), unique=True, nullable=False)
    folder_name = Column(String(50), unique=True, nullable=False)
    ingredients = relationship("IngredientEntity", secondary=product_ingredient_association)
    nutrition = Column(JSONB)
    photo_url = Column(String(50))
