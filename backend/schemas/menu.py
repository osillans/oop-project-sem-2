from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class MenuItemOut(BaseModel):
    id: int
    product_id: int
    product_name: str
    meal_number: int
    weight_g: float
    kcal: float
    protein: float
    fat: float
    carbs: float

    class Config:
        from_attributes = True


class MenuOut(BaseModel):
    id: int
    meals_count: int
    created_at: Optional[datetime] = None
    total_kcal: float
    total_protein: float
    total_fat: float
    total_carbs: float
    items: List[MenuItemOut]

    class Config:
        from_attributes = True


class MenuGenerateRequest(BaseModel):
    meals_count: int = 3
    strategy: str = "proportional"
    product_ids: Optional[List[int]] = None
