from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth

# Create your views here.
@login_required
def home(request):
    return HttpResponse('logged in')


def login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        context = {
            'form': form
        }
        return render(request, 'core/login.html', context)
    else:
        form = AuthenticationForm(request.POST)
        user = auth.authenticate(username=request.POST['username'],
                                 password=request.POST['password'])

        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponse('not authenticate')
