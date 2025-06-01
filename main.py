from fastapi import FastAPI
from routes import router
from database import init_db

app=FastAPI()
app.include_router(router)

init_db()   #best to put it after app starts
    