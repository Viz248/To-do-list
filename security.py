from passlib.context import CryptContext    #for hashing, encoding/decoding, salting automatically. 
                                            #O/w you'd have to include the whole do them with bcrypt everywhere

pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str)->str:  #->str is used to show what the function is supposed to return the data type as. It's not needed but is a
    return pwd_context.hash(password)   #good practice for readability

def verify_password(password: str, hashed_password: str)->bool: #used when logging in
    return pwd_context.verify(password, hashed_password)

from jose import JWTError, jwt  #for JWT token
from datetime import datetime, timedelta    #timedelta is for time difference i.e. for making an expiry time
import os   #Used to interact w the operating system. Allows FastAPI to load .env and treat variables as runtime config
from dotenv import load_dotenv

load_dotenv()   #looks for .env file

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

def create_access_token(data: dict):    #this data will be something like {"sub":"Jordan"}. Note that sub is a good naming convention to identify who the token is for
    to_encode=data.copy()   #keeps the original dictionary the same
    expire=date.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})   #adds a key-value pair for the expiry time to the dictionary
    encoded_jwt=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt