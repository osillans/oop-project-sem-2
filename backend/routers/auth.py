from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.user import UserRegister, UserResponse, TokenResponse
from services.auth_service import (
    hash_password, verify_password, create_access_token, calculate_targets
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(data: UserRegister, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email вже використовується")
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="Ім'я користувача вже зайняте")

    targets = {}
    if all([data.age, data.weight, data.height, data.sex, data.goal, data.activity_level]):
        targets = calculate_targets(
            data.age, data.weight, data.height, data.sex, data.goal, data.activity_level
        )

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
        **targets,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token, user=UserResponse.model_validate(user))


@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Невірне ім'я користувача або пароль")

    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token, user=UserResponse.model_validate(user))
