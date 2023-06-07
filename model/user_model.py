from typing import List

from model.basket_model import BasketDTO
from model.product_model import ProductDTO
from pydantic import BaseModel, EmailStr

from model.diet_model import DietRequest, DietDTO


class UserRegisterRequest(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str
    diet: List[DietRequest]


class UserDTO(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    is_active: bool
    diets: List[DietDTO]
    baskets: List[BasketDTO]
    likes: List[ProductDTO]

    class Config:
        orm_mode = True
