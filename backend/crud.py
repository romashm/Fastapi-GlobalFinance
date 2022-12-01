from sqlmodel import Session
import sqlite3 as lite

from .models import User

def get_users(
    db: Session()
):
    return db.query(User).all()

def get_users_by_username(db: Session, username: str):
    return (
        db.query(User).filter(User.username == username).first()
    )
    
def get_users_by_mail(
    db: Session,
    email: str
):
    return (
        db.query(User).filter(User.email == email).first()
    )
