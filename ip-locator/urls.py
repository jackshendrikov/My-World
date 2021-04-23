from django.urls import path
from . import views

app_name = 'iplocator'
urlpatterns = [
    path('', views.index, name='iplocator')
]
