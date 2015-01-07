from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import ListView
from django.utils.decorators import method_decorator

from core.models import Student


@login_required
def home(request):
    return render(request, 'core/home.html')


class StudentView(ListView):
    model = Student
    context_object_name = 'students'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StudentView, self).dispatch(*args, **kwargs)
