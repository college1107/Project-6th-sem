from django.shortcuts import render
from college_admin.models import *
from User.models import *
from datetime import datetime
from django.http import HttpResponse
from django.views import View
from pymongo import *
from openpyxl import Workbook
import time
import xlwt
import os
import pandas as pd


def F_home(request):
    data = register.objects.values("en_no", "name", "attended")

    current_time = time.localtime()
    current_datetime = datetime.fromtimestamp(time.mktime(current_time))

    formatted_date = current_datetime.strftime("%d-%m-%Y")
    date_string = str(formatted_date)
    # ***************************************************************************************




    
    # ***************************************************************************************


    context = {
        "page": "Faculty",
        "data": data,
        "current_datetime": current_datetime,
    }
    return render(request, "F_index.html", context)


def download_excel_data(request):
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = f'attachment; filename="{time.strftime("%d-%m-%Y")}.xlsx"'

    # Create a new workbook and add a worksheet
    wb = Workbook()
    ws = wb.active

    # Define column headers
    columns = ["En_no", "Name", "Attended"]

    # Write column headers to the worksheet
    for col_num, column in enumerate(columns, 1):
        ws.cell(row=1, column=col_num, value=column)

    # Fetch data from the register model
    queryset = register.objects.all().values("en_no", "name", "attended")

    # Write data to the worksheet
    for row_num, row_data in enumerate(queryset, 2):
        ws.cell(row=row_num, column=1, value=row_data["en_no"])
        ws.cell(row=row_num, column=2, value=row_data["name"])
        ws.cell(row=row_num, column=3, value=row_data["attended"])

    # Save the workbook to the response
    wb.save(response)

    return response
