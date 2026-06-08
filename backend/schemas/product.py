from pydantic import BaseModel
from typing import Optional


class ProductCreate(BaseModel):
    name: str
    kcal_per_100g: float
    protein: float
    fat: float
    carbs: float


class ProductUpdate(ProductCreate):
    pass


class ProductOut(ProductCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True
