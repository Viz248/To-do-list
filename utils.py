#This file is for stuff like helper functions. This helps in reusability
from sqlmodel import Session, select
from models import Task

def get_all_tasks(session: Session):
    return session.exec(select(Task)).all()