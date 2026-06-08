from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.menu import Menu
from routers.users import get_current_user
from models.user import User
from routers.menu import build_menu_out

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/summary")
def get_summary(menu_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    menu = db.query(Menu).filter(Menu.id == menu_id, Menu.user_id == current_user.id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Меню не знайдено")

    menu_out = build_menu_out(menu)

    def pct(actual, target):
        if not target:
            return 0
        return round(actual / target * 100, 1)

    return {
        "menu_id": menu_id,
        "actual": {
            "kcal": menu_out.total_kcal,
            "protein": menu_out.total_protein,
            "fat": menu_out.total_fat,
            "carbs": menu_out.total_carbs,
        },
        "target": {
            "kcal": current_user.target_kcal,
            "protein": current_user.target_protein,
            "fat": current_user.target_fat,
            "carbs": current_user.target_carbs,
        },
        "percent": {
            "kcal": pct(menu_out.total_kcal, current_user.target_kcal),
            "protein": pct(menu_out.total_protein, current_user.target_protein),
            "fat": pct(menu_out.total_fat, current_user.target_fat),
            "carbs": pct(menu_out.total_carbs, current_user.target_carbs),
        },
    }
