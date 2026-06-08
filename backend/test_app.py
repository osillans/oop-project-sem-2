import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

USER_DATA = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "age": 25,
    "weight": 70,
    "height": 175,
    "sex": "male",
    "goal": "maintain",
    "activity_level": "moderate"
}


def get_token():
    client.post("/api/auth/register", json=USER_DATA)
    res = client.post(
        "/api/auth/login",
        data={"username": USER_DATA["username"], "password": USER_DATA["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    return res.json()["access_token"]


# Тест 1: Успішна реєстрація
def test_register_success():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    res = client.post("/api/auth/register", json=USER_DATA)
    assert res.status_code == 201
    assert "access_token" in res.json()
    assert res.json()["user"]["username"] == "testuser"


# Тест 2: Реєстрація з дублікатом email
def test_register_duplicate_email():
    data = USER_DATA.copy()
    data["username"] = "anotheruser"
    res = client.post("/api/auth/register", json=data)
    assert res.status_code == 400
    assert "Email" in res.json()["detail"]


# Тест 3: Реєстрація з дублікатом username
def test_register_duplicate_username():
    data = USER_DATA.copy()
    data["email"] = "another@example.com"
    res = client.post("/api/auth/register", json=data)
    assert res.status_code == 400
    assert "користувача" in res.json()["detail"]


# Тест 4: Успішний вхід
def test_login_success():
    res = client.post(
        "/api/auth/login",
        data={"username": "testuser", "password": "password123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert res.status_code == 200
    assert "access_token" in res.json()
    assert res.json()["token_type"] == "bearer"


# Тест 5: Вхід з невірним паролем
def test_login_wrong_password():
    res = client.post(
        "/api/auth/login",
        data={"username": "testuser", "password": "wrongpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert res.status_code == 401


# Тест 6: Вхід з неіснуючим користувачем
def test_login_nonexistent_user():
    res = client.post(
        "/api/auth/login",
        data={"username": "nobody", "password": "password123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert res.status_code == 401


# Тест 7: Отримання профілю
def test_get_profile():
    token = get_token()
    res = client.get("/api/users/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["username"] == "testuser"
    assert res.json()["email"] == "test@example.com"


# Тест 8: Профіль без токена
def test_get_profile_unauthorized():
    res = client.get("/api/users/me")
    assert res.status_code == 401


# Тест 9: Автоматичний розрахунок КБЖВ при реєстрації
def test_kbjv_calculated_on_register():
    token = get_token()
    res = client.get("/api/users/me", headers={"Authorization": f"Bearer {token}"})
    user = res.json()
    assert user["target_kcal"] is not None
    assert user["target_protein"] is not None
    assert user["target_fat"] is not None
    assert user["target_carbs"] is not None
    assert user["target_kcal"] > 0


# Тест 10: Коректність формули Міффліна (чоловік)
def test_mifflin_formula_male():
    from services.auth_service import calculate_targets
    result = calculate_targets(25, 70, 175, "male", "maintain", "moderate")
    # BMR = 10*70 + 6.25*175 - 5*25 + 5 = 1723.75
    # TDEE = 1723.75 * 1.55 = 2671.8
    assert 2500 < result["target_kcal"] < 2750


# Тест 11: Коректність формули Міффліна (жінка)
def test_mifflin_formula_female():
    from services.auth_service import calculate_targets
    result = calculate_targets(25, 60, 165, "female", "maintain", "moderate")
    # BMR = 10*60 + 6.25*165 - 5*25 - 161 = 1370
    # TDEE = 1370 * 1.55 = 2123.5
    assert 2050 < result["target_kcal"] < 2200


# Тест 12: Ціль схуднення зменшує калорії
def test_goal_lose_reduces_kcal():
    from services.auth_service import calculate_targets
    maintain = calculate_targets(25, 70, 175, "male", "maintain", "moderate")
    lose = calculate_targets(25, 70, 175, "male", "lose", "moderate")
    assert lose["target_kcal"] == maintain["target_kcal"] - 500


# Тест 13: Ціль набору збільшує калорії
def test_goal_gain_increases_kcal():
    from services.auth_service import calculate_targets
    maintain = calculate_targets(25, 70, 175, "male", "maintain", "moderate")
    gain = calculate_targets(25, 70, 175, "male", "gain", "moderate")
    assert gain["target_kcal"] == maintain["target_kcal"] + 300


# Тест 14: Оновлення профілю перераховує КБЖВ
def test_update_profile_recalculates_kbjv():
    token = get_token()
    res = client.put(
        "/api/users/me",
        json={"weight": 80, "goal": "gain", "activity_level": "active"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    updated = res.json()
    assert updated["weight"] == 80
    assert updated["goal"] == "gain"
    assert updated["target_kcal"] is not None


# Тест 15: JWT токен містить правильний user_id
def test_jwt_contains_user_id():
    from services.auth_service import create_access_token, decode_token
    token = create_access_token({"sub": "42"})
    payload = decode_token(token)
    assert payload is not None
    assert payload["sub"] == "42"