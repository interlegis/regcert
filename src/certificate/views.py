from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView, FormView
from django.utils.decorators import method_decorator

from certificate.models import Certificate, InvalidCertificate
from certificate.forms import InvalidateCertificateForm, SearchCertificateForm


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


class CertificateList(LoginRequiredMixin, ListView):
    model = Certificate
    context_object_name = 'certificates'
    template_name = 'certificate/list_certificates.html'


class CertificateCreate(LoginRequiredMixin, CreateView):
    model = Certificate
    template_name = 'certificate/create_certificate.html'
    success_url = reverse_lazy('certificate_list')
    fields = ['certificate_number', 'book_number', 'book_sheet', 'book_date',
              'process_number', 'executive_director', 'educational_secretary',
              'course_name', 'course_duration', 'course_start_date',
              'course_end_date', 'student_name', 'student_birthday',
              'student_nationality', 'student_rg']


class CertificateDetail(LoginRequiredMixin, ListView):
    context_object_name = 'certificate'
    template_name = 'certificate/detail_certificate.html'

    def get_queryset(self):
        certificate = get_object_or_404(Certificate, id=self.kwargs['pk'])
        return certificate


class CertificateValidate(View):

    def get(self, request, verification_code):
        try:
            certificate = Certificate.objects.get(
                verification_code=verification_code)
            context = {'certificate': certificate}
        except Certificate.DoesNotExist:
            context = {'verification_code': verification_code}

        return render(request, 'certificate/validate_certificate.html',
                      context)


class CertificateInvalidate(LoginRequiredMixin, FormView):
    form_class = InvalidateCertificateForm
    template_name = 'certificate/invalidate_certificate.html'
    success_url = reverse_lazy('certificate_list')

    def get_context_data(self, **kwargs):
        context = super(CertificateInvalidate, self).get_context_data(**kwargs)
        context['certificate'] = Certificate.objects.get(id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        certificate = get_object_or_404(Certificate, id=self.kwargs['pk'])
        invalid_certificate = InvalidCertificate()

        fields = certificate._meta.fields
        for field in fields:
            value = getattr(certificate, field.name)
            setattr(invalid_certificate, field.name, value)

        invalid_certificate.invalidated_reason = self.request.POST['reason']

        invalid_certificate.save()
        certificate.delete()

        return super(CertificateInvalidate, self).form_valid(form)


class CertificateSearch(LoginRequiredMixin, View):

    def get(self, request):

        form = SearchCertificateForm(request.GET)

        context = {}
        context['form'] = form

        if form.is_valid():
            data = form.cleaned_data
            if data['search_options'] == 'name':
                context['by_name'] = Certificate.objects.filter(
                    student_name__startswith=data['search_text'])
                if not len(context['by_name']):
                    context['invalid'] = True
            else:
                context['by_verification_code'] = Certificate.objects.filter(
                    verification_code=data['search_text'])
                if not len(context['by_verification_code']):
                    context['invalid'] = True

        return render(request, 'certificate/search_certificate.html', context)
