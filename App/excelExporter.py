import xlsxwriter
from datetime import datetime
from xlsx2html import xlsx2html
from ftfy import fix_encoding

from .crud import getPost

def excelExporter(
    
):
    workbook = xlsxwriter.Workbook(f'./Layout/results {datetime.now().strftime("%m.%d")}.xlsx')
    worksheet = workbook.add_worksheet()
    # Field open a day with prices
    worksheet.write(0, 0, "Дата")
    worksheet.write(0, 1, datetime.now().strftime("%Y/%m/%d"))

    currencyDefine = [
        "RUB", "USD", "EURO", "GPB", "CNY", "Тенге"
    ]
    TheActions = [
        "Объем", "Курс", "Цена операции", "Объем", "Курс", "Цена операции", " ", " ", " "
    ]

    count = 2
    while count <= len(currencyDefine)+1:
        worksheet.write(0, count, currencyDefine[count-2])
            
        count += 1
        
    merge_format = workbook.add_format({
        'bold': 1,
        'align': 'center',
        'valign': 'vcenter',
    })

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


    for deals in range(len(getPost())):
        if getPost()[deals][1] == "Рубль":
            productionPurchesorSell = lambda dataofexcel: ( 
            worksheet.write(9+incres, 0, incres+1), 
            worksheet.write(9+incres, 1, getPost()[deals][2]), 
            worksheet.write(9+incres, 2, getPost()[deals][5]), 
            worksheet.write(9+incres, 3, getPost()[deals][6]),
            worksheet.write(9+incres, 8, getPost()[deals][7]),
            worksheet.write(9+incres, 7, getPost()[deals][8])
            ) if (dataofexcel == "Покупка") else (
            worksheet.write(9+incres, 0, incres+1), 
            worksheet.write(9+incres, 4, getPost()[deals][2]), 
            worksheet.write(9+incres, 5, getPost()[deals][5]), 
            worksheet.write(9+incres, 6, getPost()[deals][6]),
            worksheet.write(9+incres, 8, getPost()[deals][7]),
            worksheet.write(9+incres, 7, getPost()[deals][8])
            )
            productionPurchesorSell(getPost()[deals][3])
            incres += 1
            
        elif getPost()[deals][1] == "Доллар":
            productionPurchesorSell = lambda dataofexcel: ( 
            worksheet.write(9+incresA, 0, incresA+1), 
            worksheet.write(9+incresA, 1+9, getPost()[deals][2]), 
            worksheet.write(9+incresA, 2+9, getPost()[deals][5]), 
            worksheet.write(9+incresA, 3+9, getPost()[deals][6]),
            worksheet.write(9+incresA, 8+9, getPost()[deals][7]),
            worksheet.write(9+incresA, 7+9, getPost()[deals][8])
            ) if (dataofexcel == "Покупка") else (
            worksheet.write(9+incresA, 0, incresA+1), 
            worksheet.write(9+incresA, 4+9, getPost()[deals][2]), 
            worksheet.write(9+incresA, 5+9, getPost()[deals][5]), 
            worksheet.write(9+incresA, 6+9, getPost()[deals][6]),
            worksheet.write(9+incresA, 8+9, getPost()[deals][7]),
            worksheet.write(9+incresA, 7+9, getPost()[deals][8])
            )
            productionPurchesorSell(getPost()[deals][3])
            incresA += 1
        elif getPost()[deals][1] == "Евро":
            productionPurchesorSell = lambda dataofexcel: ( 
            worksheet.write(9+incresB, 0, incresB+1), 
            worksheet.write(9+incresB, 1+9*2, getPost()[deals][2]), 
            worksheet.write(9+incresB, 2+9*2, getPost()[deals][5]), 
            worksheet.write(9+incresB, 3+9*2, getPost()[deals][6]),
            worksheet.write(9+incresB, 8+9*2, getPost()[deals][7]),
            worksheet.write(9+incresB, 7+9*2, getPost()[deals][8])
            ) if (dataofexcel == "Покупка") else (
            worksheet.write(9+incresB, 0, incresB+1), 
            worksheet.write(9+incresB, 4+18, getPost()[deals][2]), 
            worksheet.write(9+incresB, 5+18, getPost()[deals][5]), 
            worksheet.write(9+incresB, 6+18, getPost()[deals][6]),
            worksheet.write(9+incresB, 8+18, getPost()[deals][7]),
            worksheet.write(9+incresB, 7+9*2, getPost()[deals][8])
            )
            productionPurchesorSell(getPost()[deals][3])
            incresB += 1
        elif getPost()[deals][1] == "Фунт":
            productionPurchesorSell = lambda dataofexcel: ( 
            worksheet.write(9+incresC, 0, incresC+1), 
            worksheet.write(9+incresC, 1+27, getPost()[deals][2]), 
            worksheet.write(9+incresC, 2+27, getPost()[deals][5]), 
            worksheet.write(9+incresC, 3+27, getPost()[deals][6]),
            worksheet.write(9+incresC, 8+27, getPost()[deals][7]),
            worksheet.write(9+incresC, 7+27, getPost()[deals][8])
            ) if (dataofexcel == "Покупка") else (
            worksheet.write(9+incresC, 0, incresC+1), 
            worksheet.write(9+incresC, 4+27, getPost()[deals][2]), 
            worksheet.write(9+incresC, 5+27, getPost()[deals][5]), 
            worksheet.write(9+incresC, 6+27, getPost()[deals][6]),
            worksheet.write(9+incresC, 8+27, getPost()[deals][7]),
            worksheet.write(9+incresC, 7+27, getPost()[deals][8])
            )
            productionPurchesorSell(getPost()[deals][3])
            incresC += 1
        else: 
            productionPurchesorSell = lambda dataofexcel: ( 
            worksheet.write(9+incresD, 0, incresD+1), 
            worksheet.write(9+incresD, 1+36, getPost()[deals][2]), 
            worksheet.write(9+incresD, 2+36, getPost()[deals][5]), 
            worksheet.write(9+incresD, 3+36, getPost()[deals][6]),
            worksheet.write(9+incresD, 8+36, getPost()[deals][7]),
            worksheet.write(9+incresD, 7+36, getPost()[deals][8])
            ) if (dataofexcel == "Покупка") else (
            worksheet.write(9+incresD, 0, incresD+1), 
            worksheet.write(9+incresD, 4+36, getPost()[deals][2]), 
            worksheet.write(9+incresD, 5+36, getPost()[deals][5]), 
            worksheet.write(9+incresD, 6+36, getPost()[deals][6]),
            worksheet.write(9+incresD, 8+36, getPost()[deals][7]),
            worksheet.write(9+incresD, 7+36, getPost()[deals][8])
            )
            productionPurchesorSell(getPost()[deals][3])
            incresD += 1

    workbook.close()
    
def htmlExporter():
    xlsx2html(f'./Layout/results {datetime.now().strftime("%m.%d")}.xlsx'.decode('utf8'), f'results {datetime.now().strftime("%m.%d")}.html'.decode('utf8'))
    
     
