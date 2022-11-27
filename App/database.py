from sqlmodel import Session, SQLModel, create_engine
from pathlib import Path
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker

import os

engine = create_engine(
    "sqlite:///SQL/Usersy.db", 
    connect_args={"check_same_thread": False}
)

engine_data = create_engine(
    "sqlite:///SQL/Data.db", 
    connect_args={"check_same_thread": False}
)

SessionLocal_data = sessionmaker(autocommit=False, autoflush=False, bind=engine_data)

Base_data = declarative_base()

def get_db():
    with Session(engine) as session:
        yield session
        
def get_db2():
    try:
        db = SessionLocal_data()
        yield db
    finally:
        db.close()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Shutdown a databese
def shutdown():
    os.remove(os.path.join(Path.cwd().resolve(), [file for file in os.listdir() if file.endswith(".db")][0]))