from django.shortcuts import render
from college_admin.models import *
from User.models import *
from datetime import datetime
from django.http import HttpResponse
from django.views import View
import time
import xlwt
import pandas as pd


def F_home(request):
    data = register.objects.values("en_no", "name", "attended")

    current_time = time.localtime()
    current_datetime = datetime.fromtimestamp(time.mktime(current_time))

    context = {
        "page": "Faculty",
        "data": data,
        "current_datetime": current_datetime,
    }
    return render(request, "F_index.html", context)


def download_excel_data(request):
    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = f'attachment; filename="{time.strftime("%d-%m-%Y")}.xls"'
    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet("sheet1")
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ["En_no", "Name", "Attended"]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()

    queryset = register.objects.all()
    data = list(queryset.values())
    df = pd.DataFrame(data)

    for index, my_row in df.iterrows():
        row_num += 1
        ws.write(row_num, 0, my_row["en_no"], font_style)
        ws.write(row_num, 1, my_row["name"], font_style)
        ws.write(row_num, 2, my_row["attended"], font_style)

    wb.save(response)
    return response
