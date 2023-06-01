from sqlalchemy import Column, Integer, String

from db.base_class import Base
from model.ingredient_model import IngredientDTO


class IngredientEntity(Base):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    @classmethod
    def from_ingredient_dto(cls, ingredient_dto: IngredientDTO):
        return cls(name=ingredient_dto.name)
