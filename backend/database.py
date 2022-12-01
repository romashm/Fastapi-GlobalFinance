from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    f'sqlite:///sql/Users.db', 
    connect_args={"check_same_thread": False}
)

def get_db():
    with Session(engine) as session:
        yield session
        
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
engine_data = create_engine(
    f'sqlite:///sql/Deals.db', 
    connect_args={"check_same_thread": False}
)
    
SessionLocal_data = sessionmaker(autocommit=False, autoflush=False, bind=engine_data)

Base_data = declarative_base()
    
def get_database_ofXlsx():
    try:
        db = SessionLocal_data()
        yield db
    finally:
        db.close()
        
admins = create_engine(
    f'sqlite:///sql/Admins.db', 
    connect_args={"check_same_thread": False}
)