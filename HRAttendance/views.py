from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, login
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from dateutil import parser
import calendar


@csrf_exempt
def create_new_employee(request):
    if request.method == "POST":
        try:
            body_unicode = eval(request.body.decode('utf-8'))
            user = User.objects.create_user(body_unicode['username'], body_unicode['email'],
                                            body_unicode['password'],
                                            is_superuser=body_unicode['is_superuser'])
            if user:
                return HttpResponse(f"Employee Sign Up Done, use username: {body_unicode['username']}, pass: {body_unicode['password']}, to login!!")
            else:
                return HttpResponse("Cannot Sign Up Employee, check your data again!!")
        except Exception as ex:
            return HttpResponse(f"Cannot Sign Up Employee, {ex}")


@csrf_exempt
def employee_log_in(request):
    if request.method == "POST":
        try:
            body_unicode = eval(request.body.decode('utf-8'))
            username = body_unicode['username']
            password = body_unicode['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse(f"""username: {username}, logged in Successfully""")
            else:
                return HttpResponse("check your data again!!")
        except Exception as ex:
            return HttpResponse(f"check your data again!!, {ex}")


@csrf_exempt
def create_new_employee_attendance_record(request):
    if request.method == "POST":
        try:
            if request.user.is_authenticated:
                body_unicode = eval(request.body.decode('utf-8'))
                check_in_time = parser.parse(body_unicode["check_in"])
                check_out_time = parser.parse(body_unicode["check_out"])

                if check_out_time.time() < check_in_time.time():
                    return HttpResponse("Check-out can't be before check-in")
                elif check_out_time.time() == check_in_time.time():
                    return HttpResponse("Check-out can't equal check-in")
                elif AttendanceRecord.objects.filter(employee_ID=request.user, day_date=datetime.now().date()):
                    return HttpResponse("Employee Attendance Record Already Found!!")
                else:
                    employee_attendance_status = check_if_employee_has_lateness(
                        check_in_time, check_out_time)
                    employee_total_overtime = check_if_employee_has_overtime(
                        check_in_time, check_out_time)
                    new_employee_attendance_record = AttendanceRecord.objects.create(employee_ID=request.user,
                                                                                     day_date=datetime.now().date(),
                                                                                     check_in=check_in_time,
                                                                                     check_out=check_out_time,
                                                                                     attendance_status=employee_attendance_status,
                                                                                     total_overtime=employee_total_overtime
                                                                                     )
                    if new_employee_attendance_record:
                        return HttpResponse(f"New Employee Attendance Record for day: {datetime.now().date()}, Created Successfully")
            else:
                return HttpResponse("You Should Login First!!")
        except Exception as ex:
            return HttpResponse(f"Can Not Create New Employee Attendance Record, {ex}")


def check_if_employee_has_lateness(check_in_time, check_out_time):
    attendance_status = "Absent"
    shift_start = parser.parse("2022-10-12T09:00:00")
    shift_end = parser.parse("2022-10-12T17:00:00")

    if check_in_time.time() > shift_start.time():
        attendance_status = "Late-Entry"
        if check_out_time.time() < shift_end.time():
            attendance_status = "Lateness"
    elif check_out_time.time() < shift_end.time():
        attendance_status = "Early-Exit"
    else:
        attendance_status = "On-Time"
    return attendance_status


def check_if_employee_has_overtime(check_in_time, check_out_time):
    total_overtime_in_sec = 0
    day_name = calendar.day_name[datetime.now().date().weekday()]
    if day_name == "Friday" or day_name == "Saturday":
        total_overtime_in_sec += (time_to_seconds(check_out_time.time()
                                                  ) - time_to_seconds(check_in_time.time()))
    else:
        total_working_hrs_in_sec = time_to_seconds(
            check_out_time.time()) - time_to_seconds(check_in_time.time())
        if total_working_hrs_in_sec > 28800:
            total_overtime_in_sec += (total_working_hrs_in_sec - 28800)
    return timedelta(seconds=total_overtime_in_sec)


def time_to_seconds(time):
    """Convert a datetime.time to seconds since midnight"""
    if time is None:
        return None
    return 3600 * time.hour + 60 * time.minute + time.second


@csrf_exempt
def get_all_employee_attendance_records(request):
    if request.method == "GET":
        try:
            if request.user.is_authenticated:
                all_employee_attendance_records = AttendanceRecord.objects.filter(
                    employee_ID=request.user)
                if all_employee_attendance_records:
                    json_data = {}
                    for record in all_employee_attendance_records:
                        json_data[str(record.day_date)] = {"employee_username": str(record.employee_ID),
                                                           "check_in": record.check_in,
                                                           "check_out": record.check_out,
                                                           "attendance_status": record.attendance_status,
                                                           "total_overtime": record.total_overtime
                                                           }
                    return JsonResponse(json_data)
            else:
                return HttpResponse("You Should Login First!!")
        except Exception as ex:
            return HttpResponse(ex)


@csrf_exempt
def get_all_employees_attendance_records(request):
    if request.method == "GET":
        try:
            if request.user.is_authenticated:
                if request.user.is_superuser:
                    all_employees_attendance_records = AttendanceRecord.objects.all()
                    if all_employees_attendance_records:
                        json_data = {}
                        for record in all_employees_attendance_records:
                            json_data[str(record.employee_ID)] = {
                                "day_date": str(record.day_date),
                                "check_in": record.check_in,
                                "check_out": record.check_out,
                                "attendance_status": record.attendance_status,
                                "total_overtime": record.total_overtime
                            }
                        return JsonResponse(json_data)
                else:
                    return HttpResponse("You dont have permission!!")
            else:
                return HttpResponse("You Should Login First!!")
        except Exception as ex:
            return HttpResponse(f"non superuser {ex}")
