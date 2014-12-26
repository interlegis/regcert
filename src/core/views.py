from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return HttpResponse('login')
