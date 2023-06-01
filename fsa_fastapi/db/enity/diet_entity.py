from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from db.base_class import Base

diet_ingredient_association = Table('diet_ingredient_association', Base.metadata,
                                    Column('diet_id', Integer, ForeignKey('diets.id')),
                                    Column('ingredient_id', Integer, ForeignKey('ingredients.id'))
                                    )


class DietEntity(Base):
    __tablename__ = 'diets'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    cant_consume = relationship("IngredientEntity", secondary=diet_ingredient_association)
