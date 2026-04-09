from pydantic import BaseModel, EmailStr
from typing import Optional


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    sex: Optional[str] = None
    goal: Optional[str] = "maintain"
    activity_level: Optional[str] = "moderate"


class UserUpdate(BaseModel):
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    sex: Optional[str] = None
    goal: Optional[str] = None
    activity_level: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    sex: Optional[str] = None
    goal: Optional[str] = None
    activity_level: Optional[str] = None
    target_kcal: Optional[float] = None
    target_protein: Optional[float] = None
    target_fat: Optional[float] = None
    target_carbs: Optional[float] = None

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
