from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.product import Product
from schemas.product import ProductCreate, ProductUpdate, ProductOut
from routers.users import get_current_user
from models.user import User

router = APIRouter(prefix="/api/products", tags=["products"])

DEFAULT_PRODUCTS = [
    # М'ясо та птиця
    {"name": "Куряче філе (варене)", "kcal_per_100g": 165, "protein": 31.0, "fat": 3.6, "carbs": 0.0},
    {"name": "Куряча грудка (запечена)", "kcal_per_100g": 150, "protein": 30.0, "fat": 3.2, "carbs": 0.0},
    {"name": "Яловичина (варена)", "kcal_per_100g": 218, "protein": 26.0, "fat": 12.0, "carbs": 0.0},
    {"name": "Свинина (пісна, варена)", "kcal_per_100g": 200, "protein": 27.0, "fat": 10.0, "carbs": 0.0},
    {"name": "Індичка філе (варена)", "kcal_per_100g": 135, "protein": 29.0, "fat": 1.5, "carbs": 0.0},
    {"name": "Тунець (консерва у воді)", "kcal_per_100g": 96, "protein": 22.0, "fat": 0.5, "carbs": 0.0},
    {"name": "Лосось (запечений)", "kcal_per_100g": 208, "protein": 23.0, "fat": 13.0, "carbs": 0.0},
    {"name": "Яйце куряче (ціле)", "kcal_per_100g": 155, "protein": 13.0, "fat": 11.0, "carbs": 1.1},
    {"name": "Яєчний білок", "kcal_per_100g": 52, "protein": 11.0, "fat": 0.2, "carbs": 0.7},
    {"name": "Скумбрія (варена)", "kcal_per_100g": 211, "protein": 19.0, "fat": 14.0, "carbs": 0.0},
    # Молочні продукти
    {"name": "Сир кисломолочний 0%", "kcal_per_100g": 71, "protein": 16.0, "fat": 0.0, "carbs": 3.0},
    {"name": "Сир кисломолочний 5%", "kcal_per_100g": 121, "protein": 17.0, "fat": 5.0, "carbs": 3.0},
    {"name": "Грецький йогурт (0%)", "kcal_per_100g": 59, "protein": 10.0, "fat": 0.4, "carbs": 3.6},
    {"name": "Молоко 2.5%", "kcal_per_100g": 52, "protein": 2.9, "fat": 2.5, "carbs": 4.7},
    {"name": "Кефір 1%", "kcal_per_100g": 40, "protein": 3.4, "fat": 1.0, "carbs": 4.7},
    {"name": "Сметана 15%", "kcal_per_100g": 158, "protein": 2.6, "fat": 15.0, "carbs": 3.0},
    {"name": "Сир твердий (Гауда)", "kcal_per_100g": 356, "protein": 25.0, "fat": 27.0, "carbs": 2.2},
    {"name": "Сир твердий (Пармезан)", "kcal_per_100g": 431, "protein": 38.0, "fat": 29.0, "carbs": 4.1},
    # Крупи та злаки
    {"name": "Гречка (варена)", "kcal_per_100g": 110, "protein": 4.1, "fat": 0.7, "carbs": 21.0},
    {"name": "Вівсянка (варена)", "kcal_per_100g": 68, "protein": 2.5, "fat": 1.5, "carbs": 12.0},
    {"name": "Рис білий (варений)", "kcal_per_100g": 130, "protein": 2.7, "fat": 0.3, "carbs": 28.0},
    {"name": "Рис бурий (варений)", "kcal_per_100g": 111, "protein": 2.6, "fat": 0.9, "carbs": 23.0},
    {"name": "Макарони (варені)", "kcal_per_100g": 158, "protein": 5.5, "fat": 0.9, "carbs": 31.0},
    {"name": "Перловка (варена)", "kcal_per_100g": 109, "protein": 3.0, "fat": 0.4, "carbs": 22.0},
    {"name": "Кукурудзяна крупа (варена)", "kcal_per_100g": 86, "protein": 1.8, "fat": 0.6, "carbs": 18.0},
    {"name": "Хліб цільнозерновий", "kcal_per_100g": 247, "protein": 9.0, "fat": 3.4, "carbs": 41.0},
    {"name": "Вівсяні пластівці (сухі)", "kcal_per_100g": 367, "protein": 13.0, "fat": 6.9, "carbs": 62.0},
    # Бобові
    {"name": "Сочевиця (варена)", "kcal_per_100g": 116, "protein": 9.0, "fat": 0.4, "carbs": 20.0},
    {"name": "Нут (варений)", "kcal_per_100g": 164, "protein": 8.9, "fat": 2.6, "carbs": 27.0},
    {"name": "Квасоля (варена)", "kcal_per_100g": 127, "protein": 8.7, "fat": 0.5, "carbs": 22.0},
    # Овочі
    {"name": "Броколі (варена)", "kcal_per_100g": 35, "protein": 2.4, "fat": 0.4, "carbs": 5.1},
    {"name": "Морква (сира)", "kcal_per_100g": 41, "protein": 0.9, "fat": 0.2, "carbs": 10.0},
    {"name": "Огірок свіжий", "kcal_per_100g": 15, "protein": 0.7, "fat": 0.1, "carbs": 3.6},
    {"name": "Томат свіжий", "kcal_per_100g": 18, "protein": 0.9, "fat": 0.2, "carbs": 3.9},
    {"name": "Капуста білокачанна", "kcal_per_100g": 25, "protein": 1.3, "fat": 0.1, "carbs": 5.8},
    {"name": "Картопля (варена)", "kcal_per_100g": 80, "protein": 2.0, "fat": 0.1, "carbs": 17.0},
    {"name": "Батат (запечений)", "kcal_per_100g": 90, "protein": 2.0, "fat": 0.1, "carbs": 21.0},
    {"name": "Цибуля ріпчаста", "kcal_per_100g": 40, "protein": 1.1, "fat": 0.1, "carbs": 9.3},
    {"name": "Шпинат свіжий", "kcal_per_100g": 23, "protein": 2.9, "fat": 0.4, "carbs": 3.6},
    {"name": "Болгарський перець", "kcal_per_100g": 31, "protein": 1.0, "fat": 0.3, "carbs": 6.0},
    {"name": "Кабачок (варений)", "kcal_per_100g": 24, "protein": 1.5, "fat": 0.3, "carbs": 4.6},
    # Фрукти
    {"name": "Яблуко", "kcal_per_100g": 52, "protein": 0.3, "fat": 0.2, "carbs": 14.0},
    {"name": "Банан", "kcal_per_100g": 89, "protein": 1.1, "fat": 0.3, "carbs": 23.0},
    {"name": "Апельсин", "kcal_per_100g": 47, "protein": 0.9, "fat": 0.1, "carbs": 12.0},
    {"name": "Полуниця", "kcal_per_100g": 32, "protein": 0.7, "fat": 0.3, "carbs": 7.7},
    {"name": "Чорниця", "kcal_per_100g": 57, "protein": 0.7, "fat": 0.3, "carbs": 14.0},
    {"name": "Груша", "kcal_per_100g": 57, "protein": 0.4, "fat": 0.1, "carbs": 15.0},
    # Горіхи та жири
    {"name": "Мигдаль", "kcal_per_100g": 579, "protein": 21.0, "fat": 50.0, "carbs": 22.0},
    {"name": "Волоський горіх", "kcal_per_100g": 654, "protein": 15.0, "fat": 65.0, "carbs": 14.0},
    {"name": "Арахіс", "kcal_per_100g": 567, "protein": 26.0, "fat": 49.0, "carbs": 16.0},
    {"name": "Арахісова паста (без цукру)", "kcal_per_100g": 588, "protein": 25.0, "fat": 50.0, "carbs": 20.0},
    {"name": "Оливкова олія", "kcal_per_100g": 884, "protein": 0.0, "fat": 100.0, "carbs": 0.0},
    {"name": "Авокадо", "kcal_per_100g": 160, "protein": 2.0, "fat": 15.0, "carbs": 9.0},
]


@router.get("", response_model=List[ProductOut])
def get_products(search: str = "", db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(Product).filter(Product.user_id == current_user.id)
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    return query.all()


@router.post("", response_model=ProductOut, status_code=201)
def create_product(data: ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    product = Product(**data.model_dump(), user_id=current_user.id)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, data: ProductUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == product_id, Product.user_id == current_user.id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Продукт не знайдено")
    for field, value in data.model_dump().items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == product_id, Product.user_id == current_user.id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Продукт не знайдено")
    db.delete(product)
    db.commit()


@router.post("/seed", status_code=201)
def seed_products(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing_names = {p.name for p in db.query(Product.name).filter(Product.user_id == current_user.id).all()}
    added = 0
    for p in DEFAULT_PRODUCTS:
        if p["name"] not in existing_names:
            db.add(Product(**p, user_id=current_user.id))
            added += 1
    db.commit()
    return {"added": added}
