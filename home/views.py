from django.shortcuts import render, redirect
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


def register(request):
    if request.user.is_authenticated:
        return redirect('main_page')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Created Account for {username}')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})