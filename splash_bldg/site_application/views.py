from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import JobVacancy, JobApplication, Contact

def home(request):
    if request.method == 'POST':
        contact = Contact(
            name=request.POST['name'],
            email=request.POST['email'],
            subject=request.POST['subject'],
            message=request.POST['message']
        )
        contact.save()
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('home')
    
    return render(request, 'site_application/home.html')

def careers(request):
    job_vacancies = JobVacancy.objects.filter(is_active=True)
    return render(request, 'site_application/careers.html', {'job_vacancies': job_vacancies})

def apply_job(request, job_id):
    job = get_object_or_404(JobVacancy, id=job_id, is_active=True)
    
    # Check if job is fully filled
    if job.is_fully_filled:
        messages.error(request, 'Sorry, this position is currently filled. Please check other available positions.')
        return redirect('careers')
    
    if request.method == 'POST':
        application = JobApplication(
            job_vacancy=job,
            full_name=request.POST['full_name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            resume=request.FILES['resume'],
            cover_letter=request.POST.get('cover_letter', ''),
            experience_years=request.POST['experience_years']
        )
        application.save()
        messages.success(request, 'Your application has been submitted successfully!')
        return redirect('careers')
    
    return render(request, 'site_application/apply_job.html', {'job': job})