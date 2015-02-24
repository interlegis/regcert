#! coding: utf-8
from itertools import chain

from easy_pdf.views import PDFTemplateView

from certificate.models import Certificate, InvalidCertificate


class ReportAllValidCertificates(PDFTemplateView):
    template_name = 'reports/all_certificates.html'

    def get_context_data(self, **kwargs):
        context = super(ReportAllValidCertificates, self).get_context_data(
            pagesize="A4",
            title="Hi there!",
            **kwargs)
        context['certificates'] = Certificate.objects.all()
        context['title'] = u'Relatório Regcert: todos os certificados \
                            cadastrados'
        return context


class ReportAllCertificates(PDFTemplateView):
    template_name = 'reports/all_certificates.html'

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


class ReportCertificatesByCourse(PDFTemplateView):
    template_name = 'reports/all_certificates.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not context['certificates']:
            return HttpResponseNotFound('<h1>Page not found</h1>')
        return self.render_to_response(context)

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
