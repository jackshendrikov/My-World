from django.urls import path
from . import views

app_name = 'cypher'
urlpatterns = [
    path('', views.cypher_main,  name="cypher-main"),
    path('affine-cipher/', views.affine, name='affine'),
    path('caesar-cipher/', views.caesar, name='caesar'),
    path('atbash-cipher/', views.atbash, name='atbash'),
    path('bacon-cipher/', views.bacon, name='bacon'),
    path('polybius-cipher/', views.polybius, name='polybius'),
    path('rot13-cipher/', views.rot13, name='rot13'),
]
