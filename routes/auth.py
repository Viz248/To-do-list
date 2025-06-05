from fastapi import APIRouter, Depends
from models import User, UserCreate, UserRead
from sqlmodel import Session
from database import get_session
from utils import hash_password

auth_router=APIRouter()

@auth_router.post("/register", response_model=UserRead)  #we are using response_model here because if you don't, it'll return newuser, which is a User
def register(user:UserCreate, session: Session=Depends(get_session)):   #object, WITH the hashed_password which we DON'T want to show. We only want the 
    hashed_pw=hash_password(user.password)                              #id & username, which is why we made the UserRead class in the first place
    newuser=User(username=user.username, hashed_password=hashed_pw)         
    session.add(newuser)  
    session.commit()
    session.refresh(newuser)
    return newuser