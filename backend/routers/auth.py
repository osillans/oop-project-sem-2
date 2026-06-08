from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.user import UserCreate, Token, LoginData, UserOut
from services.auth_service import hash_password, verify_password, create_access_token, calculate_nutrition

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=Token, status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="Ім'я користувача вже зайняте")
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email вже зареєстровано")

    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(data.password),
        age=data.age,
        weight=data.weight,
        height=data.height,
        sex=data.sex,
        goal=data.goal,
        activity_level=data.activity_level,
    )

    if all([data.age, data.weight, data.height, data.sex, data.goal, data.activity_level]):
        nutrition = calculate_nutrition(data.age, data.weight, data.height, data.sex, data.goal, data.activity_level)
        user.target_kcal = nutrition["target_kcal"]
        user.target_protein = nutrition["target_protein"]
        user.target_fat = nutrition["target_fat"]
        user.target_carbs = nutrition["target_carbs"]

    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer", "user": user}


@router.post("/login", response_model=Token)
def login(data: LoginData, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Невірний логін або пароль")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer", "user": user}
