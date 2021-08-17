from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib import messages
from .forms import UserRegisterForm


def error_403(request, exception=None):
    return render(request, 'home/home/403.html')


def error_404(request, exception):
    return render(request, "home/home/404.html", {})


def error_500(request, exception=None):
    return render(request, "home/home/500.html", {})


def main_page(request):
    return render(request, 'home/home/start.html')


def secret(request):
    return HttpResponseRedirect('https://youtu.be/dQw4w9WgXcQ')


def register(request):
    if request.user.is_authenticated:
        return redirect('home_page')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'],)
            login(request, new_user)

            default_group = Group.objects.get(name='Whispering Vision')
            default_group.user_set.add(new_user)

            messages.success(request, f'Thanks for registering. You are now logged in.')
            return redirect('home_page')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})
