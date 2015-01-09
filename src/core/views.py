from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator

from core.models import Certificate, Course, Student


class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


@login_required
def home(request):
    return render(request, 'core/home.html')


class StudentView(LoginRequiredMixin, ListView):
    model = Student
    context_object_name = 'students'


class StudentCreate(LoginRequiredMixin, CreateView):
    model = Student
    success_url = '/alunos'


class StudentUpdate(LoginRequiredMixin, UpdateView):
    model = Student
    success_url = '/alunos'


class StudentDelete(LoginRequiredMixin, DeleteView):
    model = Student
    context_object_name = 'student'
    success_url = '/alunos'


class CourseView(LoginRequiredMixin, ListView):
    model = Course
    context_object_name = 'courses'


class CourseCreate(LoginRequiredMixin, CreateView):
    model = Course
    success_url = '/cursos'


class CourseUpdate(LoginRequiredMixin, UpdateView):
    model = Course
    success_url = '/cursos'


class CourseDelete(LoginRequiredMixin, DeleteView):
    model = Course
    context_object_name = 'course'
    success_url = '/cursos'


class CertificateView(LoginRequiredMixin, ListView):
    model = Certificate
    context_object_name = 'certificates'
