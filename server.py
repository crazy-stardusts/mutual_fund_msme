from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import router as auth_router
from routes.protected import router as protected_router
from starlette.middleware.base import BaseHTTPMiddleware




app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Register the custom CORS middleware
# app.add_middleware(CustomCORSMiddleware)

app.include_router(auth_router)
app.include_router(protected_router)
