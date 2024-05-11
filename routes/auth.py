from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.session import get_db
from models.user import User
from core.security import verify_password, create_access_token, pwd_context

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class LoginInfo(BaseModel):
    username : str
    password : str


@router.post("/token")
async def login_for_access_token(form_data: LoginInfo, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=1440)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/signup")
async def signup(form_data: LoginInfo, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if user:
        return {"success" : False, "message": "Username already exists"}
    
    user = User(username=form_data.username, hashed_password=pwd_context.hash(form_data.password))
    db.add(user)
    db.commit()
    return {"success" : True, "message": "User created successfully"}
