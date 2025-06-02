from sqlmodel import create_engine, SQLModel, Session

DATABASE_URL="sqlite:///./tasks.db" #Creates a tasks.db file using sqlite
engine=create_engine(DATABASE_URL, echo=True)   #echo here prints all SQL statements

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session   #to close session after function finishes