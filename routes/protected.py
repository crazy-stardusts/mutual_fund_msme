from typing import Annotated
from fastapi import APIRouter, Depends
from requests import Session
from core.security import get_current_user
from datetime import datetime

from db.session import get_db
from models.fund_plans import FundPlan
from models.user import User

router = APIRouter()

@router.get("/protected-route")
async def protected_route(current_user: Annotated[User, Depends(get_current_user)]):
    return {"message": "You are authenticated!", "user" : current_user}

@router.get("/mutual-funds")
async def get_mutual_funds(page: int = 1, size : int = 10, db : Session = Depends(get_db)):
    offset = (page - 1) * size
    return db.query(FundPlan).offset(offset).limit(size).all()
    
