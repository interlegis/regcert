from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.utils.decorators import method_decorator

from core.forms import InvalidateCertificateForm, StudentForm, StudentCoursesForm
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
    paginate_by = 10
    template_name = 'core/student/list.html'


class StudentCreate(View):

    def get(self, request):
        student_form = StudentForm(prefix='student')
        courses_form = StudentCoursesForm(prefix='courses')

        context = {
            'student_form': student_form,
            'courses_form': courses_form
        }
        return render(request, 'core/student/create.html', context)

    def post(self, request):
        student_form = StudentForm(request.POST, prefix='student')
        courses_form = StudentCoursesForm(request.POST,
                                                  prefix='courses')

        if student_form.is_valid() and courses_form.is_valid():
            student = student_form.save()
            data = courses_form.clean()
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
                'courses_form': courses_form
            }
        return render(request, 'core/student/create.html', context)


class StudentUpdate(View):

    def get(self, request, pk):

        student = Student.objects.get(id=pk)
        student_form = StudentForm(initial={
            'name': student.name,
            'birthday': student.birthday,
            'nationality': student.nationality,
            'rg': student.rg
        }, prefix='student')

        enrollments = Enrollment.objects.filter(student=student)
        courses_form = StudentCoursesForm(initial={
            'courses': [e.course.id for e in enrollments]
        }, prefix='student_courses')

        context = {
            'student_form': student_form,
            'courses_form': courses_form
        }
        return render(request, 'core/student/edit.html', context)

    def post(self, request, pk):
        student = get_object_or_404(Student, pk=pk)

        student_form = StudentForm(request.POST, prefix='student',
                                   instance=student)
        courses_form = StudentCoursesForm(request.POST,
                                          prefix='student_courses')

        if student_form.is_valid() and courses_form.is_valid():
            student_form.save()

            enrollments = Enrollment.objects.filter(student=student)
            courses = [e.course for e in enrollments]
            courses_form = courses_form.clean()

            to_enroll = list(set(courses_form['courses']) - set(courses))
            to_un_enroll = list(set(courses) - set(courses_form['courses']))

            for course in to_enroll:
                e = Enrollment(student=student, course=course)
                e.save()

            for course in to_un_enroll:
                e = Enrollment.objects.get(student=student, course=course)
                e.delete()

            return HttpResponseRedirect('/alunos')
        else:
            context = {
                'student_form': student_form,
                'courses_form': courses_form
            }
        return render(request, 'core/student/edit.html', context)


class StudentDelete(LoginRequiredMixin, DeleteView):
    model = Student
    context_object_name = 'student'
    template_name = 'core/student/confirm_delete.html'
    success_url = '/alunos'

    def get_context_data(self, **kwargs):
        context = super(StudentDelete, self).get_context_data(**kwargs)
        context['enrollments'] = Enrollment.objects.filter(student=self.object)
        return context


class CourseView(LoginRequiredMixin, ListView):
    model = Course
    context_object_name = 'courses'
    template_name = 'core/course/list.html'


class CourseCreate(LoginRequiredMixin, CreateView):
    model = Course
    success_url = '/cursos'
    template_name = 'core/course/form.html'


class CourseUpdate(LoginRequiredMixin, UpdateView):
    model = Course
    success_url = '/cursos'
    template_name = 'core/course/form.html'


class CourseDelete(LoginRequiredMixin, DeleteView):
    model = Course
    context_object_name = 'course'
    template_name_suffix = '/confirm_delete'
    success_url = '/cursos'

    def get_context_data(self, **kwargs):
        context = super(CourseDelete, self).get_context_data(**kwargs)
        context['enrollments'] = Enrollment.objects.filter(course=self.object)
        return context


class CertificateView(LoginRequiredMixin, ListView):
    model = Certificate
    context_object_name = 'certificates'
    template_name = 'core/certificate/list.html'


class CertificateCreate(LoginRequiredMixin, CreateView):
    model = Certificate
    fields = ['enrollment', 'book_number', 'book_sheet', 'book_date',
        'book_date', 'process_number', 'executive_director',
        'educational_secretary']
    template_name = 'core/certificate/create.html'
    success_url = '/certificados'


class CertificateDetail(LoginRequiredMixin, ListView):
    context_object_name = 'certificate'
    template_name = 'core/certificate/detail.html'
    InvalidateCertificateForm

    def get_queryset(self):
        certificate = get_object_or_404(Certificate, id=self.kwargs['pk'])
        return certificate


class CertificateInvalidate(LoginRequiredMixin, FormView):
    form_class = InvalidateCertificateForm
    template_name = 'core/certificate/invalidate.html'
    success_url = '/certificados'

    def form_valid(self, form):
        certificate = get_object_or_404(Certificate, id=self.kwargs['pk'])
        certificate.invalidated = True
        certificate.invalidated_reason = self.request.POST['reason']
        certificate.save()
        print(certificate)

        return super(CertificateInvalidate, self).form_valid(form)


class CertificateDelete(LoginRequiredMixin, DeleteView):
    model = Certificate
    context_object_name = 'certificate'
    template_name = 'core/certificate/confirm_delete.html'
    success_url = '/certificados'


class CertificateValidate(LoginRequiredMixin, View):

    def get(self, request, validation_code):
        try:
            certificate = Certificate.objects.get(
                validation_code__startswith=validation_code)
            context = {'certificate': certificate}
        except Certificate.DoesNotExist:
            context = {'validation_code': validation_code}


        return render(request, 'core/certificate/validate.html', context)
