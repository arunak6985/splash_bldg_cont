from django.db import models
from django.utils import timezone

class JobVacancy(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=100)
    salary_range = models.CharField(max_length=100, blank=True)
    employment_type = models.CharField(max_length=50, choices=[
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
    ], default='full_time')
    is_active = models.BooleanField(default=True)
    total_positions = models.IntegerField(default=1, help_text="Total number of positions available")
    filled_positions = models.IntegerField(default=0, help_text="Number of positions filled")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def available_positions(self):
        return self.total_positions - self.filled_positions
    
    @property
    def is_fully_filled(self):
        return self.filled_positions >= self.total_positions

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class JobApplication(models.Model):
    job_vacancy = models.ForeignKey(JobVacancy, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True)
    experience_years = models.IntegerField()
    applied_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.full_name} - {self.job_vacancy.title}"

    class Meta:
        ordering = ['-applied_at']

class JobTitle(models.Model):
    title = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']

class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']
