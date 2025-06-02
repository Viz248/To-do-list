from sqlmodel import SQLModel, Field #for data validation
from pydantic import BaseModel
from typing import Optional

class TaskBase(SQLModel):   #DRY (Don't Repeat Everything). We reuse these a lot so just put it in a class and just use that
    title: str
    
class Task(TaskBase, table=True):
    id: Optional[int]=Field(default=None, primary_key=True) #We put Optional since WE don't have it give it in SQLModel, the TABLE generates it for us by autoincrementing
    done: bool=False

class TaskCreate(TaskBase):
    pass

class UpdateTask(SQLModel):
    title: Optional[str]=None
    done: Optional[bool]=None

class TaskRead(SQLModel):   #We have a seperate reading class for GET since class Task has id as Optional so FastAPI might think that it might not 
    id: int                 #even exist at all which is NOT possible.
    title: str              #response_model=List[Task] is the one that is responsible for data validation and hence gives the error
    done: bool