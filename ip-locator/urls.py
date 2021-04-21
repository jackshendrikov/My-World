from django.urls import path
from . import views

app_name = 'ip-locator'
urlpatterns = [
    path('', views.index)
]
