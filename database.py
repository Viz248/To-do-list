from typing import List #for type hints
from models import Task

tasks: List[Task]=[]    #tasks is a list that must be made up of class Task i.e. all contain id, title, is_done status
nextid=1