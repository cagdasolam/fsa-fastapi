from typing import List

from model.basket_model import BasketDTO
from model.diet_model import DietRequest, DietDTO
from model.product_model import ProductDTO
from pydantic import BaseModel, EmailStr


class UserRegisterRequest(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str
    diet: List[str]


class UserChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str


class UserUpdateDietRequest(BaseModel):
    new_diet: List[str]


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
