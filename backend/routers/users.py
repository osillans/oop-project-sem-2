from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.user import UserOut, UserUpdate
from services.auth_service import calculate_nutrition, decode_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/api/users", tags=["users"])
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    payload = decode_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Недійсний токен")
    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not user:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    return user


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserOut)
def update_me(data: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(current_user, field, value)

    if all([current_user.age, current_user.weight, current_user.height,
            current_user.sex, current_user.goal, current_user.activity_level]):
        nutrition = calculate_nutrition(
            current_user.age, current_user.weight, current_user.height,
            current_user.sex, current_user.goal, current_user.activity_level,
        )
        current_user.target_kcal = nutrition["target_kcal"]
        current_user.target_protein = nutrition["target_protein"]
        current_user.target_fat = nutrition["target_fat"]
        current_user.target_carbs = nutrition["target_carbs"]

    db.commit()
    db.refresh(current_user)
    return current_user
