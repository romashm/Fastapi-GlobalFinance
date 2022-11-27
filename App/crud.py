from sqlmodel import Session
import sqlite3 as lite

from . import models

def get_users(
    db: Session()
):
    return db.query(models.User).all()

def get_datas(
    db: Session
):
    return db.query(models.Deal).all()

def get_users_by_mail(
    db: Session,
    email: str
):
    return (
        db.query(models.User).filter(models.User.email == email).first()
    )
    

def getPost():
    conn = lite.connect('SQL/Data.db')
    cur = conn.cursor()
    with conn:
        cur.execute("SELECT * FROM Deal;")
        return cur.fetchall()
    
def clearData():
    conn = lite.connect('SQL/Data.db')
    cur = conn.cursor()
    with conn:
        cur.execute("DELETE FROM Deal;")
        return cur.fetchall()