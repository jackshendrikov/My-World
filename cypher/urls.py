from django.urls import path
from . import views

app_name = 'cypher'
urlpatterns = [
    path('', views.caesar, name='caesar')
]
