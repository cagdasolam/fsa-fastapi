from typing import List, Optional

from pydantic import BaseModel

from model.ingredient_model import IngredientDTO, IngredientRequest


class ProductNutritionPer100GramRequest(BaseModel):
    calories: int
    fat: int
    saturated_fat: int
    carbs: int
    sugar: int
    fiber: int
    protein: int
    salt: int


class ProductRequest(BaseModel):
    brand: str
    name: str
    ingredients: List[IngredientRequest]
    nutrition: ProductNutritionPer100GramRequest

    class Config:
        arbitrary_types_allowed = True


class ProductNutritionPer100GramDTO(BaseModel):
    calories: Optional[int]
    fat: Optional[int]
    saturated_fat: Optional[int]
    carbs: Optional[int]
    sugar: Optional[int]
    fiber: Optional[int]
    protein: Optional[int]
    salt: Optional[int]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ProductDTO(BaseModel):
    id: int
    brand: str
    name: str
    ingredients: List[IngredientDTO]
    nutrition: ProductNutritionPer100GramDTO

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
