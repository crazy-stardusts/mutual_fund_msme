from typing import Annotated
from fastapi import APIRouter, Depends
from requests import Session
from core.security import get_current_user
from datetime import datetime

from db.session import get_db
from models.fund_plans import FundPlan
from models.holdings import Holdings
from models.user import User

router = APIRouter()

@router.get("/protected-route")
async def protected_route(current_user: Annotated[User, Depends(get_current_user)]):
    return {"message": "You are authenticated!", "user" : current_user}

@router.get("/mutual-funds")
async def get_mutual_funds(page: int = 1, size : int = 10, db : Session = Depends(get_db)):
    offset = (page - 1) * size
    return db.query(FundPlan).offset(offset).limit(size).all()

@router.post("/mutual-funds/{plan_id}")
async def get_mutual_fund_by_id(plan_id: int, units: int, current_user: Annotated[User, Depends(get_current_user)], db : Session = Depends(get_db)):
    mutual_fund = db.query(FundPlan).filter(FundPlan.plan_id == plan_id).first()
    if not mutual_fund:
        return {"success" : False, "message" : "Invalid plan id"}
    holding = db.query(Holdings).filter(Holdings.plan_id == plan_id, Holdings.user_id == current_user.id).first()
    if holding:
        holding.number_of_units += units
        db.commit()
        return {"success" : True, "message" : "Units added successfully"}
    holding = Holdings(user_id = current_user.id, plan_id = plan_id, number_of_units = units, nav = mutual_fund.nav)
    db.add(holding)
    db.commit()
    return {"success" : True, "message" : "Units added successfully"}

@router.get("/mutual-funds/portfolio")
async def get_portfolio(current_user: Annotated[User, Depends(get_current_user)], db : Session = Depends(get_db)):
    holdings =  db.query(Holdings).filter(Holdings.user_id == current_user.id).all()
    for holding in holdings:
        holding.mf_details = db.query(FundPlan).filter(FundPlan.plan_id == holding.plan_id).first()
        holding.username = current_user.username
        holding.amount = holding.nav * holding.number_of_units
        holding.risk_grade = holding.mf_details.risk_grade
        if(holding.mf_details.risk_grade == "High"):
            holding.loan_eligibility = float(holding.amount) * 0.8
        elif(holding.mf_details.risk_grade == "Medium"):
            holding.loan_eligibility = float(holding.amount) * 0.6
        else:
            holding.loan_eligibility = float(holding.amount) * 0.5
    return holdings

@router.get("/loans")
async def get_loans(current_user: Annotated[User, Depends(get_current_user)], db : Session = Depends(get_db)):
    holdings = db.query(Holdings).filter(Holdings.user_id == current_user.id).all()
    total_nav = sum([holding.nav * holding.number_of_units for holding in holdings])
    return {"loans" : float(total_nav) * 0.8}

