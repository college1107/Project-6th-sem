from django.shortcuts import render
from college_admin.models import *
from User.models import *
from datetime import datetime
from django.http import HttpResponse
from django.views import View
from pymongo import *
from faculty.utils import *
from django.contrib import messages
import time
from io import BytesIO

current_time = time.localtime()
current_datetime = datetime.fromtimestamp(time.mktime(current_time))
formatted_date = current_datetime.strftime("%Y-%m-%d")


def Add_Attendance_to_postgres(date):
    data = FetchColumn("attendance_system", "en_no")
    for en in data:
        register_instance = register.objects.get(en_no=en[0])
        attendance_data = register_instance.attended
        row_column(attendance_data, en[0], date)


def F_home(request):
    data = register.objects.values("en_no", "name", "attended")
    context = {
        "page": "Faculty",
        "data": data,
        "current_datetime": current_datetime,
    }
    date = ""
    if request.method == "POST":
        date = request.POST.get("date")
        if not date:
            messages.success(request, "Please add Date")
            context.update({"color": "danger"})
            return render(request, "F_index.html", context)

    # ***************************************************************************************
    # DropColumn('attendance_system','2024-01-01')
    # Truncate_column('attendance_system',date)
    if data:
        AddData(data)
    if date:
        CreateColumn("attendance_system", date, "BOOLEAN")
        Add_Attendance_to_postgres(date)
    # ***************************************************************************************
    return render(request, "F_index.html", context)


def download_excel_data():
    query = "SELECT * FROM attendance_system"
    data_frame = fetch_data_from_postgres(db_params, query)
    excel_data = BytesIO()
    data_frame.to_excel(excel_data, index=False, engine="openpyxl")
    excel_data.seek(0)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f"attachment; filename={formatted_date}.xlsx"
    response.write(excel_data.read())

    return response

def SetFalse():
   pass