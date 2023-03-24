from typing import List

from pydantic import BaseModel, EmailStr

from model.diet_model import DietRequest, DietDTO


class UserRegisterRequest(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str
    diet: List[DietRequest]


class UserDTO(BaseModel):
    name: str
    surname: str
    email: EmailStr
    is_active: bool
    diets: List[DietDTO]

    class Config:
        orm_mode = True
