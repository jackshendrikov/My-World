from django.urls import path
from . import views

app_name = 'cypher'
urlpatterns = [
    path('caesar-cipher/', views.caesar, name='caesar'),
    path('atbash-cipher/', views.atbash, name='atbash')
]
