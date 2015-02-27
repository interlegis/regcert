#! coding: utf-8
from itertools import chain

from django.http import HttpResponseNotFound
from django.views.generic import View
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from easy_pdf.views import PDFTemplateView

from certificate.models import Certificate, InvalidCertificate


class PDFGenerator(PDFTemplateView):

    template_name = 'reports/report.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not context['certificates']:
            return HttpResponseNotFound('<h1>Page not found</h1>')
        return self.render_to_response(context)


class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class ReportsView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'reports/reports.html', {})


class ReportAllValidCertificates(LoginRequiredMixin, PDFGenerator):

    def get_context_data(self, **kwargs):
        context = super(ReportAllValidCertificates, self).get_context_data(
            pagesize="A4",
            title="Hi there!",
            **kwargs)
        context['certificates'] = Certificate.objects.all()
        context['title'] = u'Relatório Regcert: todos os certificados \
                            cadastrados'
        return context


class ReportAllCertificates(LoginRequiredMixin, PDFGenerator):

    def get_context_data(self, **kwargs):
        context = super(ReportAllCertificates, self).get_context_data(
            pagesize="A4",
            title="Hi there!",
            **kwargs)
        valid_certificates = Certificate.objects.order_by('book_number')
        invalid_certificates = InvalidCertificate.objects.order_by(
            'book_number')
        all_certificates = chain(valid_certificates, invalid_certificates)
        context['has_invalid_certificates'] = True
        context['certificates'] = sorted(all_certificates,
                                         key=lambda c: c.book_number)
        context['title'] = u'Relatório Regcert: todos os certificados \
                            cadastrados e anulados'
        return context


class ReportCertificatesByCourse(LoginRequiredMixin, PDFGenerator):

    def get_context_data(self, **kwargs):
        context = super(ReportCertificatesByCourse, self).get_context_data(
            pagesize="A4",
            title="Hi there!",
            **kwargs)
        course_name = kwargs['course_name'].replace('-', ' ')
        context['certificates'] = Certificate.objects.filter(
            course_name=course_name)
        context['title'] = u'Relatório Regcert: todos os certificados do \
                             curso de pós-graduação lato sensu em {} \
                             do ILB'.format(course_name)
        return context


class ReportCertificatesByDate(LoginRequiredMixin, PDFGenerator):

    def get_context_data(self, **kwargs):
        context = super(ReportCertificatesByDate, self).get_context_data(
            pagesize="A4",
            title="Hi there!",
            **kwargs)

        # must be a better way to do it
        _date = [int(d) for d in reversed(kwargs['date'].split('-'))]
        context['certificates'] = Certificate.objects.filter(
            verification_code_date_time__year=_date[0],
            verification_code_date_time__month=_date[1],
            verification_code_date_time__day=_date[2])
        context['title'] = u'Relatório Regcert: todos os certificados \
                             cadastrados no sistema em {}/{}/{}.'.format(
            _date[2],
            _date[1],
            _date[0]
        )
        return context


class ReportCertificatesByBookDate(LoginRequiredMixin, PDFGenerator):

    def get_context_data(self, **kwargs):
        context = super(ReportCertificatesByBookDate, self).get_context_data(
            pagesize="A4",
            title="Hi there!",
            **kwargs)

        # must be a better way to do it
        _date = [int(d) for d in reversed(kwargs['date'].split('-'))]
        context['certificates'] = Certificate.objects.filter(
            book_date__year=_date[0],
            book_date__month=_date[1],
            book_date__day=_date[2])
        context['title'] = u'Relatório Regcert: todos os certificados \
                             registrados no Livro de Registro Escolar do ILB \
                             em {}/{}/{}.'.format(_date[2], _date[1], _date[0])
        return context


class ReportCertificatesByStudent(LoginRequiredMixin, PDFGenerator):

    def get_context_data(self, **kwargs):
        context = super(ReportCertificatesByStudent, self).get_context_data(
            pagesize="A4",
            title="Hi there!",
            **kwargs)
        student_name = kwargs['student_name'].replace('-', ' ')
        context['certificates'] = Certificate.objects.filter(
            student_name=student_name)
        context['title'] = u'Relatório Regcert: todos os certificados de {} \
                             emitidos pelo ILB'.format(student_name)
        context['student_report'] = True
        return context
