from django.urls import path
from . import views
from .pdf_views import generate_attendance_pdf
from .bulk_pdf_views import generate_bulk_pdf
from .cheque_views import cheque_upload, process_cheque_upload
from .translate_views import pdf_translate, process_pdf_translate

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
    path('attendance/delete-all/', views.delete_all_attendance, name='delete_all_attendance'),
    path('attendance/pdf/<int:record_id>/', generate_attendance_pdf, name='generate_attendance_pdf'),
    path('attendance/bulk-pdf/', generate_bulk_pdf, name='generate_bulk_pdf'),
    
    # Cheque Upload URLs
    path('cheque-upload/', cheque_upload, name='cheque_upload'),
    path('process-cheque-upload/', process_cheque_upload, name='process_cheque_upload'),
    
    # PDF Translation URLs
    path('pdf-translate/', pdf_translate, name='pdf_translate'),
    path('process-pdf-translate/', process_pdf_translate, name='process_pdf_translate'),
]