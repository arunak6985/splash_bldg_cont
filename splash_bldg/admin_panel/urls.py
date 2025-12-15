from django.urls import path
from . import views
from .pdf_views import generate_attendance_pdf

urlpatterns = [
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('admin-vacancy-management/', views.admin_vacancy_management, name='admin_vacancy_management'),
    path('job-applications/', views.job_applications, name='job_applications'),
    path('toggle-job-status/<int:job_id>/', views.toggle_job_status, name='toggle_job_status'),
    path('update-vacancy-count/<int:job_id>/', views.update_vacancy_count, name='update_vacancy_count'),
    path('create-job-vacancy/', views.create_job_vacancy, name='create_job_vacancy'),
    path('edit-job-vacancy/<int:job_id>/', views.edit_job_vacancy, name='edit_job_vacancy'),
    path('delete-job-vacancy/<int:job_id>/', views.delete_job_vacancy, name='delete_job_vacancy'),
    path('get-job-vacancy/<int:job_id>/', views.get_job_vacancy, name='get_job_vacancy'),
    
    # Configuration URLs
    path('job-titles/', views.job_titles, name='job_titles'),
    path('add-job-title/', views.add_job_title, name='add_job_title'),
    path('delete-job-title/<int:title_id>/', views.delete_job_title, name='delete_job_title'),
    path('locations/', views.locations, name='locations'),
    path('add-location/', views.add_location, name='add_location'),
    path('delete-location/<int:location_id>/', views.delete_location, name='delete_location'),
    
    # Attendance URLs
    path('attendance/', views.attendance, name='attendance'),
    path('attendance/delete/<int:record_id>/', views.delete_attendance_record, name='delete_attendance_record'),
    path('attendance/delete-bulk/', views.delete_attendance_bulk, name='delete_attendance_bulk'),
    path('attendance/pdf/<int:record_id>/', generate_attendance_pdf, name='generate_attendance_pdf'),
]