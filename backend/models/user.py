from sqlalchemy import Column, Integer, String, Float, Enum
from database import Base
import enum


class GoalEnum(str, enum.Enum):
    lose = "lose"
    gain = "gain"
    maintain = "maintain"


class ActivityEnum(str, enum.Enum):
    sedentary = "sedentary"
    light = "light"
    moderate = "moderate"
    active = "active"
    very_active = "very_active"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    sex = Column(String, nullable=True)
    goal = Column(String, nullable=True, default="maintain")
    activity_level = Column(String, nullable=True, default="moderate")
    target_kcal = Column(Float, nullable=True)
    target_protein = Column(Float, nullable=True)
    target_fat = Column(Float, nullable=True)
    target_carbs = Column(Float, nullable=True)
