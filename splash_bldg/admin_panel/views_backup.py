from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from .models import JobTitle, Location, EmploymentType, AttendanceRecord
from site_application.models import JobVacancy, JobApplication
from functools import wraps
import pandas as pd
import calendar
from datetime import datetime

def custom_staff_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('admin_login')
        if not request.user.is_staff:
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@custom_staff_required
def admin_vacancy_management(request):
    """Admin-only view for managing job vacancies"""
    jobs = JobVacancy.objects.all().order_by('-created_at')
    
    # Calculate statistics
    active_jobs_count = jobs.filter(is_active=True).count()
    total_positions = sum(job.total_positions for job in jobs)
    available_positions = sum(job.available_positions for job in jobs)
    
    context = {
        'jobs': jobs,
        'active_jobs_count': active_jobs_count,
        'total_positions': total_positions,
        'available_positions': available_positions,
    }
    return render(request, 'admin_vacancy_management.html', context)

@custom_staff_required
def toggle_job_status(request, job_id):
    """Admin-only view to toggle job active status"""
    if request.method == 'POST':
        job = get_object_or_404(JobVacancy, id=job_id)
        job.is_active = not job.is_active
        job.save()
        status = "opened" if job.is_active else "closed"
        return JsonResponse({
            'success': True, 
            'message': f'Job "{job.title}" has been {status}.',
            'is_active': job.is_active
        })
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@custom_staff_required
def update_vacancy_count(request, job_id):
    """Admin-only view to update vacancy counts"""
    if request.method == 'POST':
        job = get_object_or_404(JobVacancy, id=job_id)
        total_positions = int(request.POST.get('total_positions', job.total_positions))
        filled_positions = int(request.POST.get('filled_positions', job.filled_positions))
        
        if filled_positions > total_positions:
            return JsonResponse({
                'success': False, 
                'message': 'Filled positions cannot exceed total positions.'
            })
        
        job.total_positions = total_positions
        job.filled_positions = filled_positions
        job.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Vacancy count updated for "{job.title}".',
            'available_positions': job.available_positions
        })
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@custom_staff_required
def create_job_vacancy(request):
    """Admin-only view to create new job vacancy"""
    if request.method == 'POST':
        job = JobVacancy(
            title=request.POST['title'],
            description=request.POST['description'],
            requirements=request.POST['requirements'],
            location=request.POST['location'],
            salary_range=request.POST.get('salary_range', ''),
            employment_type=request.POST['employment_type'],
            total_positions=int(request.POST.get('total_positions', 1)),
            is_active=request.POST.get('is_active') == 'on'
        )
        job.save()
        messages.success(request, f'Job vacancy "{job.title}" created successfully!')
        return redirect('admin_vacancy_management')
    
    job_titles = JobTitle.objects.all()
    locations = Location.objects.all()
    jobs = JobVacancy.objects.all().order_by('-created_at')
    return render(request, 'create_job_vacancy.html', {
        'job_titles': job_titles,
        'locations': locations,
        'jobs': jobs
    })

@custom_staff_required
def edit_job_vacancy(request, job_id):
    """Admin-only view to edit job vacancy"""
    job = get_object_or_404(JobVacancy, id=job_id)
    
    if request.method == 'POST':
        job.title = request.POST['title']
        job.description = request.POST['description']
        job.requirements = request.POST['requirements']
        job.location = request.POST['location']
        job.salary_range = request.POST.get('salary_range', '')
        job.employment_type = request.POST['employment_type']
        job.total_positions = int(request.POST.get('total_positions', 1))
        job.is_active = request.POST.get('is_active') == 'on'
        job.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Job vacancy "{job.title}" updated successfully!'
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@custom_staff_required
def delete_job_vacancy(request, job_id):
    """Admin-only view to delete job vacancy"""
    if request.method == 'POST':
        job = get_object_or_404(JobVacancy, id=job_id)
        job_title = job.title
        job.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Job vacancy "{job_title}" deleted successfully!'
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@custom_staff_required
def get_job_vacancy(request, job_id):
    """Admin-only view to get job vacancy details for editing"""
    job = get_object_or_404(JobVacancy, id=job_id)
    
    return JsonResponse({
        'success': True,
        'job': {
            'id': job.id,
            'title': job.title,
            'description': job.description,
            'requirements': job.requirements,
            'location': job.location,
            'salary_range': job.salary_range,
            'employment_type': job.employment_type,
            'total_positions': job.total_positions,
            'is_active': job.is_active
        }
    })

def admin_login(request):
    """Admin login page"""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_vacancy_management')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_vacancy_management')
        
        messages.error(request, 'Invalid credentials.')
    
    return render(request, 'admin_login.html')

def admin_logout(request):
    """Admin logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('admin_login')

@custom_staff_required
def job_applications(request):
    """Admin view for job applications"""
    from datetime import datetime, timedelta
    
    applications = JobApplication.objects.all().order_by('-applied_at')
    
    # Calculate statistics
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    
    today_applications = applications.filter(applied_at__date=today).count()
    week_applications = applications.filter(applied_at__date__gte=week_ago).count()
    unique_jobs = applications.values('job_vacancy').distinct().count()
    
    context = {
        'applications': applications,
        'today_applications': today_applications,
        'week_applications': week_applications,
        'unique_jobs': unique_jobs,
    }
    return render(request, 'job_applications.html', context)

@custom_staff_required
def job_titles(request):
    job_titles = JobTitle.objects.all()
    return render(request, 'job_titles.html', {'job_titles': job_titles})

@custom_staff_required
def add_job_title(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        if title:
            job_title, created = JobTitle.objects.get_or_create(name=title)
            if created:
                return JsonResponse({'success': True, 'message': 'Job title added successfully'})
            else:
                return JsonResponse({'success': False, 'message': 'Job title already exists'})
        return JsonResponse({'success': False, 'message': 'Title is required'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@custom_staff_required
def delete_job_title(request, title_id):
    if request.method == 'POST':
        try:
            job_title = get_object_or_404(JobTitle, id=title_id)
            job_title.delete()
            return JsonResponse({'success': True, 'message': 'Job title deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Error deleting job title'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@custom_staff_required
def locations(request):
    locations = Location.objects.all()
    return render(request, 'locations.html', {'locations': locations})

@custom_staff_required
def add_location(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            location, created = Location.objects.get_or_create(name=name)
            if created:
                return JsonResponse({'success': True, 'message': 'Location added successfully'})
            else:
                return JsonResponse({'success': False, 'message': 'Location already exists'})
        return JsonResponse({'success': False, 'message': 'Location name is required'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@custom_staff_required
def delete_location(request, location_id):
    if request.method == 'POST':
        try:
            location = get_object_or_404(Location, id=location_id)
            location.delete()
            return JsonResponse({'success': True, 'message': 'Location deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Error deleting location'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@custom_staff_required
def attendance(request):
    import openpyxl
    import json
    
    # Handle file upload with default values
    if request.method == 'POST' and request.FILES.get('excel_file'):
        try:
            excel_file = request.FILES['excel_file']
            month = request.POST.get('month', 'January')
            year = int(request.POST.get('year', datetime.now().year))
            
            # Default values
            default_p_value = request.POST.get('default_p', '8')
            default_ot_value = request.POST.get('default_ot', '2')
            
            # Read Excel file using pandas
            df = pd.read_excel(excel_file)
            employees_processed = 0
            
            for index, row in df.iterrows():
                try:
                    ref_no = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ''
                    name = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else ''
                    category = str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else ''
                    
                    if not ref_no or not name:
                        continue
                    
                    # Parse date fields
                    def parse_date(date_val):
                        if pd.isna(date_val) or date_val == '':
                            return None
                        try:
                            if isinstance(date_val, datetime):
                                return date_val.date()
                            date_str = str(date_val).strip()
                            if '/12025' in date_str:
                                date_str = date_str.replace('/12025', '/2025')
                            return pd.to_datetime(date_str, dayfirst=True).date()
                        except:
                            return None
                    
                    new_joining = parse_date(row.iloc[3]) if len(row) > 3 else None
                    duty_stop = parse_date(row.iloc[4]) if len(row) > 4 else None
                    re_joining = parse_date(row.iloc[5]) if len(row) > 5 else None
                    
                    # Process attendance data
                    attendance_data = {}
                    days_in_month = calendar.monthrange(year, ['January', 'February', 'March', 'April', 'May', 'June',
                                                               'July', 'August', 'September', 'October', 'November', 'December'].index(month) + 1)[1]
                    
                    for day in range(1, days_in_month + 1):
                        col_index = 5 + day
                        if col_index < len(row):
                            cell_value = row.iloc[col_index]
                            if pd.isna(cell_value) or str(cell_value).strip() == '':
                                attendance_data[str(day)] = default_p_value
                            else:
                                attendance_data[str(day)] = str(cell_value).strip().upper()
                        else:
                            attendance_data[str(day)] = default_p_value
                    
                    # Save to database
                    AttendanceRecord.objects.update_or_create(
                        ref_no=ref_no,
                        month=month,
                        year=year,
                        defaults={
                            'name': name,
                            'category': category,
                            'new_joining': new_joining,
                            'duty_stop': duty_stop,
                            're_joining': re_joining,
                            'attendance_data': attendance_data
                        }
                    )
                    employees_processed += 1
                    
                except Exception as e:
                    print(f"Error processing row {index}: {str(e)}")
                    continue
            
            return JsonResponse({
                'success': True,
                'message': f'Successfully processed {employees_processed} employees with P={default_p_value}, OT={default_ot_value} for {month} {year}',
                'count': employees_processed
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error processing file: {str(e)}'})
    
    # Get attendance records for display
    records = AttendanceRecord.objects.all().order_by('-uploaded_at')
    
    context = {
        'records': records,
        'months': ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December'],
        'years': range(2020, 2030),
        'days_range': range(1, 32)
    }
    return render(request, 'attendance.html', context)

@custom_staff_required
def delete_attendance_record(request, record_id):
    if request.method == 'POST':
        try:
            record = get_object_or_404(AttendanceRecord, id=record_id)
            record.delete()
            return JsonResponse({'success': True, 'message': 'Record deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@custom_staff_required
def delete_attendance_bulk(request):
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            record_ids = data.get('ids', [])
            
            if not record_ids:
                return JsonResponse({'success': False, 'message': 'No records selected'})
            
            deleted_count = AttendanceRecord.objects.filter(id__in=record_ids).delete()[0]
            return JsonResponse({
                'success': True, 
                'message': f'Successfully deleted {deleted_count} records'
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@custom_staff_required
def download_excel_template(request):
    """Generate and download Excel template for attendance upload"""
    import openpyxl
    from openpyxl.styles import Font, Alignment, PatternFill
    from io import BytesIO
    
    # Create workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Attendance Template"
    
    # Headers
    headers = ['REF.NO', 'NAME', 'CATEGORY', 'NEW JOINING', 'DUTY STOP', 'RE JOINING']
    
    # Add day columns (1-31)
    for day in range(1, 32):
        headers.append(str(day))
    
    # Write headers
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center')
        cell.fill = PatternFill(start_color='CCCCCC', end_color='CCCCCC', fill_type='solid')
    
    # Add sample data row
    sample_data = ['EMP001', 'John Doe', 'LABOUR', '01/01/2024', '', '']
    # Add empty cells for days (will use default P value)
    sample_data.extend([''] * 31)
    
    for col, value in enumerate(sample_data, 1):
        ws.cell(row=2, column=col, value=value)
    
    # Adjust column widths
    ws.column_dimensions['A'].width = 12
    ws.column_dimensions['B'].width = 20
    ws.column_dimensions['C'].width = 15
    ws.column_dimensions['D'].width = 15
    ws.column_dimensions['E'].width = 15
    ws.column_dimensions['F'].width = 15
    
    # Day columns
    for col in range(7, 38):
        ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 4
    
    # Save to BytesIO
    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    
    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="attendance_template.xlsx"'
    return response

@custom_staff_required
def excel_template_page(request):
    """Show Excel template download page"""
    return render(request, 'excel_template_download.html')