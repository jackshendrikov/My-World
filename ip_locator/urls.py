from django.urls import path
from . import views

app_name = 'ip_locator'
urlpatterns = [
    path('', views.index, name='ip_locator')
]
