from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    meals_count = Column(Integer)

    owner = relationship("User", back_populates="menus")
    items = relationship("MenuItem", back_populates="menu", cascade="all, delete-orphan")


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    menu_id = Column(Integer, ForeignKey("menus.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    meal_number = Column(Integer)
    weight_g = Column(Float)

    menu = relationship("Menu", back_populates="items")
    product = relationship("Product", back_populates="menu_items")
