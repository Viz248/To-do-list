from fastapi import FastAPI
from routes.tasks import tasks_router
from routes.auth import auth_router
from database import init_db

app=FastAPI()
app.include_router(tasks_router, prefix="/tasks")   #if you have an endpoint w/ .post("login"), it'll actually be /tasks/login. 
app.include_router(auth_router, prefix="/auth")     #This avoids collision and keeps things neat in SwaggerUI

init_db()   #best to put it after app starts
    