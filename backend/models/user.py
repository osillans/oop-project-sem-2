from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    age = Column(Integer, nullable=True)
    weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    sex = Column(String, nullable=True)
    goal = Column(String, nullable=True)
    activity_level = Column(String, nullable=True)
    target_kcal = Column(Float, nullable=True)
    target_protein = Column(Float, nullable=True)
    target_fat = Column(Float, nullable=True)
    target_carbs = Column(Float, nullable=True)

    products = relationship("Product", back_populates="owner")
    menus = relationship("Menu", back_populates="owner")
