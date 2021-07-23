from django.urls import path
from . import views
from .views import (PostListView, PostListViewUser, PostUpdateView, PostDeleteView)

urlpatterns = [
    path('review/', views.fill_form, name="review"),
    path('reviews/', PostListViewUser.as_view(), name="my-reviews"),
    path('reviews/allreviews/', PostListView.as_view(), name="all-reviews"),

    path('reviews/<int:pk>/update/', PostUpdateView.as_view(), name="review-update"),
    path('reviews/<int:pk>/delete/', PostDeleteView.as_view(), name="review-delete")
]
