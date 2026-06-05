from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [('seeker', 'Job Seeker'), ('employer', 'Employer')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    company_name = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Job(models.Model):
    JOB_TYPE_CHOICES = [('full-time','Full Time'),('part-time','Part Time'),('remote','Remote'),('internship','Internship')]
    employer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    salary = models.CharField(max_length=100, blank=True)
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_filled = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Application(models.Model):
    STATUS_CHOICES = [('pending','Pending'),('reviewed','Reviewed'),('accepted','Accepted'),('rejected','Rejected')]
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    cover_letter = models.TextField()
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.applicant.username} → {self.job.title}"