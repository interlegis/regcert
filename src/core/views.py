from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator

from core.forms import StudentForm, StudentCoursesForm
from core.models import Certificate, Course, Enrollment, Student


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


class StudentCreate(View):

    def get(self, request):
        student_form = StudentForm(prefix='student')
        student_courses_form = StudentCoursesForm(prefix='student_courses')

        context = {
            'student_form': student_form,
            'student_courses_form': student_courses_form
        }
        return render(request, 'core/student_create.html', context)

    def post(self, request):
        student_form = StudentForm(request.POST, prefix='student')
        student_courses_form = StudentCoursesForm(request.POST,
                                                  prefix='student_courses')

        if student_form.is_valid() and student_courses_form.is_valid():
            student = student_form.save()
            data = student_courses_form.clean()
            for course in data['courses']:

                c = Enrollment(
                    student=student,
                    course=course
                )
                c.save()
            return HttpResponseRedirect('/alunos')
        else:
            context = {
                'student_form': student_form,
                'student_courses_form': student_courses_form
            }
        return render(request, 'core/student_create.html', context)


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


class CertificateCreate(LoginRequiredMixin, CreateView):
    model = Certificate
    success_url = '/certificados'


class CertificateUpdate(LoginRequiredMixin, UpdateView):
    model = Certificate
    success_url = '/certificados'


class CertificateDelete(LoginRequiredMixin, DeleteView):
    model = Certificate
    context_object_name = 'certificate'
    success_url = '/certificados'
