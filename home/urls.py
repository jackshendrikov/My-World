from django.conf.urls import url
from django.urls import path, include
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.main_page, name="main_page"),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),

    path('intro/', TemplateView.as_view(template_name='home/home/intro.html'), name='intro'),
    path('home/', TemplateView.as_view(template_name='home/home/main.html'), name='home_page'),

    path('home/concentus', TemplateView.as_view(template_name='home/concentus/index.html'), name='concentus'),
    path('home/constellation', TemplateView.as_view(template_name='home/constellation/index.html'), name='constellation'),
    path('home/expressionism', TemplateView.as_view(template_name='home/expressionism/index.html'), name='expressionism'),
    path('home/expressionism2', TemplateView.as_view(template_name='home/expressionism2/index.html'), name='expressionism2'),
    path('home/fractal', TemplateView.as_view(template_name='home/fractal/index.html'), name='fractal'),
    path('home/galaxy', TemplateView.as_view(template_name='home/galaxy/index.html'), name='galaxy'),
    path('home/heartverse', TemplateView.as_view(template_name='home/heartverse/index.html'), name='heartverse'),
    path('home/infinity', TemplateView.as_view(template_name='home/infinity/index.html'), name='infinity'),
    path('home/neon', TemplateView.as_view(template_name='home/neon/index.html'), name='neon'),
    path('home/phoenix', TemplateView.as_view(template_name='home/phoenix/index.html'), name='phoenix'),
    path('home/psychedelic', TemplateView.as_view(template_name='home/psychedelic/index.html'), name='psychedelic'),
    path('home/spirals', TemplateView.as_view(template_name='home/spirals/index.html'), name='spirals'),
    path('home/whirlpool', TemplateView.as_view(template_name='home/whirlpool/index.html'), name='whirlpool'),
    path('home/secret', views.secret, name='secret'),

    path('home/xmas-tree', TemplateView.as_view(template_name='home/xmas-tree/index.html'), name='xmas-home'),
    path('home/xmas-tree/intro', TemplateView.as_view(template_name='home/xmas-tree/intro.html'), name='xmas-intro'),
    path('home/xmas-tree/xmas-scene', TemplateView.as_view(template_name='home/xmas-tree/xmas-scene/index.html'), name='xmas-scene'),
    path('home/xmas-tree/xmas-special', TemplateView.as_view(template_name='home/xmas-tree/xmas-special/index.html'), name='xmas-special'),
    path('home/xmas-tree/xmas-game', TemplateView.as_view(template_name='home/xmas-tree/xmas-game/index.html'), name='xmas-game'),
]

