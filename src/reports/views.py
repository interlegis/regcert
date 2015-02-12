from easy_pdf.views import PDFTemplateView

from certificate.models import Certificate


class ReportAllCertificates(PDFTemplateView):
    template_name = 'reports/all_certificates.html'

    def get_context_data(self, **kwargs):
        context = super(ReportAllCertificates, self).get_context_data(
            pagesize="A4",
            title="Hi there!",
            **kwargs)
        context['certificates'] = Certificate.objects.all()
        return context
