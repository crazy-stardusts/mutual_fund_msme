from fastapi import FastAPI
from routes.auth import router as auth_router
from routes.protected import router as protected_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(protected_router)