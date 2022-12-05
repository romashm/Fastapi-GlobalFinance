
import sqlite3 as lite
from datetime import datetime, timedelta
from functools import reduce


def special_currency_dol_purs_osk():
    conn = lite.connect('sql/Admins.db')
    cur = conn.cursor()
    with conn:
        cur.execute('''
        select * from Deals where place = "Оскар" AND deal = "Покупка" AND currn = "$";
        ''')
        return cur.fetchall()

def special_currency_dol_sell_osk():
    conn = lite.connect('sql/Admins.db')
    cur = conn.cursor()
    with conn:
        cur.execute('''
        select * from Deals where place = "Оскар" AND deal = "Продажа" AND currn = "$";
        ''')
        return cur.fetchall()
    

def special_currency_rub_purs_osk():
    conn = lite.connect('sql/Admins.db')
    cur = conn.cursor()
    with conn:
        cur.execute('''
        select * from Deals where place = "Оскар" AND deal = "Покупка" AND currn = "₽";
        ''')
        return cur.fetchall()

def special_currency_rub_sell_osk():
    conn = lite.connect('sql/Admins.db')
    cur = conn.cursor()
    with conn:
        cur.execute('''
        select * from Deals where place = "Оскар" AND deal = "Продажа" AND currn = "₽";
        ''')
        return cur.fetchall()
    
def special_currency_eur_purs_osk():
    conn = lite.connect('sql/Admins.db')
    cur = conn.cursor()
    with conn:
        cur.execute('''
        select * from Deals where place = "Оскар" AND deal = "Покупка" AND currn = "€";
        ''')
        return cur.fetchall()

def special_currency_eur_sell_osk():
    conn = lite.connect('sql/Admins.db')
    cur = conn.cursor()
    with conn:
        cur.execute('''
        select * from Deals where place = "Оскар" AND deal = "Продажа" AND currn = "€";
        ''')
        return cur.fetchall()
    
def special_currency_gpb_purs_osk():
    conn = lite.connect('sql/Admins.db')
    cur = conn.cursor()
    with conn:
        cur.execute('''
        select * from Deals where place = "Оскар" AND deal = "Покупка" AND currn = "£";
        ''')
        return cur.fetchall()

def special_currency_gpb_sell_osk():
    conn = lite.connect('sql/Admins.db')
    cur = conn.cursor()
    with conn:
        cur.execute('''
        select * from Deals where place = "Оскар" AND deal = "Продажа" AND currn = "£";
        ''')
        return cur.fetchall()

def special_currency_uan_purs_osk():
    conn = lite.connect('sql/Admins.db')
    cur = conn.cursor()
    with conn:
        cur.execute('''
        select * from Deals where place = "Оскар" AND deal = "Покупка" AND currn = "¥";
        ''')
        return cur.fetchall()

def special_currency_uan_sell_osk():
    conn = lite.connect('sql/Admins.db')
    cur = conn.cursor()
    with conn:
        cur.execute('''
        select * from Deals where place = "Оскар" AND deal = "Продажа" AND currn = "¥";
        ''')
        return cur.fetchall()
    
def usd_osk():
    arr = []
    count = 0
    
    arr_1 = []
    count_1 = 0
    while count < len(special_currency_dol_purs_osk()):
        arr.append(float(special_currency_dol_purs_osk()[count][2]))
        
        count += 1
        
    while count_1 < len(special_currency_dol_sell_osk()):
        arr_1.append(float(special_currency_dol_sell_osk()[count_1][2]))
        
        count_1 += 1    
        
    a = sum(map(float,arr_1))
    b = sum(map(float,arr))
    
    return b-a

def rub_osk():
    arr = []
    count = 0
    
    arr_1 = []
    count_1 = 0
    while count < len(special_currency_rub_purs_osk()):
        arr.append(float(special_currency_rub_purs_osk()[count][2]))
        
        count += 1
        
    while count_1 < len(special_currency_rub_sell_osk()):
        arr_1.append(float(special_currency_rub_sell_osk()[count_1][2]))
        
        count_1 += 1    
        
    a = sum(map(float,arr_1))
    b = sum(map(float,arr))
    
    return b-a

def eur_osk():
    arr = []
    count = 0
    
    arr_1 = []
    count_1 = 0
    while count < len(special_currency_eur_purs_osk()):
        arr.append(float(special_currency_eur_purs_osk()[count][2]))
        
        count += 1
        
    while count_1 < len(special_currency_eur_sell_osk()):
        arr_1.append(float(special_currency_eur_sell_osk()[count_1][2]))
        
        count_1 += 1    
    
    a = sum(map(float,arr_1))
    b = sum(map(float,arr))
    
    return b-a

def gpb_osk():
    arr = []
    count = 0
    
    arr_1 = []
    count_1 = 0
    while count < len(special_currency_gpb_purs_osk()):
        arr.append(float(special_currency_gpb_purs_osk()[count][2]))
        
        count += 1
        
    while count_1 < len(special_currency_gpb_sell_osk()):
        arr_1.append(float(special_currency_gpb_sell_osk()[count_1][2]))
        
        count_1 += 1    
    
    a = sum(map(float,arr_1))
    b = sum(map(float,arr))
    
    return b-a

def cny_osk():
    arr = []
    count = 0
    
    arr_1 = []
    count_1 = 0
    while count < len(special_currency_uan_purs_osk()):
        arr.append(float(special_currency_uan_purs_osk()[count][2]))
        
        count += 1
        
    while count_1 < len(special_currency_uan_sell_osk()):
        arr_1.append(float(special_currency_uan_sell_osk()[count_1][2]))
        
        count_1 += 1    
    
    a = sum(map(float,arr_1))
    b = sum(map(float,arr))
    
    return b-a

def sqlite_for_adm_osk():
    conn = lite.connect('sql/Currency.db')
    cur = conn.cursor()
    with conn:
        cur.execute("""
            CREATE TABLE Currency_Osk(
                id integer primary key,
                day TEXT UNIQUE,
                rub varchar(100),
                usd varchar(100),
                eur varchar(100),
                gpb varchar(100),
                cny varchar(100)
            );    
        """)
    return cur.fetchall()

def existence_Osk():
    conn = lite.connect('sql/Currency.db')
    cur = conn.cursor()
    with conn:
        cur.execute(f'''
            select 
            case when exists 
                (select 1 from sqlite_master WHERE type='table' and name='Currency_Osk') 
                then 1 
                else 0         
            end
        ''')
    return cur.fetchall()

def insertsqlite_for_adm_osk():
    conn = lite.connect('sql/Currency.db')
    cur = conn.cursor()
    with conn:
        cur.execute("""
            INSERT INTO Currency_Osk (day,rub, usd, eur, gpb, cny) VALUES (?,?,?,?,?,?);    
        """, (datetime.now().strftime("%Y-%m-%d"),0, 0, 0, 0, 0))
    return cur.fetchall()

def updatetables_osk(
    day, rub, usd, eur, gpb, cny
):
    conn = lite.connect('sql/Currency.db')
    cur = conn.cursor()
    with conn:
        cur.execute(f'''
            UPDATE Currency_Osk SET rub = {rub}, usd = {usd}, eur = {eur}, gpb = {gpb}, cny = {cny} WHERE day = "{day}";
        ''')
    return cur.fetchall()

def oskar(day, currency):
    conn = lite.connect('sql/Currency.db')
    cur = conn.cursor()
    with conn:
        cur.execute(f'''
            select {currency} from Currency_Osk where day="{day}";
        ''')
    return cur.fetchall()