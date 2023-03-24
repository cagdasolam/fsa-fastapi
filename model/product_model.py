from typing import List

from pydantic import BaseModel

from model.ingredient_model import IngredientDTO, IngredientRequest


class ProductRequest(BaseModel):
    name: str
    ingredients: List[IngredientRequest]

    class Config:
        arbitrary_types_allowed = True


class ProductDTO(BaseModel):
    id: int
    name: str
    ingredients: List[IngredientDTO]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
