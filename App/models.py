from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table

from .database import Base_data

class BaseUser(SQLModel):
    username: str
    lastname: str
    
    email: Optional[str] = Field(unique=True)
    password: str
    tax: int
    phone: int

    is_active: bool = False
    role: str
    
class User(BaseUser, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

#  Table moduls (✅)
class Deal(Base_data):
    __tablename__ = "Deal"
    
    id = Column(Integer, primary_key=True, index=True)

    currn = Column(String)
    currency = Column(String)
    deal = Column(String)
    calendar = Column(String)
    exchange = Column(Integer)
    result = Column(Integer)
    comment = Column(String)
    
    user = Column(String)