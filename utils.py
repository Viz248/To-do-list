#This file is for stuff like helper functions. This helps in reusability
from sqlmodel import Session, select
from models import Task
from passlib.context import CryptContext    #for hashing, encoding/decoding, salting automatically. 
                                            #O/w you'd have to include the whole do them with bcrypt everywhere

def get_all_tasks(session: Session):
    return session.exec(select(Task)).all()

pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str)->str:  #->str is used to show what the function is supposed to return the data type as. It's not needed but is a
    return pwd_context.hash(password)   #good practice for readability

def verify_password(password: str, hashed_password: str)->bool: #used when logging in
    return pwd_context.verify(password, hashed_password)
