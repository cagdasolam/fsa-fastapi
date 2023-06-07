from typing import List

from pydantic import BaseModel

from model.product_model import ProductDTO


class BasketRequest(BaseModel):
    name: str
    products: List[int]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class BasketDTO(BaseModel):
    id: int
    name: str
    products: List[ProductDTO]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
