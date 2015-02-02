from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View


from certificate.forms import ValidateCertificateForm


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
