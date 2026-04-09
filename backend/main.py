from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models

models.Base.metadata.create_all(bind=engine)

from routers.auth import router as auth_router
from routers.users import router as users_router
from routers.products import router as products_router
from routers.menu import router as menu_router
from routers.analytics import router as analytics_router

app = FastAPI(title="SuperSportyk API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(products_router)
app.include_router(menu_router)
app.include_router(analytics_router)


@app.get("/")
def root():
    return {"message": "SuperSportyk API працює"}
