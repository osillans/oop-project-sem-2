from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.menu import Menu, MenuItem
from models.product import Product
from schemas.menu import MenuOut, MenuItemOut, MenuGenerateRequest
from services.optimizer import optimize_menu
from routers.users import get_current_user
from models.user import User

router = APIRouter(prefix="/api/menu", tags=["menu"])


def build_menu_out(menu: Menu) -> MenuOut:
    items = []
    for item in menu.items:
        items.append(MenuItemOut(
            id=item.id,
            product_id=item.product_id,
            product_name=item.product.name,
            meal_number=item.meal_number,
            weight_g=item.weight_g,
            kcal=round(item.product.kcal_per_100g * item.weight_g / 100, 1),
            protein=round(item.product.protein * item.weight_g / 100, 1),
            fat=round(item.product.fat * item.weight_g / 100, 1),
            carbs=round(item.product.carbs * item.weight_g / 100, 1),
        ))

    total_kcal = sum(i.kcal for i in items)
    total_protein = sum(i.protein for i in items)
    total_fat = sum(i.fat for i in items)
    total_carbs = sum(i.carbs for i in items)

    return MenuOut(
        id=menu.id,
        meals_count=menu.meals_count,
        created_at=menu.created_at,
        total_kcal=round(total_kcal, 1),
        total_protein=round(total_protein, 1),
        total_fat=round(total_fat, 1),
        total_carbs=round(total_carbs, 1),
        items=items,
    )


@router.post("/generate", response_model=MenuOut)
def generate_menu(
    req: MenuGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.target_kcal:
        raise HTTPException(status_code=400, detail="Спочатку заповніть профіль для розрахунку КБЖВ")

    products = db.query(Product).filter(Product.user_id == current_user.id).all()
    if req.product_ids:
        products = [p for p in products if p.id in req.product_ids]
    if not products:
        raise HTTPException(status_code=400, detail="Додайте або виберіть продукти перед генерацією меню")

    products_data = [{"id": p.id, "name": p.name, "kcal_per_100g": p.kcal_per_100g,
                      "protein": p.protein, "fat": p.fat, "carbs": p.carbs} for p in products]

    optimized = optimize_menu(
        products=products_data,
        target_kcal=current_user.target_kcal,
        target_protein=current_user.target_protein,
        target_fat=current_user.target_fat,
        target_carbs=current_user.target_carbs,
        meals_count=req.meals_count,
        strategy_name=req.strategy,
    )

    menu = Menu(user_id=current_user.id, meals_count=req.meals_count)
    db.add(menu)
    db.flush()

    for item_data in optimized:
        item = MenuItem(
            menu_id=menu.id,
            product_id=item_data["product_id"],
            meal_number=item_data["meal_number"],
            weight_g=item_data["weight_g"],
        )
        db.add(item)

    db.commit()
    db.refresh(menu)
    return build_menu_out(menu)


@router.get("/history", response_model=List[MenuOut])
def get_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    menus = db.query(Menu).filter(Menu.user_id == current_user.id).order_by(Menu.created_at.desc()).limit(10).all()
    return [build_menu_out(m) for m in menus]


@router.get("/{menu_id}", response_model=MenuOut)
def get_menu(menu_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    menu = db.query(Menu).filter(Menu.id == menu_id, Menu.user_id == current_user.id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Меню не знайдено")
    return build_menu_out(menu)
