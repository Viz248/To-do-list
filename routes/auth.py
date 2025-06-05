from fastapi import APIRouter, Depends, HTTPException
from models import User, UserCreate, UserRead
from sqlmodel import Session, select
from database import get_session
from security import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm  #fetches user's username and password from login submission form

auth_router=APIRouter()

@auth_router.post("/register", response_model=UserRead)  #we are using response_model here because if you don't, it'll return newuser, which is a User
def register(user:UserCreate, session: Session=Depends(get_session)):   #object, WITH the hashed_password which we DON'T want to show. We only want the 
    hashed_pw=hash_password(user.password)                              #id & username, which is why we made the UserRead class in the first place
    newuser=User(username=user.username, hashed_password=hashed_pw)         
    session.add(newuser)  
    session.commit()
    session.refresh(newuser)
    return newuser

@auth_router.post("/login")
def login(form_data: OAuth2PasswordRequestForm=Depends(), session: Session=Depends(get_session)):
    user=session.exec(select(User).where(User.username==form_data.username)).first()
    if not user or not verify_password(form_data.password,user.hashed_password):
        raise HTTPException(status_code=404, detail="Invalid credentials")
    token=create_access_token({"sub":user.username})
    return {"access_token":token, "token_type":"bearer"}