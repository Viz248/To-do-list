from fastapi import FastAPI, HTTPException
from models import Task, TaskCreate, UpdateTask #importing from models and database is just to avoid clutter in 1 single file, you could remove these 2 and
from database import tasks, nextid  #put everything right here to understand it better, but it would look kinda messy
from typing import List, Optional   #for type hints

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


@app.post("/tasks") #CREATE
def create_task(task:TaskCreate):
    global nextid
    newtask=Task(id=nextid,title=task.title,done=False)
    tasks.append(newtask)
    nextid+=1
    return newtask

@app.get("/tasks", response_model=List[Task])  #READ    [COME BACK TO THIS] response_model is a good practice since there might be some other stuff that the dev has to see that clients don't need to. It doesn't do anything rn but come back to it 
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

@app.put("/tasks/{task_id}/done", response_model=Task)    #UPDATE Marking task as done
def mark_done(task_id: int):
    if tasks==[]:
        raise HTTPException(status_code=404, detail="There are no tasks")
    for task in tasks:
        if task.id==task_id:
            task.done=True
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}/title", response_model=Task)    #UPDATE Editing task
def edit_task(task_id: int, updated_task: str):
    if tasks==[]:
        raise HTTPException(status_code=404, detail="There are no tasks")
    for task in tasks:
        if task.id==task_id:
            task.title=updated_task
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.patch("/tasks/{task_id}", response_model=Task)    #PARTIAL UPDATE Editing task and/or status
def partially_edit_task(task_id: int, updated_task:UpdateTask):
    if tasks==[]:
        raise HTTPException(status_code=404, detail="There are no tasks")
    for task in tasks:
        if task.id==task_id:
            if updated_task.title is not None:
                task.title=updated_task.title
            if updated_task.done is not None:
                task.done=updated_task.done
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

@app.get("/search", response_model=List[Task])  #Searching for task 
def search_tasks(keyword: str):   
    if tasks==[]:
        raise HTTPException(status_code=404, detail="There are no tasks")
    filtered_tasks=[task for task in tasks if keyword.lower() in task.title.lower()]
    if filtered_tasks!=[]:
        return filtered_tasks
    raise HTTPException(status_code=404, detail="Task not found")
    