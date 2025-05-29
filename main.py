from fastapi import FastAPI

app=FastAPI()

@app.get("/")   #The "/" stuff is after the http://127.0.0.1:8000 so it would be http://127.0.0.1:8000/ in the end
def read_root():
    return {"message":"HELLOOO!"}  #If you went there, you'd see this
                                    #It's a dictionary since python frameworks like FastAPI or Django often return data as dictionaries which 
                                    #then gets converted into JSON. This is because APIs talk in JSON.

@app.get("/hello/{name}")    #name here is gonna be dynamic, u can put anything
def greet(name: str):   #like any string
    return {"message": f"Hello {name}!"}

#Okay, this section's done

from pydantic import BaseModel #for data validation
from typing import List #for type hints

class Task(BaseModel):
    id: int
    title: str
    is_done: bool=False
#so Task MUST have these 3 attributes and is_done is False by default

tasks: List[Task]=[]  #tasks is a list that must be made up of class Task i.e. all contain id, title, is_done status

@app.post("/tasks")
def create_task(task:Task):
    tasks.append(task)
    return task

@app.get("/tasks")
def get_tasks():
    return tasks

