from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
import json
from flask import Flask

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# TO-DO ~> 1. Make better (❌)
class database():
    # mechanism of data collection
    @app.post('/Name')
    async def content(sum: int=Form(...), currency: int=Form(...), res: int=Form(...), exchange: int=Form(...), comment: str=Form(...)): 
        datas = {'sum':sum, 'currency':currency, 'res':res, 'exchange':exchange, 'comment':comment}
        datatable = json.dumps(datas)
        with open('test.json', 'w') as f:
            info = f.write(datatable)
            
        return datas

    # Submition 
    @app.get('/ending')
    def ending(request: Request):
        context = {'request':request, 'date':datetime.now().strftime("%H:%M"),'dateandtime': datetime.now().strftime("%c")}
        return templates.TemplateResponse('endingSection.html', context)

@app.get('/report')
def report(request: Request):
    context = {'request':request, 'date':datetime.now().strftime("%H:%M"),'dateandtime': datetime.now().strftime("%c")}
    return templates.TemplateResponse('report.html', context)

# TO-DO ~> 1. a table (❌)
@app.get('/history')
def history(request: Request):
    with open('test.json', 'r') as file:
        info = json.load(file)
        print(info)
    
    context = {'request':request, 'date':datetime.now().strftime("%H:%M"),'dateandtime': datetime.now().strftime("%c"),'sum':info['sum'],'currency':info['currency'], 'res':info['res'], 'exchange':info['exchange'], 'comment':info['comment']}
    return templates.TemplateResponse('history.html', context)

@app.get('/Name', response_class=HTMLResponse)
def content(request: Request):
    
    context = {'request':request, 'date':datetime.now().strftime("%H:%M"), 'dateandtime': datetime.now().strftime("%c")}
    return templates.TemplateResponse('deal.html', context)   

# sign in & up form
@app.get('/')
def login(request: Request):
    context = {'request':request, 'date':datetime.now().strftime("%H:%M"), 'dateandtime': datetime.now().strftime("%c")}
    return templates.TemplateResponse('index.html', context)

@app.get('/registration')
def reg(request: Request):
    context = {'request':request, 'date':datetime.now().strftime("%H:%M"), 'dateandtime': datetime.now().strftime("%c")}
    return templates.TemplateResponse('reg.html', context)