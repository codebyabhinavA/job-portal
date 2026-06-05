from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, Job, Application

def home(request):
    jobs = Job.objects.filter(is_filled=False).order_by('-created_at')
    keyword = request.GET.get('keyword', '')
    location = request.GET.get('location', '')
    job_type = request.GET.get('job_type', '')
    if keyword:
        jobs = jobs.filter(title__icontains=keyword)
    if location:
        jobs = jobs.filter(location__icontains=location)
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    return render(request, 'home.html', {'jobs': jobs, 'keyword': keyword, 'location': location, 'job_type': job_type})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('register')
        user = User.objects.create_user(username=username, email=email, password=password)
        Profile.objects.create(user=user, role=role)
        login(request, user)
        return redirect('home')
    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Invalid credentials.')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    already_applied = False
    if request.user.is_authenticated:
        already_applied = Application.objects.filter(job=job, applicant=request.user).exists()
    return render(request, 'job_detail.html', {'job': job, 'already_applied': already_applied})

@login_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        cover_letter = request.POST['cover_letter']
        Application.objects.create(job=job, applicant=request.user, cover_letter=cover_letter)
        messages.success(request, 'Application submitted successfully!')
        return redirect('seeker_dashboard')
    return render(request, 'apply.html', {'job': job})

@login_required
def seeker_dashboard(request):
    applications = Application.objects.filter(applicant=request.user).order_by('-applied_at')
    return render(request, 'seeker_dashboard.html', {'applications': applications})

@login_required
def employer_dashboard(request):
    jobs = Job.objects.filter(employer=request.user).order_by('-created_at')
    return render(request, 'employer_dashboard.html', {'jobs': jobs})

@login_required
def post_job(request):
    if request.method == 'POST':
        Job.objects.create(
            employer=request.user,
            title=request.POST['title'],
            description=request.POST['description'],
            requirements=request.POST['requirements'],
            location=request.POST['location'],
            job_type=request.POST['job_type'],
            salary=request.POST.get('salary', ''),
            deadline=request.POST['deadline'],
        )
        messages.success(request, 'Job posted successfully!')
        return redirect('employer_dashboard')
    return render(request, 'post_job.html')

@login_required
def edit_job(request, pk):
    job = get_object_or_404(Job, pk=pk, employer=request.user)
    if request.method == 'POST':
        job.title = request.POST['title']
        job.description = request.POST['description']
        job.requirements = request.POST['requirements']
        job.location = request.POST['location']
        job.job_type = request.POST['job_type']
        job.salary = request.POST.get('salary', '')
        job.deadline = request.POST['deadline']
        job.save()
        messages.success(request, 'Job updated successfully!')
        return redirect('employer_dashboard')
    return render(request, 'edit_job.html', {'job': job})

@login_required
def delete_job(request, pk):
    job = get_object_or_404(Job, pk=pk, employer=request.user)
    job.delete()
    messages.success(request, 'Job deleted.')
    return redirect('employer_dashboard')

@login_required
def mark_filled(request, pk):
    job = get_object_or_404(Job, pk=pk, employer=request.user)
    job.is_filled = True
    job.save()
    return redirect('employer_dashboard')

@login_required
def profile(request):
    prof = request.user.profile
    if request.method == 'POST':
        prof.phone = request.POST.get('phone', '')
        prof.location = request.POST.get('location', '')
        prof.bio = request.POST.get('bio', '')
        prof.skills = request.POST.get('skills', '')
        prof.company_name = request.POST.get('company_name', '')
        prof.website = request.POST.get('website', '')
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.save()
        prof.save()
        messages.success(request, 'Profile updated!')
        return redirect('profile')
    return render(request, 'profile.html', {'prof': prof})