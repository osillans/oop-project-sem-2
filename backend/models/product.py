from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    kcal_per_100g = Column(Float)
    protein = Column(Float)
    fat = Column(Float)
    carbs = Column(Float)

    owner = relationship("User", back_populates="products")
    menu_items = relationship("MenuItem", back_populates="product")
