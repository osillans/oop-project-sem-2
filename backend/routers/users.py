from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.user import UserResponse, UserUpdate
from services.auth_service import get_user_by_token, calculate_targets

router = APIRouter(prefix="/api/users", tags=["users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    user = get_user_by_token(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="Недійсний токен")
    return user


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserResponse)
def update_me(data: UserUpdate, db: Session = Depends(get_db),
              current_user: User = Depends(get_current_user)):
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(current_user, field, value)

    age = current_user.age
    weight = current_user.weight
    height = current_user.height
    sex = current_user.sex
    goal = current_user.goal
    activity = current_user.activity_level

    if all([age, weight, height, sex, goal, activity]):
        targets = calculate_targets(age, weight, height, sex, goal, activity)
        for k, v in targets.items():
            setattr(current_user, k, v)

    db.commit()
    db.refresh(current_user)
    return current_user
