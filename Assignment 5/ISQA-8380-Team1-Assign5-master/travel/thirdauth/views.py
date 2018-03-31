from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *


def authentication(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                        password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    #return HttpResponse('Authenticated ' \
                     #       'successfully')
                    return HttpResponseRedirect('/home/')
            else:
                return HttpResponse('Disabled account')

        else:
            return HttpResponse('Invalid login')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})


def logout_self(request):
    logout(request)
    return render(request, 'registration/logout.html')