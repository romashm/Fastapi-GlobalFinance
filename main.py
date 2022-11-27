from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse


from datetime import datetime

import os
import itertools

# from dotenv import find_dotenv, load_dotenv

# load_dotenv(find_dotenv())

from App.database import create_db_and_tables, shutdown, get_db, get_db2
from App.models import User, Deal
from App.crud import get_users, get_users_by_mail, get_datas, getPost, clearData
from App.auth import create_password_hash, verify_password
from App.excelExporter import excelExporter, htmlExporter
# from App.sendmail import send_mail

from typing import Optional
from fastapi.responses import FileResponse



app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
def startup_event():
    create_db_and_tables()
    
@app.on_event("shutdown")
def startup_event():
    shutdown()

@app.get('/')
def main(
    request: Request
):
    return templates.TemplateResponse('index.html', {'request':request, 'timestamp':datetime.now().strftime("%H:%M")})

# Registration field ~> 1. Skin of the website (✅), 2. Register form in development (❌)
@app.get('/registration')
def registrationUser(
    request: Request
):
    return templates.TemplateResponse('registration.html', {'request':request, 'timestamp':datetime.now().strftime("%H:%M")})

# Create an user account 👤
@app.post("/registration")
def registrationUser(
    request: Request,
    db: Session = Depends(get_db),
    
    username: str = Form(),
    lastname: str = Form(),

    email: str = Form(),
    password: str = Form(),
    tax: int = Form(),
    phone: int = Form(),
    
    role: str = Form()
):
    db_user = User(
        username = username,
        lastname = lastname,
        
        email = email,
        password = password,
        tax = tax,
        phone = phone,

        role = role,
        hashed_password = create_password_hash(password)
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # send_mail(
    #     to='romashmlc@gmail.com', username=db_user.username
    # )
    
    
    return templates.TemplateResponse('emailSender.html', {'request':request, 'timestamp':datetime.now().strftime("%H:%M")})


dictoftheUser = {}

@app.post('/')
def main(
    request: Request,
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
    email: str = Form(),
    password: str = Form(),
    username: str = Form()
):
    db_user = get_users_by_mail(db=db, email=email)
    if not db_user:
        raise HTTPException(
            status_code=401, detail="Пользователя не существует"
        )
        # 🚀 HERE  
    if password == db_user.password and db_user.email == email and db_user.username == username:
        # if db_user.role == "Cashier":  return RedirectResponse(url=app.url_path_for('/Deal'))
        # elif db_user.role == "Admin": return "Work in progress"
        dictoftheUser["username"] = username
        dictoftheUser["lastname"] = db_user.lastname
        dictoftheUser["role"] = db_user.role
        
        dictoftheUser["email"] = email
 
        # return db_user
        context = {'request':request, 'timestamp':datetime.now().strftime("%H:%M"),'dateandtime': datetime.now().strftime("%Y/%m/%d")}
        return templates.TemplateResponse('Temporary.html', context)   
    raise HTTPException(
            status_code=401, detail="Вход не верный"
        )

# 📂 Get all user information, admin side
@app.get("/users")
def get_all_users(
    db: Session = Depends(get_db)
):
    return get_users(db=db)

@app.get('/ending')
def ending(
    request: Request
):
    context = {'request':request, 'timestamp':datetime.now().strftime("%H:%M"),'dateandtime': datetime.now().strftime("%Y/%m/%d")}
    return templates.TemplateResponse('end_session.html', context)

@app.post('/ending')
def ending(
    
):
    pass


@app.get('/Home')
def home(
    request: Request,
    db: Session = Depends(get_db2),
):
    
    print(dictoftheUser["username"])
    context = {'request':request, 'timestamp':datetime.now().strftime("%H:%M"),'dateandtime': datetime.now().strftime("%Y/%m/%d"), 'deal': len(get_datas(db=db)), 'i': [i for i in itertools.chain(*getPost())], 'n' : getPost()[::-1]}
    return templates.TemplateResponse('Home.html', context)   

@app.post("/Home")
def home(
    request: Request,
    db: Session = Depends(get_db2),
    currn: str = Form(),
    currency: str = Form(),
    currencyVAL: str = Form(),
    valval: str = Form(),
    deal: str = Form(),
    exchange: str = Form(),
    result: float = Form(),
    comment: Optional[str] = Form('')
):  
    
    db_deal = Deal(
        currn = currn,
        currency = str(currency+'.'+currencyVAL),
        deal = deal,
        calendar = datetime.now().strftime("%Y/%m/%d"),
        exchange = str(exchange+'.'+valval),
        result = result,

        comment = comment,
        
        user = dictoftheUser["username"]
    )
    
    db.add(db_deal)
    db.commit()
    
    context = {'request':request, 'timestamp':datetime.now().strftime("%H:%M"),'dateandtime': datetime.now().strftime("%Y/%m/%d"), 'deal': len(get_datas(db=db)), 'i': [i for i in itertools.chain(*getPost())], 'n' : getPost()[::-1]}
    return templates.TemplateResponse('Home.html', context)

@app.post('/Disactivate')
def Disactivate(
    request: Request
):
    excelExporter()
    clearData()
    
    return "😎"

@app.get('/Default')
def default(
    request: Request
):
    
    # 🛠️ Building ... 
    
    excelExporter()
    
    # 🛠️ Building ... 
    
    
    context = {'request':request, 'timestamp':datetime.now().strftime("%H:%M"),'dateandtime': datetime.now().strftime("%Y/%m/%d")}
    return templates.TemplateResponse('Default.html', context)

@app.post('/Default')
def default(
    request: Request,
    time: str = Form(),
    format: str = Form()
):

    # 🛠️ Building ... 
    
    # 🛠️ Building ... 

    path = r'C:\Users\roman\OneDrive\Рабочий стол\Application\export'

    if format == "Excel":
        if os.path.exists(os.path.join(path, "results.xlsx")): return FileResponse(os.path.join(path, "results.xlsx"), media_type="xlsx", filename=f"result-{time}.xlsx")
        return {"error" : "File not found!"}
    elif format == "PDF":
        pass
        
        return {"error" : "File not found!"}
        
        
    context = {'request':request, 'timestamp':datetime.now().strftime("%H:%M"),'dateandtime': datetime.now().strftime("%Y/%m/%d")}
    return templates.TemplateResponse('Default.html', context)

@app.get('/bla')
def bla (
    
):
    pass