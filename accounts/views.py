from django.contrib.auth import authenticate, logout as do_logout 
from django.contrib.auth import login as do_login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse

from .forms import LoginForm

# Create your views here.
def login(request):
    if not request.user.is_authenticated:
        form = LoginForm()
        
        if request.method == 'POST': 
            form = LoginForm(data=request.POST)

            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                
                user = authenticate(username=username, password=password)
                if user is not None:
                    do_login(request, user)
                    return HttpResponseRedirect(reverse('easycomb_theme:index'))

        return render(request, 'accounts/login.html', {'form': form})
    else:
        return HttpResponseRedirect(reverse('easycomb_theme:index'))

def logout(request):
    if request.user.is_authenticated:
        do_logout(request)
        return HttpResponseRedirect(reverse('accounts:login'))
