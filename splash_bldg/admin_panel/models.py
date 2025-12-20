from django.db import models
from django.utils import timezone

class JobTitle(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Location(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class EmploymentType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class AttendanceRecord(models.Model):
    ref_no = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    new_joining = models.DateField(null=True, blank=True)
    duty_stop = models.DateField(null=True, blank=True)
    re_joining = models.DateField(null=True, blank=True)
    month = models.CharField(max_length=20)
    year = models.IntegerField()
    attendance_data = models.JSONField()  # Store daily attendance as JSON
    uploaded_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.ref_no} - {self.name} - {self.month} {self.year}"
    
    class Meta:
        ordering = ['-uploaded_at', 'ref_no']
        unique_together = ['ref_no', 'month', 'year']

class Supervisor(models.Model):
    employee_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    mobile_number = models.CharField(max_length=20)
    site_location = models.CharField(max_length=200)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.employee_id} - {self.name}"
    
    class Meta:
        ordering = ['employee_id']

class EmployeeAttendance(models.Model):
    ref_no = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    joining_date = models.DateField(null=True, blank=True)
    rejoining_date = models.DateField(null=True, blank=True)
    month = models.CharField(max_length=20)
    year = models.IntegerField()
    attendance_data = models.JSONField()  # Store daily attendance as JSON
    uploaded_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.ref_no} - {self.name} - {self.month} {self.year}"
    
    class Meta:
        ordering = ['-uploaded_at', 'ref_no']
        unique_together = ['ref_no', 'month', 'year']