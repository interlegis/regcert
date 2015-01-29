from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, View
from django.views.generic.edit import (CreateView, FormView, UpdateView,
                                      DeleteView)
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.db import IntegrityError

from core.forms import (InvalidateCertificateForm, ValidateCertificateForm,
                       SearchCertificateForm, CertificateCreateForm)
from core.models import Certificate, Course, Enrollment, Student


class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class Home(View):

    def get(self, request):
        return render(request, 'core/home.html',
            {'form': ValidateCertificateForm})

    def post(self, request):
        form = ValidateCertificateForm(request.POST)
        if form.is_valid():
            verification_code = form.cleaned_data['verification_code']

            return HttpResponseRedirect('/certificados/validar/{}'.format(
                verification_code))
        else:
            return render(request, 'core/home.html', {'form': form})


class StudentView(LoginRequiredMixin, ListView):
    model = Student
    context_object_name = 'students'
    paginate_by = 10
    template_name = 'core/student/list.html'


class StudentCreate(LoginRequiredMixin, CreateView):
    model = Student
    success_url = '/alunos'
    template_name = 'core/student/create.html'


class StudentUpdate(LoginRequiredMixin, UpdateView):
    model = Student
    success_url = '/alunos'
    template_name = 'core/student/edit.html'


class CourseView(LoginRequiredMixin, ListView):
    model = Course
    context_object_name = 'courses'
    template_name = 'core/course/list.html'


class CourseCreate(LoginRequiredMixin, CreateView):
    model = Course
    success_url = '/cursos'
    template_name = 'core/course/create.html'


class CourseUpdate(LoginRequiredMixin, UpdateView):
    model = Course
    success_url = '/cursos'
    template_name = 'core/course/edit.html'


class CertificateView(LoginRequiredMixin, ListView):
    model = Certificate
    queryset = Certificate.objects.filter(invalidated=False)
    context_object_name = 'certificates'
    template_name = 'core/certificate/list.html'


class CertificateCreate(LoginRequiredMixin, FormView):
    form_class = CertificateCreateForm
    template_name = 'core/certificate/create.html'
    success_url = '/certificados'

    def form_valid(self, form):
        try:
            form.save()
        except Student.DoesNotExist:
            form.add_error('student_rg', _('student not registered.'))
            return super(CertificateCreate, self).form_invalid(form)

        except Course.DoesNotExist:
            form.add_error('course', _('course not registered.'))
            return super(CertificateCreate, self).form_invalid(form)

        except IntegrityError:
            form.add_error('enrollment', _('enrollment already exists.'))
            return super(CertificateCreate, self).form_invalid(form)

        return super(CertificateCreate, self).form_valid(form)


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


    def get_context_data(self, **kwargs):
        context = super(CertificateInvalidate, self).get_context_data(**kwargs)
        context['certificate'] = Certificate.objects.get(id=self.kwargs['pk'])
        return context


    def form_valid(self, form):
        certificate = get_object_or_404(Certificate, id=self.kwargs['pk'])
        certificate.invalidated = True
        certificate.invalidated_reason = self.request.POST['reason']
        certificate.save()

        return super(CertificateInvalidate, self).form_valid(form)


class CertificateValidate(View):

    def get(self, request, verification_code):
        try:
            certificate = Certificate.objects.get(
                verification_code=verification_code)
            context = {'certificate': certificate}
        except Certificate.DoesNotExist:
            context = {'verification_code': verification_code}

        return render(request, 'core/certificate/validate.html', context)


class CertificateSearch(LoginRequiredMixin, View):

    def get(self, request):

        form = SearchCertificateForm(request.GET)

        context = {}
        context['form'] = form

        if form.is_valid():
            data  = form.cleaned_data
            if data['search_options'] == 'name':
                context['by_name'] = Certificate.objects.filter(
                    enrollment__student__name=data['search_text'])
                if not len(context['by_name']):
                    context['invalid'] = True
            else:
                context['by_verification_code'] = Certificate.objects.filter(
                    verification_code__startswith=data['search_text'])
                if not len(context['by_verification_code']):
                    context['invalid'] = True


        return render(request, 'core/certificate/search.html', context)
