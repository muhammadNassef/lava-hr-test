from django.urls import path
from . import views


urlpatterns = [
    path('employee-sign-up/', views.create_new_employee),
    path('employee-sign-in/', views.employee_log_in),
    path('create-new-employee-attendance-record/',
         views.create_new_employee_attendance_record),
    path('get-employee-attendance-records/',
         views.get_all_employee_attendance_records),
    path('get-employees-attendance-records/',
         views.get_all_employees_attendance_records),

]
