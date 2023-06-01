from pydantic import BaseModel


class IngredientDTO(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class IngredientRequest(BaseModel):
    name: str
