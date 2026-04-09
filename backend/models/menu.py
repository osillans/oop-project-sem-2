from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    meals_count = Column(Integer, default=3)

    user = relationship("User", back_populates="menus")
    items = relationship("MenuItem", back_populates="menu", cascade="all, delete-orphan")


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    menu_id = Column(Integer, ForeignKey("menus.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    meal_number = Column(Integer, nullable=False)
    weight_g = Column(Float, nullable=False)

    menu = relationship("Menu", back_populates="items")
    product = relationship("Product", back_populates="menu_items")
