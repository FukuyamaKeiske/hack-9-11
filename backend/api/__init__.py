from fastapi import FastAPI
from .api import router as api_router
from auth.auth import router as auth_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(api_router)
