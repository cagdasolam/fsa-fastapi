from typing import List

from pydantic import BaseModel

from model.ingredient_model import IngredientDTO, IngredientRequest


class DietDTO(BaseModel):
    id: int
    name: str
    cant_consume: List[IngredientDTO]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class DietRequest(BaseModel):
    name: str
    cant_consume: List[str]

    class Config:
        arbitrary_types_allowed = True
