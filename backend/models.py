from typing import Optional
from sqlmodel import SQLModel, Field 


class BaseUser(SQLModel):
    username: str
    lastname: str
    
    email: Optional[str] = Field(unique=True)
    password: str
    tax: int
    phone: Optional[int] = Field(unique=True)

    is_active: bool = False
    role: str
    place: str
    shortname: str
    
class User(BaseUser, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    