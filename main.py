from fastapi import FastAPI, HTTPException

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
from typing import List, Optional #for type hints

class Task(BaseModel):
    id: int
    title: str
    done: bool=False
#so Task MUST have these 3 attributes and is_done is False by default

class TaskCreate(BaseModel):    #This is the Task the client makes, they only need to enter the string
    title: str

tasks: List[Task]=[]    #tasks is a list that must be made up of class Task i.e. all contain id, title, is_done status
nextid=1

@app.post("/tasks") #CREATE
def create_task(task:TaskCreate):
    global nextid
    newtask=Task(id=nextid,title=task.title,done=False)
    tasks.append(newtask)
    nextid+=1
    return newtask

@app.get("/tasks")  #READ
def get_tasks(done: Optional[bool]=None):   #Used to filter the done attribute in SwaggerUI. Nice
    if tasks==[]:
        raise HTTPException(status_code=404, detail="There are no tasks")
    if done is None:    #If there is NO filter given (True/False), then it is considered None and everything is shown
        return tasks    #The reason we put Optional is because None isn't actually a bool value, but rather a special value 
    filtered_tasks=[]   #List comprehension (can also use return [task for task in tasks if tasks.done==done] i don't understand ew)
    for task in tasks:
        if task.done==done:
            filtered_tasks.append(task)
    return filtered_tasks
            

@app.get("/tasks/{task_id}")    #Filtering by task id.
def get_tasks(task_id: int):
    if tasks==[]:
        raise HTTPException(status_code=404, detail="There are no tasks")
    for task in tasks:
        if task.id==task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")   #FastAPI does NOT catch logical errors in your own garbage code, only JSON errors
        #We DETECT where to spot for an HTTPException error, we stop execution, raise a proper HTTP error code, and send a JSON error response.
        #try/catch isn't really necessary here for exception handling since FastAPI does that FOR YOU already and displays it w/ JSON error codes.                                                    
        #Also we don't use else since that's only for successful stuff. Not errors lol.

@app.put("/tasks/{task_id}")    #UPDATE
def mark_done(task_id: int):
    if tasks==[]:
        raise HTTPException(status_code=404, detail="There are no tasks")
    for task in tasks:
        if task.id==task_id:
            task.done=True
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}") #DELETE
def delete_task(task_id: int):
    if tasks==[]:
        raise HTTPException(status_code=404, detail="There are no tasks")
    for i,task in enumerate(tasks): #Python equivalent to for(i=0,i<len(tasks),i++) lol
        if task.id==task_id:
            return tasks.pop(i)
    raise HTTPException(status_code=404, detail="Task not found")   