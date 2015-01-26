from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import ListView, View
from django.views.generic.edit import (CreateView, FormView, UpdateView,
                                      DeleteView)
from django.utils.decorators import method_decorator

from core.forms import (InvalidateCertificateForm, ValidateCertificateForm,
                       SearchCertificateForm)
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
            validation_code = form.cleaned_data['validation_code']

            return HttpResponseRedirect('/certificados/validar/{}'.format(
                validation_code))
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


    def get_context_data(self, **kwargs):
        context = super(CertificateInvalidate, self).get_context_data(**kwargs)
        context['certificate'] = Certificate.objects.get(id=self.kwargs['pk'])
        return context


    def form_valid(self, form):
        certificate = get_object_or_404(Certificate, id=self.kwargs['pk'])
        certificate.invalidated = True
        certificate.invalidated_reason = self.request.POST['reason']
        certificate.save()
        print(certificate)

        return super(CertificateInvalidate, self).form_valid(form)


class CertificateValidate(View):

    def get(self, request, validation_code):
        try:
            certificate = Certificate.objects.get(
                validation_code__startswith=validation_code)
            context = {'certificate': certificate}
        except Certificate.DoesNotExist:
            context = {'validation_code': validation_code}

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
                context['by_validation_code'] = Certificate.objects.filter(
                    validation_code__startswith=data['search_text'])
                if not len(context['by_validation_code']):
                    context['invalid'] = True


        return render(request, 'core/certificate/search.html', context)
