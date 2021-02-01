from django.shortcuts import render
from django.views import View
from django.conf import settings


def error_403(request, exception=None):
    return render(request, 'home/403.html')


def error_404(request, exception):
    return render(request, "home/404.html", {})


def error_500(request, exception=None):
    return render(request, "home/500.html", {})


class HomeView(View):
    def get(self, request):
        print(request.get_host())
        host = request.get_host()
        islocal = host.find('localhost') >= 0 or host.find('127.0.0.1') >= 0
        context = {
            'installed': settings.INSTALLED_APPS,
            'islocal': islocal
        }
        return render(request, 'home/start.html', context)
