from pydantic import BaseModel #for data validation

class Task(BaseModel):
    id: int
    title: str
    done: bool=False
#so Task MUST have these 3 attributes and is_done is False by default

class TaskCreate(BaseModel):    #This is the Task the client makes, they only need to enter the string
    title: str