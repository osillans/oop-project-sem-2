# SuperSportyk

Система автоматичного формування персоналізованого раціону харчування на основі заданих показників КБЖВ (калорії, білки, жири, вуглеводи) та наявних продуктів.

## Технологічний стек

Частина - Технологія

Backend - Python, FastAPI, SQLAlchemy, SQLite;
Frontend - React, TypeScript, Vite, Tailwind CSS;
Авторизація - JWT (python-jose), bcrypt (passlib);
Стан - Zustand;
HTTP - Axios

## Базова структура

```
supersportyk/
├── backend/
│   ├── main.py               # Ініціалізація FastAPI, CORS, роутери
│   ├── database.py           # Підключення до SQLite, сесія SQLAlchemy
│   ├── models/
│   │   ├── __init__.py       # Імпорт моделей та зв'язків
│   │   ├── user.py           # Модель користувача
│   │   ├── product.py        # Модель продукту
│   │   └── menu.py           # Моделі меню та позицій
│   ├── schemas/
│   │   └── user.py           # Pydantic схеми користувача
│   ├── routers/
│   │   ├── auth.py           # Реєстрація та вхід
│   │   └── users.py          # Профіль користувача
│   ├── services/
│   │   └── auth_service.py   # JWT, bcrypt, розрахунок КБЖВ
│   └── requirements.txt
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.ts
    └── src/
        ├── main.tsx
        ├── App.tsx
        ├── api/
        │   └── client.ts     # Axios з токеном
        ├── store/
        │   └── authStore.ts  # Zustand сховище
        └── pages/
            ├── LoginPage.tsx
            └── RegisterPage.tsx
```
## Реалізований функціонал

- Реєстрація користувача з параметрами тіла (вік, вага, зріст, стать)
- Автоматичний розрахунок добової норми КБЖВ за формулою Міффліна-Сан Жеора
- Вибір цілі: схуднення / набір маси / підтримка ваги
- Вибір рівня активності
- Авторизація через JWT токен
- Захищені роути для авторизованих користувачів
- Збереження сесії у localStorage

## Розрахунок КБЖВ

Базовий метаболізм (BMR) за формулою Міффліна-Сан Жеора:

```
Чоловіки: BMR = 10 × вага + 6.25 × зріст − 5 × вік + 5
Жінки:    BMR = 10 × вага + 6.25 × зріст − 5 × вік − 161
```

Множники активності:
Рівень - Множник

Сидячий - 1.2;
Легка активність - 1.375;
Помірна - 1.55;
Активний - 1.725;
Дуже активний - 1.9

Коригування за ціллю: −500 ккал (схуднення) / +300 ккал (набір) / без змін (підтримка)

## Запуск

### Вимоги
- Python 3.11+
- Node.js 20+

### Backend
```bash
cd backend
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Інтерфейс: http://localhost:5173
API документація: http://localhost:8001/docs

## API ендпоінти (базові)

| Метод | URL | Опис |
|---|---|---|
| POST | `/api/auth/register` | Реєстрація нового користувача |
| POST | `/api/auth/login` | Вхід, отримання JWT токена |
| GET | `/api/users/me` | Отримання профілю |
| PUT | `/api/users/me` | Оновлення профілю та перерахунок КБЖВ |
