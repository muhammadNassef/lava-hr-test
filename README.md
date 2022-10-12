# lava-hr-test

Description: HRAttendnace module

Database Models:
- Django User Built-in model for Employee Register and login.
- AttendanceRecord custom model for logging employee check in/out
- AttendanceRecord Model Description:
    - employee_id: ForeignKey to represent one-to-many relationship with User Model
    - day_date: Date field to track log day date
    - check_in / check_out: DateTime Fields to store employee check_in / check_out
    - attendance_status: Charfield with some options ('On-Time', 'Late-Entry', 'Early-Exit', 'Lateness') to represt employee attendance status, default (Absent)
    - total_overtime: DurationField To represent total overtime working hours for employee, default (0)
    
    
Dependencies & configurations needed to run the code:
- you can try the live version using provided APIs, (sent via Email)
- to run the code locally:
    - setup mysql database and provide the authentication data through settings.py file
 
