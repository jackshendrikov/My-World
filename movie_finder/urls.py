from django.urls import include, path
from django.views.generic import TemplateView

from . import views

app_name = 'movie-finder'
urlpatterns = [
    path('', views.main_page, name="movies-main"),
    path('', include("users.urls")),

    path('specials/', TemplateView.as_view(template_name='movie_finder/specials.html'), name='specials'),
    path('genres/', TemplateView.as_view(template_name='movie_finder/genres.html'), name='genres'),
    path('watchlist/', views.watchlist, name="watchlist"),
    path('genre/', views.genre, name='genre'),
    path('popular/', views.popular, name='popular'),

    path('series/', views.all_series, name='series'),
    path('xmas-category/', views.xmas, name='xmas-category'),
    path('top/', views.top_movies, name='top100'),
    path('netflix/', views.netflix, name='netflix'),

    path('search/', views.movie_search, name='movie-search'),
    path('advsearch/', views.advanced_search, name='advanced-search'),

    path('intro/', views.show_intro, name='show-intro'),
    path('movie-info/<str:movie_id>/', views.result_page, name='result'),
]
