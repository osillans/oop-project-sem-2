from database import Base
from models.user import User
from models.product import Product
from models.menu import Menu, MenuItem
from sqlalchemy.orm import relationship

User.products = relationship("Product", back_populates="user", cascade="all, delete-orphan")
User.menus = relationship("Menu", back_populates="user", cascade="all, delete-orphan")
