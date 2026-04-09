from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models

models.Base.metadata.create_all(bind=engine)

from routers.auth import router as auth_router
from routers.users import router as users_router

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

@app.get("/")
def root():
    return {"message": "SuperSportyk API працює"}
