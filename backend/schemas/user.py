from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    sex: Optional[str] = None
    goal: Optional[str] = None
    activity_level: Optional[str] = None


class UserUpdate(BaseModel):
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    sex: Optional[str] = None
    goal: Optional[str] = None
    activity_level: Optional[str] = None


class UserOut(BaseModel):
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


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut


class LoginData(BaseModel):
    username: str
    password: str
