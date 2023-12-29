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
import psycopg2
import pandas as pd


def F_home(request):
    data = register.objects.values("en_no", "name", "attended")

    current_time = time.localtime()
    current_datetime = datetime.fromtimestamp(time.mktime(current_time))

    formatted_date = current_datetime.strftime("%d-%m-%Y")
    date_string = str(formatted_date)
    # ***************************************************************************************
    db_params = {
        "host": "127.0.0.1",
        "database": "Attendance system",
        "user": "postgres",
        "password": "1107",
        "port": "5432", 
    }

    try:
        with psycopg2.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                cursor.execute( """
                select * from attendance_system
                """)
                rows = cursor.fetchall()
                print(rows)

    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
    # ***************************************************************************************

    context = {
        "page": "Faculty",
        "data": data,
        "current_datetime": current_datetime,
    }
    return render(request, "F_index.html", context)


def download_excel_data(request):
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response[
        "Content-Disposition"
    ] = f'attachment; filename="{time.strftime("%d-%m-%Y")}.xlsx"'

    wb = Workbook()
    ws = wb.active

    columns = ["En_no", "Name", "Attended"]

    for col_num, column in enumerate(columns, 1):
        ws.cell(row=1, column=col_num, value=column)

    queryset = register.objects.all().values("en_no", "name", "attended")

    for row_num, row_data in enumerate(queryset, 2):
        ws.cell(row=row_num, column=1, value=row_data["en_no"])
        ws.cell(row=row_num, column=2, value=row_data["name"])
        ws.cell(row=row_num, column=3, value=row_data["attended"])

    wb.save(response)

    return response
