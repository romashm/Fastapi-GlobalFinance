from fastapi import FastAPI, HTTPException, Request, Form, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse

import sqlite3 as lite
from typing import Optional
from sqlmodel import Session


import os
from datetime import datetime, timedelta

from xlsx2html import xlsx2html
import openpyxl
import xlsxwriter


from backend.database import create_db_and_tables, get_db, get_database_ofXlsx
from backend.models import User
from backend.sendmail import send_mail
from backend.auth import get_password_hash, create_access_token, verify_token
from backend.crud import get_users, get_users_by_username, get_users_by_mail

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


def create_xlsxofDB(user):
    conn = lite.connect('sql/Deals.db')
    cur = conn.cursor()
    with conn:
        cur.execute(f'''
            CREATE TABLE Deals_{user}(
                id integer primary key,
                currn varchar(100),
                currency varchar(100),
                deal varchar(100),
                calendar varchar(100),
                exchange int,
                result int,
                comment varchar(200),
                user varchar(100)
            );
        ''')
    return cur.fetchall()

def mergedTable():
    conn = lite.connect('sql/Admins.db')
    cur = conn.cursor()
    with conn:
        cur.execute("""
            CREATE TABLE Deals(
                id integer primary key,
                currn varchar(100),
                currency varchar(100),
                deal varchar(100),
                calendar varchar(100),
                exchange int,
                result int,
                comment varchar(200),
                user varchar(100),
                place varchar(100)
            );    
        """)
    return cur.fetchall()

def catchALL_Data(user):
    conn = lite.connect('sql/Deals.db')
    cur = conn.cursor()
    with conn:
        cur.execute(f'''
            SELECT * FROM Deals_{user};
        ''')
    return cur.fetchall()

def catchAdmin_data():
    conn = lite.connect('sql/Admins.db')
    cur = conn.cursor()
    with conn:
        cur.execute(f'''
            SELECT * FROM Deals;
        ''')
    return cur.fetchall()

# CURRENT WORK OUT SECTION 
def excelExporter(
    name
):

    workbook = xlsxwriter.Workbook(f'./layout/results {datetime.today().strftime("%Y.%m.%d")} {name}.xlsx')
    worksheet = workbook.add_worksheet()
    # Field open a day with prices
    Previous_Date = datetime.today() - timedelta(days=1)
    # Determind a data of this day
    worksheet.write(0, 0, "Дата")
    worksheet.write(0, 1, Previous_Date.strftime("%Y.%m.%d"))
    worksheet.write(0, 10, "Дата")
    worksheet.write(0, 11, datetime.today().strftime("%Y.%m.%d"))

    currencyDefine = [
        "RUB", "USD", "EURO", "GPB", "CNY", "Тенге"
    ]
    TheActions = [
        "Объем", "Курс", "Цена операции", "Объем", "Курс", "Цена операции", " ", " ", " "
    ]

    count = 2
    while count <= len(currencyDefine)+1:
        worksheet.write(0, count, currencyDefine[count-2])
        
        worksheet.write(0, count+10, currencyDefine[count-2])
            
        count += 1
        
    merge_format = workbook.add_format({
        'bold': 1,
        'align': 'center',
        'valign': 'vcenter',
    })
    
    currency_format = workbook.add_format({'num_format': '#,##0.00'})
    
    _DICTFORVALUES = {
        'RUB': 0,
        'USD': 0,
        'EURO': 0,
        'GPB': 0,
        'CNY': 0
    }
    

    # wb = openpyxl.load_workbook(f'./layout/results {(datetime.today() - timedelta(days=1)).strftime("%Y.%m.%d")}.xlsx')
    # sheet = wb.active
        
    path = fr'C:\Users\roman\OneDrive\Рабочий стол\Global Finance inc\layout\results {Previous_Date.strftime("%Y.%m.%d")}.xlsx'
    # condition for new day event
    
    if os.path.exists(path):
        # _DICTFORVALUES['RUB'] =  
        # _DICTFORVALUES['USD'] = sheet['N2'].value
        # _DICTFORVALUES['EURO'] = sheet['O2'].value
        # _DICTFORVALUES['GPB'] = sheet['P2'].value
        # _DICTFORVALUES['CNY'] = sheet['Q2'].value
        print(_DICTFORVALUES)
        
        print(worksheet.write_formula(1, 12, f'=C2+B{10+len(catchALL_Data(name))}-E{10+len(catchALL_Data(name))}',currency_format))
        
        print(_DICTFORVALUES)
    else: print(False)
    
    
    
    worksheet.write(1, 2, _DICTFORVALUES['RUB'])
    worksheet.write(1, 3, _DICTFORVALUES['USD'])
    worksheet.write(1, 4, _DICTFORVALUES['EURO'])
    worksheet.write(1, 5, _DICTFORVALUES['GPB'])
    worksheet.write(1, 6, _DICTFORVALUES['CNY'])
    
    worksheet.merge_range('A2:B2','Остатки на начало дня', merge_format)
    worksheet.merge_range('K2:L2','Остатки на конец дня', merge_format)
    # RUB
    worksheet.merge_range('B7:I7', 'Рубль', merge_format)
    worksheet.merge_range('B8:D8', 'Покупка', merge_format)
    worksheet.merge_range('E8:G8', 'Продажа', merge_format)
    worksheet.merge_range('H8:H9', "Сотрудник", merge_format)
    worksheet.merge_range('I8:I9', "Коммент", merge_format)
    worksheet.merge_range('A7:A9', '№', merge_format)

    # USD
    worksheet.merge_range('K7:R7', 'Доллар', merge_format)
    worksheet.merge_range('K8:M8', 'Покупка', merge_format)
    worksheet.merge_range('N8:P8', 'Продажа', merge_format)
    worksheet.merge_range('Q8:Q9', "Сотрудник", merge_format)
    worksheet.merge_range('R8:R9', "Коммент", merge_format)

    # Euro
    worksheet.merge_range('T7:AA7', 'Евро', merge_format)
    worksheet.merge_range('T8:V8', 'Покупка', merge_format)
    worksheet.merge_range('W8:Y8', 'Продажа', merge_format)
    worksheet.merge_range('Z8:Z9', "Сотрудник", merge_format)
    worksheet.merge_range('AA8:AA9', "Коммент", merge_format)

    # Pound
    worksheet.merge_range('AC7:AJ7', 'Фунт', merge_format)
    worksheet.merge_range('AC8:AE8', 'Покупка', merge_format)
    worksheet.merge_range('AF8:AH8', 'Продажа', merge_format)
    worksheet.merge_range('AI8:AI9', "Сотрудник", merge_format)
    worksheet.merge_range('AJ8:AJ9', "Коммент", merge_format)

    # Yuan
    worksheet.merge_range('AL7:AS7', 'Юань', merge_format)
    worksheet.merge_range('AL8:AN8', 'Покупка', merge_format)
    worksheet.merge_range('AO8:AQ8', 'Продажа', merge_format)
    worksheet.merge_range('AR8:AR9', "Сотрудник", merge_format)
    worksheet.merge_range('AS8:AS9', "Коммент", merge_format)

    counts = 1
    for i in TheActions*5:
        worksheet.write(8, counts, i, merge_format)

        counts += 1

    incres = 0
    incresA = 0
    incresB = 0
    incresC = 0
    incresD = 0

    for deals in range(len(catchALL_Data(name))):
        # print(type(float(catchALL_Data(name)[deals][2])))
        if catchALL_Data(name)[deals][1] == "₽":
            productionPurchesorSell = lambda dataofexcel: ( 
            worksheet.write(9+incres, 0, incres+1),
            worksheet.write(9+incres, 1, float(catchALL_Data(name)[deals][2]),currency_format), 
            worksheet.write(9+incres, 2, float(catchALL_Data(name)[deals][5]),currency_format), 
            worksheet.write(9+incres, 3, catchALL_Data(name)[deals][6],currency_format),
            worksheet.write(9+incres, 8, catchALL_Data(name)[deals][7],currency_format),
            worksheet.write(9+incres, 7, catchALL_Data(name)[deals][8],currency_format)
            ) if (dataofexcel == "Покупка") else (
            worksheet.write(9+incres, 0, incres+1), 
            worksheet.write(9+incres, 4, float(catchALL_Data(name)[deals][2]),currency_format), 
            worksheet.write(9+incres, 5, float(catchALL_Data(name)[deals][5]),currency_format), 
            worksheet.write(9+incres, 6, catchALL_Data(name)[deals][6],currency_format),
            worksheet.write(9+incres, 8, catchALL_Data(name)[deals][7],currency_format),
            worksheet.write(9+incres, 7, catchALL_Data(name)[deals][8],currency_format)
            )
            productionPurchesorSell(catchALL_Data(name)[deals][3])
            worksheet.write(9+len(catchALL_Data(name)), 0, "Итого")
            incres += 1
            incresA += 1
            incresB += 1
            incresC += 1
            incresD += 1
            
        elif catchALL_Data(name)[deals][1] == "$":
            productionPurchesorSell = lambda dataofexcel: ( 
            worksheet.write(9+incresA, 0, incresA+1), 
            worksheet.write(9+incresA, 1+9, float(catchALL_Data(name)[deals][2]),currency_format), 
            worksheet.write(9+incresA, 2+9, float(catchALL_Data(name)[deals][5]),currency_format), 
            worksheet.write(9+incresA, 3+9, catchALL_Data(name)[deals][6],currency_format),
            worksheet.write(9+incresA, 8+9, catchALL_Data(name)[deals][7],currency_format),
            worksheet.write(9+incresA, 7+9, catchALL_Data(name)[deals][8],currency_format)
            ) if (dataofexcel == "Покупка") else (
            worksheet.write(9+incresA, 0, incresA+1), 
            worksheet.write(9+incresA, 4+9, float(catchALL_Data(name)[deals][2]),currency_format), 
            worksheet.write(9+incresA, 5+9, float(catchALL_Data(name)[deals][5]),currency_format), 
            worksheet.write(9+incresA, 6+9, catchALL_Data(name)[deals][6],currency_format),
            worksheet.write(9+incresA, 8+9, catchALL_Data(name)[deals][7],currency_format),
            worksheet.write(9+incresA, 7+9, catchALL_Data(name)[deals][8],currency_format)
            )
            productionPurchesorSell(catchALL_Data(name)[deals][3])
            worksheet.write(9+len(catchALL_Data(name)), 0, "Итого"),
            incres += 1
            incresA += 1
            incresB += 1
            incresC += 1
            incresD += 1
        elif catchALL_Data(name)[deals][1] == "€":
            productionPurchesorSell = lambda dataofexcel: ( 
            worksheet.write(9+incresB, 0, incresB+1), 
            worksheet.write(9+incresB, 1+9*2, float(catchALL_Data(name)[deals][2]),currency_format), 
            worksheet.write(9+incresB, 2+9*2, float(catchALL_Data(name)[deals][5]),currency_format), 
            worksheet.write(9+incresB, 3+9*2, catchALL_Data(name)[deals][6],currency_format),
            worksheet.write(9+incresB, 8+9*2, catchALL_Data(name)[deals][7],currency_format),
            worksheet.write(9+incresB, 7+9*2, catchALL_Data(name)[deals][8],currency_format)
            ) if (dataofexcel == "Покупка") else (
            worksheet.write(9+incresB, 0, incresB+1), 
            worksheet.write(9+incresB, 4+18, float(catchALL_Data(name)[deals][2]),currency_format), 
            worksheet.write(9+incresB, 5+18, float(catchALL_Data(name)[deals][5]),currency_format), 
            worksheet.write(9+incresB, 6+18, catchALL_Data(name)[deals][6],currency_format),
            worksheet.write(9+incresB, 8+18, catchALL_Data(name)[deals][7],currency_format),
            worksheet.write(9+incresB, 7+9*2, catchALL_Data(name)[deals][8],currency_format)
            )
            productionPurchesorSell(catchALL_Data(name)[deals][3])
            worksheet.write(9+len(catchALL_Data(name)), 0, "Итого")
            incres += 1
            incresA += 1
            incresB += 1
            incresC += 1
            incresD += 1
        elif catchALL_Data(name)[deals][1] == "¥":
            productionPurchesorSell = lambda dataofexcel: ( 
            worksheet.write(9+incresC, 0, incresC+1), 
            worksheet.write(9+incresC, 1+27, float(catchALL_Data(name)[deals][2]),currency_format), 
            worksheet.write(9+incresC, 2+27, float(catchALL_Data(name)[deals][5]),currency_format), 
            worksheet.write(9+incresC, 3+27, catchALL_Data(name)[deals][6],currency_format),
            worksheet.write(9+incresC, 8+27, catchALL_Data(name)[deals][7],currency_format),
            worksheet.write(9+incresC, 7+27, catchALL_Data(name)[deals][8],currency_format)
            ) if (dataofexcel == "Покупка") else (
            worksheet.write(9+incresC, 0, incresC+1), 
            worksheet.write(9+incresC, 4+27, float(catchALL_Data(name)[deals][2]),currency_format), 
            worksheet.write(9+incresC, 5+27, float(catchALL_Data(name)[deals][5]),currency_format), 
            worksheet.write(9+incresC, 6+27, catchALL_Data(name)[deals][6],currency_format),
            worksheet.write(9+incresC, 8+27, catchALL_Data(name)[deals][7],currency_format),
            worksheet.write(9+incresC, 7+27, catchALL_Data(name)[deals][8],currency_format)
            )
            productionPurchesorSell(catchALL_Data(name)[deals][3])
            worksheet.write(9+len(catchALL_Data(name)), 0, "Итого")
            incres += 1
            incresA += 1
            incresB += 1
            incresC += 1
            incresD += 1
        else: 
            productionPurchesorSell = lambda dataofexcel: ( 
            worksheet.write(9+incresD, 0, incresD+1), 
            worksheet.write(9+incresD, 1+36, float(catchALL_Data(name)[deals][2]),currency_format), 
            worksheet.write(9+incresD, 2+36, float(catchALL_Data(name)[deals][5]),currency_format), 
            worksheet.write(9+incresD, 3+36, catchALL_Data(name)[deals][6],currency_format),
            worksheet.write(9+incresD, 8+36, catchALL_Data(name)[deals][7],currency_format),
            worksheet.write(9+incresD, 7+36, catchALL_Data(name)[deals][8],currency_format)
            ) if (dataofexcel == "Покупка") else (
            worksheet.write(9+incresD, 0, incresD+1), 
            worksheet.write(9+incresD, 4+36, float(catchALL_Data(name)[deals][2]),currency_format), 
            worksheet.write(9+incresD, 5+36, float(catchALL_Data(name)[deals][5]),currency_format), 
            worksheet.write(9+incresD, 6+36, catchALL_Data(name)[deals][6],currency_format),
            worksheet.write(9+incresD, 8+36, catchALL_Data(name)[deals][7],currency_format),
            worksheet.write(9+incresD, 7+36, catchALL_Data(name)[deals][8],currency_format)
            )
            productionPurchesorSell(catchALL_Data(name)[deals][3])
            worksheet.write(9+len(catchALL_Data(name)), 0, "Итого")
            
            incres += 1
            incresA += 1
            incresB += 1
            incresC += 1
            incresD += 1
        

        worksheet.write_formula(9+len(catchALL_Data(name)), 1, f'=SUM(B10:B{int(len(catchALL_Data(name)))+9})', currency_format)
        
        worksheet.write_formula(9+len(catchALL_Data(name)), 3, f'=SUM(D10:D{int(len(catchALL_Data(name)))+9})',currency_format)

        worksheet.write_formula(9+len(catchALL_Data(name)), 4, f'=SUM(E10:E{int(len(catchALL_Data(name)))+9})',currency_format)
        
        worksheet.write_formula(9+len(catchALL_Data(name)), 6, f'=SUM(G10:G{int(len(catchALL_Data(name)))+9})',currency_format)
        
        
        
        worksheet.write_formula(9+len(catchALL_Data(name)), 10, f'=SUM(K10:K{int(len(catchALL_Data(name)))+9})', currency_format)
        
        worksheet.write_formula(9+len(catchALL_Data(name)), 12, f'=SUM(M10:M{int(len(catchALL_Data(name)))+9})',currency_format)

        worksheet.write_formula(9+len(catchALL_Data(name)), 13, f'=SUM(N10:N{int(len(catchALL_Data(name)))+9})',currency_format)
        
        worksheet.write_formula(9+len(catchALL_Data(name)), 15, f'=SUM(P10:P{int(len(catchALL_Data(name)))+9})',currency_format)
    
    
        worksheet.write_formula(9+len(catchALL_Data(name)), 19, f'=SUM(T10:T{int(len(catchALL_Data(name)))+9})', currency_format)
        
        worksheet.write_formula(9+len(catchALL_Data(name)), 21, f'=SUM(V10:V{int(len(catchALL_Data(name)))+9})',currency_format)

        worksheet.write_formula(9+len(catchALL_Data(name)), 22, f'=SUM(W10:W{int(len(catchALL_Data(name)))+9})',currency_format)
        
        worksheet.write_formula(9+len(catchALL_Data(name)), 24, f'=SUM(Y10:Y{int(len(catchALL_Data(name)))+9})',currency_format)
        
        
        worksheet.write_formula(9+len(catchALL_Data(name)), 28, f'=SUM(AC10:AC{int(len(catchALL_Data(name)))+9})', currency_format)
        
        worksheet.write_formula(9+len(catchALL_Data(name)), 30, f'=SUM(AE10:AE{int(len(catchALL_Data(name)))+9})',currency_format)

        worksheet.write_formula(9+len(catchALL_Data(name)), 31, f'=SUM(AF10:AF{int(len(catchALL_Data(name)))+9})',currency_format)
        
        worksheet.write_formula(9+len(catchALL_Data(name)), 33, f'=SUM(AH10:AH{int(len(catchALL_Data(name)))+9})',currency_format)
        

        worksheet.write_formula(9+len(catchALL_Data(name)), 37, f'=SUM(AL10:AL{int(len(catchALL_Data(name)))+9})', currency_format)
        
        worksheet.write_formula(9+len(catchALL_Data(name)), 39, f'=SUM(AN10:AN{int(len(catchALL_Data(name)))+9})',currency_format)

        worksheet.write_formula(9+len(catchALL_Data(name)), 40, f'=SUM(AO10:AO{int(len(catchALL_Data(name)))+9})',currency_format)
        
        worksheet.write_formula(9+len(catchALL_Data(name)), 42, f'=SUM(AQ10:AQ{int(len(catchALL_Data(name)))+9})',currency_format)
        
        worksheet.write_formula(1, 12, f'=C2+B{10+len(catchALL_Data(name))}-E{10+len(catchALL_Data(name))}',currency_format)
        
        worksheet.write_formula(1, 13, f'=D2+K{10+len(catchALL_Data(name))}-N{10+len(catchALL_Data(name))}',currency_format)
        
        worksheet.write_formula(1, 14, f'=E2+T{10+len(catchALL_Data(name))}-W{10+len(catchALL_Data(name))}',currency_format)
        
        worksheet.write_formula(1, 15, f'=F2+AC{10+len(catchALL_Data(name))}-AF{10+len(catchALL_Data(name))}',currency_format)
        
        worksheet.write_formula(1, 16, f'=G2+AL{10+len(catchALL_Data(name))}-AO{10+len(catchALL_Data(name))}',currency_format)
        
    workbook.close()
    
def existence(user):
    conn = lite.connect('sql/Deals.db')
    cur = conn.cursor()
    with conn:
        cur.execute(f'''
            select 
            case when exists 
                (select 1 from sqlite_master WHERE type='table' and name='Deals_{user}') 
                then 1 
                else 0         
            end
        ''')
    return cur.fetchall()

def existenceAdmin():
    conn = lite.connect('sql/Admins.db')
    cur = conn.cursor()
    with conn:
        cur.execute(f'''
            select 
            case when exists 
                (select 1 from sqlite_master WHERE type='table' and name='Deals') 
                then 1 
                else 0         
            end
        ''')
    return cur.fetchall()
    
# ❗ Properly importants event for database creation
@app.on_event("startup")
def startup_event():
    create_db_and_tables()

@app.get('/')
def main(
    request: Request
):
    return templates.TemplateResponse('index.html', {'request':request, 'timestamp':datetime.now().strftime("%H:%M")})

@app.post('/')
def main(
    request: Request,
    db: Session = Depends(get_db),
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
    if password == db_user.password and db_user.email == email and db_user.username == username and db_user.is_active == True:
        if db_user.role == "Администратор":
            if not (existence(username) == [(1,)]):
                create_xlsxofDB(username)
            if not (existenceAdmin() == [(1,)]):
                mergedTable()

        

            context = {'request':request, 'timestamp':datetime.now().strftime("%H:%M"),'dateandtime': datetime.now().strftime("%Y/%m/%d"), 'user': username}
            return templates.TemplateResponse('Temporary.html', context)
        elif db_user.role == "Директор":
            return "no direction"
        else: pass
    
    raise HTTPException(
            status_code=401, detail="Вход не верный"
        )

# Create an user account 👤
@app.post("/Registration")
def registrationUser(
    request: Request,
    db: Session = Depends(get_db),
    
    username: str = Form(),
    lastname: str = Form(),

    email: str = Form(),
    password: str = Form(),
    tax: int = Form(),
    phone: int = Form(),
    
    Role: str = Form(),
    Place: str = Form(),
):

    db_user = User(
        username = username,
        lastname = lastname,
        
        email = email,
        password = password,
        tax = tax,
        phone = phone,

        role = Role,
        place = Place,
        
        hashed_password = get_password_hash(password)
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    token = create_access_token(db_user)
    send_mail(to=db_user.email, token=token, username=db_user.username)
    
    return templates.TemplateResponse('Send-request.html', {'request':request, 'timestamp':datetime.now().strftime("%H:%M")})

@app.get('/Registration')
def registrationUser(
    request: Request
):
    return templates.TemplateResponse('Sign-up.html', {'request':request, 'timestamp':datetime.now().strftime("%H:%M")})

@app.get("/verify/{token}", response_class=HTMLResponse)
def login_user(
    request: Request,
    token: str, 
    db: Session = Depends(get_db)
):
    payload = verify_token(token)
    username = payload.get("sub")
    db_user = get_users_by_username(db, username)

    db_user.is_active = True
    db.commit()
    
    return templates.TemplateResponse('Accepted.html', {'request':request, 'timestamp':datetime.now().strftime("%H:%M")})

# 📂 Get all user information, admin side
@app.get("/users")
def get_all_users(
    db: Session = Depends(get_db)
):
    return get_users(db=db)

@app.get('/{user}/Home')
def home(
    request: Request,
    user: str,
    
    db: Session = Depends(get_database_ofXlsx),
):
    
    context = {'request':request, 'timestamp':datetime.now().strftime("%H:%M"),'dateandtime': datetime.now().strftime("%Y/%m/%d"), 'deal': len(catchALL_Data(user)), 'n' : catchALL_Data(user)[::-1], 'user': user}
    return templates.TemplateResponse('Home.html', context)

@app.post('/{user}/Home')
def home(
    request: Request,
    user: str,
    
    db: Session = Depends(get_database_ofXlsx),
    currn: str = Form(),
    currency: str = Form(),
    currencyVAL: str = Form(),
    valval: str = Form(),
    deal: str = Form(),
    exchange: str = Form(),
    result: float = Form(),
    comment: Optional[str] = Form('')
):  
    conn = lite.connect('sql/Deals.db')
    cur = conn.cursor()
    with conn:
        cur.execute(f'''
            INSERT INTO Deals_{user} (currn, currency, deal, calendar, exchange, result, comment, user) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        ''',(currn, float(currency+'.'+currencyVAL), deal, datetime.now().strftime("%Y.%m.%d"), float(exchange+'.'+valval), result, comment, user))
        
    conn = lite.connect('sql/Admins.db')
    cur = conn.cursor()
    with conn:
        cur.execute(f'''
            INSERT INTO Deals (currn, currency, deal, calendar, exchange, result, comment, user) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        ''',(currn, float(currency+'.'+currencyVAL), deal, datetime.now().strftime("%Y.%m.%d"), float(exchange+'.'+valval), result, comment, user))

    context = {'request':request, 'timestamp':datetime.now().strftime("%H:%M"),'dateandtime': datetime.now().strftime("%Y/%m/%d"), 'deal': len(catchALL_Data(user)), 'n' : catchALL_Data(user)[::-1], 'user': user}
    return templates.TemplateResponse('Home.html', context)


@app.get('/{user}/Default')
def default(
    request: Request,
    
    user: str
):
    excelExporter(user)
    context = {'request':request, 'timestamp':datetime.now().strftime("%H:%M"),'dateandtime': datetime.now().strftime("%Y.%m.%d"), 'user': user}
    return templates.TemplateResponse('Default.html', context)

@app.post('/{user}/Default')
def default(
    request: Request,
    
    user: str,
    time: str = Form(),
    format: str = Form()
):

    path = r'C:\Users\roman\OneDrive\Рабочий стол\Global Finance inc\layout'

    if format == "Excel":
        if os.path.exists(os.path.join(path, f'results {datetime.today().strftime("%Y.%m.%d")} {user}.xlsx')): return FileResponse(os.path.join(path, f'results {datetime.today().strftime("%Y.%m.%d")} {user}.xlsx'), media_type="xlsx", filename=f'results {datetime.today().strftime("%Y.%m.%d")} {user}.xlsx')
        return {"error" : "File not found!"}
    elif format == "PDF":
        pass
        
        return {"error" : "File not found!"}
        
        
    context = {'request':request, 'timestamp':datetime.now().strftime("%H:%M"),'dateandtime': datetime.now().strftime("%Y/%m/%d"), 'user': user}
    return templates.TemplateResponse('Default.html', context)

