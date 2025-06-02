from fastapi import APIRouter, Depends, HTTPException
from models import Task, TaskCreate, TaskRead, UpdateTask #importing from models and database is just to avoid clutter in 1 single file, you could remove these 2 and
from typing import List, Optional   #for type hints
from sqlmodel import Session, select    #MAKE SURE YOU IMPORT SELECT FROM SQLMODEL AND [NOT] SQLALCHEMY
from database import get_session

router=APIRouter()

@router.get("/")   #The "/" stuff is after the http://127.0.0.1:8000 so it would be http://127.0.0.1:8000/ in the end
def read_root():
    return {"message":"HELLOOO!"}  #If you went there, you'd see this
                                    #It's a dictionary since python frameworks like FastAPI or Django often return data as dictionaries which 
                                    #then gets converted into JSON. This is because APIs talk in JSON.

@router.get("/hello/{name}")    #name here is gonna be dynamic, u can put anything
def greet(name: str):   #like any string
    return {"message": f"Hello {name}!"}

#Okay, this section's done


@router.post("/tasks") #CREATE
def create_task(task:TaskCreate, session: Session=Depends(get_session)):
    newtask=Task(title=task.title)
    session.add(newtask)    #stages
    session.commit()
    session.refresh(newtask)    #updates python objects with database's new data
    return newtask

@router.get("/tasks", response_model=List[TaskRead])  #READ    response_model VALIDATES what the API returns to the user
def get_tasks(done: Optional[bool]=None, session: Session=Depends(get_session)):   #Used to filter the done attribute in SwaggerUI. Nice
    all_tasks=session.exec(select(Task)).all()
    if not all_tasks:  #Checks if the table is empty
        raise HTTPException(status_code=404, detail="There are no tasks")
    if done is None:    #If there is NO filter given (True/False), then it is considered None and everything is shown
        return all_tasks    #The reason we put Optional is because None isn't actually a bool value, but rather a special value 
    filtered_tasks=session.exec(select(Task).where(Task.done==done)).all()
    return filtered_tasks
            

@router.get("/tasks/{task_id}")    #Filtering by task id.
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

@router.put("/tasks/{task_id}/done", response_model=Task)    #UPDATE Marking task as done
def mark_done(task_id: int):
    if tasks==[]:
        raise HTTPException(status_code=404, detail="There are no tasks")
    for task in tasks:
        if task.id==task_id:
            task.done=True
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@router.put("/tasks/{task_id}/title", response_model=Task)    #UPDATE Editing task
def edit_task(task_id: int, updated_task: str):
    if tasks==[]:
        raise HTTPException(status_code=404, detail="There are no tasks")
    for task in tasks:
        if task.id==task_id:
            task.title=updated_task
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@router.patch("/tasks/{task_id}", response_model=Task)    #PARTIAL UPDATE Editing task and/or status
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

@router.delete("/tasks/{task_id}") #DELETE
def delete_task(task_id: int):
    if tasks==[]:
        raise HTTPException(status_code=404, detail="There are no tasks")
    for i,task in enumerate(tasks): #Python equivalent to for(i=0,i<len(tasks),i++) lol
        if task.id==task_id:
            return tasks.pop(i)
    raise HTTPException(status_code=404, detail="Task not found")   

@router.get("/search", response_model=List[Task])  #Searching for task 
def search_tasks(keyword: str):   
    if tasks==[]:
        raise HTTPException(status_code=404, detail="There are no tasks")
    filtered_tasks=[task for task in tasks if keyword.lower() in task.title.lower()]
    if filtered_tasks!=[]:
        return filtered_tasks
    raise HTTPException(status_code=404, detail="Task not found")