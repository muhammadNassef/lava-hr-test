from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class AttendanceRecord(models.Model):
    attendance_states = [
        ('On-Time', 'On-Time'),
        ('Late-Entry', 'Late-Entry'),
        ('Early-Exit', 'Early-Exit'),
        ('Lateness', 'Lateness'),
        ('Absent', 'Absent')
    ]
    employee_ID = models.ForeignKey(
        User, related_name='user_attendance', on_delete=models.CASCADE)
    day_date = models.DateField(unique=False)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    attendance_status = models.CharField(
        choices=attendance_states, default='Absent', max_length=50)
    total_overtime = models.DurationField()
