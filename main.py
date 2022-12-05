from fastapi import FastAPI, HTTPException, Request, Form, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse

import sqlite3 as lite
from typing import Optional
from sqlmodel import Session
from pathlib import Path


import os
import itertools
import nltk
from datetime import datetime, timedelta

import xlsxwriter

from backend.database import create_db_and_tables, get_db
from backend.models import User
from backend.sendmail import send_mail
from backend.auth import get_password_hash, create_access_token, verify_token
from backend.crud import get_users, get_users_by_username, get_users_by_mail
from backend.currencyforTulskaya import usd, rub, eur, gpb, cny, sqlite_for_adm, existence_Tulskaya, insertsqlite_for_adm, updatetables, tulskaya
from backend.currencyforOskar import usd_osk, rub_osk, eur_osk, gpb_osk, cny_osk, sqlite_for_adm_osk, existence_Osk, insertsqlite_for_adm_osk, updatetables_osk, oskar
from backend.currencyforKesher import usd_kesher, rub_kesher, eur_kesher, gpb_kesher, cny_kesher, sqlite_for_adm_kesher, existence_kesher, insertsqlite_for_adm_kesher, updatetables_kesher, kesher


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.absolute() / "static"),
    name="static",
)

@app.get('/')
def main(
    request: Request
):
    return templates.TemplateResponse('index.html', {'request':request, 'timestamp':datetime.now().strftime("%H:%M")})

@app.get('/signup')
def signup(
    request: Request
):
    return templates.TemplateResponse('Sign-up.html', {'request':request, 'timestamp':datetime.now().strftime("%H:%M")})

@app.get('/{user}/Home')
def home(
    request: Request,
    user: str
):

    if not (existence_Tulskaya() == [(1,)]):
        sqlite_for_adm()
    try:
        insertsqlite_for_adm()
    except:
        updatetables(datetime.now().strftime("%Y-%m-%d"), rub(), usd(), eur(), gpb(), cny())
        
    if not (existence_Osk() == [(1,)]):
        sqlite_for_adm_osk()
    try:
        insertsqlite_for_adm_osk()
    except:
        updatetables_osk(datetime.now().strftime("%Y-%m-%d"), rub_osk(), usd_osk(), eur_osk(), gpb_osk(), cny_osk())
        
    if not (existence_kesher() == [(1,)]):
        sqlite_for_adm_kesher()
    try:
        insertsqlite_for_adm_kesher()
    except:
        updatetables_kesher(datetime.now().strftime("%Y-%m-%d"), rub_kesher(), usd_kesher(), eur_kesher(), gpb_kesher(), cny_kesher())
    
    
    context = {'request':request, 'timestamp':datetime.now().strftime("%H:%M"),'dateandtime': datetime.now().strftime("%Y-%m-%d"), 'deal': len(catchALL_Data(user)), 'n' : catchALL_Data(user)[::-1], 'user': user}
    return templates.TemplateResponse('Home.html', context)

@app.get('/{user}/Default')
def default(
    request: Request,
    user: str
):

    context = {'request':request, 'timestamp':datetime.now().strftime("%H:%M"),'dateandtime': datetime.now().strftime("%Y-%m-%d"), 'user': user}
    return templates.TemplateResponse('Default.html', context)

@app.get('/{user}/Director')
def director(
    request: Request,
    user: str
):  
    excelExporter_forADM(user)
    context = {'request':request, 'timestamp':datetime.now().strftime("%H:%M"),'dateandtime': datetime.now().strftime("%Y-%m-%d"), 'deal': len(catchAdmin_data()), 'n' : catchAdmin_data()[::-1], 'user': user}
    return templates.TemplateResponse('Director.html', context)

@app.get('/{user}/Choosen')
def Choosen(
    request: Request,
    user: str  
):
    context = {'request':request, 'timestamp':datetime.now().strftime("%H:%M"),'dateandtime': datetime.now().strftime("%d.%m.%Y"), 'user': user}
    return templates.TemplateResponse('Choosen.html', context)

@app.get('/{user}/Analise')
def Analise(
    request: Request,
    user: str  
):
    print(currency_osk())
    
    context = {'request':request, 'timestamp':datetime.now().strftime("%H:%M"),'dateandtime': datetime.now().strftime("%d.%m.%Y"), 'user': user}
    return templates.TemplateResponse('Analise.html', context)

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

# ❗ Properly importants event for database creation
@app.on_event("startup")
def startup_event():
    create_db_and_tables()
    
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
                user varchar(100),
                place varchar(100)
            );
        ''')
    return cur.fetchall()

def currency_osk():
    conn = lite.connect('sql/Currency.db')
    cur = conn.cursor()
    with conn:
        cur.execute(f'''
            select rub, usd, eur, gpb, cny from Currency_Osk;
        ''')
    return cur.fetchall()[0]

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

def catchAdmin_data_kesher():
    conn = lite.connect('sql/Admins.db')
    cur = conn.cursor()
    with conn:
        cur.execute(f'''
            SELECT * FROM Deals where place = "Кешер";
        ''')
    return cur.fetchall()

def catchAdmin_data_oskar():
    conn = lite.connect('sql/Admins.db')
    cur = conn.cursor()
    with conn:
        cur.execute(f'''
            SELECT * FROM Deals where place = "Оскар";
        ''')
    return cur.fetchall()

def catchAdmin_data_tulskaya():
    conn = lite.connect('sql/Admins.db')
    cur = conn.cursor()
    with conn:
        cur.execute(f'''
            SELECT * FROM Deals where place = "Тульская";
        ''')
    return cur.fetchall()


def excelExporter_forADM(
    name
):

    workbook = xlsxwriter.Workbook(f'./layout/admins {datetime.today().strftime("%Y-%m-%d")} {name}.xlsx')
    worksheet = workbook.add_worksheet("Кешер")
    worksheet_oskar = workbook.add_worksheet("Оскар")
    worksheet_tulskaya = workbook.add_worksheet("Тульская")
    
    # Field open a day with prices
    Previous_Date = datetime.today() - timedelta(days=1)
    # Determind a data of this day
    worksheet.write(0, 0, "Дата")
    worksheet.write(0, 1, Previous_Date.strftime("%Y-%m-%d"))
    worksheet.write(0, 10, "Дата")
    worksheet.write(0, 11, datetime.today().strftime("%Y-%m-%d"))

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
    
    try:
        worksheet.write(1, 2, kesher((datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"), 'rub')[0][0])
        worksheet.write(1, 3, kesher((datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"), 'usd')[0][0])
        worksheet.write(1, 4, kesher((datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"), 'eur')[0][0])
        worksheet.write(1, 5, kesher((datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"), 'gpb')[0][0])
        worksheet.write(1, 6, kesher((datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"), 'cny')[0][0])
        worksheet.write(1, 12, f'{rub_kesher()}',currency_format)
    
        worksheet.write(1, 13, f'{usd_kesher()}',currency_format)
        
        worksheet.write(1, 14, f'{eur_kesher()}',currency_format)
        
        worksheet.write(1, 15, f'{gpb_kesher()}',currency_format)
        
        worksheet.write(1, 16, f'{cny_kesher()}',currency_format)
    except:
        worksheet.write(1, 2, 0)
        worksheet.write(1, 3, 0)
        worksheet.write(1, 4, 0)
        worksheet.write(1, 5, 0)
        worksheet.write(1, 6, 0)
        worksheet.write(1, 12, f'{rub_kesher()}',currency_format)
    
        worksheet.write(1, 13, f'{usd_kesher()}',currency_format)
        
        worksheet.write(1, 14, f'{eur_kesher()}',currency_format)
        
        worksheet.write(1, 15, f'{gpb_kesher()}',currency_format)
        
        worksheet.write(1, 16, f'{cny_kesher()}',currency_format)
    
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

    incres1 = 0
    incresA1 = 0
    incresB1 = 0
    incresC1 = 0
    incresD1 = 0

    for deals in range(len(catchAdmin_data_kesher())):
        # print(type(float(catchAdmin_data_kesher()[deals][2])))
        if catchAdmin_data_kesher()[deals][1] == "₽":
            productionPurchesorSell = lambda dataofexcel: ( 
            worksheet.write(9+incres1, 0, incres1+1),
            worksheet.write(9+incres1, 1, float(catchAdmin_data_kesher()[deals][2]),currency_format), 
            worksheet.write(9+incres1, 2, float(catchAdmin_data_kesher()[deals][5]),currency_format), 
            worksheet.write(9+incres1, 3, catchAdmin_data_kesher()[deals][6],currency_format),
            worksheet.write(9+incres1, 8, catchAdmin_data_kesher()[deals][7],currency_format),
            worksheet.write(9+incres1, 7, catchAdmin_data_kesher()[deals][8],currency_format),
            
            ) if (dataofexcel == "Покупка") else (
            worksheet.write(9+incres1, 0, incres1+1), 
            worksheet.write(9+incres1, 4, float(catchAdmin_data_kesher()[deals][2]),currency_format), 
            worksheet.write(9+incres1, 5, float(catchAdmin_data_kesher()[deals][5]),currency_format), 
            worksheet.write(9+incres1, 6, catchAdmin_data_kesher()[deals][6],currency_format),
            worksheet.write(9+incres1, 8, catchAdmin_data_kesher()[deals][7],currency_format),
            worksheet.write(9+incres1, 7, catchAdmin_data_kesher()[deals][8],currency_format)
            )
            productionPurchesorSell(catchAdmin_data_kesher()[deals][3])
            worksheet.write(9+len(catchAdmin_data_kesher()), 0, "Итого")
            incres1 += 1
            incresA1 += 1
            incresB1 += 1
            incresC1 += 1
            incresD1 += 1
            
        elif catchAdmin_data_kesher()[deals][1] == "$":
            productionPurchesorSell = lambda dataofexcel: ( 
            worksheet.write(9+incresA1, 0, incresA1+1), 
            worksheet.write(9+incresA1, 1+9, float(catchAdmin_data_kesher()[deals][2]),currency_format), 
            worksheet.write(9+incresA1, 2+9, float(catchAdmin_data_kesher()[deals][5]),currency_format), 
            worksheet.write(9+incresA1, 3+9, catchAdmin_data_kesher()[deals][6],currency_format),
            worksheet.write(9+incresA1, 8+9, catchAdmin_data_kesher()[deals][7],currency_format),
            worksheet.write(9+incresA1, 7+9, catchAdmin_data_kesher()[deals][8],currency_format)
            ) if (dataofexcel == "Покупка") else (
            worksheet.write(9+incresA1, 0, incresA1+1), 
            worksheet.write(9+incresA1, 4+9, float(catchAdmin_data_kesher()[deals][2]),currency_format), 
            worksheet.write(9+incresA1, 5+9, float(catchAdmin_data_kesher()[deals][5]),currency_format), 
            worksheet.write(9+incresA1, 6+9, catchAdmin_data_kesher()[deals][6],currency_format),
            worksheet.write(9+incresA1, 8+9, catchAdmin_data_kesher()[deals][7],currency_format),
            worksheet.write(9+incresA1, 7+9, catchAdmin_data_kesher()[deals][8],currency_format)
            )
            productionPurchesorSell(catchAdmin_data_kesher()[deals][3])
            worksheet.write(9+len(catchAdmin_data_kesher()), 0, "Итого"),
            incres1 += 1
            incresA1 += 1
            incresB1 += 1
            incresC1 += 1
            incresD1 += 1
        elif catchAdmin_data_kesher()[deals][1] == "€":
            productionPurchesorSell = lambda dataofexcel: ( 
            worksheet.write(9+incresB1, 0, incresB1+1), 
            worksheet.write(9+incresB1, 1+9*2, float(catchAdmin_data_kesher()[deals][2]),currency_format), 
            worksheet.write(9+incresB1, 2+9*2, float(catchAdmin_data_kesher()[deals][5]),currency_format), 
            worksheet.write(9+incresB1, 3+9*2, catchAdmin_data_kesher()[deals][6],currency_format),
            worksheet.write(9+incresB1, 8+9*2, catchAdmin_data_kesher()[deals][7],currency_format),
            worksheet.write(9+incresB1, 7+9*2, catchAdmin_data_kesher()[deals][8],currency_format)
            ) if (dataofexcel == "Покупка") else (
            worksheet.write(9+incresB1, 0, incresB1+1), 
            worksheet.write(9+incresB1, 4+18, float(catchAdmin_data_kesher()[deals][2]),currency_format), 
            worksheet.write(9+incresB1, 5+18, float(catchAdmin_data_kesher()[deals][5]),currency_format), 
            worksheet.write(9+incresB1, 6+18, catchAdmin_data_kesher()[deals][6],currency_format),
            worksheet.write(9+incresB1, 8+18, catchAdmin_data_kesher()[deals][7],currency_format),
            worksheet.write(9+incresB1, 7+9*2, catchAdmin_data_kesher()[deals][8],currency_format)
            )
            productionPurchesorSell(catchAdmin_data_kesher()[deals][3])
            worksheet.write(9+len(catchAdmin_data_kesher()), 0, "Итого")
            incres1 += 1
            incresA1 += 1
            incresB1 += 1
            incresC1 += 1
            incresD1 += 1
        elif catchAdmin_data_kesher()[deals][1] == "¥":
            productionPurchesorSell = lambda dataofexcel: ( 
            worksheet.write(9+incresC1, 0, incresC1+1), 
            worksheet.write(9+incresC1, 1+27, float(catchAdmin_data_kesher()[deals][2]),currency_format), 
            worksheet.write(9+incresC1, 2+27, float(catchAdmin_data_kesher()[deals][5]),currency_format), 
            worksheet.write(9+incresC1, 3+27, catchAdmin_data_kesher()[deals][6],currency_format),
            worksheet.write(9+incresC1, 8+27, catchAdmin_data_kesher()[deals][7],currency_format),
            worksheet.write(9+incresC1, 7+27, catchAdmin_data_kesher()[deals][8],currency_format)
            ) if (dataofexcel == "Покупка") else (
            worksheet.write(9+incresC1, 0, incresC1+1), 
            worksheet.write(9+incresC1, 4+27, float(catchAdmin_data_kesher()[deals][2]),currency_format), 
            worksheet.write(9+incresC1, 5+27, float(catchAdmin_data_kesher()[deals][5]),currency_format), 
            worksheet.write(9+incresC1, 6+27, catchAdmin_data_kesher()[deals][6],currency_format),
            worksheet.write(9+incresC1, 8+27, catchAdmin_data_kesher()[deals][7],currency_format),
            worksheet.write(9+incresC1, 7+27, catchAdmin_data_kesher()[deals][8],currency_format)
            )
            productionPurchesorSell(catchAdmin_data_kesher()[deals][3])
            worksheet.write(9+len(catchAdmin_data_kesher()), 0, "Итого")
            incres1 += 1
            incresA1 += 1
            incresB1 += 1
            incresC1 += 1
            incresD1 += 1
        else: 
            productionPurchesorSell = lambda dataofexcel: ( 
            worksheet.write(9+incresD1, 0, incresD1+1), 
            worksheet.write(9+incresD1, 1+36, float(catchAdmin_data_kesher()[deals][2]),currency_format), 
            worksheet.write(9+incresD1, 2+36, float(catchAdmin_data_kesher()[deals][5]),currency_format), 
            worksheet.write(9+incresD1, 3+36, catchAdmin_data_kesher()[deals][6],currency_format),
            worksheet.write(9+incresD1, 8+36, catchAdmin_data_kesher()[deals][7],currency_format),
            worksheet.write(9+incresD1, 7+36, catchAdmin_data_kesher()[deals][8],currency_format)
            ) if (dataofexcel == "Покупка") else (
            worksheet.write(9+incresD1, 0, incresD1+1), 
            worksheet.write(9+incresD1, 4+36, float(catchAdmin_data_kesher()[deals][2]),currency_format), 
            worksheet.write(9+incresD1, 5+36, float(catchAdmin_data_kesher()[deals][5]),currency_format), 
            worksheet.write(9+incresD1, 6+36, catchAdmin_data_kesher()[deals][6],currency_format),
            worksheet.write(9+incresD1, 8+36, catchAdmin_data_kesher()[deals][7],currency_format),
            worksheet.write(9+incresD1, 7+36, catchAdmin_data_kesher()[deals][8],currency_format)
            )
            productionPurchesorSell(catchAdmin_data_kesher()[deals][3])
            worksheet.write(9+len(catchAdmin_data_kesher()), 0, "Итого")
            
            incres1 += 1
            incresA1 += 1
            incresB1 += 1
            incresC1 += 1
            incresD1 += 1
        

        worksheet.write_formula(9+len(catchAdmin_data_kesher()), 1, f'=SUM(B10:B{int(len(catchAdmin_data_kesher()))+9})', currency_format)
        
        worksheet.write_formula(9+len(catchAdmin_data_kesher()), 3, f'=SUM(D10:D{int(len(catchAdmin_data_kesher()))+9})',currency_format)

        worksheet.write_formula(9+len(catchAdmin_data_kesher()), 4, f'=SUM(E10:E{int(len(catchAdmin_data_kesher()))+9})',currency_format)
        
        worksheet.write_formula(9+len(catchAdmin_data_kesher()), 6, f'=SUM(G10:G{int(len(catchAdmin_data_kesher()))+9})',currency_format)
        
        
        
        worksheet.write_formula(9+len(catchAdmin_data_kesher()), 10, f'=SUM(K10:K{int(len(catchAdmin_data_kesher()))+9})', currency_format)
        
        worksheet.write_formula(9+len(catchAdmin_data_kesher()), 12, f'=SUM(M10:M{int(len(catchAdmin_data_kesher()))+9})',currency_format)

        worksheet.write_formula(9+len(catchAdmin_data_kesher()), 13, f'=SUM(N10:N{int(len(catchAdmin_data_kesher()))+9})',currency_format)
        
        worksheet.write_formula(9+len(catchAdmin_data_kesher()), 15, f'=SUM(P10:P{int(len(catchAdmin_data_kesher()))+9})',currency_format)
    
    
        worksheet.write_formula(9+len(catchAdmin_data_kesher()), 19, f'=SUM(T10:T{int(len(catchAdmin_data_kesher()))+9})', currency_format)
        
        worksheet.write_formula(9+len(catchAdmin_data_kesher()), 21, f'=SUM(V10:V{int(len(catchAdmin_data_kesher()))+9})',currency_format)

        worksheet.write_formula(9+len(catchAdmin_data_kesher()), 22, f'=SUM(W10:W{int(len(catchAdmin_data_kesher()))+9})',currency_format)
        
        worksheet.write_formula(9+len(catchAdmin_data_kesher()), 24, f'=SUM(Y10:Y{int(len(catchAdmin_data_kesher()))+9})',currency_format)
        
        
        worksheet.write_formula(9+len(catchAdmin_data_kesher()), 28, f'=SUM(AC10:AC{int(len(catchAdmin_data_kesher()))+9})', currency_format)
        
        worksheet.write_formula(9+len(catchAdmin_data_kesher()), 30, f'=SUM(AE10:AE{int(len(catchAdmin_data_kesher()))+9})',currency_format)

        worksheet.write_formula(9+len(catchAdmin_data_kesher()), 31, f'=SUM(AF10:AF{int(len(catchAdmin_data_kesher()))+9})',currency_format)
        
        worksheet.write_formula(9+len(catchAdmin_data_kesher()), 33, f'=SUM(AH10:AH{int(len(catchAdmin_data_kesher()))+9})',currency_format)
        

        worksheet.write_formula(9+len(catchAdmin_data_kesher()), 37, f'=SUM(AL10:AL{int(len(catchAdmin_data_kesher()))+9})', currency_format)
        
        worksheet.write_formula(9+len(catchAdmin_data_kesher()), 39, f'=SUM(AN10:AN{int(len(catchAdmin_data_kesher()))+9})',currency_format)

        worksheet.write_formula(9+len(catchAdmin_data_kesher()), 40, f'=SUM(AO10:AO{int(len(catchAdmin_data_kesher()))+9})',currency_format)
        
        worksheet.write_formula(9+len(catchAdmin_data_kesher()), 42, f'=SUM(AQ10:AQ{int(len(catchAdmin_data_kesher()))+9})',currency_format)        
        
    # Determind a data of this day
    worksheet_oskar.write(0, 0, "Дата")
    worksheet_oskar.write(0, 1, Previous_Date.strftime("%Y-%m-%d"))
    worksheet_oskar.write(0, 10, "Дата")
    worksheet_oskar.write(0, 11, datetime.today().strftime("%Y-%m-%d"))

    currencyDefine = [
        "RUB", "USD", "EURO", "GPB", "CNY", "Тенге"
    ]
    TheActions = [
        "Объем", "Курс", "Цена операции", "Объем", "Курс", "Цена операции", " ", " ", " "
    ]

    count = 2
    while count <= len(currencyDefine)+1:
        worksheet_oskar.write(0, count, currencyDefine[count-2])
        
        worksheet_oskar.write(0, count+10, currencyDefine[count-2])
            
        count += 1
        
    merge_format = workbook.add_format({
        'bold': 1,
        'align': 'center',
        'valign': 'vcenter',
    })
    
    currency_format = workbook.add_format({'num_format': '#,##0.00'})

    try:
        worksheet_oskar.write(1, 2, oskar((datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"), 'rub')[0][0])
        worksheet_oskar.write(1, 3, oskar((datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"), 'usd')[0][0])
        worksheet_oskar.write(1, 4, oskar((datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"), 'eur')[0][0])
        worksheet_oskar.write(1, 5, oskar((datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"), 'gpb')[0][0])
        worksheet_oskar.write(1, 6, oskar((datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"), 'cny')[0][0])
        worksheet_oskar.write(1, 12, f'{rub_osk()}',currency_format)
    
        worksheet_oskar.write(1, 13, f'{usd_osk()}',currency_format)
        
        worksheet_oskar.write(1, 14, f'{eur_osk()}',currency_format)
        
        worksheet_oskar.write(1, 15, f'{gpb_osk()}',currency_format)
        
        worksheet_oskar.write(1, 16, f'{cny_osk()}',currency_format)
    except:
        worksheet_oskar.write(1, 2, 0)
        worksheet_oskar.write(1, 3, 0)
        worksheet_oskar.write(1, 4, 0)
        worksheet_oskar.write(1, 5, 0)
        worksheet_oskar.write(1, 6, 0)
        worksheet_oskar.write(1, 12, f'{rub_osk()}',currency_format)
    
        worksheet_oskar.write(1, 13, f'{usd_osk()}',currency_format)
        
        worksheet_oskar.write(1, 14, f'{eur_osk()}',currency_format)
        
        worksheet_oskar.write(1, 15, f'{gpb_osk()}',currency_format)
        
        worksheet_oskar.write(1, 16, f'{cny_osk()}',currency_format)
    
    worksheet_oskar.merge_range('A2:B2','Остатки на начало дня', merge_format)
    worksheet_oskar.merge_range('K2:L2','Остатки на конец дня', merge_format)
    # RUB
    worksheet_oskar.merge_range('B7:I7', 'Рубль', merge_format)
    worksheet_oskar.merge_range('B8:D8', 'Покупка', merge_format)
    worksheet_oskar.merge_range('E8:G8', 'Продажа', merge_format)
    worksheet_oskar.merge_range('H8:H9', "Сотрудник", merge_format)
    worksheet_oskar.merge_range('I8:I9', "Коммент", merge_format)
    worksheet_oskar.merge_range('A7:A9', '№', merge_format)

    # USD
    worksheet_oskar.merge_range('K7:R7', 'Доллар', merge_format)
    worksheet_oskar.merge_range('K8:M8', 'Покупка', merge_format)
    worksheet_oskar.merge_range('N8:P8', 'Продажа', merge_format)
    worksheet_oskar.merge_range('Q8:Q9', "Сотрудник", merge_format)
    worksheet_oskar.merge_range('R8:R9', "Коммент", merge_format)

    # Euro
    worksheet_oskar.merge_range('T7:AA7', 'Евро', merge_format)
    worksheet_oskar.merge_range('T8:V8', 'Покупка', merge_format)
    worksheet_oskar.merge_range('W8:Y8', 'Продажа', merge_format)
    worksheet_oskar.merge_range('Z8:Z9', "Сотрудник", merge_format)
    worksheet_oskar.merge_range('AA8:AA9', "Коммент", merge_format)

    # Pound
    worksheet_oskar.merge_range('AC7:AJ7', 'Фунт', merge_format)
    worksheet_oskar.merge_range('AC8:AE8', 'Покупка', merge_format)
    worksheet_oskar.merge_range('AF8:AH8', 'Продажа', merge_format)
    worksheet_oskar.merge_range('AI8:AI9', "Сотрудник", merge_format)
    worksheet_oskar.merge_range('AJ8:AJ9', "Коммент", merge_format)

    # Yuan
    worksheet_oskar.merge_range('AL7:AS7', 'Юань', merge_format)
    worksheet_oskar.merge_range('AL8:AN8', 'Покупка', merge_format)
    worksheet_oskar.merge_range('AO8:AQ8', 'Продажа', merge_format)
    worksheet_oskar.merge_range('AR8:AR9', "Сотрудник", merge_format)
    worksheet_oskar.merge_range('AS8:AS9', "Коммент", merge_format)

    counts = 1
    for i in TheActions*5:
        worksheet_oskar.write(8, counts, i, merge_format)

        counts += 1

    incres2 = 0
    incresA2 = 0
    incresB2 = 0
    incresC2 = 0
    incresD2 = 0

    for deals in range(len(catchAdmin_data_oskar())):
        # print(type(float(catchAdmin_data_oskar()[deals][2])))
        if catchAdmin_data_oskar()[deals][1] == "₽":
            productionPurchesorSell = lambda dataofexcel: ( 
            worksheet_oskar.write(9+incres2, 0, incres2+1),
            worksheet_oskar.write(9+incres2, 1, float(catchAdmin_data_oskar()[deals][2]),currency_format), 
            worksheet_oskar.write(9+incres2, 2, float(catchAdmin_data_oskar()[deals][5]),currency_format), 
            worksheet_oskar.write(9+incres2, 3, catchAdmin_data_oskar()[deals][6],currency_format),
            worksheet_oskar.write(9+incres2, 8, catchAdmin_data_oskar()[deals][7],currency_format),
            worksheet_oskar.write(9+incres2, 7, catchAdmin_data_oskar()[deals][8],currency_format)
            ) if (dataofexcel == "Покупка") else (
            worksheet_oskar.write(9+incres2, 0, incres2+1), 
            worksheet_oskar.write(9+incres2, 4, float(catchAdmin_data_oskar()[deals][2]),currency_format), 
            worksheet_oskar.write(9+incres2, 5, float(catchAdmin_data_oskar()[deals][5]),currency_format), 
            worksheet_oskar.write(9+incres2, 6, catchAdmin_data_oskar()[deals][6],currency_format),
            worksheet_oskar.write(9+incres2, 8, catchAdmin_data_oskar()[deals][7],currency_format),
            worksheet_oskar.write(9+incres2, 7, catchAdmin_data_oskar()[deals][8],currency_format)
            )
            productionPurchesorSell(catchAdmin_data_oskar()[deals][3])
            worksheet_oskar.write(9+len(catchAdmin_data_oskar()), 0, "Итого")
            incres2 += 1
            incresA2 += 1
            incresB2 += 1
            incresC2 += 1
            incresD2 += 1
            
        elif catchAdmin_data_oskar()[deals][1] == "$":
            productionPurchesorSell = lambda dataofexcel: ( 
            worksheet_oskar.write(9+incresA2, 0, incresA2+1), 
            worksheet_oskar.write(9+incresA2, 1+9, float(catchAdmin_data_oskar()[deals][2]),currency_format), 
            worksheet_oskar.write(9+incresA2, 2+9, float(catchAdmin_data_oskar()[deals][5]),currency_format), 
            worksheet_oskar.write(9+incresA2, 3+9, catchAdmin_data_oskar()[deals][6],currency_format),
            worksheet_oskar.write(9+incresA2, 8+9, catchAdmin_data_oskar()[deals][7],currency_format),
            worksheet_oskar.write(9+incresA2, 7+9, catchAdmin_data_oskar()[deals][8],currency_format)
            ) if (dataofexcel == "Покупка") else (
            worksheet_oskar.write(9+incresA2, 0, incresA2+1), 
            worksheet_oskar.write(9+incresA2, 4+9, float(catchAdmin_data_oskar()[deals][2]),currency_format), 
            worksheet_oskar.write(9+incresA2, 5+9, float(catchAdmin_data_oskar()[deals][5]),currency_format), 
            worksheet_oskar.write(9+incresA2, 6+9, catchAdmin_data_oskar()[deals][6],currency_format),
            worksheet_oskar.write(9+incresA2, 8+9, catchAdmin_data_oskar()[deals][7],currency_format),
            worksheet_oskar.write(9+incresA2, 7+9, catchAdmin_data_oskar()[deals][8],currency_format)
            )
            productionPurchesorSell(catchAdmin_data_oskar()[deals][3])
            worksheet_oskar.write(9+len(catchAdmin_data_oskar()), 0, "Итого"),
            incres2 += 1
            incresA2 += 1
            incresB2 += 1
            incresC2 += 1
            incresD2 += 1
        elif catchAdmin_data_oskar()[deals][1] == "€":
            productionPurchesorSell = lambda dataofexcel: ( 
            worksheet_oskar.write(9+incresB2, 0, incresB2+1), 
            worksheet_oskar.write(9+incresB2, 1+9*2, float(catchAdmin_data_oskar()[deals][2]),currency_format), 
            worksheet_oskar.write(9+incresB2, 2+9*2, float(catchAdmin_data_oskar()[deals][5]),currency_format), 
            worksheet_oskar.write(9+incresB2, 3+9*2, catchAdmin_data_oskar()[deals][6],currency_format),
            worksheet_oskar.write(9+incresB2, 8+9*2, catchAdmin_data_oskar()[deals][7],currency_format),
            worksheet_oskar.write(9+incresB2, 7+9*2, catchAdmin_data_oskar()[deals][8],currency_format)
            ) if (dataofexcel == "Покупка") else (
            worksheet_oskar.write(9+incresB2, 0, incresB2+1), 
            worksheet_oskar.write(9+incresB2, 4+18, float(catchAdmin_data_oskar()[deals][2]),currency_format), 
            worksheet_oskar.write(9+incresB2, 5+18, float(catchAdmin_data_oskar()[deals][5]),currency_format), 
            worksheet_oskar.write(9+incresB2, 6+18, catchAdmin_data_oskar()[deals][6],currency_format),
            worksheet_oskar.write(9+incresB2, 8+18, catchAdmin_data_oskar()[deals][7],currency_format),
            worksheet_oskar.write(9+incresB2, 7+9*2, catchAdmin_data_oskar()[deals][8],currency_format)
            )
            productionPurchesorSell(catchAdmin_data_oskar()[deals][3])
            worksheet_oskar.write(9+len(catchAdmin_data_oskar()), 0, "Итого")
            incres2 += 1
            incresA2 += 1
            incresB2 += 1
            incresC2 += 1
            incresD2 += 1
        elif catchAdmin_data_oskar()[deals][1] == "£":
            productionPurchesorSell = lambda dataofexcel: ( 
            worksheet_oskar.write(9+incresC2, 0, incresC2+1), 
            worksheet_oskar.write(9+incresC2, 1+27, float(catchAdmin_data_oskar()[deals][2]),currency_format), 
            worksheet_oskar.write(9+incresC2, 2+27, float(catchAdmin_data_oskar()[deals][5]),currency_format), 
            worksheet_oskar.write(9+incresC2, 3+27, catchAdmin_data_oskar()[deals][6],currency_format),
            worksheet_oskar.write(9+incresC2, 8+27, catchAdmin_data_oskar()[deals][7],currency_format),
            worksheet_oskar.write(9+incresC2, 7+27, catchAdmin_data_oskar()[deals][8],currency_format)
            ) if (dataofexcel == "Покупка") else (
            worksheet_oskar.write(9+incresC2, 0, incresC2+1), 
            worksheet_oskar.write(9+incresC2, 4+27, float(catchAdmin_data_oskar()[deals][2]),currency_format), 
            worksheet_oskar.write(9+incresC2, 5+27, float(catchAdmin_data_oskar()[deals][5]),currency_format), 
            worksheet_oskar.write(9+incresC2, 6+27, catchAdmin_data_oskar()[deals][6],currency_format),
            worksheet_oskar.write(9+incresC2, 8+27, catchAdmin_data_oskar()[deals][7],currency_format),
            worksheet_oskar.write(9+incresC2, 7+27, catchAdmin_data_oskar()[deals][8],currency_format)
            )
            productionPurchesorSell(catchAdmin_data_oskar()[deals][3])
            worksheet_oskar.write(9+len(catchAdmin_data_oskar()), 0, "Итого")
            incres2 += 1
            incresA2 += 1
            incresB2 += 1
            incresC2 += 1
            incresD2 += 1
        else: 
            productionPurchesorSell = lambda dataofexcel: ( 
            worksheet_oskar.write(9+incresD2, 0, incresD2+1), 
            worksheet_oskar.write(9+incresD2, 1+36, float(catchAdmin_data_oskar()[deals][2]),currency_format), 
            worksheet_oskar.write(9+incresD2, 2+36, float(catchAdmin_data_oskar()[deals][5]),currency_format), 
            worksheet_oskar.write(9+incresD2, 3+36, catchAdmin_data_oskar()[deals][6],currency_format),
            worksheet_oskar.write(9+incresD2, 8+36, catchAdmin_data_oskar()[deals][7],currency_format),
            worksheet_oskar.write(9+incresD2, 7+36, catchAdmin_data_oskar()[deals][8],currency_format)
            ) if (dataofexcel == "Покупка") else (
            worksheet_oskar.write(9+incresD2, 0, incresD2+1), 
            worksheet_oskar.write(9+incresD2, 4+36, float(catchAdmin_data_oskar()[deals][2]),currency_format), 
            worksheet_oskar.write(9+incresD2, 5+36, float(catchAdmin_data_oskar()[deals][5]),currency_format), 
            worksheet_oskar.write(9+incresD2, 6+36, catchAdmin_data_oskar()[deals][6],currency_format),
            worksheet_oskar.write(9+incresD2, 8+36, catchAdmin_data_oskar()[deals][7],currency_format),
            worksheet_oskar.write(9+incresD2, 7+36, catchAdmin_data_oskar()[deals][8],currency_format)
            )
            productionPurchesorSell(catchAdmin_data_oskar()[deals][3])
            worksheet_oskar.write(9+len(catchAdmin_data_oskar()), 0, "Итого")
            
            incres2 += 1
            incresA2 += 1
            incresB2 += 1
            incresC2 += 1
            incresD2 += 1
        

        worksheet_oskar.write_formula(9+len(catchAdmin_data_oskar()), 1, f'=SUM(B10:B{int(len(catchAdmin_data_oskar()))+9})', currency_format)
        
        worksheet_oskar.write_formula(9+len(catchAdmin_data_oskar()), 3, f'=SUM(D10:D{int(len(catchAdmin_data_oskar()))+9})',currency_format)

        worksheet_oskar.write_formula(9+len(catchAdmin_data_oskar()), 4, f'=SUM(E10:E{int(len(catchAdmin_data_oskar()))+9})',currency_format)
        
        worksheet_oskar.write_formula(9+len(catchAdmin_data_oskar()), 6, f'=SUM(G10:G{int(len(catchAdmin_data_oskar()))+9})',currency_format)
        
        
        
        worksheet_oskar.write_formula(9+len(catchAdmin_data_oskar()), 10, f'=SUM(K10:K{int(len(catchAdmin_data_oskar()))+9})', currency_format)
        
        worksheet_oskar.write_formula(9+len(catchAdmin_data_oskar()), 12, f'=SUM(M10:M{int(len(catchAdmin_data_oskar()))+9})',currency_format)

        worksheet_oskar.write_formula(9+len(catchAdmin_data_oskar()), 13, f'=SUM(N10:N{int(len(catchAdmin_data_oskar()))+9})',currency_format)
        
        worksheet_oskar.write_formula(9+len(catchAdmin_data_oskar()), 15, f'=SUM(P10:P{int(len(catchAdmin_data_oskar()))+9})',currency_format)
    
    
        worksheet_oskar.write_formula(9+len(catchAdmin_data_oskar()), 19, f'=SUM(T10:T{int(len(catchAdmin_data_oskar()))+9})', currency_format)
        
        worksheet_oskar.write_formula(9+len(catchAdmin_data_oskar()), 21, f'=SUM(V10:V{int(len(catchAdmin_data_oskar()))+9})',currency_format)

        worksheet_oskar.write_formula(9+len(catchAdmin_data_oskar()), 22, f'=SUM(W10:W{int(len(catchAdmin_data_oskar()))+9})',currency_format)
        
        worksheet_oskar.write_formula(9+len(catchAdmin_data_oskar()), 24, f'=SUM(Y10:Y{int(len(catchAdmin_data_oskar()))+9})',currency_format)
        
        
        worksheet_oskar.write_formula(9+len(catchAdmin_data_oskar()), 28, f'=SUM(AC10:AC{int(len(catchAdmin_data_oskar()))+9})', currency_format)
        
        worksheet_oskar.write_formula(9+len(catchAdmin_data_oskar()), 30, f'=SUM(AE10:AE{int(len(catchAdmin_data_oskar()))+9})',currency_format)

        worksheet_oskar.write_formula(9+len(catchAdmin_data_oskar()), 31, f'=SUM(AF10:AF{int(len(catchAdmin_data_oskar()))+9})',currency_format)
        
        worksheet_oskar.write_formula(9+len(catchAdmin_data_oskar()), 33, f'=SUM(AH10:AH{int(len(catchAdmin_data_oskar()))+9})',currency_format)
        

        worksheet_oskar.write_formula(9+len(catchAdmin_data_oskar()), 37, f'=SUM(AL10:AL{int(len(catchAdmin_data_oskar()))+9})', currency_format)
        
        worksheet_oskar.write_formula(9+len(catchAdmin_data_oskar()), 39, f'=SUM(AN10:AN{int(len(catchAdmin_data_oskar()))+9})',currency_format)

        worksheet_oskar.write_formula(9+len(catchAdmin_data_oskar()), 40, f'=SUM(AO10:AO{int(len(catchAdmin_data_oskar()))+9})',currency_format)
        
        worksheet_oskar.write_formula(9+len(catchAdmin_data_oskar()), 42, f'=SUM(AQ10:AQ{int(len(catchAdmin_data_oskar()))+9})',currency_format)
                
    worksheet_tulskaya.write(0, 0, "Дата")
    worksheet_tulskaya.write(0, 1, Previous_Date.strftime("%Y-%m-%d"))
    worksheet_tulskaya.write(0, 10, "Дата")
    worksheet_tulskaya.write(0, 11, datetime.today().strftime("%Y-%m-%d"))

    currencyDefine = [
        "RUB", "USD", "EURO", "GPB", "CNY", "Тенге"
    ]
    TheActions = [
        "Объем", "Курс", "Цена операции", "Объем", "Курс", "Цена операции", " ", " ", " "
    ]

    count = 2
    while count <= len(currencyDefine)+1:
        worksheet_tulskaya.write(0, count, currencyDefine[count-2])
        
        worksheet_tulskaya.write(0, count+10, currencyDefine[count-2])
            
        count += 1
        
    merge_format = workbook.add_format({
        'bold': 1,
        'align': 'center',
        'valign': 'vcenter',
    })
    
    currency_format = workbook.add_format({'num_format': '#,##0.00'})
    
    try:
        worksheet_tulskaya.write(1, 2, tulskaya((datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"), 'rub')[0][0])
        worksheet_tulskaya.write(1, 3, tulskaya((datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"), 'usd')[0][0])
        worksheet_tulskaya.write(1, 4, tulskaya((datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"), 'eur')[0][0])
        worksheet_tulskaya.write(1, 5, tulskaya((datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"), 'gpb')[0][0])
        worksheet_tulskaya.write(1, 6, tulskaya((datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"), 'cny')[0][0])
        worksheet_tulskaya.write(1, 12, f'{rub()}',currency_format)
    
        worksheet_tulskaya.write(1, 13, f'{usd()}',currency_format)
        
        worksheet_tulskaya.write(1, 14, f'{eur()}',currency_format)
        
        worksheet_tulskaya.write(1, 15, f'{gpb()}',currency_format)
        
        worksheet_tulskaya.write(1, 16, f'{cny()}',currency_format)
    except:
        worksheet_tulskaya.write(1, 2, 0)
        worksheet_tulskaya.write(1, 3, 0)
        worksheet_tulskaya.write(1, 4, 0)
        worksheet_tulskaya.write(1, 5, 0)
        worksheet_tulskaya.write(1, 6, 0)
        worksheet_tulskaya.write(1, 12, f'{rub()}',currency_format)
    
        worksheet_tulskaya.write(1, 13, f'{usd()}',currency_format)
        
        worksheet_tulskaya.write(1, 14, f'{eur()}',currency_format)
        
        worksheet_tulskaya.write(1, 15, f'{gpb()}',currency_format)
        
        worksheet_tulskaya.write(1, 16, f'{cny()}',currency_format)
    
    worksheet_tulskaya.merge_range('A2:B2','Остатки на начало дня', merge_format)
    worksheet_tulskaya.merge_range('K2:L2','Остатки на конец дня', merge_format)
    # RUB
    worksheet_tulskaya.merge_range('B7:I7', 'Рубль', merge_format)
    worksheet_tulskaya.merge_range('B8:D8', 'Покупка', merge_format)
    worksheet_tulskaya.merge_range('E8:G8', 'Продажа', merge_format)
    worksheet_tulskaya.merge_range('H8:H9', "Сотрудник", merge_format)
    worksheet_tulskaya.merge_range('I8:I9', "Коммент", merge_format)
    worksheet_tulskaya.merge_range('A7:A9', '№', merge_format)

    # USD
    worksheet_tulskaya.merge_range('K7:R7', 'Доллар', merge_format)
    worksheet_tulskaya.merge_range('K8:M8', 'Покупка', merge_format)
    worksheet_tulskaya.merge_range('N8:P8', 'Продажа', merge_format)
    worksheet_tulskaya.merge_range('Q8:Q9', "Сотрудник", merge_format)
    worksheet_tulskaya.merge_range('R8:R9', "Коммент", merge_format)

    # Euro
    worksheet_tulskaya.merge_range('T7:AA7', 'Евро', merge_format)
    worksheet_tulskaya.merge_range('T8:V8', 'Покупка', merge_format)
    worksheet_tulskaya.merge_range('W8:Y8', 'Продажа', merge_format)
    worksheet_tulskaya.merge_range('Z8:Z9', "Сотрудник", merge_format)
    worksheet_tulskaya.merge_range('AA8:AA9', "Коммент", merge_format)

    # Pound
    worksheet_tulskaya.merge_range('AC7:AJ7', 'Фунт', merge_format)
    worksheet_tulskaya.merge_range('AC8:AE8', 'Покупка', merge_format)
    worksheet_tulskaya.merge_range('AF8:AH8', 'Продажа', merge_format)
    worksheet_tulskaya.merge_range('AI8:AI9', "Сотрудник", merge_format)
    worksheet_tulskaya.merge_range('AJ8:AJ9', "Коммент", merge_format)

    # Yuan
    worksheet_tulskaya.merge_range('AL7:AS7', 'Юань', merge_format)
    worksheet_tulskaya.merge_range('AL8:AN8', 'Покупка', merge_format)
    worksheet_tulskaya.merge_range('AO8:AQ8', 'Продажа', merge_format)
    worksheet_tulskaya.merge_range('AR8:AR9', "Сотрудник", merge_format)
    worksheet_tulskaya.merge_range('AS8:AS9', "Коммент", merge_format)

    counts = 1
    for i in TheActions*5:
        worksheet_tulskaya.write(8, counts, i, merge_format)

        counts += 1

    incres = 0
    incresA = 0
    incresB = 0
    incresC = 0
    incresD = 0

    for deals in range(len(catchAdmin_data_tulskaya())):
        # print(type(float(catchAdmin_data_tulskaya()[deals][2])))
        if catchAdmin_data_tulskaya()[deals][1] == "₽":
            productionPurchesorSell = lambda dataofexcel: ( 
            worksheet_tulskaya.write(9+incres, 0, incres+1),
            worksheet_tulskaya.write(9+incres, 1, float(catchAdmin_data_tulskaya()[deals][2]),currency_format), 
            worksheet_tulskaya.write(9+incres, 2, float(catchAdmin_data_tulskaya()[deals][5]),currency_format), 
            worksheet_tulskaya.write(9+incres, 3, catchAdmin_data_tulskaya()[deals][6],currency_format),
            worksheet_tulskaya.write(9+incres, 8, catchAdmin_data_tulskaya()[deals][7],currency_format),
            worksheet_tulskaya.write(9+incres, 7, catchAdmin_data_tulskaya()[deals][8],currency_format)
            ) if (dataofexcel == "Покупка") else (
            worksheet_tulskaya.write(9+incres, 0, incres+1), 
            worksheet_tulskaya.write(9+incres, 4, float(catchAdmin_data_tulskaya()[deals][2]),currency_format), 
            worksheet_tulskaya.write(9+incres, 5, float(catchAdmin_data_tulskaya()[deals][5]),currency_format), 
            worksheet_tulskaya.write(9+incres, 6, catchAdmin_data_tulskaya()[deals][6],currency_format),
            worksheet_tulskaya.write(9+incres, 8, catchAdmin_data_tulskaya()[deals][7],currency_format),
            worksheet_tulskaya.write(9+incres, 7, catchAdmin_data_tulskaya()[deals][8],currency_format)
            )
            productionPurchesorSell(catchAdmin_data_tulskaya()[deals][3])
            worksheet_tulskaya.write(9+len(catchAdmin_data_tulskaya()), 0, "Итого")
            incres += 1
            incresA += 1
            incresB += 1
            incresC += 1
            incresD += 1
            
        elif catchAdmin_data_tulskaya()[deals][1] == "$":
            productionPurchesorSell = lambda dataofexcel: ( 
            worksheet_tulskaya.write(9+incresA, 0, incresA+1), 
            worksheet_tulskaya.write(9+incresA, 1+9, float(catchAdmin_data_tulskaya()[deals][2]),currency_format), 
            worksheet_tulskaya.write(9+incresA, 2+9, float(catchAdmin_data_tulskaya()[deals][5]),currency_format), 
            worksheet_tulskaya.write(9+incresA, 3+9, catchAdmin_data_tulskaya()[deals][6],currency_format),
            worksheet_tulskaya.write(9+incresA, 8+9, catchAdmin_data_tulskaya()[deals][7],currency_format),
            worksheet_tulskaya.write(9+incresA, 7+9, catchAdmin_data_tulskaya()[deals][8],currency_format)
            ) if (dataofexcel == "Покупка") else (
            worksheet_tulskaya.write(9+incresA, 0, incresA+1), 
            worksheet_tulskaya.write(9+incresA, 4+9, float(catchAdmin_data_tulskaya()[deals][2]),currency_format), 
            worksheet_tulskaya.write(9+incresA, 5+9, float(catchAdmin_data_tulskaya()[deals][5]),currency_format), 
            worksheet_tulskaya.write(9+incresA, 6+9, catchAdmin_data_tulskaya()[deals][6],currency_format),
            worksheet_tulskaya.write(9+incresA, 8+9, catchAdmin_data_tulskaya()[deals][7],currency_format),
            worksheet_tulskaya.write(9+incresA, 7+9, catchAdmin_data_tulskaya()[deals][8],currency_format)
            )
            productionPurchesorSell(catchAdmin_data_tulskaya()[deals][3])
            worksheet_tulskaya.write(9+len(catchAdmin_data_tulskaya()), 0, "Итого"),
            incres += 1
            incresA += 1
            incresB += 1
            incresC += 1
            incresD += 1
        elif catchAdmin_data_tulskaya()[deals][1] == "€":
            productionPurchesorSell = lambda dataofexcel: ( 
            worksheet_tulskaya.write(9+incresB, 0, incresB+1), 
            worksheet_tulskaya.write(9+incresB, 1+9*2, float(catchAdmin_data_tulskaya()[deals][2]),currency_format), 
            worksheet_tulskaya.write(9+incresB, 2+9*2, float(catchAdmin_data_tulskaya()[deals][5]),currency_format), 
            worksheet_tulskaya.write(9+incresB, 3+9*2, catchAdmin_data_tulskaya()[deals][6],currency_format),
            worksheet_tulskaya.write(9+incresB, 8+9*2, catchAdmin_data_tulskaya()[deals][7],currency_format),
            worksheet_tulskaya.write(9+incresB, 7+9*2, catchAdmin_data_tulskaya()[deals][8],currency_format)
            ) if (dataofexcel == "Покупка") else (
            worksheet_tulskaya.write(9+incresB, 0, incresB+1), 
            worksheet_tulskaya.write(9+incresB, 4+18, float(catchAdmin_data_tulskaya()[deals][2]),currency_format), 
            worksheet_tulskaya.write(9+incresB, 5+18, float(catchAdmin_data_tulskaya()[deals][5]),currency_format), 
            worksheet_tulskaya.write(9+incresB, 6+18, catchAdmin_data_tulskaya()[deals][6],currency_format),
            worksheet_tulskaya.write(9+incresB, 8+18, catchAdmin_data_tulskaya()[deals][7],currency_format),
            worksheet_tulskaya.write(9+incresB, 7+9*2, catchAdmin_data_tulskaya()[deals][8],currency_format)
            )
            productionPurchesorSell(catchAdmin_data_tulskaya()[deals][3])
            worksheet_tulskaya.write(9+len(catchAdmin_data_tulskaya()), 0, "Итого")
            incres += 1
            incresA += 1
            incresB += 1
            incresC += 1
            incresD += 1
        elif catchAdmin_data_tulskaya()[deals][1] == "£":
            productionPurchesorSell = lambda dataofexcel: ( 
            worksheet_tulskaya.write(9+incresC, 0, incresC+1), 
            worksheet_tulskaya.write(9+incresC, 1+27, float(catchAdmin_data_tulskaya()[deals][2]),currency_format), 
            worksheet_tulskaya.write(9+incresC, 2+27, float(catchAdmin_data_tulskaya()[deals][5]),currency_format), 
            worksheet_tulskaya.write(9+incresC, 3+27, catchAdmin_data_tulskaya()[deals][6],currency_format),
            worksheet_tulskaya.write(9+incresC, 8+27, catchAdmin_data_tulskaya()[deals][7],currency_format),
            worksheet_tulskaya.write(9+incresC, 7+27, catchAdmin_data_tulskaya()[deals][8],currency_format)
            ) if (dataofexcel == "Покупка") else (
            worksheet_tulskaya.write(9+incresC, 0, incresC+1), 
            worksheet_tulskaya.write(9+incresC, 4+27, float(catchAdmin_data_tulskaya()[deals][2]),currency_format), 
            worksheet_tulskaya.write(9+incresC, 5+27, float(catchAdmin_data_tulskaya()[deals][5]),currency_format), 
            worksheet_tulskaya.write(9+incresC, 6+27, catchAdmin_data_tulskaya()[deals][6],currency_format),
            worksheet_tulskaya.write(9+incresC, 8+27, catchAdmin_data_tulskaya()[deals][7],currency_format),
            worksheet_tulskaya.write(9+incresC, 7+27, catchAdmin_data_tulskaya()[deals][8],currency_format)
            )
            productionPurchesorSell(catchAdmin_data_tulskaya()[deals][3])
            worksheet_tulskaya.write(9+len(catchAdmin_data_tulskaya()), 0, "Итого")
            incres += 1
            incresA += 1
            incresB += 1
            incresC += 1
            incresD += 1
        else: 
            productionPurchesorSell = lambda dataofexcel: ( 
            worksheet_tulskaya.write(9+incresD, 0, incresD+1), 
            worksheet_tulskaya.write(9+incresD, 1+36, float(catchAdmin_data_tulskaya()[deals][2]),currency_format), 
            worksheet_tulskaya.write(9+incresD, 2+36, float(catchAdmin_data_tulskaya()[deals][5]),currency_format), 
            worksheet_tulskaya.write(9+incresD, 3+36, catchAdmin_data_tulskaya()[deals][6],currency_format),
            worksheet_tulskaya.write(9+incresD, 8+36, catchAdmin_data_tulskaya()[deals][7],currency_format),
            worksheet_tulskaya.write(9+incresD, 7+36, catchAdmin_data_tulskaya()[deals][8],currency_format)
            ) if (dataofexcel == "Покупка") else (
            worksheet_tulskaya.write(9+incresD, 0, incresD+1), 
            worksheet_tulskaya.write(9+incresD, 4+36, float(catchAdmin_data_tulskaya()[deals][2]),currency_format), 
            worksheet_tulskaya.write(9+incresD, 5+36, float(catchAdmin_data_tulskaya()[deals][5]),currency_format), 
            worksheet_tulskaya.write(9+incresD, 6+36, catchAdmin_data_tulskaya()[deals][6],currency_format),
            worksheet_tulskaya.write(9+incresD, 8+36, catchAdmin_data_tulskaya()[deals][7],currency_format),
            worksheet_tulskaya.write(9+incresD, 7+36, catchAdmin_data_tulskaya()[deals][8],currency_format)
            )
            productionPurchesorSell(catchAdmin_data_tulskaya()[deals][3])
            worksheet_tulskaya.write(9+len(catchAdmin_data_tulskaya()), 0, "Итого")
            
            incres += 1
            incresA += 1
            incresB += 1
            incresC += 1
            incresD += 1
        

        worksheet_tulskaya.write_formula(9+len(catchAdmin_data_tulskaya()), 1, f'=SUM(B10:B{int(len(catchAdmin_data_tulskaya()))+9})', currency_format)
        
        worksheet_tulskaya.write_formula(9+len(catchAdmin_data_tulskaya()), 3, f'=SUM(D10:D{int(len(catchAdmin_data_tulskaya()))+9})',currency_format)

        worksheet_tulskaya.write_formula(9+len(catchAdmin_data_tulskaya()), 4, f'=SUM(E10:E{int(len(catchAdmin_data_tulskaya()))+9})',currency_format)
        
        worksheet_tulskaya.write_formula(9+len(catchAdmin_data_tulskaya()), 6, f'=SUM(G10:G{int(len(catchAdmin_data_tulskaya()))+9})',currency_format)
        
        
        
        worksheet_tulskaya.write_formula(9+len(catchAdmin_data_tulskaya()), 10, f'=SUM(K10:K{int(len(catchAdmin_data_tulskaya()))+9})', currency_format)
        
        worksheet_tulskaya.write_formula(9+len(catchAdmin_data_tulskaya()), 12, f'=SUM(M10:M{int(len(catchAdmin_data_tulskaya()))+9})',currency_format)

        worksheet_tulskaya.write_formula(9+len(catchAdmin_data_tulskaya()), 13, f'=SUM(N10:N{int(len(catchAdmin_data_tulskaya()))+9})',currency_format)
        
        worksheet_tulskaya.write_formula(9+len(catchAdmin_data_tulskaya()), 15, f'=SUM(P10:P{int(len(catchAdmin_data_tulskaya()))+9})',currency_format)
    
    
        worksheet_tulskaya.write_formula(9+len(catchAdmin_data_tulskaya()), 19, f'=SUM(T10:T{int(len(catchAdmin_data_tulskaya()))+9})', currency_format)
        
        worksheet_tulskaya.write_formula(9+len(catchAdmin_data_tulskaya()), 21, f'=SUM(V10:V{int(len(catchAdmin_data_tulskaya()))+9})',currency_format)

        worksheet_tulskaya.write_formula(9+len(catchAdmin_data_tulskaya()), 22, f'=SUM(W10:W{int(len(catchAdmin_data_tulskaya()))+9})',currency_format)
        
        worksheet_tulskaya.write_formula(9+len(catchAdmin_data_tulskaya()), 24, f'=SUM(Y10:Y{int(len(catchAdmin_data_tulskaya()))+9})',currency_format)
        
        
        worksheet_tulskaya.write_formula(9+len(catchAdmin_data_tulskaya()), 28, f'=SUM(AC10:AC{int(len(catchAdmin_data_tulskaya()))+9})', currency_format)
        
        worksheet_tulskaya.write_formula(9+len(catchAdmin_data_tulskaya()), 30, f'=SUM(AE10:AE{int(len(catchAdmin_data_tulskaya()))+9})',currency_format)

        worksheet_tulskaya.write_formula(9+len(catchAdmin_data_tulskaya()), 31, f'=SUM(AF10:AF{int(len(catchAdmin_data_tulskaya()))+9})',currency_format)
        
        worksheet_tulskaya.write_formula(9+len(catchAdmin_data_tulskaya()), 33, f'=SUM(AH10:AH{int(len(catchAdmin_data_tulskaya()))+9})',currency_format)
        

        worksheet_tulskaya.write_formula(9+len(catchAdmin_data_tulskaya()), 37, f'=SUM(AL10:AL{int(len(catchAdmin_data_tulskaya()))+9})', currency_format)
        
        worksheet_tulskaya.write_formula(9+len(catchAdmin_data_tulskaya()), 39, f'=SUM(AN10:AN{int(len(catchAdmin_data_tulskaya()))+9})',currency_format)

        worksheet_tulskaya.write_formula(9+len(catchAdmin_data_tulskaya()), 40, f'=SUM(AO10:AO{int(len(catchAdmin_data_tulskaya()))+9})',currency_format)
        
        worksheet_tulskaya.write_formula(9+len(catchAdmin_data_tulskaya()), 42, f'=SUM(AQ10:AQ{int(len(catchAdmin_data_tulskaya()))+9})',currency_format)
        
    workbook.close()

    

# CURRENT WORK OUT SECTION 
def excelExporter(
    name, place
):

    workbook = xlsxwriter.Workbook(f'./layout/results {datetime.today().strftime("%Y-%m-%d")} {name}.xlsx')
    worksheet = workbook.add_worksheet(place)
    # Field open a day with prices
    Previous_Date = datetime.today() - timedelta(days=1)
    # Determind a data of this day
    worksheet.write(0, 0, "Дата")
    worksheet.write(0, 1, Previous_Date.strftime("%Y-%m-%d"))
    worksheet.write(0, 10, "Дата")
    worksheet.write(0, 11, datetime.today().strftime("%Y-%m-%d"))

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
    print(place)
    
    if place == "Тульская":
        try:
            worksheet.write(1, 2, tulskaya((datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"), 'rub')[0][0])
            worksheet.write(1, 3, tulskaya((datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"), 'usd')[0][0])
            worksheet.write(1, 4, tulskaya((datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"), 'eur')[0][0])
            worksheet.write(1, 5, tulskaya((datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"), 'gpb')[0][0])
            worksheet.write(1, 6, tulskaya((datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"), 'cny')[0][0])
            worksheet.write(1, 12, f'{rub()}',currency_format)
        
            worksheet.write(1, 13, f'{usd()}',currency_format)
            
            worksheet.write(1, 14, f'{eur()}',currency_format)
            
            worksheet.write(1, 15, f'{gpb()}',currency_format)
            
            worksheet.write(1, 16, f'{cny()}',currency_format)
        except:
            worksheet.write(1, 2, 0)
            worksheet.write(1, 3, 0)
            worksheet.write(1, 4, 0)
            worksheet.write(1, 5, 0)
            worksheet.write(1, 6, 0)
            worksheet.write(1, 12, f'{rub()}',currency_format)
        
            worksheet.write(1, 13, f'{usd()}',currency_format)
            
            worksheet.write(1, 14, f'{eur()}',currency_format)
            
            worksheet.write(1, 15, f'{gpb()}',currency_format)
            
            worksheet.write(1, 16, f'{cny()}',currency_format)
    elif place == "Оскар":
        try:
            worksheet.write(1, 2, oskar((datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"), 'rub')[0][0])
            worksheet.write(1, 3, oskar((datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"), 'usd')[0][0])
            worksheet.write(1, 4, oskar((datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"), 'eur')[0][0])
            worksheet.write(1, 5, oskar((datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"), 'gpb')[0][0])
            worksheet.write(1, 6, oskar((datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"), 'cny')[0][0])
            worksheet.write(1, 12, f'{rub_osk()}',currency_format)
        
            worksheet.write(1, 13, f'{usd_osk()}',currency_format)
            
            worksheet.write(1, 14, f'{eur_osk()}',currency_format)
            
            worksheet.write(1, 15, f'{gpb_osk()}',currency_format)
            
            worksheet.write(1, 16, f'{cny_osk()}',currency_format)
        except:
            worksheet.write(1, 2, 0)
            worksheet.write(1, 3, 0)
            worksheet.write(1, 4, 0)
            worksheet.write(1, 5, 0)
            worksheet.write(1, 6, 0)
            worksheet.write(1, 12, f'{rub_osk()}',currency_format)
        
            worksheet.write(1, 13, f'{usd_osk()}',currency_format)
            
            worksheet.write(1, 14, f'{eur_osk()}',currency_format)
            
            worksheet.write(1, 15, f'{gpb_osk()}',currency_format)
            
            worksheet.write(1, 16, f'{cny_osk()}',currency_format)
    elif place == "Кешер": 
        try:
            worksheet.write(1, 2, kesher((datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"), 'rub')[0][0])
            worksheet.write(1, 3, kesher((datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"), 'usd')[0][0])
            worksheet.write(1, 4, kesher((datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"), 'eur')[0][0])
            worksheet.write(1, 5, kesher((datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"), 'gpb')[0][0])
            worksheet.write(1, 6, kesher((datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"), 'cny')[0][0])
            worksheet.write(1, 12, f'{rub_kesher()}',currency_format)
        
            worksheet.write(1, 13, f'{usd_kesher()}',currency_format)
            
            worksheet.write(1, 14, f'{eur_kesher()}',currency_format)
            
            worksheet.write(1, 15, f'{gpb_kesher()}',currency_format)
            
            worksheet.write(1, 16, f'{cny_kesher()}',currency_format)
        except:
            worksheet.write(1, 2, 0)
            worksheet.write(1, 3, 0)
            worksheet.write(1, 4, 0)
            worksheet.write(1, 5, 0)
            worksheet.write(1, 6, 0)
            worksheet.write(1, 12, f'{rub_kesher()}',currency_format)
        
            worksheet.write(1, 13, f'{usd_kesher()}',currency_format)
            
            worksheet.write(1, 14, f'{eur_kesher()}',currency_format)
            
            worksheet.write(1, 15, f'{gpb_kesher()}',currency_format)
            
            worksheet.write(1, 16, f'{cny_kesher()}',currency_format)
    
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
            worksheet.write(9+incres, 7, catchALL_Data(name)[deals][8],currency_format),
           
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
        elif catchALL_Data(name)[deals][1] == "£":
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
            if not (existence(db_user.shortname) == [(1,)]):
                create_xlsxofDB(db_user.shortname)
            if not (existenceAdmin() == [(1,)]):
                mergedTable()
            context = {'request':request, 'timestamp':datetime.now().strftime("%H:%M"),'dateandtime': datetime.now().strftime("%Y-%m-%d"), 'user': db_user.shortname}
            return templates.TemplateResponse('Temporary.html', context)
        elif db_user.role == "Директор":
            if not (existence(db_user.shortname) == [(1,)]):
                create_xlsxofDB(db_user.shortname)
            if not (existenceAdmin() == [(1,)]):
                mergedTable()
            context = {'request':request, 'timestamp':datetime.now().strftime("%H:%M"),'dateandtime': datetime.now().strftime("%Y-%m-%d"), 'user': db_user.shortname}
            return templates.TemplateResponse('Temporary-director.html', context)
        else: pass
    
    raise HTTPException(
            status_code=401, detail="Вход не верный"
        )
    
# Create an user account 👤
@app.post("/signup")
def signup(
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
        
        shortname = nltk.RegexpTokenizer(r'\w+').tokenize(email)[0],
        hashed_password = get_password_hash(password)
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    token = create_access_token(db_user)
    send_mail(to=db_user.email, token=token, username=db_user.username)
    
    return templates.TemplateResponse('Send-request.html', {'request':request, 'timestamp':datetime.now().strftime("%H:%M")})

@app.post('/{user}/Home')
def home(
    request: Request,
    user: str,

    currn: str = Form(),
    currency: str = Form(),
    currencyVAL: str = Form(),
    valval: str = Form(),
    deal: str = Form(),
    exchange: str = Form(),
    result: float = Form(),
    comment: Optional[str] = Form('')
):  
    def place():
        conn = lite.connect('sql/Users.db')
        cur = conn.cursor()
        with conn:
            cur.execute(f'''
                SELECT place FROM user where shortname = "{user}";
            ''')
        return cur.fetchall()[0][0]
        
    conn = lite.connect('sql/Deals.db')
    cur = conn.cursor()
    with conn:
        cur.execute(f'''
            INSERT INTO Deals_{user} (currn, currency, deal, calendar, exchange, result, comment, user, place) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        ''',(currn, float(currency+'.'+currencyVAL), deal, datetime.now().strftime("%Y-%m-%d"), float(exchange+'.'+valval), result, comment, user, place()))
        
    conn = lite.connect('sql/Admins.db')
    cur = conn.cursor()
    with conn:
        cur.execute(f'''
            INSERT INTO Deals (currn, currency, deal, calendar, exchange, result, comment, user, place) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        ''',(currn, float(currency+'.'+currencyVAL), deal, datetime.now().strftime("%Y-%m-%d"), float(exchange+'.'+valval), result, comment, user, place()))
        
    excelExporter(user, place())

    context = {'request':request, 'timestamp':datetime.now().strftime("%H:%M"),'dateandtime': datetime.now().strftime("%Y-%m-%d"), 'deal': len(catchALL_Data(user)), 'n' : catchALL_Data(user)[::-1], 'user': user}
    return templates.TemplateResponse('Home.html', context)

@app.post('/{user}/Default')
def default(
    request: Request,
    
    user: str,
    time: str = Form(),
    format: str = Form()
):
    path = r'C:\Users\roman\OneDrive\Рабочий стол\Global Finance inc\layout'

    if format == "Excel":
        if os.path.exists(os.path.join(path, f'results {time} {user}.xlsx')): return FileResponse(os.path.join(path, f'results {time} {user}.xlsx'), media_type="xlsx", filename=f'results {time} {user}.xlsx')
        return {"error" : "File not found!"}
    elif format == "PDF":
        pass
        
        context = {'request':request, 'timestamp':datetime.now().strftime("%H:%M"),'dateandtime': datetime.now().strftime("%Y-%m-%d"), 'user': user}
        return templates.TemplateResponse('Default.html', context)
        
        
    context = {'request':request, 'timestamp':datetime.now().strftime("%H:%M"),'dateandtime': datetime.now().strftime("%Y-%m-%d"), 'user': user}
    return templates.TemplateResponse('Error.html', context)

@app.post('/{user}/Director')
def director(
    request: Request,
    user: str,
    
    currn: str = Form(),
    currency: str = Form(),
    currencyVAL: str = Form(),
    valval: str = Form(),
    deal: str = Form(),
    exchange: str = Form(),
    result: float = Form(),
    comment: Optional[str] = Form('')
    
):    
    def place():
        conn = lite.connect('sql/Users.db')
        cur = conn.cursor()
        with conn:
            cur.execute(f'''
                SELECT place FROM user where shortname = "{user}";
            ''')
        return cur.fetchall()[0][0]
        
    conn = lite.connect('sql/Deals.db')
    cur = conn.cursor()
    with conn:
        cur.execute(f'''
            INSERT INTO Deals_{user} (currn, currency, deal, calendar, exchange, result, comment, user, place) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        ''',(currn, float(currency+'.'+currencyVAL), deal, datetime.now().strftime("%Y-%m-%d"), float(exchange+'.'+valval), result, comment, user, place()))
        
    conn = lite.connect('sql/Admins.db')
    cur = conn.cursor()
    with conn:
        cur.execute(f'''
            INSERT INTO Deals (currn, currency, deal, calendar, exchange, result, comment, user, place) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        ''',(currn, float(currency+'.'+currencyVAL), deal, datetime.now().strftime("%Y-%m-%d"), float(exchange+'.'+valval), result, comment, user, place()))
    
    context = {'request':request, 'timestamp':datetime.now().strftime("%H:%M"),'dateandtime': datetime.now().strftime("%Y-%m-%d"), 'deal': len(catchAdmin_data()), 'n' : catchAdmin_data()[::-1], 'user': user}
    return templates.TemplateResponse('Director.html', context)

@app.post('/{user}/Choosen')
def Choosen(
    request: Request,
    user: str,
    time: str = Form(),
    format: str = Form()
):
    path = r'C:\Users\roman\OneDrive\Рабочий стол\Global Finance inc\layout'

    if format == "Excel":
        if os.path.exists(os.path.join(path, f'admins {time} {user}.xlsx')): return FileResponse(os.path.join(path, f'admins {time} {user}.xlsx'), media_type="xlsx", filename=f'admins {time} {user}.xlsx')
        return {"error" : "File not found!"}
    elif format == "PDF":
        pass
        
        context = {'request':request, 'timestamp':datetime.now().strftime("%H:%M"),'dateandtime': datetime.now().strftime("%Y-%m-%d"), 'user': user}
        return templates.TemplateResponse('Choosen.html', context)
        
        
    context = {'request':request, 'timestamp':datetime.now().strftime("%H:%M"),'dateandtime': datetime.now().strftime("%Y-%m-%d"), 'user': user}
    return templates.TemplateResponse('Error.html', context)

def cleardatabase(user):
    conn = lite.connect('sql/Deals.db')
    cur = conn.cursor()
    with conn:
        cur.execute(f'''
            DELETE FROM Deals_{user};
        ''')
    return cur.fetchall()

def cleardatabaseADM():
    conn = lite.connect('sql/Admins.db')
    cur = conn.cursor()
    with conn:
        cur.execute(f'''
            DELETE FROM Deals;
        ''')
    return cur.fetchall()

@app.post('/{user}/Disactivate')
def Disactivate(
    request: Request,
    user: str
):
    cleardatabase(user)
    return templates.TemplateResponse('Disactivate.html', {'request':request, 'timestamp':datetime.now().strftime("%H:%M")})

@app.post('/{user}/DisactivateDirector')
def Disactivate(
    request: Request,
    user: str
):
    cleardatabaseADM()
    return templates.TemplateResponse('Disactivate.html', {'request':request, 'timestamp':datetime.now().strftime("%H:%M")})