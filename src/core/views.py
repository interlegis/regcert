from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from core.models import Student


@login_required
def home(request):
    return render(request, 'core/home.html')


@login_required
def students(request):
    students = Student.objects.all()
    context = {
        'students': students
    }
    return render(request, 'core/students.html', context)
