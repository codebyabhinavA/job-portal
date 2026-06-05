from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from jobs.models import Profile, Job
import datetime

class Command(BaseCommand):
    help = 'Seed sample data'

    def handle(self, *args, **kwargs):
        if Job.objects.exists():
            self.stdout.write('Data already exists, skipping.')
            return

        employer = User.objects.create_user(username='techcorp', email='hr@techcorp.com', password='test1234')
        Profile.objects.create(user=employer, role='employer', company_name='TechCorp Solutions', location='Bangalore')

        seeker = User.objects.create_user(username='johndoe', email='john@gmail.com', password='test1234')
        Profile.objects.create(user=seeker, role='seeker', skills='Python, Django, React', location='Bangalore')

        jobs = [
            {'title': 'Frontend Developer', 'description': 'Build responsive web applications using React and modern CSS frameworks.', 'requirements': 'React, HTML, CSS, JavaScript, 1+ years experience', 'location': 'Bangalore', 'job_type': 'full-time', 'salary': '4-7 LPA', 'deadline': datetime.date(2026, 7, 30)},
            {'title': 'Python Django Developer', 'description': 'Develop and maintain backend APIs using Django.', 'requirements': 'Python, Django, REST APIs, SQL, 2+ years experience', 'location': 'Remote', 'job_type': 'remote', 'salary': '6-10 LPA', 'deadline': datetime.date(2026, 7, 15)},
            {'title': 'UI/UX Designer', 'description': 'Design intuitive user interfaces for web and mobile apps.', 'requirements': 'Figma, Adobe XD, Prototyping, 1+ years experience', 'location': 'Mumbai', 'job_type': 'full-time', 'salary': '5-8 LPA', 'deadline': datetime.date(2026, 8, 1)},
            {'title': 'Data Analyst Intern', 'description': 'Analyse data and generate insights using Python and Excel.', 'requirements': 'Python, Pandas, Excel, SQL basics', 'location': 'Hyderabad', 'job_type': 'internship', 'salary': '15000/month', 'deadline': datetime.date(2026, 6, 30)},
            {'title': 'Full Stack Developer', 'description': 'Work on both frontend and backend of our SaaS product.', 'requirements': 'React, Node.js or Django, PostgreSQL, Git', 'location': 'Remote', 'job_type': 'remote', 'salary': '8-14 LPA', 'deadline': datetime.date(2026, 7, 20)},
            {'title': 'DevOps Engineer', 'description': 'Manage cloud infrastructure and CI/CD pipelines.', 'requirements': 'AWS, Docker, Jenkins, Linux, 2+ years experience', 'location': 'Bangalore', 'job_type': 'full-time', 'salary': '10-16 LPA', 'deadline': datetime.date(2026, 8, 10)},
        ]

        for j in jobs:
            Job.objects.create(employer=employer, **j)

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))