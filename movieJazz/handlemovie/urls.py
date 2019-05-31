from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'handlemovie'
urlpatterns = [
    path('/', views.movies, name = 'movies'),
    path('/<int:movieId>', views.specificMovie, name='specificMovie'),
    path('/search', views.search, name = 'search'),
    path('/<int:movie_id>/review', views.review, name = 'review')
]